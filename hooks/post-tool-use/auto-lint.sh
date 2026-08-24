#!/usr/bin/env bash
# PostToolUse hook: lint-fix a file after it is edited.
# Register with matcher "Edit|MultiEdit|Write". Payload arrives on stdin.
set -u

command -v jq >/dev/null 2>&1 || exit 0

FILE=$(jq -r '.tool_input.file_path // empty')
{ [ -z "$FILE" ] || [ ! -f "$FILE" ]; } && exit 0

have() { command -v "$1" >/dev/null 2>&1; }

case "$FILE" in
  *.py)        have ruff   && ruff check --fix "$FILE" ;;
  *.ts|*.tsx)  have eslint && eslint --fix "$FILE" ;;
esac
exit 0
