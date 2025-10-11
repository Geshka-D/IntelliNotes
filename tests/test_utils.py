from backend.utils.text_utils import clean_text

def test_clean():
    assert clean_text("  a  b ") == "a b"
