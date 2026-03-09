# Chapter 8: GitHub Actions — Claude in CI/CD

Claude Code can run as part of your CI/CD pipeline through the official `anthropics/claude-code-action` GitHub Action. This means Claude can review every PR, audit dependencies on a schedule, sync documentation, and flag code quality issues — all without a human triggering it.

This chapter covers the four workflow patterns, setup, customization, and cost management.

---

## How It Works

The `anthropics/claude-code-action@v1` action:

1. Checks out your repository in a GitHub Actions runner
2. Sends a prompt to Claude with relevant context (diff, files, commit history)
3. Claude analyzes the input and produces a response
4. The action posts results as PR comments, creates PRs, or takes other configured actions

Claude runs with read access to your code and write access to pull request comments. It does not push code directly — it creates PRs for human review.

---

## Setup Requirements

### 1. Add the API Key

Go to your repository **Settings > Secrets and variables > Actions** and add:

```
ANTHROPIC_API_KEY = sk-ant-...
```

This key is used by the action to authenticate with the Anthropic API. Use a dedicated key for CI — not your personal key.

### 2. Configure Permissions

Each workflow needs explicit permissions. At minimum:

```yaml
permissions:
  contents: read          # Read repository files
  pull-requests: write    # Post PR comments
```

For workflows that create PRs or push changes, add:

```yaml
permissions:
  contents: write
  pull-requests: write
```

### 3. Copy Workflow Files

Copy the desired `.yml` files from this repository's [`github-actions/`](../github-actions/) directory into your project's `.github/workflows/` directory.

---

## Workflow 1: PR Review (Every Pull Request)

**Trigger:** Every PR opened or updated.
**What it does:** Reviews the diff for security, performance, quality, and missing tests.

```yaml
name: Claude Code PR Review
on:
  pull_request:
    types: [opened, synchronize]

permissions:
  contents: read
  pull-requests: write

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get PR diff
        id: diff
        run: |
          git diff origin/${{ github.base_ref }}...HEAD > pr-diff.txt
          echo "diff_size=$(wc -l < pr-diff.txt)" >> $GITHUB_OUTPUT

      - name: Review with Claude
        if: steps.diff.outputs.diff_size > 0
        uses: anthropics/claude-code-action@v1
        with:
          prompt: |
            Review this PR diff for:
            1. Security vulnerabilities (OWASP top 10)
            2. Performance issues (N+1 queries, missing indexes, blocking I/O)
            3. Code quality (complexity, naming, error handling)
            4. Missing tests for new logic

            Be specific: file:line references, concrete suggestions.
            Skip style/formatting — linters handle that.
          diff_file: pr-diff.txt
```

**Customization ideas:**

- Add your tech stack to the prompt so Claude gives framework-specific advice
- Filter by file type: only review `.py` files, skip generated code
- Set a diff size threshold to skip trivial PRs (< 10 lines)

### Making Reviews Project-Specific

Tailor the prompt to your stack. A FastAPI project might use:

```yaml
prompt: |
  Review this PR for a FastAPI + SQLAlchemy project:
  1. SQL injection via string concatenation (must use parameterized queries)
  2. Missing Depends() for authentication on new endpoints
  3. N+1 queries — check for loops calling DB without joinedload
  4. Pydantic models missing validation (Field constraints, validators)
  5. Missing pytest coverage for new endpoints

  Ignore: formatting, import ordering, type hints on trivial functions.
```

---

## Workflow 2: Monthly Documentation Sync

**Trigger:** First day of each month at 9am UTC (also manually dispatchable).
**What it does:** Reads recent commits and updates outdated documentation.

```yaml
name: Monthly Docs Sync
on:
  schedule:
    - cron: '0 9 1 * *'
  workflow_dispatch:

jobs:
  docs-sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get recent commits
        run: |
          git log --oneline --since="1 month ago" > recent-commits.txt

      - name: Sync documentation
        uses: anthropics/claude-code-action@v1
        with:
          prompt: |
            Review the recent commits and check if documentation is still accurate.
            Update any outdated READMEs, API docs, or code comments.
            Create a PR with the changes.
```

**What Claude does:**

1. Reads the commit log to understand what changed
2. Finds documentation files (READMEs, docstrings, API docs)
3. Cross-references code changes with docs
4. Creates a PR with updates for anything that drifted

---

## Workflow 3: Weekly Code Quality

**Trigger:** Every Monday at 9am UTC.
**What it does:** Samples random directories and reviews for quality issues.

```yaml
name: Weekly Code Quality
on:
  schedule:
    - cron: '0 9 * * 1'
  workflow_dispatch:

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Quality review
        uses: anthropics/claude-code-action@v1
        with:
          prompt: |
            Pick 3 random directories in the codebase and review for:
            1. Dead code and unused imports
            2. Functions >100 lines or complexity >8
            3. Missing error handling
            4. Security issues

            Create a PR fixing any issues found. Keep changes minimal and atomic.
```

**Why random sampling works:** Reviewing the entire codebase weekly is expensive. Random sampling catches rot across different areas over time, and the cost stays predictable.

---

## Workflow 4: Biweekly Dependency Audit

**Trigger:** 1st and 15th of each month.
**What it does:** Audits dependencies, updates safe versions, and flags risky changes.

```yaml
name: Biweekly Dependency Audit
on:
  schedule:
    - cron: '0 9 1,15 * *'
  workflow_dispatch:

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Audit dependencies
        uses: anthropics/claude-code-action@v1
        with:
          prompt: |
            1. Run dependency audit (pip-audit, npm audit, or equivalent)
            2. Update any safe minor/patch versions
            3. Flag major version bumps for manual review
            4. Run tests after updates to verify nothing breaks
            5. Create a PR with safe updates
```

**Safety built in:** Claude only auto-updates minor and patch versions. Major version bumps are flagged in the PR description for human review, since they may contain breaking changes.

---

## Cost Considerations

Every workflow run consumes API tokens. Here is how to manage costs:

### Estimating Usage

| Workflow | Frequency | Estimated Tokens/Run | Monthly Cost (approx) |
|----------|-----------|---------------------|----------------------|
| PR Review | ~20 PRs/month | 5K-20K per PR | $2-8 |
| Docs Sync | 1x/month | 10K-30K | $0.50-2 |
| Code Quality | 4x/month | 10K-20K per run | $2-4 |
| Dependency Audit | 2x/month | 5K-15K per run | $0.50-2 |

Actual costs depend on codebase size, diff size, and prompt complexity. These estimates assume a mid-size project (50-200 files).

### Reducing Costs

1. **Filter PRs by size.** Skip trivial diffs (< 5 changed lines)
   ```yaml
   - name: Review with Claude
     if: steps.diff.outputs.diff_size > 5
   ```

2. **Limit review scope.** Only review certain file types
   ```yaml
   prompt: |
     Only review files matching: **/*.py, **/*.ts
     Skip: generated files, migrations, lock files
   ```

3. **Use cheaper models for triage.** If the action supports model selection, use Haiku for initial screening and Sonnet only for flagged issues

4. **Reduce schedule frequency.** Monthly quality reviews instead of weekly. Quarterly dependency audits instead of biweekly

5. **Set spending alerts.** Monitor your Anthropic API dashboard for unexpected spikes

---

## Advanced Configuration

### Conditional Triggers

Run reviews only on PRs that touch specific paths:

```yaml
on:
  pull_request:
    types: [opened, synchronize]
    paths:
      - 'src/**'
      - 'api/**'
      - '!**/*.md'
      - '!**/test/**'
```

### Multi-Step Workflows

Chain Claude actions for deeper analysis:

```yaml
steps:
  - name: Security scan
    uses: anthropics/claude-code-action@v1
    id: security
    with:
      prompt: |
        Focus ONLY on security issues in this diff.
        Output a JSON array of findings with severity ratings.
      diff_file: pr-diff.txt

  - name: Performance analysis
    uses: anthropics/claude-code-action@v1
    with:
      prompt: |
        Focus ONLY on performance issues in this diff.
        Check for: N+1 queries, missing caching, blocking I/O,
        unbounded data fetches.
      diff_file: pr-diff.txt
```

### Using with Monorepos

For monorepos, scope reviews to the changed service:

```yaml
- name: Identify changed services
  id: changes
  run: |
    changed=$(git diff --name-only origin/${{ github.base_ref }}...HEAD | cut -d/ -f1 | sort -u)
    echo "services=$changed" >> $GITHUB_OUTPUT

- name: Review with Claude
  uses: anthropics/claude-code-action@v1
  with:
    prompt: |
      This is a monorepo. Only review changes in: ${{ steps.changes.outputs.services }}
      Apply the coding standards specific to each service.
    diff_file: pr-diff.txt
```

---

## Setting Up Your First Workflow

The fastest path to value:

1. Copy `pr-review.yml` to `.github/workflows/pr-review.yml`
2. Add `ANTHROPIC_API_KEY` to your repo secrets
3. Open a test PR
4. Review Claude's feedback and tune the prompt

Start with PR review. It gives the fastest feedback loop — you see results on every PR. Add scheduled workflows once you have validated the setup.

See all workflow files in the [`github-actions/`](../github-actions/) directory.

---

Next: [Chapter 9 — Advanced Patterns](./09-advanced-patterns.md)
