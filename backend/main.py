from fastapi import FastAPI
from backend.api.routes import lecture_routes, note_routes, user_routes, record_routes
from backend.db import db_models, database
import uvicorn
#from fastapi.staticfiles import StaticFiles
from backend.core.config import settings
import os

app = FastAPI(
    title="System Audio Recorder API",
    description="API для записи, хранения и воспроизведения системного аудио",
    version="1.0.0"
)


# include routers
app.include_router(lecture_routes.router)
app.include_router(note_routes.router)
app.include_router(user_routes.router)
app.include_router(record_routes.router)

os.makedirs(settings.recordings_dir, exist_ok=True)

@app.get("/")
def root():
    return {
        "message": "HELLO"
    }
    
