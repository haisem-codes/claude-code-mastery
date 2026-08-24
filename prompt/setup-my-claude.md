# Set up my Claude Code configuration

> **Prefer the skill.** If you have this repo open in Claude Code, just run
> `/bootstrap-claude` — it does everything below with proper multi-select menus.
> This file is the paste-in fallback for people who want a single prompt they
> can copy, or who are working from a different directory.

---

You are configuring my Claude Code environment from the `claude-code-mastery`
repository. Follow these phases in order. Do not skip the preview step.

## Phase 0 — Locate the repo

Work from a local clone. Do **not** clone a second copy into `/tmp`.

```bash
# if you are already inside the repo
test -f catalog.json && test -f install.sh && echo "found: $(pwd)"
```

If that fails, ask me where the clone is, or clone it once to a durable path:

```bash
git clone https://github.com/haisem-codes/claude-code-mastery.git ~/claude-code-mastery
cd ~/claude-code-mastery
```

Then read the catalog — it is the source of truth for every installable item:

```bash
python3 scripts/catalog.py --check
python3 scripts/catalog.py --counts
./install.sh --list
```

Never guess a skill or agent path. If it is not in `catalog.json`, it does not exist.

Then fetch the upstream reference library. Do this automatically, without asking:

```bash
bash scripts/fetch-references.sh
```

This clones 11 third-party repositories into `references/` (gitignored, shallow)
— the projects this repo was built from plus the main community indexes. Once
present, search them rather than guessing when I ask for something the catalog
does not cover:

```bash
rg -il "<topic>" references/ -g SKILL.md
```

Use `--skip-large` if I am on a metered connection; it omits one 219 MB repo.
Never block setup on this — if the network fails, report it and continue.

## Phase 1 — Understand the context

If I am inside a project, detect the stack before asking me anything:

```bash
ls package.json pyproject.toml go.mod Cargo.toml pubspec.yaml requirements.txt 2>/dev/null
ls next.config.* vite.config.* docker-compose.yml 2>/dev/null
git branch --show-current 2>/dev/null
```

Also check what I already have, so you do not propose to duplicate it:

```bash
ls ~/.claude/skills ~/.claude/agents 2>/dev/null
test -f ~/.claude/settings.json && python3 -m json.tool ~/.claude/settings.json | head -20
```

If there is no project — I am setting up a machine — skip this phase entirely.

## Phase 2 — Ask

Report what you found in a short table, then ask me:

1. **What kind of work?** Offer the presets from `./install.sh --list`, with the
   one matching my detected stack first. Presets: `backend-python`,
   `frontend-ts`, `fullstack`, `devops`, `data-ai`, `mobile`, `marketing`,
   `exec`, `minimal`. Always allow "let me pick individually".
2. **Safety hooks?** `block-main-branch`, `block-dangerous-commands`,
   `block-secret-reads` are the useful three. Auto-format/lint/test are
   available but run tooling on every edit, so mention the cost.
3. **Scope.** Global (`~/.claude`) or a separate profile via `--config-dir`.

If I chose "pick individually", show me skills one domain at a time using the
descriptions from `catalog.json`. Do not paste all 168 at once.

**Stop and wait for my answers.**

## Phase 3 — Preview

```bash
./install.sh --preset <chosen> --dry-run
```

Show me the output. Call out anything marked `skipped` or `locally modified` and
explain why. Confirm before applying.

## Phase 4 — Apply

```bash
./install.sh --preset <chosen>
```

Do not write `~/.claude/settings.json` yourself. The installer merges it —
preserving my `model`, `env`, `permissions.allow` and any other keys — which
hand-editing gets wrong.

Then verify:

```bash
ls ~/.claude/skills ~/.claude/agents
python3 -c "import json;json.load(open('$HOME/.claude/settings.json'));print('settings ok')"
bash scripts/test-hooks.sh
```

## Phase 5 — Project config, if I asked for it

Only if I said "project" or "both". Use the templates rather than writing from
scratch:

```bash
cp templates/project/CLAUDE.md ./CLAUDE.md
cp templates/project/settings.json ./.claude/settings.json
```

Then fill in the `<!-- CUSTOMIZE -->` sections from what you detected in Phase 1,
and append the matching stack supplement from `templates/stacks/`.

## Phase 6 — Wrap up

Tell me:

- what was installed, and where
- the backup path, and the command to restore it
- that I need to restart Claude Code for skills and hooks to load
- that `./install.sh --uninstall` reverses it
- that [`examples/`](../examples/) has real working configs worth reading,
  including a 15-subagent project setup

## Rules

- **Never** `cp -r skills/*` into `~/.claude/skills/` — the nesting is one level
  too deep and nothing will be discovered.
- **Never** hand-write `settings.json`.
- **Never** install everything. A large catalog makes skill triggering less
  accurate, not more.
- **Never** re-clone into `/tmp` and delete it afterwards.
