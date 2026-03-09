#!/usr/bin/env bash
# PreToolUse hook: Block edits on main/master branch
# Usage: Add to settings.json under hooks.PreToolUse with matcher "Edit|MultiEdit|Write"
branch=$(git branch --show-current 2>/dev/null)
if [ "$branch" = "main" ] || [ "$branch" = "master" ]; then
  echo '{"decision":"block","reason":"Cannot edit files on main/master. Create a feature branch first."}' >&2
  exit 2
fi
