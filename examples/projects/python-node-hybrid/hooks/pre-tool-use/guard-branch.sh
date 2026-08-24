#!/usr/bin/env bash
# PreToolUse(Edit|Write|MultiEdit): block edits on protected branches.
# exit 2 = block (stderr shown to Claude); exit 0 = allow. Default-safe outside git.
set -uo pipefail
cat >/dev/null 2>&1 || true   # drain stdin

# --show-current also reports unborn branches (fresh repo, no commits yet)
branch="$(git branch --show-current 2>/dev/null || true)"
case "$branch" in
  main|master)
    echo "Blocked: editing on protected branch '$branch'. Create a feature branch first: git switch -c <type>/<slug>" >&2
    exit 2
    ;;
esac
exit 0
