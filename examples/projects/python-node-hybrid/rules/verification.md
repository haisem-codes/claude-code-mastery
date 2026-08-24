# Verification standard

The objective quality signal for the GATE. Two stacks, both must be green for a loop to close.

## Backend (`backend/` — Python 3.12, uv)
1. Lint: `uv run --project backend ruff check backend/src backend/tests`
2. Format check: `uv run --project backend ruff format --check backend/src backend/tests`
3. Types: `uv run --directory backend mypy src` (`--strict` per pyproject; MUST use
   `--directory`, not `--project` from root — mypy reads config from cwd, so the root form
   silently drops strict)
4. Tests: `uv run --project backend pytest -q` (related first via `-k <name>`, full when closing a loop)

## Frontend (`frontend/` — Vite + React + TS, pnpm)
1. Lint: `pnpm -C frontend lint` (eslint)
2. Types: `pnpm -C frontend exec tsc --noEmit`
3. Unit tests: `pnpm -C frontend test` (vitest)
4. Build: `pnpm -C frontend build` (when closing a loop — catches what dev mode hides)
5. E2E: `pnpm -C frontend exec playwright test` (when E2E specs exist and the change touches user flows)

## Scope
- Inner iterations: only the stack(s) the change touched, related tests only.
- Closing a loop / PR / release: both stacks, full suites.
- A stack that doesn't exist yet (early phases) is reported as "n/a", not silently skipped.

## Reporting
One line per stage: `✓ ruff (0)  ✓ format  ✓ mypy (0)  ✓ pytest 12/12  ✓ eslint (0)  ✓ tsc (0)  ✓ vitest 8/8`
On failure: show the failing output, STATUS=FAIL. Never claim PASS without green output captured.

## Escalation
3+ consecutive failed fix attempts on the same failure → STOP. Document what was tried, the
actual failure mode, the smallest reproducer. Ask the user — it's an assumption problem.
