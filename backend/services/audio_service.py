from backend.utils.file_utils import save_bytes_file
from nlp_engine.transcriber import transcribe_file

async def transcribe_audio(upload_file):
    """
    Minimal transcription service:
    - saves uploaded bytes to data/uploads/
    - calls nlp_engine.transcribe_file(file_path)
    """
    contents = await upload_file.read()
    saved_path = save_bytes_file(contents, upload_file.filename)
    text = transcribe_file(saved_path)
    return text
