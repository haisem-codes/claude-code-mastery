---
name: standup
description: Summarize backlog and loop status — what's done, in-progress, blocked, and the next ready task. A quick project status read; changes nothing.
argument-hint: (none)
---

# /standup

Give a concise status read of the virtual-tour project. Do **not** change anything.

1. **Active loop** — read `.claude/loop-state.local.json`; if active, report task_file + iteration/max.
2. **Backlog** — scan `backlog/ROADMAP.md` and `backlog/tasks/*.md`. For each task summarize id, title,
   owner, and status: *done* if all acceptance boxes checked, *in-progress* if some, *ready* if unblocked,
   *blocked* otherwise.
3. **Next** — recommend the single next task to run with `/tour-loop`, and why.
4. **Health** — if quick to check, note the last verification status; flag anything stale or blocked > 1 loop.

Output: a short table (id · title · owner · status) + a one-line `next:` recommendation. Keep it skimmable.
