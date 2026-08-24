---
name: research-scan
description: Manually scan recent (~last 3 years) research papers on a topic and extract leverage-able material for Aegis. Triggers the research-scout agent.
argument-hint: <topic> (default - LLM-based vulnerability detection + static/taint analysis)
---

# /research-scan $ARGUMENTS

Dispatch the `research-scout` agent to survey **recent (last ~3 years)** academic papers on **$ARGUMENTS**
(default: LLM-based vulnerability detection + static/taint analysis) and extract concrete, leverage-able
material for Aegis.

Instruct it to: find papers on open venues (arXiv / USENIX / ACL / OpenReview), read the HTML versions,
extract per paper `{core idea · what's leverage-able · how we'd apply it · results + caveats · confidence}`,
synthesise a value-to-effort-ranked **try / adopt / watch** list tied to our wedge (deep + verified, low FP),
and save the report under `docs/research/papers/` (citing every claim). Then summarise the top findings for me.
