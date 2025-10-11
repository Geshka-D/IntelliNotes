import os

def save_bytes_file(content_bytes: bytes, filename: str, folder: str = "data/uploads") -> str:
    """
    Save bytes to disk and return path. Create folder if needed.
    """
    os.makedirs(folder, exist_ok=True)
    safe = filename.replace("/", "_").replace("\\", "_")
    path = os.path.join(folder, safe)
    with open(path, "wb") as f:
        f.write(content_bytes)
    return path
