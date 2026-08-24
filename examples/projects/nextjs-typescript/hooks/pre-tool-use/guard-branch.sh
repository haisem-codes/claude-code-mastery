#!/usr/bin/env bash
# PreToolUse(Edit|Write|MultiEdit): on a protected branch, block edits to files INSIDE the repo.
# Writes outside the repo (e.g. the ~/.claude memory dir) are allowed even on main.
# exit 2 = block (stderr shown to Claude); exit 0 = allow. Default-safe outside git / on missing tools.
set -uo pipefail
payload="$(cat 2>/dev/null || true)"

branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
case "$branch" in
  main|master) ;;      # protected: fall through to the path check
  *) exit 0 ;;         # any other branch: allow
esac

msg="Blocked: editing '%s' on protected branch '$branch'. Create a feature branch first: git switch -c <type>/<slug>"

root="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
file="$(jq -r '.tool_input.file_path // empty' <<<"$payload" 2>/dev/null || true)"

# Can't determine target or repo root -> stay safe, block (preserves the old guarantee).
if [ -z "$file" ] || [ -z "$root" ]; then
  printf "$msg\n" "(unknown path)" >&2
  exit 2
fi

case "$file" in
  /*) abs="$file" ;;
  *)  abs="$root/$file" ;;
esac
abs="$(realpath -m "$abs" 2>/dev/null || echo "$abs")"
root="$(realpath -m "$root" 2>/dev/null || echo "$root")"

case "$abs" in
  "$root"/*|"$root")
    printf "$msg\n" "$file" >&2
    exit 2
    ;;
esac
exit 0   # target is outside the repo -> allow
