---
name: security-audit
description: Audit code or a diff for vulnerabilities using the Aegis taxonomy (injection, authz, crypto, deserialization, secrets, SSRF, resource/DoS, logic/data-flow) and return findings mapped to CWE with severity + confidence. Use for security-sensitive changes, threat models, or "audit this", "find vulnerabilities", "is this safe".
---

# security-audit

A vulnerability-focused audit that traces attacker-controlled data to dangerous sinks. This is the
security gate of the Aegis loop; it applies `.claude/rules/security.md`.

## When to use
- A change touches input parsing, auth/authz, crypto, subprocess/exec, file/network I/O, deserialization, the detection rules, or secrets.
- A design needs a threat model before build.
- Someone asks "is this safe / exploitable?"

## Steps
1. **Map trust boundaries** — what is attacker-controlled (including the code under analysis, which is hostile input)? What are the sinks?
2. **Walk the taxonomy** (`.claude/rules/security.md`): injection · authz/IDOR · crypto misuse · unsafe deserialization/exec · secrets · SSRF/unsafe outbound · resource/DoS · logic & data-flow (TOCTOU, overflow, swallowed errors, cross-function invariants).
3. **Trace** at least one tainted-input → sink path concretely; note where validation/escaping belongs.
4. **For analyzed-code handling:** confirm target code is never executed unsandboxed; path-traversal and resource limits hold.
5. **For each finding:** `severity · confidence · file:line · attack scenario · fix`, mapped to CWE. Verdict PASS / CHANGES-REQUESTED.

## Judgment
- Lead with exploitability — a real path beats a theoretical worry. Mark confidence honestly.
- A hardcoded secret is always reported to the user, never silently relocated.
- Separate "exploitable now" (blocking) from "hardening" (suggestion).

## Output artifacts
| You ask for… | You get… |
|---|---|
| "audit this change" | CWE-mapped findings + attack scenarios + PASS/CHANGES-REQUESTED |
| "threat-model X" | trust-boundary map + ranked risks + mitigations |

## Related
- `deep-review` — general correctness/quality review. `report` — formats findings for delivery.
