#!/usr/bin/env bash
# PostToolUse(Edit|Write|MultiEdit): auto-format + auto-fix the edited file. Never blocks.
# Python -> ruff. Web files (ts/tsx/js/jsx/css/html/json/md) -> prettier if the frontend has it.
set -uo pipefail
input="$(cat 2>/dev/null || true)"
f="$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null || true)"
[[ -z "$f" || ! -f "$f" ]] && exit 0

proj="${CLAUDE_PROJECT_DIR:-$(pwd)}"

case "$f" in
  *.py)
    if command -v ruff >/dev/null 2>&1; then
      ruff check --fix --quiet "$f" >/dev/null 2>&1 || true
      ruff format --quiet "$f"     >/dev/null 2>&1 || true
    fi
    ;;
  *.ts|*.tsx|*.js|*.jsx|*.css|*.html|*.json)
    prettier=""
    if [[ -x "$proj/frontend/node_modules/.bin/prettier" ]]; then
      prettier="$proj/frontend/node_modules/.bin/prettier"
    elif command -v prettier >/dev/null 2>&1; then
      prettier="prettier"
    fi
    [[ -n "$prettier" ]] && "$prettier" --write --log-level silent "$f" >/dev/null 2>&1 || true
    ;;
esac
exit 0
