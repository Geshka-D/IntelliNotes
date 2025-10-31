# nlp_engine/link_generator.py
from typing import List, Dict
import requests
from urllib.parse import quote
from .utils import detect_lang
from .config import settings
from .cache import cache_get, cache_set

# [NEW] Вики-клиент с кешем и дизамбигуацией
def _guess_lang(keywords: List[str], explicit: str) -> str:
    if explicit in ("ru", "en"):
        return explicit
    joined = "".join(keywords)
    # простая эвристика: кириллица => ru
    return "ru" if any(ord(c) > 127 and c.isalpha() for c in joined) else "en"

def _wiki_search(term: str, lang: str) -> Dict:
    """
    Возвращает лучшую страницу: {title, url, summary, lang, source}
    Порядок: REST search → summary по canonical title → fallback: opensearch → прямой slug.
    """
    ttl = settings.LINKS_CACHE_TTL_DAYS * 24 * 3600
    key = f"{lang}:{term}"
    cached = cache_get(settings.LINKS_CACHE_PATH, "wikipedia", key, ttl)
    if cached:
        return cached

    base = f"https://{lang}.wikipedia.org"
    session = requests.Session()
    out = {"title": term, "url": f"{base}/wiki/{quote(term.replace(' ', '_'))}",
           "summary": "", "lang": lang, "source": "wikipedia"}

    try:
        # 1) REST search title (v1)
        r = session.get(f"{base}/w/rest.php/v1/search/title", params={"q": term, "limit": 1}, timeout=6)
        if r.ok:
            js = r.json()
            items = js.get("pages") or []
            if items:
                title = items[0].get("title") or term
                slug = quote(title.replace(" ", "_"))
                # 2) page summary по найденному title
                rs = session.get(f"{base}/api/rest_v1/page/summary/{slug}", timeout=6)
                if rs.ok:
                    j2 = rs.json()
                    out["title"] = j2.get("title", title)
                    out["url"] = j2.get("content_urls", {}).get("desktop", {}).get("page",
                                   f"{base}/wiki/{slug}")
                    out["summary"] = j2.get("extract", "")
                    cache_set(settings.LINKS_CACHE_PATH, "wikipedia", key, out)
                    return out

        # 3) fallback opensearch
        ro = session.get(f"{base}/w/api.php",
                         params={"action": "opensearch", "search": term, "limit": 1, "namespace": 0, "format": "json"},
                         timeout=6)
        if ro.ok:
            arr = ro.json()
            if len(arr) >= 4 and arr[1]:
                title = arr[1][0]
                url = arr[3][0] if len(arr[3]) else out["url"]
                out["title"], out["url"] = title, url
                # 4) попытаемся summary
                slug = quote(title.replace(" ", "_"))
                rs = session.get(f"{base}/api/rest_v1/page/summary/{slug}", timeout=6)
                if rs.ok:
                    j2 = rs.json()
                    out["summary"] = j2.get("extract", out["summary"])
                cache_set(settings.LINKS_CACHE_PATH, "wikipedia", key, out)
                return out

    except Exception:
        pass

    # 5) финальный fallback — прямой slug без summary
    cache_set(settings.LINKS_CACHE_PATH, "wikipedia", key, out)
    return out

def links_for_keywords(keywords: List[str], lang: str = "auto") -> List[Dict]:
    """
    [CHANGED] Возвращает список обогащённых ссылок:
    [{"term": "...", "title":"...", "url":"...", "summary":"...", "lang":"ru/en", "source":"wikipedia"}, ...]
    """
    if not keywords:
        return []
    lng = _guess_lang(keywords, settings.LINKS_LANG if lang == "auto" else lang)
    if settings.LINKS_PROVIDER != "wikipedia":
        # На будущее: другие провайдеры
        return [{"term": k, "title": k, "url": "", "summary": "", "lang": lng, "source": "unknown"} for k in keywords]

    res = []
    for k in keywords:
        item = _wiki_search(k, lng) if settings.LINKS_ENRICH else {
            "term": k, "title": k, "url": f"https://{lng}.wikipedia.org/wiki/{quote(k.replace(' ', '_'))}",
            "summary": "", "lang": lng, "source": "wikipedia"
        }
        item["term"] = k
        res.append(item)
    return res
