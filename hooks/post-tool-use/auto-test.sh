#!/usr/bin/env bash
# PostToolUse hook: run the test file that was just edited.
# Register with matcher "Edit|MultiEdit|Write". Payload arrives on stdin.
set -u

command -v jq >/dev/null 2>&1 || exit 0

FILE=$(jq -r '.tool_input.file_path // empty')
{ [ -z "$FILE" ] || [ ! -f "$FILE" ]; } && exit 0

have() { command -v "$1" >/dev/null 2>&1; }

case "$FILE" in
  *test*.py|*_test.py)
      have pytest && pytest "$FILE" -x -q ;;
  *.test.ts|*.test.tsx|*.spec.ts|*.spec.tsx)
      have jest && jest "$FILE" --silent ;;
esac
exit 0
