def get_links_for_topic(topic: str):
    """
    Return simple Wiki link for a provided topic. Replace with search in future.
    """
    key = topic.replace(" ", "_")
    return [f"https://en.wikipedia.org/wiki/{key}"]
