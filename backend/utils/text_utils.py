def clean_text(text: str) -> str:
    """
    Simple whitespace cleanup and normalization.
    """
    return " ".join(text.strip().split())
