---
name: verify
description: Run the Notetaker verification loop on both stacks (ruff/mypy/pytest for backend, eslint/tsc/vitest for frontend) and report a one-line PASS/FAIL per stage. Use at VERIFY, before commits/PRs, or when asked to "verify", "check changes", "lint and test".
allowed-tools: Bash(uv run:*), Bash(uv sync:*), Bash(pnpm:*), Bash(git diff:*), Read, Grep, Glob
---

# verify

The objective quality signal for the GATE. Applies `.claude/rules/verification.md`.

## When to use
- A change is at VERIFY, before a commit/PR, or any "is it green?" check.

## Steps
1. **Scope** — find changed files (`git diff --name-only`); run only the stack(s) touched
   during inner iterations, both stacks in full when closing a loop.
2. **Backend** (if `backend/**` touched or closing):
   `uv run --project backend ruff check backend/src backend/tests` →
   `uv run --project backend ruff format --check backend/src backend/tests` →
   `uv run --directory backend mypy src` (NOT `--project` from root — strict config needs cwd=backend/) →
   `uv run --project backend pytest -q` (related via `-k <name>` first).
3. **Frontend** (if `frontend/**` touched or closing):
   `pnpm -C frontend lint` → `pnpm -C frontend exec tsc --noEmit` →
   `pnpm -C frontend test` → `pnpm -C frontend build` (closing only) →
   `pnpm -C frontend exec playwright test` (when E2E specs exist and flows changed).
4. Run `uv sync --project backend` / `pnpm -C frontend install` first if an environment isn't ready.
5. A stack that doesn't exist yet is reported "n/a", never silently skipped.

## Report (one line each)
`✓ ruff (0)  ✓ format  ✓ mypy (0)  ✓ pytest 12/12  |  ✓ eslint (0)  ✓ tsc (0)  ✓ vitest 8/8`
On failure, show the failing output and STATUS=FAIL — never report PASS without green output.

## Rules
- Partial (related) tests during inner iterations; full suites before closing a loop / PR / release.
- Report faithfully: skipped steps, flaky tests, and missing tools are stated, not hidden.
