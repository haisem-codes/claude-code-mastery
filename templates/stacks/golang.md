# Go Stack

## Runtime & Tooling

| Purpose | Tool |
|---------|------|
| Runtime | Go 1.22+ |
| Format | gofmt / goimports |
| Lint | golangci-lint |
| Test | go test ./... |
| Build | go build |

## Conventions

- Standard project layout (cmd/, internal/, pkg/)
- Explicit error handling (no panic for expected errors)
- Context propagation through all function chains
- Interfaces defined by consumers, not producers
- Table-driven tests
- Structured logging (slog)

## Project Structure

```
cmd/
├── server/main.go   # Entry point
internal/
├── handler/         # HTTP handlers
├── service/         # Business logic
├── repository/      # Data access
├── model/           # Domain types
└── middleware/       # HTTP middleware
pkg/                 # Public libraries
```
