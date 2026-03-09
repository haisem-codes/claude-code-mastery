<div align="center">

# Claude Code Mastery

**The definitive guide to configuring Claude Code for maximum performance**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-179%2B-green)]()
[![Agents](https://img.shields.io/badge/Agents-37-purple)]()
[![Hooks](https://img.shields.io/badge/Hooks-10-orange)]()

*179+ curated skills, 37 specialized agents, battle-tested templates, and a single prompt that builds your entire setup.*

[Quick Start](#-quick-start) | [Skills](#-skill-library) | [Agents](#-agent-collection) | [Guide](#-learning-path) | [Templates](#-configuration-templates)

</div>

---

## What is this?

Stop configuring Claude Code by trial and error. This repository gives you:

- **One-prompt setup** — Copy a single prompt into Claude Code, answer 5 questions, get a production-grade config
- **179+ skills** covering engineering, marketing, product, C-suite, compliance, finance, and more
- **37 specialized agents** for development, infrastructure, security, data/AI, and quality testing
- **Battle-tested templates** for CLAUDE.md, settings.json, rules, and stack-specific configs
- **10 hook scripts** for safety gates, auto-formatting, and intelligent skill matching
- **4 GitHub Actions** for automated PR review, docs sync, and dependency auditing
- **9-chapter guide** from beginner to advanced

---

## Quick Start

### Option 1: The Setup Prompt (Recommended)

Open Claude Code in your project, paste the contents of [`prompt/setup-my-claude.md`](prompt/setup-my-claude.md), and Claude will:

1. Analyze your codebase (stack, frameworks, tools)
2. Ask 5 focused questions about your preferences
3. Generate personalized global + project configuration
4. Apply files with your approval

**What it generates:**
| File | Purpose |
|------|---------|
| `~/.claude/CLAUDE.md` | Global development standards |
| `~/.claude/settings.json` | Security permissions & hooks |
| `~/.claude/rules/security.md` | Secret handling rules |
| `~/.claude/rules/verification.md` | Lint/typecheck/test loop |
| `.claude/CLAUDE.md` | Project-specific config |
| `.claude/settings.json` | Project hooks |

### Option 2: Manual Setup

1. Copy templates from [`templates/`](templates/) to your `~/.claude/` directory
2. Install skills from [`skills/`](skills/) to `~/.claude/skills/`
3. Install agents from [`agents/`](agents/) to `~/.claude/agents/`

---

## What's Inside

| Directory | Contents | Description |
|-----------|----------|-------------|
| [`prompt/`](prompt/) | 1 setup prompt | Auto-generates your entire Claude Code config |
| [`guide/`](guide/) | 9 chapters | Progressive learning from beginner to advanced |
| [`templates/`](templates/) | 13 files | Global, project, and stack-specific config templates |
| [`skills/`](skills/) | 179+ skills | Domain knowledge across 11 categories |
| [`agents/`](agents/) | 37 agents | Specialized AI for delegated tasks |
| [`hooks/`](hooks/) | 10 scripts | Safety gates, auto-format, skill matching |
| [`github-actions/`](github-actions/) | 4 workflows | Automated PR review, docs sync, quality, deps |

---

## Skill Library

179+ production-ready skills organized by domain. Install any skill by copying its directory to `~/.claude/skills/`.

<details>
<summary><b>C-Level Advisory — 29 skills</b></summary>

CEO, CFO, CMO, CTO, CISO, COO, CHRO, CPO, CRO advisor skills plus board-deck-builder, board-meeting, competitive-intel, company-os, change-management, chief-of-staff, culture-architect, decision-logger, executive-mentor, founder-coach, internal-narrative, intl-expansion, ma-playbook, org-health-diagnostic, scenario-war-room, strategic-alignment, cs-onboard, context-engine, and agent-protocol.

[Browse all &rarr;](skills/c-level-advisor/)
</details>

<details>
<summary><b>Engineering — 26 skills</b></summary>

| Skill | Description |
|-------|-------------|
| api-design-reviewer | REST API linting, breaking change detection, design scorecards |
| ci-cd-pipeline-builder | CI/CD pipeline design and optimization |
| codebase-onboarding | Automated codebase analysis and documentation |
| env-secrets-manager | .env lifecycle, secret leak detection, rotation workflows |
| pr-review-expert | Automated pull request review with checklists |
| mcp-server-builder | Design and build MCP servers |
| dependency-auditor | Dependency security scanning and updates |
| performance-profiler | CPU/memory profiling, query optimization, load testing |
| database-designer | Schema design, normalization, migration planning |
| rag-architect | RAG system design, vector search, embedding strategies |
| agent-designer | AI agent architecture and workflow design |
| agent-workflow-designer | Multi-agent orchestration patterns |
| api-test-suite-builder | API test generation and coverage |
| changelog-generator | Automated changelog from commit history |
| database-schema-designer | Advanced schema modeling |
| git-worktree-manager | Git worktree workflows |
| interview-system-designer | Technical interview system design |
| migration-architect | Database and system migration planning |
| monorepo-navigator | Monorepo tooling and navigation |
| observability-designer | Logging, metrics, tracing architecture |
| release-manager | Release planning and automation |
| runbook-generator | Operations runbook creation |
| skill-security-auditor | Skill file security analysis |
| skill-tester | Skill validation and testing |
| tech-debt-tracker | Technical debt identification and tracking |

[Browse all &rarr;](skills/engineering/)
</details>

<details>
<summary><b>Engineering Team — 24 skills</b></summary>

Senior architect, senior backend, senior frontend, senior fullstack, senior DevOps, senior QA, senior security, senior SecOps, senior data engineer, senior data scientist, senior ML engineer, senior prompt engineer, senior computer vision, AWS solution architect, Playwright pro, self-improving agent, incident commander, code reviewer, email template builder, MS365 tenant manager, Stripe integration expert, TDD guide, tech stack evaluator, and more.

[Browse all &rarr;](skills/engineering-team/)
</details>

<details>
<summary><b>Marketing — 44 skills</b></summary>

AI SEO, content creator, ad creative, A/B test setup, analytics tracking, app store optimization, brand guidelines, campaign analytics, churn prevention, cold email, content humanizer, content production, content strategy, copy editing, copywriting, email sequence, form CRO, free tool strategy, launch strategy, marketing context, marketing demand acquisition, marketing ideas, marketing ops, marketing psychology, marketing strategy PMM, onboarding CRO, page CRO, paid ads, paywall upgrade CRO, popup CRO, pricing strategy, programmatic SEO, prompt engineer toolkit, referral program, schema markup, SEO audit, signup flow CRO, site architecture, social content, social media analyzer, social media manager, and competitor alternatives.

[Browse all &rarr;](skills/marketing/)
</details>

<details>
<summary><b>Product — 9 skills</b></summary>

Product strategist, agile product owner, competitive teardown, UX researcher-designer, UI design system, SaaS scaffolder, product manager toolkit, landing page generator, and more.

[Browse all &rarr;](skills/product/)
</details>

<details>
<summary><b>Project Management — 8 skills</b></summary>

Scrum master, senior PM, Jira expert, Confluence expert, Atlassian admin, and Atlassian templates.

[Browse all &rarr;](skills/project-management/)
</details>

<details>
<summary><b>Compliance — 13 skills</b></summary>

FDA consultant specialist, GDPR/DSGVO expert, ISO 27001 information security manager, QMS audit expert, ISMS audit expert, MDR 745 specialist, CAPA officer, quality documentation manager, quality manager QMR, quality manager QMS ISO 13485, regulatory affairs head, risk management specialist.

[Browse all &rarr;](skills/compliance/)
</details>

<details>
<summary><b>Business Growth — 5 skills</b></summary>

Sales engineer, revenue operations, customer success manager, contract and proposal writer.

[Browse all &rarr;](skills/business-growth/)
</details>

<details>
<summary><b>Finance — 2 skills</b></summary>

Financial analyst.

[Browse all &rarr;](skills/finance/)
</details>

<details>
<summary><b>Anthropic Official — 16 skills</b></summary>

| Skill | Description |
|-------|-------------|
| pdf | Read, extract, merge, split, watermark, OCR PDF files |
| docx | Create, read, edit Word documents |
| xlsx | Create, read, edit spreadsheets |
| pptx | Create and edit PowerPoint presentations |
| webapp-testing | Test web apps with Playwright |
| skill-creator | Guide for creating new skills |
| brand-guidelines | Brand identity and style guide creation |
| canvas-design | Visual design with HTML Canvas |
| frontend-design | Frontend UI/UX design patterns |
| mcp-builder | Build MCP servers |
| algorithmic-art | Generative art and creative coding |
| doc-coauthoring | Collaborative document authoring |
| internal-comms | Internal communications drafting |
| slack-gif-creator | Slack GIF creation |
| theme-factory | Theme and styling generation |
| web-artifacts-builder | Interactive web artifact creation |

[Browse all &rarr;](skills/anthropic-official/)
</details>

<details>
<summary><b>Reference — 3 skills</b></summary>

Background knowledge skills (user-invocable: false) — loaded automatically when relevant:

| Skill | Description |
|-------|-------------|
| fastapi-patterns | FastAPI project structure, async, DI, Pydantic v2, Celery |
| postgres-optimization | Indexing, EXPLAIN ANALYZE, schema design, Alembic |
| perf-profiler | py-spy, cProfile, memory profiling, k6 load testing |

[Browse all &rarr;](skills/reference/)
</details>

---

## Agent Collection

37 specialized AI agents organized by domain. Install by copying to `~/.claude/agents/`.

<details>
<summary><b>Development — 14 agents</b></summary>

| Agent | Specialty |
|-------|-----------|
| frontend-developer | React, TypeScript, responsive design, accessibility |
| backend-architect | System design, microservices, API architecture |
| full-stack-developer | End-to-end web development |
| python-pro | Idiomatic Python, async/await, performance |
| typescript-pro | Type safety, advanced TS features |
| react-pro | React patterns, hooks, performance |
| nextjs-pro | SSR/SSG/ISR, App Router |
| golang-pro | Concurrent systems, goroutines, channels |
| mobile-developer | React Native/Flutter |
| electorn-pro | Desktop applications with Electron |
| ui-designer | Visual design, design systems |
| ux-designer | User experience, accessibility |
| dx-optimizer | Developer experience, tooling |
| legacy-modernizer | Refactoring, gradual modernization |

</details>

<details>
<summary><b>Infrastructure — 5 agents</b></summary>

| Agent | Specialty |
|-------|-----------|
| cloud-architect | AWS/Azure/GCP, cost optimization, Terraform |
| deployment-engineer | CI/CD, Docker/Kubernetes |
| performance-engineer | Bottleneck analysis, caching, profiling |
| devops-incident-responder | Production debugging, log analysis |
| incident-responder | Critical outages, crisis management |

</details>

<details>
<summary><b>Quality & Testing — 5 agents</b></summary>

| Agent | Specialty |
|-------|-----------|
| code-reviewer | Code quality, security, best practices |
| architect-review | Architectural consistency, design patterns |
| test-automator | Test strategy, Jest/Pytest/Playwright |
| debugger | Error analysis, root cause investigation |
| qa-expert | Testing strategy, QA processes |

</details>

<details>
<summary><b>Data & AI — 8 agents</b></summary>

| Agent | Specialty |
|-------|-----------|
| ai-engineer | LLM apps, RAG systems, prompt engineering |
| ml-engineer | ML pipelines, model serving |
| data-engineer | ETL, data warehouses, streaming |
| data-scientist | SQL, BigQuery, statistical analysis |
| database-optimizer | Query optimization, indexing, EXPLAIN |
| postgres-pro | PostgreSQL advanced features |
| graphql-architect | GraphQL schema, resolvers, federation |
| prompt-engineer | LLM prompt optimization |

</details>

<details>
<summary><b>Security — 1 agent</b></summary>

| Agent | Specialty |
|-------|-----------|
| security-auditor | Penetration testing, OWASP, threat modeling |

</details>

<details>
<summary><b>Business — 1 agent</b></summary>

| Agent | Specialty |
|-------|-----------|
| product-manager | Product roadmaps, market analysis |

</details>

<details>
<summary><b>Specialization — 2 agents</b></summary>

| Agent | Specialty |
|-------|-----------|
| api-documenter | OpenAPI/Swagger, API docs |
| documentation-expert | Technical writing, style guides |

</details>

<details>
<summary><b>Orchestration — 1 agent</b></summary>

| Agent | Specialty |
|-------|-----------|
| agent-organizer | Master orchestrator — analyzes projects and assembles optimal agent teams |

</details>

---

## Hooks Library

Ready-to-use hook scripts for safety, quality, and intelligence.

### Safety (PreToolUse)

| Hook | What it does |
|------|-------------|
| [`block-main-branch.sh`](hooks/pre-tool-use/block-main-branch.sh) | Prevents edits on main/master branch |
| [`block-dangerous-commands.sh`](hooks/pre-tool-use/block-dangerous-commands.sh) | Blocks rm -rf, sudo, force-push, hard-reset |
| [`block-secret-reads.sh`](hooks/pre-tool-use/block-secret-reads.sh) | Prevents reading .env, .key, .pem, credentials |
| [`enforce-package-manager.sh`](hooks/pre-tool-use/enforce-package-manager.sh) | Enforces a single package manager |

### Quality (PostToolUse)

| Hook | What it does |
|------|-------------|
| [`auto-format.sh`](hooks/post-tool-use/auto-format.sh) | Auto-formats with ruff/prettier/gofmt/rustfmt |
| [`auto-lint.sh`](hooks/post-tool-use/auto-lint.sh) | Auto-lints with ruff/eslint |
| [`auto-test.sh`](hooks/post-tool-use/auto-test.sh) | Runs related tests when test files change |

### Intelligence (UserPromptSubmit)

| Hook | What it does |
|------|-------------|
| [`skill-eval.sh`](hooks/user-prompt-submit/skill-eval.sh) + [`skill-eval.js`](hooks/user-prompt-submit/skill-eval.js) | Analyzes prompts and suggests relevant skills |
| [`skill-rules.json`](hooks/user-prompt-submit/skill-rules.json) | Configurable skill matching rules |

---

## Configuration Templates

Copy-paste templates for every part of the config system.

### Global Configuration

| Template | Purpose |
|----------|---------|
| [`global/CLAUDE.md`](templates/global/CLAUDE.md) | Development standards, philosophy, code quality |
| [`global/settings.json`](templates/global/settings.json) | Security permissions, deny lists, hooks |
| [`global/rules/security.md`](templates/global/rules/security.md) | Secret handling, code safety, dependencies |
| [`global/rules/verification.md`](templates/global/rules/verification.md) | Lint/typecheck/test/review loop |

### Project Configuration

| Template | Purpose |
|----------|---------|
| [`project/CLAUDE.md`](templates/project/CLAUDE.md) | Project-specific config with placeholders |
| [`project/settings.json`](templates/project/settings.json) | Project hooks (auto-format, auto-lint) |
| [`project/mcp.json`](templates/project/mcp.json) | MCP server configuration |

### Stack-Specific Templates

| Stack | Template |
|-------|----------|
| Python + FastAPI | [`stacks/python-fastapi.md`](templates/stacks/python-fastapi.md) |
| TypeScript + Next.js | [`stacks/typescript-nextjs.md`](templates/stacks/typescript-nextjs.md) |
| Flutter + Dart | [`stacks/flutter-dart.md`](templates/stacks/flutter-dart.md) |
| Go | [`stacks/golang.md`](templates/stacks/golang.md) |
| Rust | [`stacks/rust.md`](templates/stacks/rust.md) |
| React Native | [`stacks/react-native.md`](templates/stacks/react-native.md) |

---

## GitHub Actions

Automated workflows using Claude Code for continuous quality.

| Workflow | Trigger | What it does |
|----------|---------|-------------|
| [`pr-review.yml`](github-actions/pr-review.yml) | Every PR | Reviews diff for security, performance, quality |
| [`scheduled-docs-sync.yml`](github-actions/scheduled-docs-sync.yml) | Monthly | Updates outdated documentation |
| [`scheduled-quality.yml`](github-actions/scheduled-quality.yml) | Weekly | Reviews random directories for issues |
| [`scheduled-dependency-audit.yml`](github-actions/scheduled-dependency-audit.yml) | Biweekly | Audits and updates dependencies |

---

## Learning Path

A progressive guide from zero to production-grade Claude Code setup.

| # | Chapter | Level | What you'll learn |
|---|---------|-------|-------------------|
| 1 | [Getting Started](guide/01-getting-started.md) | Beginner | Config hierarchy, 5-minute setup |
| 2 | [CLAUDE.md Deep Dive](guide/02-claude-md.md) | Beginner | Global vs project config, what to include |
| 3 | [Settings & Permissions](guide/03-settings-and-permissions.md) | Beginner | Deny lists, security, environment |
| 4 | [Hooks](guide/04-hooks.md) | Intermediate | PreToolUse, PostToolUse, UserPromptSubmit |
| 5 | [Skills](guide/05-skills.md) | Intermediate | Skills 2.0, frontmatter, invocation control |
| 6 | [Agents](guide/06-agents.md) | Intermediate | Subagents, delegation, orchestration |
| 7 | [MCP Servers](guide/07-mcp-servers.md) | Intermediate | External integrations, recommended servers |
| 8 | [GitHub Actions](guide/08-github-actions.md) | Advanced | CI/CD automation with Claude Code |
| 9 | [Advanced Patterns](guide/09-advanced-patterns.md) | Advanced | Skill evaluation, worktrees, context management |

---

## Skill Authoring

Want to create your own skills? See the [Skill Authoring Standard](skills/AUTHORING-STANDARD.md) for the 10 patterns that make skills effective:

1. **Context-First** — Check for existing context before asking questions
2. **Practitioner Voice** — Expert coaching, not textbook prose
3. **Multi-Mode Workflows** — Build, optimize, and edge-case modes
4. **Related Skills Navigation** — When to use each, when NOT to
5. **Reference Separation** — SKILL.md for workflow, references/ for knowledge
6. **Proactive Triggers** — Surface issues without being asked
7. **Output Artifacts** — Map requests to concrete deliverables
8. **Quality Loop** — Self-verify before presenting
9. **Communication Standard** — Bottom line first, confidence tagging
10. **Python Tools** — Stdlib-only automation scripts

---

## Credits

This repo curates and builds upon work from these projects:

| Project | Author | What we sourced |
|---------|--------|----------------|
| [claude-skills](https://github.com/alirezarezvani/claude-skills) | Alireza Rezvani | 171 enterprise skills across 9 domains |
| [anthropic-skills](https://github.com/anthropics/skills) | Anthropic | 16 official document, design, and dev skills |
| [claude-code-sub-agents](https://github.com/lst97/claude-code-sub-agents) | Nelson (lst97) | 33 specialized subagent definitions |
| [claude-code-config](https://github.com/trailofbits/claude-code-config) | Trail of Bits | Security-first settings.json and deny lists |

---

## Contributing

Contributions welcome! Areas where you can help:

- Adding new skills (follow the [Authoring Standard](skills/AUTHORING-STANDARD.md))
- Adding new agents
- Improving guide chapters
- Submitting hook scripts

---

## License

MIT License — see [LICENSE](LICENSE)

---

<div align="center">

**If this repo helped you, give it a star!**

</div>
