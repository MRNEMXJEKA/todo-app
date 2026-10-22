import time

from sqlalchemy.orm import Session

from app.cache.redis import RedisCacheBackend
from app.repositories.repos import CategoryRepository, TaskRepository
from app.schemas import (
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
    TaskCreate,
    TaskRead,
    TaskUpdate,
)

TASKS_CACHE_KEY = "tasks"
CATEGORIES_CACHE_KEY = "categories"


class TaskNotFoundError(Exception):
    pass


class CategoryNotFoundError(Exception):
    pass


class TaskService:
    """Ключевые операции с задачами, включая бизнес-логику, валидацию и прочее"""

    def __init__(self, db: Session, cache: RedisCacheBackend):
        self.db = db
        self.repository = TaskRepository(db)
        self.cache = cache

    def list_tasks(self) -> list[TaskRead]:
        start = time.perf_counter()

        cached = self.cache.get(TASKS_CACHE_KEY)
        if cached is not None:
            print(f"Получение списка задач по кешу заняло {time.perf_counter() - start}")
            return [TaskRead.model_validate(item) for item in cached]

        tasks = [TaskRead.model_validate(t) for t in self.repository.get_all()]
        self.cache.set(TASKS_CACHE_KEY, [t.model_dump() for t in tasks])
        print(f"Получение списка задач заняло {time.perf_counter() - start}")
        return tasks

    def create_task(self, payload: TaskCreate) -> TaskRead:
        task = self.repository.create(title=payload.title)
        self.db.commit()
        self.db.refresh(task)
        self.cache.delete(TASKS_CACHE_KEY)  # список изменился — старый кэш больше не верен
        return TaskRead.model_validate(task)

    def update_task(self, task_id: str, payload: TaskUpdate) -> TaskRead:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError

        # только поля, которые клиент реально прислал
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        self.db.commit()
        self.db.refresh(task)
        self.cache.delete(TASKS_CACHE_KEY)
        return TaskRead.model_validate(task)

    def delete_task(self, task_id: str) -> None:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError

        self.repository.delete(task)
        self.db.commit()
        self.cache.delete(TASKS_CACHE_KEY)


class CategoryService:
    """Ключевые операции с категориями"""

    def __init__(self, db: Session, cache: RedisCacheBackend):
        self.db = db
        self.repository = CategoryRepository(db)
        self.cache = cache

    def list_categories(self) -> list[CategoryRead]:
        start = time.perf_counter()

        cached = self.cache.get(CATEGORIES_CACHE_KEY)
        if cached is not None:
            print(f"Получение списка категорий по кешу заняло {time.perf_counter() - start}")
            return [CategoryRead.model_validate(item) for item in cached]

        categories = [CategoryRead.model_validate(c) for c in self.repository.get_all()]
        self.cache.set(CATEGORIES_CACHE_KEY, [c.model_dump() for c in categories])
        print(f"Получение списка категорий заняло {time.perf_counter() - start}")
        return categories

    def create_category(self, payload: CategoryCreate) -> CategoryRead:
        category = self.repository.create(name=payload.name)
        self.db.commit()
        self.db.refresh(category)
        self.cache.delete(CATEGORIES_CACHE_KEY)
        return CategoryRead.model_validate(category)

    def update_category(self, category_id: str, payload: CategoryUpdate) -> CategoryRead:
        category = self.repository.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(category, field, value)

        self.db.commit()
        self.db.refresh(category)
        self.cache.delete(CATEGORIES_CACHE_KEY)
        return CategoryRead.model_validate(category)

    def delete_category(self, category_id: str) -> None:
        category = self.repository.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError

        self.repository.delete(category)
        self.db.commit()
        self.cache.delete(CATEGORIES_CACHE_KEY)
