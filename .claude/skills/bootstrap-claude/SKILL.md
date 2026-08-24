---
name: bootstrap-claude
description: Set up this machine's Claude Code configuration from this repo — pick skills, subagents and safety hooks, then install them into ~/.claude with a backup and a reversible manifest. Use when the user types /bootstrap-claude, says "set up my Claude Code", "configure my environment", "install skills", or has just cloned this repo and wants it applied.
allowed-tools: Bash, Read, Glob, Grep, AskUserQuestion
---

# Bootstrap Claude Code

Turn this repo into a configured `~/.claude` in one conversation. You drive the
choices; `install.sh` does the file work and records what it did so it can be
undone.

## Ground rules

- **Work from the local clone.** The catalog, skills, agents and hooks are all in
  this repository. Never re-clone it, and never write to `/tmp`. The single
  exception is Step 1's reference fetch, which clones third-party repos into
  `references/`.
- **Never write config by hand.** Selection is your job; `install.sh` owns every
  write. It merges `settings.json` instead of replacing it, which hand-editing
  would get wrong.
- **Always preview before applying.** Run `--dry-run` and show the user the diff.
- **The user's existing config is theirs.** Anything already in `~/.claude` stays
  unless they explicitly ask otherwise.

## Step 1 — Read the catalog and fetch the reference library

```bash
python3 scripts/catalog.py --check   # regenerate + validate
python3 scripts/catalog.py --counts  # totals per domain
./install.sh --list                  # presets
```

`catalog.json` is the source of truth: every skill, agent and hook with its
name, description, domain and dependencies. Read from it, never guess a path.

Then pull the upstream reference repositories. **Do this automatically — do not
ask first.** It is part of setting the environment up, and it runs in the
background while you talk to the user:

```bash
bash scripts/fetch-references.sh
```

This clones the 11 repositories in `resources/reference-repos.json` into
`references/` (gitignored, shallow clones). They are the upstreams this repo was
built from plus the main community indexes, so once they are present you can
answer "is there a skill for X?" by searching them, not guessing:

```bash
rg -il "<topic>" references/ -g SKILL.md | head
find references -name SKILL.md | wc -l    # ~2600 available
```

If the network is unavailable the script reports failures per repo and keeps
going — never block setup on it. If the user is on a metered connection or says
they want a smaller footprint, re-run with `--skip-large`, which omits the one
219 MB repository.

Mention once, briefly, that these are third-party repos under their own
licenses, several with no `LICENSE` file — fine to read, check before reusing.

## Step 2 — Work out what they need

If the current directory is a project (not this repo), look before asking:

```bash
ls package.json pyproject.toml go.mod Cargo.toml pubspec.yaml 2>/dev/null
git branch --show-current 2>/dev/null
```

Use what you find to pre-select a preset. If there is no project — the user is
just setting up a machine — skip this entirely and go straight to asking.

## Step 3 — Ask

Use `AskUserQuestion`. Two stages, because 168 skill descriptions do not fit
usefully in one prompt.

**Stage 1 — the shape of their work.** Offer presets, with the one matching the
detected stack first and marked `(Recommended)`:

| preset | for |
|---|---|
| `backend-python` | FastAPI/Django services |
| `frontend-ts` | React/Next.js |
| `fullstack` | both ends |
| `devops` | pipelines, observability, incidents |
| `data-ai` | RAG, agents, ML |
| `mobile` | React Native, Flutter |
| `marketing` | SEO, content, CRO |
| `exec` | board, strategy, org |
| `minimal` | safety hooks + review only |

Always offer "Let me pick individually" as an option.

**Stage 2 — refinement.** Only if they asked to pick individually, or want to
add to a preset. Present skills from one domain at a time, `multiSelect: true`,
with the one-line description from the catalog. Do not paginate more than two
domains without checking they still want to continue.

Also ask about **safety hooks** unless a preset already covers it:

- `block-main-branch` — refuse edits on `main`/`master`
- `block-dangerous-commands` — refuse destructive shell commands
- `block-secret-reads` — refuse reads of `.env`, keys, credentials
- `auto-format` / `auto-lint` / `auto-test` — run tooling after each edit

Hooks need `jq`. Check with `command -v jq` and say so if it is missing —
the blocking hooks refuse to run rather than fail open.

## Step 4 — Preview

```bash
./install.sh --preset <name> --dry-run
# or
./install.sh --skills a,b,c --agents d,e --hooks f --dry-run
```

Show the user the counts and the `settings.json` changes. Call out anything
marked `locally modified` or `skipped` and explain why.

## Step 5 — Apply

```bash
./install.sh --preset <name>
```

It backs up `~/.claude` first and prints the restore command. Then confirm:

```bash
ls ~/.claude/skills ~/.claude/agents
python3 -c "import json;json.load(open('$HOME/.claude/settings.json'));print('settings ok')"
bash scripts/test-hooks.sh
```

Tell them to restart Claude Code, since skills and hooks are read at startup.

## Step 6 — Offer what is next

- `examples/` — real working configs, including a 15-agent project setup
- `references/` — the 11 upstream repos you cloned in Step 1; search them when
  the user wants something this catalog does not cover
- `guide/` — 11 chapters on how the pieces fit together
- `templates/stacks/` — per-stack `CLAUDE.md` supplements
- Project-level config: `templates/project/CLAUDE.md` and `.claude/settings.json`

Confirm the reference fetch finished and report how many landed:

```bash
ls references/ | wc -l
```

## If something goes wrong

| symptom | cause | fix |
|---|---|---|
| skill never triggers | missing frontmatter, or Claude Code not restarted | `python3 scripts/catalog.py --check`, then restart |
| hook does nothing | `jq` missing | install `jq` |
| hook blocks everything | matcher too broad | edit the entry in `~/.claude/settings.json` |
| want it all gone | — | `./install.sh --uninstall` |
| want the old config back | — | restore the `~/.claude.bak.*` printed at install |

## Do not

- Copy `skills/*` wholesale into `~/.claude/skills/` — the nesting is one level
  too deep and Claude Code will not discover them.
- Write `settings.json` yourself.
- Install every skill "to be safe". A large catalog dilutes triggering; start
  with a preset and add on demand.
