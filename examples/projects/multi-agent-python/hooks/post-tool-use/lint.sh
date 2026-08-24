#!/usr/bin/env bash
# PostToolUse(Edit|Write|MultiEdit): fast per-file lint gate for Python.
# After format.sh auto-fixes, any remaining ruff error is real -> surface it (exit 2)
# so Claude fixes before moving on. mypy/pytest run at VERIFY time, not here.
set -uo pipefail
input="$(cat 2>/dev/null || true)"
f="$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null || true)"
[[ -z "$f" || ! -f "$f" ]] && exit 0
[[ "$f" == *.py ]] || exit 0
command -v ruff >/dev/null 2>&1 || exit 0

if ! out="$(ruff check "$f" 2>&1)"; then
  {
    echo "ruff reports issues in $f — fix before continuing:"
    echo "$out"
  } >&2
  exit 2
fi
exit 0
