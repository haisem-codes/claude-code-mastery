#!/usr/bin/env bash
# End-to-end tests for install.sh against throwaway config dirs.
# Never touches the real ~/.claude — every case uses its own mktemp dir.
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO" || exit 1

pass=0; fail=0
check() {           # check <label> <condition-result>
  if [ "$2" = "0" ]; then printf '  ok    %s\n' "$1"; pass=$((pass+1))
  else printf '  FAIL  %s\n' "$1"; fail=$((fail+1)); fi
}
newdir() { mktemp -d "${TMPDIR:-/tmp}/ccm-test.XXXXXX"; }

# ---------------------------------------------------------------- 1. clean install
echo "1. clean install"
A=$(newdir)
./install.sh --preset minimal --config-dir "$A" --no-backup >/dev/null 2>&1
check "skills land at skills/<name>/SKILL.md" \
      "$([ -f "$A/skills/pr-review-expert/SKILL.md" ] && echo 0 || echo 1)"
check "agents land at agents/<name>.md" \
      "$([ -f "$A/agents/debugger.md" ] && echo 0 || echo 1)"
check "hooks are executable" \
      "$([ -x "$A/hooks/block-main-branch.sh" ] && echo 0 || echo 1)"
check "manifest written" \
      "$([ -f "$A/.mastery-manifest.json" ] && echo 0 || echo 1)"
check "settings.json is valid JSON" \
      "$(python3 -c "import json,sys;json.load(open('$A/settings.json'))" >/dev/null 2>&1 && echo 0 || echo 1)"

# ---------------------------------------------------------------- 2. idempotency
echo "2. re-run is a no-op"
OUT=$(./install.sh --preset minimal --config-dir "$A" --no-backup 2>&1)
check "reports 0 new" "$(echo "$OUT" | grep -q '0 new' && echo 0 || echo 1)"
check "reports unchanged items" "$(echo "$OUT" | grep -qE '[1-9][0-9]* unchanged' && echo 0 || echo 1)"

# ---------------------------------------------------------------- 3. merge, not replace
echo "3. merge preserves an existing config"
B=$(newdir)
cat > "$B/settings.json" <<'JSON'
{
  "model": "opus[1m]",
  "theme": "dark",
  "env": { "MY_OWN_VAR": "keep-me" },
  "permissions": { "allow": ["Bash(mytool:*)"], "deny": ["Bash(danger:*)"] }
}
JSON
./install.sh --preset minimal --config-dir "$B" --no-backup >/dev/null 2>&1
q() { python3 -c "import json;d=json.load(open('$B/settings.json'));print($1)" 2>/dev/null; }
check "user model preserved"        "$([ "$(q "d.get('model')")" = "opus[1m]" ] && echo 0 || echo 1)"
check "user theme preserved"        "$([ "$(q "d.get('theme')")" = "dark" ] && echo 0 || echo 1)"
check "user env var preserved"      "$([ "$(q "d['env'].get('MY_OWN_VAR')")" = "keep-me" ] && echo 0 || echo 1)"
check "user allow rule preserved"   "$([ "$(q "'Bash(mytool:*)' in d['permissions']['allow']")" = "True" ] && echo 0 || echo 1)"
check "user deny rule preserved"    "$([ "$(q "'Bash(danger:*)' in d['permissions']['deny']")" = "True" ] && echo 0 || echo 1)"
check "template deny rules unioned in" "$([ "$(q "len(d['permissions']['deny'])>1")" = "True" ] && echo 0 || echo 1)"
check "hooks added"                 "$([ "$(q "'PreToolUse' in d.get('hooks',{})")" = "True" ] && echo 0 || echo 1)"

# ---------------------------------------------------------------- 4. local edits protected
echo "4. locally modified files are not clobbered"
echo "# my own edit" >> "$A/agents/debugger.md"
OUT=$(./install.sh --preset minimal --config-dir "$A" --no-backup 2>&1)
check "modified file is skipped" "$(echo "$OUT" | grep -q 'locally modified' && echo 0 || echo 1)"
check "my edit survived" \
      "$(grep -q '# my own edit' "$A/agents/debugger.md" && echo 0 || echo 1)"
OUT=$(./install.sh --preset minimal --config-dir "$A" --no-backup --force 2>&1)
check "--force overwrites it" \
      "$(grep -q '# my own edit' "$A/agents/debugger.md" && echo 1 || echo 0)"

# ---------------------------------------------------------------- 5. unknown ids rejected
echo "5. bad input is rejected"
C=$(newdir)
./install.sh --skills "engineering/does-not-exist" --config-dir "$C" --no-backup >/dev/null 2>&1
check "unknown skill exits non-zero" "$([ $? -ne 0 ] && echo 0 || echo 1)"
./install.sh --preset no-such-preset --config-dir "$C" --no-backup >/dev/null 2>&1
check "unknown preset exits non-zero" "$([ $? -ne 0 ] && echo 0 || echo 1)"

# ---------------------------------------------------------------- 6. collision prefixing
echo "6. name collisions are prefixed"
D=$(newdir)
./install.sh --skills "anthropic-official/brand-guidelines,marketing/brand-guidelines" \
             --config-dir "$D" --no-backup >/dev/null 2>&1
check "both variants installed under distinct names" \
      "$([ "$(ls "$D/skills" | wc -l | tr -d ' ')" = "2" ] && echo 0 || echo 1)"

# ---------------------------------------------------------------- 7. uninstall
echo "7. uninstall"
E=$(newdir)
./install.sh --preset minimal --config-dir "$E" --no-backup >/dev/null 2>&1
mkdir -p "$E/skills/my-own-skill" && echo "mine" > "$E/skills/my-own-skill/SKILL.md"
./install.sh --uninstall --config-dir "$E" >/dev/null 2>&1
check "installed skill removed" \
      "$([ ! -d "$E/skills/pr-review-expert" ] && echo 0 || echo 1)"
check "user's own skill left alone" \
      "$([ -f "$E/skills/my-own-skill/SKILL.md" ] && echo 0 || echo 1)"
check "settings.json left in place" \
      "$([ -f "$E/settings.json" ] && echo 0 || echo 1)"

echo
echo "passed $pass, failed $fail"
[ "$fail" -eq 0 ]
