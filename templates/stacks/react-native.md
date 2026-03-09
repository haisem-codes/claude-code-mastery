# React Native Stack

## Runtime & Tooling

| Purpose | Tool |
|---------|------|
| Framework | React Native / Expo |
| Language | TypeScript (strict) |
| Navigation | React Navigation |
| State | Redux Toolkit / Jotai |
| Test | Jest + React Native Testing Library |
| E2E | Maestro / Detox |

## Conventions

- TypeScript strict mode
- Feature-based folder structure
- Custom hooks for shared logic
- Memoize expensive renders (React.memo, useMemo, useCallback)
- FlashList over FlatList for long lists
- Platform-specific code via .ios.tsx / .android.tsx

## Project Structure

```
src/
├── app/             # Navigation, providers
├── components/      # Shared UI components
├── features/        # Feature modules
├── hooks/           # Custom hooks
├── services/        # API clients
├── state/           # Global state
└── utils/           # Helpers
```
