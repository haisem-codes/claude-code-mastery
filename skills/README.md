# Skill Catalog

193 skills across 11 domains, ready to install.

## Installation

Copy any skill or entire domain to your global skills directory:

```bash
# Single skill
cp -r skills/engineering/code-review ~/.claude/skills/

# Entire domain
cp -r skills/engineering ~/.claude/skills/

# All skills
cp -r skills/* ~/.claude/skills/
```

Skills are recognized automatically after copying — no restart required.

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
