#!/usr/bin/env bash
# PreToolUse hook: enforce one package manager across a project.
# Set ALLOWED_PM, register with matcher "Bash". Payload arrives on stdin.
set -u

ALLOWED_PM="${ALLOWED_PM:-pnpm}"   # npm | yarn | pnpm | bun

command -v jq >/dev/null 2>&1 || exit 0   # advisory hook: degrade quietly

CMD=$(jq -r '.tool_input.command // empty')
[ -z "$CMD" ] && exit 0

case "$CMD" in
  npm\ install*|npm\ i\ *|npm\ add*|yarn\ add*|yarn\ install*|bun\ add*|bun\ install*|pnpm\ add*|pnpm\ install*)
    case "$CMD" in
      "$ALLOWED_PM"\ *) exit 0 ;;
      *)
        echo "BLOCKED: this project uses $ALLOWED_PM. Re-run the command with $ALLOWED_PM." >&2
        exit 2
        ;;
    esac
    ;;
esac
exit 0
