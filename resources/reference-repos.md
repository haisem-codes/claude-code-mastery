# Reference Repositories

Eleven upstream repositories that this project was built from, plus the main
community indexes. They are **cloned, not vendored** — each stays on its own
upstream, keeps its own license, and can be refreshed independently.

`/bootstrap-claude` fetches them automatically during setup. To do it by hand:

```bash
./scripts/fetch-references.sh              # all 11, shallow clones (~241 MB)
./scripts/fetch-references.sh --skip-large # omit the 219 MB CLI repo (~90 MB)
./scripts/fetch-references.sh --list       # show what would be cloned
./scripts/fetch-references.sh --update     # refresh existing clones
```

They land in `references/`, which is gitignored. The manifest that drives all of
this is [`reference-repos.json`](reference-repos.json) — edit that, not this page.

## Why clone instead of vendor

Copying these in would mean maintaining eleven stale forks, inheriting eleven
licenses, and adding ~241 MB to every clone of this repo. Cloning keeps them
current, keeps attribution unambiguous, and keeps this repository's own diff
readable.

## Skill libraries

| repo | license | size | why read it |
|---|---|---|---|
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | MIT | 21 MB | **The origin of 149 of this repo's 168 skills.** The upstream set is larger (345+) and updated more often than the snapshot here. |
| [anthropics/skills](https://github.com/anthropics/skills) | per-skill | 4 MB | Anthropic's own skills, and the reference for how a skill should be structured. The 16 in `skills/anthropic-official/` come from here. |
| [feiskyer/claude-code-settings](https://github.com/feiskyer/claude-code-settings) | MIT | 1 MB | Compact and well-organised — a good model for laying out commands and agents without the volume of the larger collections. |

## Configuration examples

| repo | license | size | why read it |
|---|---|---|---|
| [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config) | none stated | 1 MB | The security-first end of the spectrum. Its deny-list patterns are the basis for `templates/global/settings.json`. |
| [ChrisWiles/claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase) | none stated | 1 MB | Source of the skill-eval hook system and the GitHub Actions here. Worth reading end to end as a complete project config. |
| [pvillega/claude-templates](https://github.com/pvillega/claude-templates) | none stated | 1 MB | Small and readable, if the larger template sets are more structure than you want. |

## Community indexes

| repo | license | size | why read it |
|---|---|---|---|
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | none stated | 34 MB | The broadest index of the ecosystem — skills, agents, status lines, tooling, plugins. Start here when something is not in this repo. |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | none stated | 3 MB | Strong on app-integration patterns — how a skill wraps a third-party API cleanly. |
| [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | none stated | 1 MB | Smaller and more Claude Code-specific than the other lists. |
| [BehiSecc/awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills) | none stated | 1 MB | Another skills index; overlaps the two above. |

## Tooling

| repo | license | size | why read it |
|---|---|---|---|
| [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates) | MIT | **219 MB** | A CLI that configures and monitors Claude Code — a different solution to the problem `install.sh` solves. Excluded by `--skip-large`. |

## Using them with Claude Code

Once cloned, they are searchable context. Instead of guessing whether a
capability exists, look:

```bash
rg -il "kubernetes" references/ -g SKILL.md
rg -l "PostToolUse" references/ -g "*.json"
find references -name 'SKILL.md' | wc -l
```

This is the main reason to have them locally rather than as links: the model can
grep them.

## Licensing

**Six of the eleven have no detectable `LICENSE` file** (shown as "none stated"
above, `NOASSERTION` in the manifest). No stated license means default copyright
— you may read them, but do not copy code out of them into your own project
without checking with the author first.

`anthropics/skills` is not MIT either; each skill carries its own `LICENSE.txt`.

Where this repository has taken content from any of these, it is recorded in
[`CREDITS.md`](../CREDITS.md).

## Adding one

Append to [`reference-repos.json`](reference-repos.json):

```json
{
  "slug": "owner/repo",
  "name": "local-directory-name",
  "category": "skill-library | config-example | curated-list | tooling",
  "license": "MIT",
  "size_mb": 5,
  "default": true,
  "sourced_from": false,
  "why": "One sentence on what a reader gets from it that they cannot get here.",
  "description": "Upstream's own one-line description."
}
```

Then `./scripts/fetch-references.sh --list` to confirm it parses.
