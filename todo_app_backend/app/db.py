from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import get_settings

settings = get_settings()
engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    """Открывает сессию на время одного запроса и всегда закрывает её."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

