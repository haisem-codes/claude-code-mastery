# The Setup Prompt

The setup prompt is the fastest way to get a production-grade Claude Code configuration for any project. It automatically clones this repo, analyzes your codebase, and installs the right skills, agents, and hooks for you.

## How to Use

1. Open Claude Code in your project directory
2. Copy the entire contents of [`setup-my-claude.md`](setup-my-claude.md)
3. Paste it as your first message to Claude Code
4. Answer the 5 questions Claude asks
5. Review and approve each batch (config files, skills, agents, hooks)

## What It Does

The prompt follows a 5-phase workflow:

1. **Clone** -- Clones this repo to `/tmp/claude-code-mastery` so Claude has access to all 190+ skills, 33 agents, and 10 hooks
2. **Analyze** -- Detects your tech stack, frameworks, tools, and existing config
3. **Report** -- Shows findings and asks 5 focused questions about scope, security, role, hooks, and skill domains
4. **Generate & Install** -- Creates tailored config, copies matching skills/agents/hooks from the repo
5. **Apply** -- Shows each batch for review before writing, then cleans up the temp clone

## What It Installs

| Category | What | Where |
|----------|------|-------|
| Global config | CLAUDE.md, settings.json, rules/ | `~/.claude/` |
| Project config | CLAUDE.md, settings.json | Project root + `.claude/` |
| Skills | Matched by stack + role from 190+ available | `~/.claude/skills/` |
| Agents | Matched by role from 33 available | `.claude/agents/` |
| Hooks | Matched by security level from 10 available | Integrated into `settings.json` |

## Skills Available by Domain

| Domain | Count | Examples |
|--------|-------|---------|
| Engineering | 63 | API design, CI/CD, code review, architecture |
| Marketing | 43 | SEO, content, ads, analytics, ASO |
| C-Suite Advisory | 34 | CEO, CFO, CMO, CISO, CTO advisors |
| Compliance | 12 | FDA, GDPR, ISO 27001, QMS |
| Product | 8 | Strategy, UX research, design systems |
| Project Management | 6 | Scrum, PM, Jira, Confluence |
| Business Growth | 4 | Sales, RevOps, contracts, CS |
| Finance | 1 | Financial analysis |
| Anthropic Official | 16 | PDF, DOCX, XLSX, web testing, skill creator |

## Tips

- Run it in your most important project first -- the global config applies everywhere
- For monorepos, run it at the root level
- If you already have a global config, choose "project config only" to avoid overwriting
- The cloned repo is automatically cleaned up after setup
- Re-run on other projects with "project config only" to add project-specific config without touching globals
