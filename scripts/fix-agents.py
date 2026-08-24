#!/usr/bin/env python3
"""One-shot repair for agent frontmatter: dedupe `tools:` lists in place.

Filename/name mismatches are fixed separately with `git mv` so history follows
the rename. Idempotent: running twice is a no-op.
"""
from __future__ import annotations

import sys
from pathlib import Path

AGENTS = Path(__file__).resolve().parent.parent / "agents"


def dedupe_tools(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    changed = False
    for i, line in enumerate(lines[:40]):
        if not line.startswith("tools:"):
            continue
        raw = line[len("tools:"):].strip()
        items = [t.strip() for t in raw.split(",") if t.strip()]
        seen, out = set(), []
        for t in items:
            if t not in seen:
                seen.add(t)
                out.append(t)
        if out != items:
            lines[i] = "tools: " + ", ".join(out)
            changed = True
        break
    if changed:
        path.write_text("\n".join(lines), encoding="utf-8")
    return changed


def main() -> int:
    fixed = []
    for md in sorted(AGENTS.rglob("*.md")):
        if dedupe_tools(md):
            fixed.append(md.name)
    if fixed:
        print(f"deduped tools in {len(fixed)} agent(s): {', '.join(fixed)}")
    else:
        print("no duplicate tools found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
