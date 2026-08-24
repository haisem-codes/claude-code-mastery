# Skill Catalog

168 installable skills across 11 domains, plus 20 sub-skills bundled inside
their parent. Counts are generated into [`catalog.json`](../catalog.json).

## Installation

Use the installer. It resolves paths from the catalog, handles name collisions
between domains, and records what it installed so it can be undone:

```bash
./install.sh --skills engineering/pr-review-expert,reference/fastapi-patterns
./install.sh --preset backend-python          # a curated bundle
./install.sh --list                           # see all presets
```

### Copying by hand

Claude Code expects a **flat** skills directory — `~/.claude/skills/<name>/SKILL.md`.
The layout in this repo is one level deeper (`skills/<domain>/<name>/SKILL.md`),
so copy the skill directory itself, never the domain directory:

```bash
# correct — the skill directory lands directly under skills/
cp -r skills/engineering/pr-review-expert ~/.claude/skills/

# WRONG — produces ~/.claude/skills/engineering/<name>/SKILL.md,
# which is one level too deep and will never be discovered
cp -r skills/engineering ~/.claude/skills/
cp -r skills/* ~/.claude/skills/
```

Two skills share the name `brand-guidelines` (in `anthropic-official/` and
`marketing/`). Installing both by hand means one overwrites the other; the
installer prefixes them instead.

Restart Claude Code after installing — skills are read at startup.

## Domains

| Domain | Skills | Description |
|--------|--------|-------------|
| [anthropic-official](anthropic-official/) | 16 | Official Anthropic skills: pdf, docx, xlsx, pptx, webapp-testing, skill-creator, design, and more |
| [engineering](engineering/) | 26 | Software engineering: code review, debugging, architecture, testing, CI/CD, documentation |
| [engineering-team](engineering-team/) | 26 | Team practices: sprint planning, retros, onboarding, knowledge sharing, incident response |
| [marketing](marketing/) | 48 | Marketing strategy: content, SEO, social media, email campaigns, analytics, branding |
| [c-level-advisor](c-level-advisor/) | 31 | Executive advisory: CEO, CTO, CFO, COO, CMO strategy and decision frameworks |
| [compliance](compliance/) | 14 | Regulatory compliance: GDPR, SOC2, HIPAA, audit preparation, policy drafting |
| [product](product/) | 12 | Product management: roadmaps, user research, feature prioritization, launch planning |
| [project-management](project-management/) | 10 | Project execution: planning, tracking, risk management, stakeholder communication |
| [business-growth](business-growth/) | 5 | Growth strategy: market analysis, partnerships, scaling, competitive intelligence |
| [finance](finance/) | 2 | Financial operations: budgeting, forecasting, financial modeling |
| [reference](reference/) | 3 | Background knowledge skills: fastapi-patterns, postgres-optimization, perf-profiler |

## Skill Types

| Type | Frontmatter | Behavior | When to use |
|------|-------------|----------|-------------|
| **Auto-invocable** | _(defaults)_ | Claude and user can trigger | General-purpose skills |
| **Background knowledge** | `user-invocable: false` | Claude triggers automatically when relevant | Reference material, domain knowledge |
| **Manual-only** | `disable-model-invocation: true` | Only user triggers via `/name` | Destructive or high-stakes actions |

## Creating New Skills

See [AUTHORING-STANDARD.md](AUTHORING-STANDARD.md) for the full skill authoring guide, including:

- Required frontmatter fields
- Directory structure conventions
- Size limits and progressive disclosure
- Dynamic context injection with `!`command``
- Best practices for descriptions and trigger keywords

## Quick Start: Minimal Skill

```yaml
---
name: my-skill
description: Helps with X when the user mentions Y or Z.
---

## Instructions

1. Do this first
2. Then do this
3. Finally verify with this
```

Save as `~/.claude/skills/my-skill.md` or `~/.claude/skills/my-skill/SKILL.md`.
