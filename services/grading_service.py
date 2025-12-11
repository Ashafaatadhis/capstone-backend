from utils.video import extract_audio
from utils.whisper_local import transcribe_audio
from utils.speech_analysis import analyze_speech_segments, calculate_wpm
from services.scoring_service import ScoringService
from sqlmodel import Session
from database import engine
from models.question import Question
from models.rubric import Rubric
from config import GROQ_API_KEY


class GradingService:

    @staticmethod
    def process_video(video_path: str, question_id: int):
        # 1. Extract audio
        audio_path = extract_audio(video_path)

        # 2. Transcribe with Whisper
        transcribed = transcribe_audio(audio_path)
        segments = transcribed["segments"]
        transcript = transcribed["text"]

        # 3. Speech analysis
        speech_stats = analyze_speech_segments(segments)
        wpm = calculate_wpm(transcript, speech_stats["total_speech_time"])

        # 4. Ambil 1 pertanyaan + rubrik dari DB
        with Session(engine) as session:
            q = session.get(Question, question_id)
            if not q:
                raise Exception("Question not found")

            rubrics = session.query(Rubric).filter(Rubric.question_id == question_id).all()

            formatted_rubrics = [
                {"score": r.score, "description": r.description}
                for r in rubrics
            ]

        # 5. Ambil jawaban lengkap (tanpa split multiple answers)
        answer_text = transcript  # 1 video = 1 answer

        scorer = ScoringService(GROQ_API_KEY)

        # 6. LLM grading
        llm_score = scorer.score_answer(
            q.text,
            answer_text,
            formatted_rubrics
        )

        # 7. Final output
        return {
            "question_id": q.id,
            "question": q.text,
            "answer": answer_text,
            "llm_result": llm_score,
            "transcript": transcript,
            "speech_analysis": {
                "wpm": wpm,
                **speech_stats
            }
        }
