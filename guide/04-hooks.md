# Hooks

> **What you'll learn:** The three hook types (PreToolUse, PostToolUse, UserPromptSubmit), how hooks receive input and communicate results via exit codes, and practical examples for each type.

## How Hooks Work

Hooks are shell commands that run automatically at specific points in Claude Code's workflow. They receive JSON input via stdin, and their behavior is controlled by exit codes.

| Hook Type | When it runs | Can block? |
|-----------|-------------|------------|
| **PreToolUse** | Before Claude executes a tool | Yes (exit 2) |
| **PostToolUse** | After Claude executes a tool | No |
| **UserPromptSubmit** | When the user submits a prompt | No (but injects context) |

### Registration in settings.json

```jsonc
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",    // Which tools trigger this hook
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/hook.sh",
            "timeout": 5                       // Seconds before timeout
          }
        ]
      }
    ]
  }
}
```

### Matcher syntax

```
"matcher": "Bash"                // Only Bash tool
"matcher": "Edit|Write"          // Edit OR Write tool
"matcher": "Edit|MultiEdit|Write" // Any file modification tool
"matcher": ""                    // All tools (empty = match everything)
```

### Exit codes

| Exit code | Meaning | Behavior |
|-----------|---------|----------|
| `0` | Success | Continue normally |
| `1` | Error | Logged, does not block |
| `2` | Block | **PreToolUse only:** blocks the tool call; stderr shown to Claude |

### Input format

Hooks receive their payload as JSON on **stdin**. There is no `$TOOL_INPUT`
environment variable — a hook that reads one gets an empty string, silently
does nothing, and still looks installed. Read stdin with `jq`:

```jsonc
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "git push --force origin main"
  }
}
```

Access fields with `jq`:

```bash
CMD=$(jq -r '.tool_input.command // empty')
FILE=$(jq -r '.tool_input.file_path // empty')
```

---

## PreToolUse Hooks

Run before Claude executes a tool. Exit 2 to block.

### Block edits on main/master

```bash
#!/usr/bin/env bash
branch=$(git branch --show-current 2>/dev/null)
if [ "$branch" = "main" ] || [ "$branch" = "master" ]; then
  echo 'BLOCKED: Create a feature branch first.' >&2
  exit 2
fi
```

Registration: `"matcher": "Edit|MultiEdit|Write"` -- see [hooks/pre-tool-use/block-main-branch.sh](../hooks/pre-tool-use/block-main-branch.sh)

### Block dangerous commands

```bash
#!/usr/bin/env bash
CMD=$(jq -r '.tool_input.command // empty')
if echo "$CMD" | grep -qE 'rm[[:space:]]+-[^[:space:]]*r[^[:space:]]*f'; then
  echo 'BLOCKED: Use trash or specific file deletion instead of rm -rf' >&2
  exit 2
fi
if echo "$CMD" | grep -qE 'git[[:space:]]+push.*(--force|--force-with-lease)'; then
  echo 'BLOCKED: Force push requires explicit user approval' >&2
  exit 2
fi
if echo "$CMD" | grep -qE '^sudo[[:space:]]'; then
  echo 'BLOCKED: sudo commands are not allowed' >&2
  exit 2
fi
```

Registration: `"matcher": "Bash"` -- see [hooks/pre-tool-use/block-dangerous-commands.sh](../hooks/pre-tool-use/block-dangerous-commands.sh)

Also available: [block-secret-reads.sh](../hooks/pre-tool-use/block-secret-reads.sh) (blocks .env, .key, .pem reads) and [enforce-package-manager.sh](../hooks/pre-tool-use/enforce-package-manager.sh) (forces a single package manager).

---

## PostToolUse Hooks

Run after Claude executes a tool. Cannot block (the action already happened). Always exit 0.

### Auto-format edited files

```bash
#!/usr/bin/env bash
FILE=$(jq -r '.tool_input.file_path // empty')
[ -z "$FILE" ] && exit 0
case "$FILE" in
  *.py)                      ruff format "$FILE" 2>/dev/null ;;
  *.ts|*.tsx|*.js|*.jsx)     npx prettier --write "$FILE" 2>/dev/null ;;
  *.go)                      gofmt -w "$FILE" 2>/dev/null ;;
  *.rs)                      rustfmt "$FILE" 2>/dev/null ;;
esac
exit 0
```

Registration: `"matcher": "Edit|Write"` -- see [hooks/post-tool-use/auto-format.sh](../hooks/post-tool-use/auto-format.sh)

Also available: [auto-lint.sh](../hooks/post-tool-use/auto-lint.sh) (linter with auto-fix) and [auto-test.sh](../hooks/post-tool-use/auto-test.sh) (runs tests when test files change).

---

## UserPromptSubmit Hooks

Run when the user submits a prompt. Stdout is injected as additional context that Claude sees. Always exit 0.

### Skill evaluation engine

This repo includes a skill evaluation system that analyzes prompts and suggests relevant skills. The architecture:

```
User prompt -> skill-eval.sh (wrapper) -> skill-eval.js (Node.js engine)
                                            -> skill-rules.json (config)
                                            -> Stdout injected into Claude's context
```

**Wrapper:** [hooks/user-prompt-submit/skill-eval.sh](../hooks/user-prompt-submit/skill-eval.sh)

```bash
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NODE_SCRIPT="$SCRIPT_DIR/skill-eval.js"
if ! command -v node &>/dev/null; then exit 0; fi
if [[ ! -f "$NODE_SCRIPT" ]]; then exit 0; fi
cat | node "$NODE_SCRIPT" 2>/dev/null
exit 0
```

**Registration** (matcher is empty -- runs on every prompt):

```jsonc
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/user-prompt-submit/skill-eval.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

**How scoring works** (configured in [skill-rules.json](../hooks/user-prompt-submit/skill-rules.json)):

| Signal | Score | Example |
|--------|-------|---------|
| Keyword match | 2 | "bug" matches debugging skill |
| Keyword pattern (regex) | 3 | `\bbug\b` matches whole word only |
| File path glob | 4 | `src/hooks/*.ts` matches react-ui-patterns |
| Directory mapping | 5 | `src/graphql/` maps to graphql-schema skill |
| Intent pattern | 4 | "fix.*bug" detected as debugging intent |
| Content pattern | 3 | `useQuery` in prompt matches graphql skill |

Skills scoring above the threshold (default: 3) are suggested to Claude.

See [hooks/user-prompt-submit/skill-eval.js](../hooks/user-prompt-submit/skill-eval.js) for the full engine.

---

## Writing Your Own Hooks

### PreToolUse template

```bash
#!/usr/bin/env bash
INPUT="$(cat)"
VALUE=$(echo "$INPUT" | jq -r '.your_field // empty')

if [ "condition" ]; then
  echo "BLOCKED: Reason" >&2
  exit 2
fi
exit 0
```

### PostToolUse template

```bash
#!/usr/bin/env bash
INPUT="$(cat)"
FILE=$(echo "$INPUT" | jq -r '.file_path // empty')
[ -z "$FILE" ] && exit 0
# Your action here
exit 0
```

### UserPromptSubmit template

```bash
#!/usr/bin/env bash
INPUT=$(cat)
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty')
if echo "$PROMPT" | grep -qi "deploy"; then
  echo "REMINDER: Run full test suite before deploying."
fi
exit 0
```

---

## Hook Composition and Timeouts

Chain multiple hooks for the same matcher -- they run in order:

```jsonc
{
  "matcher": "Edit|Write",
  "hooks": [
    { "type": "command", "command": "bash auto-format.sh", "timeout": 10 },
    { "type": "command", "command": "bash auto-lint.sh",   "timeout": 15 },
    { "type": "command", "command": "bash auto-test.sh",   "timeout": 30 }
  ]
}
```

| Hook type | Recommended timeout |
|-----------|-------------------|
| PreToolUse (git/regex check) | 5s |
| PostToolUse (formatter/linter) | 10-15s |
| PostToolUse (test runner) | 30s |
| UserPromptSubmit | 5s |

If a hook exceeds its timeout, it is killed and treated as exit 0.

For simple checks, inline the command in settings.json. For multi-condition checks, use an external script file.

---

## All Available Hooks

| Hook | Type | Purpose |
|------|------|---------|
| [block-main-branch.sh](../hooks/pre-tool-use/) | PreToolUse | Prevents edits on main/master |
| [block-dangerous-commands.sh](../hooks/pre-tool-use/) | PreToolUse | Blocks rm -rf, sudo, force-push |
| [block-secret-reads.sh](../hooks/pre-tool-use/) | PreToolUse | Blocks .env, .key, .pem reads |
| [enforce-package-manager.sh](../hooks/pre-tool-use/) | PreToolUse | Enforces single package manager |
| [auto-format.sh](../hooks/post-tool-use/) | PostToolUse | Runs formatter on edited files |
| [auto-lint.sh](../hooks/post-tool-use/) | PostToolUse | Runs linter with auto-fix |
| [auto-test.sh](../hooks/post-tool-use/) | PostToolUse | Runs tests on test file changes |
| [skill-eval.sh + skill-eval.js](../hooks/user-prompt-submit/) | UserPromptSubmit | Skill matching engine |

---

## Next Steps

- [Chapter 5: Skills](05-skills.md) -- Domain knowledge, Skills 2.0 features, directory structure
