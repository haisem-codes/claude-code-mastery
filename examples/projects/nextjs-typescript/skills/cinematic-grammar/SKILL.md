---
name: cinematic-grammar
description: How to turn a structured trip into a cinematic scene plan — story arc, shot grammar, pacing, typography, grading, curation rubric. Read before any scene-planning, template, or footage work.
---

# Cinematic grammar for tour videos

## Story arc (every video, scaled to the trip)
`roadmap -> [chapter blocks] -> peak? -> finale` (ADR-0010 D2). The client already chose and paid
for this trip: the video shows them THEIR itinerary, so orientation comes before atmosphere.
- roadmap: the whole plan of the tour — title, scale line, chapter list, empty timeline — over
  strong destination footage. 4.5-6s. **Scene 1 always. There is no hook before it.** Poster frame.
- chapter block, one per day-chapter, in day order:
  - chapter marker: "DAYS 1-3" over "Tokyo", timeline advanced. 3-4.5s. First scene of its block.
  - beat scenes: one per real itinerary activity, bound via `scene.beat` (day, timeOfDay, activity,
    location). Beats ride on establishing/movement/people/peak — never on `detail`.
  - breathing scenes: `detail`, `beat: null`, no text, a texture close-up between beats.
- peak: emotional apex. 4-6s. In the spine suffix or inside the strongest chapter, never both.
- finale: branded outro + title + CTA. 4-5s. A spine scene — `chapterId` and `beat` both null.
`hook` is still a legal type mid-arc; it is simply no longer the opener.

Spine scenes (`chapterId === null`) may appear only as a prefix and/or a suffix. The chapter region
in the middle is uninterrupted.

## Shot grammar table
| type | content | duration | motion |
|------|---------|----------|--------|
| roadmap | destination hero/aerial + the plan card | 4.5-6s | slow |
| chapter | wide establishing of the chapter's location + marker card | 3-4.5s | slow push or static |
| hook | aerial/drone wide (mid-arc only) | 2.5-4s | fast reveal |
| establishing | skyline/landmark wide | 3-5s | slow push or static |
| detail | texture close-up: food, hands, fabric, water | 2-3s | subtle drift |
| movement | walking POV, vehicle, crowd flow | 3-4s | native motion |
| people | candid medium shots, families | 2.5-4s | static/handheld |
| peak | golden-hour wide | 4-6s | slow |
| finale | calm wide + title card | 4-5s | settle to still |

Both structural types carry footage like any other scene — cards OVER a clip with a heavy scrim,
never flat graphics. Any scene rendering a derived marker (`roadmap`, `chapter`, or `beat != null`)
holds >= 3s, whatever its own type band says.

## Pacing
- Duration is DERIVED per trip, not chosen from a menu (ADR-0010 D12); the schema's 20-300s bound is
  a sanity rail, not a product tier. Scene count scales with it: 8-10 at 30s, 14-18 at 60s, 20-26 at
  90s, linear in between.
- **Chapter-count band is keyed to the trip's DAY COUNT**, not the package length. A chapter spans
  at most ~4 days (so >= `ceil(days/4)` chapters) and the roadmap card lists at most 7 rows (so
  <= `min(days, 7)`). On a long trip the two cross and roadmap readability wins.
- Chapters PARTITION days `[1..N]`: sorted, contiguous, no gaps, no overlaps. A day is never
  dropped — widen a span instead. Repeated/degenerate days collapse into one wide chapter.
- Cut rhythm: chapter cards steady, beats medium (3-4s), peak/finale slow (4-6s).
- Prefer varying shot type within a chapter, but two same-type beats in a row is legal when the
  itinerary calls for it — it is a flag, not a block. Never two clips from the same source video.
- Cuts land on SFX accents (see audio-design); max 1 accent per 2 cuts; accents only on
  roadmap/peak/finale — a chapter card is carried by the ambience change, not a hit.

## Footage curation rubric (fetch stage ranks by this, in order)
0. Two rungs per scene (ADR-0010 D6). `query` names the activity at its place at its time of day
   ("Trevi Fountain Rome evening crowd walking"); `fallbackQuery` drops the activity and keeps
   location + shot type + light ("Rome street evening"). Light words: morning -> sunrise/morning
   light, midday -> midday, afternoon -> afternoon, evening -> golden hour/evening, night -> night,
   unspecified -> omitted. A scene filled from its fallback depicts the PLACE, not the activity its
   heading names — that is recorded, never silent.
1. Relevance: exact landmark > named city > region > country > generic theme match.
2. Technical: >=1080p (prefer 4K), no watermark/logo/text burn-in, neutral gradeable exposure, correct aspect.
3. Content fit: family-friendly filter — exclude clips centered on alcohol, nightlife/club scenes, or immodest content; prefer nature, architecture, food, culture, families.
4. Motion quality: stable or intentionally moving; no shaky amateur pans.
5. Diversity: penalize clips visually similar to already-selected scenes.

## Typography on footage
Max 2 typefaces per video. Hold >= 2.5s. 10% safe margins. One entrance movement per element, no
perpetual animation. Text never over faces or the frame's focal point.
**Itinerary text is DERIVED, never authored** (ADR-0010 D3): the composition builds the eyebrow and
heading from `scene.beat` and `plan.chapters`. A scene carries at most ONE text group — one eyebrow
(<= 5 words, uppercase, tracked) plus one heading (1-6 words) — behind ONE shared scrim plate. The
pair counts as a single element for "one movement per element". `texts` holds authored editorial
copy only: exactly one title on the roadmap, 1-2 overlays on the finale, and nothing on any scene
that renders a derived marker.

## Grading
One LUT family per video, chosen from destination character: warm (heritage/desert/food),
teal-orange (coast/city), cool (mountain/nordic). Applied in composition, recorded per scene in
ScenePlan.scenes[].gradeLut.

## Pre-render checklist (cinematic-director verdict gate)
- [ ] Arc complete: scene 1 is `roadmap`, last is `finale`, no scene before the roadmap
- [ ] Chapters partition the trip's days `[1..N]`; the count is inside the day-count band
- [ ] Every chapter has its marker card first, at least one more scene, and at least one beat
- [ ] Every beat's day sits inside its chapter's span and comes from the real itinerary
- [ ] Text ownership holds: nothing authored on a marker or beat scene; roadmap has one title
- [ ] Shot-type variety is sane; durations within type ranges; markers >= 3s
- [ ] Every scene has both query rungs; all clips pass the curation rubric; licenses recorded
- [ ] Typography and grading rules hold (one LUT family across the whole video, no exceptions)
- [ ] Audio plan conforms to audio-design skill

Anti-Patterns: generic b-roll padding; text walls; same-y drone-only videos; ignoring trip data
in favor of pretty-but-irrelevant clips; melodic audio of any kind; **a postcard reel — footage
that never says what the client will do, where, or on which day**; **inventing an activity the
itinerary does not name** (a factual claim to a paying client, Critical severity); a per-region LUT
on a multi-city trip.
Cross-References: audio-design skill, rules/design.md video section, video-judge agent rubric.
