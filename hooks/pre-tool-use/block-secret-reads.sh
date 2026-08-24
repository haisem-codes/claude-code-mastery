#!/usr/bin/env bash
# PreToolUse hook: block reads of secret/credential files.
# Register with matcher "Bash|Read". Payload arrives as JSON on stdin.
set -u

command -v jq >/dev/null 2>&1 || {
  echo 'block-secret-reads: jq not found; refusing to fail open' >&2
  exit 2
}

PAYLOAD=$(cat)
CMD=$(printf '%s' "$PAYLOAD" | jq -r '.tool_input.command // empty')
FILE=$(printf '%s' "$PAYLOAD" | jq -r '.tool_input.file_path // empty')
TARGET="$CMD $FILE"

case "$TARGET" in
  " ") exit 0 ;;
esac

# Templates and samples are safe by design.
echo "$TARGET" | grep -qiE '\.(env|key|pem|p12)\.(example|sample|template)' && exit 0

if echo "$TARGET" | grep -qiE '\.(env|key|pem|p12)([[:space:]]|$|")|\.env\.|credentials\.json|secrets\.json|service-account|id_rsa|\.ssh/|\.aws/|\.gnupg/|\.npmrc|\.pypirc'; then
  echo 'BLOCKED: that path looks like a secret. Use an .example file or an env var.' >&2
  exit 2
fi
exit 0
