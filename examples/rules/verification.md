# Verification rule

Loaded when touching `**/*.py`, `**/*.ts`, `**/*.tsx`, `**/*.js`, `**/*.jsx`, `**/*.go`, `**/*.rs`.

After every meaningful code change, run the verification loop:

1. **Lint**
   - Python: `uv run ruff check <changed-files>` (or `ruff check .` if scope-wide)
   - TS/JS: `pnpm eslint <changed-files>` or `pnpm dlx oxlint`
2. **Typecheck**
   - Python: `uv run mypy <module>`
   - TS: `pnpm tsc --noEmit`
3. **Test** — only related tests
   - Python: `uv run pytest -x -k <test-name-substring>`
   - TS: `pnpm test <file-pattern>`
4. **Re-read your own diff** with `git diff` — look for: unnecessary complexity, dead code, leftover prints/comments, accidental file moves

## When to run full test suite
- Before opening a PR
- When user explicitly asks
- After refactors touching 5+ files
- Before tagging a release

## Escalation
- If 3+ consecutive fix attempts fail, **STOP**
- Document: what you tried, what the failure mode actually is, the smallest reproducer
- Ask the user — this is almost always an architecture or assumption issue, not a typo

## Output reporting
After verification: report lint + typecheck + test status as one line each, e.g.:  
`✓ ruff (0 issues)  ✓ mypy (0 errors)  ✓ pytest 4/4 related tests pass`
