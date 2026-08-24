# Security standard (Aegis)

Two jobs: (a) the **detection taxonomy** Aegis must find in *other* people's code, and (b) how we
keep *Aegis itself* secure. Complements the global security rule.

## (a) Detection taxonomy — what Aegis hunts
The shared vocabulary for what "a vulnerability" means to Aegis. `detection-engineer` builds passes
for these; `security-auditor` reviews against them.
- **Injection** — SQL, command, path traversal, template, LDAP, NoSQL. Trace tainted input → sink.
- **AuthN/AuthZ** — missing/incorrect access checks, IDOR, privilege escalation, broken session logic.
- **Crypto misuse** — weak algorithms, static IVs/keys, `alg:none`, missing verification, bad randomness.
- **Unsafe deserialization / code exec** — pickle, yaml.load, eval/exec, gadget chains.
- **Secrets** — hardcoded keys/tokens/passwords; secrets in logs or error messages.
- **SSRF / unsafe outbound** — user-controlled URLs, missing TLS verification, open redirects.
- **Memory/resource** — unbounded allocation, leaks, DoS via algorithmic complexity.
- **Logic/data-flow** — TOCTOU races, integer overflow, error-handling that swallows failures,
  cross-function invariant violations that single-file linters miss. **This is Aegis's differentiator.**
Map findings to CWE where possible; score with severity + confidence.

## (b) Securing Aegis itself
- Validate at boundaries (CLI args, API handlers, file uploads, the code under review is untrusted input).
- Never `verify=False`; HTTPS for all external calls; restrictive CORS by default.
- Treat analyzed repositories as **hostile input** — sandbox execution, no eval of target code, guard
  path traversal and resource exhaustion when parsing arbitrary projects.
- Secrets via env + `.env.example`; never commit `.env`, keys, tokens. Flag hardcoded secrets to the user.
- Pin deps in `uv.lock`; run `uv pip audit` before release; review new deps for attack surface.
- LLM-specific: treat model output that drives actions as untrusted; guard against prompt injection in
  analyzed code/comments influencing Aegis's own behavior.
