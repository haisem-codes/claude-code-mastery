# Orchestration Contract

The operating contract for the Aegis team. The **main session acts as the
delivery-orchestrator**. Read this before running any loop. Loaded via `/aegis-loop` and
referenced by every agent.

## 1. Unit of work: the loop
A **loop** is one small, shippable task defined in `backlog/tasks/NNNN-slug.md`. Every task
carries machine-checkable **acceptance criteria** (markdown checkboxes under
`## Acceptance criteria`). A loop is **done** only when every acceptance box is `[x]` and the
gates pass (§5). Keep tasks small enough to finish in one focused loop; split if not.

Task file shape: see `backlog/tasks/TEMPLATE.md`.

## 2. The loop protocol — PLAN → BUILD → VERIFY → GATE

**PLAN** (`planner`, `product-strategist`, `principal-architect` as needed)
- Confirm the task is well-formed: clear goal, scoped, with concrete acceptance criteria.
- If criteria are missing/vague, write them first. If the task is too big, split into sub-tasks.
- Output: an agreed task file with acceptance criteria + a short build plan.

**BUILD** (one or more execution specialists — dispatched, not parallel-on-shared-code)
- Route to the right specialist(s) via the delegation map (§3).
- Code changes touching the same files run **sequentially** through one specialist at a time
  (tightly-coupled coding parallelizes badly). Independent files may go to different specialists.
- Output: the change + a handoff report (§4).

**VERIFY** (read-only gates, run in **parallel**)
- `qa-verifier` → runs lint → type → test, checks acceptance criteria, emits PASS/FAIL.
- `code-reviewer` → correctness, clarity, maintainability; emits PASS/CHANGES-REQUESTED.
- `security-auditor` → vulns + threat-model delta (required when the change is security-sensitive).
- These are read-only and independent → dispatch them in a single batch (parallel).

**GATE** (orchestrator decides)
- All gates PASS and all acceptance criteria met → run `report`, check the boxes, mark done.
- Any FAIL/CHANGES-REQUESTED → route findings to `debugger` (failures) or the owning specialist
  (review/security findings) → return to BUILD → re-VERIFY. Repeat until green or capped (§7).

**TEACH** (`teacher`, automatic — after GATE, non-blocking)
- After a loop is done, `teacher` writes/updates a Roman Urdu `.docx` lesson in `docs/learn/` explaining the
  concepts (especially cybersecurity) that loop used — concept level, no code. Keeps the owner's understanding current.

## 3. Delegation map
| Situation | Route to |
|---|---|
| Vague goal / missing requirements / acceptance criteria | `product-strategist` then `planner` |
| System design, tech choice, cross-cutting structure | `principal-architect` (writes an ADR) |
| "How do we do X?" / prior art / feasibility | `research-analyst` |
| **A phase just finished** — decide the next phase's scope from full context + deep external research (OSS teardowns, recent papers, competitor + market analysis) with a novel, sellable angle | `phase-strategist` (phase boundary only; proposes → `product-strategist`/`planner` task it) |
| Break work into ordered tasks/loops | `planner` |
| Core services, API, CLI, data models, plumbing | `backend-engineer` |
| The detection engine: AST / data-flow / call-graph / LLM-reasoning passes | `detection-engineer` |
| Tests, fixtures, coverage, the known-vuln benchmark suite | `test-engineer` |
| CI/CD, Docker, packaging, release | `devops-engineer` |
| A failing test / stack trace / wrong output | `debugger` |
| Review a diff before the gate; scope fidelity / anti-hallucination (no unapproved adds, no approved drops) | `code-reviewer` |
| Vulnerability / threat-model review | `security-auditor` |
| Run lint+type+test and check acceptance criteria | `qa-verifier` |
| Teach the concepts behind the work (Roman Urdu, `.docx`), each loop | `teacher` (auto after GATE) |

## 4. Handoff / report contract (every subagent returns this)
```
SUMMARY:   one-line what-I-did / what-I-found
CHANGES:   files touched (path — one-line why), or "none (read-only)"
FINDINGS:  list of {severity, confidence, file:line, issue, fix}  — or "none"
VERIFY:    commands run + results (lint/type/test), or "n/a"
STATUS:    PASS | FAIL | CHANGES-REQUESTED | BLOCKED | NEEDS-REVIEW
NEXT:      recommended next role/action, or "ready for gate"
```
Subagents return raw data, not prose for a human — the orchestrator synthesizes for the user.

## 5. Definition of Done (the gate)
A loop is done when **all** hold:
- [ ] Every acceptance criterion in the task file is `[x]`.
- [ ] `qa-verifier` = PASS (ruff + mypy + pytest all green on the change).
- [ ] `code-reviewer` = PASS (no unresolved Critical/High findings **and no scope drift** — the change matches
      the approved acceptance criteria exactly: no unapproved feature added, no approved one removed).
- [ ] `security-auditor` = PASS — **required** when the change touches: input parsing, auth/authz,
      crypto, subprocess/exec, file/network I/O, deserialization, the detection rules, or secrets.
- [ ] A `report` entry is written (what changed, findings resolved, residual risk).

## 6. Parallel vs sequential (cost-aware)
- **Parallel**: independent read-only work — the three VERIFY gates, multi-angle research,
  scanning different modules. Dispatch as one batch of Agent calls.
- **Sequential / single conductor**: edits to shared code, debugging, anything needing shared
  state. Multi-agent coding on the same surface duplicates and conflicts — don't.
- Subagents cost ~4–15× a single turn. Delegate for **isolation** (separate context, tool limits,
  read-only enforcement) and **breadth**, not for trivial lookups.

## 7. Loop state and the Stop-gate (the "don't quit early" backstop)
`/aegis-loop` writes `.claude/loop-state.local.json` (git-ignored):
```json
{ "active": true, "task": "0001-slug", "task_file": "backlog/tasks/0001-slug.md",
  "iteration": 1, "max_iterations": 12, "phase": "BUILD" }
```
The `Stop` hook (`.claude/hooks/stop/qa-gate.sh`) enforces completion:
- No state file, or `active:false`, or env `AEGIS_LOOP_OFF=1` → stop is allowed (default-safe).
- All acceptance boxes checked → stop allowed (done).
- `iteration >= max_iterations` → stop allowed, with a warning (safety cap against runaway).
- Otherwise → increments iteration and **blocks the stop**, re-injecting "continue the loop".

To end a loop manually: set `active:false` in the state file (or `rm` it), or `export AEGIS_LOOP_OFF=1`.
Outside an active loop the hook never fires — normal sessions are unaffected.

## 8. Severity & confidence vocabulary (shared by all findings/reviews)
**Severity** — Critical: exploitable / data loss / silent corruption. High: likely bug or vuln,
real impact. Medium: correctness/maintainability risk under some conditions. Low: style, minor.
**Confidence** — verified: reproduced or proven (test/trace). likely: strong static evidence,
not yet reproduced. speculative: plausible, needs investigation. Always state both; never present
speculative as verified.

## 9. Process & documentation (lightweight, proven — right-sized for a subagent team)
Full version: `docs/process/README.md`. We adopt proven artifacts at small-team weight; subagents play the roles.
- **Doc set & owners:** vision + strategy → `product-strategist`; design docs + ADRs → `principal-architect`;
  tasks + sprint plans → `planner`; lessons log → orchestrator captures; Definition of Done → the VERIFY gates.
- **Design-doc trigger:** for an ambiguous / contentious / multi-component decision, `principal-architect` writes a
  Google-format design doc (`docs/architecture/`, see `design-doc-template.md`) before coding, then records the
  decision as an ADR. Skip it for straightforward tasks — acceptance criteria suffice. For a **detection**
  design doc, include a `research-scout` SOTA literature scan (last ~3 years) as input.
- **Sprints (Shape-Up appetite):** group loops into a just-in-time-planned sprint (`docs/process/sprint-template.md`);
  fixed time-box, variable scope — cut scope, not quality. Plan only the next sprint in detail.
- **Continuity:** **read `docs/process/lessons.md` before planning** any sprint/loop; append a 3-line retro
  (Worked / Didn't / Change) to it at every GATE so we don't repeat mistakes.
- **JIT depth:** pre-development docs stay high-level; deep code-level design happens in the loop that builds it.

## 10. Phase boundaries — the `phase-strategist` (deciding the *next* phase)
Loops close tasks; something must decide the **next phase**. That's the `phase-strategist` — dispatched
**only at a phase boundary** (all the phase's loops done, results in), via `/phase-review` or the orchestrator.
It is *not* part of the per-loop protocol (that ends at TEACH); it fires once per phase.
- **Input:** complete context — shipped loops + their reports, ADRs, strategy docs, `lessons.md`, the code
  reality, and the phase's **measured results** (e.g. the benchmark numbers). It needs the outcome, so it runs
  *after* the phase's results exist, never before.
- **Work:** deep external research — open-source SAST/SCA teardowns (keep what's useful, beat what isn't),
  recent (2023+) papers (reusing `research-scout`'s reading-log), and competitor + market/sellability analysis
  — then proposes the next phase as a **small, finishable portfolio: 1–2 novel approaches done right (quality
  over quantity) PLUS proven, still-missing capabilities and language/coverage support that make Aegis
  sellable** (measurable milestone + ordered candidate loops labelled novel vs. proven-coverage + alternatives
  + risks/kill-criteria) in `docs/strategy/phase-<N+1>-proposal.md`.
- **Authority:** it **proposes; it does not decide.** The user (owner) picks the phase; then
  `product-strategist` (requirements) → `planner` (ordered loops with acceptance criteria) task it, and normal
  `/aegis-loop`s resume. Advisory + generative — it never blocks shipping.
- **Bar:** the mandate is the best, *actually-sellable* tool in the niche — a me-too next phase, novelty that
  can't ship or sell, or a sprawling wish-list that finishes nothing, is a failed review. **Quality over
  quantity: 1–2 novel approaches done right, paired with proven coverage/language fills, beat a broad shallow
  list.** Evidence over hype; cite sources; respect accepted ADRs unless it explicitly argues to override one.
