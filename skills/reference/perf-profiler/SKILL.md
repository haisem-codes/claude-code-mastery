---
name: perf-profiler
description: Performance profiling for Python and PostgreSQL. Use when diagnosing slow endpoints, finding CPU/memory bottlenecks, optimizing database queries, detecting N+1 problems, or running load tests. Covers py-spy, cProfile, EXPLAIN ANALYZE, and k6.
user-invocable: false
---

# Performance Profiler

**Golden rule:** Measure first, optimize second. Record baseline before touching anything.

## Python CPU Profiling

```bash
# py-spy: profile running FastAPI/uvicorn (no code changes)
pip install py-spy
py-spy top --pid $(pgrep -f "uvicorn")
py-spy record -o flamegraph.svg --pid $(pgrep -f "uvicorn") --duration 30

# cProfile: function-level profiling
python -m cProfile -s cumulative app/scripts/benchmark.py 2>&1 | head -30
```

## Python Memory Profiling

```bash
pip install memory-profiler
python -m memory_profiler scripts/profile_function.py
```

```python
from memory_profiler import profile

@profile
def suspect_function():
    data = load_large_dataset()  # shows line-by-line memory delta
    return process(data)
```

## PostgreSQL Query Diagnosis

```sql
-- Enable pg_stat_statements
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Top 10 slowest queries by mean time
SELECT round(mean_exec_time::numeric, 2) AS mean_ms,
       calls,
       left(query, 80) AS query
FROM pg_stat_statements
WHERE calls > 10
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Diagnose specific query
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ...;
```

**EXPLAIN red flags:**
| Pattern | Problem | Fix |
|---------|---------|-----|
| Seq Scan on large table | Missing index | Add targeted index |
| Nested Loop + high rows | N+1 join | Add index or use JOIN |
| Sort with high cost | Unindexed ORDER BY | Add matching index |

## N+1 Detection

```python
# SQLAlchemy: enable echo to count queries per request
engine = create_engine(url, echo=True)

# Fix: use selectinload/joinedload
from sqlalchemy.orm import selectinload
stmt = select(Order).options(selectinload(Order.items))
```

## Load Testing with k6

```javascript
// tests/load/api-test.js
import http from 'k6/http'
import { check } from 'k6'

export const options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '1m',  target: 50 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
}

export default function() {
  const res = http.get(`${__ENV.BASE_URL}/api/v1/items`)
  check(res, { 'status 200': (r) => r.status === 200 })
}
```

```bash
k6 run --env BASE_URL=http://localhost:8000 tests/load/api-test.js
```

## Quick Wins Checklist

```
Database
- [ ] Missing indexes on WHERE/ORDER BY/FK columns
- [ ] N+1 queries (check query count per request)
- [ ] SELECT * when only 2-3 columns needed
- [ ] No LIMIT on unbounded queries
- [ ] Missing connection pool

Python/FastAPI
- [ ] Sync I/O in async endpoint (blocks event loop)
- [ ] No caching for expensive computations
- [ ] Serial awaits that could be asyncio.gather()
- [ ] Heavy computation in request handler (move to Celery)
```
