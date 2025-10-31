# tests/test_nlp_config_and_init.py
def test_default_providers_and_public_exports(nlp_env):
    cfg, summarizer, kw, lg, tr, cache, utils, api = nlp_env()
    # дефолты
    assert cfg.settings.STT_PROVIDER == "dummy", "STT_PROVIDER по умолчанию должен быть 'dummy'"
    assert cfg.settings.SUMMARIZER_PROVIDER in {"extractive", "hf", "openai"}, "Неожиданный SUMMARIZER_PROVIDER"

    # публичные экспорты через пакет
    for name in [
        "transcribe_file", "transcribe_file_detailed",
        "summarize", "summarize_bullets", "make_note",
        "extract_keywords", "links_for_keywords"
    ]:
        assert hasattr(api, name), f"nlp_engine.{name} отсутствует в публичном API"
