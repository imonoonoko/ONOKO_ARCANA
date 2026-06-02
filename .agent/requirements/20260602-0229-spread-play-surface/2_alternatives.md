# Alternatives

## A. Native C++ play-surface bridge

Use `AOnokoArcanaTableController` to own a `UOnokoArcanaSpreadReadingViewModel` and a runtime array of `AOnokoArcanaCardActor` instances.

Pros:

- Reuses existing runtime card actor and material path.
- Works without a custom Blueprint widget.
- Keeps proof in game runtime rather than Python actor spawn.

Cons:

- The first visual layout is functional, not final art direction.

## B. UMG-only card slots

Render three cards as UMG image slots in the fallback HUD.

Pros:

- Fast to make a visible proof.

Cons:

- Does not prove table actors or 3D card placement.
- Duplicates visual card handling instead of reusing `AOnokoArcanaCardActor`.

## Chosen

Use Alternative A for this slice, with small HUD text additions only where needed.
