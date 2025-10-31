# tests/test_nlp_keyword_extractor.py
def test_keywords_ru_dedup_substrings(nlp_env):
    cfg, summarizer, kw, lg, tr, cache, utils, api = nlp_env(KEYWORDS_TOP_K="6")
    text = (
        "Машинное обучение улучшает распознавание речи. "
        "Обучение моделей требует качественных данных. "
        "Машинное обучение распространено в индустрии."
    )
    kws = kw.extract_keywords(text, top_k=6, language="ru")
    assert any("машинное обучение" == k for k in kws), f"Нет ключа 'машинное обучение': {kws}"
    # важно: одиночное 'обучение' либо отсутствует, либо ниже по рангу
    assert "обучение" not in kws, f"Ожидали дедупликацию подстрок, получили: {kws}"

def test_keywords_en_basic(nlp_env):
    cfg, summarizer, kw, lg, tr, cache, utils, api = nlp_env(KEYWORDS_TOP_K="5")
    text = (
        "Neural networks improve speech recognition. "
        "Deep learning models require data. "
        "Neural networks are widely used."
    )
    kws = kw.extract_keywords(text, top_k=5, language="en")
    assert any("neural networks" == k for k in kws), f"Ожидали 'neural networks' среди ключей: {kws}"
