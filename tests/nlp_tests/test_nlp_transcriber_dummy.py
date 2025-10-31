# tests/test_nlp_transcriber_dummy.py
def test_transcriber_dummy_returns_placeholder(nlp_env):
    # Включаем заглушку
    cfg, summarizer, kw, lg, tr, cache, utils, api = nlp_env(
        STT_PROVIDER="dummy",
        DUMMY_TEXT_PREFIX="Dummy:"
    )
    # Файл может не существовать — dummy берёт только имя
    out = tr.transcribe_file("some_dir/sample.wav")
    assert isinstance(out, str) and "Dummy:" in out and "sample.wav" in out, \
        f"Ожидался плейсхолдер с именем файла, получили: {out!r}"
