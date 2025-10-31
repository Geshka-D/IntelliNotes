from __future__ import annotations

import threading
import wave
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

try:
    import pyaudiowpatch as pyaudio  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pyaudio = None  # type: ignore

from backend.core.config import settings


class SystemAudioRecorder:
    _instance: Optional["SystemAudioRecorder"] = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "initialized"):
            return

        self.available = pyaudio is not None
        self.chunk_size = settings.chunk_size
        self.recordings_dir = Path(settings.recordings_dir)
        self.recordings_dir.mkdir(parents=True, exist_ok=True)

        self.p = pyaudio.PyAudio() if self.available else None  # type: ignore
        self.recording = False
        self.frames = []
        self.stream = None
        self.filename: Optional[Path] = None
        self.loopback_device = None
        self.started_at: Optional[datetime] = None
        self.initialized = True

    # --------------------------------------------------------------------- Utils
    def _error(self, message: str) -> Dict:
        return {"status": "error", "message": message}

    def _ensure_available(self) -> Optional[Dict]:
        if not self.available or self.p is None:
            return self._error("Audio recording backend is not available on this system.")
        return None

    def get_loopback_device(self) -> Optional[dict]:
        """Return loopback device info for WASAPI (Windows)."""
        if err := self._ensure_available():
            return None
        try:
            wasapi_info = self.p.get_host_api_info_by_type(pyaudio.paWASAPI)  # type: ignore
        except OSError:
            return None

        default_speakers = self.p.get_device_info_by_index(
            wasapi_info["defaultOutputDevice"]  # type: ignore[index]
        )

        if not default_speakers.get("isLoopbackDevice"):
            for loopback in self.p.get_loopback_device_info_generator():  # type: ignore[attr-defined]
                if default_speakers["name"] in loopback["name"]:
                    return loopback
        else:
            return default_speakers
        return None

    def get_device_info(self) -> Optional[dict]:
        device = self.get_loopback_device()
        if device:
            return {
                "name": device["name"],
                "index": device["index"],
                "channels": device["maxInputChannels"],
                "sample_rate": device["defaultSampleRate"],
                "is_loopback": device.get("isLoopbackDevice", False),
            }
        return None

    # ----------------------------------------------------------------- Recording
    def callback(self, in_data, frame_count, time_info, status):  # pragma: no cover
        if self.recording:
            self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)  # type: ignore

    def start_recording(self) -> Dict:
        if err := self._ensure_available():
            return err
        if self.recording:
            return self._error("Recording is already running.")

        loopback_device = self.get_loopback_device()
        if not loopback_device:
            return self._error("Loopback device not found.")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = self.recordings_dir / f"lecture_{timestamp}.wav"

        self.frames = []
        self.recording = True
        self.loopback_device = loopback_device
        self.started_at = datetime.now()

        self.stream = self.p.open(  # type: ignore[union-attr]
            format=pyaudio.paInt16,  # type: ignore[attr-defined]
            channels=loopback_device["maxInputChannels"],
            rate=int(loopback_device["defaultSampleRate"]),
            frames_per_buffer=self.chunk_size,
            input=True,
            input_device_index=loopback_device["index"],
            stream_callback=self.callback,
        )
        self.stream.start_stream()

        return {
            "status": "success",
            "message": "Recording started.",
            "filename": self.filename.name,
            "device_name": loopback_device["name"],
            "timestamp": self.started_at.isoformat(),
        }

    def stop_recording(self) -> Dict:
        if err := self._ensure_available():
            return err
        if not self.recording or not self.filename:
            return self._error("Recording is not running.")

        self.recording = False

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        wave_path = self.filename
        with wave.open(str(wave_path), "wb") as wave_file:
            wave_file.setnchannels(self.loopback_device["maxInputChannels"])  # type: ignore[index]
            wave_file.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))  # type: ignore[arg-type]
            wave_file.setframerate(int(self.loopback_device["defaultSampleRate"]))  # type: ignore[index]
            wave_file.writeframes(b"".join(self.frames))

        response = {
            "status": "success",
            "message": "Recording saved.",
            "filename": wave_path.name,
        }

        self.filename = None
        self.started_at = None
        self.frames = []
        return response

    def get_status(self) -> Dict:
        duration = None
        if self.recording and self.started_at:
            duration = (datetime.now() - self.started_at).total_seconds()

        return {
            "is_recording": self.recording,
            "current_filename": self.filename.name if self.filename else None,
            "device_name": self.loopback_device["name"] if self.loopback_device else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "duration_seconds": duration,
            "available": self.available,
        }

    def cleanup(self):
        if self.stream:
            self.stream.close()
        if self.p:
            self.p.terminate()


recorder_service = SystemAudioRecorder()
