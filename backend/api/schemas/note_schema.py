from pydantic import BaseModel
from typing import Optional

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteOut(BaseModel):
    id: int
    title: str
    summary: Optional[str]
    content: Optional[str]
