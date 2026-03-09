#!/usr/bin/env bash
# PostToolUse hook: Auto-format files after editing
# Usage: Add to settings.json under hooks.PostToolUse with matcher "Edit|Write"
FILE=$(echo "$TOOL_INPUT" | jq -r '.file_path // empty')
[ -z "$FILE" ] && exit 0
case "$FILE" in
  *.py)     ruff format "$FILE" 2>/dev/null ;;
  *.ts|*.tsx|*.js|*.jsx) npx prettier --write "$FILE" 2>/dev/null ;;
  *.go)     gofmt -w "$FILE" 2>/dev/null ;;
  *.rs)     rustfmt "$FILE" 2>/dev/null ;;
esac
exit 0
