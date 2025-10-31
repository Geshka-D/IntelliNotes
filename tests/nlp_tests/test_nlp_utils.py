# tests/test_nlp_utils.py
def test_normalize_and_detect(nlp_env):
    cfg, summarizer, kw, lg, tr, cache, utils, api = nlp_env()
    assert utils.normalize_ws("  a   b \n c ") == "a b c"
    assert utils.detect_lang("Привет мир") == "ru"
    assert utils.detect_lang("Hello world") == "en"

def test_split_sentences_and_tokens(nlp_env):
    cfg, summarizer, kw, lg, tr, cache, utils, api = nlp_env()
    text = "Привет! Как дела? Всё хорошо."
    sents = utils.split_sentences(text)
    assert sents == ["Привет!", "Как дела?", "Всё хорошо."]
    toks = utils.simple_tokens("OpenAI, версия 3.11!")
    assert toks == ["openai", "версия", "3", "11"]
