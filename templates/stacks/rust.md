# Rust Stack

## Runtime & Tooling

| Purpose | Tool |
|---------|------|
| Toolchain | rustup (stable) |
| Format | rustfmt |
| Lint | clippy |
| Test | cargo test |
| Build | cargo build --release |

## Conventions

- Prefer `Result<T, E>` over panics
- Use `thiserror` for library errors, `anyhow` for applications
- Derive traits generously: Debug, Clone, PartialEq
- Minimize `unsafe` — justify every usage
- Use `#[must_use]` on functions returning important values
- Prefer iterators over manual loops

## Project Structure

```
src/
├── main.rs          # Entry point
├── lib.rs           # Library root
├── config.rs        # Configuration
├── error.rs         # Error types
├── handlers/        # Request handlers
├── models/          # Data structures
└── services/        # Business logic
```
