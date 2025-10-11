def summarize(text: str) -> str:
    """
    Minimal summarizer:
    - return first sentence or first 200 chars
    """
    if not text:
        return ""
    parts = text.split(".")
    if len(parts) > 0 and len(parts[0].strip())>5:
        return parts[0].strip() + "."
    return (text[:200] + "...") if len(text) > 200 else text
