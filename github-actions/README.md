# GitHub Actions for Claude Code

Automated workflows that use Claude Code for continuous code quality, security, and maintenance.

## Available Workflows

| Workflow | Trigger | What it does |
|----------|---------|-------------|
| **PR Review** | Every PR open/update | Reviews diff for security, performance, quality, missing tests |
| **Docs Sync** | Monthly (1st) | Reads recent commits, updates outdated documentation |
| **Code Quality** | Weekly (Monday) | Reviews random directories for dead code, complexity, security |
| **Dependency Audit** | Biweekly (1st, 15th) | Audits and updates dependencies, runs tests |

## Setup

1. Copy the desired `.yml` files to your `.github/workflows/` directory
2. Configure the `ANTHROPIC_API_KEY` secret in your repo settings
3. Adjust cron schedules and review criteria to match your needs

## Requirements

- GitHub Actions enabled on your repository
- `ANTHROPIC_API_KEY` set as a repository secret
- `anthropics/claude-code-action@v1` (official GitHub Action)

## Customization

Each workflow is self-contained. Modify the `prompt` field to match your project's conventions, tech stack, and review criteria.
