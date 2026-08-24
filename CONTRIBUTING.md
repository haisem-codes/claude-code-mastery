# Contributing to Claude Code Mastery

We welcome contributions! Here's how to help improve this repository.

## Adding Skills

1. Create a directory under the appropriate domain in `skills/`
2. Add a `SKILL.md` with YAML frontmatter (name + description required)
3. Follow the [Skill Authoring Standard](skills/AUTHORING-STANDARD.md)
4. Keep SKILL.md under 10KB — put detailed content in `references/`
5. Include practical examples, not just theory

### Skill Structure

```
skills/<domain>/<skill-name>/
├── SKILL.md              # Required: workflow and instructions
├── references/           # Optional: detailed knowledge bases
├── scripts/              # Optional: Python tools (stdlib-only)
└── assets/               # Optional: templates, examples
```

### Frontmatter Requirements

```yaml
---
name: skill-name
description: When to use this skill. Include trigger keywords.
---
```

## Adding Agents

1. Create a `.md` file in the appropriate subdirectory of `agents/`
2. Follow the existing agent format (YAML frontmatter + structured sections)
3. Define clear boundaries — what the agent does and doesn't do
4. Specify required tools and MCP integrations

## Improving Guide Chapters

1. Each chapter should be 150-400 lines
2. Start with "What you'll learn"
3. End with links to the next chapter
4. Include copy-paste examples
5. Reference templates/ and hooks/ for full versions

## Submitting Hook Scripts

1. Place in the appropriate subdirectory of `hooks/`
2. Include a comment header explaining what the hook does
3. Use `jq` for parsing tool input (standard across all hooks)
4. Handle errors gracefully (exit 0 for non-blocking, exit 2 for blocking)

## Required checks

CI runs these on every push and blocks the merge if any fails. Run them locally
before opening a PR:

```bash
python3 scripts/sanitize.py --check   # no personal data in examples/
python3 scripts/catalog.py --check    # frontmatter, agent names, hook contract
python3 scripts/catalog.py            # regenerate catalog.json — commit the result
bash scripts/test-hooks.sh            # hook block/allow contract
bash scripts/test-install.sh          # installer end-to-end
```

### The redaction gate

This repository is public and `examples/` is derived from real machines.
`scripts/sanitize.py` fails on emails, phone numbers, public IPs, home paths,
client names, tokens and credential-shaped strings, and refuses whole file
classes outright — memory directories, `*.local.json`, plugin manifests, MCP
configs with real endpoints.

Contributing an example:

```bash
python3 scripts/sanitize.py --scrub ~/myproject/.claude examples/projects/my-archetype
python3 scripts/sanitize.py --check
git diff examples/          # read it yourself — the scrubber is a net, not a substitute
```

If a line is a deliberate test fixture containing a fake credential, mark it
`# sanitize:allow` rather than weakening a pattern.

### Adding a skill

Every `SKILL.md` needs `name` and `description` frontmatter. Without both,
Claude Code never discovers the skill — `catalog.py --check` enforces this.
Place it at `skills/<domain>/<skill-name>/SKILL.md`; the directory name is the
installed name.

### Adding an agent

Frontmatter `name` must equal the filename stem. The validator fails when they
drift, because the installer keys off `name` and users refer to files.

### Adding a hook

Hooks read their payload as JSON on **stdin** (`jq -r '.tool_input.command'`).
There is no `$TOOL_INPUT` variable. Blocking hooks exit `2`; advisory hooks must
always exit `0`. Add cases to `scripts/test-hooks.sh` covering both the block
and the allow path.

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the required checks above
5. Submit a PR with a clear description of what was added or changed

## Style Guidelines

- Dense bullets over prose
- Tables for structured comparisons
- Code blocks for copy-paste content
- No emoji in file content unless explicitly requested
- Keep line lengths reasonable (no hard wrap, but readable)
