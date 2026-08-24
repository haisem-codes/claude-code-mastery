---
name: audio-design
description: The halal audio identity — modes, layers, mix levels, the recitation adab rules, TTS stack, and audio sourcing/licensing. Read before any audio, TTS, scene-audio-cue, or pack work. The no-instrumental-music rule is absolute.
---

# Audio design

Full design: docs/superpowers/specs/2026-07-21-audio-identity-design.md. Sourcing + licensing detail:
research/reports/audio-sourcing.md. This skill is the operating rulebook.

## Hard rule
No instrumental music. No melodies. Ever, in anything WE generate, curate, or supply — including
samples, fixtures, tests, demos, and every shipped audio-pack clip. Allowed in our content = natural
ambience, non-melodic sound-design accents (noise-based whoosh/riser/impact), the human voice (TTS
narration + a-cappella vocal). Any melodic/instrumental content in OUR content = automatic fail
(video-judge scores it 0).
**Exception — user-uploaded custom audio (BYOA):** a user may upload their OWN background audio track
(see Custom audio below). That is the user's own content used at their discretion and rights; the
no-music rule polices what WE produce, not what a user brings. video-judge does not score BYOA content
for the music rule, but still checks levels/mix.

## Layers (building blocks)
| Layer | Content | Basis |
|-------|---------|-------|
| L1 ambience bed | scene soundscapes by ambienceTags | natural sound |
| L2 accents | whoosh/riser/impact on cuts, noise-based | synth SFX |
| L3 voice | narration: generated script OR user transcript, via pluggable TTS; or off | human/TTS voice |
| L4 vocal-energy | a-cappella vocal percussion / beatbox / vocal pads (human voice only, no instruments) | human voice |

## Modes (presets that combine layers)
| Mode | Recipe | Feel |
|------|--------|------|
| Ambient (default) | L1 + sparse L2 + optional L3 | cinematic-trailer |
| Narrated | L3-forward + low L1 + minimal L2 | documentary; custom transcript shines |
| Vocal-energy | L1 + L4 + optional L3 | lively, the halal alternative to a music bed |
| Custom | user-uploaded background track (+ optional L2/L3) | user's own audio, their choice |

## Mix levels (integrated LUFS)
bed -28 (crossfade 500ms, no silent gaps) · accents -20 peak (max 1 per 2 cuts; no pitched sweep
resolving to a note) · voice -16 (bed ducks -6dB under VO, 200ms attack / 500ms release) ·
vocal L4 -20. Master -14 LUFS, true peak <= -1dBTP, no clipping. One master calm<->energetic dial
scales accent density + bed level + cut-timing bias. Mix is a pure function of the ScenePlan audio
fields (deterministic, re-mixable).

## Scene -> ambience mapping (L1 bed by ambienceTags; canonical tag set — must match the plan prompt/reviewer)
Canonical tags: coast, city, market, souk, mountain, desert, garden, park, night, heritage-interior, rain, snow.
coast: waves + distant gulls | city: street murmur + footsteps | market, souk: crowd + vendor calls
mountain: wind + birdsong | desert: low wind | garden, park: birdsong + leaves | night: crickets
heritage-interior: reverberant room tone | rain: rain on surfaces | snow: muffled wind

## Voice / TTS
English only at launch. Pluggable provider abstraction (mirror @vt/core/providers): default
**kokoro** (Apache-2.0, local, CPU-ok) -> **elevenlabs** / **azure|google** premium. Never PlayHT
(defunct), Coqui XTTS (no commercial license), or unofficial Edge-TTS (ToS-gray).
Custom transcript is a first-class field (per-scene or whole-video); falls back to the generated
script when empty. Script tone: warm, concrete, second person ("you'll wander...", not "one can
observe"). Max 14 words per scene-visible sentence; silence is fine — do not narrate every scene.

## Custom audio (bring-your-own — BYOA)
User uploads their own background audio file; it becomes the bed/background for the video (with level
+ ducking-under-VO control). This is the customization escape hatch and the user's own content.
- Accepted: mp3 / wav / m4a / ogg. Magic-byte sniff + size cap; hostile-upload safety (reuse the
  ingest upload patterns — validate at the boundary, store under tenant/{tenantId}/uploads/, no local
  decode of untrusted bytes beyond a header sniff). Recorded as `license: "user-provided"`.
- The user warrants they hold the rights and that the content is appropriate — a clear acknowledgement
  at upload. We do not police BYOA for the music rule; that is the user's choice.
- Stored as a reusable per-tenant asset OR a per-video upload; selectable as the "Custom" mode source.

## Recitation — NOT offered as a built-in feature (user decision 2026-07-21)
Dropped: no off-the-shelf source grants clean commercial white-label rights, and adab guidance cautions
against recitation over generic tour footage. We do not source, host, or ship recitation. A user who
has their OWN licensed recitation may use it via BYOA at their sole discretion and responsibility
(including the adab/attribution considerations) — we neither provide nor endorse specific recitation
content. See research/reports/audio-sourcing.md §4 for the licensing/adab background.

## Settings (pre + post generation)
Pre-gen (tenant default -> per-video override): mode, ambience intensity, accent density, voice
on/off + provider + voice, custom transcript, pack, custom-audio upload (BYOA), master feel,
language. Post-gen: audio is data
in the ScenePlan, so editing re-runs only mix + mux (footage cached) — per-scene editor (swap
ambience, mute accent, replace VO line, levels) + "re-render audio". No re-fetch, no re-plan.

## Sourcing & licensing (the two-hop white-label chain: us -> agency -> their client)
"Commercial OK" is necessary but not sufficient — need explicit redistribution/sublicensing rights or
CC0/owned content. Backbone = what we control: curated **Freesound-CC0 + Pixabay** (ambience/SFX) and a
**commissioned custom vocal pack** (full buyout, white-label chain named in contract). Scale add-ons
under negotiated terms: **Epidemic Sound Partner API** (SFX). NOT usable: Zapsplat/Uppbeat/Mixkit/
consumer tiers; nasheed libs (use *daf* = a drum, and non-transferable licenses). Every shipped clip
records `license` + `sourceUrl`; unlicensed audio never renders (footage-provenance gate,
rules/security.md). Legal review of the final mix is a launch gate.

## Audio pack shape
assets/audio-packs/<pack-id>/manifest.json: { "id","name","strictness":"ambience-only"|"standard"|
"with-vocals", "clips":[{"file","type":"bed"|"accent"|"vocal","sceneTags":[],"license","sourceUrl"}] }.
Default pack strictness "standard"; tenant may set stricter and the pipeline must honor it.

Anti-Patterns: background "royalty-free music"; melodic risers; wall-to-wall narration; accent spam
on every cut; unlicensed/unverified clips; wiring recitation to a non-commercial API; assuming a
single-hop license covers our resale chain.
Cross-References: cinematic-grammar skill, video-judge audio rubric, the audio-identity spec,
research/reports/audio-sourcing.md, rules/security.md (provenance).
