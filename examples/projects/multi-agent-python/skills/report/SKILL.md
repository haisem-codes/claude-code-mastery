---
name: report
description: Generate a clear findings/review report in Markdown - severity table, per-finding detail (location, evidence, fix), and residual risk. Use to close a loop, summarize a review/audit, or produce Aegis's user-facing output. Triggers - "write the report", "summarize findings", "generate the review".
---

# report

Turn raw findings into a report a human can act on. Used to close a loop, and as the template for
Aegis's own user-facing output.

## When to use
- Closing a loop (what changed, findings resolved, residual risk).
- Summarizing a `deep-review` or `security-audit`.
- Producing the deliverable Aegis emits about a scanned codebase.

## Structure
1. **Bottom line** — one sentence: ship / fix-first / needs-info, and why.
2. **Summary table** — counts by severity (Critical/High/Medium/Low) and the verdict.
3. **Findings** — for each: `severity · confidence · file:line`, the issue, the evidence (data/control path or repro), and a concrete fix. Order by severity.
4. **Verification** — the `verify` result line (ruff/mypy/pytest) and which acceptance criteria are met.
5. **Residual risk / follow-ups** — what's deferred and why; link new backlog tasks.

## Principles
- Every finding has evidence and a fix; no vague concerns.
- State confidence honestly; never present speculative as verified.
- Be concise and skimmable — tables and bullets, not walls of prose.

## Output artifacts
| You ask for… | You get… |
|---|---|
| "write the loop report" | bottom-line + severity table + findings + verify + residual risk |
| "format these findings" | the same, from a supplied findings list |

## Related
- `deep-review`, `security-audit` produce the findings this formats. `plan-feature` captures follow-ups as tasks.
