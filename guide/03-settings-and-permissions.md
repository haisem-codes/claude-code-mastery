# Settings & Permissions

> **What you'll learn:** The settings.json schema, permission system with deny/allow patterns, environment variables, and the settings.local.json pattern for personal overrides.

## settings.json Overview

`settings.json` controls three things:

1. **Permissions** -- what Claude can and cannot do (deny/allow lists)
2. **Hooks** -- scripts that run at specific workflow points (see [Chapter 4](04-hooks.md))
3. **Environment variables** -- values injected into Claude's shell environment

Settings load from:
- `~/.claude/settings.json` -- global (all projects)
- `.claude/settings.json` -- project-level (committed to git)
- `.claude/settings.local.json` -- personal overrides (gitignored)

---

## The Permission System

### How permissions work

```jsonc
{
  "permissions": {
    "allow": [
      // Always allowed (no confirmation prompt)
    ],
    "deny": [
      // Always blocked (Claude cannot execute)
    ]
  }
}
```

Anything not in `allow` or `deny` triggers a confirmation prompt.

### Pattern syntax

Permissions use `Tool(glob)` format:

- **Tool** is the tool name: `Bash`, `Read`, `Edit`, `Write`, `MultiEdit`
- **glob** matches the tool's input (command text or file path)
- `*` matches within a single path segment; `**` matches across segments

### Deny list: copy-paste starter

```jsonc
{
  "permissions": {
    "deny": [
      "Bash(rm -rf *)",
      "Bash(rm -fr *)",
      "Bash(sudo *)",
      "Bash(mkfs *)",
      "Bash(dd *)",
      "Bash(curl *|bash*)",
      "Bash(wget *|bash*)",

      "Bash(git push --force*)",
      "Bash(git push *--force*)",
      "Bash(git reset --hard*)",

      "Edit(~/.bashrc)",
      "Edit(~/.zshrc)",
      "Edit(~/.ssh/**)",

      "Read(~/.ssh/**)",
      "Read(~/.gnupg/**)",
      "Read(~/.aws/**)",
      "Read(~/.azure/**)",
      "Read(~/.config/gh/**)",
      "Read(~/.git-credentials)",
      "Read(~/.docker/config.json)",
      "Read(~/.kube/**)",
      "Read(~/.npmrc)",
      "Read(~/.pypirc)"
    ]
  }
}
```

### Allow list: skip confirmation for safe commands

```jsonc
{
  "permissions": {
    "allow": [
      "Bash(pytest *)",
      "Bash(ruff check*)",
      "Bash(ruff format*)",
      "Read(src/**)",
      "Read(tests/**)",
      "Edit(src/**)",
      "Edit(tests/**)"
    ]
  }
}
```

---

## Environment Variables

```jsonc
{
  "env": {
    "DISABLE_TELEMETRY": "1",
    "NODE_ENV": "development",
    "PYTHONDONTWRITEBYTECODE": "1"
  }
}
```

Never put secrets in `settings.json` (it gets committed). Use `settings.local.json` instead.

---

## Complete Annotated Example

```jsonc
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",

  "env": {
    "DISABLE_TELEMETRY": "1"
  },

  "permissions": {
    "deny": [
      // Destructive commands
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Bash(curl *|bash*)",

      // Git safety
      "Bash(git push --force*)",
      "Bash(git push *--force*)",
      "Bash(git reset --hard*)",

      // Shell config protection
      "Edit(~/.bashrc)",
      "Edit(~/.zshrc)",
      "Edit(~/.ssh/**)",

      // Credential file protection
      "Read(~/.ssh/**)",
      "Read(~/.aws/**)",
      "Read(~/.git-credentials)",
      "Read(~/.docker/config.json)",
      "Read(~/.kube/**)"
    ]
  },

  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "branch=$(git branch --show-current 2>/dev/null); if [ \"$branch\" = \"main\" ] || [ \"$branch\" = \"master\" ]; then echo 'BLOCKED: Create a feature branch first.' >&2; exit 2; fi",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

See [templates/global/settings.json](../templates/global/settings.json) for the copy-paste version.

---

## Project-Level settings.json

Project settings extend global settings. They do not repeat global rules.

**Example: Auto-format on save**

```jsonc
// .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path // empty'); [ -z \"$FILE\" ] && exit 0; case \"$FILE\" in *.py) ruff format \"$FILE\" 2>/dev/null ;; *.ts|*.tsx) npx prettier --write \"$FILE\" 2>/dev/null ;; esac; exit 0",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

See [templates/project/settings.json](../templates/project/settings.json).

---

## settings.local.json

Personal, developer-specific overrides. Never committed to git.

### Setup

```bash
cat > .claude/settings.local.json << 'EOF'
{
  "env": {
    "DATABASE_URL": "postgresql://dev:devpass@localhost:5432/myapp_dev"
  }
}
EOF
```

Add to `.gitignore`:

```
.claude/settings.local.json
```

### Common use cases

**Allow Docker commands on your machine:**

```jsonc
{
  "permissions": {
    "allow": ["Bash(docker *)", "Bash(docker-compose *)"]
  }
}
```

---

## Merging Behavior

**Permissions merge additively.** A project cannot remove a global deny entry.

```
Global deny  + Project deny  = Combined deny (union)
Global allow + Project allow = Combined allow (union)
```

**Environment variables:** local overrides project for the same key.

```jsonc
// .claude/settings.json:     { "env": { "NODE_ENV": "test" } }
// .claude/settings.local.json: { "env": { "NODE_ENV": "development" } }
// Result: NODE_ENV = "development"
```

---

## Deny List vs Hooks

| Mechanism | Best for | Example |
|-----------|----------|---------|
| Deny list | Static patterns you never want | `Bash(rm -rf *)` |
| PreToolUse hook | Dynamic checks (branch name, file content) | Block edits on main branch |

Deny lists are evaluated first and are faster. Hooks run shell commands and can inspect tool input with `jq`.

---

## Troubleshooting

**"Why is Claude asking for permission?"** -- The command is not in `allow` or `deny`. Add it to `allow` to skip the prompt.

**"Why is Claude blocked?"** -- Check your deny list for overly broad patterns. `"Bash(git push*)"` blocks all pushes, not just force push.

**"settings.local.json not loading"** -- Verify valid JSON (no trailing commas), correct path (`.claude/settings.local.json`), and restart Claude Code.

---

## Next Steps

- [Chapter 4: Hooks](04-hooks.md) -- Deep dive into PreToolUse, PostToolUse, UserPromptSubmit
- [Chapter 5: Skills](05-skills.md) -- Domain knowledge and tool skills
