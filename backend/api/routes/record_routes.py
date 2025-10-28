from fastapi import APIRouter, HTTPException, Path
from fastapi.responses import FileResponse, StreamingResponse
from backend.services.record_service import recorder_service
from backend.api.schemas.record_schema import (
    RecordingResponse, 
    RecordingStatus, 
    DeviceInfo,
    RecordingInfo,
    RecordingsList
)
from typing import List
import os
from backend.core.config import settings

router = APIRouter(prefix="/recording", tags=["Record"])

@router.post("/start", response_model=RecordingResponse)
async def start_recording():
    """Начать запись системного аудио"""
    result = recorder_service.start_recording()

    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])

    return result

@router.post("/stop", response_model=RecordingResponse)
async def stop_recording():
    """Остановить запись и сохранить файл"""
    result = recorder_service.stop_recording()

    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])

    return result

@router.get("/status", response_model=RecordingStatus)
async def get_recording_status():
    """Получить текущий статус записи"""
    return recorder_service.get_status()

@router.get("/info", response_model=DeviceInfo)
async def get_device_info():
    """Получить информацию о loopback устройстве"""
    device_info = recorder_service.get_device_info()

    if not device_info:
        raise HTTPException(
            status_code=404, 
            detail="Loopback устройство не найдено"
        )

    return device_info

@router.get("/list", response_model=RecordingsList)
async def list_recordings():
    """Получить список всех записей"""
    try:
        files = []
        recordings_dir = settings.recordings_dir

        if not os.path.exists(recordings_dir):
            return RecordingsList(recordings=[], count=0)

        for filename in os.listdir(recordings_dir):
            if filename.endswith('.wav'):
                filepath = os.path.join(recordings_dir, filename)
                file_stat = os.stat(filepath)

                files.append(RecordingInfo(
                    filename=filename,
                    size=file_stat.st_size,
                    created_at=file_stat.st_ctime,
                    url=f"/recordings/{filename}"
                ))

        files.sort(key=lambda x: x.created_at, reverse=True)

        return RecordingsList(recordings=files, count=len(files))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{filename}")
async def get_recording(filename: str = Path(..., description="Имя файла записи")):
    """Скачать или воспроизвести запись"""
    filepath = os.path.join(settings.recordings_dir, filename)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Файл не найден")

    if not filename.endswith('.wav'):
        raise HTTPException(status_code=400, detail="Неверный формат файла")

    return FileResponse(
        path=filepath,
        media_type="audio/wav",
        filename=filename
    )

@router.get("/{filename}/stream")
async def stream_recording(filename: str = Path(..., description="Имя файла записи")):
    """Потоковое воспроизведение записи"""
    filepath = os.path.join(settings.recordings_dir, filename)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Файл не найден")

    if not filename.endswith('.wav'):
        raise HTTPException(status_code=400, detail="Неверный формат файла")

    def iterfile():
        with open(filepath, mode="rb") as file:
            yield from file

    return StreamingResponse(iterfile(), media_type="audio/wav")

@router.delete("/{filename}", response_model=RecordingResponse)
async def delete_recording(filename: str = Path(..., description="Имя файла записи")):
    """Удалить запись"""
    filepath = os.path.join(settings.recordings_dir, filename)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Файл не найден")

    if not filename.endswith('.wav'):
        raise HTTPException(status_code=400, detail="Неверный формат файла")

    try:
        os.remove(filepath)
        return {
            "status": "success",
            "message": f"Файл {filename} успешно удален",
            "filename": filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка удаления файла: {str(e)}")