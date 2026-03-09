---
name: postgres-optimization
description: PostgreSQL query optimization and schema design patterns. Use when writing SQL queries, creating indexes, designing schemas, reviewing slow queries, or working with Alembic migrations. Covers indexing strategies, query performance, connection pooling, and common anti-patterns.
user-invocable: false
---

# PostgreSQL Optimization

## Indexing Strategy

```sql
-- Always index foreign keys
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Composite index: most selective column first
CREATE INDEX idx_orders_status_date ON orders(status, created_at);

-- Partial index: only index what you query
CREATE INDEX idx_orders_active ON orders(status)
  WHERE status IN ('pending', 'processing');

-- Covering index: avoid table lookups
CREATE INDEX idx_users_email_name ON users(email) INCLUDE (name);
```

**Index rules:**
- Every FK gets an index
- Composite indexes: leftmost column must appear in WHERE
- Partial indexes for filtered queries (save space)
- Don't over-index: each index slows writes

## Query Performance

```sql
-- Use EXPLAIN ANALYZE to diagnose
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ...;
```

**What to look for in EXPLAIN:**
| Pattern | Problem | Fix |
|---------|---------|-----|
| Seq Scan on large table | Missing index | Add targeted index |
| Nested Loop with high rows | N+1 join | Use Hash/Merge Join, add index |
| Sort with high cost | Sorting unindexed column | Add index matching ORDER BY |
| Bitmap Heap Scan Recheck | Low selectivity index | Use partial index or redesign |

**Query patterns:**
```sql
-- Pagination: keyset (fast) over OFFSET (slow)
SELECT * FROM items WHERE id > :last_id ORDER BY id LIMIT 20;

-- Batch operations: use ANY instead of IN for large lists
SELECT * FROM users WHERE id = ANY(:id_array);

-- Avoid SELECT *: fetch only needed columns
SELECT id, name, email FROM users WHERE active = true;

-- Use EXISTS over COUNT for existence checks
SELECT EXISTS(SELECT 1 FROM orders WHERE user_id = :uid);
```

## Schema Design

```sql
-- Use appropriate types
id          BIGSERIAL PRIMARY KEY     -- or UUID if distributed
created_at  TIMESTAMPTZ DEFAULT NOW() -- always use timezone-aware
status      TEXT CHECK(status IN (...))-- or enum type
price       NUMERIC(10,2)             -- never FLOAT for money
metadata    JSONB                     -- not JSON (indexable)

-- JSONB indexing
CREATE INDEX idx_meta_gin ON items USING GIN (metadata);
-- Query: WHERE metadata @> '{"category": "electronics"}'
```

## Connection Management

```
Pool sizing: connections = (cores * 2) + effective_spindle_count
Typical: 10-20 connections per service

Use PgBouncer for connection pooling:
├── transaction mode (default, best for web apps)
├── session mode (needed for prepared statements)
└── statement mode (most aggressive, limited use)
```

## Alembic Migration Patterns

```python
# Always: explicit, reversible migrations
def upgrade():
    op.add_column('users', sa.Column('phone', sa.String(20)))
    op.create_index('idx_users_phone', 'users', ['phone'])

def downgrade():
    op.drop_index('idx_users_phone')
    op.drop_column('users', 'phone')
```

**Migration safety:**
- Add columns as nullable first, backfill, then add NOT NULL
- Create indexes CONCURRENTLY for zero-downtime
- Never rename columns in one step (add new, migrate data, drop old)
- Test migrations on a copy of production data

## Anti-Patterns

- `SELECT *` in production queries (fetches unnecessary data)
- OFFSET-based pagination on large tables (scans all skipped rows)
- Missing indexes on foreign keys (slow JOINs and CASCADE)
- `COUNT(*)` for existence checks (scans entire result set)
- FLOAT/DOUBLE for monetary values (precision loss)
- JSON instead of JSONB (not indexable, stored as text)
- Long-running transactions (blocks vacuuming, causes bloat)
