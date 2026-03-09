#!/usr/bin/env bash
# PostToolUse hook: Run linter on edited files
# Usage: Add to settings.json under hooks.PostToolUse with matcher "Edit|Write"
FILE=$(echo "$TOOL_INPUT" | jq -r '.file_path // empty')
[ -z "$FILE" ] && exit 0
case "$FILE" in
  *.py)     ruff check --fix "$FILE" 2>/dev/null ;;
  *.ts|*.tsx) npx eslint --fix "$FILE" 2>/dev/null ;;
esac
exit 0
