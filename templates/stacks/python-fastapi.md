# Python + FastAPI Stack

## Runtime & Tooling

| Purpose | Tool |
|---------|------|
| Runtime | Python 3.12+ |
| Package Manager | uv |
| Lint & Format | ruff check, ruff format |
| Type Check | mypy (or pyright) |
| Test | pytest -x -q |
| Task Queue | Celery + Redis |

## Conventions

- Use `async def` for I/O-bound endpoints (database, HTTP, file)
- Use `def` for CPU-bound or sync-only libraries (FastAPI auto-threadpools)
- Async drivers: asyncpg, httpx, aiofiles, redis-py async
- Business logic in `services/`, not route handlers
- Separate Pydantic schemas: `Create`, `Update`, `Response`
- Dependency injection for DB sessions, auth, config
- Celery for long-running tasks (AI calls, file processing)

## Project Structure

```
app/
├── main.py
├── core/config.py, dependencies.py
├── models/          # SQLAlchemy
├── schemas/         # Pydantic v2
├── services/        # Business logic
├── api/v1/endpoints/
└── tasks/           # Celery
tests/
```

## Database

- PostgreSQL with SQLAlchemy 2.0 async
- Alembic for migrations (explicit upgrade + downgrade)
- Always index foreign keys
- Use TIMESTAMPTZ, NUMERIC for money, JSONB over JSON
