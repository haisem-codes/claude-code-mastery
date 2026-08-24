#!/usr/bin/env bash
# PostToolUse hook: format a file after it is edited.
# Register with matcher "Edit|MultiEdit|Write". Payload arrives on stdin.
set -u

command -v jq >/dev/null 2>&1 || exit 0

FILE=$(jq -r '.tool_input.file_path // empty')
{ [ -z "$FILE" ] || [ ! -f "$FILE" ]; } && exit 0

have() { command -v "$1" >/dev/null 2>&1; }

case "$FILE" in
  *.py)                   have ruff     && ruff format "$FILE" ;;
  *.ts|*.tsx|*.js|*.jsx|*.json|*.css|*.md)
                          have prettier && prettier --write "$FILE" ;;
  *.go)                   have gofmt    && gofmt -w "$FILE" ;;
  *.rs)                   have rustfmt  && rustfmt "$FILE" ;;
esac
exit 0
