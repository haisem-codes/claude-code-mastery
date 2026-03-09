# Skills 2.0 Reference

A complete reference for Claude Code Skills 2.0 frontmatter fields and features.

## YAML Frontmatter

Every skill requires a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: skill-name                    # Required: kebab-case identifier
description: When to use this...    # Required: trigger keywords for auto-matching
user-invocable: false              # Optional: false = background knowledge only
disable-model-invocation: true     # Optional: true = only user can trigger via /name
argument-hint: "[branch-name]"     # Optional: autocomplete hint for /name
license: MIT                       # Optional: license information
---
```

## Frontmatter Fields

### name (required)
- Kebab-case identifier: `my-skill-name`
- Used for `/name` invocation
- Must be unique within the scope (global or project)

### description (required)
- Always loaded into context (~100 words recommended)
- Include trigger keywords users would naturally mention
- Claude uses this to decide when to apply the skill
- Budget: ~2% of context window across all skill descriptions

### user-invocable
- `true` (default): Both Claude and user can trigger
- `false`: Only Claude can invoke (background knowledge)
- Use `false` for reference skills that should load automatically when relevant

### disable-model-invocation
- `false` (default): Claude can auto-invoke based on context
- `true`: Only the user can trigger via `/name` slash command
- Use for destructive or high-stakes actions (PR creation, deployments)

### argument-hint
- Autocomplete hint shown when user types `/name`
- Example: `argument-hint: "[branch-name]"` shows as `/pr-workflow [branch-name]`

## Dynamic Context Injection

Use `!` followed by a backtick-wrapped command to inject live data:

```markdown
## Current State
- Branch: !`git branch --show-current 2>/dev/null || echo "unknown"`
- Uncommitted files: !`git status --short 2>/dev/null | wc -l`
```

The command output replaces the placeholder before the skill content is sent to Claude.

## String Substitutions

| Variable | Value |
|----------|-------|
| `$ARGUMENTS` | Full argument string from user |
| `$ARGUMENTS[0]`, `$ARGUMENTS[1]` | Individual arguments |
| `$1`, `$2` | Shorthand for `$ARGUMENTS[0]`, etc. |
| `${CLAUDE_SESSION_ID}` | Current session identifier |
| `${CLAUDE_SKILL_DIR}` | Directory containing the SKILL.md |

## Progressive Disclosure

Skills load in layers to save context:

1. **Description** — Always in context (from frontmatter)
2. **SKILL.md body** — Loaded when Claude determines it's relevant
3. **Bundled resources** — scripts/, references/, assets/ loaded on demand

## Directory Structure

```
skill-name/
├── SKILL.md              # Required: frontmatter + instructions
├── scripts/              # Optional: Python tools, shell scripts
├── references/           # Optional: detailed knowledge bases
└── assets/               # Optional: templates, images
```

Flat file alternative: `skill-name.md` (single file, no directory needed)

## Invocation Patterns

| Pattern | user-invocable | disable-model-invocation | Behavior |
|---------|---------------|------------------------|----------|
| Auto-invocable | true (default) | false (default) | Claude and user can trigger |
| Background knowledge | false | — | Only Claude triggers, user cannot |
| Manual-only | true | true | Only user triggers via /name |
