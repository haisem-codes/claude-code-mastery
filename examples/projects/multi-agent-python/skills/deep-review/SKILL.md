---
name: deep-review
description: Run a multi-lens review of a diff or module - correctness, security, tests, clarity - and return findings with severity + confidence and a PASS / CHANGES-REQUESTED verdict. Use at the VERIFY step, before commits/PRs, or when asked to "review this", "check this diff", "find issues".
---

# deep-review

A structured, adversarial review that catches what a linter can't. This is the code-review gate of
the Aegis loop; it applies `.claude/rules/code-review.md` and the severity/confidence vocabulary
from `.claude/rules/orchestration.md`.

## When to use
- A change is at VERIFY, or before a commit/PR.
- You want a thorough pass on correctness and security, not just style.

## Steps
1. **Scope** — get the diff (`git diff`) and read enough surrounding context to judge correctness, not just the changed lines.
2. **Review in priority order:**
   - **Correctness** — edge cases, error paths, None/empty, off-by-one, async/concurrency races, resource leaks, encoding/locale/time assumptions, cross-function invariants.
   - **Security** — boundary validation, injection, unsafe deserialization, secrets, authz. Escalate deep vulns to `security-audit`.
   - **Tests** — do changed paths have tests that would actually fail on regression?
   - **Clarity / maintainability** — names, function size, complexity, dead code, premature abstraction, comments that explain *why*.
   - **Fit** — matches conventions, smallest viable change, no scope creep.
3. **For each finding:** `severity · confidence · file:line · issue · concrete fix`. Group by severity.
4. **Verdict:** PASS (no unresolved Critical/High) or CHANGES-REQUESTED (list the blockers).

## Make it adversarial (find the non-obvious)
- Ask "how does this break under hostile input / concurrency / partial failure?"
- Trace one real data path end-to-end rather than skimming.
- Assume the happy path works; spend your attention on the unhappy paths.

## Output artifacts
| You ask for… | You get… |
|---|---|
| "review this diff" | grouped findings + PASS/CHANGES-REQUESTED verdict |
| "is this correct?" | a correctness-focused trace with edge cases checked |

## Related
- `security-audit` — deeper vuln analysis for security-sensitive changes.
- `verify` — the objective lint/type/test signal that accompanies this review.
