import whisper
from config import WHISPER_MODEL


# Load model sekali di awal (lebih cepat)
_model = whisper.load_model(WHISPER_MODEL)


def transcribe_audio(audio_path: str):
    """
    Transcribe audio dan mengembalikan:
    - full text transcript
    - segments (start, end, text)
    - duration
    """
 
    result = _model.transcribe(
        audio_path,
        language="en",
        task="translate",  # <--- force output to English
        verbose=False,
        word_timestamps=True,
        initial_prompt = """This interview is about:
        TensorFlow, Transfer Learning, VGG16, VGG19, Keras, MobileNet, EfficientNet,
        Conv2D, MaxPooling, image classification, neural network accuracy, model loss.
        """
    )

    transcript = result.get("text", "").strip()
    segments = result.get("segments", [])
    duration = result.get("duration")

    return {
        "text": transcript,
        "segments": segments,
        "duration": duration
    }
