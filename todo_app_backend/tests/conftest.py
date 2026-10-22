import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.dependencies import get_category_service, get_task_service
from app.main import app
from app.models.base import Base
from app.service import CategoryService, TaskService


class FakeCache:
    """Подменяет Redis: хранит значения в обычном словаре."""

    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value

    def delete(self, key):
        self.data.pop(key, None)


@pytest.fixture
def db_session():
    """Отдельная база SQLite в памяти на каждый тест."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def cache():
    return FakeCache()


@pytest.fixture
def client(db_session, cache):
    """HTTP-клиент, у которого Postgres и Redis подменены на тестовые."""
    app.dependency_overrides[get_task_service] = lambda: TaskService(db_session, cache)
    app.dependency_overrides[get_category_service] = lambda: CategoryService(db_session, cache)
    yield TestClient(app)  # без `with`, чтобы не запускался lifespan с Postgres
    app.dependency_overrides.clear()
