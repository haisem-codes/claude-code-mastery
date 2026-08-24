# Git hygiene rule

Loaded when the user mentions commit, push, PR, merge, branch, or invokes `/commit`.

## Branch
- Always work on a feature branch off `main`/`master`. Never edit on the default branch.
- Branch name: `<type>/<short-slug>` — e.g., `feat/uv-migration`, `fix/auth-timeout`, `docs/setup-notes`
- Default branch protection is enforced by a PreToolUse hook (blocks Edit on main).

## Commits
- One logical change per commit
- Stage only the files you touched: `git add path/to/specific/file.py` — never `git add -A` or `git add .`
- Message format (Conventional Commits):
  ```
  <type>(<optional-scope>): <imperative subject, ≤72 chars>

  <body — wrap at 72, explain *why*, not what>

  Co-Authored-By: Claude <you@example.com>
  ```
- Types: `feat` `fix` `docs` `style` `refactor` `perf` `test` `chore` `ci` `build`
- Subject in imperative mood: "add X" not "added X" / "adds X"

## Bodies — when to include
- Always for `feat:`, `fix:`, `refactor:`, `perf:`
- Skip body for trivial `docs:` / `chore:` / `style:` (subject only is fine)
- The body answers "why this change matters", not "what changed" — the diff already shows what

## Never
- `git push --force` (use `--force-with-lease` only when explicitly asked, never on main/master)
- `git reset --hard` without warning the user about the work they're about to lose
- `git rebase -i` in scripts (interactive flag won't work)
- Amend commits already pushed — make a new commit

## PR-time checks (before `gh pr create`)
- All commits compile and pass lint/type/test
- No `WIP` / `fixup!` / debug commits — squash or rebase first
- PR title follows Conventional Commits (it becomes the squash-merge subject)
- Body has Summary + Test plan + Linked issue (if any)
