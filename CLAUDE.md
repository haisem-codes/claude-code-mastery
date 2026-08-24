# claude-code-mastery

A catalog of Claude Code skills, subagents, hooks and templates, plus an
installer that applies a chosen subset to a machine.

**If the user wants to set up their environment, run `/bootstrap-claude`.** That
skill owns the flow. Do not hand-copy files or hand-write `settings.json`.

## Layout

| path | what it is |
|---|---|
| `catalog.json` | generated index of everything installable — the source of truth |
| `presets.json` | curated bundles (`backend-python`, `devops`, `exec`, …) |
| `install.sh` | the installer: backup, merge, manifest, uninstall |
| `scripts/` | `catalog.py` (build + validate), `installer_lib.py` (merge engine), tests |
| `skills/` | 168 installable skills across 11 domains |
| `agents/` | 37 subagent definitions |
| `hooks/` | 8 hook scripts (`pre-tool-use/`, `post-tool-use/`, `user-prompt-submit/`) |
| `templates/` | `global/` and `project/` config, plus 6 per-stack supplements |
| `examples/` | real working configurations, sanitized |
| `references/` | 11 cloned upstream repos (gitignored) — search these for anything the catalog lacks |
| `resources/reference-repos.json` | the manifest driving `scripts/fetch-references.sh` |
| `guide/` | 11 chapters explaining the config system |
| `.claude/skills/bootstrap-claude/` | the setup skill itself |

## Reference repositories

`references/` holds shallow clones of the upstreams this repo was built from and
the main community indexes. `/bootstrap-claude` fetches them automatically; do it
manually with `./scripts/fetch-references.sh` (add `--skip-large` to omit the one
219 MB repo).

Search them before concluding a capability does not exist:

```bash
rg -il "<topic>" references/ -g SKILL.md
```

They are third-party and gitignored. Six have no stated license — readable, but
do not copy code out of them without checking. Never add `references/` content to
`skills/` or `examples/` without attribution in `CREDITS.md`.

## Working in this repo

Regenerate and validate the catalog after touching `skills/`, `agents/` or
`hooks/` — counts in the docs are derived from it, and CI checks it:

```bash
python3 scripts/catalog.py --check    # validate; non-zero on problems
python3 scripts/catalog.py            # rewrite catalog.json
bash scripts/test-hooks.sh            # hook block/allow contract
bash scripts/test-install.sh          # installer end-to-end
```

## Conventions that matter

- **Skill layout is `skills/<domain>/<skill>/SKILL.md`.** Installed flat as
  `~/.claude/skills/<skill>/SKILL.md`. Copying a domain directory wholesale
  produces a layout one level too deep and nothing is discovered.
- **Every `SKILL.md` needs `name` and `description` frontmatter.** Without both,
  Claude Code never triggers the skill. `catalog.py --check` enforces this.
- **Agents are keyed by frontmatter `name`, not filename.** Keep them equal;
  the validator fails when they drift.
- **Hooks read their payload as JSON on stdin**, e.g.
  `jq -r '.tool_input.command'`. There is no `$TOOL_INPUT` environment variable.
  Blocking hooks exit `2`; advisory hooks always exit `0`.
- **Nothing in `examples/` may contain real personal data.** `scripts/sanitize.py`
  gates it and CI runs it. See `examples/README.md`.

## Style

Match the surrounding files. Skills are practitioner-voiced and specific;
descriptions state what the skill does and when to invoke it. No emoji in
committed files.
