import re
from typing import List

_CYRILLIC_RE = re.compile(r"[\u0400-\u04FF\uFFFD]")
_SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\u0400-\u04FF\uFFFD])", flags=re.U)
_TOKEN_RE = re.compile(r"[A-Za-z\u0400-\u04FF\uFFFD\d]+")


def normalize_ws(text: str) -> str:
    return " ".join((text or "").split())


def contains_cyrillic(text: str) -> bool:
    return bool(_CYRILLIC_RE.search(text or ""))


def detect_lang(text: str) -> str:
    # Fast heuristic: detect cyrillic to switch to Russian; otherwise use English.
    return "ru" if contains_cyrillic(text) else "en"


def split_sentences(text: str) -> List[str]:
    t = normalize_ws(text)
    if not t:
        return []
    # First try regex for punctuation + uppercase, fallback to generic split.
    parts = _SENT_SPLIT_RE.split(t)
    if len(parts) == 1:
        parts = re.split(r"(?<=[.!?])\s+", t)
    return [p.strip() for p in parts if p.strip()]


def simple_tokens(text: str) -> List[str]:
    # Tokenize alphanumeric words (latin and cyrillic); lowercase for stability.
    return [m.group(0).lower() for m in _TOKEN_RE.finditer(text or "")]
