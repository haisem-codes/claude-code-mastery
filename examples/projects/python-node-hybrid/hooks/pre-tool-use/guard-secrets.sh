#!/usr/bin/env bash
# PreToolUse(Read|Bash): block reading secret-like files. exit 2 = block.
set -uo pipefail
input="$(cat 2>/dev/null || true)"
tool="$(printf '%s' "$input" | jq -r '.tool_name // empty' 2>/dev/null || true)"

secret_re='(\.env($|\.)|\.key($|[^a-zA-Z])|\.pem($|[^a-zA-Z])|\.p12($|[^a-zA-Z])|id_rsa|credentials|secrets?\.(json|ya?ml|txt)|\.netrc|\.pypirc|\.npmrc|\.git-credentials|\.token($|[^a-zA-Z]))'

case "$tool" in
  Read)
    f="$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null || true)"
    if [[ -n "$f" && "$f" =~ $secret_re ]]; then
      echo "Blocked: reading secret-like file '$f'. Use .env.example / env vars instead." >&2
      exit 2
    fi
    ;;
  Bash)
    cmd="$(printf '%s' "$input" | jq -r '.tool_input.command // empty' 2>/dev/null || true)"
    reader='(cat|less|bat|head|tail|grep|rg|strings|xxd|od|nano|vim|view|more|cp|scp)[[:space:]]'
    full="$reader[^|;&]*$secret_re"
    if [[ -n "$cmd" && "$cmd" =~ $full ]]; then
      echo "Blocked: command accesses a secret-like file. Use env vars / .env.example." >&2
      exit 2
    fi
    ;;
esac
exit 0
