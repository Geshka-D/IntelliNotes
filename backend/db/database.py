from pathlib import Path
from typing import Iterable, Tuple

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.db import db_models

# Base directory relative to this file.
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "data"
DB_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DB_DIR / "lecture_notes.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _ensure_note_columns() -> None:
    """Best-effort schema upgrade for existing SQLite files."""
    migrations: Iterable[Tuple[str, str]] = (
        ("language", "TEXT"),
        ("status", "TEXT DEFAULT 'ready'"),
        ("audio_path", "TEXT"),
        ("payload", "JSON"),
        ("created_at", "DATETIME DEFAULT (CURRENT_TIMESTAMP)"),
        ("updated_at", "DATETIME DEFAULT (CURRENT_TIMESTAMP)"),
    )
    with engine.begin() as conn:
        table_exists = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='notes'")
        ).fetchone()
        if not table_exists:
            return
        info = conn.execute(text("PRAGMA table_info(notes)")).fetchall()
        existing = {row[1] for row in info}
        for column_name, ddl in migrations:
            if column_name not in existing:
                conn.execute(text(f"ALTER TABLE notes ADD COLUMN {column_name} {ddl}"))



def init_db() -> None:
    """
    Initialize database schema.
    Creates tables and fills missing columns for existing SQLite files.
    """
    _ensure_note_columns()
    db_models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
