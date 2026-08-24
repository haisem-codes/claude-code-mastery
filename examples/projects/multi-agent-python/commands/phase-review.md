---
name: phase-review
description: At a phase boundary, dispatch the phase-strategist to propose the next phase's scope from complete internal context + deep external research (OSS teardowns, recent papers, competitor + market analysis) with a novel, sellable, differentiated angle. Runs only when a phase is complete.
argument-hint: "[phase just completed, e.g. 3] [optional focus, e.g. 'lean toward auto-fix']"
---

# /phase-review $ARGUMENTS

Invoke this **only at a phase boundary** — when the just-finished phase's loops are all done and its
**results are in** (e.g. the benchmark numbers exist). Not mid-phase; the strategist needs the measured outcome.

You are the delivery-orchestrator. Do this:

1. **Confirm the phase is actually complete** — its loops closed, gates green, and any results doc
   (`docs/architecture/benchmark-*-results.md`, etc.) written. If not, say so and stop; there's nothing to
   review yet.
2. **Dispatch `phase-strategist`** (Fable) with: which phase just finished, the measured results, and any
   focus the user gave in `$ARGUMENTS`. It runs read-only + web research and writes
   `docs/strategy/phase-<N+1>-proposal.md` — the assessment, the researched competitive/academic landscape,
   **1–2 novel differentiated approaches done right (quality over quantity)** balanced with **proven,
   still-missing coverage / language support**, and a recommended next-phase scope (measurable milestone +
   ordered candidate loops labelled novel vs. proven-coverage) with alternatives + risks + kill-criteria.
3. **Synthesize for the user** — the strategist returns raw analysis; you present its top recommendation, the
   key trade-offs, and the one decision the user must make. **The user picks the phase.**
4. **On the user's pick** → hand the chosen direction to `product-strategist` (requirements) then `planner`
   (ordered loops with acceptance criteria), exactly as any new phase is planned. Then normal `/aegis-loop`s resume.

This is advisory + generative, not a gate: it never blocks shipping. It exists so each new phase is chosen
from evidence and aimed at making Aegis the best, actually-sellable tool in its niche — not picked ad hoc.
