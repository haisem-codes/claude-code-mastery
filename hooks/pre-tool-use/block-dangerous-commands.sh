#!/usr/bin/env bash
# PreToolUse hook: block destructive shell commands.
# Register with matcher "Bash". Payload arrives as JSON on stdin.
set -u

command -v jq >/dev/null 2>&1 || {
  echo 'block-dangerous-commands: jq not found; refusing to fail open' >&2
  exit 2
}

CMD=$(jq -r '.tool_input.command // empty')
[ -z "$CMD" ] && exit 0

block() { echo "BLOCKED: $1" >&2; exit 2; }

echo "$CMD" | grep -qE 'rm[[:space:]]+-[^[:space:]]*r[^[:space:]]*f' \
  && block 'recursive force delete. Remove specific paths, or use trash.'

# --force-with-lease is the safe form and stays allowed.
echo "$CMD" | grep -qE 'git[[:space:]]+push[^|;&]*--force([^-]|$)' \
  && block 'force push. Use --force-with-lease if you must rewrite history.'

echo "$CMD" | grep -qE 'git[[:space:]]+reset[[:space:]]+--hard' \
  && block 'hard reset discards uncommitted work.'

echo "$CMD" | grep -qE 'git[[:space:]]+clean[[:space:]]+-[a-z]*f' \
  && block 'git clean -f deletes untracked files.'

echo "$CMD" | grep -qE '(^|[;&|][[:space:]]*)sudo[[:space:]]' \
  && block 'sudo. Run privileged commands yourself.'

echo "$CMD" | grep -qE 'mkfs|dd[[:space:]]+if=/dev' \
  && block 'destructive disk operation.'

echo "$CMD" | grep -qE '(curl|wget)[^|]*\|[[:space:]]*(ba|z)?sh' \
  && block 'piping a download into a shell. Download, read, then run.'

exit 0
