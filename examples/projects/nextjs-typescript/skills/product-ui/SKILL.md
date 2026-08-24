---
name: product-ui
description: The tour-build-flow app UI — upload, the pipeline states, aria-live progress, the scene-plan editor, and the signed-sources player embed, in premium light mode. Read before building any apps/web product surface.
---

# Product UI (tour-build flow)

The functional app surface premium-web-design deliberately excludes (it targets marketing sites). This
skill operationalizes rules/design.md's "every async surface has designed states" for THIS flow.
Premium LIGHT mode; consumes the shipped design tokens (ui-designer owns them, task 0013).

## The build flow (map every state)
`upload -> parsing -> queued -> planning -> fetching -> plan_ready (review/edit) -> voicing ->
assembling -> rendering -> judging -> done | failed`.
**The human pause is AFTER fetch** (docs/adr/0008 D3): the plan is only released once its footage is
cached, so a reviewer never edits a plan whose clips do not exist. `failed` is terminal from ANY stage,
not a step in the order.
- `upload` + `parsing` are trip-level (`trips.status = ingesting`); everything from `queued` onward is a
  literal `RenderStatus` from `@vt/core`. The UI's ordered copy lives in `apps/web/app/lib/pipeline.ts`
  (`FLOW`, `FAILED`) — extend that, don't restate it. Drift is a typecheck failure in BOTH directions:
  `FlowStage` catches a removed/misspelt status, and the coverage assertion at the bottom of that file
  fails the build (naming the status) when one is ADDED to `@vt/core` without a UI step. Adding a status
  therefore means adding a step here in the same change.
- `FlowStep.human` marks the two stages that wait on a PERSON — `upload` and `plan_ready`. Use it to
  place a review affordance; it is not "this row is interactive". `done` is not `human`: the run waits
  on nobody there.
- Each is a **designed** state — empty, loading, error, success — no raw spinners, no layout jumps.
- **Upload:** drag/drop + paste (text/PDF/image); designed empty/hover/uploading/error/success; clear
  affordance + constraints (25MB, types). Keyboard-operable.
- **Progress:** poll the render status (see the API); render a designed state per stage; announce
  changes via **aria-live** (accessibility gate); failure surfaces the judge issues, not a stack trace.
- **plan_ready editor:** review the AI scene plan with a **live-synced @remotion/player preview** (edit
  narration/text/timing/order -> preview updates without a re-render round-trip); a dual mode
  (accept AI plan vs edit manually); **Approve** triggers the render. See the scene-plan-editor task.
- **Preview:** @remotion/player fed the REAL ScenePlan with footage from **OUR signed storage URLs**
  (never FootageRef.url — SSRF-inert); null-footage scenes fall back to the tinted placeholder.
- **Ready:** a working signed download of the MP4; failed state surfaces judge score/issues.

## What already exists — reuse it, don't rebuild it
Shipped in task 0013 (`apps/web`):
- `app/styles/tokens.css` — the single token source. `app/README-tokens.md` documents the tenant
  override surface. `pnpm --filter web verify:contrast` re-measures every AA pair.
- `app/components/states.tsx` — `EmptyState`, `LoadingState` (progress rail + stage ledger +
  `role="status" aria-live="polite"`), `ErrorState` (issue list), `SuccessState` (receipt). One frame,
  four dressings: swapping between them does not move the layout.
- `app/components/ui.tsx` — `Button`, `ButtonLink`, `Panel`, `StatusPill`, `Eyebrow`, `Meta`,
  `SectionHeader`, `ActionRow`, `Seam`. `app/components/icons.tsx` — hairline SVG set (no emoji, no
  icon library). `app/components/shell.tsx` — masthead, skip link, `#main`, colophon.
- `/styleguide` — live specimen of every token plus the four states. Check it before inventing a value.

## Token names (use these; never a raw hex or magic px)
- Grounds: `--vt-surface-page` (warm paper) `-raised` `-sunken` `-inverse`
- Ink: `--vt-text-strong` `--vt-text` `--vt-text-muted` `--vt-text-subtle` `--vt-text-on-accent`
  `--vt-text-on-inverse` `--vt-text-on-inverse-muted`
- Lines: `--vt-border-control` (the only one rated for interactive boundaries, >=3:1)
  `--vt-graphic-line` `--vt-border-strong` `--vt-border-hairline`
- Brand: `--vt-accent` `-strong` `-soft` `-line` `-on-inverse`; `--vt-secondary` + the same suffixes
- States: `--vt-success|warn|danger|info` + `-strong` `-soft` `-line`
- Type: `--vt-font-display|sans|mono`; sizes `--vt-text-micro|fine|body|lead|title|headline|display|hero`;
  `--vt-leading-*`, `--vt-tracking-*`, `--vt-measure` (68ch)
- Space `--vt-space-1..32` (4px grid) · radii `--vt-radius-xs|sm|md|lg|pill` ·
  elevation `--vt-shadow-flat|raised|lifted|floating|inset` · layers `--vt-z-*`
- Motion `--vt-duration-fast|base|slow` (150/220/300ms), `--vt-stagger`,
  `--vt-ease-standard|entrance|exit|emphasis`. Use ONLY these durations: the
  `prefers-reduced-motion` block in tokens.css zeroes them, which is how the whole app degrades.
  A looping animation must ALSO define its own designed still under that query.

## Craft
- Tokens only (no raw hex); premium light (warm paper, editorial type, soft-shadow depth) per design.md.
- Motion via motion-design (functional register for state changes); the hero uses earth-flyto/webgl-3d.
- Responsive + usable at 390px and 1440px; WCAG AA; visible focus; long jobs announced.
- Every async surface: empty + loading + error + success designed; optimistic where safe; no dead ends.
- Review with `pnpm --filter web build && pnpm --filter web screenshot` (local only, writes gitignored
  PNGs at 390/1440 incl. a reduced-motion pass). Attach them to the VERIFY handoff.

## Data / boundaries
- The dev-tenant header (x-tenant-id) until Phase-4 auth; all fetches go through the app's API client.
- Never load an origin CDN/footage URL directly in the browser — only signed storage URLs from the API.

Anti-Patterns: raw spinners with no context; undesigned error/empty states; layout jumps on state change;
status conveyed by motion alone; loading FootageRef.url directly; ad-hoc colors; a build flow that dead-ends;
restating the stage list instead of importing `FLOW`; hardcoding a duration instead of a motion token.
Cross-References: premium-web-design, motion-design, webgl-3d, earth-flyto skills; rules/design.md;
apps/web/app/README-tokens.md; .claude/agents/{ui-designer,frontend-engineer,motion-3d-engineer}.md.
