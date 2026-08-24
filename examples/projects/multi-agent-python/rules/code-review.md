# Code review standard (Aegis)

How `code-reviewer` (and anyone reviewing a diff) evaluates a change. `code-reviewer` is also the team's
**scope guardian / anti-hallucinator**. Output uses the handoff contract in `orchestration.md` and the
shared severity/confidence vocab.

## What to check (in priority order)
1. **Scope fidelity (anti-hallucination)** — the change implements **exactly** the task's approved acceptance
   criteria (and the agreed scope in `docs/strategy/` / ADRs): **no unapproved feature, dependency, endpoint,
   config, or behavior added**, and **no approved feature removed, weakened, or silently changed**. Scope drift
   is **blocking** (CHANGES-REQUESTED), even if the code is otherwise correct.
2. **Correctness** — does it do what the task says? Edge cases, off-by-one, error paths, None/empty,
   concurrency/async races, resource leaks, time/locale/encoding assumptions.
3. **Security** — input validation at boundaries, injection (SQL/command/path), unsafe deserialization,
   secrets in code, authz checks. Deep security goes to `security-auditor`; flag anything suspicious.
4. **Tests** — do new/changed paths have tests? Do tests assert behavior, not implementation? Would they
   actually fail if the code regressed?
5. **Clarity & maintainability** — names, function size, cyclomatic complexity, dead code, premature
   abstraction (rule of three), comments that explain *why* not *what*.

## Output
For each finding: `severity · confidence · file:line · issue · concrete fix`. Group by severity. End with a verdict:
- **PASS** — no unresolved Critical/High and no scope drift; Medium/Low noted as suggestions.
- **CHANGES-REQUESTED** — one or more Critical/High, **or any scope drift**, must be fixed before the gate.

## Principles
- Review the diff, not the whole repo — but read enough surrounding context to judge correctness and scope.
- Prefer specific, actionable feedback with a suggested fix over vague concerns.
- Distinguish blocking issues from preferences; don't block on style the linter already enforces.
- Be adversarial about correctness, security, and **scope**; be generous about style.
