# Chapter 6: Agents — Delegating Complex Tasks

Agents are specialized AI units that handle work delegated by Claude Code. Instead of Claude doing everything in a single conversation thread, agents let you break complex tasks into scoped, parallel units of work — each with its own tools, instructions, and focus area.

This chapter covers what agents are, when to use them, how they work internally, and how to build your own.

---

## What Is an Agent?

An agent is a markdown file with YAML frontmatter that defines:

- **Who** the agent is (name, description, persona)
- **What tools** it can access (scoped subset of all available tools)
- **Which model** it runs on (can differ from your main session)
- **How it behaves** (instructions in the markdown body)

When Claude encounters a task that matches an agent's expertise, it dispatches the work using the `Task` tool. The agent runs in its own context, completes the work, and returns results to the main session.

```
You (prompt) → Claude (main session) → Task tool → Agent (scoped work) → Results back
```

Agents are not plugins or external services. They run inside Claude Code using the same infrastructure as your main session, but with isolated context and scoped permissions.

---

## When to Use Agents

**Use agents when:**

- A task spans multiple domains (frontend + backend + database)
- You need parallel execution (run 3 independent analyses simultaneously)
- The task requires deep domain expertise (security audit, performance profiling)
- You want to protect your main context window from exploratory work
- A multi-step workflow benefits from structured delegation

**Handle directly when:**

- The task is a single-step operation (rename a variable, fix a typo)
- You already know exactly what to change
- The work touches one file or one small area
- Answering a quick question about the codebase

**Rule of thumb:** If you would ask a colleague to handle it rather than doing it yourself, it is a good candidate for an agent.

---

## How Agents Work Internally

### The Task Tool

Claude dispatches work to agents via the `Task` tool. This tool:

1. Loads the agent's markdown file
2. Creates a new conversation context with the agent's instructions
3. Provides only the tools listed in the agent's frontmatter
4. Runs the agent on the specified model
5. Returns the agent's output to the main session

### Scoped Tools

Each agent declares which tools it can access. A code reviewer agent might get `Read`, `Grep`, and `Glob` but not `Write` or `Bash` — preventing it from making changes when its job is only to review.

### Model Selection

Agents can run on different models. Use a fast model like `haiku` for triage and analysis tasks. Use the full model for complex implementation work. This controls both speed and cost.

---

## Agent File Format

An agent is a `.md` file with YAML frontmatter followed by markdown instructions.

### Minimal Example

```markdown
---
name: code-reviewer
description: Reviews code for quality, security, and maintainability issues.
tools: Read, Grep, Glob
model: haiku
---

# Code Reviewer

You are a senior code reviewer. Your job is to analyze code and provide
actionable feedback on:

- Security vulnerabilities
- Performance issues
- Code quality and maintainability
- Missing error handling

## Process

1. Read the files specified in the task
2. Analyze each file against the criteria above
3. Report findings with file:line references
4. Prioritize: critical > high > medium > low

## Output Format

For each finding:
- **File**: path/to/file.py:42
- **Severity**: critical | high | medium | low
- **Issue**: One-line description
- **Fix**: Concrete suggestion
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (kebab-case) |
| `description` | Yes | When to use this agent (include trigger keywords) |
| `tools` | Yes | Comma-separated list of tools the agent can access |
| `model` | No | Model to use (`haiku`, `sonnet`, `opus`). Defaults to session model |

### Full Example — Database Migration Agent

```markdown
---
name: migration-writer
description: Creates database migration files for schema changes. Use when
  adding tables, columns, indexes, or modifying existing schema.
tools: Read, Write, Edit, Bash, Grep, Glob
model: sonnet
---

# Database Migration Writer

You are a database migration specialist. You create safe, reversible
migrations that follow the project's existing patterns.

## Before Writing

1. Find existing migrations: `Glob("**/migrations/*.py")` or
   `Glob("**/migrations/*.sql")`
2. Identify the migration framework (Alembic, Django, Knex, Prisma)
3. Read the 3 most recent migrations to match the style
4. Check the current schema state

## Migration Rules

- Every migration MUST have a rollback (downgrade/revert)
- Add indexes for any new foreign key columns
- Use explicit column types — never rely on defaults
- Name migrations descriptively: `add_user_email_verification_columns`
- Test the migration runs forward AND backward before reporting done

## Output

- The migration file(s) created
- SQL that will execute (for review)
- Rollback SQL
- Any warnings about data loss or locking
```

---

## Installing Agents

Agents live in one of two locations:

### Global Agents (All Projects)

```
~/.claude/agents/
├── code-reviewer.md
├── migration-writer.md
└── security-auditor.md
```

These are available in every Claude Code session regardless of which project you open.

### Project Agents (Single Project)

```
your-project/
└── .claude/
    └── agents/
        ├── api-endpoint.md
        └── celery-worker.md
```

These are only available when working in that specific project. Use project agents for workflows tied to your tech stack or conventions.

### Precedence

If a global agent and a project agent share the same `name`, the project agent takes priority. This lets you override global defaults per project.

---

## The Agent-Organizer Pattern

For complex tasks that span multiple domains, a meta-agent called the **agent-organizer** acts as a strategic coordinator:

```
User prompt
  → Claude (main session)
    → agent-organizer (analyzes task, picks team)
      → Returns: recommended agents + execution plan
    → Claude dispatches recommended agents in sequence/parallel
  → Final result assembled and returned
```

The agent-organizer does NOT implement solutions. It:

1. Analyzes the project structure and tech stack
2. Selects 3-4 specialist agents from the available pool
3. Defines the execution sequence and dependencies
4. Sets quality checkpoints between phases

### When the Organizer Activates

The dispatch protocol in `CLAUDE.md` defines when delegation is mandatory:

- Code generation or refactoring
- Debugging beyond simple syntax errors
- Adding features that touch multiple layers
- Writing tests for complex logic
- Architecture analysis or planning

For trivial tasks (typo fixes, simple questions), Claude handles them directly without involving the organizer.

### Example Flow

**Prompt:** "Add user authentication to the Express API, audit it for security, and document the endpoints."

1. **agent-organizer** analyzes: 3 domains (backend, security, docs)
2. Recommends: `backend-architect` → `security-auditor` → `api-documenter`
3. Defines sequence: implement first, then audit, then document
4. Sets checkpoints: security review must pass before documentation begins

See the full agent-organizer definition in [`agents/agent-organizer.md`](../agents/agent-organizer.md).

---

## Agent Dispatch Protocol

The standard dispatch flow has three phases:

### 1. Triage

Claude analyzes the user's prompt:

- **Trivial?** Handle directly (answer questions, fix typos)
- **Single domain?** Dispatch to one specialist agent
- **Multi-domain?** Invoke the agent-organizer for team assembly

### 2. Delegate

For single-agent tasks:
```
Task tool → agent with user's prompt + relevant context
```

For multi-agent tasks:
```
Task tool → agent-organizer → returns team + plan
Task tool → agent-1 (phase 1 work)
Task tool → agent-2 (phase 2 work, receives phase 1 output)
Task tool → agent-3 (phase 3 work, receives prior outputs)
```

Independent agents can run in parallel (multiple `Task` calls in one message). Dependent agents run sequentially.

### 3. Await and Assemble

Claude waits for all dispatched agents to complete, then:

- Assembles results into a coherent response
- Validates outputs against success criteria
- Presents the final result to the user

---

## Auto-Delegation

Claude can automatically select agents based on the `description` field in the agent's frontmatter. When a user prompt contains keywords that match an agent's description, Claude may delegate without being explicitly asked.

To control this behavior:

- **Enable auto-delegation:** Write rich descriptions with trigger keywords
  ```yaml
  description: Creates database migrations for schema changes. Use when
    adding tables, columns, indexes, or altering existing schema. Handles
    Alembic, Django, Knex, and Prisma migrations.
  ```

- **Disable auto-delegation:** Add the frontmatter flag
  ```yaml
  disable-model-invocation: true
  ```
  This makes the agent manual-only — it runs only when you explicitly invoke it.

---

## Practical Tips

- **Start small.** One well-scoped agent beats five vague ones
- **Scope tools tightly.** A reviewer should not have `Write`. A writer should not have `Bash` unless it needs to run tests
- **Use haiku for analysis, sonnet/opus for implementation.** Match model cost to task complexity
- **Test agents incrementally.** Run them on a real task before adding to your global config
- **Keep instructions dense.** Agents have limited context — bullet points over paragraphs
- **Include process steps.** Agents work better with explicit "do this, then this" sequences than with abstract goals

---

## Available Agents

This repository includes a library of pre-built agents organized by domain:

```
agents/
├── agent-organizer.md          # Meta-agent for team assembly
├── business/                   # Product, strategy, growth
├── data-ai/                    # Data engineering, ML, analytics
├── development/                # Frontend, backend, full-stack
├── infrastructure/             # Cloud, DevOps, deployment
├── quality-testing/            # Code review, QA, testing
├── security/                   # Security audit, compliance
└── specialization/             # Domain-specific experts
```

Browse the [`agents/`](../agents/) directory for the full catalog. Each agent file is self-contained — copy it to your `~/.claude/agents/` directory to start using it.

---

Next: [Chapter 7 — MCP Servers](./07-mcp-servers.md)
