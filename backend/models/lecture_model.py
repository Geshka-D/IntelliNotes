from pydantic import BaseModel
from typing import Optional

class Lecture(BaseModel):
    id: int
    filename: str
    duration: Optional[float] = None
    uploaded_at: Optional[str] = None
