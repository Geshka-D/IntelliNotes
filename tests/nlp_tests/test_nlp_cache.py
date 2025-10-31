# tests/test_nlp_cache.py
import time

def test_file_cache_roundtrip(tmp_path):
    from nlp_engine.cache import cache_get, cache_set
    store = tmp_path / "store.json"
    ns = "wikipedia"
    key = "ru:машинное обучение"
    val = {"x": 1}

    # пусто
    assert cache_get(str(store), ns, key, ttl_seconds=10) is None

    # записали → прочитали
    cache_set(str(store), ns, key, val)
    got = cache_get(str(store), ns, key, ttl_seconds=10)
    assert got == val

    # TTL
    got2 = cache_get(str(store), ns, key, ttl_seconds=0)
    assert got2 is None, "По истечении TTL значение должно пропадать"
