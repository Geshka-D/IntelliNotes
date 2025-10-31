from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Optional

from sqlalchemy.orm import Session

from backend.core.config import settings
from backend.db import db_models
from backend.utils.file_utils import save_bytes_file
from nlp_engine.summarizer import make_note
from nlp_engine.transcriber import transcribe_file

NOTE_META_FIELDS: Iterable[str] = (
    "bullets",
    "decisions",
    "action_items",
    "open_questions",
    "keywords",
    "links",
    "summarizer_provider",
)


def _persist_note(
    db: Session,
    *,
    note_payload: Dict,
    title: Optional[str],
    audio_path: Optional[str],
) -> db_models.Note:
    content = note_payload.get("content", "") or ""
    summary = note_payload.get("summary") or ""
    language = note_payload.get("language")

    payload = {
        key: note_payload.get(key)
        for key in NOTE_META_FIELDS
        if note_payload.get(key) not in (None, [], {})
    }

    note = db_models.Note(
        title=title or note_payload.get("title") or "Untitled note",
        content=content,
        summary=summary,
        language=language,
        status="ready",
        audio_path=audio_path,
        payload=payload,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def create_note_from_text(
    db: Session,
    *,
    title: Optional[str],
    text: str,
    audio_path: Optional[str] = None,
) -> db_models.Note:
    note_payload = make_note(text, title=title)
    return _persist_note(db, note_payload=note_payload, title=title, audio_path=audio_path)


def create_note_from_file(
    db: Session,
    *,
    filename: str,
    contents: bytes,
    title: Optional[str] = None,
    upload_dir: str = "data/uploads",
) -> db_models.Note:
    saved_path = Path(save_bytes_file(contents, filename, folder=upload_dir))
    return create_note_from_existing_path(
        db, path=saved_path, title=title or saved_path.stem
    )


def create_note_from_existing_path(
    db: Session,
    *,
    path: Path,
    title: Optional[str] = None,
) -> db_models.Note:
    path = path.resolve()
    transcript = transcribe_file(str(path))
    relative_audio_path: Optional[str] = None
    recordings_dir = Path(settings.recordings_dir).resolve()
    try:
        relative_audio_path = str(path.relative_to(recordings_dir))
    except ValueError:
        # File is outside recordings directory; keep absolute path for reference.
        relative_audio_path = str(path)
    return create_note_from_text(
        db,
        title=title or path.stem,
        text=transcript,
        audio_path=relative_audio_path,
    )


def serialize_note(note: db_models.Note, *, include_content: bool = False) -> Dict:
    payload = note.payload or {}
    data: Dict = {
        "id": note.id,
        "title": note.title,
        "summary": note.summary,
        "language": note.language,
        "status": note.status,
        "created_at": note.created_at.isoformat() if note.created_at else None,
        "updated_at": note.updated_at.isoformat() if note.updated_at else None,
        "audio_path": note.audio_path,
        "has_transcript": bool(note.content),
        "keywords": payload.get("keywords", []),
        "bullets": payload.get("bullets", []),
        "decisions": payload.get("decisions", []),
        "action_items": payload.get("action_items", []),
        "open_questions": payload.get("open_questions", []),
        "links": payload.get("links", []),
        "summarizer_provider": payload.get("summarizer_provider"),
    }
    if include_content:
        data["content"] = note.content
    return data


def list_notes(db: Session) -> List[Dict]:
    notes = db.query(db_models.Note).order_by(db_models.Note.created_at.desc()).all()
    return [serialize_note(note, include_content=False) for note in notes]


def get_note(db: Session, note_id: int) -> Optional[Dict]:
    note = db.query(db_models.Note).filter(db_models.Note.id == note_id).first()
    if not note:
        return None
    return serialize_note(note, include_content=True)


def delete_note(db: Session, note_id: int) -> bool:
    note = db.query(db_models.Note).filter(db_models.Note.id == note_id).first()
    if not note:
        return False
    db.delete(note)
    db.commit()
    return True
