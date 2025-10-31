from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from backend.api.schemas.note_schema import NoteDetail, NoteListResponse
from backend.db import database
from backend.services import note_service

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/", response_model=NoteListResponse)
def list_notes(db: Session = Depends(database.get_db)):
    items = note_service.list_notes(db)
    return {"items": items, "count": len(items)}


@router.get("/{note_id}", response_model=NoteDetail)
def get_note(note_id: int, db: Session = Depends(database.get_db)):
    note = note_service.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(database.get_db)):
    deleted = note_service.delete_note(db, note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return Response(status_code=204)
