from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings  # Issue 2: Single source of truth config

# Core engine initialized from your centralized settings file
engine = create_engine(settings.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
