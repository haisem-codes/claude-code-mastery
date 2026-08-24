#!/usr/bin/env python3
"""Build catalog.json — the single source of truth for what this repo ships.

Walks skills/, agents/, hooks/ and examples/, parses frontmatter, and emits a
machine-readable catalog the installer and the docs both read from. Also doubles
as the validator: --check exits non-zero if anything is malformed.

Stdlib only, Python 3.9+. No dependencies, so a fresh clone can run it.

    python3 scripts/catalog.py            # write catalog.json
    python3 scripts/catalog.py --check    # validate only, exit 1 on problems
    python3 scripts/catalog.py --counts   # print counts for the docs
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Files that live beside skills but are not skills. A glob-based installer would
# otherwise copy these into ~/.claude/skills/.
DOMAIN_CRUFT = {
    "README.md", "CLAUDE.md", "LICENSE", "CONTRIBUTING.md",
    "AUTHORING-STANDARD.md", "INSTALLATION_GUIDE.txt", "START_HERE.md",
    "TEAM_STRUCTURE_GUIDE.md", "IMPLEMENTATION_SUMMARY.md",
    "REAL_WORLD_SCENARIO.md",
}

KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")


def parse_frontmatter(text: str) -> dict:
    """Minimal YAML-frontmatter reader: top-level scalar keys only.

    Enough to validate name/description/tools/model. Nested blocks (metadata:)
    are recorded as present-but-unparsed rather than crashing the walk.
    """
    if not text.startswith("---"):
        return {}
    lines = text.split("\n")
    if lines[0].strip() != "---":
        return {}
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}  # unterminated block

    out: dict = {}
    key = None
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[:1] in (" ", "\t"):
            # continuation of a folded scalar or a nested mapping
            if key and isinstance(out.get(key), str):
                out[key] = (out[key] + " " + raw.strip()).strip()
            continue
        m = KEY_RE.match(raw)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val in (">", "|", ">-", "|-"):
            val = ""  # folded scalar; continuation lines append below
        elif len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        out[key] = val
    return out


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def dir_size(path: Path) -> int:
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())


def detect_deps(skill_dir: Path) -> list:
    """What a skill needs at runtime beyond Claude Code itself."""
    deps = set()
    if (skill_dir / "scripts").is_dir():
        if any((skill_dir / "scripts").rglob("*.py")):
            deps.add("python3")
        if any((skill_dir / "scripts").rglob("*.sh")):
            deps.add("bash")
    if any(skill_dir.rglob("requirements.txt")):
        deps.add("pip")
    if any(skill_dir.rglob("package.json")):
        deps.add("node")
    return sorted(deps)


def collect_skills() -> list:
    root = REPO / "skills"
    units = []
    if not root.is_dir():
        return units
    for sk in sorted(root.rglob("SKILL.md")):
        rel = sk.relative_to(root)
        parts = rel.parts
        depth = len(parts)
        if depth == 2:
            kind = "domain"          # skills/<domain>/SKILL.md
        elif depth == 3:
            kind = "unit"            # skills/<domain>/<skill>/SKILL.md  <- installable
        else:
            kind = "nested"          # bundled sub-skill, installs with its parent
        fm = parse_frontmatter(read(sk))
        d = sk.parent
        units.append({
            "id": "/".join(parts[:-1]),
            "type": "skill",
            "kind": kind,
            "domain": parts[0],
            "dir": str(d.relative_to(REPO)),
            "name": fm.get("name", ""),
            "description": fm.get("description", ""),
            "user_invocable": fm.get("user-invocable", ""),
            "license": fm.get("license", ""),
            "deps": detect_deps(d),
            "bytes": dir_size(d),
            "valid": bool(fm.get("name") and fm.get("description")),
        })
    return units


def collect_agents() -> list:
    root = REPO / "agents"
    out = []
    if not root.is_dir():
        return out
    for md in sorted(root.rglob("*.md")):
        if md.name in DOMAIN_CRUFT:
            continue
        fm = parse_frontmatter(read(md))
        if not fm.get("name"):
            continue  # prose doc, not an agent
        tools = [t.strip() for t in fm.get("tools", "").split(",") if t.strip()]
        rel = md.relative_to(root)
        out.append({
            "id": fm["name"],
            "type": "agent",
            "category": rel.parts[0] if len(rel.parts) > 1 else "general",
            "file": str(md.relative_to(REPO)),
            "name": fm["name"],
            "description": fm.get("description", ""),
            "model": fm.get("model", ""),
            "tools": tools,
            "mcp_tools": sorted({t for t in tools if t.startswith("mcp__")}),
            "filename_matches_name": md.stem == fm["name"],
            "duplicate_tools": len(tools) != len(set(tools)),
            "valid": bool(fm.get("name") and fm.get("description")),
        })
    return out


def collect_hooks() -> list:
    root = REPO / "hooks"
    out = []
    if not root.is_dir():
        return out
    for sh in sorted(root.rglob("*.sh")):
        body = read(sh)
        out.append({
            "id": sh.stem,
            "type": "hook",
            "event": sh.parent.name,
            "file": str(sh.relative_to(REPO)),
            "reads_stdin": "tool_input" in body,
            "uses_legacy_tool_input_env": "$TOOL_INPUT" in body,
            "needs_jq": "jq" in body,
            "executable": sh.stat().st_mode & 0o111 != 0,
        })
    return out


def collect_examples() -> list:
    root = REPO / "examples"
    out = []
    if not root.is_dir():
        return out
    for readme in sorted(root.glob("*/README.md")):
        d = readme.parent
        out.append({
            "id": d.name,
            "type": "example",
            "dir": str(d.relative_to(REPO)),
            "bytes": dir_size(d),
        })
    return out


def build() -> dict:
    skills = collect_skills()
    agents = collect_agents()
    hooks = collect_hooks()
    examples = collect_examples()
    installable = [s for s in skills if s["kind"] == "unit"]
    domains: dict = {}
    for s in installable:
        domains.setdefault(s["domain"], 0)
        domains[s["domain"]] += 1
    # Deliberately no git SHA here. catalog.json describes the *content* of the
    # repo, and CI asserts it is not stale by regenerating and diffing. Embedding
    # HEAD would make the file differ immediately after every commit, so the
    # staleness check could never pass. The installer records the commit at
    # install time instead, which is when provenance actually matters.
    return {
        "counts": {
            "skills_installable": len(installable),
            "skills_nested": len([s for s in skills if s["kind"] == "nested"]),
            "skills_domain_level": len([s for s in skills if s["kind"] == "domain"]),
            "skills_invalid": len([s for s in installable if not s["valid"]]),
            "agents": len(agents),
            "hooks": len(hooks),
            "examples": len(examples),
        },
        "domains": dict(sorted(domains.items(), key=lambda kv: -kv[1])),
        "skills": skills,
        "agents": agents,
        "hooks": hooks,
        "examples": examples,
    }


def check(cat: dict) -> int:
    problems = []
    warnings = []
    for s in cat["skills"]:
        if s["kind"] == "unit" and not s["valid"]:
            missing = []
            if not s["name"]:
                missing.append("name")
            if not s["description"]:
                missing.append("description")
            problems.append(f"skill  {s['id']}: missing frontmatter {'+'.join(missing)}")
    # Name collisions are expected across domains and are resolved at install
    # time by prefixing, so they are reported but do not fail the check.
    seen: dict = {}
    for s in cat["skills"]:
        if s["kind"] != "unit":
            continue
        leaf = s["id"].split("/")[-1]
        seen.setdefault(leaf, []).append(s["id"])
    for leaf, ids in sorted(seen.items()):
        if len(ids) > 1:
            warnings.append(f"collide  '{leaf}' from {len(ids)} domains: {', '.join(ids)} "
                            f"(installer prefixes on collision)")
    for a in cat["agents"]:
        if not a["valid"]:
            problems.append(f"agent  {a['id']}: missing name/description")
        if not a["filename_matches_name"]:
            problems.append(f"agent  {a['file']}: frontmatter name '{a['name']}' != filename")
        if a["duplicate_tools"]:
            problems.append(f"agent  {a['id']}: duplicate entries in tools list")
    for h in cat["hooks"]:
        if h["uses_legacy_tool_input_env"]:
            problems.append(f"hook   {h['file']}: reads $TOOL_INPUT; payload arrives on stdin")

    for w in warnings:
        print(f"  warn  {w}")

    if problems:
        print(f"\nFAIL — {len(problems)} problem(s):\n", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 1
    print(f"OK — catalog is clean ({len(warnings)} warning(s))")
    return 0


def check_docs(cat: dict) -> int:
    """Verify the counts printed in README.md match the catalog.

    The README claims its numbers cannot drift; this is what makes that true.
    """
    readme = REPO / "README.md"
    if not readme.is_file():
        print("README.md missing", file=sys.stderr)
        return 1
    text = readme.read_text(encoding="utf-8")

    label_to_domain = {
        "C-Level Advisory": "c-level-advisor", "Engineering": "engineering",
        "Engineering Team": "engineering-team", "Marketing": "marketing",
        "Product": "product", "Project Management": "project-management",
        "Compliance": "compliance", "Business Growth": "business-growth",
        "Finance": "finance", "Anthropic Official": "anthropic-official",
        "Reference": "reference",
    }
    bad = []
    for label, domain in label_to_domain.items():
        want = cat["domains"].get(domain, 0)
        m = re.search(rf"<b>{re.escape(label)} — (\d+) skills?</b>", text)
        if not m:
            bad.append(f"README: no count header for '{label}'")
        elif int(m.group(1)) != want:
            bad.append(f"README: '{label}' says {m.group(1)}, catalog says {want}")

    c = cat["counts"]
    for claim, want in ((r"(\d+) installable skills", c["skills_installable"]),
                        (r"\*\*(\d+) subagents\*\*", c["agents"]),
                        (r"\*\*(\d+) hook scripts\*\*", c["hooks"])):
        m = re.search(claim, text)
        if m and int(m.group(1)) != want:
            bad.append(f"README: '{m.group(0)}' should be {want}")

    if bad:
        print(f"FAIL — {len(bad)} doc count mismatch(es):\n", file=sys.stderr)
        for b in bad:
            print(f"  {b}", file=sys.stderr)
        return 1
    print("OK — README counts match the catalog")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="validate, do not write")
    ap.add_argument("--check-docs", action="store_true",
                    help="verify README counts match the catalog")
    ap.add_argument("--counts", action="store_true", help="print counts and exit")
    args = ap.parse_args()

    cat = build()

    if args.check_docs:
        return check_docs(cat)
    if args.counts:
        print(json.dumps({"counts": cat["counts"], "domains": cat["domains"]}, indent=2))
        return 0
    if args.check:
        return check(cat)

    out = REPO / "catalog.json"
    out.write_text(json.dumps(cat, indent=2) + "\n", encoding="utf-8")
    c = cat["counts"]
    print(f"wrote {out.relative_to(REPO)}")
    print(f"  {c['skills_installable']} installable skills "
          f"({c['skills_invalid']} invalid), {c['skills_nested']} nested")
    print(f"  {c['agents']} agents, {c['hooks']} hooks, {c['examples']} examples")
    return 0


if __name__ == "__main__":
    sys.exit(main())
