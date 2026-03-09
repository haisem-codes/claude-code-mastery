#!/usr/bin/env bash
# PreToolUse hook: Block dangerous shell commands
# Usage: Add to settings.json under hooks.PreToolUse with matcher "Bash"
CMD=$(echo "$TOOL_INPUT" | jq -r '.command // empty')
if echo "$CMD" | grep -qE 'rm[[:space:]]+-[^[:space:]]*r[^[:space:]]*f'; then
  echo 'BLOCKED: Use trash or specific file deletion instead of rm -rf' >&2
  exit 2
fi
if echo "$CMD" | grep -qE 'git[[:space:]]+push.*(--force|--force-with-lease)'; then
  echo 'BLOCKED: Force push requires explicit user approval' >&2
  exit 2
fi
if echo "$CMD" | grep -qE 'git[[:space:]]+reset[[:space:]]+--hard'; then
  echo 'BLOCKED: Hard reset requires explicit user approval' >&2
  exit 2
fi
if echo "$CMD" | grep -qE '^sudo[[:space:]]'; then
  echo 'BLOCKED: sudo commands are not allowed' >&2
  exit 2
fi
