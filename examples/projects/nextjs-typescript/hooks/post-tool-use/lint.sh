#!/usr/bin/env bash
# PostToolUse Edit|Write: lint touched file. Blocks (exit 2) on errors so they surface immediately.
set -u
payload=$(cat)
file=$(printf '%s' "$payload" | jq -r '.tool_input.file_path // empty')
[ -z "$file" ] && exit 0
case "$file" in
  *.ts|*.tsx|*.js|*.jsx) ;;
  *) exit 0 ;;
esac
[ -f "$file" ] || exit 0
cd "$CLAUDE_PROJECT_DIR" || exit 0
pnpm exec biome --version >/dev/null 2>&1 || exit 0
out=$(pnpm exec biome lint "$file" 2>&1)
if [ $? -ne 0 ]; then
  echo "biome lint failed for $file:" >&2
  echo "$out" | head -30 >&2
  exit 2
fi
exit 0
