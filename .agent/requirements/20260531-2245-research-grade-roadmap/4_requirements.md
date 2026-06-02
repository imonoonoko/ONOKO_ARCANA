# ONOKO ARCANA Research-Grade Roadmap Requirements

## 1. Overview

ONOKO ARCANAは、PC上の3D占い卓でタロットを引き、ユーザー自身の解釈を書き、補助解釈と比較しながら学習できるUnreal Engine製デスクトップソフトである。現在の最重要要件は、全カード量産より先に、Unreal向けカード画像の画質、透過、外形、比率を安定させることである。

## 2. User Stories

- As a learner, I want to draw tarot cards on a PC table, so that I can practice without owning physical cards.
- As a learner, I want to write my interpretation before seeing the guide, so that I learn actively.
- As a creator, I want every card to share the same aspect ratio and alpha shape, so that Unreal display is stable.
- As a creator, I want ONOKO character art to stay sharp, so that the card deck feels production quality.
- As a developer, I want asset audits before Unreal import, so that broken images do not enter the project.

## 3. Acceptance Criteria

### Card Asset Pipeline

- Given a generated or composed card, when it is accepted for Unreal import, then it is `1024x1536`.
- Given a UE-ready card PNG, when alpha is audited, then the alpha bbox is `(54,32,970,1514)`.
- Given a UE-ready card PNG, when alpha is audited, then alpha values are only `0` and `255`.
- Given a UE-ready card PNG, when key-spill audit runs, then visible magenta/key pixels are `0`.
- Given a card with ONOKO central art, when the character crop report is reviewed, then face and hands are not visibly destroyed.

### Unreal QA

- Given V4 card assets, when opened in Alpha QA Map, then no rectangular background leak is visible.
- Given front and back cards, when displayed side by side in Alpha QA Map, then their visible width matches.
- Given the Production Preview Map, when card shadows are enabled, then any rectangular shadow issue is classified separately from image alpha.

### Reading Flow

- Given the app has loaded, when the user starts a one-card reading, then a card is drawn and displayed on the table.
- Given a card is drawn, when orientation is reversed, then reversed keywords are shown and card orientation reflects the state.
- Given a reading session, when the guide is unrevealed, then user interpretation input is still available.
- Given a saved reading, when the app restarts, then the reading can be reopened.

## 4. User-Facing Nonfunctional Requirements

### Responsiveness

- Card draw, flip, and panel updates should feel immediate after short animation.
- Study/history views must not stall because of large texture loading.

### Usability

- The first screen should be the actual divination table, not a marketing page.
- Controls must support repeated use: Draw, Reset, Save, Study, History.
- Text must remain readable over the dark ONOKO table.

### Accessibility

- State must not rely only on blue glow. Position, labels, icon state, and motion must support recognition.
- Card meanings and user notes must use high-contrast UI text, not baked image text.

### Feedback And Errors

- Missing texture, failed save, empty history, and invalid card data must have visible states.
- Asset QA failures must stop import or mark the asset as blocked.

## 5. Open Questions

- Should native transparent image generation via API be adopted, or should chroma-key plus fixed mask remain the default?
- What exact central art crop size gives enough ONOKO character fidelity inside the final card?
- Should card text overlays be pure UMG panels or world-space Widget Components on cards?
- What is the acceptable texture memory budget for 22 cards and later 78 cards?

