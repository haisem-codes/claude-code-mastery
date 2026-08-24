# Verification rule

After any code change, in order (stop at first failure, fix, restart):
1. Lint+format: `pnpm biome check --write <changed-files>` (repo-wide: `pnpm turbo lint`)
2. Typecheck: `pnpm turbo typecheck` (per package: `pnpm --filter <pkg> typecheck`)
3. Tests (related only): `pnpm --filter <pkg> test -- <file-pattern>`
4. UI changes additionally: `pnpm --filter web build` + Playwright screenshot at 1440px and 390px
5. Re-read your own diff: dead code, leftover logs, accidental scope

Full suite (`pnpm turbo lint typecheck test build`) only: before PR, after refactors touching
5+ files, or when asked. Report one line per step: `OK biome (0)  OK tsc (0)  OK vitest 12/12`.
Integration tests need infra: `make up` first (postgres/redis/minio); they are env-gated and
skip cleanly when infra is down.
3+ failed fix attempts -> STOP, hand to debugger with reproducer.
