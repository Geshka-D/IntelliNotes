from nlp_engine.summarizer import summarize
from nlp_engine.keyword_extractor import extract_keywords

def generate_summary(text: str) -> str:
    """
    Wrapper: produce summary and possibly keywords/tags (MVP).
    """
    summary = summarize(text)
    # in future: call extract_keywords(text) and attach tags
    return summary
