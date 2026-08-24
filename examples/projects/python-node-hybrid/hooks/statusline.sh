#!/usr/bin/env bash
# Status line: "notetaker  ⎇ <branch>  ◆ loop:<task> <iter>/<max>" when a loop is active.
set -uo pipefail
input="$(cat 2>/dev/null || true)"
proj="$(printf '%s' "$input" | jq -r '.workspace.current_dir // .cwd // empty' 2>/dev/null || true)"
[[ -z "$proj" ]] && proj="$(pwd)"

branch="$(git -C "$proj" branch --show-current 2>/dev/null)"
if [[ -z "$branch" ]]; then
  git -C "$proj" rev-parse --git-dir >/dev/null 2>&1 && branch="detached" || branch="no-git"
fi

loop=""
state="$proj/.claude/loop-state.local.json"
if [[ -f "$state" ]] && [[ "$(jq -r '.active // false' "$state" 2>/dev/null || echo false)" == "true" ]]; then
  t="$(jq -r '.task // "?"' "$state" 2>/dev/null || echo '?')"
  i="$(jq -r '.iteration // "?"' "$state" 2>/dev/null || echo '?')"
  m="$(jq -r '.max_iterations // "?"' "$state" 2>/dev/null || echo '?')"
  loop="  ◆ loop:$t $i/$m"
fi

printf 'notetaker  ⎇ %s%s' "$branch" "$loop"
