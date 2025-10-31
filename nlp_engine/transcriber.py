from dataclasses import dataclass
from typing import List, Optional
import os
import logging

from .config import settings
from .utils import normalize_ws

logger = logging.getLogger(__name__)

# Безопасные импорты провайдеров
try:
    from faster_whisper import WhisperModel  # type: ignore
except Exception:  # пакет не установлен
    WhisperModel = None  # type: ignore

try:
    from openai import OpenAI  # >= 1.x
except Exception:
    OpenAI = None  # type: ignore

try:
    import vosk  # type: ignore
    import wave
except Exception:
    vosk = None  # type: ignore

@dataclass
class Segment:
    start: float
    end: float
    text: str

@dataclass
class Transcript:
    text: str
    language: str
    segments: List[Segment]

def supported_stt_providers() -> List[str]:
    return ["dummy", "faster-whisper", "openai", "vosk"]

# --- провайдеры --------------------------------------------------------------

def _asr_dummy(path: str, language: Optional[str]) -> Transcript:
    # Если передали .txt — прочитать содержимое, иначе вернуть плейсхолдер
    text = ""
    if path.lower().endswith(".txt") and os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception:
            pass
    if not text:
        base = os.path.basename(path)
        text = f"{settings.DUMMY_PREFIX} {base}"
    text = normalize_ws(text)
    seg = Segment(start=0.0, end=0.0, text=text)
    lang = language or ("ru" if "Transcribed" not in text and "замена" in text else "en")
    return Transcript(text=text, language=lang, segments=[seg])

def _asr_faster_whisper(path: str, language: Optional[str]) -> Transcript:
    if WhisperModel is None:
        raise RuntimeError("faster-whisper не установлен. Установите из requirements-nlp.txt")
    model = WhisperModel(
        settings.FWHISPER_MODEL,
        device=settings.FWHISPER_DEVICE,
        compute_type=settings.FWHISPER_COMPUTE_TYPE,
    )
    # Подавление шума на паузах (VAD) и сегменты
    segments_iter, info = model.transcribe(
        path,
        language=language if language else None,
        vad_filter=True,
        beam_size=5,
        word_timestamps=False,
    )
    segments: List[Segment] = []
    texts: List[str] = []
    for s in segments_iter:
        st = float(getattr(s, "start", 0.0) or 0.0)
        en = float(getattr(s, "end", st) or st)
        tx = normalize_ws(getattr(s, "text", ""))
        if tx:
            segments.append(Segment(start=st, end=en, text=tx))
            texts.append(tx)
    full_text = normalize_ws(" ".join(texts))
    lang = getattr(info, "language", "") or (language or "")
    return Transcript(text=full_text, language=lang, segments=segments)

def _asr_openai(path: str, language: Optional[str]) -> Transcript:
    if OpenAI is None:
        raise RuntimeError("openai не установлен. Установите пакет 'openai>=1.0'.")
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("Не задан OPENAI_API_KEY для STT_PROVIDER=openai.")
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    with open(path, "rb") as f:
        # Возвращается только текст; сегментов нет → делаем один общий
        resp = client.audio.transcriptions.create(
            model=settings.OPENAI_WHISPER_MODEL,
            file=f,
            language=language if language else None,
            response_format="json",
        )
    text = normalize_ws(resp.text or "")
    seg = Segment(start=0.0, end=0.0, text=text)
    return Transcript(text=text, language=language or "", segments=[seg])

def _asr_vosk(path: str, language: Optional[str]) -> Transcript:
    if vosk is None:
        raise RuntimeError("vosk не установлен.")
    model_path = settings.VOSK_MODEL_PATH
    if not model_path or not os.path.isdir(model_path):
        raise RuntimeError("VOSK_MODEL_PATH не задан или путь некорректен.")
    mdl = vosk.Model(model_path)
    # Vosk требует PCM WAV
    if not path.lower().endswith(".wav"):
        raise RuntimeError("Для Vosk ожидается .wav (PCM). Конвертируйте заранее.")
    wf = wave.open(path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in (8000, 16000, 32000, 44100, 48000):
        raise RuntimeError("Нужен одноканальный PCM WAV, 16-bit. Конвертируйте файл.")
    rec = vosk.KaldiRecognizer(mdl, wf.getframerate())
    texts: List[str] = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            import json
            j = json.loads(rec.Result())
            tx = normalize_ws(j.get("text", ""))
            if tx:
                texts.append(tx)
    import json
    j = json.loads(rec.FinalResult())
    tx = normalize_ws(j.get("text", ""))
    if tx:
        texts.append(tx)
    full = normalize_ws(" ".join(texts))
    seg = Segment(start=0.0, end=0.0, text=full)
    return Transcript(text=full, language=language or "", segments=[seg])

# --- публичные функции -------------------------------------------------------

def transcribe_file_detailed(path: str, language: Optional[str] = None) -> Transcript:
    provider = settings.STT_PROVIDER
    if provider == "faster-whisper":
        return _asr_faster_whisper(path, language or settings.STT_LANGUAGE or None)
    if provider == "openai":
        return _asr_openai(path, language or settings.STT_LANGUAGE or None)
    if provider == "vosk":
        return _asr_vosk(path, language or settings.STT_LANGUAGE or None)
    # default dummy
    return _asr_dummy(path, language or settings.STT_LANGUAGE or None)

def transcribe_file(path: str, language: Optional[str] = None) -> str:
    """
    Совместимая с текущим backend.services.audio_service обёртка:
    возвращает СТРОКУ с полным текстом транскрипта.
    """
    return transcribe_file_detailed(path, language).text
