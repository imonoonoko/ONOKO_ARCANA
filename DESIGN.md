# Design

## Visual Style

ONOKO ARCANA uses a dark cyber-oracle interface: black acrylic panels, low-opacity blue glow, fine gold dividers, compact product controls, and high-contrast text. The visual priority is the tarot table first, then the current card guide, then saved history.

## Color

- Background: near-black `#03070C`
- Panel: blue-black `#07101A` at high opacity
- Panel layer: cool charcoal `#101923`
- Text: ice white `#EAF6FF`
- Muted text: blue gray `#9CB3C5`
- Gold: `#D8B46B`
- Active blue: `#43A8FF`
- Error: `#FF8A7A`

## Typography

Use reliable Japanese UI fonts first: Yu Gothic UI, Meiryo, Segoe UI, or the host platform default. Headings should be larger and letter-spaced only through content spacing, not negative tracking. Labels stay compact.

## Layout

The running play screen should use:

- left panel for spread and question input
- right panel for selected-card guide and history
- bottom command bar for repeated actions
- world table labels for spread positions

## Components

- Panels: dark translucent backgrounds with thin gold/blue border feel.
- Buttons: compact, consistent, with gold text and blue emphasis for active/reveal actions.
- Inputs: dark framed fields with clear focus state.
- Table labels: concise Japanese labels for each spread position.
- Generated HUD overlay: use transparent `imagegen` ornament assets as atmospheric frames behind native controls, not as the only source of functional affordance.

## Motion

Use restrained motion only for card reveal state and selected-card feedback. Avoid decorative motion until the table loop is stable.
