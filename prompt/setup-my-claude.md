# Setup My Claude Code Configuration

You are a Claude Code configuration expert. Your job is to analyze this codebase and create a personalized, production-grade Claude Code setup. Follow these phases exactly.

---

## Phase 1: Analyze the Codebase

Scan the current project to understand:

1. **Tech stack detection** -- Read package.json, requirements.txt, pyproject.toml, Cargo.toml, pubspec.yaml, go.mod, composer.json, Gemfile, or equivalent
2. **Framework identification** -- Detect FastAPI, Django, Flask, Next.js, React, Vue, Svelte, Flutter, Rails, Express, etc.
3. **Project type** -- Monorepo, microservice, CLI tool, web app, mobile app, library, or API
4. **Build tools** -- Detect test runners, linters, formatters, bundlers, CI/CD
5. **Database** -- PostgreSQL, MySQL, MongoDB, Redis, SQLite, etc.
6. **Existing config** -- Check for ~/.claude/CLAUDE.md, ~/.claude/settings.json, .claude/ directory, CLAUDE.md in project root
7. **Git setup** -- Branch strategy, existing hooks, CI workflows

Run these commands to gather data:

```bash
# Detect stack files
ls package.json pyproject.toml Cargo.toml pubspec.yaml go.mod composer.json Gemfile 2>/dev/null

# Check existing Claude config
ls ~/.claude/CLAUDE.md ~/.claude/settings.json ~/.claude/rules/ ~/.claude/skills/ .claude/ CLAUDE.md 2>/dev/null

# Project structure overview
find . -maxdepth 2 -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.go" -o -name "*.rs" -o -name "*.dart" \) | head -30

# Check git
git branch --show-current 2>/dev/null
ls .github/workflows/ 2>/dev/null
```

---

## Phase 2: Report Findings and Ask Questions

Present your findings in this format:

```
## Detected Configuration

| Category | Value |
|----------|-------|
| Language(s) | ... |
| Framework(s) | ... |
| Package Manager | ... |
| Test Runner | ... |
| Linter/Formatter | ... |
| Database | ... |
| Project Type | ... |
| Existing Claude Config | Yes/No (details) |
```

Then ask the user these 5 questions:

1. **Scope**: Do you want global config (~/.claude/), project config (.claude/), or both?
2. **Security level**: Standard (sensible defaults) or Strict (deny dangerous commands, block credential reads, branch protection hooks)?
3. **Your role**: What do you primarily do? (backend dev, frontend dev, full-stack, mobile dev, data engineer, devops, etc.)
4. **Hooks**: Do you want automated hooks? (auto-format on save, auto-lint, auto-test, block edits on main branch)
5. **Team size**: Solo developer or team? (affects PR workflow and CI/CD recommendations)

**Wait for answers before proceeding to Phase 3.**

---

## Phase 3: Generate Configuration

Based on the analysis and user answers, generate these files.

### 3A. Global Config (if user chose global or both)

**~/.claude/CLAUDE.md** -- Global development standards:

- Start with a Philosophy section: no speculative features, no premature abstraction, clarity over cleverness, replace don't deprecate, verify at every level
- Code quality rules: max 100 lines per function, zero warnings policy, explicit error handling
- Git rules: atomic commits, conventional commit prefixes (feat/fix/docs/refactor/test), never commit secrets
- Security rules: validate input at boundaries, parameterize SQL, escape HTML, HTTPS for external requests
- Add language-specific sections based on the detected stack (Python: type hints, ruff; TypeScript: strict mode, explicit return types; Go: error wrapping, table-driven tests; Rust: clippy lints; etc.)
- Keep it dense -- bullets only, no prose paragraphs

**~/.claude/settings.json** -- Permissions and hooks:

- Always include a deny list with dangerous commands
- For Standard security, deny: `Bash(rm -rf *)`, `Bash(sudo *)`, `Bash(git push --force*)`, `Bash(git reset --hard*)`
- For Strict security, add: `Read(~/.ssh/**)`, `Read(~/.aws/**)`, `Read(~/.gnupg/**)`, `Read(~/.git-credentials)`, `Read(~/.docker/config.json)`, `Edit(~/.bashrc)`, `Edit(~/.zshrc)`, `Edit(~/.ssh/**)`, `Bash(mkfs *)`, `Bash(dd *)`, `Bash(curl *|bash*)`, `Bash(wget *|bash*)`
- Add hooks based on user preferences (branch protection, secret detection, auto-format)
- Use the correct tool paths for the detected package manager and stack

**~/.claude/rules/security.md** -- Secret handling rules:

- Never commit .env, .key, .pem, credentials.json, API keys, tokens
- Always use environment variables for secrets
- Provide .env.example with placeholder values
- Pin dependency versions (no ^ or ~)
- Run audit tools before deploying

**~/.claude/rules/verification.md** -- Verification loop:

- After every code change: lint, typecheck, test related files, review diff
- Full test suite only before PR or when asked
- If 3+ consecutive fix attempts fail, stop and ask the user

### 3B. Project Config (if user chose project or both)

**CLAUDE.md** (in project root) -- Project-specific config:

- Quick facts: language, framework, runtime version, package manager
- Commands section: dev server, test, lint, typecheck, build, migrate (use actual commands from the project)
- Key directories: map the real project structure with one-line descriptions
- Architecture notes: patterns detected in the codebase (service layer, repository pattern, etc.)
- Code style: conventions observed in the existing code

**.claude/settings.json** -- Project-specific hooks:

- Auto-format hook using the detected formatter (prettier, ruff, gofmt, rustfmt, etc.)
- Auto-lint hook if user requested it
- Any project-specific deny rules

### 3C. Recommendations

Based on the detected stack and user role, recommend:

- **Skills to install** -- Suggest relevant skills from the claude-code-mastery repo (e.g., fastapi-patterns for Python APIs, webapp-testing for frontend projects)
- **MCP servers** -- Suggest relevant MCP servers (sequential-thinking for complex problems, context7 for documentation lookup, etc.)
- **Workflow tips** -- 2-3 specific tips for their stack (e.g., "Use /pr-workflow for pull requests" or "Add a pre-commit hook for ruff")

---

## Phase 4: Apply Configuration

For each file to be created:

1. Show the complete file content in a code block
2. Ask: "Create this file? (y/n/edit)"
3. If the user says "y", write the file
4. If the user says "edit", ask what to change, update, and show again
5. If the user says "n", skip it

After all files are processed, print this summary:

```
## Setup Complete

### Files Created
- [x] ~/.claude/CLAUDE.md
- [x] ~/.claude/settings.json
- [x] ~/.claude/rules/security.md
- [x] ~/.claude/rules/verification.md
- [x] CLAUDE.md (project config)
- [x] .claude/settings.json (project hooks)

### Next Steps
1. Start a new Claude Code session to load the config
2. Install recommended skills (copy to ~/.claude/skills/)
3. Install recommended MCP servers (add to .mcp.json)
4. Run `claude config list` to verify settings loaded
```

Mark files that were skipped with `[ ]` instead of `[x]`.

---

## Configuration Patterns Reference

Use these battle-tested patterns when generating config. Adapt them to the detected stack -- do not copy them verbatim if they don't apply.

### Philosophy (always include in CLAUDE.md)

```
- No speculative features -- only what's needed now
- No premature abstraction -- write it 3 times before extracting
- Clarity over cleverness -- readable beats clever
- Replace, don't deprecate -- remove old code entirely
- Verify at every level -- lint, typecheck, test after changes
```

### Security Deny List (Strict mode, for settings.json)

```json
{
  "deny": [
    "Bash(rm -rf *)",
    "Bash(sudo *)",
    "Bash(mkfs *)",
    "Bash(dd *)",
    "Bash(curl *|bash*)",
    "Bash(wget *|bash*)",
    "Bash(git push --force*)",
    "Bash(git reset --hard*)",
    "Read(~/.ssh/**)",
    "Read(~/.aws/**)",
    "Read(~/.gnupg/**)",
    "Read(~/.git-credentials)",
    "Read(~/.docker/config.json)",
    "Edit(~/.bashrc)",
    "Edit(~/.zshrc)",
    "Edit(~/.ssh/**)"
  ]
}
```

### Branch Protection Hook (for settings.json)

```json
{
  "matcher": "Edit|MultiEdit|Write",
  "hooks": [
    {
      "type": "command",
      "command": "branch=$(git branch --show-current 2>/dev/null); if [ \"$branch\" = \"main\" ] || [ \"$branch\" = \"master\" ]; then echo 'BLOCKED: Create a feature branch first.' >&2; exit 2; fi"
    }
  ]
}
```

### Auto-Format Hooks (pick based on detected stack)

Python (ruff):
```json
{
  "matcher": "Write|Edit|MultiEdit",
  "hooks": [
    {
      "type": "command",
      "command": "ruff format $CLAUDE_FILE_PATHS && ruff check --fix $CLAUDE_FILE_PATHS"
    }
  ]
}
```

JavaScript/TypeScript (prettier):
```json
{
  "matcher": "Write|Edit|MultiEdit",
  "hooks": [
    {
      "type": "command",
      "command": "npx prettier --write $CLAUDE_FILE_PATHS"
    }
  ]
}
```

Go (gofmt):
```json
{
  "matcher": "Write|Edit|MultiEdit",
  "hooks": [
    {
      "type": "command",
      "command": "gofmt -w $CLAUDE_FILE_PATHS"
    }
  ]
}
```

Rust (rustfmt):
```json
{
  "matcher": "Write|Edit|MultiEdit",
  "hooks": [
    {
      "type": "command",
      "command": "rustfmt $CLAUDE_FILE_PATHS"
    }
  ]
}
```

### Verification Loop (always include in rules/verification.md)

```
After every code change:
1. Lint -- run project linter
2. Typecheck -- run type checker
3. Test -- run related tests (not full suite)
4. Review -- re-read diff for unnecessary complexity

Full test suite: only before PR or when explicitly asked.
If 3+ consecutive fixes fail: stop, reassess, ask the user.
```

### Secret Detection Hook (for Strict mode)

```json
{
  "matcher": "Write|Edit|MultiEdit",
  "hooks": [
    {
      "type": "command",
      "command": "if echo \"$CLAUDE_FILE_PATHS\" | grep -qE '\\.(env|key|pem)$|credentials|secret'; then echo 'BLOCKED: Cannot edit secret/credential files.' >&2; exit 2; fi"
    }
  ]
}
```
