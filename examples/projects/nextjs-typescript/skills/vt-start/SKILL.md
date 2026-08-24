---
name: vt-start
description: Boot the full local stack from cold — infra, migrations, apps, health checks. Use at session start or after environment changes.
---
1. Prereqs: `node -v` (>=22), `pnpm -v` (>=9), `docker compose version`. Missing -> stop, tell user.
2. `cp -n .env.example .env` (first run only; never overwrite).
3. `make up` -> wait for healthy: `docker compose ps` all "healthy" (retry 10x, 3s apart).
4. `pnpm install` (if node_modules missing or lockfile newer).
5. Migrations: `pnpm --filter @vt/db migrate`.
6. Health: `curl -s http://localhost:3001/health` -> {"status":"ok"}; worker log shows "stages registered".
7. Debug playbook: port busy -> `docker compose ps` + report; postgres unhealthy -> `docker logs vt-postgres --tail 20`; pnpm errors -> remove node_modules only with user approval.
Anti-Patterns: sudo anything; killing processes by pattern; overwriting .env.
Cross-References: Makefile, docker-compose.yml, rules/verification.md.
