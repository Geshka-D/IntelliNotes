from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import db_models, database
from backend.api.schemas.note_schema import NoteCreate, NoteOut

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post("/create", response_model=NoteOut)
def create_note(note: NoteCreate, db: Session = Depends(database.get_db)):
    new_note = db_models.Note(**note.dict())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@router.get("/read", response_model=NoteOut)
def read_note(note_id: int, db: Session = Depends(database.get_db)):
    note = db.query(db_models.Note).filter(db_models.Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note