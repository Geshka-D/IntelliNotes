# nlp_engine/__init__.py
from .transcriber import (
    transcribe_file,
    transcribe_file_detailed,
    Transcript, Segment, supported_stt_providers,
)
from .summarizer import summarize, summarize_bullets, make_note
from .keyword_extractor import extract_keywords
from .link_generator import links_for_keywords  # теперь возвращает обогащённые ссылки
