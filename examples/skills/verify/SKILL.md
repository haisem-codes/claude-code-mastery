---
name: verify
description: Run the full verification loop (lint → typecheck → related tests) on changed files. Invoke when the user types /verify or asks to "verify", "check changes", or "lint and test".
allowed-tools: Bash
---

# /verify

Run the verification loop against the current diff. Report each step on one line.

## Procedure

1. Find changed Python and TS files:
   ```bash
   PY=$(git diff --name-only HEAD --diff-filter=ACMR -- '*.py' 2>/dev/null)
   TS=$(git diff --name-only HEAD --diff-filter=ACMR -- '*.ts' '*.tsx' '*.js' '*.jsx' 2>/dev/null)
   ```

2. If `$PY` non-empty:
   - `uv run ruff check $PY`
   - `uv run mypy $PY` (or skip if no `pyproject.toml`)
   - `uv run pytest -x --quiet --no-header $(echo "$PY" | xargs -I{} dirname {} | sort -u)`

3. If `$TS` non-empty:
   - `pnpm eslint $TS`
   - `pnpm tsc --noEmit`
   - `pnpm test --run --reporter=dot $TS` (or `npx vitest run --reporter=dot $TS`)

4. Report (one line per check):
   ```
   ✓ ruff (0 issues)         ✗ ruff (3 issues in foo.py)
   ✓ mypy (0 errors)
   ✓ pytest 4/4 related tests pass
   ```

5. If any step fails, paste the relevant 10 lines of output and **stop**. Do not attempt fixes unless asked.

## When to skip
- If `git diff HEAD` is empty: report "no changes to verify" and exit
- If no Python/TS files changed and project is something else (Go/Rust/etc): adapt commands to that stack and run analogous steps
