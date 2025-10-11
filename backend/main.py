from fastapi import FastAPI
from backend.api.routes import lecture_routes, note_routes, user_routes
from backend.db.database import init_db
import uvicorn
app = FastAPI(title="LectureNotesAI Backend")

# include routers
app.include_router(lecture_routes.router, prefix="/lectures", tags=["Lectures"])
app.include_router(note_routes.router, prefix="/notes", tags=["Notes"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])

@app.on_event("startup")
def on_startup():
    # initialize database tables
    init_db()

@app.get("/")
def root():
    return {"message": "LectureNotesAI backend running"}
if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)