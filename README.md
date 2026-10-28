# TODO App

![CI](https://github.com/MRNEMXJEKA/todo-app/actions/workflows/ci.yml/badge.svg)

Приложение для задач и категорий: REST API на FastAPI с PostgreSQL, кэшем в Redis и фоновыми задачами Celery, плюс готовый фронтенд на React.

Фронтенд взят из учебного шаблона [makedonsky-it/todo-app-frontend](https://github.com/makedonsky-it/todo-app-frontend). Бэкенд написан под его API-контракт.

## Стек

| Часть | Технологии |
| --- | --- |
| API | Python 3.14, FastAPI, Pydantic 2, Uvicorn |
| База данных | PostgreSQL 18, SQLAlchemy 2, Alembic |
| Кэш и брокер | Redis 8 |
| Фоновые задачи | Celery |
| Фронтенд | React (react-scripts), Axios |
| Тесты | pytest, FastAPI TestClient |
| Инфраструктура | Docker, docker-compose, GitHub Actions |

## Возможности

- CRUD для задач: создание, список, частичное обновление (`PATCH` только присланных полей), удаление.
- CRUD для категорий.
- Кэширование списков задач и категорий в Redis со сбросом кэша при любом изменении.
- Ответ `404` с понятным `detail` для несуществующих записей.
- Слоистая архитектура: роутер → сервис → репозиторий → модель.
- CI: тесты на каждый push и pull request, сборка Docker-образа и публикация в GitHub Container Registry при push в `main`.

## Структура проекта

```
todo-app/
├── .github/workflows/ci.yml     # CI/CD
├── docker-compose.yml           # Postgres, Redis, API, Celery worker
├── todo-app-frontend/           # React-фронтенд
└── todo_app_backend/
    ├── app/
    │   ├── main.py              # создание FastAPI-приложения, CORS, роутеры
    │   ├── config.py            # настройки из переменных окружения
    │   ├── db.py                # engine и сессия SQLAlchemy
    │   ├── dependencies.py      # зависимости FastAPI (сервисы, кэш)
    │   ├── celery.py            # приложение Celery
    │   ├── schemas.py           # Pydantic-схемы запросов и ответов
    │   ├── service.py           # бизнес-логика и работа с кэшем
    │   ├── models/              # ORM-модели (Task, Category)
    │   ├── repositories/        # доступ к данным
    │   ├── routers/             # эндпоинты /tasks и /categories
    │   └── cache/redis.py       # обёртка над Redis
    ├── migrations/              # Alembic
    ├── tests/                   # pytest
    └── requirements.txt
```

## API

Базовый URL: `http://localhost:8080`. Интерактивная документация: `http://localhost:8080/docs`.

### Задачи

| Метод | Путь | Тело запроса | Ответ |
| --- | --- | --- | --- |
| `GET` | `/tasks` | — | `200`, список задач |
| `POST` | `/tasks` | `{"title": "Сделать ДЗ"}` | `201`, созданная задача |
| `PATCH` | `/tasks/{id}` | `{"title": "...", "completed": true}` (любые поля) | `200`, обновлённая задача / `404` |
| `DELETE` | `/tasks/{id}` | — | `204` / `404` |

Пример задачи:

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "Сделать ДЗ",
  "completed": false
}
```

### Категории

| Метод | Путь | Тело запроса | Ответ |
| --- | --- | --- | --- |
| `GET` | `/categories` | — | `200`, список категорий |
| `POST` | `/categories` | `{"name": "Учеба"}` | `201`, созданная категория |
| `PATCH` | `/categories/{id}` | `{"name": "Работа"}` | `200` / `404` |
| `DELETE` | `/categories/{id}` | — | `204` / `404` |

Ошибка «не найдено»:

```json
{ "detail": "Task not found" }
```

## Запуск

### Вариант 1. Через Docker Compose

Нужен только Docker.

```bash
docker compose up --build
```

Поднимутся PostgreSQL (порт `5433` на хосте), Redis, API (`http://localhost:8080`) и Celery worker.

Фронтенд запускается отдельно:

```bash
cd todo-app-frontend
npm install
npm run dev
```

Он откроется на `http://localhost:3000`.

### Вариант 2. Локально

Нужны Python 3.14, Node.js и Docker (для PostgreSQL и Redis).

1. Запустить базу и Redis:

   ```bash
   docker run -d --name todo-db -e POSTGRES_PASSWORD=admin -p 5433:5432 \
     -v todo-pgdata:/var/lib/postgresql postgres:18
   docker run -d --name todo-redis -p 6379:6379 redis:8
   ```

2. Установить зависимости и запустить API:

   ```bash
   cd todo_app_backend
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8080
   ```

   Таблицы создаются автоматически при старте приложения.

3. Запустить фронтенд (в отдельном терминале):

   ```bash
   cd todo-app-frontend
   npm install
   npm run dev
   ```

## Переменные окружения

| Переменная | По умолчанию | Назначение |
| --- | --- | --- |
| `DATABASE_URL` | `postgresql+psycopg://postgres:admin@127.0.0.1:5433/postgres` | подключение к PostgreSQL |
| `REDIS_URL` | `redis://localhost:6379/0` | кэш |
| `CELERY_BROKER_URL` | `redis://localhost:6379/0` | брокер Celery |
| `CELERY_RESULT_BACKEND` | `redis://localhost:6379/0` | хранилище результатов Celery |

Значения по умолчанию рассчитаны на локальный запуск. В `docker-compose.yml` адреса переопределены на имена сервисов (`db`, `redis`).

## Тесты

```bash
cd todo_app_backend
pip install pytest httpx
pytest -v
```

Тестам не нужны запущенные PostgreSQL и Redis: в `tests/conftest.py` база подменяется на SQLite в памяти, а Redis на словарь. Покрыты все эндпоинты, ответы `404` и `422`, частичное обновление задач и сброс кэша после изменений.

## CI/CD

Workflow `.github/workflows/ci.yml`:

- **На каждый push и pull request** устанавливает зависимости и запускает `pytest`.
- **При push в `main`**, если тесты прошли, собирает Docker-образ бэкенда и публикует его:

  ```bash
  docker pull ghcr.io/mrnemxjeka/todo-backend:latest
  ```

## Планы

- [ ] Миграции Alembic вместо `create_all` при старте
- [ ] Настройки через `.env` и `pydantic-settings`
- [ ] Связь задач с категориями
- [ ] Регистрация пользователей и авторизация JWT
- [ ] Фильтры, поиск и пагинация
- [ ] Дедлайны и напоминания через Celery Beat
- [ ] Деплой
