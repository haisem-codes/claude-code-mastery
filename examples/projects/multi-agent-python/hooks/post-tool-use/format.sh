#!/usr/bin/env bash
# PostToolUse(Edit|Write|MultiEdit): auto-format + auto-fix the edited file. Never blocks.
set -uo pipefail
input="$(cat 2>/dev/null || true)"
f="$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null || true)"
[[ -z "$f" || ! -f "$f" ]] && exit 0

case "$f" in
  *.py)
    if command -v ruff >/dev/null 2>&1; then
      ruff check --fix --quiet "$f" >/dev/null 2>&1 || true
      ruff format --quiet "$f"     >/dev/null 2>&1 || true
    fi
    ;;
esac
exit 0
