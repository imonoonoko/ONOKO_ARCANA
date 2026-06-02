# Alternatives

## A. Single Full-Screen HUD Overlay

Rejected for this slice. It looks rich in screenshots, but it is difficult to align with real card positions, variable spread counts, responsive layouts, Japanese text, and future UI states.

## B. Pure CSS Ornament

Useful but insufficient. It is easy to scale and maintain, but it does not use the generated ONOKO HUD material language strongly enough.

## C. Modular PNG Components Over Code-Native Layout

Chosen. Keep functional layout, controls, labels, and text in HTML/CSS/JS. Use transparent PNG parts for plaques, panel ornaments, card slots, pips, and command styling.

## D. Immediate UE/UMG Integration

Deferred. The Web/Electron loop currently gives faster feedback, easier screenshots, and lower risk while the product surface is still moving.
