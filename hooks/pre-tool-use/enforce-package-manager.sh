#!/usr/bin/env bash
# PreToolUse hook: Enforce consistent package manager
# Usage: Customize ALLOWED_PM and add to settings.json
ALLOWED_PM="pnpm"  # Change to: npm, yarn, pnpm, or bun
CMD=$(echo "$TOOL_INPUT" | jq -r '.command // empty')
case "$CMD" in
  npm\ install*|npm\ i\ *|yarn\ add*|yarn\ install*|bun\ add*|bun\ install*)
    if ! echo "$CMD" | grep -q "^$ALLOWED_PM"; then
      echo "BLOCKED: Use $ALLOWED_PM instead. This project enforces $ALLOWED_PM as the package manager." >&2
      exit 2
    fi
    ;;
esac
