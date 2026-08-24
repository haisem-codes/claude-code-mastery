#!/usr/bin/env bash
# PreToolUse hook for Bash — blocks destructive commands even if permissions slip
# Exit 2 = block + send stderr back to Claude
input=$(cat)
cmd=$(jq -r '.tool_input.command // ""' <<<"$input" 2>/dev/null)
[ -z "$cmd" ] && exit 0

block() { echo "BLOCKED by safety hook: $1" >&2; exit 2; }

# Recursive force removal
[[ "$cmd" =~ rm[[:space:]]+(-[a-zA-Z]*r[a-zA-Z]*f|-rf|-fr|--recursive[[:space:]]+--force) ]] && \
  block "destructive rm -rf"
# Filesystem destruction
[[ "$cmd" =~ ^[[:space:]]*mkfs ]] && block "mkfs is destructive"
[[ "$cmd" =~ ^[[:space:]]*dd[[:space:]]+.*if=/dev ]] && block "dd from device"
# Curl/wget piped to a shell
[[ "$cmd" =~ (curl|wget)[^\|]*\|[[:space:]]*(bash|sh|zsh) ]] && \
  block "curl|sh pattern — download, inspect, then execute"
# Git destructive
[[ "$cmd" =~ git[[:space:]]+push[[:space:]]+.*--force ]] && \
  [[ ! "$cmd" =~ --force-with-lease ]] && block "git push --force (use --force-with-lease)"
[[ "$cmd" =~ git[[:space:]]+reset[[:space:]]+.*--hard ]] && block "git reset --hard"
[[ "$cmd" =~ git[[:space:]]+clean[[:space:]]+.*-f ]] && block "git clean -f"
# sudo
[[ "$cmd" =~ ^[[:space:]]*sudo[[:space:]] ]] && block "sudo from inside Claude is not allowed"

exit 0
