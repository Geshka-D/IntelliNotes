from fastapi import FastAPI
from backend.api.routes import lecture_routes, note_routes, user_routes
from backend.db import db_models, database
import uvicorn
app = FastAPI(title="LectureNotesAI Backend")

# include routers
app.include_router(lecture_routes.router)
app.include_router(note_routes.router)
app.include_router(user_routes.router)

@app.on_event("startup")
def on_startup():
    # initialize database tables
    db_models.Base.metadata.create_all(bind=database.engine)


@app.get("/")
def root():
    return {"message": "LectureNotesAI backend running"}
if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)