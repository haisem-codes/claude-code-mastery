# Skills

> **What you'll learn:** Skills 2.0 features -- YAML frontmatter, invocation control, dynamic context injection, argument hints, directory structure, and progressive disclosure.

## What Are Skills?

Skills are structured knowledge files (SKILL.md) that give Claude domain expertise on demand. Unlike CLAUDE.md (always loaded), skills are activated only when relevant.

- **CLAUDE.md** = always loaded, project-wide standards
- **Skills** = loaded on demand, domain-specific expertise

---

## Anatomy of a Skill

```
skill-name/
  SKILL.md                    # Required: definition + instructions
  references/                 # Optional: deep knowledge (loaded on demand)
    frameworks.md
  templates/                  # Optional: user-fillable templates
    output-template.md
  scripts/                    # Optional: Python automation (stdlib only)
    analyzer.py
```

Every SKILL.md has two parts: YAML frontmatter and markdown body.

```markdown
---
name: fastapi-patterns
description: "FastAPI backend patterns for API development. Use when creating
  or modifying FastAPI endpoints, services, schemas, or background tasks."
user-invocable: false
---

# FastAPI Patterns

[Markdown body with instructions and examples]
```

---

## YAML Frontmatter

### Required fields

```yaml
---
name: skill-name                  # Unique identifier (kebab-case)
description: "Trigger keywords    # Claude reads this to decide activation
  and scenarios for this skill."
---
```

The `description` is critical -- Claude reads all skill descriptions to decide when to activate. Pack it with keywords and scenarios.

### Optional fields

```yaml
---
name: pr-workflow
description: "Create pull requests with proper titles and descriptions."
disable-model-invocation: true    # Manual-only (user must type /pr-workflow)
argument-hint: "[branch-name]"    # Autocomplete hint shown to user
user-invocable: false             # Background knowledge (no slash command)
---
```

---

## Three Invocation Modes

### 1. Auto-invocable (default)

Claude decides whether to activate based on the description and user prompt.

```yaml
---
name: systematic-debugging
description: "Four-phase debugging with root cause analysis. Use when
  investigating bugs, errors, crashes, or unexpected behavior."
---
```

When Claude sees "fix the login bug," it matches "bugs, errors" in the description and activates the skill.

### 2. Background knowledge (user-invocable: false)

Available as reference knowledge. No slash command. Claude activates it automatically when relevant.

```yaml
---
name: fastapi-patterns
description: "FastAPI backend patterns. Use when creating or modifying
  FastAPI endpoints, services, schemas, dependencies, or background tasks."
user-invocable: false
---
```

**Use for:** Framework patterns, database guides, security best practices -- knowledge Claude should use silently.

**Examples in this repo:**
- `fastapi-patterns` -- see [skills/reference/fastapi-patterns/SKILL.md](../skills/reference/fastapi-patterns/SKILL.md)
- `postgres-optimization` -- see [skills/reference/postgres-optimization/SKILL.md](../skills/reference/postgres-optimization/SKILL.md)
- `perf-profiler` -- see [skills/reference/perf-profiler/SKILL.md](../skills/reference/perf-profiler/SKILL.md)

### 3. Manual-only (disable-model-invocation: true)

Only activated when the user explicitly types the slash command.

```yaml
---
name: pr-workflow
description: "Create pull requests with proper titles and descriptions."
disable-model-invocation: true
argument-hint: "[branch-name]"
---
```

**Use for:** PR workflows, deployment procedures, database migrations -- actions that should only run on explicit request.

---

## Dynamic Context Injection

Skills can inject live data using `` !`command` `` syntax. The command runs when the skill loads, and its output replaces the placeholder.

```markdown
---
name: pr-workflow
description: "Create pull requests."
disable-model-invocation: true
argument-hint: "[branch-name]"
---

# PR Workflow

## Current State
- Branch: !`git branch --show-current`
- Commits ahead of main: !`git rev-list --count main..HEAD`
- Changed files: !`git diff --name-only main..HEAD`

## Recent Commits
!`git log --oneline main..HEAD`

## Instructions
1. Analyze the commits above
2. Draft a PR title (under 70 characters)
3. Create the PR with `gh pr create`
```

When the user types `/pr-workflow`, the commands execute and Claude sees actual git state.

**Rules:**
- Commands run in the project root directory
- Failed commands produce empty output
- Keep commands fast (< 2 seconds)
- Only use read-only commands (never mutate state)

---

## Arguments and $ARGUMENTS

Skills accept arguments from the user. The `argument-hint` provides autocomplete text, and `$ARGUMENTS` is replaced with user input.

```markdown
---
name: explain
description: "Explain a concept in simple terms."
argument-hint: "[topic]"
---

# Explain

Explain the following topic with practical code examples:

**Topic:** $ARGUMENTS
```

When the user types `/explain dependency injection`, Claude sees `**Topic:** dependency injection`.

---

## Progressive Disclosure

Claude loads skill content in two phases:

1. **Phase 1 (always loaded):** The `description` from frontmatter. Used to decide relevance.
2. **Phase 2 (on activation):** The full markdown body. Only loaded when triggered.

This means:
- 50 skills with good descriptions cost minimal tokens
- A 500-line SKILL.md only uses tokens when activated
- Files in `references/` are only read when the body tells Claude to read them

### Optimizing descriptions

```yaml
# GOOD: Rich trigger keywords
description: "FastAPI backend patterns. Use when creating or modifying
  FastAPI endpoints, services, schemas, Pydantic models, dependencies,
  middleware, or background tasks with Celery."

# BAD: Vague
description: "Patterns for backend development."
```

### Keeping SKILL.md lean

Keep SKILL.md under 10KB. Move detailed content to `references/`:

```markdown
## Endpoint Pattern
[Concise pattern with one example]

For the full catalog, see [references/response-patterns.md](references/response-patterns.md).
```

---

## Authoring a Skill: Step by Step

### Step 1: Create the directory

```bash
mkdir -p ~/.claude/skills/my-skill
```

### Step 2: Write SKILL.md

```markdown
---
name: my-skill
description: "Brief description with trigger keywords. Use when [scenarios]."
---

# My Skill

You are an expert in [domain]. Your goal is [specific outcome].

## Instructions
[What Claude should do when this skill is active]

## Patterns
[Reusable patterns with copy-paste examples]
```

### Step 3: Add references/scripts (optional)

Create `references/` for deep knowledge and `scripts/` for stdlib-only Python automation.

### Step 4: Test

Start a new Claude Code session, trigger the skill with a relevant prompt, and verify activation.

---

## Global vs Project Skills

**Global skills** (`~/.claude/skills/`) are available in every project. **Project skills** (`.claude/skills/`) are available only in that project. If both define a skill with the same name, the project version takes precedence.

Skills work even better with the [skill evaluation hook](04-hooks.md#skill-evaluation-engine) -- configure your skills in [skill-rules.json](../hooks/user-prompt-submit/skill-rules.json) for prompt-based activation.

---

## Anthropic Official Skills

Pre-built skills in [skills/anthropic-official/](../skills/anthropic-official/): `pdf`, `xlsx`, `docx`, `webapp-testing`, `skill-creator`, `frontend-design`, `mcp-builder`, and more.

---

## Quality Checklist

- [ ] YAML frontmatter with `name` and `description` (trigger keywords included)
- [ ] Invocation mode set if not default
- [ ] SKILL.md under 10KB (heavy content in `references/`)
- [ ] Practitioner voice ("You are an expert in X. Your goal is Y.")
- [ ] Concrete, copy-paste examples
- [ ] Scripts are stdlib-only Python with JSON output

See [AUTHORING-STANDARD.md](../skills/AUTHORING-STANDARD.md) for the full 10-pattern authoring guide.

---

## Summary: When to Use What

| Need | Solution |
|------|----------|
| Standards for every project | Global CLAUDE.md |
| Standards for one project | Project CLAUDE.md |
| Modular cross-cutting rules | `rules/*.md` |
| Domain expertise loaded on demand | Skill (auto-invocable) |
| Reference knowledge Claude uses silently | Skill (`user-invocable: false`) |
| Workflow triggered by slash command | Skill (`disable-model-invocation: true`) |
| Automated quality checks | Hooks (PreToolUse, PostToolUse) |
| Intelligent prompt analysis | Hook (UserPromptSubmit) |
