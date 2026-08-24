---
name: memory-audit
description: Audit and prune auto-memory entries to prevent bloat. Invoke when user types /memory-audit, asks to "clean memory" / "review memory" / "what does Claude remember", or when MEMORY.md is reported >200 lines by the session-start hook.
allowed-tools: Read, Edit, Write, Bash
---

# /memory-audit

Find stale, redundant, or oversized auto-memory entries and propose pruning. **Do not delete anything without user approval.**

## Procedure

1. **Locate memory dirs:**
   ```bash
   find $HOME/.claude/projects -name 'MEMORY.md' -exec du -h {} \;
   ```

2. **For each `MEMORY.md` > 150 lines OR each project memory dir > 100 KB:**
   - Read MEMORY.md
   - List all topic files in same dir
   - Identify candidates for pruning:
     - **Stale**: references files/branches/issues that no longer exist (verify with `git`/`ls`)
     - **Obsolete**: snapshot-style facts >30 days old (workstation state, "as of <date>")
     - **Duplicates**: two entries covering same topic — consolidate
     - **Trivia**: facts derivable from `git log` / current code (delete; not real memory)
     - **Wrong type**: ephemeral session notes saved as user/project memory — delete

3. **Report findings as a table:**
   | File | Lines | Status | Suggested action |
   |------|-------|--------|------------------|
   | foo.md | 45 | references deleted branch `feat-x` | DELETE |
   | bar.md | 90 | duplicates baz.md | MERGE into baz.md |
   | qux.md | 120 | still relevant | KEEP |

4. **Wait for user approval** before any Edit/delete

5. **After approval:**
   - Update individual topic files
   - Update `MEMORY.md` index to drop dead links
   - Re-run size check, report new sizes

## Anti-bloat rules to enforce
- MEMORY.md index: ≤200 lines, ≤150 chars per line
- Topic files: ≤80 lines each
- No prose paragraphs — only structured bullets / tables
- Every entry needs a "Why this is still relevant" justification or it's pruned
