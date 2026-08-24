---
name: motion-design
description: Premium web motion — GSAP + Framer Motion, scroll-driven reveals, page/scene transitions, easing language, and the functional-vs-experiential motion rules. Read before any animation/transition work.
---

# Motion design

Stack: **Framer Motion** (component/layout/state transitions, gestures) + **GSAP** (timeline/scroll
choreography, the heavier hero sequences). Deep patterns enriched via /phase-research 2.

## Two motion registers (per rules/design.md)
- **Functional** (state/progress/feedback): subtle, 150-300ms, ease-out; communicates, never decorates. Framer Motion `AnimatePresence`/`layout` for state + list changes; announce long jobs via aria-live (not motion alone).
- **Experiential** (hero, storytelling): richer, cinematic — the Earth fly-to, scroll reveals, section transitions. GSAP timelines / ScrollTrigger. Still intentional + performant, never jank or churn.

## Craft rules
- One coherent easing language (e.g. a custom cubic-bezier for entrances, a snappier one for exits); define easings as tokens, reuse.
- Stagger reveals (60-120ms) for lists/grids; entrance = fade + small translate/scale, ONE movement per element (mirrors the video typography rule).
- Transitions have intent: motion should map to spatial/logical relationships (where a thing comes from), not random.
- 60fps: animate transform + opacity only (GPU-friendly); avoid animating layout/box-shadow/filter on large areas; `will-change` sparingly.
- Scroll: prefer transform-based; clean up ScrollTrigger/listeners on unmount.

## Accessibility (blocking)
- Honor `prefers-reduced-motion` everywhere: swap experiential motion for instant/opacity-only, disable autoplay/parallax/looping. Provide a real static state, not a frozen mid-animation.
- Never gate meaning on motion; focus order + aria-live carry state for reduced-motion + AT users.

Anti-Patterns: decorative churn; animating layout/shadow on big surfaces; motion with no reduced-motion fallback; inconsistent ad-hoc easings; parallax that fights scroll; relying on animation to convey status.
Cross-References: webgl-3d skill, earth-flyto skill, product-ui skill, rules/design.md (Motion), .claude/agents/motion-3d-engineer.md.
