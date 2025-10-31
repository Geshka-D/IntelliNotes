from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "System Audio Recorder API"
    chunk_size: int = 512
    recordings_dir: str = "recordings"
    max_recording_duration: Optional[int] = None

    # Allow unrelated NLP env vars from the shared .env file.
    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
