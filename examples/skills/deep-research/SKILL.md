---
name: deep-research
description: Fan out parallel research across web search, official docs, and local code. Invoke when user types /deep-research, says "deeply research", "find the best", or asks a question requiring authoritative sources + community sentiment + cross-references.
allowed-tools: WebSearch, WebFetch, Read, Grep, Glob, Bash
---

# /deep-research

Run high-bandwidth research by launching multiple Agent calls in parallel.

## Procedure

1. **Clarify the question** if vague — one sentence back to the user confirming scope, or proceed if obvious

2. **Decompose into 2–4 parallel research lanes:**
   - Lane A: **Authoritative docs** — official documentation, API references, RFC/spec
   - Lane B: **Community signal** — Reddit, HackerNews, top-starred GitHub repos, blog posts from known practitioners
   - Lane C: **Local context** — if the user's repo has related code, grep for current patterns
   - Lane D: **Comparisons** — alternatives, pros/cons, recent benchmarks (only if user asked "which is best")

3. **Launch each lane as a parallel Agent call** (single message, multiple Agent tool uses, `subagent_type: general-purpose`). Prompt each one for:
   - Specific sources to consult
   - Word budget (e.g., "under 400 words")
   - Output format (bullets, link-heavy)

4. **Synthesize results into one output:**
   ```
   ## TL;DR (1–2 sentences)

   ## Findings
   - <bullet — link to source>
   - <bullet — link to source>

   ## Tradeoffs
   - <option A> vs <option B>: …

   ## Recommendation
   <opinionated pick + 1-sentence rationale>

   ## Sources consulted
   - <flat list of URLs>
   ```

## Discipline
- Do NOT echo subagent output verbatim — synthesize
- Drop low-signal results (StackOverflow answers >5 years old, content-farm SEO blogs)
- Cite ≥3 distinct sources per claim
- Flag disagreement between sources rather than picking arbitrarily
- If research takes >5 minutes, checkpoint with the user before continuing
