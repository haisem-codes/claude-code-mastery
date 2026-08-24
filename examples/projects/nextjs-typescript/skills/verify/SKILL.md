---
name: verify
description: Run the verification loop on changed files — biome, typecheck, related tests, diff self-review. Use for /verify or before any commit.
---
1. `git diff --name-only HEAD` -> changed set.
2. `pnpm biome check --write` on changed ts/tsx/js/json files.
3. `pnpm turbo typecheck` (scope with --filter when a single package changed).
4. Related tests only: `pnpm --filter <pkg> test -- <pattern-from-changed-files>`.
5. UI touched? `pnpm --filter web build`.
6. Re-read the diff: dead code, stray logs, scope creep.
Report one line per step: `OK biome (0)  OK tsc (0)  OK vitest 12/12`.
Anti-Patterns: running the full suite for a one-file change; ticking boxes without output.
Cross-References: rules/verification.md (source of truth), qa-verifier agent.
