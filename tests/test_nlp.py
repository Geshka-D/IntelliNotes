from nlp_engine.summarizer import summarize

def test_summarize():
    text = "Hello world. This is a second sentence."
    s = summarize(text)
    assert "Hello" in s
