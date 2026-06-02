# Requirements

## Functional Requirements

1. The project shall expose a built-in spread catalog through a Blueprint-visible runtime class.
2. Each spread shall have a stable id, display name, description, layout type, card count, and ordered slot list.
3. Each slot shall have a stable position key, display label, reveal order, guide prompt, table location, and table yaw.
4. `one_card` shall remain the default active spread.
5. The table controller shall initialize the spread registry during table initialization.
6. The table controller shall support selecting a spread by id.
7. Selecting an unknown spread shall fail with a readable error and preserve the previous active spread.
8. The native fallback HUD shall show active spread text and slot text.
9. The native fallback HUD shall expose a spread selector combo box when using the native widget tree.
10. Existing draw/reveal/guide/save/reset controls shall continue to work for `one_card`.
11. Saved one-card readings shall include spread metadata so old Phase 1 readings can coexist with future spread readings.

## Acceptance Criteria

- `one_card` is the default spread after table initialization.
- At least six spread definitions are available from C++/Blueprint.
- `celtic_cross` reports 10 slots.
- `three_card_past_present_future` reports 3 slots with reveal order 1, 2, 3.
- Selecting `three_card_past_present_future` changes the active spread metadata.
- Selecting an invalid id returns false and sets `LastErrorMessage`.
- A one-card save includes `SpreadId=one_card` and `CardCount=1`.
- Existing Phase 1 preflight still passes.

## Risks

- The native fallback HUD can show metadata, but it is not the final polished spread selector.
- If multi-card runtime is implemented before save schema is planned, the current single-card save structure will need migration.
- Generated UI images contain some English placeholder text; final UI copy must remain code-native and reviewed.
