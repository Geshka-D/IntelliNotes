import os
import importlib.util
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from dotenv import dotenv_values, find_dotenv


def _load_dotenv_defaults() -> Dict[str, str]:
    """Read .env without mutating os.environ; fallback to project root."""
    path = find_dotenv(usecwd=True)
    if not path:
        root_candidate = Path(__file__).resolve().parents[1] / ".env"
        path = str(root_candidate) if root_candidate.exists() else ""
    return {k: str(v) for k, v in dotenv_values(path).items()} if path else {}


_ENV_DEFAULTS = _load_dotenv_defaults()


def _getenv(key: str, default: str = "") -> str:
    """Fetch env var with local override support."""
    if key in os.environ:
        return os.environ[key]
    return _ENV_DEFAULTS.get(key, default)


_VALID_STT_PROVIDERS = {"dummy", "faster-whisper", "openai", "vosk"}


def _resolve_stt_provider(raw: str) -> str:
    value = (raw or "").strip().lower() or "dummy"
    if value not in _VALID_STT_PROVIDERS:
        return "dummy"
    if value == "faster-whisper" and importlib.util.find_spec("faster_whisper") is None:
        return "dummy"
    if value == "openai" and not _getenv("OPENAI_API_KEY", ""):
        return "dummy"
    if value == "vosk":
        model_path = _getenv("VOSK_MODEL_PATH", "")
        if not model_path or not Path(model_path).is_dir():
            return "dummy"
    return value


@dataclass(frozen=True)
class Settings:
    # ==== STT ===============================================================
    STT_PROVIDER: str = _resolve_stt_provider(_getenv("STT_PROVIDER", "dummy"))
    STT_LANGUAGE: str = _getenv("STT_LANGUAGE", "").strip()
    FWHISPER_MODEL: str = _getenv("FWHISPER_MODEL", "base")
    FWHISPER_DEVICE: str = _getenv("FWHISPER_DEVICE", "cpu")
    FWHISPER_COMPUTE_TYPE: str = _getenv("FWHISPER_COMPUTE_TYPE", "int8")
    OPENAI_API_KEY: str = _getenv("OPENAI_API_KEY", "")
    OPENAI_WHISPER_MODEL: str = _getenv("OPENAI_WHISPER_MODEL", "whisper-1")
    VOSK_MODEL_PATH: str = _getenv("VOSK_MODEL_PATH", "")

    # ==== Summarization =====================================================
    SUMMARIZER_PROVIDER: str = _getenv("SUMMARIZER_PROVIDER", "extractive").lower()
    SUM_MAX_SENTENCES: int = int(_getenv("SUM_MAX_SENTENCES", "5"))
    SUM_MAX_BULLETS: int = int(_getenv("SUM_MAX_BULLETS", "7"))
    SUM_CHUNK_SENTENCES: int = int(_getenv("SUM_CHUNK_SENTENCES", "40"))
    SUM_SECOND_PASS_SENTENCES: int = int(_getenv("SUM_SECOND_PASS_SENTENCES", "8"))
    HF_SUM_MODEL_EN: str = _getenv("HF_SUM_MODEL_EN", "facebook/bart-large-cnn")
    HF_SUM_MODEL_RU: str = _getenv("HF_SUM_MODEL_RU", "IlyaGusev/mbart_ru_sum_gazeta")
    HF_SUM_MAX_INPUT_CHARS: int = int(_getenv("HF_SUM_MAX_INPUT_CHARS", "3500"))

    # ==== Keywords ==========================================================
    KEYWORDS_PROVIDER: str = _getenv("KEYWORDS_PROVIDER", "hybrid").lower()
    KEYWORDS_TOP_K: int = int(_getenv("KEYWORDS_TOP_K", "12"))
    KEYWORDS_MIN_NGRAM: int = int(_getenv("KEYWORDS_MIN_NGRAM", "1"))
    KEYWORDS_MAX_NGRAM: int = int(_getenv("KEYWORDS_MAX_NGRAM", "3"))
    KEYWORDS_DEDUP_SIM: float = float(_getenv("KEYWORDS_DEDUP_SIM", "0.8"))
    KEYBERT_MODEL: str = _getenv("KEYBERT_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")
    KEYWORDS_LANG: str = _getenv("KEYWORDS_LANG", "auto")

    # ==== Links =============================================================
    LINKS_PROVIDER: str = _getenv("LINKS_PROVIDER", "wikipedia").lower()
    LINKS_LANG: str = _getenv("LINKS_LANG", "auto")
    LINKS_ENRICH: bool = _getenv("LINKS_ENRICH", "true").lower() == "true"
    LINKS_CACHE_PATH: str = _getenv("LINKS_CACHE_PATH", "data/cache/wiki_cache.json")
    LINKS_CACHE_TTL_DAYS: int = int(_getenv("LINKS_CACHE_TTL_DAYS", "14"))

    # Dummy
    DUMMY_PREFIX: str = _getenv("DUMMY_TEXT_PREFIX", "Transcribed text placeholder for")


settings = Settings()
