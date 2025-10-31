from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class RecordingResponse(BaseModel):
    status: str
    message: str
    filename: Optional[str] = None
    device_name: Optional[str] = None
    timestamp: Optional[str] = None

class RecordingStatus(BaseModel):
    is_recording: bool
    current_filename: Optional[str] = None
    device_name: Optional[str] = None
    started_at: Optional[str] = None
    duration_seconds: Optional[float] = None
    available: bool = True

class DeviceInfo(BaseModel):
    name: str
    index: int
    channels: int
    sample_rate: float
    is_loopback: bool

class RecordingInfo(BaseModel):
    filename: str
    size: int
    created_at: float
    url: str

class RecordingsList(BaseModel):
    recordings: List[RecordingInfo]
    count: int