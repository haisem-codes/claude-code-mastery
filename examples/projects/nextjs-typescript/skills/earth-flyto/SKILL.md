---
name: earth-flyto
description: The signature Google-Earth-style fly-to hero — a 3D globe flies from origin to destination then dissolves into the real scene image/footage. Read before building the hero.
---

# Earth fly-to hero

The signature experience (user direction 2026-07-22): a premium 3D Earth flies from the user's
home/origin to the trip destination, then **transitions into the actual destination image/footage** —
like Google Earth zooming into a place. Owned by motion-3d-engineer; uses webgl-3d + motion-design.

## The sequence
1. **Establish:** a premium 3D globe (see webgl-3d) at rest, warm/light grade, origin marked.
2. **Fly:** animate the camera along an arc from origin (lat/long) to destination (lat/long) with
   cinematic easing (GSAP timeline) — accelerate, cruise, decelerate; the globe rotates under it.
3. **Approach:** as the camera nears the destination, zoom/tilt toward the surface.
4. **Dissolve:** cross-fade / match-cut from the 3D surface into the **destination image or footage**
   (the auto-fetched premium picture, or the first scene's clip) — a seamless hand-off from map to place.
5. **Land:** settle on the destination hero (image/footage + title), then reveal the build flow.

## Data
- Geocode origin + destination (destination from the Trip; origin from a sensible default/user input) to
  lat/long. Use a lightweight geocoder or a bundled city dataset — decide per the scout report; do NOT
  fetch an attacker-controlled URL (SSRF), only an allowlisted geocode API/dataset.
- The destination image comes from the destination-image-fetch feature (premium picture fetched when the
  user provides none) — served from OUR storage (signed URL), never a raw origin CDN link (SSRF-inert).

## Guardrails
- **Reduced-motion:** skip the globe animation entirely -> show the static premium destination hero
  (image + title). The fly-to is enhancement, never required.
- **Performance:** the globe follows webgl-3d perf rules (dispose, DPR cap, demand frameloop, lazy load);
  the hero must not block first paint — poster first, globe hydrates after.
- **Halal:** any audio under the sequence follows audio-design (no instrumental music); default silent.
- **Taste:** cinematic, not gimmicky; one deliberate journey, premium light grade throughout.

Anti-Patterns: janky/heavy globe blocking load; a hard cut instead of a considered map->place transition;
no reduced-motion fallback; geocoding/imagery from unvalidated URLs; spinning-globe cliche with no purpose.
Cross-References: webgl-3d, motion-design, product-ui skills; rules/design.md (Motion signature); the
destination-image-fetch task; .claude/agents/motion-3d-engineer.md.
