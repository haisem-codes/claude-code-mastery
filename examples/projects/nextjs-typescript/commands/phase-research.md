---
name: phase-research
description: Gather reusable reference material for a phase before planning it — syncs the pinned research repos, mines them for the phase's concepts, and writes a reuse report. Runs after /phase-review picks the next phase.
argument-hint: <phase-number>
---

# /phase-research <phase-number>

Runs once the next phase is chosen (by /phase-review), before /tour-loop plans it. Read-only on
product code; sources are proposed, the user approves before anything new is cloned.

1. Read research/sources.json + research/README.md. List the sources tagged for `<phase-number>`
   and show the user which are `pinned` vs proposed `candidate`s.
2. If candidates exist (or the user names new ones), present them for approval. Only after approval,
   set them `pinned`. Never clone an unapproved source.
3. Dispatch the research-scout: `make research-sync PHASE=<phase-number>` then survey each synced
   source per its `mine` list. For many sources, run scouts in parallel (one per source) and merge.
4. Produce research/reports/phase-<phase-number>-reuse.md: per concept -> vendor file:line -> the
   backlog task it helps -> `adapt` (permissive/vendorable) or `read-only` (re-implement). Enforce
   the licensing policy (research/README.md, rules/security.md Third-party reuse).
5. Hand the report to planner so PLAN for this phase starts with the reuse material in hand.
   Note any concept for which no good reference exists (author from scratch).
