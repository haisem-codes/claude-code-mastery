# Design standard — what "beautiful" means here, concretely

The bar for every UI surface and the exported PDF. `ui-designer` sets direction in
`docs/design/`; the design-review gate judges against THIS list. Subjective taste doesn't
pass gates — these checkboxes do.

## Direction
- One deliberate visual identity, defined once in `docs/design/design-system.md` (tokens:
  color, type scale, spacing, radii, shadows, motion) and consumed everywhere. No ad-hoc values.
- **No generic-AI defaults**: no stock Inter/Roboto-on-white, no purple-gradient hero, no
  unstyled component-library look. The app should be recognizable at a glance.
- Typography does the heavy lifting: a real type scale (e.g. 1.25 ratio), tight heading
  tracking, comfortable reading measure (60–75ch) for notes text.

## Layout & states
- Spacing on a 4/8px grid; alignment is intentional, not incidental.
- Every async surface has designed **empty, loading, error, and success states** — the
  recording flow especially: idle → recording (live level/waveform + elapsed) → uploading →
  transcribing → structuring → done. No raw spinners with no context, no layout jumps.
- Responsive: usable at 360px and 1440px. Keyboard-operable throughout.

## Accessibility (blocking)
- WCAG 2.1 AA contrast for text and interactive elements.
- Focus states visible; controls labelled; recording state announced (aria-live).

## Motion
- Subtle and purposeful (state transitions, progress), 150–300ms, respects
  `prefers-reduced-motion`. Never decorative churn.

## The PDF is a designed artifact too — with its own identity
- Two sibling identities, one brand: the **app** is premium light (airy, refined, calm);
  the **PDF** is the handwritten-notebook style defined by the owner's samples
  (`docs/samples/*.pdf`, component inventory in `docs/design/pdf-reference.md`).
- PDF bar: judged side-by-side against the samples — sticky-note cards, callout bars,
  bilingual quote blocks (RTL Arabic rendered correctly), vocab grids, flow diagrams,
  takeaways; page furniture (header badge, footer, page numbers); print margins ≥18mm;
  `break-inside: avoid` on cards; no default-library look.
- Notes structure is visually distinct and scannable at flip-through speed.

## Gate verdicts
`design-reviewer` emits PASS / CHANGES-REQUESTED with findings per §4 of
`.claude/rules/orchestration.md`. Violations of Accessibility or "no generic defaults" are
severity ≥ High. When the app runs, judge from Playwright screenshots (key states, 360px +
1440px), not from code alone.
