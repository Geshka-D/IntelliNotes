def links_for_keywords(keywords):
    """
    Return simple wikipedia links for provided keywords.
    """
    return [f"https://en.wikipedia.org/wiki/{k.replace}" for k in keywords]
