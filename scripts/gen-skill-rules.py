#!/usr/bin/env python3
"""Generate hooks/user-prompt-submit/skill-rules.json from catalog.json.

The shipped rules file described an unrelated React Native project and pointed at
skills that do not exist here, so the skill-eval hook suggested nothing useful.
This derives the rules from the actual catalog: keywords come from each skill's
name and description, so the file cannot drift from the skills on disk.

    python3 scripts/gen-skill-rules.py            # write the file
    python3 scripts/gen-skill-rules.py --check    # fail if stale

Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CATALOG = REPO / "catalog.json"
OUT = REPO / "hooks" / "user-prompt-submit" / "skill-rules.json"

# Words too generic to discriminate between 168 skills.
STOP = {
    "use", "when", "the", "and", "for", "with", "that", "this", "from", "into",
    "your", "you", "a", "an", "of", "to", "in", "on", "or", "it", "is", "are",
    "be", "as", "by", "at", "not", "but", "can", "will", "each", "then", "than",
    "skill", "skills", "using", "used", "uses", "make", "makes", "run", "runs",
    "new", "one", "two", "all", "any", "its", "their", "them", "they", "how",
    "what", "which", "who", "why", "where", "more", "most", "some", "such",
    "before", "after", "over", "under", "across", "per", "via", "plus", "also",
    "need", "needs", "want", "wants", "get", "gets", "set", "sets", "add",
    "adds", "including", "includes", "include", "covers", "cover", "produce",
    "produces", "generate", "generates", "generated", "output", "outputs",
    "based", "well", "good", "best", "real", "full", "complete", "production",
    "ready", "team", "teams", "work", "works", "working", "code", "project",
    "projects", "file", "files", "data", "time", "help", "helps", "review",
    "reviews", "write", "writes", "writing", "create", "creates", "creating",
    "build", "builds", "building", "design", "designs", "designing", "manage",
    "manages", "managing", "handle", "handles", "analysis", "analyze", "across",
}

# Directory hints -> skill leaf names, for path-based scoring.
DIR_HINTS = {
    "migrations": ["database-schema-designer", "migration-architect"],
    "tests": ["api-test-suite-builder", "tdd-guide"],
    "test": ["api-test-suite-builder", "tdd-guide"],
    ".github/workflows": ["ci-cd-pipeline-builder", "release-manager"],
    "terraform": ["runbook-generator", "observability-designer"],
    "k8s": ["runbook-generator", "observability-designer"],
    "docs": ["codebase-onboarding", "runbook-generator"],
}


def tokens(text: str) -> list:
    words = re.findall(r"[a-z][a-z0-9+.#-]{2,}", text.lower())
    seen, out = set(), []
    for w in words:
        w = w.strip(".-")
        if len(w) < 3 or w in STOP or w in seen:
            continue
        seen.add(w)
        out.append(w)
    return out


def build() -> dict:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    skills = {}

    for s in catalog["skills"]:
        if s["kind"] != "unit" or not s["valid"]:
            continue
        leaf = s["id"].split("/")[-1]

        # Name words are the strongest signal; description words fill in.
        name_words = [w for w in leaf.split("-") if len(w) > 2 and w not in STOP]
        desc_words = tokens(s["description"])[:12]

        keywords = list(dict.fromkeys(name_words + desc_words))[:14]
        if not keywords:
            continue

        entry = {
            "description": s["description"][:160],
            "priority": 8 if s["domain"] in ("engineering", "engineering-team", "reference") else 5,
            "domain": s["domain"],
            "triggers": {
                "keywords": keywords,
                # the full hyphenated name, and the spaced form
                "keywordPatterns": [
                    r"\b" + re.escape(leaf) + r"\b",
                    r"\b" + re.escape(leaf.replace("-", r" ")) + r"\b",
                ],
                "intentPatterns": [
                    r"(?:create|add|write|build|design|review|audit|fix|debug|generate)"
                    r".*\b(?:" + "|".join(re.escape(w) for w in name_words[:3]) + r")\b"
                ] if name_words else [],
            },
        }
        skills[leaf] = entry

    dir_map = {}
    known = set(skills)
    for d, names in DIR_HINTS.items():
        present = [n for n in names if n in known]
        if present:
            dir_map[d] = present

    return {
        "_generated_by": "scripts/gen-skill-rules.py — do not edit by hand",
        "_source_commit": catalog.get("generated_from", "unknown"),
        "version": "2.0",
        "config": {
            "minConfidenceScore": 4,
            "showMatchReasons": True,
            "maxSkillsToShow": 4,
        },
        "scoring": {
            "keyword": 2,
            "keywordPattern": 3,
            "pathPattern": 4,
            "directoryMatch": 5,
            "intentPattern": 4,
            "contentPattern": 3,
            "contextPattern": 2,
        },
        "directoryMappings": dir_map,
        "skills": skills,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if not CATALOG.is_file():
        print("catalog.json missing — run scripts/catalog.py first", file=sys.stderr)
        return 1

    rules = build()
    text = json.dumps(rules, indent=2) + "\n"

    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.is_file() else ""
        if current != text:
            print("skill-rules.json is stale — run python3 scripts/gen-skill-rules.py",
                  file=sys.stderr)
            return 1
        print(f"OK — skill-rules.json current ({len(rules['skills'])} skills)")
        return 0

    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}  ({len(rules['skills'])} skills, "
          f"{len(rules['directoryMappings'])} directory mappings)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
