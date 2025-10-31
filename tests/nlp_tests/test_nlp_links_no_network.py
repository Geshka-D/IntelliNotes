# tests/test_nlp_links_no_network.py
def test_links_without_enrichment(nlp_env):
    cfg, summarizer, kw, lg, tr, cache, utils, api = nlp_env(
        LINKS_ENRICH="false",
        LINKS_LANG="ru"
    )
    terms = ["машинное обучение", "нейронная сеть"]
    items = lg.links_for_keywords(terms, lang="ru")
    assert len(items) == 2
    for item in items:
        assert isinstance(item, dict)
        assert item["url"].startswith("https://ru.wikipedia.org/wiki/")
        assert item["title"]  # в режиме без enrichment title=term
        assert "summary" in item and item["summary"] == ""
