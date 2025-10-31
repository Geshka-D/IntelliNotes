from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class LinkOut(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    summary: Optional[str] = None
    lang: Optional[str] = None
    source: Optional[str] = None
    term: Optional[str] = None


class NoteBase(BaseModel):
    id: int
    title: str
    summary: Optional[str] = None
    language: Optional[str] = None
    status: str = "ready"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    audio_path: Optional[str] = None
    has_transcript: bool = False
    keywords: List[str] = []
    bullets: List[str] = []
    decisions: List[str] = []
    action_items: List[str] = []
    open_questions: List[str] = []
    links: List[LinkOut] = []
    summarizer_provider: Optional[str] = None


class NoteDetail(NoteBase):
    content: Optional[str] = None


class NoteListResponse(BaseModel):
    items: List[NoteBase]
    count: int


class NoteCreateText(BaseModel):
    title: Optional[str] = None
    text: str


class NoteProcessRecording(BaseModel):
    filename: str
    title: Optional[str] = None
