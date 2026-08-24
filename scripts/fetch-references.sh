#!/usr/bin/env bash
# Clone the upstream reference repositories listed in resources/reference-repos.json
# into references/ so Claude Code can read them alongside this repo.
#
# They are cloned, never vendored: each stays on its own upstream, keeps its own
# license, and can be refreshed with --update. references/ is gitignored.
#
#   ./scripts/fetch-references.sh              # all repos, shallow
#   ./scripts/fetch-references.sh --skip-large # omit anything over 100 MB
#   ./scripts/fetch-references.sh --update     # git pull each existing clone
#   ./scripts/fetch-references.sh --list       # show what would be cloned
#   ./scripts/fetch-references.sh --full       # full history instead of --depth 1
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$REPO/references"
MANIFEST="$REPO/resources/reference-repos.json"

DEPTH="--depth 1"
SKIP_LARGE=0
MODE="clone"

while [ $# -gt 0 ]; do
  case "$1" in
    --skip-large) SKIP_LARGE=1; shift ;;
    --update)     MODE="update"; shift ;;
    --list)       MODE="list"; shift ;;
    --full)       DEPTH=""; shift ;;
    --dest)       DEST="${2:?--dest needs a path}"; shift 2 ;;
    -h|--help)    sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *)            echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

command -v git >/dev/null 2>&1 || { echo "git is required" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "python3 is required" >&2; exit 1; }
[ -f "$MANIFEST" ] || { echo "missing $MANIFEST" >&2; exit 1; }

# name<TAB>slug<TAB>size_mb<TAB>license<TAB>why
rows=$(python3 - "$MANIFEST" "$SKIP_LARGE" <<'PY'
import json, sys
manifest, skip_large = sys.argv[1], sys.argv[2] == "1"
for r in json.load(open(manifest))["repos"]:
    if skip_large and r.get("size_mb", 0) > 100:
        continue
    print("\t".join([r["name"], r["slug"], str(r.get("size_mb", "?")),
                     r.get("license", "?"), r.get("why", "")]))
PY
)

if [ "$MODE" = "list" ]; then
  printf '%-28s %-38s %6s  %s\n' NAME SLUG SIZE LICENSE
  printf '%s\n' "$rows" | while IFS=$'\t' read -r name slug size lic why; do
    printf '%-28s %-38s %5sM  %s\n' "$name" "$slug" "$size" "$lic"
  done
  exit 0
fi

mkdir -p "$DEST"
total=$(printf '%s\n' "$rows" | grep -c .)
n=0; cloned=0; updated=0; failed=0

printf '\nReference repositories -> %s\n\n' "$DEST"

printf '%s\n' "$rows" | while IFS=$'\t' read -r name slug size lic why; do
  n=$((n+1))
  target="$DEST/$name"

  if [ -d "$target/.git" ]; then
    if [ "$MODE" = "update" ]; then
      printf '  [%2d/%2d] updating %-26s ' "$n" "$total" "$name"
      if git -C "$target" pull --quiet --ff-only 2>/dev/null; then
        echo "ok"
      else
        echo "skipped (diverged or shallow)"
      fi
    else
      printf '  [%2d/%2d] %-26s already present\n' "$n" "$total" "$name"
    fi
    continue
  fi

  printf '  [%2d/%2d] cloning  %-26s (%sM, %s) ... ' "$n" "$total" "$name" "$size" "$lic"
  # shellcheck disable=SC2086
  if git clone --quiet $DEPTH "https://github.com/$slug.git" "$target" 2>/dev/null; then
    echo "ok"
  else
    echo "FAILED"
  fi
done

echo
present=$(find "$DEST" -maxdepth 2 -name .git -type d 2>/dev/null | wc -l | tr -d ' ')
echo "  $present of $total reference repos present in $DEST"
echo
echo "  These are third-party repositories under their own licenses."
echo "  See resources/reference-repos.md before reusing anything from them."
