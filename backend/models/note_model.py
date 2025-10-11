from pydantic import BaseModel
from typing import Optional

class Note(BaseModel):
    id: int
    title: str
    content: str
    summary: Optional[str] = None
