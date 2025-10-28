from pydantic import BaseModel

class RecordingResponse(BaseModel):
    status: str
    message: str
    filename: str = None

class RecordingStatus(BaseModel):
    is_recording: bool

class DeviceInfo(BaseModel):
    name: str
    index: int
    channels: int

class RecordingInfo(BaseModel):
    filename: str
    size: int
    created_at: float
    url: str

class RecordingsList(BaseModel):
    recordings: list = []
    count: int
