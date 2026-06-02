# Alternatives

## Option A: Extend `UOnokoArcanaOneCardSession`

Add arrays and slot behavior directly to the existing one-card session.

Rejected. The one-card class names and public methods are already used by Phase 1 tests and HUD. Mutating them into a spread engine would blur the current working proof.

## Option B: Build A New Spread Runtime Beside Phase 1

Add `UOnokoArcanaSpreadReadingSession` and related state beside the current one-card runtime. The table controller can route one-card through the existing path and multi-card through the new path.

Chosen. This preserves the stable Phase 1 path while allowing multi-card semantics to be tested independently.

## Option C: Make Blueprint-Only Multi-Card State

Keep C++ unchanged and build multi-card behavior in UMG/Blueprint.

Rejected for the next step. The project already uses C++ for deck runtime, session state, SaveGame, and view models. Multi-card state needs the same commandlet-testable reliability.
