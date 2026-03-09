# TypeScript + Next.js Stack

## Runtime & Tooling

| Purpose | Tool |
|---------|------|
| Runtime | Node 22 LTS, ESM only |
| Package Manager | pnpm (or bun) |
| Lint | eslint (or biome) |
| Format | prettier (or biome) |
| Type Check | tsc --noEmit |
| Test | vitest (or jest) |

## Conventions

- TypeScript strict mode always enabled
- Prefer `interface` over `type` for object shapes
- Never use `any` — use `unknown` and narrow
- Server Components by default, `'use client'` only when needed
- App Router with file-based routing
- Server Actions for mutations
- Zod for runtime validation at API boundaries

## Project Structure

```
src/
├── app/             # Next.js App Router pages
├── components/      # React components
├── lib/             # Utilities and helpers
├── server/          # Server-side logic
└── types/           # TypeScript type definitions
```
