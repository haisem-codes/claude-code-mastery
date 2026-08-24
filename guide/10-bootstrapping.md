# 10. Bootstrapping a Machine

The previous chapters explain what each piece of Claude Code configuration does.
This one is about getting a working setup onto a new machine quickly, and being
able to change your mind afterwards.

## The two paths

**Conversational.** Open this repo in Claude Code and run `/bootstrap-claude`.
The skill reads `catalog.json`, asks what kind of work you do, previews the
changes, and applies them. Use this if you are not sure what you want.

**Direct.** Run the installer yourself:

```bash
./install.sh --list
./install.sh --preset backend-python --dry-run
./install.sh --preset backend-python
```

Use this if you already know, or if you are scripting a machine build.

Both end in the same place. The skill is a front-end for the installer, not a
separate mechanism.

## What actually happens

1. **Preflight.** Checks `python3` and `git`. Warns if `jq` is missing, because
   the blocking hooks refuse to run without it rather than failing open — a
   safety hook that silently stops working is worse than no hook.
2. **Backup.** Copies `~/.claude` to `~/.claude.bak.<timestamp>` and prints the
   restore command. Skipped with `--no-backup`, which you want in CI.
3. **Copy.** Each selected skill, agent and hook is copied and checksummed.
4. **Merge.** `settings.json` is merged, never replaced. See below.
5. **Manifest.** `~/.claude/.mastery-manifest.json` records every installed path
   and its checksum.

## Why merging matters

The naive installer writes `settings.json` from a template. If you already had
one, you have just lost your `model`, your `env`, your `permissions.allow`, your
statusline and your MCP config.

This installer unions instead:

| key | behavior |
|---|---|
| `permissions.deny` / `allow` / `ask` | template rules appended; yours kept, order preserved |
| `env` | only missing keys added; an existing value is never overwritten |
| `hooks` | appended by `(event, matcher, command)`; exact duplicates skipped |
| everything else | untouched |

The installer also verifies no top-level key disappeared, and aborts if one
would. You can check this yourself:

```bash
bash scripts/test-install.sh   # case 3 asserts exactly this
```

## Re-running it

Running twice is safe and is the normal way to add things later:

```bash
./install.sh --preset backend-python        # first run: 19 new
./install.sh --preset backend-python        # second run: 0 new, 19 unchanged
./install.sh --skills marketing/seo-audit   # add one more
```

If you edited an installed file, the checksum no longer matches and the
installer says so:

```
  ! agents/debugger.md  (locally modified — use --force to overwrite)
```

Your edit is kept. Pass `--force` only when you want the repo version back.

## Undoing it

```bash
./install.sh --uninstall            # remove what was installed
./install.sh --uninstall --dry-run  # see what that would remove first
```

Uninstall reads the manifest, so it only touches files it put there. Skills you
wrote yourself in the same directory are left alone, and locally-modified files
are skipped unless you add `--force`.

`settings.json` is deliberately **not** reverted — by then it may contain your
own later edits. Remove the hook entries by hand, or restore the backup:

```bash
mv ~/.claude.bak.<timestamp> ~/.claude
```

## Choosing what to install

Resist installing everything. Skill selection is a retrieval problem: the model
picks from descriptions, and 168 similar-sounding options produce worse matches
than 12 well-chosen ones. The same applies to subagents — see the note in
[`examples/README.md`](../examples/README.md) on why the reference global config
ships two agents rather than thirty-seven.

Start with a preset. Add a skill the first time you actually miss it.

## A different config directory

Everything respects `CLAUDE_CONFIG_DIR`:

```bash
CLAUDE_CONFIG_DIR=~/.claude-work ./install.sh --preset devops
# or
./install.sh --preset devops --config-dir ~/.claude-work
```

Useful for keeping a work profile and a personal profile apart, and for testing
a config without touching your real one.

## Verifying it worked

```bash
ls ~/.claude/skills ~/.claude/agents
python3 -c "import json;json.load(open('$HOME/.claude/settings.json'));print('ok')"
bash scripts/test-hooks.sh
```

Then restart Claude Code — skills and hooks are read at startup, so nothing you
just installed is active in the current session.

## Troubleshooting

| symptom | cause | fix |
|---|---|---|
| skill never triggers | no `name`/`description` frontmatter | `python3 scripts/catalog.py --check` |
| skill never triggers | copied a domain directory, so nesting is too deep | reinstall with `install.sh` |
| hook does nothing | `jq` missing | `brew install jq` / `apt install jq` |
| hook blocks everything | matcher too broad | edit the entry in `~/.claude/settings.json` |
| installer skips a file | you edited it after install | `--force`, or keep your version |
| `unknown preset` | typo | `./install.sh --list` |

Next: [11. Real-World Configurations](11-real-world-configs.md)
