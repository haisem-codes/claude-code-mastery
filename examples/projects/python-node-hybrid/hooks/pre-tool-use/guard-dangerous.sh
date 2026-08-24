#!/usr/bin/env bash
# PreToolUse(Bash): block destructive / unsafe commands. exit 2 = block.
set -uo pipefail
input="$(cat 2>/dev/null || true)"
cmd="$(printf '%s' "$input" | jq -r '.tool_input.command // empty' 2>/dev/null || true)"
[[ -z "$cmd" ]] && exit 0

block() { echo "Blocked: $1. If this is intentional, run it yourself (e.g. via '! $cmd') or adjust the request." >&2; exit 2; }

shopt -s nocasematch
if [[ "$cmd" =~ (^|[^[:alnum:]])rm[[:space:]]+(-[a-z]*[rf][a-z]*[rf]|-rf|-fr) ]]; then block "recursive force remove (rm -rf)"; fi
if [[ "$cmd" =~ (^|[[:space:]])sudo[[:space:]]   ]]; then block "sudo"; fi
if [[ "$cmd" =~ (^|[[:space:]])mkfs            ]]; then block "mkfs"; fi
if [[ "$cmd" =~ (^|[[:space:]])dd[[:space:]]+if= ]]; then block "dd if=..."; fi
if [[ "$cmd" =~ (curl|wget)[[:space:]].*\|[[:space:]]*(ba)?sh ]]; then block "pipe-to-shell (curl|bash)"; fi
if [[ "$cmd" =~ git[[:space:]]+push[[:space:]].*--force([^-]|$) ]]; then block "git push --force (use --force-with-lease, and ask first)"; fi
if [[ "$cmd" =~ git[[:space:]]+reset[[:space:]]+--hard ]]; then block "git reset --hard (destructive)"; fi
if [[ "$cmd" =~ git[[:space:]]+clean[[:space:]]+-[a-z]*f ]]; then block "git clean -f (destructive)"; fi
if [[ "$cmd" =~ chmod[[:space:]]+(-R[[:space:]]+)?0?777 ]]; then block "chmod 777"; fi
exit 0
