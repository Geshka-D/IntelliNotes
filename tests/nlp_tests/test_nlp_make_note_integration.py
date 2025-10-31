# tests/test_nlp_make_note_integration.py
def test_make_note_full_integration_no_network(nlp_env):
    cfg, summarizer, kw, lg, tr, cache, utils, api = nlp_env(
        SUMMARIZER_PROVIDER="extractive",
        KEYWORDS_TOP_K="8",
        LINKS_ENRICH="false",
        LINKS_LANG="auto"
    )
    text = (
        "Сегодня обсуждали план релиза Intellinotes. "
        "Система делает интеллектуальные конспекты встреч. "
        "Нужно добавить таймкоды, боковую навигацию и обогащённые ссылки. "
        "Ключевые функции: распознавание речи, суммаризация, поиск. "
        "Договорились проверить качество ключевых слов и ссылок."
    )
    note = summarizer.make_note(text, title="Internal meeting")
    assert note["summarizer_provider"] == "extractive"
    assert 1 <= len(note["bullets"]) <= cfg.settings.SUM_MAX_BULLETS
    assert isinstance(note["keywords"], list) and len(note["keywords"]) > 0
    assert isinstance(note["links"], list)
    # Структура ссылок
    for it in note["links"]:
        assert {"term","title","url","summary","lang","source"} <= set(it.keys())
