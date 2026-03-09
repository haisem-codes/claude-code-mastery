# Chapter 9: Advanced Patterns for Power Users

This final chapter covers patterns that go beyond basic configuration. These are techniques for users who manage multiple projects, want automated skill matching, need parallel development environments, or want to squeeze maximum performance from Claude Code.

---

## 1. Skill Evaluation Hooks

The skill evaluation system automatically suggests relevant skills based on what you type. It runs as a `UserPromptSubmit` hook — analyzing your prompt before Claude sees it and injecting skill suggestions into the context.

### How It Works

```
You type a prompt
  → skill-eval.sh runs (UserPromptSubmit hook)
    → skill-eval.js parses the prompt
      → Matches against skill-rules.json
        → Returns: suggested skills with confidence scores
  → Claude receives your prompt + skill suggestions
```

### The Scoring System

Each skill in `skill-rules.json` defines triggers across multiple dimensions. When your prompt matches a trigger, it accumulates points:

| Trigger Type | Points | Example |
|-------------|--------|---------|
| `keyword` | 2 | "debug" matches the debugging skill |
| `keywordPattern` | 3 | `\btest(s\|ing)?\b` matches "testing" |
| `pathPattern` | 4 | `**/*.test.ts` matches when you mention test files |
| `directoryMatch` | 5 | Working in `src/components/` triggers component skills |
| `intentPattern` | 4 | "fix the bug in..." matches debugging intent |
| `contentPattern` | 3 | `useFormik` in context triggers form skill |
| `contextPattern` | 2 | "from the reviewer" triggers code review skill |

A skill must reach the `minConfidenceScore` (default: 3) to be suggested. The top 5 scoring skills are shown.

### Configuring Skill Rules

The `skill-rules.json` file defines all skill matching rules. Here is a condensed example:

```json
{
  "version": "2.0",
  "config": {
    "minConfidenceScore": 3,
    "showMatchReasons": true,
    "maxSkillsToShow": 5
  },
  "scoring": {
    "keyword": 2,
    "keywordPattern": 3,
    "pathPattern": 4,
    "directoryMatch": 5,
    "intentPattern": 4
  },
  "directoryMappings": {
    "src/components": "core-components",
    ".github/workflows": "github-actions",
    ".maestro": "maestro-e2e"
  },
  "skills": {
    "systematic-debugging": {
      "description": "Four-phase debugging with root cause analysis",
      "priority": 9,
      "triggers": {
        "keywords": ["bug", "debug", "fix", "error", "crash"],
        "intentPatterns": [
          "(?:fix|debug|resolve).*(?:bug|error|issue)",
          "(?:why).*(?:not working|broken|failing)"
        ]
      },
      "excludePatterns": ["fix typo", "fix formatting"]
    }
  }
}
```

### Adding a New Skill Rule

To add skill matching for a new skill:

1. Add an entry to the `skills` object in `skill-rules.json`
2. Define triggers that capture how users naturally describe the task
3. Add `excludePatterns` to prevent false matches
4. Set `priority` (1-10) to break ties between competing skills

```json
"api-endpoint": {
  "description": "FastAPI endpoint scaffolding",
  "priority": 7,
  "triggers": {
    "keywords": ["endpoint", "route", "api", "fastapi"],
    "keywordPatterns": ["\\bendpoint\\b", "\\broute\\b"],
    "pathPatterns": ["**/routers/**", "**/routes/**", "**/api/**"],
    "intentPatterns": [
      "(?:create|add|build).*(?:endpoint|route|api)",
      "(?:endpoint|route).*(?:for|that)"
    ]
  },
  "excludePatterns": ["api docs", "api key"]
}
```

### Installing the Hook

Add to your `settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/hooks/user-prompt-submit/skill-eval.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

The hook requires Node.js (for `skill-eval.js`) and `jq` (for JSON parsing). It exits silently if either is missing — it never blocks your prompt.

See the full implementation in [`hooks/user-prompt-submit/`](../hooks/user-prompt-submit/).

---

## 2. Status Line Customization

Claude Code displays a status line at the bottom of the terminal. You can customize it to show contextual information — git branch, token usage, environment, or anything your workflow needs.

### Using the `/config` Command

Run `/config` in Claude Code to access status line settings. The status line supports dynamic values that update as you work.

### Common Customizations

**Show git branch and status:**

```
{git_branch} | {modified_files} modified
```

**Show token usage:**

```
Tokens: {input_tokens} in / {output_tokens} out | Cost: ${session_cost}
```

**Show project context:**

```
{project_name} | {language} | {framework}
```

### Why This Matters

When managing multiple projects or long sessions, the status line gives you instant awareness of:

- Which branch you are on (prevents accidental edits on main)
- How much context you have consumed (signals when to start a new session)
- What project context is active

---

## 3. Git Worktrees for Parallel Work

Git worktrees let you check out multiple branches simultaneously in separate directories. Combined with Claude Code, this enables parallel development — one session per feature branch, each in its own worktree.

### Setting Up a Worktree

```bash
# From your main repo
git worktree add ../feature-auth feature/auth
git worktree add ../bugfix-login bugfix/login-redirect
```

This creates:

```
~/projects/
├── my-app/              # main branch (original repo)
├── feature-auth/        # feature/auth branch (worktree)
└── bugfix-login/        # bugfix/login-redirect branch (worktree)
```

### Using with Claude Code

Open separate Claude Code sessions in each worktree directory:

```bash
# Terminal 1
cd ~/projects/feature-auth
claude

# Terminal 2
cd ~/projects/bugfix-login
claude
```

Each session has its own:

- Working directory and branch context
- CLAUDE.md (if project-level config differs)
- Git state (staged files, uncommitted changes)

### Why Worktrees Beat Branches

| Approach | Problem |
|----------|---------|
| Single directory, switching branches | Stash/unstash juggling, risk of losing changes |
| Multiple clones | Wastes disk space, `.git` directory duplicated |
| Worktrees | Shared `.git`, separate working directories, zero stashing |

### Cleanup

```bash
# When done with a worktree
git worktree remove ../feature-auth

# List active worktrees
git worktree list
```

---

## 4. The `/loop` Command

The `/loop` command runs a recurring task at a specified interval. This is useful for monitoring, periodic checks, or iterative workflows.

### Basic Usage

```
/loop every 30m: run the test suite and report any new failures
```

```
/loop every 2h: check for TODO comments added in the last 2 hours
```

```
/loop every 1h: run lint and typecheck, fix any new issues
```

### Practical Applications

**Continuous test monitoring during development:**
```
/loop every 15m: run pytest tests/unit/ -x and summarize failures
```

**Periodic security checks:**
```
/loop every 4h: scan for hardcoded secrets, exposed ports, or SQL injection patterns in recently modified files
```

**Keep-alive code quality:**
```
/loop every 1h: run ruff check and mypy on files modified today, fix auto-fixable issues
```

### When to Use `/loop` vs. GitHub Actions

| Scenario | Use `/loop` | Use GitHub Actions |
|----------|-------------|-------------------|
| During active development | Yes | No |
| Monitoring a running server | Yes | No |
| Scheduled maintenance | No | Yes |
| PR-triggered reviews | No | Yes |
| One-off recurring checks | Yes | No |

`/loop` is for your local development session. GitHub Actions is for your team's CI/CD pipeline.

---

## 5. Multi-Project Configuration

When you manage multiple projects, organizing configuration at the right level prevents duplication and keeps each project focused.

### The Configuration Hierarchy

```
~/.claude/
├── CLAUDE.md                    # Global rules (apply everywhere)
├── settings.json                # Global settings + MCP servers
├── agents/                      # Global agents (available in all projects)
│   ├── code-reviewer.md
│   └── security-auditor.md
├── skills/                      # Global skills (reference knowledge)
│   ├── fastapi-patterns/
│   └── postgres-optimization/
└── rules/                       # Global rules (security, verification)
    ├── security.md
    └── verification.md

~/projects/my-app/
├── CLAUDE.md                    # Project-specific instructions
├── .mcp.json                    # Project MCP servers
└── .claude/
    ├── settings.json            # Project settings
    └── agents/                  # Project-specific agents
        └── api-endpoint.md
```

### What Goes Where

| Level | Content | Examples |
|-------|---------|---------|
| **Global CLAUDE.md** | Universal rules, never-do list | No rm -rf, no force push, no secret commits |
| **Global rules/** | Cross-cutting concerns | Security practices, verification loop |
| **Global agents/** | Reusable across projects | Code reviewer, security auditor |
| **Global skills/** | Reference knowledge | FastAPI patterns, Postgres optimization |
| **Project CLAUDE.md** | Stack-specific rules, commands | "Run `pnpm test` for tests", "Use Alembic for migrations" |
| **Project .mcp.json** | Project-specific tools | Context7 for library docs, Playwright for E2E |
| **Project agents/** | Project-specific workflows | API endpoint scaffolder, migration writer |

### Avoiding Duplication

- **Never duplicate global rules in project config.** Projects inherit from global automatically
- **Override only when the project diverges.** If your Python project uses `ruff` but your Node project uses `eslint`, put linter commands in project CLAUDE.md
- **Share agents via global, specialize via project.** A global `code-reviewer` works for any language. A project `fastapi-endpoint` is specific

### Example: Portfolio of Three Projects

```
# Global CLAUDE.md — applies to all three
- Never commit .env files
- Use conventional commits
- Run verification loop after every change

# Project A (FastAPI API)
CLAUDE.md:
  - Run `ruff check` for linting
  - Run `mypy` for typechecking
  - Run `pytest tests/` for tests
  - Database: PostgreSQL via SQLAlchemy

# Project B (Next.js Frontend)
CLAUDE.md:
  - Run `pnpm lint` for linting
  - Run `tsc --noEmit` for typechecking
  - Run `pnpm test` for tests
  - Framework: Next.js 14 with App Router

# Project C (Flutter Mobile App)
CLAUDE.md:
  - Run `dart analyze` for linting
  - Run `flutter test` for tests
  - State management: Riverpod
```

Each project gets only what is unique to it. Security rules, the verification loop, and general agents come from global config.

---

## 6. Context Management

Claude Code has a finite context window. As conversations grow, older context gets pushed out. Managing this window is critical for long sessions and complex tasks.

### Keep CLAUDE.md Concise

Your CLAUDE.md is loaded into every conversation turn. Every line costs tokens.

**Bad — 50 lines of prose:**

```markdown
## Introduction

This project is a comprehensive web application that provides
users with the ability to manage their tasks and projects. The
application is built using modern web technologies and follows
best practices for software development...
```

**Good — 8 lines of dense bullets:**

```markdown
## Stack
- FastAPI + SQLAlchemy + PostgreSQL
- Next.js 14 (App Router) frontend
- Redis for caching, Celery for async tasks

## Commands
- Lint: `ruff check src/`
- Test: `pytest tests/ -x`
- Types: `mypy src/`
```

**Target:** Under 100 lines for project CLAUDE.md. Move reference material to skills or separate docs.

### Use Subagents to Protect Context

When you need to explore a codebase or analyze multiple files, delegate to a subagent:

```
Analyze the authentication flow across all services.
Don't summarize the code — just tell me which files handle
token validation and where the middleware is configured.
```

The subagent's exploration happens in its own context. Only the final answer comes back to your main session — not the 50 files it read along the way.

**When to use subagents for context protection:**

- Searching for code patterns across many files
- Reading large files to extract specific information
- Comparing implementations across multiple modules
- Any exploratory work where the journey is not important, only the destination

### Progressive Disclosure with Skills

Instead of loading all knowledge into CLAUDE.md, use skills that load on demand:

```
CLAUDE.md (always loaded):
  - Stack, commands, key conventions — 50 lines

Skills (loaded when needed):
  - fastapi-patterns/   — loaded when working on endpoints
  - postgres-optimization/ — loaded when working on queries
  - env-secrets/        — loaded when handling configuration
```

This pattern keeps your base context small while making deep knowledge available when Claude needs it. Skills are loaded only when triggered by matching rules or explicit invocation.

### Signs You Need a Fresh Session

- Claude starts forgetting instructions from earlier in the conversation
- Responses become less accurate or more generic
- You are working on a completely different task than you started with
- The session has been running for several hours with many tool calls

When these happen, start a new session. Claude Code will reload your CLAUDE.md and start with a full context window.

### Session Checkpointing

Before ending a long session, ask Claude to summarize:

```
Summarize what we accomplished, what's pending, and any
decisions made. Format as bullet points I can paste into
the next session.
```

Paste this summary at the start of your next session to maintain continuity without carrying the full conversation history.

---

## Putting It All Together

A fully configured Claude Code setup combines these patterns:

1. **Global CLAUDE.md** — Universal rules, never-do list, operating principles
2. **Global hooks** — Safety gates (block dangerous commands, protect secrets)
3. **Skill evaluation** — Automatic skill suggestions based on prompt analysis
4. **Project CLAUDE.md** — Stack-specific commands and conventions
5. **Project MCP servers** — Tools specific to the project's needs
6. **Agents** — Specialized workers for complex, multi-step tasks
7. **GitHub Actions** — Automated reviews and maintenance in CI/CD
8. **Worktrees** — Parallel development across feature branches

Each layer is independent. You can adopt them incrementally — start with CLAUDE.md and hooks, add skills and agents as your workflow matures, and set up GitHub Actions when you are ready for automation.

You now have all the tools to configure Claude Code for maximum performance.

---

Previous: [Chapter 8 — GitHub Actions](./08-github-actions.md)
