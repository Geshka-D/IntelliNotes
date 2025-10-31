# nlp_engine/cache.py
import os, json, time, threading
from typing import Any, Optional

_lock = threading.Lock()

def _now() -> int:
    return int(time.time())

def _ensure_dir(path: str):
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)

def cache_get(store_path: str, namespace: str, key: str, ttl_seconds: int) -> Optional[Any]:
    try:
        with _lock:
            if not os.path.isfile(store_path):
                return None
            with open(store_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            ns = data.get(namespace, {})
            rec = ns.get(key)
            if not rec:
                return None
            if ttl_seconds >= 0 and _now() - int(rec.get("ts", 0)) >= ttl_seconds:
                return None
            return rec.get("val")
    except Exception:
        return None

def cache_set(store_path: str, namespace: str, key: str, value: Any) -> None:
    try:
        with _lock:
            _ensure_dir(store_path)
            data = {}
            if os.path.isfile(store_path):
                try:
                    with open(store_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception:
                    data = {}
            if namespace not in data:
                data[namespace] = {}
            data[namespace][key] = {"ts": _now(), "val": value}
            with open(store_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
