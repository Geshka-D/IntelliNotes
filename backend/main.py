import os
from pathlib import Path

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.routes import lecture_routes, note_routes, record_routes, user_routes
from backend.core.config import settings
from backend.db import database

app = FastAPI(
    title="LectureSynth API",
    description="Backend for transcription, summarisation and recording workflows.",
    version="1.0.0",
)

api_router = APIRouter(prefix="/api")
api_router.include_router(lecture_routes.router)
api_router.include_router(note_routes.router)
api_router.include_router(user_routes.router)
api_router.include_router(record_routes.router)
app.include_router(api_router)


@app.on_event("startup")
def on_startup() -> None:
    os.makedirs(settings.recordings_dir, exist_ok=True)
    database.init_db()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "HELLO"}


def _mount_frontend():
    repo_root = Path(__file__).resolve().parents[1]
    frontend_dist = repo_root / "dist"
    if not frontend_dist.exists():
        alt = repo_root / "build"
        if alt.exists():
            frontend_dist = alt
    if frontend_dist.exists():
        app.mount(
            "/app",
            StaticFiles(directory=str(frontend_dist), html=True),
            name="frontend",
        )


_mount_frontend()


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=False)
