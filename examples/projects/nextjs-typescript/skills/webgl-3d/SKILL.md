---
name: webgl-3d
description: Premium 3D in the web app — React Three Fiber + drei + Three.js patterns, the 3D globe, camera fly-to, and WebGL performance/accessibility. Read before any 3D/WebGL/canvas work.
---

# WebGL / 3D

Stack: **React Three Fiber (R3F)** + **@react-three/drei** + Three.js, inside Next.js 15 (App Router).
Deep references enriched via /phase-research 2 (three-globe / react-globe.gl / cobe, drei helpers).

## Setup rules
- 3D is **client-only**: wrap the `<Canvas>` in a `"use client"` component and `dynamic(import, { ssr: false })`. Never SSR WebGL.
- Gate assets behind `<Suspense>`; show a premium static poster/skeleton while loading.
- One `<Canvas>` per hero/scene; reuse via context — don't mount many canvases.
- Consume design tokens for any color/material tint; no hardcoded hex.

## The 3D globe (Earth fly-to backbone — see earth-flyto skill)
- Prefer a lightweight globe (cobe = tiny/no-three, or three-globe/react-globe.gl for richer control). Pick per weight vs control; the scout report recommends.
- Camera fly = animate camera position/target along an arc between two lat/long points with cinematic easing (see motion-design). End framed on the destination, then hand off to the image/footage transition.

## Performance (a gate, not a nicety)
- Dispose geometries, materials, textures on unmount (drei `<Detailed>`/manual `.dispose()`); leaks kill long sessions.
- Cap `dpr={[1, 2]}`; throttle/`frameloop="demand"` when idle; pause the loop when the canvas is offscreen (IntersectionObserver).
- Lazy-load textures/models; compress (ktx2/draco where it fits); budget for mid-tier laptops + phones.
- Measure: no dropped frames on a 4-year-old laptop; no growing memory across route changes.

## Accessibility
- `prefers-reduced-motion` -> render a static premium frame (no animation, no autoplay spin), never a blank canvas.
- 3D is decorative/experiential: the product is fully usable with WebGL disabled/failed — always provide the 2D fallback.

Anti-Patterns: SSR-ing the canvas; many canvases; undisposed resources; uncapped DPR; motion with no reduced-motion path; hardcoded colors; blocking first paint on a heavy model.
Cross-References: earth-flyto skill, motion-design skill, product-ui skill, rules/design.md (Motion: experiential), .claude/agents/motion-3d-engineer.md.
