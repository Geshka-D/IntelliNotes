import os

def transcribe_file(path: str) -> str:
    """
    Minimal transcription placeholder.
    Replace with Whisper/VOSK implementation later.
    """
    fname = os.path.basename(path)
    return f"Transcribed text placeholder for {fname}"
