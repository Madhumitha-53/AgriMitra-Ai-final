try:
    from faster_whisper import WhisperModel
except ImportError:  # pragma: no cover - handled at runtime
    WhisperModel = None


LANGUAGE_MAP = {
    "ta": "Tamil",
    "te": "Telugu",
    "hi": "Hindi",
    "en": "English",
    "kn": "Kannada",
    "ml": "Malayalam"
}


def _get_model():
    if WhisperModel is None:
        raise RuntimeError("faster-whisper is not installed. Install it to enable speech-to-text.")

    return WhisperModel(
        "small",
        device="cpu",
        compute_type="int8"
    )


def speech_to_text(audio_file):
    if not audio_file:
        return {
            "text": "",
            "language": "en",
            "language_name": "English"
        }

    model = _get_model()

    segments, info = model.transcribe(
        audio_file,
        beam_size=5,
        vad_filter=True,
        condition_on_previous_text=False
    )

    text = ""
    for segment in segments:
        text += segment.text + " "

    language = getattr(info, "language", None) or "en"

    return {
        "text": text.strip(),
        "language": language,
        "language_name": LANGUAGE_MAP.get(language, "English")
    }