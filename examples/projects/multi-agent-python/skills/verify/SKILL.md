---
name: verify
description: Run the Aegis verification loop (ruff then mypy then pytest) on changed files and report a one-line PASS/FAIL per stage. Use at VERIFY, before commits/PRs, or when asked to "verify", "check changes", "lint and test".
allowed-tools: Bash(uv run ruff:*), Bash(uv run mypy:*), Bash(uv run pytest:*), Bash(uv sync:*), Bash(git diff:*), Read, Grep, Glob
---

# verify

The objective quality signal for the GATE. Applies `.claude/rules/verification.md`.

## When to use
- A change is at VERIFY, before a commit/PR, or any "is it green?" check.

## Steps
1. **Scope** — find changed files (`git diff --name-only`), or default to `src tests`.
2. **Lint** — `uv run ruff check src tests` (auto-fixable: `ruff check --fix`).
3. **Format check** — `uv run ruff format --check src tests`.
4. **Typecheck** — `uv run mypy src` (`--strict`).
5. **Test** — related first (`uv run pytest -q -k <name>`), then full (`uv run pytest -q`) when closing a loop.
6. Run `uv sync` first if the environment isn't ready.

## Report (one line each)
`✓ ruff (0 issues)  ✓ format  ✓ mypy (0 errors)  ✓ pytest 12/12`
On failure, show the failing output and STATUS=FAIL — never report PASS without green output.

## Rules
- Partial (related) tests during inner iterations; full suite before closing a loop / PR / release.
- Report faithfully: skipped steps, flaky tests, and missing tools are stated, not hidden.

## Related
- `deep-review` / `security-audit` — the human-judgment gates that complement this objective one.
