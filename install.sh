#!/usr/bin/env bash
# claude-code-mastery installer.
#
# Installs selected skills, agents and hooks into your Claude Code config
# directory, merging settings rather than overwriting them, and recording a
# manifest so the install can be re-run or reversed.
#
#   ./install.sh --list                     show available presets
#   ./install.sh --preset backend-python    install a preset
#   ./install.sh --preset devops --dry-run  show what would change
#   ./install.sh --skills a,b --agents c    install specific items
#   ./install.sh --uninstall                remove what this installed
#
# Safe to run twice: unchanged files are skipped, locally-modified files are
# reported and left alone unless --force is given.
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
MANIFEST_NAME=".mastery-manifest.json"

PRESET=""
SEL_SKILLS=""
SEL_AGENTS=""
SEL_HOOKS=""
DRY=0
FORCE=0
ACTION="install"
NO_BACKUP=0

# ------------------------------------------------------------------ output
if [ -t 1 ]; then
  B=$'\033[1m'; DIM=$'\033[2m'; GRN=$'\033[32m'; YLW=$'\033[33m'; RED=$'\033[31m'; RST=$'\033[0m'
else
  B=""; DIM=""; GRN=""; YLW=""; RED=""; RST=""
fi
say()  { printf '%s\n' "$*"; }
head1(){ printf '\n%s%s%s\n' "$B" "$*" "$RST"; }
ok()   { printf '  %s✓%s %s\n' "$GRN" "$RST" "$*"; }
warn() { printf '  %s!%s %s\n' "$YLW" "$RST" "$*"; }
err()  { printf '  %s✗%s %s\n' "$RED" "$RST" "$*" >&2; }
die()  { printf '%serror:%s %s\n' "$RED" "$RST" "$*" >&2; exit 1; }

usage() {
  sed -n '2,18p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
}

# ------------------------------------------------------------------ args
while [ $# -gt 0 ]; do
  case "$1" in
    --preset)      PRESET="${2:-}"; [ -n "$PRESET" ] || die "--preset needs a value"; shift 2 ;;
    --skills)      SEL_SKILLS="${2:-}"; shift 2 ;;
    --agents)      SEL_AGENTS="${2:-}"; shift 2 ;;
    --hooks)       SEL_HOOKS="${2:-}"; shift 2 ;;
    --config-dir)  CONFIG_DIR="${2:-}"; [ -n "$CONFIG_DIR" ] || die "--config-dir needs a value"; shift 2 ;;
    --dry-run)     DRY=1; shift ;;
    --force)       FORCE=1; shift ;;
    --no-backup)   NO_BACKUP=1; shift ;;
    --list)        ACTION="list"; shift ;;
    --uninstall)   ACTION="uninstall"; shift ;;
    -h|--help)     usage ;;
    *)             die "unknown argument: $1 (try --help)" ;;
  esac
done

# ------------------------------------------------------------------ preflight
missing=""
for c in python3 git; do
  command -v "$c" >/dev/null 2>&1 || missing="$missing $c"
done
[ -n "$missing" ] && die "required command(s) not found:$missing"

command -v jq >/dev/null 2>&1 || \
  warn "jq not found — the safety hooks need it. macOS: brew install jq · Debian: apt install jq"

[ -f "$REPO/catalog.json" ] || {
  say "catalog.json missing, generating…"
  python3 "$REPO/scripts/catalog.py" >/dev/null || die "could not build catalog"
}

PY="python3 $REPO/scripts/installer_lib.py"

# ------------------------------------------------------------------ list
if [ "$ACTION" = "list" ]; then
  $PY list-presets --repo "$REPO"
  exit $?
fi

# ------------------------------------------------------------------ uninstall
if [ "$ACTION" = "uninstall" ]; then
  head1 "Uninstall from $CONFIG_DIR"
  [ -f "$CONFIG_DIR/$MANIFEST_NAME" ] || die "no manifest at $CONFIG_DIR/$MANIFEST_NAME — nothing to uninstall"
  $PY uninstall --repo "$REPO" --config-dir "$CONFIG_DIR" \
      $([ "$DRY" -eq 1 ] && echo --dry-run) $([ "$FORCE" -eq 1 ] && echo --force)
  exit $?
fi

# ------------------------------------------------------------------ resolve
if [ -z "$PRESET" ] && [ -z "$SEL_SKILLS" ] && [ -z "$SEL_AGENTS" ] && [ -z "$SEL_HOOKS" ]; then
  say "Nothing selected. Pick a preset:"
  say ""
  $PY list-presets --repo "$REPO"
  say ""
  say "  ./install.sh --preset <name>"
  say "  ./install.sh --preset <name> --dry-run     ${DIM}# preview first${RST}"
  exit 1
fi

head1 "claude-code-mastery → $CONFIG_DIR"
[ "$DRY" -eq 1 ] && say "${DIM}dry run — nothing will be written${RST}"

# ------------------------------------------------------------------ backup
if [ "$DRY" -eq 0 ] && [ "$NO_BACKUP" -eq 0 ] && [ -d "$CONFIG_DIR" ]; then
  STAMP="$(date +%Y%m%dT%H%M%S)"
  BACKUP="${CONFIG_DIR}.bak.${STAMP}"
  if cp -a "$CONFIG_DIR" "$BACKUP" 2>/dev/null; then
    ok "backed up $CONFIG_DIR → $BACKUP"
    echo "$BACKUP" > "$CONFIG_DIR/.mastery-last-backup"
  else
    warn "could not back up $CONFIG_DIR — continuing"
  fi
fi

# ------------------------------------------------------------------ install
$PY install \
  --repo "$REPO" \
  --config-dir "$CONFIG_DIR" \
  --preset "$PRESET" \
  --skills "$SEL_SKILLS" \
  --agents "$SEL_AGENTS" \
  --hooks "$SEL_HOOKS" \
  $([ "$DRY" -eq 1 ] && echo --dry-run) \
  $([ "$FORCE" -eq 1 ] && echo --force)
rc=$?

if [ $rc -ne 0 ]; then
  err "install failed (exit $rc)"
  exit $rc
fi

# ------------------------------------------------------------------ hooks exec bit
if [ "$DRY" -eq 0 ] && [ -d "$CONFIG_DIR/hooks" ]; then
  chmod +x "$CONFIG_DIR"/hooks/*.sh 2>/dev/null || true
fi

if [ "$DRY" -eq 0 ]; then
  head1 "Next steps"
  say "  1. Restart Claude Code so it picks up the new config."
  say "  2. Run ${B}/help${RST} and confirm your skills are listed."
  say "  3. Re-run this installer any time — it only applies what changed."
  say ""
  say "  Undo:      ./install.sh --uninstall"
  [ -f "$CONFIG_DIR/.mastery-last-backup" ] && \
    say "  Full restore: rm -rf \"$CONFIG_DIR\" && mv \"$(cat "$CONFIG_DIR/.mastery-last-backup")\" \"$CONFIG_DIR\""
fi
exit 0
