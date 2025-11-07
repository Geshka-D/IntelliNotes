# IntelliNotes

A full-stack lecture capture prototype combining:

- **FastAPI backend** for ingestion, transcription, summarisation and recordings
- **NLP engine** (Whisper / extractive summariser / keyword + link generator)
- **React (Vite) frontend** with an end-to-end dashboard
- **SQLite persistence** for generated notes and metadata

## Quick start

### Backend

`ash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
`

The API is exposed under http://localhost:8000/api. Static builds of the frontend are served from /app when dist/ exists.

### Frontend

`ash
npm install
npm run dev
`

The dev server runs on http://localhost:5173 and proxies requests to the backend. Build for production with 
pm run build.
### Start

Одной строкой
  - cmd /c "npm install && npm run build && venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000"
Если хотите dev-режим (автообновление на 3000)
  - В одном окне: venv\Scripts\python.exe -m uvicorn backend.main:app --reload
  - В другом: npm run dev
Открывайте: http://localhost:3000

## Key features

- Upload audio/video and receive automatic transcription, summary, keywords and enrichment links
- Record loopback audio on Windows via WASAPI (with graceful fallback when unavailable)
- Central note library with filtering, deletions and detailed view of summaries, decisions and full transcript
- Unified configuration via .env feeding backend and NLP modules

## Tests

Activate the virtual environment and run:

`ash
venv\Scripts\python.exe -m pytest
`

All unit/integration tests should pass (17 passed, 1 skipped at time of writing).
