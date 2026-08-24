---
name: phase-review
description: Phase-boundary retrospective and next-phase proposal — read-only research, proposals not decisions. User-invoked only.
argument-hint: (none)
---

# /phase-review

Run at phase boundaries only (user-invoked). Read-only research; proposals, not decisions.
1. Read backlog/ROADMAP.md, all lessons.md entries this phase, video-judge score history if any.
2. Research externally (WebSearch): competitor moves, new Remotion/stock-API/TTS capabilities.
3. Evaluate the config itself: agent roster gaps/overlaps, skill staleness, hook friction,
   model-routing spend vs value (docs/process/model-routing.md).
4. Write docs/strategy/phase-N-review.md: findings, 2-3 options for next phase, recommendation,
   config-evolution proposal (roster/skills/MCP changes).
5. Present to user. Apply nothing until approved. After approval: prune lessons.md, update ROADMAP.
6. Once the user picks the next phase, run `/phase-research <that-phase>` to sync and mine the
   reference repos for it, so planning starts with a reuse report in hand.
