# ONOKO ARCANA Unreal Roadmap Requirements

## 1. Overview
ONOKO ARCANAは、タロットカードを持っていないユーザーがPC上で占いを操作しながら学べる、ONOKO世界観のタロット学習ソフトである。最初の実装目標は、Unreal Engine上で3D占い卓、カードドロー、カード意味表示、ユーザー解釈メモ、履歴保存をつなぐ縦断スライスを作ることである。

## 2. User Stories
- As a tarot beginner, I want to draw a card on a PC table, so that I can practice without owning physical tarot cards.
- As a learner, I want to write my interpretation before seeing the guide, so that I can train reading skill instead of only reading answers.
- As a creator, I want all ONOKO ARCANA assets to follow a fixed ratio and naming rule, so that Unreal import and future card expansion stay manageable.
- As a returning user, I want my past questions and notes saved locally, so that I can compare how my interpretation changes.
- As a visual user, I want the table, card backs, and UI panels to feel like ONOKO's cyber divination desk, so that the app has a clear identity.

## 3. Acceptance Criteria

### Asset Corpus
- Given the roadmap document, when the user opens it, then it lists the current kanban boards, reference sheet, generated card fronts, card back, JSON data, reports, and prototype.
- Given a production card image, when its dimensions are checked, then it conforms to `1024x1536px` and `2:3`.
- Given card name or keyword text, when the asset policy is applied, then the text is rendered by the app UI rather than baked into the image.

### Unreal Vertical Slice
- Given the app has launched, when the first scene loads, then a 3D ONOKO-style divination table is visible.
- Given the user draws one card, when the card lands in the active slot, then the app shows the correct card name, upright/reversed state, keywords, and study focus.
- Given the user writes a note, when the session is closed and reopened, then the note is recoverable from local save data.
- Given a card is hovered or selected, when the user requests detail, then a larger view or side panel appears without hiding the table context.

### Learning Flow
- Given a reading starts, when a card appears, then the user's note area is visually primary before the guide interpretation.
- Given the user submits or expands the guide, when the guide appears, then it helps compare symbols, keywords, and user interpretation rather than replacing the user's judgment.

### Visual Identity
- Given any primary UI surface, when viewed beside the kanban board, then it uses the same ONOKO vocabulary: black, white, electric blue, muted gold, cat iconography, crystal/observation lines, dark desk material, and holographic panels.
- Given a small or medium window, when the user reads card text, then names and keywords remain legible and do not overlap card art.

## 4. User-Facing Nonfunctional Requirements

### Responsiveness
- Card draw and panel transitions should feel immediate after input.
- Visual effects must remain short and readable; they should support repeated practice rather than slow every reading.

### Usability
- The first screen should be the usable divination table, not a marketing page.
- Core operations should be discoverable from visible table affordances: shuffle, draw, reset, note, guide, history.
- The user should be able to repeat one-card readings without navigating through multiple screens.

### Accessibility
- Text must maintain strong contrast against dark surfaces.
- State must not be communicated only by color; selected, reversed, saved, and guide-visible states need shape, label, or placement differences.
- Keyboard and mouse flows should both be considered for Windows desktop use.

### Feedback And Errors
- Missing card image, missing JSON field, and save failure should show clear development-time warnings.
- User-facing errors should be short and recoverable.
- Empty history should display an empty state, not a broken panel.

## 5. Open Questions
- Unreal Engine 5.7系をこのPCにインストールするタイミング。
- 最初のUnrealプロジェクトをBlueprint-onlyで始めるか、C++プロジェクトとして始めてBlueprintを主運用にするか。
- JSONを直接読むか、Unreal DataTable/DataAssetに変換するか。
- ONOKOガイドを最初はテキストUIにするか、2D立ち絵/3Dアバターを早めに置くか。
- セーブ形式をUnreal SaveGameだけにするか、将来のエクスポートを見越してJSONにも出すか。
