# Examples

Working Claude Code configurations taken from real projects, then sanitized.
Everything here ran in production on someone's machine — these are not
hypothetical templates.

**Every file in this directory passes `python3 scripts/sanitize.py --check`,**
which fails the build on emails, phone numbers, IPs, home paths, client names,
tokens and credential-shaped strings. CI runs it on every push. If you contribute
an example, run the scrubber first:

```bash
python3 scripts/sanitize.py --scrub /path/to/your/.claude examples/projects/your-archetype
python3 scripts/sanitize.py --check
```

## Global configuration

| path | what to take from it |
|---|---|
| `global-config/CLAUDE.md` | A complete global memory file: never-do list, operating principles, context discipline, a verification loop, stack defaults. The `<!-- CUSTOMIZE -->` markers show what to change. |
| `global-config/settings.json` | 56 allow rules and 37 deny rules, tuned over months. The deny list is the interesting half. |
| `hooks/` | Four hooks that work: dangerous-command blocking, branch protection, secret-read guarding, and a session-start context injector. |
| `skills/` | Four small, sharp skills — `commit`, `verify`, `deep-research`, `memory-audit`. Good models for writing your own. |
| `agents/` | Two subagents, `code-reviewer` and `debugger`. Two, not twenty — see the note below. |
| `rules/` | Path-scoped rule files for security, verification and git hygiene. |
| `tools/` | Six stdlib-only Python CLIs, including `redaction_linter.py`, the scrubber this repo's own gate is built on. |

### Why only two global subagents

The global config deliberately ships two agents while `agents/` in this repo
offers 37. A large roster makes delegation *less* accurate: the model has to
choose among many similar descriptions, and picks worse. Start with two
well-scoped agents, add one when you feel a specific gap.

## Project configurations

Project-level `.claude/` directories. Each is a different shape of setup.

| archetype | what makes it worth reading |
|---|---|
| `projects/multi-agent-python/` | The most elaborate: **15 subagents**, 4 slash commands, a Stop-gate QA hook, and orchestration rules. This is what a mature multi-agent project config looks like. |
| `projects/nextjs-typescript/` | 14 agents and **42 project-scoped skills** — an example of pushing most capability into the project rather than the global config. |
| `projects/python-node-hybrid/` | A smaller, more typical setup for a mixed Python/Node repo. Start here if the other two feel like too much. |

Each contains `settings.json`, `agents/`, `commands/`, `hooks/`, `rules/` and
`skills/`. Machine-local files (`*.local.json`) are never included — they hold
per-machine allowlists and would not transfer anyway.

## Using these

Nothing here is installed by `install.sh`. They are reference material — read
them, copy the parts you want.

To adopt a project config wholesale:

```bash
cp -r examples/projects/multi-agent-python .claude
```

Then read `.claude/settings.json` before starting a session: the hook `command`
paths are relative to the original project and need adjusting, and the deny
rules may be stricter than you want.

## What is deliberately absent

- **Memory directories.** Auto-memory files hold credentials, client names and
  personal notes. None ship, and `scripts/sanitize.py` blocks the whole class.
- **`settings.local.json`.** Machine-scoped permission grants accreted from
  debugging sessions. Noise at best, leaks at worst.
- **MCP server configs with real endpoints.** See `templates/project/mcp.json`
  for the shape instead.
- **Plugin manifests.** They embed absolute install paths from the source
  machine. Reinstall plugins by name instead.
