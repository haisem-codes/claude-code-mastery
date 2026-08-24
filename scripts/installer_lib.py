#!/usr/bin/env python3
"""Install engine for claude-code-mastery.

install.sh handles CLI ergonomics and backups; this does the work that has to be
exact: settings.json merging, name-collision resolution, checksum tracking and
the manifest that makes re-runs and uninstall safe.

Design rules:
  - Never replace settings.json. Merge into it, preserving unknown keys.
  - Never overwrite a file the user edited after install, unless --force.
  - Record a checksum per installed file so "unchanged", "updated by us" and
    "modified by the user" are distinguishable on the next run.

Stdlib only, Python 3.8+.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

MANIFEST_NAME = ".mastery-manifest.json"


def repo_commit(repo: Path) -> str:
    """The commit installed from. Recorded here rather than in catalog.json,
    which must stay byte-stable across commits for CI's staleness check."""
    try:
        return subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, OSError):
        return "unknown"


# ----------------------------------------------------------------- helpers
def load_json(p: Path, default):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def sha(path: Path) -> str:
    h = hashlib.sha256()
    if path.is_dir():
        for f in sorted(path.rglob("*")):
            if f.is_file():
                h.update(str(f.relative_to(path)).encode())
                h.update(f.read_bytes())
    elif path.is_file():
        h.update(path.read_bytes())
    return h.hexdigest()[:16]


class Reporter:
    def __init__(self) -> None:
        self.counts = {"new": 0, "updated": 0, "unchanged": 0, "skipped": 0, "removed": 0}

    def line(self, kind: str, what: str, note: str = "") -> None:
        mark = {"new": "+", "updated": "~", "unchanged": "=", "skipped": "!", "removed": "-"}[kind]
        self.counts[kind] += 1
        if kind == "unchanged":
            return  # keep output readable; summarised at the end
        suffix = f"  ({note})" if note else ""
        print(f"  {mark} {what}{suffix}")

    def summary(self) -> None:
        c = self.counts
        parts = [f"{c['new']} new", f"{c['updated']} updated", f"{c['unchanged']} unchanged"]
        if c["skipped"]:
            parts.append(f"{c['skipped']} skipped")
        if c["removed"]:
            parts.append(f"{c['removed']} removed")
        print("\n  " + ", ".join(parts))


# ----------------------------------------------------------------- selection
def resolve_selection(repo: Path, args) -> dict:
    catalog = load_json(repo / "catalog.json", {})
    presets = load_json(repo / "presets.json", {})

    skills: list = []
    agents: list = []
    hooks: list = []

    if args.preset:
        p = presets.get(args.preset)
        if not p:
            names = [k for k in presets if not k.startswith("_")]
            raise SystemExit(f"error: unknown preset '{args.preset}'. Available: {', '.join(names)}")
        skills += p.get("skills", [])
        agents += p.get("agents", [])
        hooks += p.get("hooks", [])

    def split(s):
        return [x.strip() for x in (s or "").split(",") if x.strip()]

    skills += split(args.skills)
    agents += split(args.agents)
    hooks += split(args.hooks)

    # de-dupe, order-preserving
    skills = list(dict.fromkeys(skills))
    agents = list(dict.fromkeys(agents))
    hooks = list(dict.fromkeys(hooks))

    known_skills = {s["id"]: s for s in catalog.get("skills", []) if s["kind"] == "unit"}
    known_agents = {a["name"]: a for a in catalog.get("agents", [])}
    known_hooks = {h["file"].replace("hooks/", "").replace(".sh", ""): h
                   for h in catalog.get("hooks", [])}

    unknown = ([f"skill '{s}'" for s in skills if s not in known_skills]
               + [f"agent '{a}'" for a in agents if a not in known_agents]
               + [f"hook '{h}'" for h in hooks if h not in known_hooks])
    if unknown:
        raise SystemExit("error: not in catalog:\n  " + "\n  ".join(unknown))

    return {
        "skills": [known_skills[s] for s in skills],
        "agents": [known_agents[a] for a in agents],
        "hooks": [known_hooks[h] for h in hooks],
    }


# ----------------------------------------------------------------- settings merge
def merge_settings(existing: dict, template: dict, hook_entries: list) -> tuple:
    """Union template into existing without clobbering user keys.

    Returns (merged, list-of-change-descriptions).
    """
    out = json.loads(json.dumps(existing))  # deep copy
    changes = []

    if "$schema" not in out and "$schema" in template:
        out["$schema"] = template["$schema"]
        changes.append("added $schema")

    # permissions: union the lists, preserve order, never drop user entries
    tperm = template.get("permissions", {})
    if tperm:
        perms = out.setdefault("permissions", {})
        for key in ("deny", "allow", "ask"):
            incoming = tperm.get(key, [])
            if not incoming:
                continue
            current = perms.setdefault(key, [])
            added = [r for r in incoming if r not in current]
            if added:
                current.extend(added)
                changes.append(f"permissions.{key}: +{len(added)}")

    # env: only fill gaps, never override an existing value
    tenv = template.get("env", {})
    if tenv:
        env = out.setdefault("env", {})
        for k, v in tenv.items():
            if k not in env:
                env[k] = v
                changes.append(f"env.{k}")

    # hooks: append by (event, matcher, command), dedup exactly
    if hook_entries:
        hooks = out.setdefault("hooks", {})
        for event, matcher, command in hook_entries:
            bucket = hooks.setdefault(event, [])
            target = None
            for group in bucket:
                if group.get("matcher") == matcher:
                    target = group
                    break
            if target is None:
                target = {"matcher": matcher, "hooks": []}
                bucket.append(target)
            cmds = [h.get("command") for h in target.get("hooks", [])]
            if command not in cmds:
                target.setdefault("hooks", []).append(
                    {"type": "command", "command": command, "timeout": 5}
                )
                changes.append(f"hooks.{event}[{matcher}]")
    return out, changes


# ----------------------------------------------------------------- copy
def install_path(src: Path, dst: Path, manifest: dict, key: str,
                 rep: Reporter, dry: bool, force: bool) -> None:
    new_sum = sha(src)
    prev = manifest.get("items", {}).get(key)

    if dst.exists():
        cur_sum = sha(dst)
        if prev and cur_sum != prev.get("sha") and not force:
            rep.line("skipped", key, "locally modified — use --force to overwrite")
            return
        if cur_sum == new_sum:
            rep.line("unchanged", key)
            manifest.setdefault("items", {})[key] = {"sha": new_sum, "path": str(dst)}
            return
        if not prev and not force:
            rep.line("skipped", key, "exists and was not installed by us — use --force")
            return
        kind = "updated"
    else:
        kind = "new"

    if not dry:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            if dst.is_dir():
                shutil.rmtree(dst)
            else:
                dst.unlink()
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    rep.line(kind, key)
    manifest.setdefault("items", {})[key] = {"sha": new_sum, "path": str(dst)}


# ----------------------------------------------------------------- commands
def cmd_list_presets(args) -> int:
    repo = Path(args.repo)
    presets = load_json(repo / "presets.json", {})
    catalog = load_json(repo / "catalog.json", {})
    counts = catalog.get("counts", {})
    for name, p in presets.items():
        if name.startswith("_"):
            continue
        print(f"  {name:16s} {p.get('label','')}")
        print(f"  {'':16s} {p.get('description','')}")
        print(f"  {'':16s} {len(p.get('skills',[]))} skills, "
              f"{len(p.get('agents',[]))} agents, {len(p.get('hooks',[]))} hooks")
        print()
    if counts:
        print(f"  Catalog: {counts.get('skills_installable',0)} skills, "
              f"{counts.get('agents',0)} agents, {counts.get('hooks',0)} hooks available.")
        print("  Pick individually with --skills a,b --agents c")
    return 0


def cmd_install(args) -> int:
    repo = Path(args.repo)
    cfg = Path(args.config_dir).expanduser()
    dry, force = args.dry_run, args.force

    sel = resolve_selection(repo, args)
    manifest = load_json(cfg / MANIFEST_NAME, {"version": 1, "items": {}})
    manifest["source"] = str(repo)
    manifest["source_commit"] = repo_commit(repo)

    rep = Reporter()

    # --- skills ------------------------------------------------------
    if sel["skills"]:
        print(f"\n\033[1mSkills\033[0m ({len(sel['skills'])})")
        # flat namespace: detect collisions and prefix with the domain
        leaf_counts: dict = {}
        for s in sel["skills"]:
            leaf = s["id"].split("/")[-1]
            leaf_counts[leaf] = leaf_counts.get(leaf, 0) + 1
        for s in sel["skills"]:
            leaf = s["id"].split("/")[-1]
            target = leaf if leaf_counts[leaf] == 1 else f"{s['domain']}-{leaf}"
            install_path(repo / s["dir"], cfg / "skills" / target,
                         manifest, f"skills/{target}", rep, dry, force)

    # --- agents ------------------------------------------------------
    if sel["agents"]:
        print(f"\n\033[1mAgents\033[0m ({len(sel['agents'])})")
        for a in sel["agents"]:
            install_path(repo / a["file"], cfg / "agents" / f"{a['name']}.md",
                         manifest, f"agents/{a['name']}.md", rep, dry, force)

    # --- hooks -------------------------------------------------------
    hook_entries = []
    if sel["hooks"]:
        print(f"\n\033[1mHooks\033[0m ({len(sel['hooks'])})")
        event_map = {
            "pre-tool-use": "PreToolUse",
            "post-tool-use": "PostToolUse",
            "user-prompt-submit": "UserPromptSubmit",
        }
        matcher_for = {
            "block-main-branch": "Edit|MultiEdit|Write",
            "block-dangerous-commands": "Bash",
            "block-secret-reads": "Bash|Read",
            "enforce-package-manager": "Bash",
            "auto-format": "Edit|MultiEdit|Write",
            "auto-lint": "Edit|MultiEdit|Write",
            "auto-test": "Edit|MultiEdit|Write",
            "skill-eval": "*",
        }
        for h in sel["hooks"]:
            src = repo / h["file"]
            name = src.stem
            dst = cfg / "hooks" / src.name
            install_path(src, dst, manifest, f"hooks/{src.name}", rep, dry, force)
            event = event_map.get(h["event"], "PreToolUse")
            hook_entries.append((event, matcher_for.get(name, "*"), f'bash "{dst}"'))

    # --- settings ----------------------------------------------------
    settings_path = cfg / "settings.json"
    template = load_json(repo / "templates" / "global" / "settings.json", {})
    existing = load_json(settings_path, {})
    merged, changes = merge_settings(existing, template, hook_entries)

    print("\n\033[1mSettings\033[0m")
    if changes:
        for c in changes:
            print(f"  ~ settings.json: {c}")
        if not dry:
            settings_path.parent.mkdir(parents=True, exist_ok=True)
            settings_path.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    else:
        print("  = settings.json already up to date")

    if existing and not dry:
        # prove we did not drop anything the user had
        lost = [k for k in existing if k not in merged]
        if lost:
            print(f"  \033[31m! keys would be lost: {lost} — aborting\033[0m", file=sys.stderr)
            return 1

    rep.summary()

    if not dry:
        cfg.mkdir(parents=True, exist_ok=True)
        (cfg / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"  manifest: {cfg / MANIFEST_NAME}")
    return 0


def cmd_uninstall(args) -> int:
    cfg = Path(args.config_dir).expanduser()
    manifest = load_json(cfg / MANIFEST_NAME, None)
    if manifest is None:
        print("no manifest — nothing to uninstall", file=sys.stderr)
        return 1
    rep = Reporter()
    kept = {}
    for key, meta in sorted(manifest.get("items", {}).items()):
        p = Path(meta["path"])
        if not p.exists():
            continue
        if sha(p) != meta.get("sha") and not args.force:
            rep.line("skipped", key, "locally modified — use --force to remove")
            kept[key] = meta
            continue
        if not args.dry_run:
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
        rep.line("removed", key)
    rep.summary()
    if not args.dry_run:
        if kept:
            manifest["items"] = kept
            (cfg / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        else:
            (cfg / MANIFEST_NAME).unlink(missing_ok=True)
        print("\n  settings.json was left untouched — remove hook entries by hand if you want them gone.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list-presets")
    p.add_argument("--repo", required=True)
    p.set_defaults(fn=cmd_list_presets)

    p = sub.add_parser("install")
    p.add_argument("--repo", required=True)
    p.add_argument("--config-dir", required=True)
    p.add_argument("--preset", default="")
    p.add_argument("--skills", default="")
    p.add_argument("--agents", default="")
    p.add_argument("--hooks", default="")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_install)

    p = sub.add_parser("uninstall")
    p.add_argument("--repo", required=True)
    p.add_argument("--config-dir", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_uninstall)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
