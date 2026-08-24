# Security rule

Loaded when touching `src/**`, `app/**`, `api/**`, `**/*.py`, `**/*.ts`, `**/*.js`, `**/Dockerfile*`, `**/*.yaml`.

## Secrets
- Never commit: `.env`, `.key`, `.pem`, `credentials.json`, API keys, tokens, JWTs, OAuth client secrets
- Always use env vars for secrets; ship `.env.example` with placeholders
- Flag any hardcoded secret immediately — do not "fix" by moving to a constant, raise to user

## Input handling
- Validate at system boundaries (HTTP handlers, CLI args, message queues, file uploads)
- Trust internal calls between your own functions
- Parameterize SQL — never `f"SELECT … {user_input}"`
- Escape HTML output to prevent XSS
- Reject path traversal: reject `..`, absolute paths, NUL bytes in user-supplied paths

## Network / API
- HTTPS for all external requests; verify TLS (no `verify=False`)
- Restrictive CORS by default (`origins=[]`, not `*`)
- Rate-limit public endpoints
- Time-bound JWTs; rotate signing keys; reject `alg: none`

## Dependencies
- Pin exact versions in lockfiles (`uv.lock`, `pnpm-lock.yaml`)
- Run `uv pip audit` / `pnpm audit` before deploy
- Review new dependencies before adding (attack surface)
- Prefer stdlib over `npm`-style micro-libs

## Container
- Run as non-root `USER` (never `root` in prod)
- Pin base image to SHA digest in prod images
- Don't bake secrets into layers; use build args + multi-stage
- `--read-only` rootfs when possible
