# Credits & Attribution

This repository curates, adapts, and builds upon work from multiple open-source projects. Full credit to the original authors.

## Source Projects

| Project | Author | License | What we sourced |
|---------|--------|---------|----------------|
| **claude-skills** | Alireza Rezvani | MIT | 171 enterprise skills across 9 domains (C-level, engineering, marketing, product, PM, compliance, business, finance), skill authoring standard, domain CLAUDE.md files |
| **anthropic-skills** | Anthropic | Proprietary (see LICENSE.txt in each skill) | 16 official skills: pdf, docx, xlsx, pptx, webapp-testing, skill-creator, brand-guidelines, canvas-design, frontend-design, mcp-builder, algorithmic-art, doc-coauthoring, internal-comms, slack-gif-creator, theme-factory, web-artifacts-builder |
| **claude-code-sub-agents** | SIO TOU LAI (Nelson) | MIT | 33 specialized subagent definitions organized by domain, agent-organizer orchestration pattern, CLAUDE.md dispatch protocol |
| **claude-code-config** | Trail of Bits | Varies | Security-first settings.json patterns, permission deny lists, CLAUDE.md template, hook patterns |
| **Claude Code Showcase** | Community | Varies | Skill evaluation hook system (skill-eval.js, skill-rules.json), GitHub Actions workflow templates, PostToolUse auto-format/lint/test hooks |

## Additional References

These projects were studied during research and influenced patterns in this repo:

| Project | What we learned |
|---------|----------------|
| **awesome-claude-code** | Community resource curation, README structure patterns |
| **claude-code-templates** | Multi-language template patterns, hook architectures |
| **claude-code-settings** | Command and agent organization patterns |
| **claude-templates** | Workflow documentation, setup script patterns |
| **composio-awesome-skills** | App integration skill patterns |

## Custom Content

The following was created specifically for this repository:

- **Reference skills** (fastapi-patterns, postgres-optimization, perf-profiler) — original content
- **Setup prompt** (prompt/setup-my-claude.md) — original prompt engineering
- **Guide chapters** (guide/) — original documentation
- **Configuration templates** (templates/) — adapted and annotated from multiple sources
- **Hook scripts** (hooks/pre-tool-use/, hooks/post-tool-use/) — adapted from multiple sources
- **README.md** — original design and writing
- **Installer** (`install.sh`, `scripts/installer_lib.py`) — original
- **Catalog and validator** (`scripts/catalog.py`, `catalog.json`, `presets.json`) — original
- **Redaction gate** (`scripts/sanitize.py`) — original, built on `examples/tools/redaction_linter.py`
- **Bootstrap skill** (`.claude/skills/bootstrap-claude/`) — original
- **Example configurations** (`examples/`) — contributed from the maintainer's own working
  machine and project repositories, sanitized before publication. See
  [`examples/README.md`](examples/README.md) for what is included and what is
  deliberately excluded.
- **Guide chapters 10–11** — original documentation

## License Note

Most content in this repo is MIT licensed. Anthropic official skills carry their own license — see the `LICENSE.txt` file in each skill directory under `skills/anthropic-official/`.
