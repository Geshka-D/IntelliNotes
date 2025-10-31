# tests/test_nlp_summarizer_extractive.py
def test_extractive_summary_and_bullets_ru(nlp_env):
    cfg, summarizer, kw, lg, tr, cache, utils, api = nlp_env(
        SUMMARIZER_PROVIDER="extractive",
        SUM_MAX_SENTENCES="3",
        SUM_MAX_BULLETS="4",
        LINKS_ENRICH="false"  # чтобы интеграция без сети прошла спокойно
    )
    text = (
        "Сегодня мы обсуждаем архитектуру Intellinotes. "
        "Цель проекта — интеллектуальные конспекты для встреч в Zoom. "
        "Мы используем распознавание речи и суммаризацию. "
        "Важно обеспечить удобную навигацию по таймкодам. "
        "Планируем поддержку ссылок на Wikipedia и быстрых справок. "
        "В конце встречи договорились о сроках релиза."
    )
    summary = summarizer.summarize(text)
    assert summary, "summary пустой"
    # в summary должно быть не более 3 предложений
    assert len(utils.split_sentences(summary)) <= 3

    bullets = summarizer.summarize_bullets(text)
    assert 1 <= len(bullets) <= 4
    # каждый буллет — это исходное предложение (экстракция)
    for b in bullets:
        assert b in text, f"Буллет не найден в исходном тексте: {b!r}"

def test_make_note_basic_structure(nlp_env):
    cfg, summarizer, kw, lg, tr, cache, utils, api = nlp_env(
        SUMMARIZER_PROVIDER="extractive",
        KEYWORDS_TOP_K="8",
        LINKS_ENRICH="false"
    )
    text = (
        "NLP is a branch of AI. It is used in chatbots, translation, and speech recognition. "
        "Transformers improved quality of text understanding."
    )
    note = summarizer.make_note(text, title="Demo")
    # обязательные поля
    for k in ["title","language","summary","keywords","links","content","summarizer_provider","bullets"]:
        assert k in note, f"В note отсутствует поле {k}"
    assert note["title"] == "Demo"
    assert note["language"] in {"ru","en"}
    assert isinstance(note["keywords"], list) and len(note["keywords"]) > 0
    assert isinstance(note["links"], list)
    # links — список объектов даже без enrichment
    assert all(isinstance(x, dict) and "url" in x for x in note["links"])
