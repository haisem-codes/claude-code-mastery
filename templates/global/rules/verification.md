# Verification Rules

After every code change, run the verification loop before moving on:

1. **Lint** — Run the project linter (ruff/eslint/biome)
2. **Typecheck** — Run type checker (mypy/tsc/pyright)
3. **Test** — Run related tests only (not full suite)
4. **Review** — Re-read your diff for unnecessary complexity

## Full Test Suite
Run the complete test suite only:
- Before creating a PR
- When explicitly asked
- After major refactors touching 5+ files

## Escalation
- If 3+ consecutive fix attempts fail, STOP
- Document what you've tried and what you observed
- Ask the user before continuing — this signals an architecture issue
