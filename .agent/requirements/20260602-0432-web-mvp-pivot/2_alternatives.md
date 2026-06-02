# Alternatives

## A. Continue Unreal as the immediate MVP

Pros:

- Existing C++ and generated UE texture work can be reused directly.
- A 3D table can feel premium when fully wired.

Cons:

- Current bottleneck is not asset quality; it is runtime/UI wiring and Editor proof.
- Lighting and material behavior can make cards hard to read.
- UE automation has already hit unstable map actor spawning.
- Iterating UI density, spread layouts, note entry, and history is slower than Web.

## B. Web prototype first, then wrap as Electron or Tauri

Pros:

- Fastest route to the real product loop.
- Generated PNG assets can be used directly.
- UI, spread layout, reveal order, memo, and history are cheap to iterate.
- The prototype can become the production desktop UI with limited rework.

Cons:

- Does not prove 3D table presence.
- Needs a later packaging decision.
- Native file save, settings, and window integration are deferred.

## C. Godot desktop app

Pros:

- More game-like than Web and lighter than UE.
- Strong 2D tooling.

Cons:

- Requires a new engine/runtime stack.
- Existing Web-style UI logic would still need to be rebuilt.
- Less direct benefit for the current generated-card proof.

## D. Visual novel engine

Pros:

- Good for story-led fortune experiences.

Cons:

- ONOKO ARCANA is primarily a repeatable tarot table, not a branching scene reader.
- Spread layout, note taking, and history become awkward if treated as a VN first.

## Recommendation

Use Web as the MVP execution surface. Keep Unreal as a parallel future expression layer after the reading loop is stable.
