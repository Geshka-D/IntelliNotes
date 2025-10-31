# tests/conftest.py
import os
import importlib
import pytest

def _reload_nlp_modules():
    """
    Полностью перезагружает модуль конфигурации и все зависящие от него модули,
    чтобы изменения env применялись сразу.
    Возвращает кортеж модулей в порядке:
    (config, summarizer, keyword_extractor, link_generator, transcriber, cache, utils, api)
    """
    import nlp_engine.config as cfg
    importlib.reload(cfg)
    import nlp_engine.summarizer as summarizer
    importlib.reload(summarizer)
    import nlp_engine.keyword_extractor as kw
    importlib.reload(kw)
    import nlp_engine.link_generator as lg
    importlib.reload(lg)
    import nlp_engine.transcriber as tr
    importlib.reload(tr)
    import nlp_engine.cache as cache
    importlib.reload(cache)
    import nlp_engine.utils as utils
    importlib.reload(utils)
    import nlp_engine as api
    importlib.reload(api)
    return cfg, summarizer, kw, lg, tr, cache, utils, api

@pytest.fixture
def nlp_env(monkeypatch):
    """
    Фикстура: применяет env‑переменные к процессу и перезагружает NLP‑модули.
    Использование:
        cfg, summarizer, kw, lg, tr, cache, utils, api = nlp_env(
            SUMMARIZER_PROVIDER="extractive",
            LINKS_ENRICH="false",
        )
    """
    def _apply(**envs):
        for k, v in envs.items():
            if v is None:
                monkeypatch.delenv(k, raising=False)
            else:
                monkeypatch.setenv(k, str(v))
        return _reload_nlp_modules()
    return _apply
