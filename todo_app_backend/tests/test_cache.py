from app.schemas import TaskCreate, TaskUpdate
from app.service import TASKS_CACHE_KEY, TaskService


def test_list_tasks_is_cached(db_session, cache):
    service = TaskService(db_session, cache)

    service.list_tasks()

    assert TASKS_CACHE_KEY in cache.data


def test_second_call_reads_from_cache(db_session, cache):
    service = TaskService(db_session, cache)
    cache.set(TASKS_CACHE_KEY, [{"id": "1", "title": "Из кэша", "completed": False}])

    tasks = service.list_tasks()

    assert tasks[0].title == "Из кэша"  # в базе пусто, значит ответ из кэша


def test_create_clears_cache(db_session, cache):
    service = TaskService(db_session, cache)
    service.list_tasks()

    service.create_task(TaskCreate(title="A"))

    assert TASKS_CACHE_KEY not in cache.data


def test_update_clears_cache(db_session, cache):
    service = TaskService(db_session, cache)
    task = service.create_task(TaskCreate(title="A"))
    service.list_tasks()

    service.update_task(task.id, TaskUpdate(completed=True))

    assert TASKS_CACHE_KEY not in cache.data
