#!/usr/bin/env bash
# SessionStart hook — injects lightweight project context + memory-bloat warning
# Output JSON with hookSpecificOutput.additionalContext to inject into the session

ctx=""

# Git context if in a repo
if git rev-parse --git-dir >/dev/null 2>&1; then
  branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
  dirty=$(git status --porcelain 2>/dev/null | wc -l)
  ctx+="Branch: $branch"
  [ "$dirty" -gt 0 ] && ctx+=" (uncommitted: $dirty files)"
  ctx+=$'\n'
fi

# Auto-memory size warning
mem_dir="$HOME/.claude/projects"
if [ -d "$mem_dir" ]; then
  total_kb=$(du -sk "$mem_dir" 2>/dev/null | awk '{print $1}')
  if [ "${total_kb:-0}" -gt 1024 ]; then
    ctx+="⚠ auto-memory exceeds 1MB across all projects — consider /memory-audit"$'\n'
  fi
  # Per-project MEMORY.md line check (current project only)
  cwd_slug=$(pwd | tr '/' '-')
  mem_file="$mem_dir/$cwd_slug/memory/MEMORY.md"
  if [ -f "$mem_file" ]; then
    lines=$(wc -l < "$mem_file")
    if [ "$lines" -gt 200 ]; then
      ctx+="⚠ MEMORY.md is $lines lines (>200 cap) — /memory-audit recommended"$'\n'
    fi
  fi
fi

# Local CONTEXT.md (project-specific, optional)
[ -f .claude/CONTEXT.md ] && ctx+=$'--- .claude/CONTEXT.md ---\n'"$(head -c 1500 .claude/CONTEXT.md)"$'\n'

[ -z "$ctx" ] && { echo '{}'; exit 0; }

jq -nc --arg c "$ctx" '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:$c}}'
