# Security rule

## Attack surface (ours)
- Uploads: PDFs/images/text from agents are HOSTILE. Parse via Claude API (multimodal), never
  local parser libs on raw bytes in-process without limits. Enforce: max size 25MB, magic-byte
  type check, no local rasterization/decompression of untrusted archives. Uploaded files go to
  object storage under `tenant/{tenantId}/uploads/`, never to repo or /tmp persistence.
- Footage fetching: only allowlisted provider APIs (Pexels, Pixabay). Never fetch arbitrary
  user-supplied URLs (SSRF). Record license + source_url per clip at fetch time; a clip without
  recorded license never reaches render.
- Tenant isolation: every tenant-owned table has tenant_id; every repository query filters by it.
  Cross-tenant access = Critical severity, blocks merge.
- LLM provider configs: encrypted at rest (llm_connections.config); never logged; keys only via
  env or DB-encrypted config. .env.example ships placeholders only.
- Rendered videos: stored under tenant/{tenantId}/renders/; delivery via signed URLs (Phase 2+).

## Third-party reuse (research library)
- Reference clones live in gitignored research/vendor/; never commit third-party code into our tree.
- Adapt a source into our packages ONLY if it is `vendorable: true` (permissive license allowing
  commercial use + white-label redistribution) in research/sources.json. `unknown`/`local-only`/
  GPL/AGPL/proprietary = read-only reference; re-implement, never copy. Non-compliant reuse = High.
- Every adaptation carries an attribution comment: `// adapted from <id> (<license>)`.

### Known licence traps — 3D / shader / imagery (research 2026-07-27)
These look free and are not. Copying from them into our tree is High severity.
- **Lygia** shader library — Prosperity/Patron, **NON-COMMERCIAL** (30-day commercial trial). Several
  popular R3F transition tutorials are built on it, so it arrives indirectly. Read-only reference.
- **Shadertoy** shaders — default **CC BY-NC-SA 3.0** unless the author says otherwise. Never paste;
  re-implement from the technique, not the source.
- **EOX Sentinel-2 cloudless (2016)** — **CC BY-SA** (not CC BY). Baking it into a globe texture makes
  an adaptation that must be shared alike: a copyleft trap inside a proprietary white-label product.
  All free EOX tiers are unusable for us; the paid tier still forces visible EOX attribution on every
  tenant page.
- **Google Earth Studio** — hard NO. Its Geo Guidelines explicitly prohibit e.g. "a real estate company
  showing where their properties are located in a company video" — directly analogous to a travel
  agency showing a destination.
- **GSAP 3.15+** — commercially free since 2025-04-30 but proprietary (Webflow). Its *Prohibited Uses*
  names tools that "allow users to build visual animations without code". Our scene-plan editor is
  almost certainly outside that intent, but keep GSAP to HERO/experiential surfaces and prefer
  `motion` (MIT) inside the editor; record the call in an ADR if the editor ever grows animation
  authoring. (User cleared GSAP for use 2026-07-27 — this is scope hygiene, not a blocker.)
- **CLEAN / verified usable**: `gl-transitions` (audited: 123 MIT, 1 BSD-3, 1 BSD-2, zero copyleft —
  GitHub's `NOASSERTION` is a false alarm); three.js's own examples (MIT); NASA imagery (prefer over
  Solar System Scope, whose CC BY attribution would travel to every tenant page);
  Sentinel-2 via `s3://sentinel-cogs` (free, commercial-OK, not requester-pays) with the credit line
  "Contains modified Copernicus Sentinel data <year>".

## Repo hygiene
- Never commit .env, keys, tokens; secret-scanner + guard-secrets hooks enforce.
- Dependencies: pnpm audit before release; new deps get one-line justification in PR.
- CI: PR workflows get NO secrets (byaan github-actions-hardening pattern); privileged workflows
  only on main.
- Containers: non-root USER, pinned base images in prod.

Severity vocab per rules/orchestration.md#severity. Hardcoded secret found = raise to user, never
"fix" silently.
