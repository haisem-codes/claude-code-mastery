# Flutter + Dart Stack

## Runtime & Tooling

| Purpose | Tool |
|---------|------|
| SDK | Flutter 3.x |
| Language | Dart 3.x |
| State Management | Riverpod (or Bloc) |
| Navigation | go_router |
| HTTP | dio |
| Test | flutter test |

## Conventions

- Feature-first folder structure
- Riverpod providers for state management
- Repository pattern for data access
- Separate models for API responses and domain entities
- Freezed for immutable data classes
- go_router for declarative navigation

## Project Structure

```
lib/
├── main.dart
├── app/             # App-wide config, theme, router
├── features/        # Feature modules
│   └── auth/
│       ├── data/    # Repositories, data sources
│       ├── domain/  # Models, entities
│       └── presentation/ # Screens, widgets
├── shared/          # Shared widgets, utils
└── core/            # Constants, theme, network
```
