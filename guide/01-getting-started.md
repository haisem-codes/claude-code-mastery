# Getting Started with Claude Code Configuration

> **What you'll learn:** The Claude Code configuration system, file hierarchy, and how to set up your first config in under 5 minutes.

## The Mental Model

Claude Code reads configuration from multiple locations, merged in this order (later overrides earlier):

```
~/.claude/CLAUDE.md          <- Global (all projects)
~/.claude/rules/*.md          <- Global rules (modular)
~/.claude/settings.json       <- Global permissions & hooks
~/.claude/skills/             <- Global skills (knowledge + tools)
~/.claude/agents/             <- Global subagents

.claude/CLAUDE.md             <- Project-level (this repo only)
.claude/rules/*.md            <- Project rules
.claude/settings.json         <- Project permissions & hooks
.claude/settings.local.json   <- Personal overrides (gitignored)
.claude/skills/               <- Project skills
.claude/agents/               <- Project agents

CLAUDE.md                     <- Project root (alternative location)
```

**Key principle:** Global config sets your baseline standards. Project config adds stack-specific details.

---

## Quick Start: 5-Minute Setup

### Step 1: Create the global directory

```bash
mkdir -p ~/.claude/rules ~/.claude/skills ~/.claude/agents
```

### Step 2: Create your global CLAUDE.md

```bash
cat > ~/.claude/CLAUDE.md << 'EOF'
# Global Development Standards

## Philosophy
- No speculative features -- only what's needed now
- No premature abstraction -- write it 3 times before extracting
- Clarity over cleverness -- readable beats clever
- Replace, don't deprecate -- remove old code entirely

## Code Quality
- Max 100 lines per function
- Fix every lint/typecheck warning
- Test behavior, not implementation

## Git
- Atomic commits: feat:, fix:, docs:, refactor:, test:
- Never commit .env, credentials, keys, tokens
- Feature branches only -- never push to main directly

## Security
- Validate all user input at system boundaries
- Parameterize SQL queries
- Pin exact dependency versions
EOF
```

### Step 3: Create a security rule

```bash
cat > ~/.claude/rules/security.md << 'EOF'
# Security Rules
- Never commit: .env, .key, .pem, credentials.json, API keys, tokens
- Use environment variables for all secrets
- Provide .env.example with placeholder values only
- Flag hardcoded secrets immediately
EOF
```

### Step 4: Create a verification rule

```bash
cat > ~/.claude/rules/verification.md << 'EOF'
# Verification Rules
After every code change:
1. Lint -- run the project linter
2. Typecheck -- run the type checker
3. Test -- run related tests (not full suite)
4. Review -- re-read your diff for unnecessary complexity

If 3+ consecutive fixes fail, STOP and ask the user.
EOF
```

### Step 5: Create your global settings.json

```bash
cat > ~/.claude/settings.json << 'SETTINGSEOF'
{
  "env": {
    "DISABLE_TELEMETRY": "1"
  },
  "permissions": {
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Bash(git push --force*)",
      "Bash(git reset --hard*)",
      "Read(~/.ssh/**)",
      "Read(~/.aws/**)",
      "Read(~/.git-credentials)"
    ]
  }
}
SETTINGSEOF
```

### Step 6: Verify it works

Start a new Claude Code session. Claude automatically loads your config on startup. Test it:

```
> What are my global development standards?
```

Claude should reference your CLAUDE.md content. If it does, your config is working.

---

## What Goes Where

| File | Purpose | Scope |
|------|---------|-------|
| `CLAUDE.md` | Development standards, philosophy, conventions | Global or project |
| `rules/*.md` | Modular rules (security, verification, etc.) | Global or project |
| `settings.json` | Permissions, hooks, environment variables | Global or project |
| `settings.local.json` | Personal overrides (gitignored) | Project only |
| `skills/` | Domain knowledge and tool skills | Global or project |
| `agents/` | Specialized subagent definitions | Global or project |

---

## Global vs Project Config

**Global config** lives in `~/.claude/` and applies to every project you open. Use it for:
- Your personal development philosophy
- Security rules you always want enforced
- Dangerous-command deny lists
- Cross-project skills (e.g., FastAPI patterns, PostgreSQL optimization)

**Project config** lives in `.claude/` inside your repo and is committed to git. Use it for:
- Stack-specific commands (`pytest -x -q`, `pnpm test`)
- Project architecture documentation
- Project-specific hooks (auto-format with the right tool)
- Skills unique to this codebase

**settings.local.json** lives in `.claude/` but is gitignored. Use it for:
- Personal MCP server configurations
- API keys or tokens that differ per developer
- Overriding team settings for local development

---

## The Override Chain in Practice

When Claude loads config, later files override earlier ones for the same keys.

**Example:** Your global CLAUDE.md says "Max 100 lines per function." Your project CLAUDE.md says "Max 50 lines per function." The project rule wins for that project.

**Hooks and permissions merge additively.** Global deny rules are not removed by project config -- they stack. A project can add more deny rules but cannot remove global ones.

**Skills inherit.** Global skills are available in every project. Project skills are available only in that project. If both define a skill with the same name, the project version takes precedence.

---

## Common Mistakes

### Too much prose in CLAUDE.md

```markdown
<!-- BAD: Claude skims this -->
When working on this project, please be mindful of the fact that we use
a microservices architecture and each service should be independently
deployable. The team has agreed that all API endpoints should follow
RESTful conventions and use proper HTTP status codes.

<!-- GOOD: Claude acts on this -->
## Architecture
- Microservices -- each service independently deployable
- RESTful APIs -- proper HTTP status codes
- No cross-service database queries
```

### Duplicating global rules in project config

If your global CLAUDE.md already says "Never commit .env files," do not repeat it in your project CLAUDE.md. It is already active.

### Putting secrets in settings.json

```jsonc
// BAD: This gets committed to git
{
  "env": {
    "OPENAI_API_KEY": "sk-abc123..."
  }
}

// GOOD: Use settings.local.json (gitignored)
// .claude/settings.local.json
{
  "env": {
    "OPENAI_API_KEY": "sk-abc123..."
  }
}
```

### Skipping the deny list

Without a deny list, Claude can run any shell command. At minimum, deny:
- `rm -rf` -- accidental recursive deletion
- `sudo` -- privilege escalation
- `git push --force` -- history rewriting
- `git reset --hard` -- losing uncommitted work
- `Read(~/.ssh/**)` -- reading SSH keys

---

## Directory Structure Reference

A fully configured setup looks like this:

```
~/.claude/
  CLAUDE.md                    # Global standards
  settings.json                # Global permissions + hooks
  rules/
    security.md                # Security rules
    verification.md            # Verification loop
  skills/
    fastapi-patterns/          # FastAPI reference knowledge
      SKILL.md
    postgres-optimization/     # PostgreSQL optimization
      SKILL.md
  agents/
    code-reviewer.md           # Specialized agent

your-project/
  .claude/
    CLAUDE.md                  # Project-specific standards
    settings.json              # Project hooks
    settings.local.json        # Personal overrides (gitignored)
    skills/
      deployment/              # Project-specific skill
        SKILL.md
  .gitignore                   # Must include .claude/settings.local.json
  src/
  ...
```

---

## Next Steps

- [Chapter 2: CLAUDE.md Deep Dive](02-claude-md.md) -- What to include, what to avoid
- [Chapter 3: Settings & Permissions](03-settings-and-permissions.md) -- Security-first configuration
- [Chapter 4: Hooks](04-hooks.md) -- Automated quality gates
- [Chapter 5: Skills](05-skills.md) -- Domain knowledge and tool skills
