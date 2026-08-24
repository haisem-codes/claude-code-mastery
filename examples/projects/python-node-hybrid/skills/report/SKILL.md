---
name: report
description: Generate a clear loop-closing report in Markdown - what changed, gate results, findings resolved, residual risk. Use to close a loop or summarize a review. Triggers - "write the report", "summarize the loop", "loop report".
---

# report

Turn a finished (or stopped) loop into a record a human can act on.

## When to use
- Closing a loop at GATE (what changed, findings resolved, residual risk).
- Summarizing a review/audit run outside a loop.

## Structure
1. **Bottom line** — one sentence: done / stopped-at-cap / blocked, and why.
2. **Gates** — one line per gate run (qa-verifier, code-reviewer, and any conditional gates)
   with verdict; the `verify` result line.
3. **Changes** — files touched, grouped by surface (backend / frontend / pipeline / docs).
4. **Findings resolved** — `severity · confidence · file:line` per item, and how each was fixed.
5. **Residual risk / follow-ups** — what's deferred and why; link new backlog tasks created.

## Principles
- Every claim backed by captured output or a diff; no vague "should work".
- State confidence honestly; never present speculative as verified.
- Concise and skimmable — tables and bullets, not walls of prose.

## Destination
Append to the task file's `## Notes` section (with date), so each task carries its own history.
