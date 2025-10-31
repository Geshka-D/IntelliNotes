# nlp_engine/keyword_extractor.py
from typing import List, Tuple, Dict
from collections import Counter, defaultdict

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

# Stop-word placeholders kept minimal for brevity in the test fixtures.
_STOP_RU = {...}  # (список слов вырезан в облегченном примере)
_STOP_EN = {...}


def _ngrams(tokens: List[str], n: int) -> List[Tuple[str, ...]]:
    return list(zip(*[tokens[i:] for i in range(n)]))


# === Fallback: simple statistical keyword extractor =========================
def _simple_keywords(text: str, lang: str, top_k: int) -> List[str]:
    stop = _STOP_RU if lang == "ru" else _STOP_EN
    toks = [t for t in simple_tokens(text) if t not in stop and len(t) > 2]
    if not toks:
        return []
    uni = Counter(toks)
    bi = Counter([" ".join(g) for g in _ngrams(toks, 2)])
    tri = Counter([" ".join(g) for g in _ngrams(toks, 3)])
    scores: Dict[str, float] = {}
    for k1, v1 in uni.items():
        scores[k1] = max(scores.get(k1, 0), float(v1))
    for k2, v2 in bi.items():
        scores[k2] = max(scores.get(k2, 0), float(v2) * 1.25)
    for k3, v3 in tri.items():
        scores[k3] = max(scores.get(k3, 0), float(v3) * 1.5)
    ranked = sorted(scores.items(), key=lambda kv: (kv[1], len(kv[0])), reverse=True)
    out: List[str] = []
    for term, _ in ranked:
        term_words = term.split()
        if len(term_words) == 1 and any(term in bigger for bigger in out if term != bigger):
            continue
        contained = [
            existing for existing in out
            if existing != term and existing in term and len(existing.split()) == 1
        ]
        if contained:
            out = [existing for existing in out if existing not in contained]
        out.append(term)
        if len(out) >= top_k:
            break
    return out


# === YAKE ====================================================================
def _yake_keywords(text: str, lang: str, top_k: int) -> List[Tuple[str, float]]:
    if yake is None:
        return []
    lan = "ru" if lang == "ru" else "en"
    try:
        kw_extractor = yake.KeywordExtractor(
            lan=lan,
            n=settings.KEYWORDS_MAX_NGRAM,
            top=top_k * 3,  # gather more to merge later
            dedupLim=0.9,
        )
        pairs = kw_extractor.extract_keywords(text)
        if not pairs:
            return []
        scores = [s for _, s in pairs]
        mn, mx = min(scores), max(scores)
        norm = []
        for k, s in pairs:
            val = 1.0 - ((s - mn) / (mx - mn + 1e-9))
            norm.append((k, float(val)))
        return norm
    except Exception:
        return []


# === KeyBERT =================================================================
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
        res = _keybert_model.extract_keywords(
            text,
            keyphrase_ngram_range=(min_n, max_n),
            stop_words=stop,
            top_n=top_k * 3,
            use_mmr=True,
            diversity=0.7,
        )
        return [(kw, float(sc)) for kw, sc in res]
    except Exception:
        return []


# === Helpers for candidate merging ===========================================
def _jaccard(a: str, b: str) -> float:
    sa, sb = set(a.split()), set(b.split())
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def _merge_and_dedup(cands: List[Tuple[str, float]], top_k: int) -> List[str]:
    # Sort by score (higher first) and favour longer phrases when tied.
    cands = sorted(cands, key=lambda x: (x[1], len(x[0])), reverse=True)
    out: List[str] = []
    for term, _ in cands:
        term_words = term.split()
        if len(term_words) == 1 and any(term in bigger for bigger in out if term != bigger):
            continue
        contained = [
            existing for existing in out
            if existing != term and existing in term and len(existing.split()) == 1
        ]
        if contained:
            out = [existing for existing in out if existing not in contained]
        if any(_jaccard(term, t) >= settings.KEYWORDS_DEDUP_SIM for t in out):
            continue
        out.append(term)
        if len(out) >= top_k:
            break
    return out


def extract_keywords(text: str, top_k: int = None, language: str = "") -> List[str]:
    """
    Hybrid keyword extractor:
    - If available, combine KeyBERT and YAKE scores for robustness.
    - When neither model is usable, fall back to a simple frequency-based approach.
    """
    if not text:
        return []
    top_k = top_k or settings.KEYWORDS_TOP_K
    lang = language or settings.KEYWORDS_LANG or "auto"
    if lang == "auto":
        lang = detect_lang(text)

    cands: Dict[str, float] = defaultdict(float)
    total_weight = 0.0

    kb = _keybert_keywords(text, lang, top_k)
    if kb:
        w = 0.6
        total_weight += w
        for k, s in kb:
            cands[k] = max(cands[k], s * w)

    yk = _yake_keywords(text, lang, top_k)
    if yk:
        w = 0.4
        total_weight += w
        for k, s in yk:
            cands[k] = max(cands[k], s * w)

    if total_weight == 0.0:
        return _simple_keywords(text, lang, top_k)

    merged = [(k, v / total_weight) for k, v in cands.items()]
    return _merge_and_dedup(merged, top_k)
