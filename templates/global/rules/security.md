# Security Rules

## Secrets
- Never commit: .env, .key, .pem, credentials.json, API keys, tokens
- Always use environment variables for secrets
- Provide .env.example with placeholder values only
- Flag hardcoded secrets immediately if spotted

## Code Safety
- Validate all user input at system boundaries
- Parameterize SQL queries (never string-concatenate user input)
- Escape HTML output to prevent XSS
- Use HTTPS for all external requests
- Set appropriate CORS headers

## Dependencies
- Pin exact versions (no ^ or ~)
- Run `pip-audit` / `npm audit` before deploying
- Review new dependencies before adding (minimize attack surface)
