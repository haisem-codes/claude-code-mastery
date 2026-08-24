# Design standard — what "beautiful" means here, concretely

The bar for every UI surface and every rendered video. `frontend-engineer` implements UI against
this file; `remotion-engineer` implements video compositions against it. `code-reviewer` judges
UI diffs; `video-judge` judges rendered video output. Subjective taste doesn't pass gates — these
checkboxes do.

## Direction
- One deliberate visual identity, defined once (tokens: color, type scale, spacing, radii,
  shadows, motion) in `apps/web` and consumed everywhere. No ad-hoc values.
- **House aesthetic = premium LIGHT mode** (user decision 2026-07-22): warm off-white/paper grounds,
  editorial type, real depth via soft shadows + hairline borders — a considered, expensive light
  identity (think Aesop / Stripe / editorial), NOT the generic bright-white SaaS look. Bring
  product-designer craft (design tokens, type scale, hierarchy, spacing rhythm); lean on the
  product-UI / tour-build-flow skill + premium-web-design.
- **No generic-AI defaults**: no stock Inter-on-white, no purple-gradient hero, no unstyled
  component-library look, no emoji-as-icons. The app should be recognizable at a glance. Light mode
  here means a deliberate premium light palette, never flat #fff with a default sans.
- Typography does the heavy lifting: a real type scale (e.g. 1.25 ratio), tight heading
  tracking, comfortable reading measure (60-75ch) for body copy.

## Copy voice (blocking, user decision 2026-07-29)
- **NO EM DASHES in any user-facing text.** Not in UI copy, error messages, aria-live
  announcements, page titles, placeholders, marketing prose, on-screen video text, or LLM-authored
  narration and titles. The em dash is the single strongest tell that a machine wrote the sentence,
  and this product is sold to agencies as considered work. Use a comma, a colon, a full stop, or
  split the sentence. If a sentence only works with an em dash, it is the wrong sentence.
- Applies to what a human reads, so code comments and internal docs are exempt. A standalone
  typographic glyph for a missing value in a table or receipt is not prose and is exempt too.
- Owners: `frontend-engineer` and `ui-designer` for the app; `cinematic-director` for the plan
  prompt (it must forbid em dashes in the titles and narration the model authors, since that text
  reaches the screen); `remotion-engineer` for anything a composition renders.
- `code-reviewer` treats a new em dash in user-facing copy as a blocking finding.

## Layout & states
- Spacing on a 4/8px grid; alignment is intentional, not incidental.
- Every async surface has designed **empty, loading, error, and success states** — the
  tour-build flow especially: upload → parsing → planning → fetching footage → rendering →
  ready. No raw spinners with no context, no layout jumps.
- Responsive: usable at 390px and 1440px. Keyboard-operable throughout.

## Accessibility (blocking)
- WCAG 2.1 AA contrast for text and interactive elements.
- Focus states visible; controls labelled; long-running job status announced (aria-live).

## Motion
- **Functional motion** (state transitions, progress, feedback): subtle + purposeful, 150–300ms,
  respects `prefers-reduced-motion`. Never decorative churn.
- **Experiential / signature motion** (hero, storytelling surfaces — user direction 2026-07-22): the
  site is deliberately rich with **premium 3D + motion** (Three.js / React Three Fiber; GSAP / Framer
  Motion; scroll-driven reveals; page/scene transitions). Richer than functional motion, but still
  intentional, performant (dispose GPU resources, cap DPR, lazy-load 3D, no jank on mid-tier hardware),
  and **fully degraded under `prefers-reduced-motion`** to a tasteful static premium state — motion is
  never required to use or understand the product.
- **Signature: the Earth fly-to hero.** A premium 3D globe flies from the user's home/origin to the
  destination, then transitions/dissolves into the actual destination image/footage (Google-Earth-like
  zoom-into-place). Owned by `motion-3d-engineer`; see the `earth-flyto` + `webgl-3d` skills. Reduced-
  motion fallback: a static premium destination hero, no globe animation.

## Video output design (applies to packages/video)
The video's job is to communicate the client's own itinerary, not to sell a destination they have
already paid for. Structure is the product; atmosphere is the wrapper (ADR-0010).
- Compositions are data-driven: props = ScenePlan from @vt/core only; zero hardcoded trip content
- **Itinerary markers are DERIVED from ScenePlan data, never authored free text.** The composition
  builds `DAY 2 · EVENING` / `Trevi Fountain` from `scene.beat`, and `DAYS 1-3` / `Tokyo` from
  `plan.chapters` — the model never writes them into `texts`. One source of truth: a human edits the
  fact, the pixels follow.
- Typography on footage: max 2 typefaces/video, hold >= 2.5s, 10% safe margins, one movement per
  text element.
- **A scene carries at most ONE text group, never two.** A group is at most one eyebrow (<= 5 words,
  uppercase, tracked) plus one heading (1-6 words). The eyebrow+heading pair counts as a single
  element for "one movement per text element": one shared fade-and-rise, eyebrow leading the heading
  by <= 4 frames, then static. (Replaces the old "titles 3-6 words", which was written for a montage
  title card and wrongly flagged legitimate one-word destination names.)
- **One shared plate per group, not one per line.** Scrim is mandatory, not optional: a single
  gradient sized to the pair's bounding box, inside the 10% safe margins.
- Grading: one LUT family per video (warm | teal-orange | cool), set in ScenePlan.scenes[].gradeLut
- Motion: cuts on SFX accents; no scene shorter than 2s or longer than 8s (schema enforces); a scene
  rendering a derived marker holds >= 3s

## Whitelabel theming (Phase 4-ready)
- All UI colors/type/radii via CSS custom properties from a single tokens file; no raw hex in
  components. Tenant brand kit later overrides tokens only — components never change per tenant.

## Gate verdicts
`code-reviewer` emits PASS / CHANGES-REQUESTED on UI diffs; `video-judge` emits a score + issues
on rendered output. Findings follow the handoff format per rules/orchestration.md#handoff-format
and the severity vocabulary per rules/orchestration.md#severity. Violations of Accessibility or
"no generic defaults" are severity >= High. When the app runs, judge UI from Playwright
screenshots (key states, 390px + 1440px), not from code alone.
