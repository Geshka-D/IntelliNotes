from fastapi import APIRouter, UploadFile, File
from backend.services.audio_service import transcribe_audio
from backend.services.text_service import generate_summary
from backend.db import crud

router = APIRouter()

@router.post("/upload")
async def upload_lecture(file: UploadFile = File(...)):
    """
    Upload an audio file, transcribe and summarize it, and save a note.
    Returns note id and summary.
    """
    text = await transcribe_audio(file)
    summary = generate_summary(text)
    nid = crud.create_note(title=file.filename, content=text, summary=summary)
    return {"note_id": nid, "summary": summary}
