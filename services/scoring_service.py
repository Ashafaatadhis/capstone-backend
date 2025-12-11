from groq import Groq
import re

class ScoringService:

    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    def score_answer(self, question_text: str, answer_text: str, rubrics: list):
        """
        rubrics = [
            {"score": 4, "description": "..."},
            {"score": 3, "description": "..."},
            {"score": 2, "description": "..."},
            {"score": 1, "description": "..."},
            {"score": 0, "description": "..."}
        ]
        """

        # Build rubric section
        rubric_text = "Scoring Criteria:\n"
        for r in sorted(rubrics, key=lambda x: x["score"], reverse=True):
            rubric_text += f"\nScore {r['score']}: {r['description']}\n"

        # Construct LLM prompt (Colab-style)
        prompt = f"""
            You are an expert assessor evaluating a candidate's interview response for a Machine Learning certification.

            Interview Question:
            {question_text}

            Candidate's Response:
            {answer_text}

            {rubric_text}

            TASK: Evaluate the candidate's response and provide:
            1. A numeric score from 0-4 based on the rubric criteria.
            2. A clear, detailed reason explaining why you gave that score.

            IMPORTANT: Your response MUST follow this EXACT format:

            SCORE: [number from 0-4]
            REASON: [Your explanation referencing the rubric]

            Example:
            SCORE: 3
            REASON: The candidate explains a challenge and solution clearly but lacks technical depth.

            Now evaluate the candidate's response:
            """
        
            # Send request to Groq
        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        response_text = completion.choices[0].message.content.strip()

        # Extract SCORE and REASON using regex
        score_match = re.search(r"SCORE:\s*(\d+)", response_text, re.IGNORECASE)
        reason_match = re.search(r"REASON:\s*(.+)", response_text, re.IGNORECASE | re.DOTALL)

        if not score_match or not reason_match:
            return {
                "score": 0,
                "reason": f"Could not parse LLM output: {response_text}"
            }

        score = int(score_match.group(1))
        reason = reason_match.group(1).strip()

        # Validate range
        if score < 0 or score > 4:
            return {
                "score": 0,
                "reason": f"Invalid score ({score}) — original LLM output: {response_text}"
            }

        return {
            "score": score,
            "reason": reason
        }

    @staticmethod
    def split_answers(segments, num_questions: int, pause_threshold=2.5):
        chunks = []
        current_text = ""
        last_end = None

        for seg in segments:
            start, end, text = seg["start"], seg["end"], seg["text"]

            if last_end is not None:
                pause = start - last_end
                if pause > pause_threshold and len(chunks) < num_questions:
                    chunks.append(current_text.strip())
                    current_text = ""

            current_text += " " + text
            last_end = end

        chunks.append(current_text.strip())

        # pad if fewer chunks than questions
        while len(chunks) < num_questions:
            chunks.append("")

        return chunks[:num_questions]
