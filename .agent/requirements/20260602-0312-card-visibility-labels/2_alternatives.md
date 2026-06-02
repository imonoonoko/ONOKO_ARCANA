# Alternatives

## A. Increase runtime lights

Raise point light intensity and add more fill lights.

Pros:

- Simple.

Cons:

- Still depends on camera exposure and scene lighting.
- Can wash out UI or table surfaces.

## B. Use Unlit Masked card material

Keep alpha masking but drive card color through Emissive Color.

Pros:

- Decouples card readability from lighting.
- Matches existing roadmap direction.
- Keeps card edges stable.

Cons:

- Less physically realistic until a final presentation material is designed.

## Chosen

Use Alternative B for the runtime/playtest material. Keep lighting changes minimal.
