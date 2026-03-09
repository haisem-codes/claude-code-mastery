# Global Development Standards

<!-- CUSTOMIZE: Add project-specific overrides in each project's own CLAUDE.md -->

## Philosophy

- **No speculative features** — Don't add features, flags, or config unless actively needed
- **No premature abstraction** — Write it 3 times before extracting a utility
- **Clarity over cleverness** — Readable code beats clever one-liners
- **Replace, don't deprecate** — Remove old code entirely when replacing
- **Verify at every level** — Lint, typecheck, test after every change
- **Bias toward action** — Decide and move for reversible choices; ask before committing to architecture or destructive operations

## Code Quality

### Hard Limits

- Max 100 lines per function, cyclomatic complexity ≤8
- Max 5 positional parameters per function
- Absolute imports only (no relative `..` paths)

### Zero Warnings Policy

Fix every warning from linters, type checkers, and tests. If unfixable, add inline ignore with justification.

### Error Handling

- Fail fast with clear, actionable messages
- Never swallow exceptions silently
- Include context: what operation failed, what input caused it, suggested fix

### Testing

- **Test behavior, not implementation** — Refactors shouldn't break tests
- **Test edges and errors** — Empty inputs, boundaries, malformed data
- **Mock boundaries, not logic** — Only mock network, filesystem, external services

## Git Workflow

- Atomic commits with conventional prefixes: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`
- Never commit: `.env`, credentials, API keys, tokens, `.key`, `.pem`
- Feature branches only — never push directly to main/master
- Never force-push or amend pushed commits without explicit approval

## Security

- Validate all user input at system boundaries
- Parameterize SQL queries (never concatenate user input)
- Escape HTML output to prevent XSS
- Use HTTPS for all external requests
- Pin exact dependency versions (no `^` or `~`)

<!-- CUSTOMIZE: Add language/framework-specific sections below -->
<!-- See templates/stacks/ for Python, TypeScript, Flutter, Go, Rust examples -->
