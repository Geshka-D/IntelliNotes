from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db import db_models, database
from backend.api.schemas.user_schema import UserOut

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/", response_model=UserOut)
def get_me(db: Session = Depends(database.get_db)):
    user = db_models.User(id=1, name="Demo user", email="demo@example.com")
    return user
