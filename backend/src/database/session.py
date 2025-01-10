# src/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.settings import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()