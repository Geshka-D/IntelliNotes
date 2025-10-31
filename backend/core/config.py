from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "System Audio Recorder API"
    chunk_size: int = 512
    recordings_dir: str = "recordings"
    max_recording_duration: Optional[int] = None

    class Config:
        env_file = ".env"
    
settings = Settings()