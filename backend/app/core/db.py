from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import os

# Create uploads directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Use SQLite for local development
if settings.LOCAL_DEV and settings.SKIP_DB:
    # Simple in-memory database for demo
    SQLALCHEMY_DATABASE_URL = "sqlite:///./nour.db"
else:
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency that provides database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
