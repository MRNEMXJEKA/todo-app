from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.service import CategoryService, TaskService

from app.cache.redis import RedisCacheBackend
from app.config import get_settings

settings = get_settings()
cache = RedisCacheBackend(
    settings.REDIS_URL, settings.cache_ttl_seconds
)


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(db, cache)


def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(db, cache)
