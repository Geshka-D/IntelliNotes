from pydantic import BaseModel
from typing import Optional

class LectureIn(BaseModel):
    title: str
    description: Optional[str] = None
