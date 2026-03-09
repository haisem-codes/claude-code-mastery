---
name: fastapi-patterns
description: FastAPI backend patterns for API development. Use when creating or modifying FastAPI endpoints, services, schemas, dependencies, or background tasks. Covers project structure, async decisions, Pydantic v2, dependency injection, error handling, and Celery integration.
user-invocable: false
---

# FastAPI Patterns

## Project Structure

```
app/
├── main.py              # FastAPI app, router includes
├── core/
│   ├── config.py        # Settings (Pydantic BaseSettings)
│   └── dependencies.py  # Shared deps (db session, auth)
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic request/response models
├── services/            # Business logic (not in routes)
├── api/
│   └── v1/
│       └── endpoints/   # Route handlers
└── tasks/               # Celery tasks (if applicable)
```

## async def vs def

```
async def → I/O-bound (database, HTTP calls, file I/O)
        → Using async drivers (asyncpg, httpx, aiofiles)
        → Want concurrent request handling

def       → CPU-bound work
        → Sync-only libraries (no async version)
        → FastAPI auto-runs in threadpool
```

**Async library picks:**
| Need | Library |
|------|---------|
| HTTP client | httpx |
| PostgreSQL | asyncpg / SQLAlchemy 2.0 async |
| Redis | redis-py async |
| File I/O | aiofiles |

## Dependency Injection

```python
# DB session (yield for cleanup)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# Current user (reusable)
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    ...

# Route usage
@router.post("/items")
async def create_item(
    data: ItemCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ItemResponse:
    return await item_service.create(db, data, user)
```

## Pydantic v2 Schemas

```python
# Separate Create / Update / Response schemas
class ItemBase(BaseModel):
    name: str
    price: Decimal

class ItemCreate(ItemBase):
    category_id: int

class ItemUpdate(BaseModel):  # All optional
    name: str | None = None
    price: Decimal | None = None

class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
```

## Error Handling

```python
# Domain exceptions in services
class NotFoundError(Exception):
    def __init__(self, resource: str, id: Any):
        self.resource = resource
        self.id = id

# Register handler once in main.py
@app.exception_handler(NotFoundError)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": f"{exc.resource} {exc.id} not found"},
    )
```

## Background Tasks

```
FastAPI BackgroundTasks → quick, fire-and-forget, same process
Celery                 → long-running, retries, distributed workers
```

```python
# Celery task pattern
@celery_app.task(bind=True, max_retries=3)
def process_ai_request(self, payload: dict):
    try:
        result = call_llm(payload)
        return result
    except RateLimitError as exc:
        self.retry(exc=exc, countdown=60)
```

## Testing

```python
# pytest + httpx async
@pytest.fixture
async def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_item(client, auth_headers):
    resp = await client.post("/api/v1/items", json={...}, headers=auth_headers)
    assert resp.status_code == 201
```

## Anti-Patterns

- Business logic in route handlers (move to services/)
- Sync libraries in async endpoints (blocks event loop)
- N+1 queries (use selectinload/joinedload)
- Hardcoded config (use Pydantic BaseSettings + env vars)
- Catching bare Exception (catch specific errors)
