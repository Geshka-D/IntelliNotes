# nlp_engine/config.py
import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Загружаем .env, если есть
load_dotenv(dotenv_path=".env", override=False)

@dataclass(frozen=True)
class Settings:
    # ==== STT (как и раньше) ==================================================
    STT_PROVIDER: str = os.getenv("STT_PROVIDER", "dummy").lower()
    STT_LANGUAGE: str = os.getenv("STT_LANGUAGE", "").strip()
    FWHISPER_MODEL: str = os.getenv("FWHISPER_MODEL", "base")
    FWHISPER_DEVICE: str = os.getenv("FWHISPER_DEVICE", "cpu")
    FWHISPER_COMPUTE_TYPE: str = os.getenv("FWHISPER_COMPUTE_TYPE", "int8")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_WHISPER_MODEL: str = os.getenv("OPENAI_WHISPER_MODEL", "whisper-1")
    VOSK_MODEL_PATH: str = os.getenv("VOSK_MODEL_PATH", "")

    # ==== Summarization (НОВОЕ) ==============================================
    # extractive | hf | openai
    SUMMARIZER_PROVIDER: str = os.getenv("SUMMARIZER_PROVIDER", "extractive").lower()
    SUM_MAX_SENTENCES: int = int(os.getenv("SUM_MAX_SENTENCES", "5"))
    SUM_MAX_BULLETS: int = int(os.getenv("SUM_MAX_BULLETS", "7"))
    # Иерархичная сводка для длинных текстов
    SUM_CHUNK_SENTENCES: int = int(os.getenv("SUM_CHUNK_SENTENCES", "40"))
    SUM_SECOND_PASS_SENTENCES: int = int(os.getenv("SUM_SECOND_PASS_SENTENCES", "8"))
    # HF-модели
    HF_SUM_MODEL_EN: str = os.getenv("HF_SUM_MODEL_EN", "facebook/bart-large-cnn")
    HF_SUM_MODEL_RU: str = os.getenv("HF_SUM_MODEL_RU", "IlyaGusev/mbart_ru_sum_gazeta")
    HF_SUM_MAX_INPUT_CHARS: int = int(os.getenv("HF_SUM_MAX_INPUT_CHARS", "3500"))  # грубая граница

    # ==== Keywords (НОВОЕ) ====================================================
    # hybrid | yake | keybert | simple
    KEYWORDS_PROVIDER: str = os.getenv("KEYWORDS_PROVIDER", "hybrid").lower()
    KEYWORDS_TOP_K: int = int(os.getenv("KEYWORDS_TOP_K", "12"))
    KEYWORDS_MIN_NGRAM: int = int(os.getenv("KEYWORDS_MIN_NGRAM", "1"))
    KEYWORDS_MAX_NGRAM: int = int(os.getenv("KEYWORDS_MAX_NGRAM", "3"))
    KEYWORDS_DEDUP_SIM: float = float(os.getenv("KEYWORDS_DEDUP_SIM", "0.8"))  # Jaccard для фраз
    KEYBERT_MODEL: str = os.getenv("KEYBERT_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")
    KEYWORDS_LANG: str = os.getenv("KEYWORDS_LANG", "auto")

    # ==== Links (НОВОЕ) =======================================================
    # wikipedia (пока один провайдер)
    LINKS_PROVIDER: str = os.getenv("LINKS_PROVIDER", "wikipedia").lower()
    LINKS_LANG: str = os.getenv("LINKS_LANG", "auto")  # ru | en | auto
    LINKS_ENRICH: bool = os.getenv("LINKS_ENRICH", "true").lower() == "true"
    LINKS_CACHE_PATH: str = os.getenv("LINKS_CACHE_PATH", "data/cache/wiki_cache.json")
    LINKS_CACHE_TTL_DAYS: int = int(os.getenv("LINKS_CACHE_TTL_DAYS", "14"))

    # Dummy
    DUMMY_PREFIX: str = os.getenv("DUMMY_TEXT_PREFIX", "Transcribed text placeholder for")

settings = Settings()
