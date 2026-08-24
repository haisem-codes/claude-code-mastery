#!/usr/bin/env bash
# Stop hook: the "don't quit early" backstop for an active /note-loop.
# Default-safe: only engages when a loop is explicitly active. Capped to avoid runaway.
#   - no state / active:false / NOTE_LOOP_OFF=1   -> allow stop
#   - all acceptance criteria checked             -> allow stop (done)
#   - iteration >= max_iterations                 -> allow stop (safety cap, warns)
#   - otherwise                                   -> bump iteration, block stop (continue loop)
set -uo pipefail
cat >/dev/null 2>&1 || true   # drain stdin

proj="${CLAUDE_PROJECT_DIR:-$(pwd)}"
state="$proj/.claude/loop-state.local.json"

[[ "${NOTE_LOOP_OFF:-0}" == "1" ]] && exit 0
[[ -f "$state" ]] || exit 0
[[ "$(jq -r '.active // false' "$state" 2>/dev/null || echo false)" == "true" ]] || exit 0

task_file="$(jq -r '.task_file // empty' "$state" 2>/dev/null || true)"
iter="$(jq -r '.iteration // 1' "$state" 2>/dev/null || echo 1)"
max="$(jq -r '.max_iterations // 12' "$state" 2>/dev/null || echo 12)"

# Count unchecked acceptance boxes under "## Acceptance criteria".
unchecked=0
if [[ -n "$task_file" && -f "$proj/$task_file" ]]; then
  unchecked="$(awk '
    /^##[[:space:]]+[Aa]cceptance/ {inb=1; next}
    inb && /^##[[:space:]]/         {inb=0}
    inb && /^[[:space:]]*-[[:space:]]*\[[[:space:]]\]/ {n++}
    END {print n+0}' "$proj/$task_file")"
fi

deactivate() { local t; t="$(mktemp)"; jq '.active=false' "$state" >"$t" 2>/dev/null && mv "$t" "$state" || rm -f "$t"; }

if [[ "$unchecked" -eq 0 ]]; then
  deactivate
  echo "Notetaker loop complete: all acceptance criteria met."
  exit 0
fi

if [[ "$iter" -ge "$max" ]]; then
  deactivate
  echo "Notetaker loop hit max_iterations ($max) with $unchecked criterion(s) unmet — stopping. Review $task_file." >&2
  exit 0
fi

next=$((iter + 1))
t="$(mktemp)"; jq --argjson n "$next" '.iteration=$n' "$state" >"$t" 2>/dev/null && mv "$t" "$state" || rm -f "$t"
reason="Notetaker loop not done: $unchecked acceptance criterion(s) in '$task_file' still unchecked. Continue the loop (BUILD -> VERIFY -> GATE per .claude/rules/orchestration.md), then check the boxes you've satisfied. Iteration $next/$max. To stop early: set active:false in .claude/loop-state.local.json or export NOTE_LOOP_OFF=1."
jq -n --arg r "$reason" '{decision:"block", reason:$r}'
exit 0
