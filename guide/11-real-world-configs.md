# 11. Real-World Configurations

Everything in [`examples/`](../examples/) came off a working machine. This
chapter is a reading guide: what to look at, and what each one demonstrates that
the templates cannot.

## The global config

[`examples/global-config/`](../examples/global-config/)

### `CLAUDE.md`

Roughly 60 lines, organised as: never-do → operating principles → context
discipline → verification loop → subagents → skills → git → stack defaults →
when stuck.

Three things worth stealing:

**The never-do list is first.** Prohibitions are cheap to check and expensive to
get wrong, so they go where the model reads first.

**Stack defaults are stated as preferences, not options.** "Python: `uv` (not
pip/conda/pyenv)" removes a decision the model would otherwise make differently
each session.

**It is bullets, not prose.** Every line is a rule. There is no narrative,
because narrative dilutes.

### `settings.json`

56 allow rules and 37 deny rules. The deny list is the interesting half — it
covers reads of `~/.ssh/**`, `~/.aws/**`, `**/.env`, `**/*.pem`, plus destructive
shell commands and force-push forms.

Note that the deny rules **overlap deliberately** with the hooks. Denies are
declarative and fast; hooks can inspect the actual command string and explain
themselves. Defence in depth: if one is misconfigured the other still catches it.

## The hooks

[`examples/hooks/`](../examples/hooks/) — four hooks that work in production.

All four follow the same contract, which is the one thing people get wrong:

```bash
CMD=$(jq -r '.tool_input.command // empty')   # payload is JSON on stdin
```

There is no `$TOOL_INPUT` environment variable. A hook that reads one silently
does nothing — it looks installed, reports no errors, and blocks nothing.

`session-start.sh` is the least obvious and most useful: it injects the current
git branch, the dirty-file count and a memory-size warning into the session as
context, so the model starts each session already knowing where it is.

## Project configurations

### `projects/multi-agent-python/` — 15 subagents

The most elaborate example, and worth reading even if you never build anything
like it. Its structure:

| piece | what it does |
|---|---|
| `agents/` (15) | roles: planner, principal-architect, backend-engineer, qa-verifier, security-auditor, teacher, research-scout, … |
| `commands/` (4) | `aegis-loop`, `phase-review`, `research-scan`, `standup` — multi-step workflows as slash commands |
| `hooks/stop/qa-gate.sh` | a **Stop hook**: quality gate that runs when the model tries to finish |
| `rules/orchestration.md` | the dispatch rules that decide which agent handles what |

The Stop-gate is the idea to take away. Instead of hoping the model verifies its
work, the hook runs at the moment it tries to stop and refuses if checks fail.

This config contradicts the "two subagents" advice in the global config, and
that is the point: **fifteen agents inside one project with explicit
orchestration rules works; fifteen global agents with no dispatch rules does
not.** Scope and routing are what make a large roster viable.

### `projects/nextjs-typescript/` — skills over agents

14 agents but **42 project-scoped skills**. The opposite bet: push capability
into skills, which load on demand, rather than agents, which need dispatch.

Compare `rules/` here with the multi-agent example — this one is shorter,
because skills carry their own trigger descriptions and need less routing.

### `projects/python-node-hybrid/` — the realistic one

A mixed Python/Node repo with a modest setup. If the other two feel like a lot,
this is closer to what most projects need.

## Reading a project config

Start with `settings.json`, then `rules/`, then spot-check two agents. The
`settings.json` tells you what the project refuses to allow, which is the fastest
way to understand what went wrong there before.

## Adopting one

```bash
cp -r examples/projects/python-node-hybrid .claude
```

Then, before your first session:

1. **Fix hook paths.** `command` strings point at the original project layout.
2. **Read the deny list.** It may be stricter than you want — the multi-agent
   example blocks edits outside `src/`, `tests/` and `docs/`.
3. **Delete agents you will not use.** An unused agent is not free; it competes
   for selection.

## What is not here, and why

No memory directories, no `settings.local.json`, no MCP configs with real
endpoints, no plugin manifests. The first two carry credentials and personal
notes; the last two embed absolute paths from the source machine and would not
work anywhere else.

`scripts/sanitize.py --check` enforces this in CI. If you contribute an example,
run `--scrub` first and read the diff yourself — an automated scrubber is a
safety net, not a substitute for looking.

Back to the [guide index](../README.md#learning-path).
