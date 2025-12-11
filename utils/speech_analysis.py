def analyze_speech_segments(segments):
    """
    segments: list of dicts from whisper
    Returns:
        total_speech_time
        total_pause_time
        number_of_pauses
        average_pause_duration
    """

    total_speech = 0.0
    pauses = []
    last_end = None

    for seg in segments:
        start = seg["start"]
        end = seg["end"]

        # speech duration
        total_speech += (end - start)

        # pause detection
        if last_end is not None:
            pause = start - last_end
            if pause > 0.25:  # threshold untuk jeda signifikan
                pauses.append(pause)

        last_end = end

    total_pause_time = sum(pauses)
    number_of_pauses = len(pauses)
    average_pause = total_pause_time / number_of_pauses if number_of_pauses > 0 else 0

    return {
        "total_speech_time": total_speech,
        "total_pause_time": total_pause_time,
        "number_of_pauses": number_of_pauses,
        "average_pause_duration": average_pause
    }


def calculate_wpm(transcript: str, speech_seconds: float):
    words = len(transcript.split())
    minutes = speech_seconds / 60

    if minutes == 0:
        return 0

    return words / minutes
