---
name: tour-loop
description: Run one delivery loop on a task — PLAN, BUILD, VERIFY, GATE — coordinating the agent team until acceptance criteria pass QA and review. The core daily driver.
argument-hint: <task-id | slug | "free-text goal"> [--max N]
---

# /tour-loop $ARGUMENTS

You are the **delivery-orchestrator**. Run the virtual-tour delivery loop on the requested task,
coordinating the team until the Definition of Done is met. The full contract is
`.claude/rules/orchestration.md` — follow it; this command is the operational checklist.

## 0. Resolve the task
- If `$ARGUMENTS` names an existing task (id `NNNN`, a slug, or a path under `backlog/tasks/`), use it.
- If it's a free-text goal, check the backlog for a match; if none, dispatch `planner` to write the
  task file (with acceptance criteria) before building.
- If `$ARGUMENTS` is empty, pick the next ready (unblocked, highest-priority) task from
  `backlog/ROADMAP.md` / `backlog/tasks/`.
- Parse an optional `--max N` (default 5) for the iteration cap.
- Confirm the chosen task and its acceptance criteria back to the user in one line before proceeding.

## 1. Arm the loop
- Ensure you are NOT on `main`/`master` (edits there are hook-blocked). If on a protected branch,
  create a feature branch: `git switch -c <type>/<slug>`.
- Write `.claude/loop-state.local.json` with exactly these keys (consumed by the `qa-gate` Stop hook):
  ```json
  { "active": true, "task_file": "backlog/tasks/<file>.md", "iteration": 0, "max_iterations": 5 }
  ```
  (`max_iterations` = the parsed `--max`, default 5.) This arms the Stop-gate, which keeps the loop
  alive until every acceptance box is checked or the cap is hit.

## 2. PLAN — `planner` (+ `architect` if flagged)
- **Read `docs/process/lessons.md` first** (apply past lessons, newest entries).
- Add `architect` when the task trips the design-doc trigger in `docs/process/README.md`
  (ambiguous, contentious, or multi-component) or the task file flags an architecture decision.
- If acceptance criteria are missing or vague, fix that first — do not build against vague criteria.
- Restate the goal + criteria + the build plan (which specialist does what).

## 3. BUILD
- Dispatch the owning specialist(s) per the delegation map
  (`.claude/rules/orchestration.md#delegation-map`): `frontend-engineer`, `pipeline-engineer`,
  `remotion-engineer`, `cinematic-director`, `test-engineer`, `security-devops`.
- Edits to the same files go through ONE specialist at a time (no parallel edits on shared code);
  independent files may parallelize.
- Each returns the handoff report (`.claude/rules/orchestration.md#handoff-format`).

## 4. VERIFY (parallel, read-only — dispatch as one batch)
- `qa-verifier` — always: lint → type → test → build, checks acceptance criteria (PASS/FAIL).
- `code-reviewer` — always, on any non-trivial diff: correctness, clarity, scope-fidelity
  (PASS/CHANGES-REQUESTED). Blocking.
- `security-devops` — required when the change is security-sensitive (`.claude/rules/security.md`):
  vuln + tenant-isolation + upload/footage-license review.
- `video-judge` — required when a render was produced: rendered-video quality score. Blocking.
- `cinematic-director` — required when a scene plan changed: scene-plan / footage-curation review.

## 5. GATE
- **All required gates PASS** AND every acceptance criterion is objectively met →
  1. Check the satisfied boxes in the task file (`- [ ]` → `- [x]`).
  2. Append a retro to `docs/process/lessons.md`, newest first under the `---`: date + one line
     each for Worked / Didn't / Change.
  3. Commit (conventional commit, both co-author trailers per the root `CLAUDE.md` conventions).
  4. Disarm the loop: set `"active": false` in `.claude/loop-state.local.json` (or remove it).
  5. Report done to the user.
- **Any FAIL/CHANGES-REQUESTED** → route findings: test/runtime failures → `debugger` (global);
  review/security/judge/director findings → the owning specialist. Return to BUILD, re-VERIFY.
  The Stop-gate enforces continuation until done or capped.

## 6. Stop conditions
- **Done:** all acceptance boxes checked → the Stop-gate allows the turn to end.
- **Capped:** `iteration >= max_iterations` → stop with a status summary of what remains.
- **Manual:** user sets `"active": false` in the state file (or removes it), or
  `export TOUR_LOOP_OFF=1`.

## Always
- Synthesize subagent reports for the user (subagents return raw data). Keep the user oriented:
  task, phase, what passed/failed, next.
- Never check an acceptance box that isn't objectively met. Never green-wash a failing gate.
