# CLAUDE.md Deep Dive

> **What you'll learn:** How to write effective CLAUDE.md files, the difference between global and project-level, the rules/ directory for modularity, and what to include vs avoid.

## How Claude Reads CLAUDE.md

Claude Code loads CLAUDE.md files in this order:

1. `~/.claude/CLAUDE.md` -- global baseline
2. `~/.claude/rules/*.md` -- global modular rules
3. `.claude/CLAUDE.md` or `CLAUDE.md` in the project root -- project-level
4. `.claude/rules/*.md` -- project modular rules

The content becomes part of Claude's system context for the entire session:

- **Everything is always active** -- Claude does not forget it mid-session
- **Brevity matters** -- every line consumes context window tokens
- **Specificity wins** -- vague guidance gets interpreted loosely; precise rules get followed

---

## Global CLAUDE.md

Your global CLAUDE.md defines standards that apply to every project.

### What to include

```markdown
## Philosophy
- No speculative features -- only what's needed now
- No premature abstraction -- write it 3 times before extracting
- Clarity over cleverness -- readable beats clever
- Replace, don't deprecate -- remove old code entirely

## Code Quality
- Max 100 lines per function, cyclomatic complexity <=8
- Max 5 positional parameters per function
- Fix every warning from linters, type checkers, and tests
- Never swallow exceptions silently

## Testing
- Test behavior, not implementation -- refactors should not break tests
- Test edges and errors -- empty inputs, boundaries, malformed data
- Mock boundaries, not logic -- only mock network, filesystem, external services

## Git
- Atomic commits: feat:, fix:, docs:, refactor:, test:
- Never commit .env, credentials, keys, tokens
- Feature branches only -- never push to main directly

## Security
- Validate all user input at system boundaries
- Parameterize SQL queries (never concatenate user input)
- Pin exact dependency versions (no ^ or ~)
```

See [templates/global/CLAUDE.md](../templates/global/CLAUDE.md) for a production-ready template.

---

## Project CLAUDE.md

Your project CLAUDE.md provides context specific to one codebase. It does not repeat global rules -- it adds to them.

```markdown
# My SaaS Backend

## Quick Facts
- Stack: FastAPI, PostgreSQL 16, Redis, Celery
- Package manager: uv
- Python: 3.12

## Commands
- Dev server: `docker compose up -d`
- Tests: `pytest -x -q`
- Lint: `ruff check .`
- Type check: `mypy app/`

## Key Directories
app/
  api/v1/endpoints/    # Route handlers
  models/              # SQLAlchemy models
  schemas/             # Pydantic request/response
  services/            # Business logic
tests/                 # Mirrors app/ structure

## Architecture
- Services contain business logic; routes are thin wrappers
- All database access through repository pattern
- Auth: JWT with refresh tokens, no session storage

## Code Style
- All endpoints return Pydantic response models (never raw dicts)
- Use Depends() for all shared logic (auth, db session, pagination)
- Error responses use ProblemDetail (RFC 9457)
```

See [templates/project/CLAUDE.md](../templates/project/CLAUDE.md) for a customizable template.

---

## The rules/ Directory

For rules that warrant their own file, use the `rules/` directory. Each `.md` file is loaded alongside CLAUDE.md.

| Use CLAUDE.md for | Use rules/ for |
|-------------------|----------------|
| Project facts (stack, commands) | Cross-cutting concerns |
| Architecture decisions | Security policies |
| Code style conventions | Verification procedures |

**Example:** `~/.claude/rules/security.md`

```markdown
# Security Rules
- Never commit: .env, .key, .pem, credentials.json, API keys, tokens
- Use environment variables for all secrets
- Provide .env.example with placeholder values only
- Validate all user input at system boundaries
- Parameterize SQL queries
- Pin exact dependency versions
- Run pip-audit / pnpm audit before deploying
```

**Example:** `~/.claude/rules/verification.md`

```markdown
# Verification Rules
After every code change:
1. Lint -- run the project linter
2. Typecheck -- run the type checker
3. Test -- run related tests (not full suite)
4. Review -- re-read your diff for unnecessary complexity

If 3+ consecutive fixes fail, STOP and ask the user.
```

See [templates/global/rules/](../templates/global/rules/) for copy-paste versions.

---

## Inheritance and Override Behavior

Both global and project content are active simultaneously. For contradictions, the project rule (loaded later) tends to win.

**Example:** Global says "Max 100 lines per function." Project says "Max 50 lines per function." Claude follows 50.

To explicitly override a global rule:

```markdown
## Overrides
- Override global: Max function length is 200 lines for migration scripts
- Override global: Allow relative imports within the migrations/ directory
```

Rules from `rules/*.md` merge additively. A project cannot "unload" a global rule -- only override it explicitly.

---

## Good vs Bad Content

### BAD: Verbose prose

```markdown
When working on this project, it's important to remember that we follow
a microservices architecture where each service is designed to be
independently deployable...
```

### GOOD: Dense bullets

```markdown
## Architecture
- Microservices -- each service independently deployable
- RESTful APIs -- proper HTTP status codes
- No cross-service database queries
```

### BAD: Session-specific notes

```markdown
## Current Work
- We're currently refactoring the auth module
- Yesterday we fixed the pagination bug
```

### GOOD: Durable standards

```markdown
## Auth Module
- JWT with refresh tokens
- Access token TTL: 15 minutes
- Token rotation on refresh
```

### BAD: Duplicating tool documentation

```markdown
## How to Use pytest
pytest is a testing framework for Python. You can run tests with...
```

### GOOD: Your conventions for the tool

```markdown
## Testing
- Run: `pytest -x -q`
- Coverage: `pytest --cov=app --cov-report=term-missing`
- Fixtures in: tests/conftest.py
```

### BAD: Aspirational rules nobody follows

```markdown
- 100% test coverage required
- Every function must have a docstring
```

### GOOD: Rules that match reality

```markdown
- New code must have tests (aim for 80%+ on new files)
- Public functions need docstrings; private helpers do not
```

---

## Size Guidelines

| Section | Recommended length |
|---------|-------------------|
| Philosophy | 3-6 bullets |
| Code quality | 5-10 bullets |
| Commands | 5-8 commands |
| Architecture | 5-15 bullets |
| Total file | 40-80 lines |

If your CLAUDE.md exceeds 100 lines, move sections into `rules/` files.

---

## Stack-Specific Additions

This repo includes stack templates you can copy into `.claude/rules/`:

- [templates/stacks/python-fastapi.md](../templates/stacks/python-fastapi.md)
- [templates/stacks/typescript-nextjs.md](../templates/stacks/typescript-nextjs.md)
- [templates/stacks/flutter-dart.md](../templates/stacks/flutter-dart.md)
- [templates/stacks/golang.md](../templates/stacks/golang.md)
- [templates/stacks/rust.md](../templates/stacks/rust.md)
- [templates/stacks/react-native.md](../templates/stacks/react-native.md)

---

## Checklist

- [ ] Under 100 lines (move details to rules/)
- [ ] Dense bullets, not prose paragraphs
- [ ] Commands are copy-paste ready
- [ ] Architecture decisions documented
- [ ] Rules match your actual codebase (not aspirational)
- [ ] No secrets, no session-specific notes
- [ ] No duplication of global rules

---

## Next Steps

- [Chapter 3: Settings & Permissions](03-settings-and-permissions.md) -- Deny lists, permissions, environment variables
- [Chapter 4: Hooks](04-hooks.md) -- Automated quality gates
- [Chapter 5: Skills](05-skills.md) -- Domain knowledge and tool skills
