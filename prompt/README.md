# The Setup Prompt

The setup prompt is the fastest way to get a production-grade Claude Code configuration for any project.

## How to Use

1. Open Claude Code in your project directory
2. Copy the entire contents of [`setup-my-claude.md`](setup-my-claude.md)
3. Paste it as your first message to Claude Code
4. Answer the 5 questions Claude asks
5. Review and approve each generated config file

## What It Generates

| File | Purpose |
|------|---------|
| `~/.claude/CLAUDE.md` | Global development standards and philosophy |
| `~/.claude/settings.json` | Security permissions, deny lists, and hooks |
| `~/.claude/rules/security.md` | Secret handling and code safety rules |
| `~/.claude/rules/verification.md` | Lint/typecheck/test verification loop |
| `CLAUDE.md` | Project-specific config (stack, commands, dirs) |
| `.claude/settings.json` | Project-specific hooks (auto-format, auto-lint) |

## How It Works

The prompt follows a 4-phase workflow:

1. **Analyze** -- Detects your tech stack, frameworks, tools, and existing config
2. **Report** -- Shows findings and asks 5 focused questions
3. **Generate** -- Creates tailored config based on your answers
4. **Apply** -- Shows each file for review before writing

## Tips

- Run it in your most important project first -- the global config applies everywhere
- For monorepos, run it at the root level
- If you already have a global config, choose "project config only" to avoid overwriting
- After setup, install recommended skills and agents from this repo
- Re-run it on other projects with "project config only" to add project-specific config without touching globals
