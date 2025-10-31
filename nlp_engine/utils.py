import re
import unicodedata
from typing import List

_CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")

def normalize_ws(text: str) -> str:
    return " ".join((text or "").split())

def contains_cyrillic(text: str) -> bool:
    return bool(_CYRILLIC_RE.search(text or ""))

def detect_lang(text: str) -> str:
    # Очень простой детектор: кириллица → ru, иначе en
    return "ru" if contains_cyrillic(text) else "en"

_SENT_SPLIT_RE = re.compile(r"(?<=[\.\!\?])\s+(?=[A-ZА-ЯЁ])", flags=re.U)

def split_sentences(text: str) -> List[str]:
    t = normalize_ws(text)
    if not t:
        return []
    # Бережный сплит: пробуем по регексу, fallback — по точкам
    parts = _SENT_SPLIT_RE.split(t)
    if len(parts) == 1:
        parts = re.split(r"(?<=[\.\!\?])\s+", t)
    return [p.strip() for p in parts if p.strip()]

_TOKEN_RE = re.compile(r"[A-Za-zА-Яа-яЁё\d]+")

def simple_tokens(text: str) -> List[str]:
    # Только буквы/цифры, lower
    return [m.group(0).lower() for m in _TOKEN_RE.finditer(text or "")]
