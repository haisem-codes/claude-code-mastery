# Hooks

Hooks are shell scripts that run automatically at specific points during Claude Code's workflow. They enable automated quality gates, safety checks, and developer experience improvements.

## Hook Types

| Type | When it runs | Use case |
|------|-------------|----------|
| **PreToolUse** | Before Claude executes a tool | Block dangerous commands, enforce conventions |
| **PostToolUse** | After Claude executes a tool | Auto-format, auto-lint, run tests |
| **UserPromptSubmit** | When the user submits a prompt | Skill matching, context injection |

## Installation

Add hooks to your `settings.json` (global or project-level):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/hooks/pre-tool-use/block-main-branch.sh",
            "timeout": 5
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/hooks/pre-tool-use/block-dangerous-commands.sh",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/hooks/post-tool-use/auto-format.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

## Available Hooks

### PreToolUse (Safety)

| Hook | What it does |
|------|-------------|
| `block-main-branch.sh` | Prevents edits on main/master branch |
| `block-dangerous-commands.sh` | Blocks rm -rf, sudo, force-push, hard-reset |
| `block-secret-reads.sh` | Prevents reading .env, .key, .pem, credentials |
| `enforce-package-manager.sh` | Enforces a single package manager (customizable) |

### PostToolUse (Quality)

| Hook | What it does |
|------|-------------|
| `auto-format.sh` | Runs formatter (ruff, prettier, gofmt, rustfmt) on edited files |
| `auto-lint.sh` | Runs linter with auto-fix on edited files |
| `auto-test.sh` | Runs related tests when test files are modified |

### UserPromptSubmit (Intelligence)

| Hook | What it does |
|------|-------------|
| `skill-eval.sh` + `skill-eval.js` | Analyzes prompts and suggests relevant skills based on keywords, file paths, and intent patterns |
| `skill-rules.json` | Configuration for the skill evaluation engine (triggers, scoring weights, directory mappings) |

## Customization

Each hook is a standalone script. Modify paths, tool names, or patterns to match your project. The hooks use `jq` to parse tool input — ensure it's installed (`brew install jq` / `apt install jq`).

## Credits

- Safety hooks adapted from [Trail of Bits claude-code-config](https://github.com/anthropics/claude-code-config)
- Skill evaluation system from [Claude Code Showcase](https://github.com/example/claude-code-showcase)
