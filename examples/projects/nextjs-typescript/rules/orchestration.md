# Orchestration Contract

The operating contract for the Virtual Tour team. The **main session acts as the
delivery-orchestrator**. Read this before running any loop. Loaded via `/tour-loop` and
referenced by every agent.

## Unit of work: the loop
A **loop** is one small, shippable task defined in `backlog/tasks/NNNN-slug.md`. Every task
carries machine-checkable **acceptance criteria** (markdown checkboxes under
`## Acceptance criteria`). A loop is **done** only when every acceptance box is `[x]` and the
gate passes (see Loop protocol, GATE below). Keep tasks small enough to finish in one focused
loop; split if not.

Task file shape: see `backlog/tasks/TEMPLATE.md`.

## Loop protocol — PLAN → BUILD → VERIFY → GATE {#loop-protocol}

**PLAN** (`planner`, `architect` as needed)
- Confirm the task is well-formed: clear goal, scoped, with concrete acceptance criteria.
- If criteria are missing/vague, write them first. If the task is too big, split into sub-tasks.
- Output: an agreed task file with acceptance criteria + a short build plan.

**BUILD** (one or more execution specialists — dispatched, not parallel-on-shared-code)
- Route to the right specialist(s) via the delegation map (#delegation-map).
- Code changes touching the same files run **sequentially** through one specialist at a time
  (tightly-coupled coding parallelizes badly). Independent files may go to different specialists.
- Output: the change + a handoff report (#handoff-format).

**VERIFY** (read-only gates, run in **parallel**)
- `qa-verifier` → runs lint → type → test → build, checks acceptance criteria, emits PASS/FAIL.
- `code-reviewer` → correctness, clarity, maintainability, scope-fidelity; emits PASS/
  CHANGES-REQUESTED.
- `security-devops` → vuln + tenant-isolation + upload/footage-license review (required when the
  change is security-sensitive — see `rules/security.md`).
- `video-judge` → rendered-video quality score (required when the change affects render output).
- These are read-only and independent → dispatch them in a single batch (parallel).

**GATE** (main session decides)
- Done when **all** hold: every acceptance criterion is `[x]`; `qa-verifier` = PASS (lint/type/
  test/build all green); `code-reviewer` = PASS (no unresolved Critical/High findings and **no
  scope drift** — the change matches the approved acceptance criteria exactly: no unapproved
  feature added, no approved one removed); `security-devops` = PASS when required;
  `video-judge` = PASS when required. `video-judge` and `code-reviewer` verdicts are blocking.
- All PASS and criteria met → mark the task done, append a `docs/process/lessons.md` retro.
- Any FAIL/CHANGES-REQUESTED → route findings to `debugger` (failures) or the owning specialist
  (review/security/judge findings) → return to BUILD → re-VERIFY. Repeat until green or capped
  (see Loop state and the Stop-gate below).

## Delegation map {#delegation-map}

| Work | Agent | Phase |
|------|-------|-------|
| Task breakdown, acceptance criteria | planner | PLAN |
| Architecture, ADRs, contracts, one-way doors | architect | PLAN |
| Next.js UI structure, data/routing, player integration | frontend-engineer | BUILD |
| Design system/tokens, premium light-mode direction, UI design review | ui-designer | BUILD/VERIFY |
| 3D/WebGL, motion, the Earth fly-to hero (experiential layer) | motion-3d-engineer | BUILD |
| API, pipeline stages, DB, stock clients, providers | pipeline-engineer | BUILD |
| Remotion compositions, motion graphics, render worker | remotion-engineer | BUILD |
| Scene-plan review, footage curation rubric, prompts | cinematic-director | BUILD/VERIFY |
| Tests, fixtures, golden samples | test-engineer | BUILD |
| Rendered-video quality scoring | video-judge | VERIFY |
| Diff review + scope-fidelity gate | code-reviewer | VERIFY |
| Run lint/typecheck/test/build, tick criteria boxes | qa-verifier | VERIFY |
| Docker, CI, deploys, tenant isolation, upload safety, licenses | security-devops | BUILD/VERIFY |
| Mine reference repos for a phase's concepts, write reuse report | research-scout | phase boundary |
| Root-cause failures | debugger (global) | any |

Rules: exactly one owner per work item. Builders never verify their own output.
video-judge and code-reviewer verdicts are blocking. UI diffs get TWO reviews: `ui-designer` judges
design/craft against rules/design.md (premium light + 3D/motion), `code-reviewer` judges
correctness/scope — both blocking. Light-mode Playwright screenshots (1440px + 390px) attach to VERIFY
handoffs. Frontend split: ui-designer (direction/tokens) -> frontend-engineer (app structure/data) +
motion-3d-engineer (3D/motion/hero).

## Handoff / report contract (every subagent returns this) {#handoff-format}
```
SUMMARY:   one-line what-I-did / what-I-found
CHANGES:   files touched (path — one-line why), or "none (read-only)"
FINDINGS:  list of {severity, confidence, file:line, issue, fix}  — or "none"
VERIFY:    commands run + results (lint/type/test), or "n/a"
STATUS:    PASS | FAIL | CHANGES-REQUESTED | BLOCKED | NEEDS-REVIEW
NEXT:      recommended next role/action, or "ready for gate"
```
Subagents return raw data, not prose for a human — the main session synthesizes for the user.

## Parallel vs sequential (cost-aware)
- **Parallel**: independent read-only work — the VERIFY gates, multi-angle research, scanning
  different modules. Dispatch as one batch of Agent calls.
- **Sequential / single conductor**: edits to shared code, debugging, anything needing shared
  state. Multi-agent coding on the same surface duplicates and conflicts — don't.
- Subagents cost ~4–15× a single turn. Delegate for **isolation** (separate context, tool limits,
  read-only enforcement) and **breadth**, not for trivial lookups.

## Loop state and the Stop-gate (the "don't quit early" backstop)
`/tour-loop` writes `.claude/loop-state.local.json` (git-ignored):
```json
{ "active": true, "task_file": "backlog/tasks/0001-slug.md",
  "iteration": 1, "max_iterations": 5 }
```
The `Stop` hook (`.claude/hooks/stop/qa-gate.sh`) enforces completion:
- No state file, or `active:false`, or env `TOUR_LOOP_OFF=1` → stop is allowed (default-safe).
- All acceptance boxes checked → stop allowed (done).
- `iteration >= max_iterations` → stop allowed, with a warning (safety cap against runaway).
- Otherwise → increments iteration and **blocks the stop**, re-injecting "continue the loop".

To end a loop manually: set `active:false` in the state file (or `rm` it), or
`export TOUR_LOOP_OFF=1`. Outside an active loop the hook never fires — normal sessions are
unaffected.

## Severity & confidence vocabulary (shared by all findings/reviews) {#severity}
**Severity** — Critical: exploitable / data loss / silent corruption. High: likely bug or vuln,
real impact. Medium: correctness/maintainability risk under some conditions. Low: style, minor.
**Confidence** — verified: reproduced or proven (test/trace). likely: strong static evidence,
not yet reproduced. speculative: plausible, needs investigation. Always state both; never present
speculative as verified.

## Process & documentation
Doc set, owners, and the adopt/defer list live in `docs/process/README.md` (single source, not
duplicated here). Continuity: read `docs/process/lessons.md` before every PLAN; append a 3-line
retro (Worked / Didn't / Change) to it at every GATE.

## Phase boundaries
Closing a phase's tasks doesn't decide the next phase — that's `/phase-review` (a command, not a
dedicated agent): `planner` + `architect` propose the next phase's scope from shipped results,
ADRs, and `lessons.md`; the user decides. Fires once per phase boundary, not part of the per-loop
protocol above.
