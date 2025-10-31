from pathlib import Path
from typing import Iterator

from fastapi import APIRouter, HTTPException, Path as PathParam
from fastapi.responses import FileResponse, StreamingResponse

from backend.api.schemas.record_schema import (
    DeviceInfo,
    RecordingInfo,
    RecordingResponse,
    RecordingStatus,
    RecordingsList,
)
from backend.core.config import settings
from backend.services.record_service import recorder_service

router = APIRouter(prefix="/recording", tags=["Recordings"])


def _recordings_dir() -> Path:
    path = Path(settings.recordings_dir).resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


@router.post("/start", response_model=RecordingResponse)
async def start_recording():
    result = recorder_service.start_recording()
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@router.post("/stop", response_model=RecordingResponse)
async def stop_recording():
    result = recorder_service.stop_recording()
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@router.get("/status", response_model=RecordingStatus)
async def get_recording_status():
    return recorder_service.get_status()


@router.get("/info", response_model=DeviceInfo)
async def get_device_info():
    device_info = recorder_service.get_device_info()
    if not device_info:
        raise HTTPException(status_code=404, detail="Loopback device is unavailable.")
    return device_info


@router.get("/list", response_model=RecordingsList)
async def list_recordings():
    try:
        recordings_dir = _recordings_dir()
        items = []
        for file_path in recordings_dir.glob("*.wav"):
            stat = file_path.stat()
            items.append(
                RecordingInfo(
                    filename=file_path.name,
                    size=stat.st_size,
                    created_at=stat.st_ctime,
                    url=f"/recordings/{file_path.name}",
                )
            )
        items.sort(key=lambda x: x.created_at, reverse=True)
        return RecordingsList(recordings=items, count=len(items))
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def _resolve_recording(filename: str) -> Path:
    recordings_dir = _recordings_dir()
    file_path = (recordings_dir / filename).resolve()
    try:
        file_path.relative_to(recordings_dir)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid recording filename.")
    if file_path.suffix.lower() != ".wav":
        raise HTTPException(status_code=400, detail="Only WAV recordings are supported.")
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Recording not found.")
    return file_path


@router.get("/{filename}")
async def get_recording(filename: str = PathParam(..., description="Recording filename")):
    file_path = _resolve_recording(filename)
    return FileResponse(path=str(file_path), media_type="audio/wav", filename=file_path.name)


@router.get("/{filename}/stream")
async def stream_recording(filename: str = PathParam(..., description="Recording filename")):
    file_path = _resolve_recording(filename)

    def iterfile() -> Iterator[bytes]:
        with open(file_path, "rb") as fh:
            while chunk := fh.read(4096):
                yield chunk

    return StreamingResponse(iterfile(), media_type="audio/wav")


@router.delete("/{filename}", response_model=RecordingResponse)
async def delete_recording(filename: str = PathParam(..., description="Recording filename")):
    file_path = _resolve_recording(filename)
    file_path.unlink(missing_ok=False)
    return {
        "status": "success",
        "message": f"Recording {file_path.name} deleted.",
        "filename": file_path.name,
    }
