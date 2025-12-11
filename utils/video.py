import ffmpeg
import os
import uuid


def extract_audio(input_video_path: str, out_dir: str = "temp_audio"):
    """
    Extract audio dari video dan convert ke .wav (mono 16kHz).
    Return path audio yang siap dipakai Whisper.
    """

    os.makedirs(out_dir, exist_ok=True)

    audio_filename = f"{uuid.uuid4().hex}.wav"
    output_audio_path = os.path.join(out_dir, audio_filename)

    (
        ffmpeg
        .input(input_video_path)
        .output(
            output_audio_path,
            format="wav",
            acodec="pcm_s16le",
            ac=1,
            ar="16000"
        )
        .overwrite_output()
        .run(quiet=True)
    )

    return output_audio_path
