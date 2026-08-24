#!/usr/bin/env bash
# PreToolUse hook for Read — block reads of secret files
input=$(cat)
fp=$(jq -r '.tool_input.file_path // ""' <<<"$input" 2>/dev/null)
[ -z "$fp" ] && exit 0

# Allowed examples (templates)
case "$fp" in
  *.env.example|*.env.sample|*.env.template) exit 0 ;;
esac

# Block patterns
block_msg() { echo "BLOCKED: reading secret-bearing file '$1' is prohibited." >&2; exit 2; }

case "$fp" in
  *.env|*.env.local|*.env.production|*.env.*.local) block_msg "$fp" ;;
  *credentials*) block_msg "$fp" ;;
  *.pem|*.key) block_msg "$fp" ;;
  */.ssh/*|*/.gnupg/*|*/.aws/*|*/.azure/*|*/.kube/*) block_msg "$fp" ;;
  */.config/gh/*|*/.git-credentials|*/.npmrc|*/.pypirc) block_msg "$fp" ;;
  */.docker/config.json) block_msg "$fp" ;;
esac

exit 0
