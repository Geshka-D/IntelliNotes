# Optional: SQLAlchemy connection placeholder
from sqlalchemy import create_engine
engine = create_engine("sqlite:///./data/lecture_notes.db", connect_args={"check_same_thread": False})
