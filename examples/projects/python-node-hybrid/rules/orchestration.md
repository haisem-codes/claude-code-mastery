# Orchestration Contract

The operating contract for the Notetaker team. The **main session acts as the
delivery-orchestrator**. Read this before running any loop. Loaded via `/note-loop` and
referenced by every agent.

## 1. Unit of work: the loop
A **loop** is one small, shippable task defined in `backlog/tasks/NNNN-slug.md`. Every task
carries machine-checkable **acceptance criteria** (markdown checkboxes under
`## Acceptance criteria`). A loop is **done** only when every acceptance box is `[x]` and the
gates pass (§5). Keep tasks small enough to finish in one focused loop; split if not.

Task file shape: see `backlog/tasks/TEMPLATE.md`.

## 2. The loop protocol — PLAN → BUILD → VERIFY → GATE

**PLAN** (`planner`, `architect`, `research-analyst` as needed)
- Confirm the task is well-formed: clear goal, scoped, with concrete acceptance criteria.
- If criteria are missing/vague, write them first. If the task is too big, split into sub-tasks.
- For a stack/library/model choice (STT engine, PDF renderer, LLM prompting strategy), get a
  short `research-analyst` comparison and record the decision as an ADR.
- Output: an agreed task file with acceptance criteria + a short build plan.

**BUILD** (one or more execution specialists — dispatched, not parallel-on-shared-code)
- Route to the right specialist(s) via the delegation map (§3).
- Code changes touching the same files run **sequentially** through one specialist at a time.
  Independent surfaces (e.g. `backend/` vs `frontend/`) may go to different specialists in parallel.
- Output: the change + a handoff report (§4).

**VERIFY** (read-only gates, run in **parallel** as one batch)
- `qa-verifier` — **always.** Runs both verification stacks (ruff+mypy+pytest, eslint+tsc+vitest),
  checks acceptance criteria, emits PASS/FAIL.
- `code-reviewer` — **always.** Correctness, clarity, maintainability, scope fidelity;
  emits PASS/CHANGES-REQUESTED.
- `security-auditor` — **required** when the change touches: file upload/parsing, audio decoding,
  subprocess/ffmpeg, auth, file paths/storage, network I/O, CORS, deserialization, or secrets.
- `design-reviewer` (`ui-designer`) — **required** when the change touches frontend UI or the PDF
  template. Judges against `.claude/rules/design.md`; screenshots via Playwright when the app runs.
- `notes-judge` — **required** when the change touches the transcription/notes pipeline or its
  prompts. Judges generated notes for faithfulness, coverage, and structure against the corpus.

**GATE** (orchestrator decides)
- All required gates PASS and all acceptance criteria met → run `report`, check the boxes, mark done.
- Any FAIL/CHANGES-REQUESTED → route findings to `debugger` (failures) or the owning specialist
  (review/design/security/notes findings) → return to BUILD → re-VERIFY. Repeat until green or capped (§7).
- **3 consecutive failed fix attempts on the same issue → STOP the loop** and report to the user:
  what was tried, the actual failure mode, the smallest reproducer. That's an assumption problem,
  not a typo.

## 3. Delegation map
| Situation | Route to |
|---|---|
| Vague goal / missing requirements / acceptance criteria | `planner` |
| System design, stack choice, API contract, cross-cutting structure | `architect` (writes an ADR) |
| "How do we do X?" / library or model comparison / feasibility | `research-analyst` |
| Break work into ordered tasks/loops | `planner` |
| Design language, layout, visual direction, interaction states, PDF template aesthetics | `ui-designer` |
| React/TS UI implementation — recording, upload, progress, notes viewer, download | `frontend-engineer` |
| FastAPI endpoints, job orchestration, storage, PDF rendering service, data models | `backend-engineer` |
| STT transcription, LLM note-structuring, prompts, chunking, notes schema, quality eval corpus | `ai-engineer` |
| Tests, fixtures (sample audio/transcripts), coverage, E2E (Playwright) | `test-engineer` |
| Docker, CI/CD, packaging, GPU runtime | `devops-engineer` |
| A failing test / stack trace / wrong output | `debugger` |
| Review a diff before the gate; scope fidelity (no unapproved adds, no approved drops) | `code-reviewer` |
| Vulnerability / hostile-input review | `security-auditor` |
| Visual quality gate on UI / PDF output | `ui-designer` (as design-reviewer) |
| Note-quality gate on pipeline/prompt changes | `notes-judge` |
| Run both verification stacks and check acceptance criteria | `qa-verifier` |

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
- [ ] `qa-verifier` = PASS (both stacks green on the change: ruff+mypy+pytest, eslint+tsc+vitest).
- [ ] `code-reviewer` = PASS (no unresolved Critical/High findings **and no scope drift** — the change
      matches the approved acceptance criteria exactly: no unapproved feature added, no approved one removed).
- [ ] `security-auditor` = PASS — when required by the §2 trigger list.
- [ ] `design-reviewer` = PASS — when the change touches UI or PDF templates (`.claude/rules/design.md`).
- [ ] `notes-judge` = PASS — when the change touches the notes pipeline or prompts.
- [ ] A `report` entry is written (what changed, findings resolved, residual risk).

## 6. Parallel vs sequential (cost-aware)
- **Parallel**: independent read-only work — the VERIFY gates, multi-angle research, scanning
  different modules; and independent surfaces (backend vs frontend) at BUILD. One batch of Agent calls.
- **Sequential / single conductor**: edits to shared code, debugging, anything needing shared
  state. Multi-agent coding on the same surface duplicates and conflicts — don't.
- Subagents cost ~4–15× a single turn. Delegate for **isolation** (separate context, tool limits,
  read-only enforcement) and **breadth**, not for trivial lookups.

## 7. Loop state and the Stop-gate (the "don't quit early" backstop)
`/note-loop` writes `.claude/loop-state.local.json` (git-ignored):
```json
{ "active": true, "task": "0001-slug", "task_file": "backlog/tasks/0001-slug.md",
  "iteration": 1, "max_iterations": 12, "phase": "BUILD" }
```
The `Stop` hook (`.claude/hooks/stop/qa-gate.sh`) enforces completion:
- No state file, or `active:false`, or env `NOTE_LOOP_OFF=1` → stop is allowed (default-safe).
- All acceptance boxes checked → stop allowed (done).
- `iteration >= max_iterations` → stop allowed, with a warning (safety cap against runaway).
- Otherwise → increments iteration and **blocks the stop**, re-injecting "continue the loop".

To end a loop manually: set `active:false` in the state file (or `rm` it), or `export NOTE_LOOP_OFF=1`.
Outside an active loop the hook never fires — normal sessions are unaffected.

## 8. Severity & confidence vocabulary (shared by all findings/reviews)
**Severity** — Critical: exploitable / data loss / silent corruption. High: likely bug or vuln,
real impact. Medium: correctness/maintainability risk under some conditions. Low: style, minor.
**Confidence** — verified: reproduced or proven (test/trace). likely: strong static evidence,
not yet reproduced. speculative: plausible, needs investigation. Always state both; never present
speculative as verified.

## 9. Process & documentation (lightweight)
- **ADRs** (`docs/adr/`) — record non-trivial architecture/stack decisions (STT engine, PDF renderer,
  storage, chunking strategy). `architect` owns them.
- **Design system** (`docs/design/`) — `ui-designer` owns the design language doc + tokens; the
  design-review gate judges against it.
- **Notes-quality corpus** (`backend/tests/corpus/`) — small set of lecture audio/transcript fixtures
  with expected note properties; `ai-engineer` maintains it, `notes-judge` gates against it.
- **Continuity:** read `docs/process/lessons.md` before planning any loop; append a 3-line retro
  (Worked / Didn't / Change) at every GATE.
- **Phase boundaries:** when a phase's loops are done, the orchestrator + `planner` (with
  `research-analyst` input) review results against `backlog/ROADMAP.md` and propose the next
  phase's loops. The user picks; `planner` tasks it. No standing strategist role — this product's
  direction is set by the roadmap.
