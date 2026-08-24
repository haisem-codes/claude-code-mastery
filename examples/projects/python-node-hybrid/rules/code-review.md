# Code review standard

Applied by `code-reviewer` at VERIFY. Priority order: correctness → security → tests →
clarity/maintainability. Don't block on style the linters already enforce.

## Scope fidelity (blocking)
- Compare the diff against the task's approved acceptance criteria.
- No unapproved additions (features, deps, endpoints, config, behaviors).
- No approved removals (nothing in scope dropped, weakened, or silently changed).
- Drift is CHANGES-REQUESTED at severity ≥ High even if the code is otherwise correct.

## Backend (Python)
- Type-annotated, `mypy --strict` clean. Async correctness in FastAPI paths (no blocking
  calls in async handlers — STT/LLM/PDF work goes through the job layer).
- Boundaries validated (upload size/type, request models); internal calls trusted.
- Errors surface as typed HTTP errors with useful messages, not bare 500s.

## Frontend (React/TS)
- No `any` leaks across module boundaries; props/state typed.
- Hooks correctness: exhaustive deps, no state updates after unmount, media resources
  (MediaRecorder, object URLs, audio contexts) released on cleanup.
- Components consume design tokens — hardcoded colors/sizes are a finding.
- Accessibility regressions are findings (see `.claude/rules/design.md`).

## Pipeline code (STT/LLM/PDF)
- Prompts live in versioned files, not inline strings scattered through code.
- LLM outputs parsed defensively (schema-validated); failure paths defined (retry/partial).
- No silent truncation of transcripts; chunking is explicit and tested.

## Findings
`severity · confidence · file:line · issue · concrete fix`, grouped by severity, vocabulary
per `.claude/rules/orchestration.md` §8. Verdict: PASS or CHANGES-REQUESTED.
