# Verification standard (Aegis)

The project verification loop. Complements the global verification rule; these are the exact
Aegis commands and gate semantics. Run after every meaningful code change.

## The loop
1. **Lint** — `uv run ruff check <changed-files>` (or `src tests` if scope-wide). Auto-fixable: `ruff check --fix`.
2. **Format** — `uv run ruff format <changed-files>`.
3. **Typecheck** — `uv run mypy src` (`--strict` is enabled in `pyproject.toml`).
4. **Test** — related first: `uv run pytest -q -k <name>`; then the file: `uv run pytest -q <path>`.
5. **Re-read the diff** — unnecessary complexity, dead code, leftover prints, accidental moves.

## Report format (one line each)
`✓ ruff (0 issues)  ✓ mypy (0 errors)  ✓ pytest 12/12 related pass`

## Full suite vs partial
- **Partial** (related tests) during a loop's inner iterations.
- **Full** (`uv run pytest -q`) before closing a loop, before a PR, after refactors touching 5+ files,
  and before tagging a release.

## Gate semantics
- A change cannot pass the loop's GATE with any lint error, type error, or failing test.
- The per-edit hooks auto-format and fast-lint each file; the full type+test gate runs in
  `qa-verifier` / the `verify` skill at VERIFY time. Don't rely on hooks alone — run `/verify`.

## Tool availability
- All tools run through `uv run` against the project venv. If `uv sync` hasn't run, do it first.
- Hooks degrade gracefully when a tool is missing (they warn, they don't falsely pass) — but the
  GATE still requires real green output from `qa-verifier`.

## Escalation
3+ consecutive failed fix attempts on the same issue → STOP. Document what was tried, the actual
failure mode, and the smallest reproducer; hand to `debugger` or raise to the user. Usually an
assumption/architecture problem, not a typo.
