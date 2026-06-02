# Requirements

## Functional Requirements

- Runtime cards should not look faded because of scene lighting.
- Card silhouettes must remain alpha-masked.
- Existing card texture parameter name remains `CardTexture`.
- Three-card spread should show table labels for Past / Present / Future.
- Existing one-card and three-card commandlet checks remain OK.

## Acceptance Criteria

- Game and Editor targets build.
- Material commandlet result is `ok=true`.
- Phase 4 play-surface check is OK.
- Phase 1 preflight is OK except existing `.git` warning.
- Updated screenshot shows stronger card readability and position labels.
