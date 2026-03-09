# Setup My Claude Code Configuration

You are a Claude Code configuration expert. Your job is to analyze this codebase and create a personalized, production-grade Claude Code setup using the claude-code-mastery resource library. Follow these phases exactly.

---

## Phase 0: Clone the Resource Library

Before doing anything else, clone the claude-code-mastery repo so you have access to 190+ skills, 33 agents, 10 hook scripts, and config templates.

```bash
# Clone into a temp directory (won't affect the user's project)
git clone https://github.com/haisem-codes/claude-code-mastery.git /tmp/claude-code-mastery 2>/dev/null || echo "Already cloned"
```

Verify the repo has what we need:

```bash
ls /tmp/claude-code-mastery/skills/ /tmp/claude-code-mastery/agents/ /tmp/claude-code-mastery/hooks/ /tmp/claude-code-mastery/templates/ 2>/dev/null
```

**This repo contains:**

| Directory | Contents |
|-----------|----------|
| `skills/` | 190+ skills across 12 domains (engineering, marketing, c-suite, compliance, product, PM, finance, sales) |
| `agents/` | 33 specialized subagents (development, infrastructure, data-ai, quality-testing, security, business) |
| `hooks/` | 10 hook scripts (branch protection, secret blocking, auto-format, auto-lint, auto-test, skill evaluation) |
| `templates/` | Global + project CLAUDE.md, settings.json, rules, and 6 stack-specific supplements |

You will use these resources throughout the setup to copy relevant skills, agents, and hooks into the user's config.

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

Also scan the cloned resource library to identify matching skills for the detected stack:

```bash
# List available skill domains
ls /tmp/claude-code-mastery/skills/

# List available agents
ls /tmp/claude-code-mastery/agents/development/ /tmp/claude-code-mastery/agents/data-ai/ /tmp/claude-code-mastery/agents/infrastructure/ /tmp/claude-code-mastery/agents/quality-testing/ /tmp/claude-code-mastery/agents/security/ /tmp/claude-code-mastery/agents/business/ /tmp/claude-code-mastery/agents/specialization/

# List available hooks
ls /tmp/claude-code-mastery/hooks/pre-tool-use/ /tmp/claude-code-mastery/hooks/post-tool-use/ /tmp/claude-code-mastery/hooks/user-prompt-submit/

# List stack-specific templates
ls /tmp/claude-code-mastery/templates/stacks/
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
3. **Your role**: What do you primarily do? (backend dev, frontend dev, full-stack, mobile dev, data engineer, devops, product manager, marketing, executive/C-suite, compliance, finance, sales, etc.)
4. **Hooks**: Do you want automated hooks? (auto-format on save, auto-lint, auto-test, block edits on main branch)
5. **Skill domains**: Which areas interest you? We have skills for: Engineering (63), Marketing (43), C-Suite Advisory (34), Compliance (12), Product (8), Project Management (6), Business Growth (4), Finance (1), plus Anthropic official tools (16). Pick any combination or say "all relevant".

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

### 3C. Install Skills from Resource Library

Based on the detected stack, user role, and chosen skill domains, copy relevant skills from the cloned repo into `~/.claude/skills/`.

**Skill mapping by stack:**

| Stack | Skills to install |
|-------|-------------------|
| Python/FastAPI | `reference/fastapi-patterns`, `reference/postgres-optimization`, `reference/perf-profiler`, `engineering/api-design-reviewer`, `engineering/performance-profiler` |
| TypeScript/Next.js | `engineering-team/senior-architect`, `engineering/ci-cd-pipeline-builder` |
| Flutter/Dart | `engineering-team/senior-architect` |
| Any with DB | `reference/postgres-optimization`, `engineering/database-designer` |
| Any with CI/CD | `engineering/ci-cd-pipeline-builder`, `engineering/observability-designer` |

**Skill mapping by role:**

| Role | Skills to install |
|------|-------------------|
| Marketing | `marketing/ai-seo`, `marketing/content-creator`, `marketing/ad-creative`, `marketing/analytics-tracking` + others from marketing/ |
| C-Suite/Executive | `c-level-advisor/ceo-advisor`, `c-level-advisor/cfo-advisor`, etc. based on their specific role |
| Product Manager | `product/product-strategist`, `product/agile-product-owner`, `product/ux-researcher-designer` |
| Project Manager | `project-management/scrum-master`, `project-management/senior-pm`, `project-management/jira-expert` |
| Compliance | `compliance/gdpr-dsgvo-expert`, `compliance/isms-audit-expert`, etc. based on their industry |
| Sales/Business | `business-growth/sales-engineer`, `business-growth/revenue-operations`, `business-growth/customer-success-manager` |
| Finance | `finance/financial-analyst` |

**Always install** (useful for everyone):
- Anthropic official skills: `anthropic-official/pdf`, `anthropic-official/docx`, `anthropic-official/xlsx`

Install by copying from the cloned repo:

```bash
# Create skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Copy selected skills (example -- adapt based on user's choices)
cp -r /tmp/claude-code-mastery/skills/reference/fastapi-patterns ~/.claude/skills/
cp -r /tmp/claude-code-mastery/skills/engineering/api-design-reviewer ~/.claude/skills/
cp -r /tmp/claude-code-mastery/skills/anthropic-official/pdf ~/.claude/skills/
# ... add more based on analysis
```

Read each skill's SKILL.md before copying to confirm it's relevant. Show the user a table of selected skills with one-line descriptions and get confirmation before copying.

### 3D. Install Agents from Resource Library

Based on the user's role and stack, recommend and install relevant subagents.

**Agent mapping:**

| Need | Agents |
|------|--------|
| Code quality | `quality-testing/code-reviewer`, `quality-testing/architect-review` |
| Backend dev | `development/backend-architect`, `development/python-pro` or `development/golang-pro` |
| Frontend dev | `development/frontend-developer`, `development/react-pro`, `development/nextjs-pro` |
| Full-stack | `development/full-stack-developer`, `development/backend-architect`, `development/frontend-developer` |
| Data/AI | `data-ai/ai-engineer`, `data-ai/database-optimizer`, `data-ai/prompt-engineer` |
| DevOps | `infrastructure/cloud-architect`, `infrastructure/deployment-engineer`, `infrastructure/devops-incident-responder` |
| Testing | `quality-testing/qa-expert`, `quality-testing/test-automator` |
| Security | `security/` agents |
| Orchestration | `agent-organizer.md` (master orchestrator that delegates to other agents) |

**Always recommend:** `quality-testing/code-reviewer` (useful for everyone writing code)

Install by copying the agent .md files into the project or global config:

```bash
# Agents go into the project's .claude/agents/ directory (or wherever subagents are configured)
mkdir -p .claude/agents

# Copy selected agents
cp /tmp/claude-code-mastery/agents/quality-testing/code-reviewer.md .claude/agents/
cp /tmp/claude-code-mastery/agents/agent-organizer.md .claude/agents/
# ... add more based on analysis
```

Show the user a table of selected agents with descriptions and get confirmation before copying.

### 3E. Install Hooks from Resource Library

Based on the user's security level and hook preferences, copy relevant hook scripts.

**Available hooks:**

| Hook | File | Purpose |
|------|------|---------|
| Block main branch edits | `pre-tool-use/block-main-branch.sh` | Prevents accidental edits on main/master |
| Block dangerous commands | `pre-tool-use/block-dangerous-commands.sh` | Blocks rm -rf, sudo, dd, etc. |
| Block secret file reads | `pre-tool-use/block-secret-reads.sh` | Blocks reading .env, .key, .pem files |
| Enforce package manager | `pre-tool-use/enforce-package-manager.sh` | Ensures consistent package manager usage |
| Auto-format | `post-tool-use/auto-format.sh` | Formats files after every edit |
| Auto-lint | `post-tool-use/auto-lint.sh` | Lints files after every edit |
| Auto-test | `post-tool-use/auto-test.sh` | Runs related tests after every edit |
| Skill evaluation | `user-prompt-submit/skill-eval.sh` + `skill-eval.js` + `skill-rules.json` | Auto-matches prompts to relevant skills |

For **Standard security**: install block-main-branch + auto-format
For **Strict security**: install all pre-tool-use hooks + auto-format + auto-lint

```bash
# Read each hook script before installing to adapt paths to user's system
cat /tmp/claude-code-mastery/hooks/pre-tool-use/block-main-branch.sh
```

Read each hook script, adapt any hardcoded paths to the user's system (package manager, formatter command, etc.), then integrate into the user's settings.json hooks configuration. Do NOT blindly copy -- adapt the command strings to match the user's detected stack.

### 3F. Additional Recommendations

- **MCP servers** -- Suggest relevant MCP servers (sequential-thinking for complex problems, context7 for documentation lookup, playwright for web testing)
- **Stack templates** -- If a matching stack template exists in `/tmp/claude-code-mastery/templates/stacks/`, read it and incorporate relevant patterns into the project CLAUDE.md
- **Workflow tips** -- 2-3 specific tips for their stack

---

## Phase 4: Apply Configuration

Work through each category in order. For each file/skill/agent/hook to be installed:

1. Show what will be created/copied in a clear table
2. Ask: "Apply this batch? (y/n/edit)"
3. If the user says "y", execute all operations in the batch
4. If the user says "edit", ask what to change, update, and show again
5. If the user says "n", skip the batch

**Batch order:**

1. **Config files** -- CLAUDE.md, settings.json, rules/ (show full content)
2. **Skills** -- Copy selected skills from /tmp/claude-code-mastery/skills/ to ~/.claude/skills/
3. **Agents** -- Copy selected agents from /tmp/claude-code-mastery/agents/ to .claude/agents/
4. **Hooks** -- Integrate adapted hook commands into settings.json
5. **Stack templates** -- Merge relevant stack supplement into project CLAUDE.md

After all batches are processed, clean up and print the summary:

```bash
# Clean up the cloned repo
rm -rf /tmp/claude-code-mastery
```

```
## Setup Complete

### Config Files
- [x] ~/.claude/CLAUDE.md (global rules)
- [x] ~/.claude/settings.json (permissions + hooks)
- [x] ~/.claude/rules/security.md
- [x] ~/.claude/rules/verification.md
- [x] ./CLAUDE.md (project config)
- [x] ./.claude/settings.json (project hooks)

### Skills Installed (X total)
- [x] skill-name -- description
- [x] ...

### Agents Installed (X total)
- [x] agent-name -- description
- [x] ...

### Hooks Configured (X total)
- [x] hook-name -- description
- [x] ...

### Next Steps
1. Start a new Claude Code session to load the config
2. Run `claude config list` to verify settings loaded
3. Try a task to see skills and agents in action
4. Read the guide for advanced patterns: https://github.com/haisem-codes/claude-code-mastery/tree/main/guide
```

Mark items that were skipped with `[ ]` instead of `[x]`.

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
