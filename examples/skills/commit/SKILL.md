---
name: commit
description: Create an atomic Conventional Commit from currently-staged changes. Invoke when user types /commit, "commit this", "make a commit", or after finishing a logical unit of work.
allowed-tools: Bash
---

# /commit

Create one atomic commit with a Conventional Commits message and Claude co-author trailer.

## Procedure

1. **Sanity check:**
   ```bash
   git status -sb
   git diff --staged --stat
   ```
   - If nothing staged: show `git status` and ask what to stage. Do NOT `git add -A`.
   - If on `main`/`master`: refuse and tell user to create a feature branch.

2. **Inspect changes:**
   ```bash
   git diff --staged
   git log --oneline -5
   ```
   Match the repo's existing commit style.

3. **Compose message** following these rules:
   - Subject: `<type>(<optional-scope>): <imperative ≤72 chars>`
   - Types: feat, fix, docs, style, refactor, perf, test, chore, ci, build
   - Body: blank line, then ≤72-char-wrapped paragraph(s) explaining *why* (skip body for trivial docs/chore/style)
   - End with: blank line + `Co-Authored-By: Claude <you@example.com>`

4. **Commit via heredoc** (preserves formatting):
   ```bash
   git commit -m "$(cat <<'EOF'
   feat(api): add rate limiting to /search

   Endpoint was being hammered by clients without backoff, causing 5xx
   spikes on the Postgres pool. 100 req/min/IP via slowapi middleware.

   Co-Authored-By: Claude <you@example.com>
   EOF
   )"
   ```

5. **Verify:**
   ```bash
   git log -1 --stat
   ```

## Guards
- Never commit `.env`, `*.key`, `*.pem`, `credentials*`, files matching `*secret*` — abort and warn
- Never use `--amend` unless the user explicitly asked
- Never bypass hooks (no `--no-verify`) unless user explicitly asks
- If pre-commit hook fails: fix the issue, re-stage, make a **new** commit (not amend)

## Multi-commit splits
If the staged diff covers >1 logical change, propose a split:
```
This diff has:
  • feat: add caching to /users
  • fix: correct timezone handling in /events

Want me to make 2 separate commits? (y/n)
```
Wait for confirmation before committing.
