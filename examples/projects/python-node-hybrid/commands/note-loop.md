---
name: note-loop
description: Run one delivery loop on a task — PLAN, BUILD, VERIFY, GATE — coordinating the agent team until acceptance criteria pass QA, review, and the conditional design/security/notes gates. The core daily driver.
argument-hint: <task-id | slug | "free-text goal"> [--max N]
---

# /note-loop $ARGUMENTS

You are the **delivery-orchestrator**. Run the Notetaker delivery loop on the requested task,
coordinating the team until the Definition of Done is met. The full contract is
`.claude/rules/orchestration.md` — follow it; this command is the operational checklist.

## 0. Resolve the task
- If `$ARGUMENTS` names an existing task (id `NNNN`, a slug, or a path under `backlog/tasks/`), use it.
- If it's a free-text goal, check the backlog for a match; if none, create the task first
  (invoke the `plan-feature` skill / `planner`) before building.
- If `$ARGUMENTS` is empty, pick the next ready (unblocked, highest-priority) task from `backlog/ROADMAP.md`.
- Parse an optional `--max N` (default 12) for the iteration cap.
- Confirm the chosen task and its acceptance criteria back to the user in one line before proceeding.

## 1. Arm the loop
- Ensure you are NOT on `main`/`master` (edits there are hook-blocked). Create a feature branch
  if needed: `git switch -c <type>/<slug>`.
- Write `.claude/loop-state.local.json`:
  `{"active": true, "task": "<id-slug>", "task_file": "backlog/tasks/<file>.md", "iteration": 1, "max_iterations": <N>, "phase": "PLAN"}`
  This arms the Stop-gate, which keeps the loop alive until the acceptance boxes are checked or the cap is hit.

## 2. PLAN
- **Read `docs/process/lessons.md` first** (apply past lessons). For an ambiguous / multi-component
  change, ensure an ADR exists (`architect`); for a library/model choice, get a `research-analyst`
  comparison first.
- If acceptance criteria are missing or vague, fix that first (`planner`). Do not build against vague criteria.
- Restate the goal + criteria + the build plan (which specialist does what). Set state `phase:"BUILD"`.

## 3. BUILD
- Dispatch the owning specialist(s) per the delegation map: `frontend-engineer`, `backend-engineer`,
  `ai-engineer`, `test-engineer`, `devops-engineer` — with `ui-designer` providing direction
  artifacts (not code) for UI work.
- Edits to the same files go through ONE specialist at a time; independent surfaces
  (backend vs frontend) may parallelize.
- Each returns the handoff report. Set state `phase:"VERIFY"`.

## 4. VERIFY (parallel, read-only — dispatch as one batch)
- `qa-verifier` — **always**: both stacks (ruff → mypy → pytest; eslint → tsc → vitest) +
  acceptance-criteria check (PASS/FAIL).
- `code-reviewer` — **always**: correctness / clarity / scope fidelity (PASS/CHANGES-REQUESTED).
- `security-auditor` — if the change touches upload/parsing, audio decoding, subprocess/ffmpeg,
  auth, paths/storage, network, CORS, or secrets.
- `ui-designer` (design-review mode) — if the change touches frontend UI or the PDF template;
  judge against `.claude/rules/design.md`, with Playwright screenshots when the app runs.
- `notes-judge` — if the change touches the transcription/notes pipeline or prompts;
  judge faithfulness / coverage / structure against the corpus.

## 5. GATE
- **All required gates green** AND every acceptance criterion objectively met → check the satisfied
  boxes in the task file (`- [ ]` → `- [x]`), invoke `report` to write the loop summary, append a
  3-line retro (Worked / Didn't / Change) to `docs/process/lessons.md`, set state `active:false`,
  and report done to the user.
- **Any red** → route findings: test/runtime failures → `debugger`; review/design/security/notes
  findings → the owning specialist. Set `phase` back to BUILD and iterate. The Stop-gate enforces
  continuation until done or capped.
- **3 consecutive failed fix attempts on the same issue** → stop, summarize what was tried and the
  smallest reproducer, ask the user. Never burn the whole iteration budget on one wall.

## 6. Stop conditions
- **Done:** all acceptance boxes checked → the Stop-gate allows the turn to end.
- **Capped:** `iteration >= max_iterations` → stop with a status summary of what remains.
- **Manual:** user sets `active:false` in the state file, or `export NOTE_LOOP_OFF=1`.

## Always
- Synthesize subagent reports for the user (subagents return raw data). Keep the user oriented:
  task, phase, what passed/failed, next.
- Never check an acceptance box that isn't objectively met. Never green-wash a failing gate.
