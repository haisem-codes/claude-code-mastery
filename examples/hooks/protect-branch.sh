#!/usr/bin/env bash
# PreToolUse hook for Edit/MultiEdit/Write — block edits when on main/master
input=$(cat)
fp=$(jq -r '.tool_input.file_path // ""' <<<"$input" 2>/dev/null)
[ -z "$fp" ] && exit 0

# Only check if file is inside a git repo
dir=$(dirname -- "$fp")
[ -d "$dir" ] || exit 0
branch=$(git -C "$dir" rev-parse --abbrev-ref HEAD 2>/dev/null) || exit 0

case "$branch" in
  main|master|develop)
    echo "BLOCKED: on branch '$branch'. Create a feature branch before editing files:" >&2
    echo "  git switch -c <type>/<short-slug>" >&2
    exit 2
    ;;
esac
exit 0
