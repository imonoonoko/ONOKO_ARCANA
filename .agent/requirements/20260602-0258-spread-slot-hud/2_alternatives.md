# Alternatives

## A. Add native fallback HUD slot buttons

Add Past / Present / Future buttons to `UOnokoArcanaTableHudWidget` and route them to `AOnokoArcanaTableController::SelectSpreadSlot`.

Pros:

- Smallest reliable implementation.
- Commandlet and screenshot friendly.
- Keeps current C++ flow intact.

Cons:

- Not final visual design.

## B. Build final WBP_TableHUD now

Create a full UMG Blueprint surface and bind all widgets.

Pros:

- Better visual direction sooner.

Cons:

- Higher editor-asset risk before interaction contracts are complete.
- Harder to validate in commandlet.

## Chosen

Use Alternative A now. Promote the behavior into `WBP_TableHUD` after this contract is stable.
