#!/usr/bin/env bash
# PreToolUse hook: Block reading secret/credential files
# Usage: Add to settings.json under hooks.PreToolUse with matcher "Bash"
CMD=$(echo "$TOOL_INPUT" | jq -r '.command // empty')
if echo "$CMD" | grep -qiE '\.(env|key|pem|p12)(\s|$|")|credentials\.json|secrets\.json|service-account'; then
  echo 'BLOCKED: Reading secret/credential files is not allowed' >&2
  exit 2
fi
