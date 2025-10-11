from fastapi import APIRouter
from backend.db import crud

router = APIRouter()

@router.get("/")
def list_notes():
    """Return list of notes (id, title, summary)."""
    return crud.list_notes()

@router.get("/{note_id}")
def get_note(note_id: int):
    note = crud.get_note(note_id)
    if not note:
        return {"error": "not found"}
    return note
