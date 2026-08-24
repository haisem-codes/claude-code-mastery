# Repository Conventions

**Mandatory conventions for skills in this repo.** Every contributor — human or AI coding agent —
must follow these rules when adding or editing a skill under `.claude/skills/`. Skills that
violate them get sent back in review.

Adapted from an external skills-repo convention doc; repo-packaging concerns not relevant here
(plugin distribution, mkdocs site generation, cross-platform sync, PR-target-branch policy) have
been trimmed. See the Conventions section of the root CLAUDE.md for this repo's own git and PR conventions.

---

## 1. Skill Structure

Every skill is a directory under `.claude/skills/`:

```
.claude/skills/<skill-name>/
├── SKILL.md          # Required — main skill file
├── scripts/           # Optional — deterministic CLI tools
│   └── *.py
├── references/        # Optional — detailed reference docs
│   └── *.md
└── assets/            # Optional — templates, examples
```

---

## 2. SKILL.md Format

### Frontmatter (YAML)

**Only two fields are allowed:**

```yaml
---
name: "skill-name"
description: "One-line description of when to use this skill. Be specific about trigger conditions."
---
```

**Do NOT include:** `license`, `metadata`, `triggers`, `version`, `author`, `category`, `updated`,
or any other fields. Extra frontmatter fields get rejected in review.

### Content Requirements

| Requirement | Rule |
|-------------|------|
| **Line limit** | Under 500 lines. Move detailed content to `references/` files. |
| **Opinionated** | Recommend specific approaches. Don't just list options. |
| **Actionable** | The agent must be able to execute, not just advise. |
| **Anti-patterns** | Include a section on what NOT to do. |
| **Cross-references** | Link to related skills and rules in the repo. |
| **Code examples** | Include concrete examples where helpful. |

### Required Sections

At minimum, every SKILL.md should include:

1. **Title** (H1) — skill name
2. **Overview** — what it does, when to use it
3. **Core content** — workflows, patterns, instructions
4. **Anti-Patterns** — common mistakes to avoid
5. **Cross-References** — related skills or rules in this repo

Reference detailed material from `references/` files:
```markdown
> See [references/detailed-guide.md](references/detailed-guide.md) for full patterns.
```

---

## 3. Scripts

All scripts in `scripts/` must follow these rules:

| Rule | Requirement |
|------|-------------|
| **Standard library only** | No new dependencies unless the repo already uses them. |
| **CLI-first** | Must support `--help`. |
| **No LLM calls** | Scripts must be deterministic — no API calls to AI services. |
| **No hardcoded secrets** | Use environment variables for credentials. |
| **Exit codes** | `0` = success, non-zero = failure. |

---

## Quick Reference

| What | Rule |
|------|------|
| Frontmatter fields | `name` + `description` only |
| SKILL.md max lines | 500 |
| Scripts | Deterministic, stdlib-first, no hardcoded secrets |
| Commit format | See the Conventions section of the root CLAUDE.md |
