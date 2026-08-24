#!/usr/bin/env bash
# PostToolUse Edit|Write: auto-format touched file. Non-blocking.
set -u
payload=$(cat)
file=$(printf '%s' "$payload" | jq -r '.tool_input.file_path // empty')
[ -z "$file" ] && exit 0
case "$file" in
  *.ts|*.tsx|*.js|*.jsx|*.json) ;;
  *) exit 0 ;;
esac
[ -f "$file" ] || exit 0
cd "$CLAUDE_PROJECT_DIR" || exit 0
pnpm exec biome format --write "$file" >/dev/null 2>&1
exit 0
