#!/usr/bin/env python3
"""One-shot repair: add `name` + `description` frontmatter to skills missing it.

30 SKILL.md files shipped with no YAML frontmatter at all, which means Claude
Code never discovers or triggers them — they were dead weight in the catalog.
Descriptions below were written from each file's actual content and follow the
repo's AUTHORING-STANDARD: state what the skill does, then when to invoke it.

Idempotent: a file that already has frontmatter is left untouched.

    python3 scripts/fix-skill-frontmatter.py [--dry-run]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SKILLS = Path(__file__).resolve().parent.parent / "skills"

DESCRIPTIONS = {
    "business-growth/contract-and-proposal-writer":
        "Generate freelance contracts, project proposals, SOWs, NDAs and MSAs as structured "
        "Markdown with jurisdiction-aware clauses for US, EU, UK and DACH. Use when drafting "
        "a client contract, writing a proposal or SOW, or reviewing standard commercial terms. "
        "Not a substitute for legal counsel.",

    "engineering/agent-designer":
        "Design and evaluate multi-agent systems: architecture patterns, agent role definition, "
        "tool design principles, communication strategies and evaluation frameworks. Use when "
        "architecting an agent system, defining agent roles and boundaries, or reviewing an "
        "existing multi-agent design.",

    "engineering/agent-workflow-designer":
        "Design production multi-agent orchestration using five core patterns: sequential "
        "pipeline, parallel fan-out/fan-in, hierarchical delegation, event-driven and consensus. "
        "Covers handoff protocols, state management, error recovery, context budgeting and cost. "
        "Use when choosing an orchestration pattern or debugging agent handoffs.",

    "engineering/api-design-reviewer":
        "Review REST API designs for convention compliance, breaking changes and overall design "
        "quality, producing a lint report and a scorecard. Use when reviewing an API spec or "
        "OpenAPI document, designing new endpoints, or checking whether a change is breaking.",

    "engineering/api-test-suite-builder":
        "Scan API routes across Next.js App Router, Express, FastAPI and Django REST, then "
        "generate test suites covering auth, validation, error codes, pagination, uploads and "
        "rate limiting. Outputs Vitest+Supertest or Pytest+httpx. Use when an API lacks tests "
        "or new endpoints need coverage.",

    "engineering/changelog-generator":
        "Produce auditable release notes from Conventional Commits, with separate commit "
        "parsing, semantic version bump logic and changelog rendering. Use when cutting a "
        "release, writing release notes, or deciding a semver bump.",

    "engineering/ci-cd-pipeline-builder":
        "Generate CI/CD pipelines from detected project stack signals, with repeatable checks "
        "and environment-aware deployment stages. Use when setting up CI for a project, adding "
        "a deployment stage, or migrating between CI providers.",

    "engineering/codebase-onboarding":
        "Analyze a codebase and generate onboarding documentation: architecture overview, key "
        "file map, local setup, common task runbooks, debugging guide and contribution "
        "guidelines. Use when joining an unfamiliar repo or writing onboarding docs for new "
        "contributors.",

    "engineering/database-designer":
        "Expert database design, analysis and optimization: schema design, index optimization "
        "and migration management for modern database systems. Use when designing a new schema, "
        "diagnosing slow queries, or planning a schema migration.",

    "engineering/database-schema-designer":
        "Turn requirements into a relational schema and generate migrations, TypeScript/Python "
        "types, seed data, RLS policies and indexes. Handles multi-tenancy, soft deletes, audit "
        "trails, versioning and polymorphic associations. Use when modeling a new feature's data.",

    "engineering/dependency-auditor":
        "Audit dependencies across multi-language projects for CVEs, license compliance, "
        "outdated packages and tree bloat, then plan safe upgrades. Use when reviewing supply "
        "chain risk, before a release, or when a vulnerability advisory lands.",

    "engineering/env-secrets-manager":
        "Manage the .env lifecycle across dev/staging/prod: auto-generate .env.example, validate "
        "required vars, detect secret leaks in git history and run credential rotation. "
        "Integrates Vault, AWS SSM, 1Password CLI and Doppler. Use when handling env config or "
        "after a suspected leak.",

    "engineering/git-worktree-manager":
        "Run parallel feature work with Git worktrees: branch isolation, port allocation, "
        "environment sync and cleanup, so each worktree runs as an independent local app. Use "
        "when working several branches at once or giving each agent session its own worktree.",

    "engineering/mcp-server-builder":
        "Design and ship production MCP servers from API contracts, treating OpenAPI as the "
        "source of truth. Covers scaffolding, schema quality, validation and safe evolution in "
        "Python and TypeScript. Use when building or reviewing an MCP server.",

    "engineering/migration-architect":
        "Plan, execute and validate complex system migrations with minimal downtime: strategy "
        "planning, compatibility analysis and rollback design. Use when moving between "
        "databases, infrastructure or major framework versions.",

    "engineering/monorepo-navigator":
        "Navigate and optimize monorepos across Turborepo, Nx, pnpm workspaces and Lerna: "
        "cross-package impact analysis, selective builds on affected packages, remote caching "
        "and dependency graph visualization. Use when working in a monorepo or migrating into one.",

    "engineering/observability-designer":
        "Design production observability across metrics, logs and traces, with SLI/SLO "
        "frameworks, golden signals, dashboard design and alert tuning. Use when instrumenting "
        "a service, defining SLOs, or reducing alert noise.",

    "engineering/performance-profiler":
        "Profile Node.js, Python and Go applications to find CPU, memory and I/O bottlenecks: "
        "flamegraphs, bundle analysis, query optimization, leak detection and k6/Artillery load "
        "tests. Always measures before and after. Use when something is slow and you need data.",

    "engineering/pr-review-expert":
        "Systematic review of GitHub PRs and GitLab MRs: blast radius analysis, security "
        "scanning, breaking change detection and test coverage delta, delivered as a prioritized "
        "report. Use when reviewing a pull request or assessing the risk of a change.",

    "engineering/rag-architect":
        "Design and optimize production RAG pipelines: chunking strategies, embedding model "
        "selection, vector database choice, retrieval strategies and evaluation frameworks. Use "
        "when building retrieval over documents or debugging poor answer quality.",

    "engineering/release-manager":
        "Manage releases end to end: parse conventional commits, generate changelogs, determine "
        "version bumps and orchestrate the release process. Use when preparing, cutting or "
        "automating a release.",

    "engineering/runbook-generator":
        "Generate operational runbooks from a codebase: detects CI/CD, database, hosting and "
        "container stack, then writes step-by-step procedures with commands, verification, "
        "rollback and escalation paths. Use when documenting deploys, incidents or on-call "
        "procedures.",

    "engineering/skill-tester":
        "Validate and score Claude Code skills: frontmatter and structure checks, script "
        "testing, multi-dimensional quality scoring and tier classification. Python stdlib only. "
        "Use when authoring a skill or auditing a skill library before publishing.",

    "engineering/tech-debt-tracker":
        "Identify, classify, prioritize and track technical debt across code, architecture, "
        "test and documentation dimensions. Use when planning refactor work, justifying a debt "
        "paydown, or assessing the cost of a shortcut.",

    "engineering-team/email-template-builder":
        "Build transactional email systems with React Email: templates, provider integration, "
        "preview server, i18n, dark mode, spam optimization and analytics. Targets Resend, "
        "Postmark, SendGrid and AWS SES. Use when adding or redesigning transactional email.",

    "engineering-team/incident-commander":
        "Run incident response from detection through resolution and postmortem: severity "
        "classification, timeline reconstruction and post-incident analysis. Use during a live "
        "incident or when writing a blameless postmortem.",

    "engineering-team/stripe-integration-expert":
        "Implement production Stripe integrations: subscriptions with trials and proration, "
        "one-time payments, usage-based billing, checkout sessions, idempotent webhook handlers, "
        "customer portal and invoicing, for Next.js, Express and Django. Use when adding or "
        "debugging billing.",

    "product/competitive-teardown":
        "Run a structured competitive analysis from pricing pages, app store reviews, job "
        "postings, SEO and social signals, producing feature matrices, SWOT, positioning maps "
        "and a UX audit. Use when sizing up a competitor or preparing a positioning review.",

    "product/landing-page-generator":
        "Generate high-converting landing pages from a product description: Next.js/React "
        "components with section variants, proven copy frameworks, SEO meta and performance-first "
        "patterns. Use when building a landing or marketing page that needs real copy, not "
        "placeholder text.",

    "product/saas-scaffolder":
        "Scaffold a production-ready SaaS from a product brief: Next.js App Router with "
        "TypeScript, Tailwind and shadcn/ui, wired to auth, database, payments and a working "
        "dashboard. Use when starting a new SaaS project rather than assembling a starter kit "
        "by hand.",
}


def add_frontmatter(rel: str, desc: str, dry: bool) -> str:
    path = SKILLS / rel / "SKILL.md"
    if not path.is_file():
        return f"MISSING  {rel}"
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        return f"skip     {rel} (already has frontmatter)"
    name = rel.split("/")[-1]
    block = f"---\nname: {name}\ndescription: {desc}\n---\n\n"
    if not dry:
        path.write_text(block + text.lstrip("\n"), encoding="utf-8")
    return f"fixed    {rel}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    results = [add_frontmatter(rel, d, args.dry_run) for rel, d in sorted(DESCRIPTIONS.items())]
    for r in results:
        print(r)
    fixed = sum(1 for r in results if r.startswith("fixed"))
    missing = [r for r in results if r.startswith("MISSING")]
    print(f"\n{fixed} fixed, {len(results) - fixed - len(missing)} skipped, {len(missing)} missing")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
