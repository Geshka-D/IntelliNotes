# tests/test_nlp_providers_optional.py
import os
import importlib
import pytest

def _has_transformers():
    try:
        import transformers  # noqa
        return True
    except Exception:
        return False

@pytest.mark.skipif(not _has_transformers(), reason="transformers не установлен — пропускаем HF тест")
def test_hf_summarizer_smoke(nlp_env):
    # Этот тест будет пропущен, если transformers не установлен.
    # Если установлен, он проверит, что HF-пайплайн хотя бы инициализируется и падает в fallback/summary.
    cfg, summarizer, kw, lg, tr, cache, utils, api = nlp_env(
        SUMMARIZER_PROVIDER="hf",
        HF_SUM_MODEL_EN="facebook/bart-large-cnn",
        HF_SUM_MODEL_RU="IlyaGusev/mbart_ru_sum_gazeta",
        LINKS_ENRICH="false"
    )
    text = "This is a short text about meeting notes and how we want to summarize them intelligently."
    out = summarizer.summarize(text)
    assert isinstance(out, str) and len(out) > 0

@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Нет OPENAI_API_KEY — пропускаем OpenAI тест")
def test_openai_summarizer_smoke(nlp_env):
    cfg, summarizer, kw, lg, tr, cache, utils, api = nlp_env(
        SUMMARIZER_PROVIDER="openai",
        LINKS_ENRICH="false"
    )
    text = "We discussed the roadmap and decided on action items for the next sprint."
    # Если ключ валиден, получим структуру; если нет — код в summarizer сам fallback'нет.
    out = summarizer.summarize(text)
    assert isinstance(out, str)
