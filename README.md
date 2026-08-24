<div align="center">

# Claude Code Mastery

**The definitive guide to configuring Claude Code for maximum performance**

[![License: MIT](https://img.shields.io/badge/License-MIT*-blue.svg)](#license)
[![Skills](https://img.shields.io/badge/Skills-168-green)]()
[![Agents](https://img.shields.io/badge/Agents-37-purple)]()
[![Hooks](https://img.shields.io/badge/Hooks-8-orange)]()

*168 skills, 37 subagents, real working example configs, and an installer that sets up your machine in one command.*

[Quick Start](#quick-start) | [Skills](#skill-library) | [Agents](#agent-collection) | [Examples](examples/) | [Guide](#learning-path)

</div>

---

## What is this?

Stop configuring Claude Code by trial and error. This repository gives you:

- **A real installer** — pick a preset, get a configured `~/.claude`. It backs up first, merges instead of overwriting, and can be undone.
- **168 skills** across engineering, marketing, product, C-suite, compliance and finance
- **37 subagents** for development, infrastructure, security, data/AI and quality testing
- **[Working example configs](examples/)** taken from real projects, including a 15-subagent setup
- **8 hook scripts** for safety gates and auto-formatting, each smoke-tested
- **Templates** for `CLAUDE.md`, `settings.json`, rules and six stacks
- **11-chapter guide** from first principles to advanced patterns

Counts come from [`catalog.json`](catalog.json), which is generated and checked in CI, so the numbers on this page cannot drift.

---

## Quick Start

```bash
git clone https://github.com/haisem-codes/claude-code-mastery.git
cd claude-code-mastery
./install.sh --list
```

### Option 1: Let Claude do it (recommended)

Open this directory in Claude Code and run:

```
/bootstrap-claude
```

It reads the catalog, asks what kind of work you do, previews the exact changes,
and applies them. If you are inside a project it will detect your stack first and
pre-select a matching preset.

It also clones **11 upstream reference repositories** into `references/` — the
projects this repo was built from, plus the main community indexes — so Claude
can search them when you need something the catalog does not cover. See
[`resources/reference-repos.md`](resources/reference-repos.md).

### Option 2: Install a preset directly

```bash
./install.sh --preset backend-python --dry-run   # see what would change
./install.sh --preset backend-python             # apply it
```

Presets: `backend-python`, `frontend-ts`, `fullstack`, `devops`, `data-ai`,
`mobile`, `marketing`, `exec`, `minimal`.

### Option 3: Pick individual pieces

```bash
./install.sh --skills engineering/pr-review-expert,reference/fastapi-patterns \
             --agents debugger,code-reviewer-pro \
             --hooks pre-tool-use/block-main-branch
```

### What the installer guarantees

- **Backs up** `~/.claude` to a timestamped directory before the first write, and prints the restore command
- **Merges** `settings.json` — your `model`, `env`, `permissions.allow` and any other keys survive; deny rules and hooks are unioned in
- **Never clobbers your edits** — a file you changed after install is reported and skipped unless you pass `--force`
- **Reversible** — `./install.sh --uninstall` removes exactly what it installed, leaving your own skills alone
- **Idempotent** — run it as often as you like; unchanged files are skipped

Requires `python3` and `git`. Install `jq` too, or the safety hooks refuse to run
rather than failing open.

---

## What's Inside

| Directory | Contents | Description |
|-----------|----------|-------------|
| [`install.sh`](install.sh) | the installer | Backup, merge, manifest, uninstall |
| [`examples/`](examples/) | real configs | Sanitized working setups, incl. a 15-subagent project |
| [`skills/`](skills/) | 168 skills | Domain knowledge across 11 categories |
| [`agents/`](agents/) | 37 subagents | Specialized AI for delegated tasks |
| [`hooks/`](hooks/) | 8 scripts | Safety gates and auto-format, smoke-tested |
| [`templates/`](templates/) | 13 files | Global, project and per-stack config |
| [`guide/`](guide/) | 11 chapters | From first principles to advanced patterns |
| [`prompt/`](prompt/) | 1 prompt | Paste-in fallback if you prefer no scripts |
| [`github-actions/`](github-actions/) | 4 workflows | PR review, docs sync, quality, deps |

---

## Skill Library

168 installable skills organized by domain, plus 20 sub-skills bundled inside their parents. Install with `./install.sh --skills <domain>/<skill>` — see [skills/README.md](skills/README.md) for the manual-copy caveats.

<details>
<summary><b>C-Level Advisory — 28 skills</b></summary>

CEO, CFO, CMO, CTO, CISO, COO, CHRO, CPO, CRO advisor skills plus board-deck-builder, board-meeting, competitive-intel, company-os, change-management, chief-of-staff, culture-architect, decision-logger, executive-mentor, founder-coach, internal-narrative, intl-expansion, ma-playbook, org-health-diagnostic, scenario-war-room, strategic-alignment, cs-onboard, context-engine, and agent-protocol.

[Browse all &rarr;](skills/c-level-advisor/)
</details>

<details>
<summary><b>Engineering — 25 skills</b></summary>

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
<summary><b>Engineering Team — 23 skills</b></summary>

Senior architect, senior backend, senior frontend, senior fullstack, senior DevOps, senior QA, senior security, senior SecOps, senior data engineer, senior data scientist, senior ML engineer, senior prompt engineer, senior computer vision, AWS solution architect, Playwright pro, self-improving agent, incident commander, code reviewer, email template builder, MS365 tenant manager, Stripe integration expert, TDD guide, tech stack evaluator, and more.

[Browse all &rarr;](skills/engineering-team/)
</details>

<details>
<summary><b>Marketing — 42 skills</b></summary>

AI SEO, content creator, ad creative, A/B test setup, analytics tracking, app store optimization, brand guidelines, campaign analytics, churn prevention, cold email, content humanizer, content production, content strategy, copy editing, copywriting, email sequence, form CRO, free tool strategy, launch strategy, marketing context, marketing demand acquisition, marketing ideas, marketing ops, marketing psychology, marketing strategy PMM, onboarding CRO, page CRO, paid ads, paywall upgrade CRO, popup CRO, pricing strategy, programmatic SEO, prompt engineer toolkit, referral program, schema markup, SEO audit, signup flow CRO, site architecture, social content, social media analyzer, social media manager, and competitor alternatives.

[Browse all &rarr;](skills/marketing/)
</details>

<details>
<summary><b>Product — 8 skills</b></summary>

Product strategist, agile product owner, competitive teardown, UX researcher-designer, UI design system, SaaS scaffolder, product manager toolkit, landing page generator, and more.

[Browse all &rarr;](skills/product/)
</details>

<details>
<summary><b>Project Management — 6 skills</b></summary>

Scrum master, senior PM, Jira expert, Confluence expert, Atlassian admin, and Atlassian templates.

[Browse all &rarr;](skills/project-management/)
</details>

<details>
<summary><b>Compliance — 12 skills</b></summary>

FDA consultant specialist, GDPR/DSGVO expert, ISO 27001 information security manager, QMS audit expert, ISMS audit expert, MDR 745 specialist, CAPA officer, quality documentation manager, quality manager QMR, quality manager QMS ISO 13485, regulatory affairs head, risk management specialist.

[Browse all &rarr;](skills/compliance/)
</details>

<details>
<summary><b>Business Growth — 4 skills</b></summary>

Sales engineer, revenue operations, customer success manager, contract and proposal writer.

[Browse all &rarr;](skills/business-growth/)
</details>

<details>
<summary><b>Finance — 1 skill</b></summary>

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
| 10 | [Bootstrapping a Machine](guide/10-bootstrapping.md) | Practical | The installer, merge semantics, re-runs, uninstall |
| 11 | [Real-World Configurations](guide/11-real-world-configs.md) | Practical | Reading the example configs, incl. a 15-subagent setup |

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

This repository is MIT licensed — see [LICENSE](LICENSE) — **with one exception.**

The 16 skills under `skills/anthropic-official/` come from
[anthropics/skills](https://github.com/anthropics/skills) and are **not MIT**.
Each carries its own `LICENSE.txt` in its directory. Check it before
redistributing them.

Third-party content and its provenance is recorded in [CREDITS.md](CREDITS.md).
The upstream repositories cloned into `references/` keep their own licenses, six
of which state none at all — see
[resources/reference-repos.md](resources/reference-repos.md).

---

<div align="center">

**If this repo helped you, give it a star!**

</div>
