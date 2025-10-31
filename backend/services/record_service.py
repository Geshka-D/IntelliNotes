import pyaudiowpatch as pyaudio
import wave
import threading
from datetime import datetime
from typing import Optional
import time
from backend.core.config import settings

class SystemAudioRecorder:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.chunk_size = settings.chunk_size
            self.p = pyaudio.PyAudio()
            self.recording = False
            self.frames = []
            self.stream = None
            self.filename = None
            self.loopback_device = None
            self.started_at = None
            self.initialized = True

    def get_loopback_device(self) -> Optional[dict]:
        """Получить loopback устройство для записи системного аудио"""
        try:
            wasapi_info = self.p.get_host_api_info_by_type(pyaudio.paWASAPI)
        except OSError:
            return None

        default_speakers = self.p.get_device_info_by_index(
            wasapi_info["defaultOutputDevice"]
        )

        if not default_speakers["isLoopbackDevice"]:
            for loopback in self.p.get_loopback_device_info_generator():
                if default_speakers["name"] in loopback["name"]:
                    return loopback
        else:
            return default_speakers

        return None

    def get_device_info(self) -> Optional[dict]:
        """Получить информацию об устройстве"""
        device = self.get_loopback_device()
        if device:
            return {
                "name": device["name"],
                "index": device["index"],
                "channels": device["maxInputChannels"],
                "sample_rate": device["defaultSampleRate"],
                "is_loopback": device.get("isLoopbackDevice", False)
            }
        return None

    def callback(self, in_data, frame_count, time_info, status):
        """Callback для записи аудио"""
        if self.recording:
            self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)

    def start_recording(self) -> dict:
        """Начать запись системного аудио"""
        if self.recording:
            return {
                "status": "error",
                "message": "Запись уже идет!"
            }

        loopback_device = self.get_loopback_device()

        if not loopback_device:
            return {
                "status": "error",
                "message": "Loopback устройство не найдено"
            }

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = f"{settings.recordings_dir}/lection_{timestamp}.wav"

        self.frames = []
        self.recording = True
        self.loopback_device = loopback_device
        self.started_at = datetime.now()

        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=loopback_device["maxInputChannels"],
            rate=int(loopback_device["defaultSampleRate"]),
            frames_per_buffer=self.chunk_size,
            input=True,
            input_device_index=loopback_device["index"],
            stream_callback=self.callback
        )

        self.stream.start_stream()

        return {
            "status": "success",
            "message": "Запись началась",
            "filename": self.filename,
            "device_name": loopback_device["name"],
            "timestamp": self.started_at.isoformat()
        }

    def stop_recording(self) -> dict:
        """Остановить запись и сохранить файл"""
        if not self.recording:
            return {
                "status": "error",
                "message": "Запись не запущена!"
            }

        self.recording = False

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        wave_file = wave.open(self.filename, 'wb')
        wave_file.setnchannels(self.loopback_device["maxInputChannels"])
        wave_file.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wave_file.setframerate(int(self.loopback_device["defaultSampleRate"]))
        wave_file.writeframes(b''.join(self.frames))
        wave_file.close()

        filename = self.filename
        self.filename = None
        self.started_at = None

        return {
            "status": "success",
            "message": "Запись остановлена и сохранена",
            "filename": filename
        }

    def get_status(self) -> dict:
        """Получить текущий статус записи"""
        duration = None
        if self.recording and self.started_at:
            duration = (datetime.now() - self.started_at).total_seconds()

        return {
            "is_recording": self.recording,
            "current_filename": self.filename,
            "device_name": self.loopback_device["name"] if self.loopback_device else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "duration_seconds": duration
        }

    def cleanup(self):
        """Очистка ресурсов"""
        if self.stream:
            self.stream.close()
        if hasattr(self, 'p'):
            self.p.terminate()

recorder_service = SystemAudioRecorder()