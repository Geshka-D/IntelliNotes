def extract_keywords(text: str, top_k: int = 10):
    """
    Naive keyword extractor: returns unique words in order (lowercased),
    skipping very short tokens.
    """
    if not text:
        return []
    words = [w.strip(".,!?()[]\"'").lower() for w in text.split()]
    seen = set()
    out = []
    for w in words:
        if len(w) > 2 and w not in seen:
            seen.add(w)
            out.append(w)
        if len(out) >= top_k:
            break
    return out
