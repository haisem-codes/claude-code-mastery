---
name: plan-feature
description: Turn a goal or vision slice into a spec with measurable acceptance criteria and an ordered set of backlog tasks. Use when starting a feature, breaking down work, or when a task lacks clear acceptance criteria. Triggers - "plan this", "break this down", "write acceptance criteria", "groom the backlog".
---

# plan-feature

Turn a fuzzy goal into a buildable plan: a short spec, measurable acceptance criteria, and an
ordered list of small tasks (loops). This is the PLAN step of the Notetaker loop.

## When to use
- A new feature/slice is starting and needs requirements + criteria.
- A task is too big, or its acceptance criteria are vague/missing.
- The backlog needs sequencing or grooming.

## Steps
1. **Frame** — read `docs/vision.md` and related ADRs. State the user-facing goal in one sentence
   and the smallest valuable slice.
2. **Specify** — write user stories and **acceptance criteria as checkboxes**. Each must be
   objective: a reviewer can mark it true/false from observable behavior. Note non-goals + assumptions.
3. **Decompose** — split into tasks each completable in one loop. Order by dependency. Assign each
   an owner role from the org.
4. **Record** — create `backlog/tasks/NNNN-slug.md` per task from `backlog/tasks/TEMPLATE.md`;
   update `backlog/ROADMAP.md`.
5. **Recommend** the next task to run with `/note-loop`.

## Writing good acceptance criteria
- Objective and observable ("uploading a 90-min .m4a returns a job id and the UI shows
  transcribing progress"), not subjective ("upload works well").
- One assertion per checkbox. Include the negative cases (a 2GB upload is rejected with a clear
  error; a corrupt file doesn't wedge the job queue).
- For UI tasks, reference the checkable items in `.claude/rules/design.md` (states designed,
  AA contrast, reduced motion) rather than "looks beautiful".
- For pipeline tasks, state measurable note-quality properties (all corpus fixtures produce notes
  with sections + key concepts; no hallucinated facts flagged by `notes-judge`).
- Lint/type/test green is implied by the GATE — but call out any *new* tests the task requires.

## Output artifacts
| You ask for… | You get… |
|---|---|
| "plan feature X" | a spec slice + acceptance criteria + ordered `backlog/tasks/*.md` |
| "break down task N" | sub-tasks with dependencies + owners |
| "groom backlog" | re-sequenced ROADMAP + ready/blocked status per task |

## Related
- `verify`, the design/security/notes gates — what each task must pass. `report` — the closing summary.
- Roles: `planner` (sequencing), `architect` (design/ADR), `research-analyst` (choices).
