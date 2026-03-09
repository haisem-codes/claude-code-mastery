#!/usr/bin/env bash
# PostToolUse hook: Auto-run tests when test files are modified
# Usage: Add to settings.json under hooks.PostToolUse with matcher "Edit|Write"
FILE=$(echo "$TOOL_INPUT" | jq -r '.file_path // empty')
[ -z "$FILE" ] && exit 0
case "$FILE" in
  *test*.py|*_test.py)   pytest "$FILE" -x -q 2>/dev/null ;;
  *.test.ts|*.test.tsx|*.spec.ts) npx jest "$FILE" --silent 2>/dev/null ;;
esac
exit 0
