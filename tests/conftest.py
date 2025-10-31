import os, sys
from pathlib import Path

# Абсолютный путь к корню репозитория (папка, где лежит backend/, nlp_engine/, main.py)
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))