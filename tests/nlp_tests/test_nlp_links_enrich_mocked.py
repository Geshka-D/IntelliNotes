# tests/test_nlp_links_enrich_mocked.py
import json
from urllib.parse import urlencode

class _Resp:
    def __init__(self, ok=True, payload=None):
        self.ok = ok
        self._payload = payload
    def json(self):
        return self._payload

class _MockSession:
    def get(self, url, params=None, timeout=6):
        # Эмулируем два запроса:
        # 1) /w/rest.php/v1/search/title?q=<term>&limit=1
        # 2) /api/rest_v1/page/summary/<slug>
        # Fallback: /w/api.php?action=opensearch...
        if "/w/rest.php/v1/search/title" in url:
            q = params.get("q")
            # "Нашли" страницу с нормализованным заголовком
            return _Resp(True, {"pages": [{"title": f"{q.title()}"}]})
        if "/api/rest_v1/page/summary/" in url:
            # Вернём краткое описание
            return _Resp(True, {"title": "Нормализованный заголовок", "extract": "Краткое описание"})
        if "/w/api.php" in url:
            return _Resp(True, ["term", ["Term"], ["desc"], ["https://example"]])
        return _Resp(False, {})

def test_links_with_enrichment_mocked(monkeypatch, nlp_env, tmp_path):
    # Подменяем requests.Session() на нашу заглушку
    import requests
    monkeypatch.setattr(requests, "Session", lambda: _MockSession())

    cache_path = tmp_path / "wiki_cache.json"
    cfg, summarizer, kw, lg, tr, cache, utils, api = nlp_env(
        LINKS_ENRICH="true",
        LINKS_LANG="ru",
        LINKS_CACHE_PATH=str(cache_path)
    )
    items = lg.links_for_keywords(["машинное обучение"], lang="ru")
    assert len(items) == 1
    it = items[0]
    assert it["url"].startswith("https://ru.wikipedia.org/wiki/")
    assert it["summary"] == "Краткое описание"
    # Повторный вызов должен браться из кеша и не падать
    items2 = lg.links_for_keywords(["машинное обучение"], lang="ru")
    assert items2[0]["summary"] == "Краткое описание"
