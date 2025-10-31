# nlp_engine/keyword_extractor.py
from typing import List, Tuple, Dict
from collections import Counter, defaultdict
from math import inf
try:
    import yake  # type: ignore
except Exception:
    yake = None  # optional
try:
    from keybert import KeyBERT  # type: ignore
    from sentence_transformers import SentenceTransformer  # type: ignore
except Exception:
    KeyBERT = None
    SentenceTransformer = None

from .utils import simple_tokens, detect_lang
from .config import settings

# Базовые списки стоп-слов — остаются как fallback
_STOP_RU = {...}  # (оставьте ваш список как был)
_STOP_EN = {...}

def _ngrams(tokens: List[str], n: int) -> List[Tuple[str, ...]]:
    return list(zip(*[tokens[i:] for i in range(n)]))

# === Fallback: прежний простой извлекатель ===================================
def _simple_keywords(text: str, lang: str, top_k: int) -> List[str]:
    stop = _STOP_RU if lang == "ru" else _STOP_EN
    toks = [t for t in simple_tokens(text) if t not in stop and len(t) > 2]
    if not toks:
        return []
    uni = Counter(toks)
    bi = Counter([" ".join(g) for g in _ngrams(toks, 2)])
    tri = Counter([" ".join(g) for g in _ngrams(toks, 3)])
    scores = {}
    for k1, v1 in uni.items(): scores[k1] = max(scores.get(k1, 0), v1)
    for k2, v2 in bi.items(): scores[k2] = max(scores.get(k2, 0), v2 * 1.25)
    for k3, v3 in tri.items(): scores[k3] = max(scores.get(k3, 0), v3 * 1.5)
    ranked = sorted(scores.items(), key=lambda kv: (kv[1], len(kv[0])), reverse=True)
    out, seen = [], set()
    for term, _ in ranked:
        if any(term in bigger for bigger in seen if term != bigger):  # подстрока большего
            continue
        out.append(term); seen.add(term)
        if len(out) >= top_k: break
    return out

# === YAKE =====================================================================
def _yake_keywords(text: str, lang: str, top_k: int) -> List[Tuple[str, float]]:
    if yake is None:
        return []
    lan = "ru" if lang == "ru" else "en"
    try:
        kw_extractor = yake.KeywordExtractor(lan=lan,
                                             n=settings.KEYWORDS_MAX_NGRAM,
                                             top=top_k*3,  # с запасом для слияния
                                             dedupLim=0.9)
        pairs = kw_extractor.extract_keywords(text)
        # YAKE: чем МЕНЬШЕ score, тем лучше — нормализуем в 0..1
        if not pairs:
            return []
        scores = [s for _, s in pairs]
        mn, mx = min(scores), max(scores)
        norm = []
        for k, s in pairs:
            val = 1.0 - ((s - mn) / (mx - mn + 1e-9))  # лучший≈1
            norm.append((k, float(val)))
        return norm
    except Exception:
        return []

# === KeyBERT ==================================================================
_keybert_model = None  # lazy init

def _ensure_keybert_model():
    global _keybert_model
    if _keybert_model is None and KeyBERT and SentenceTransformer:
        try:
            st = SentenceTransformer(settings.KEYBERT_MODEL)
            _keybert_model = KeyBERT(model=st)
        except Exception:
            _keybert_model = None

def _keybert_keywords(text: str, lang: str, top_k: int) -> List[Tuple[str, float]]:
    _ensure_keybert_model()
    if _keybert_model is None:
        return []
    try:
        stop = "russian" if lang == "ru" else "english"
        min_n, max_n = settings.KEYWORDS_MIN_NGRAM, settings.KEYWORDS_MAX_NGRAM
        # возвращает [(kw, score)], score 0..1 — чем больше, тем лучше
        res = _keybert_model.extract_keywords(
            text,
            keyphrase_ngram_range=(min_n, max_n),
            stop_words=stop,
            top_n=top_k*3,
            use_mmr=True,
            diversity=0.7
        )
        return [(kw, float(sc)) for kw, sc in res]
    except Exception:
        return []

# === Слияние, ранжирование и дедупликация ====================================
def _jaccard(a: str, b: str) -> float:
    sa, sb = set(a.split()), set(b.split())
    if not sa or not sb: return 0.0
    return len(sa & sb) / len(sa | sb)

def _merge_and_dedup(cands: List[Tuple[str, float]], top_k: int) -> List[str]:
    # сортируем по score и длине
    cands = sorted(cands, key=lambda x: (x[1], len(x[0])), reverse=True)
    out: List[str] = []
    for term, sc in cands:
        # подстроки большего термина — пропускаем
        if any(term in bigger for bigger in out if term != bigger):
            continue
        # Jaccard-дедуп
        if any(_jaccard(term, t) >= settings.KEYWORDS_DEDUP_SIM for t in out):
            continue
        out.append(term)
        if len(out) >= top_k:
            break
    return out

def extract_keywords(text: str, top_k: int = None, language: str = "") -> List[str]:
    """
    [CHANGED] Гибридный извлекатель:
    - Если доступны: KeyBERT + YAKE → слияние, весовая агрегация, дедуп.
    - Если нет — fallback на простой извлекатель.
    """
    if not text:
        return []
    top_k = top_k or settings.KEYWORDS_TOP_K
    lang = (language or settings.KEYWORDS_LANG or "auto")
    if lang == "auto":
        lang = detect_lang(text)

    # кандидаты
    cands: Dict[str, float] = defaultdict(float)
    total_weight = 0.0

    # KeyBERT (0..1), вес 0.6
    kb = _keybert_keywords(text, lang, top_k)
    if kb:
        w = 0.6
        total_weight += w
        for k, s in kb:
            cands[k] = max(cands[k], s * w)

    # YAKE (0..1 после нормализации), вес 0.4
    yk = _yake_keywords(text, lang, top_k)
    if yk:
        w = 0.4
        total_weight += w
        for k, s in yk:
            cands[k] = max(cands[k], s * w)

    # Если нет ни одного провайдера — fallback
    if total_weight == 0.0:
        return _simple_keywords(text, lang, top_k)

    merged = list(cands.items())  # [(term, score)]
    # нормируем на сумму весов и дедуплицируем
    merged = [(k, v / total_weight) for k, v in merged]
    return _merge_and_dedup(merged, top_k)
