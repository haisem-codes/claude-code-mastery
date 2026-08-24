# Global Claude Code Rules

<!-- CUSTOMIZE: one line about you and your stack. Claude reads this first.
     Name the languages, package managers and tools you actually use — it
     changes which commands Claude reaches for. Do not list hardware. -->

Senior engineer; Python + Node + Docker. Daily tools: uv, gh, docker, ruff, mypy,
pnpm, ripgrep. See `~/.claude/projects/<path>/memory/MEMORY.md` for per-project
context.

## Never do
- Read `.env`, `.env.*`, `.key`, `.pem`, `*credentials*`, `*.token`, `~/.ssh/**`, `~/.aws/**`, `~/.gnupg/**`, `~/.kube/**`, `~/.azure/**`, `~/.config/gh/**`, `~/.npmrc`, `~/.pypirc`, `~/.docker/config.json`
- Recursive force deletes, `sudo`, `mkfs`, `dd if=...`, `curl|bash`, `wget|bash`
- `git push --force`, `git reset --hard`, `git clean -f`, amend pushed commits
- Edit `~/.zshrc`, `~/.bashrc`, `~/.ssh/**` without explicit user request
- Push to `main`/`master`; always feature-branch
- Hardcode secrets; use env vars + `.env.example`
- Emojis in code/files/commits unless the user explicitly asks
- Write descriptions inside markdown files when asked for a description — reply in chat instead

## Operating principles
- Read before edit; smallest viable change; no speculative features, flags, or config
- Verify after change: lint → typecheck → relevant tests (not full suite)
- No premature abstraction; write it three times before extracting
- Replace, don't deprecate; remove old code when superseding
- Trust internal code/framework guarantees; validate only at system boundaries
- Default to no comments; add only when the *why* is non-obvious
- Don't reference the current task in comments ("added for issue #123") — that belongs in the PR description

## Context discipline
- Prefer `rg` + targeted `Read` over reading whole files
- Use the Explore subagent for cross-file searches spanning more than three queries
- Run independent subagents in parallel (single message, multiple Agent calls)
- Keep every `.md` config file lean — dense bullets, no prose
- If context fills: summarize, checkpoint, continue — never hand off mid-task

## Verification loop (after any code change)
1. Lint — Python: `uv run ruff check`; TS/JS: `pnpm eslint` or `oxlint`
2. Typecheck — Python: `uv run mypy`; TS: `pnpm tsc --noEmit`
3. Test — only related tests via `pytest -x -k <name>` or `pnpm test <file>`
4. Re-read your diff for unnecessary complexity and dead code
- Full suite only before a PR, or when asked
- Three failed fix attempts → stop, reassess, ask

## Subagents
<!-- CUSTOMIZE: keep this list short. Two well-scoped agents beat twenty vague
     ones — a crowded roster makes delegation less accurate, not more. -->
- **code-reviewer** — review the current diff for correctness and security
- **debugger** — reproduce and root-cause a failing test or runtime error
- Built-in: Explore (read-only search), Plan (architecture), general-purpose
- Use for: separate-context research, isolated verification, bounded specialized work
- Do not use for: simple lookups — call `Bash`/`Read`/`Grep` directly

## Skills (load on demand)
- `/verify` — the codified lint → typecheck → test loop
- `/commit` — atomic conventional commit with co-author trailer
- `/deep-research` — fan out across web, docs and code in parallel
- `/memory-audit` — prune stale auto-memory entries

## Git
- Atomic commits: only files you touched, explicit paths (never `git add -A`)
- Conventional commits: `feat:` `fix:` `docs:` `refactor:` `test:` `chore:` `perf:`
- Never commit `.env`, credentials, keys, tokens, large binaries, generated artifacts
- Co-author trailer on every Claude-authored commit:
  `Co-Authored-By: Claude <noreply@anthropic.com>`
- Identity is configured in `~/.gitconfig`; do not overwrite it

## Stack defaults
<!-- CUSTOMIZE: replace with your own. These are the strongest opinions in the
     file — they decide which tool Claude reaches for without asking. -->
- Python: `uv` (not pip/conda/pyenv); `ruff` for lint and format; `mypy --strict` for libraries; `pytest`; FastAPI for APIs
- Node/TS: `pnpm`; `eslint` + `tsc --noEmit`; `vitest` or `node:test`
- Docker: multistage builds; pin the base image SHA in prod; non-root `USER`
- Shell: prefer `gh`, `uv`, `pnpm`, `ruff`, `mypy`, `rg`, `fd`, `bat`, `jq`
- Avoid: `pip` (use `uv pip`), `npm` (use `pnpm`), `find` (use `fd`)

## When stuck or ambiguous
- One clarifying question maximum, then proceed with best judgment
- If told "no questions, just do it" — make the reasonable call, note it, continue
- If the user disagrees or redirects, adjust; don't argue
