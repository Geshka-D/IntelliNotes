# nlp_engine/summarizer.py
from typing import List, Dict, Optional
from collections import Counter
import logging

from .utils import split_sentences, simple_tokens, detect_lang, normalize_ws
from .keyword_extractor import extract_keywords
from .link_generator import links_for_keywords
from .config import settings

logger = logging.getLogger(__name__)

# ===== Экстрактивная оценка предложений (улучшенная) =========================
def _sent_scores(sentences: List[str], lang: str) -> List[float]:
    stop_ru = { ... }  # как раньше (ваш список)
    stop_en = { ... }
    stop = stop_ru if lang == "ru" else stop_en

    token_lists = [[t for t in simple_tokens(s) if t not in stop] for s in sentences]
    freq = Counter([t for lst in token_lists for t in lst])

    scores: List[float] = []
    n = len(sentences)
    for i, (s, toks) in enumerate(zip(sentences, token_lists)):
        if not toks:
            scores.append(0.0); continue
        base = sum(freq[t] for t in toks) / max(1, len(toks))
        pos_bonus = 1.0 + (0.25 * (1.0 - i / max(1, n - 1)))
        length = max(1, len(s))
        len_penalty = 1.0
        if length < 40: len_penalty = 0.75
        elif length > 400: len_penalty = 0.8
        scores.append(base * pos_bonus * len_penalty)
    return scores

def _extractive_summary(text: str, k: int) -> str:
    t = normalize_ws(text or "")
    if not t:
        return ""
    sents = split_sentences(t)
    if not sents:
        return t[:400] + ("..." if len(t) > 400 else "")
    if len(sents) <= k:
        return " ".join(sents)
    lang = detect_lang(t)
    scores = _sent_scores(sents, lang)
    top_idx = sorted(range(len(sents)), key=lambda i: scores[i], reverse=True)[:k]
    top_idx.sort()
    return " ".join(sents[i] for i in top_idx)

# ===== HF-провайдер (map-reduce для длинных) =================================
_hf_pipes = {"ru": None, "en": None}

def _ensure_hf(lang: str):
    global _hf_pipes
    try:
        from transformers import pipeline
    except Exception as e:
        logger.warning("transformers не установлен: %s", e)
        return None
    if _hf_pipes[lang] is None:
        mdl = settings.HF_SUM_MODEL_RU if lang == "ru" else settings.HF_SUM_MODEL_EN
        try:
            _hf_pipes[lang] = pipeline("summarization", model=mdl)  # device auto
        except Exception as e:
            logger.warning("Невозможно инициализировать HF summarizer (%s): %s", mdl, e)
            _hf_pipes[lang] = None
    return _hf_pipes[lang]

def _hf_summarize(text: str, lang: str, chunk_sents: int, second_pass_k: int) -> str:
    pipe = _ensure_hf(lang)
    if pipe is None:
        # fallback на экстрактивную
        return _extractive_summary(text, settings.SUM_MAX_SENTENCES)

    sents = split_sentences(text)
    if not sents:
        return text[:400] + ("..." if len(text) > 400 else "")

    chunks = []
    cur = []
    for s in sents:
        cur.append(s)
        if len(cur) >= chunk_sents or sum(len(x) for x in cur) >= settings.HF_SUM_MAX_INPUT_CHARS:
            chunks.append(" ".join(cur)); cur = []
    if cur: chunks.append(" ".join(cur))

    partials: List[str] = []
    for ch in chunks:
        try:
            out = pipe(ch, max_length=220, min_length=60, do_sample=False)[0]["summary_text"].strip()
            partials.append(out)
        except Exception:
            # локальный fallback кусочка
            partials.append(_extractive_summary(ch, max(2, settings.SUM_MAX_SENTENCES // 2)))

    glue = " ".join(partials)
    # второй проход — сжать сводку
    try:
        out2 = pipe(glue, max_length=240, min_length=80, do_sample=False)[0]["summary_text"].strip()
        return out2
    except Exception:
        return _extractive_summary(glue, second_pass_k)

# ===== OpenAI-провайдер (структурированная сводка) ============================
def _openai_summarize(text: str) -> Dict:
    try:
        from openai import OpenAI
    except Exception as e:
        logger.warning("openai не установлен: %s", e); return {}
    if not settings.OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY не задан"); return {}

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    prompt = (
        "You are an expert meeting summarizer. Create a structured summary in JSON with keys: "
        "`overview` (2-3 sentences), `bullets` (5-8 bullets), `decisions` (0-5), "
        "`action_items` (0-8 with owners if possible), `open_questions` (0-5). "
        "Be concise. Use the meeting language.\n\nMEETING TRANSCRIPT:\n"
        + text
    )
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=700
        )
        raw = resp.choices[0].message.content
        # Пробуем найти JSON (может прийти и просто текстом)
        import json, re
        code_blocks = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", raw, flags=re.S)
        payload = json.loads(code_blocks[0]) if code_blocks else json.loads(raw)
        return payload
    except Exception as e:
        logger.warning("OpenAI summarization failed: %s", e)
        return {}

# ===== Публичный API ==========================================================
def summarize(text: str, max_sentences: Optional[int] = None) -> str:
    """
    [CHANGED] Единая точка: extractive | hf | openai (overview → строка)
    """
    t = normalize_ws(text or "")
    if not t:
        return ""
    k = max(1, (max_sentences or settings.SUM_MAX_SENTENCES))
    prov = settings.SUMMARIZER_PROVIDER
    lang = detect_lang(t)

    if prov == "hf":
        return _hf_summarize(t, lang, settings.SUM_CHUNK_SENTENCES, settings.SUM_SECOND_PASS_SENTENCES)

    if prov == "openai":
        payload = _openai_summarize(t)
        if payload.get("overview"):
            return payload["overview"]
        # fallback: экстрактивное
        return _extractive_summary(t, k)

    # default: extractive
    return _extractive_summary(t, k)

def summarize_bullets(text: str, max_points: int = None) -> List[str]:
    """
    [CHANGED] Буллеты: OpenAI → bullets; HF/Extractive → лучшие предложения.
    """
    t = normalize_ws(text or ""); 
    if not t: return []
    max_points = max_points or settings.SUM_MAX_BULLETS
    prov = settings.SUMMARIZER_PROVIDER
    lang = detect_lang(t)

    if prov == "openai":
        payload = _openai_summarize(t)
        bullets = payload.get("bullets") or []
        return bullets[:max_points] if isinstance(bullets, list) else []

    # HF/Extractive: берём топ предложений
    sents = split_sentences(t)
    if not sents: return []
    scores = _sent_scores(sents, lang)
    idx = sorted(range(len(sents)), key=lambda i: scores[i], reverse=True)[:max_points]
    idx.sort()
    return [sents[i] for i in idx]

def make_note(
    text: str,
    title: Optional[str] = None,
    language: Optional[str] = None,
    top_k_keywords: Optional[int] = None,
) -> Dict:
    """
    [CHANGED] Формируем "интеллектуальный конспект":
    - summary (overview),
    - bullets (если есть),
    - decisions/action_items/open_questions (для openai),
    - keywords (гибрид),
    - links (обогащённые),
    - content.
    """
    lang = language or detect_lang(text or "")
    k = top_k_keywords or settings.KEYWORDS_TOP_K

    prov = settings.SUMMARIZER_PROVIDER
    overview = summarize(text)
    bullets = summarize_bullets(text)

    decisions, actions, questions = [], [], []
    if prov == "openai":
        payload = _openai_summarize(text)
        decisions = payload.get("decisions") or []
        actions = payload.get("action_items") or []
        questions = payload.get("open_questions") or []

    keywords = extract_keywords(text, top_k=k, language=lang)
    links = links_for_keywords(keywords, lang=settings.LINKS_LANG)

    return {
        "title": title or "",
        "language": lang,
        "summary": overview,
        "bullets": bullets,
        "decisions": decisions,
        "action_items": actions,
        "open_questions": questions,
        "keywords": keywords,
        "links": links,          # теперь это список объектов с summary/url
        "content": text,
        "summarizer_provider": prov
    }
