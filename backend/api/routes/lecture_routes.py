from backend.services.audio_service import transcribe_audio
from backend.services.text_service import generate_summary
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from backend.db import db_models, database
from backend.api.schemas.lecture_schema import LectureIn
from backend.api.schemas.note_schema import NoteOut


router = APIRouter(prefix="/lectures", tags=["Lectures"])


@router.post("/", response_model=NoteOut)
async def create_note(note: LectureIn, db: Session = Depends(database.get_db), file: UploadFile = File(...)):
    text = await transcribe_audio(file)
    summary = generate_summary(text)
    new_note = db_models.Note(title=note.title, content=text, summary=summary)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note
