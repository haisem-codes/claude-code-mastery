# Security standard — project specifics

Global `~/.claude/rules/security.md` applies. This adds what's specific to an app that
accepts user audio and renders PDFs. Applied by `security-auditor`; triggers in
`.claude/rules/orchestration.md` §2.

## Uploaded audio is hostile input
- Enforce size limit and an allowlist of audio MIME types/extensions **server-side**;
  sniff magic bytes, don't trust Content-Type.
- Store uploads under generated names (UUID) in a dedicated directory; never use
  client-supplied filenames in paths. Reject `..`, absolute paths, NUL bytes.
- Decode/probe via ffmpeg/ffprobe with argument lists (never shell=True), timeouts, and
  resource caps. Treat decoder crashes as expected input, not bugs.

## Pipeline
- Transcripts and LLM outputs are untrusted text: escape on render (React does; PDF
  templates must too — no raw HTML injection into the PDF renderer).
- Prompt-injection aware: lecture audio can contain adversarial instructions. The
  note-structuring prompt must scope the model to the transcript; never execute or fetch
  anything an LLM output asks for.
- `ANTHROPIC_API_KEY` and friends only via env / `.env` (git-ignored, `.env.example` shipped).

## API surface
- CORS restricted to the frontend origin — not `*`.
- Job/resource IDs are unguessable (UUIDv4); no sequential enumeration of other users' notes.
- Rate-limit upload and generation endpoints.
- Serve generated PDFs with `Content-Disposition: attachment` and a sane Content-Type.

## Housekeeping
- Uploaded audio and generated artifacts have a retention/cleanup policy (disk is finite;
  lectures are big).
- Dependency audits (`uv pip audit` in CI, `pnpm audit`) before release.
