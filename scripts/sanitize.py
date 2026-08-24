#!/usr/bin/env python3
"""Redaction gate for examples/.

This repository is public. examples/ is derived from a real working machine, so
every file that lands there must be scrubbed of anything identifying: names,
emails, phone numbers, IPs, absolute home paths, client names, tokens.

Two modes:

    python3 scripts/sanitize.py --check            # CI gate: exit 1 on any hit
    python3 scripts/sanitize.py --scrub SRC DST    # copy SRC->DST, redacting

--check scans examples/ (or --path) and reports file:line for every match. It is
deliberately noisy: a false positive costs a minute, a leak is permanent.

Stdlib only, Python 3.8+.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Extensions worth scanning. Binary/image files are skipped.
TEXTY = {".md", ".json", ".sh", ".py", ".js", ".ts", ".yml", ".yaml", ".toml",
         ".txt", ".cfg", ".ini", ".env", ".example", ".tsx", ".jsx", ""}

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}

# --- patterns -----------------------------------------------------------
# (label, regex, replacement-used-by-scrub)
PATTERNS = [
    ("email",        re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"), "you@example.com"),
    ("phone",        re.compile(r"\+\d{1,3}[\s-]?\d{2,4}[\s-]?\d{3,4}[\s-]?\d{3,4}\b"), "+1 555 0100"),
    ("ipv4",         re.compile(r"\b(?!(?:0|10|127|172|192|255)\.)\d{1,3}(?:\.\d{1,3}){3}\b"), "203.0.113.10"),
    ("linux-home",   re.compile(r"/home/[A-Za-z0-9._-]+"), "$HOME"),
    ("macos-home",   re.compile(r"/Users/[A-Za-z0-9._-]+"), "$HOME"),
    ("data-mount",   re.compile(r"/mnt/[A-Za-z0-9._/-]*work"), "$PROJECT_ROOT"),
    ("owner-handle", re.compile(r"\bhaisem[\w-]*\b", re.I), "example-user"),
    ("org-name",     re.compile(r"\bmetaviz[\w-]*\b", re.I), "example-org"),
    ("token-shape",  re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|"
                                r"xox[baprs]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16})\b"), "REDACTED_TOKEN"),
    ("bearer",       re.compile(r"(?i)\b(?:bearer|api[_-]?key|secret|passwd|password)\s*[:=]\s*"
                                r"['\"]?[A-Za-z0-9._\-]{8,}"), "PASSWORD=REDACTED"),
    ("private-key",  re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "REDACTED_PRIVATE_KEY"),
]

# Client/person names carried over from the source machine. Substring match,
# case-insensitive, word-bounded.
NAMES = ["raoul", "wanyumba", "getapro", "handman", "sazoom", "deringocek",
         "awaisjamil", "fabio silva", "cyrus"]
NAME_RE = re.compile(r"\b(" + "|".join(re.escape(n) for n in NAMES) + r")\b", re.I)

# Paths never copied into examples/ under any circumstances. Matched against the
# path, so keep these specific: a hook named guard-secrets.sh is not a secret.
NEVER_COPY = re.compile(
    r"(projects-memory|\.local\.json$|mcp-servers\.json|"
    r"installed_plugins\.json|known_marketplaces\.json|\.credentials|"
    r"secrets\.tar|secrets-inventory|test_credentials|"
    r"/\.env$|/\.env\.|\.pem$|\.key$|\.p12$|id_rsa)", re.I)

# Lines that legitimately contain a pattern. Two sources: our own placeholders,
# and the documented no-reply address used in commit trailers.
# A line may also opt out explicitly with a `sanitize:allow` comment — used by
# linters that carry deliberately fake tokens as test vectors.
ALLOW_LINE = re.compile(r"(you@example\.com|example-user|example-org|"
                        r"203\.0\.113|\$HOME|\$PROJECT_ROOT|REDACTED|"
                        r"user@example|name@example|placeholder|"
                        r"noreply@anthropic\.com|sanitize:allow|"
                        r"AKIAIOSFODNN7EXAMPLE)", re.I)


def scan_text(text: str):
    """Yield (lineno, label, snippet) for every hit."""
    for i, line in enumerate(text.split("\n"), 1):
        if ALLOW_LINE.search(line):
            continue
        for label, rx, _ in PATTERNS:
            m = rx.search(line)
            if m:
                yield i, label, m.group(0)[:60]
        m = NAME_RE.search(line)
        if m:
            yield i, "client-name", m.group(0)


def is_texty(p: Path) -> bool:
    return p.suffix.lower() in TEXTY


def walk(root: Path):
    for p in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.is_file() and is_texty(p):
            yield p


def cmd_check(args) -> int:
    root = Path(args.path) if args.path else REPO / "examples"
    if not root.exists():
        print(f"nothing to check — {root} does not exist")
        return 0

    hits = 0
    blocked = 0
    for p in walk(root):
        try:
            rel = p.relative_to(REPO)
        except ValueError:
            rel = p  # scanning a path outside the repo (e.g. a candidate source)
        if NEVER_COPY.search(str(rel)):
            print(f"  BLOCKED  {rel}  (this file class must never be published)")
            blocked += 1
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for lineno, label, snip in scan_text(text):
            print(f"  {rel}:{lineno}  [{label}]  {snip}")
            hits += 1

    if hits or blocked:
        print(f"\nFAIL — {hits} redaction hit(s), {blocked} blocked file(s) under {root}",
              file=sys.stderr)
        print("Fix with: python3 scripts/sanitize.py --scrub <src> <dst>", file=sys.stderr)
        return 1
    print(f"OK — {root} is clean")
    return 0


def scrub_text(text: str) -> str:
    for _, rx, repl in PATTERNS:
        text = rx.sub(repl, text)
    text = NAME_RE.sub("acme", text)
    return text


def cmd_scrub(args) -> int:
    src, dst = Path(args.src), Path(args.dst)
    if not src.exists():
        print(f"error: {src} does not exist", file=sys.stderr)
        return 1

    copied = skipped = 0
    files = [src] if src.is_file() else list(walk(src))
    for p in files:
        rel = p.name if src.is_file() else p.relative_to(src)
        if NEVER_COPY.search(str(rel)) or NEVER_COPY.search(p.name):
            print(f"  skip   {rel}  (never-copy class)")
            skipped += 1
            continue
        target = dst if src.is_file() else dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        cleaned = scrub_text(text)
        target.write_text(cleaned, encoding="utf-8")
        if cleaned != text:
            print(f"  scrub  {rel}")
        else:
            print(f"  copy   {rel}")
        copied += 1
    print(f"\n{copied} copied, {skipped} skipped -> {dst}")
    print("Now run: python3 scripts/sanitize.py --check")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="scan and fail on any hit")
    ap.add_argument("--path", help="directory to scan (default: examples/)")
    ap.add_argument("--scrub", nargs=2, metavar=("SRC", "DST"),
                    help="copy SRC to DST, redacting as it goes")
    args = ap.parse_args()

    if args.scrub:
        args.src, args.dst = args.scrub
        return cmd_scrub(args)
    if args.check or args.path:
        return cmd_check(args)
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
