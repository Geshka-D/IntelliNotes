from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.api.schemas.note_schema import NoteCreateText, NoteDetail, NoteProcessRecording
from backend.core.config import settings
from backend.db import database
from backend.services import note_service

router = APIRouter(prefix="/lectures", tags=["Lectures"])


@router.post("/upload", response_model=NoteDetail)
async def create_from_upload(
    title: str = Form(default=""),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
):
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")
    created = note_service.create_note_from_file(
        db,
        filename=file.filename,
        contents=contents,
        title=title or None,
    )
    return note_service.get_note(db, created.id)


@router.post("/text", response_model=NoteDetail)
def create_from_text(payload: NoteCreateText, db: Session = Depends(database.get_db)):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text content is empty")
    created = note_service.create_note_from_text(
        db,
        title=payload.title,
        text=payload.text,
    )
    return note_service.get_note(db, created.id)


@router.post("/process-recording", response_model=NoteDetail)
def process_recording(
    payload: NoteProcessRecording,
    db: Session = Depends(database.get_db),
):
    recordings_dir = Path(settings.recordings_dir).resolve()
    recording_path = (recordings_dir / payload.filename).resolve()
    try:
        recording_path.relative_to(recordings_dir)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid recording filename")
    if not recording_path.exists():
        raise HTTPException(status_code=404, detail="Recording file not found")
    created = note_service.create_note_from_existing_path(
        db,
        path=recording_path,
        title=payload.title or recording_path.stem,
    )
    return note_service.get_note(db, created.id)
