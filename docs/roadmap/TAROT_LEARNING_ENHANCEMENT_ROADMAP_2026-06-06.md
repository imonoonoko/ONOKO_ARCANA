# ONOKO ARCANA Tarot Learning Enhancement Roadmap

Updated: 2026-06-07

## Summary

ONOKO ARCANA should evolve from "a reading table with saved history" into "a tarot study table." The product should teach through repeated reading, recall, reflection, and review rather than by dumping card meanings upfront.

The next strategic move is to build a learning layer around the existing Major Arcana loop:

- Learn each card.
- Read before study sheet.
- Compare after writing.
- Review past readings by card.
- Practice recall over time.

## Research Basis

Verified source pass: 2026-06-06.

Tarot content research:

- Tarot is historically a card-game structure before it is a divination UI: Britannica describes the 1430s Italy deck pattern as four suits plus 21 trionfi/trumps and the Fool, and the standard modern deck as 78 cards split into 22 Major Arcana and 56 Minor Arcana: https://www.britannica.com/topic/tarot
- Museum sources support treating tarot cards as visual, historical, and symbolic artifacts. V&A notes the 78-card structure, Italian suits, the late-18th-century shift toward fortune-telling, and Rider-Waite-Smith's intuitive illustrated pip cards: https://www.vam.ac.uk/articles/tarot-cards
- Beinecke/Yale's Visconti Tarot material supports a "card lineage" layer: early hand-painted 15th-century cards, court context, and surviving visual artifacts can become optional study notes rather than front-loaded instruction: https://beinecke.library.yale.edu/collections/highlights/visconti-tarot
- Tarot meaning libraries commonly organize learning by upright/reversed meanings, keywords, symbolism, guidance, suggested questions, and context-specific interpretation: https://support.biddytarot.com/hc/en-us/articles/13184136583311-Where-do-I-find-the-Tarot-Card-Meanings-Library
- Labyrinthos' Major Arcana meaning list reinforces treating the 22 cards as the Fool's Journey and presenting compact upright/reversed keywords as a learnable foundation: https://labyrinthos.co/blogs/tarot-card-meanings-list/tagged/major-arcana
- Biddy Tarot's beginner learning guidance emphasizes daily one-card practice, writing intuitive impressions before looking up meanings, and keeping a tarot journal. This supports ONOKO's "write first, study sheet later" rule: https://biddytarot.com/podcast/btp71-learn-tarot-from-day-one/
- Tarot.com recommends starting small, from one card to three-card spreads, before moving into Celtic Cross. This supports keeping learning milestones separate from complex spread clutter: https://www.tarot.com/tarot/tarot-101-how-readings-work
- Tarot learning apps and journals commonly use keywords, correspondences, reading records, reflection prompts, pattern tracking, quizzes, and reminders rather than one-off "answer" screens: https://app.labyrinthos.co/ and https://play.google.com/store/apps/details?id=com.labyrinthos.app
- 2026 HCI research on AI-assisted tarot frames tarot as subjective, plural, and non-causal interpretive meaning-making, and recommends preserving ambiguity and user agency. This supports keeping ONOKO as a comparison/study companion rather than an automatic answer engine: https://arxiv.org/abs/2602.11367

Learning science research:

- Retrieval practice should be active and low-stakes. Carnegie Mellon summarizes it as recalling from memory through quizzes, flashcards, or practice problems, and notes that feedback improves learning: https://www.cmu.edu/teaching/resources/instructionalstrategies/activelearningstrategies/retrievalpractice/index.html
- Practice testing and distributed practice have strong support across learners and tasks. Dunlosky et al. rate practice testing and distributed practice as high-utility techniques: https://journals.sagepub.com/doi/10.1177/1529100612453266
- Spacing should be added after a minimal attempt log exists. Cepeda et al.'s distributed-practice review is the basis for turning hard/ok/easy attempts into future due cards: https://pubmed.ncbi.nlm.nih.gov/16719566/

## Product Principle

The user should encounter tarot knowledge in this order:

1. Observe the card and slot.
2. Write their own read.
3. Reveal the study sheet or explanation.
4. Compare.
5. Save.
6. Review later.
7. Practice recall.

This protects the original ONOKO ARCANA idea: the app is a study companion, not an answer machine.

## Roadmap

Implementation note 2026-06-07: Phase L1 Card Study Sheet, Phase L2, the minimal Phase L3 Recall Practice slice, Slot Interpretation Drill, the first Phase L4 due-card slice, and the card-tab full study sheet beside the user's note are implemented. Study Lens clickthrough, card-specific history review filter, note-vs-study-sheet comparison, card sheet open from selected cards or Study Lens, keyword recall, upright/reversed practice, selected-card slot interpretation, hard/ok/easy confidence saving, separate learning data export/import/clear, first-launch learning guidance, after-save next actions, and a minimal due-card cue are verified in `reports/web-app-smoke-20260607-011915.json`. Visual evidence: `reports/ui-visual-audit-20260607-012023/report.json`, `reports/onoko-arcana-card-tab-study-sheet-20260607-0120.png`, `reports/onoko-arcana-settings-20260607-011915.png`, and `reports/onoko-arcana-first-launch-20260607-011915.png`.

### Phase L1: Study Content Foundation

Status: Card Study Sheet implemented; historical/context notes remain backlog

Purpose: make each Major Arcana card learnable inside the app.

Tasks:

| Item | Priority | Description | Done Evidence |
|---|---|---|---|
| Card Study Sheet | P0 | Add a detail surface for each Major Arcana card with upright, reversed, current keywords, study focus, symbols, common misreads, and reflection questions. | `reports/web-app-smoke-20260606-201152.json`, `reports/ui-visual-audit-20260606-201207/report.json` |
| Card Data v1.1 | P0 | Extend card data with `studyDetails.symbols`, `studyDetails.reflectionQuestions`, and `studyDetails.commonMisreads` while preserving current fields. | `reports/web-app-check-20260606-201256.json`, `docs/data/CARD_SCHEMA_V1.md` |
| Reversal Framing | P1 | Teach reversals as blocked, delayed, internalized, excessive, or redirected expressions instead of always "bad." | Card content review |
| History Note | P2 | Add short historical/context note for each Major Arcana where useful. | Content fixture |

Acceptance:

- Existing readings still work.
- In recall and slot drills, the answer/explanation still unlocks only after the user writes first.
- In the normal card tab, the full study sheet can stay visible beside the user's note.
- No history migration is required.

### Phase L2: Card-Specific Review

Status: Highest-impact product slice

Purpose: turn saved history into actual study material.

Tasks:

| Item | Priority | Description | Done Evidence |
|---|---|---|---|
| Study Lens Clickthrough | P0 | Frequent/unseen/next-candidate cards open a card review view. | Web smoke |
| Card Review Filter | P0 | Show all saved readings containing the selected card. | Web smoke |
| Note vs Study Sheet Compare | P1 | For each matching reading, show user's note beside keywords/study focus. | Screenshot |
| Confused Cards | P2 | Mark pairs that the user frequently mixes up or rates low-confidence. | Learning state fixture |

Acceptance:

- A user can answer: "What have I written before about The Hermit?"
- A user can see whether their interpretation is becoming more precise over time.

### Phase L3: Recall Practice

Status: Minimal practice loop verified

Purpose: add active learning rather than passive reading.

Tasks:

| Item | Priority | Description | Done Evidence |
|---|---|---|---|
| Keyword Recall | P0 | Show a card and ask the user to type remembered keywords before revealing the study sheet answer. | Practice smoke |
| Orientation Drill | P1 | Ask the user to distinguish upright vs reversed reading tendencies. | Practice smoke |
| Slot Interpretation Drill | P1 | Given card + spread slot, ask what changes because of the slot. | `reports/web-app-smoke-20260606-203136.json`, `tests/fixtures/learning/learning-valid-v1.json` |
| Confidence Rating | P1 | User marks hard / ok / easy after reveal. | Learning state fixture |

Status note 2026-06-06:

- Keyword Recall, Orientation Drill, Slot Interpretation Drill, and Confidence Rating have a verified minimal implementation.
- Slot Interpretation Drill is available only when the Study Sheet card matches the selected table card, so it keeps real spread context.
- Learning attempts are stored separately from reading history under `onoko-arcana:desktop:learning:v1`.

Acceptance:

- Practice mode does not replace normal readings.
- User can practice without saving a full reading.
- Results are local and optional.

### Phase L4: Spaced Review Queue

Status: Minimal due queue verified / interval expansion backlog

Purpose: schedule review so card meanings are retained.

Tasks:

| Item | Priority | Description | Done Evidence |
|---|---|---|---|
| Learning State v1 | P0 | Add `onoko-arcana:desktop:learning:v1` for practice attempts and due-date derivation. | `docs/data/LEARNING_SCHEMA_V1_DRAFT.md`, `reports/web-app-check-20260606-195432.json` |
| Due Cards | P0 | Show cards due today based on last attempt and confidence, with a direct return path to recall practice. | `reports/web-app-smoke-20260606-194424.json` |
| Simple Intervals | P1 | Use hard = same day, ok = 1 day, easy = 3 days for the minimal loop; 7 and 14 day extensions require fixture coverage first. | `docs/data/LEARNING_SCHEMA_V1_DRAFT.md` |
| Export Learning State | P2 | Export/import/clear learning state separately from reading history. | `reports/web-app-smoke-20260606-194424.json`, `reports/onoko-arcana-learning-export-20260606-194424.json` |

Acceptance:

- Existing reading history remains untouched.
- Learning state can be cleared without deleting readings.

### Phase L5: Spread Tutor

Status: Backlog

Purpose: teach how card meaning changes by position and spread.

Tasks:

| Item | Priority | Description | Done Evidence |
|---|---|---|---|
| One-Card Tutor | P0 | Teach focal reading: "What is the one thing to observe?" | Smoke |
| Three-Card Tutor | P1 | Teach temporal/story flow: past, present, future. | Smoke |
| Celtic Cross Gate | P2 | Encourage simpler spreads before complex spreads when learning progress is low. | UX review |
| Story Synthesis | P2 | Ask user to write a one-paragraph synthesis after all cards are revealed. | History schema v2 proposal |

Acceptance:

- Beginner is guided toward smaller spreads first.
- Larger spreads become learning milestones, not visual clutter.

### Phase L6: Symbolism, History, And Minor Arcana Readiness

Status: Hold until Major Arcana study loop is proven

Purpose: deepen tarot literacy after Major Arcana learning works.

Tasks:

| Item | Priority | Description | Done Evidence |
|---|---|---|---|
| Symbol Glossary | P2 | Track recurring symbols: sun, moon, tower, water, sword, path, crown, etc. | Content review |
| Numerology Basics | P2 | Teach number patterns for future Minor Arcana. | Content review |
| Suit Correspondences | P2 | Prepare cups/swords/wands/pentacles schema without adding 56 cards yet. | Schema proposal |
| Minor Arcana Gate | P3 | Decide whether to add 56 cards only after L1-L5 are stable. | Roadmap review |

Acceptance:

- Minor Arcana is not started until study UI, review, and practice prove useful with 22 cards.

## Recommended Next Implementation Slice

Build **Package Settings Local Data Check + History Filter Expansion** next.

Why:

- The first-launch, recall, settings, due-card loop, Card Study Sheet, and Slot Interpretation Drill now exist.
- Learning attempts now include both `keyword_recall` and `slot_interpretation`, so the user needs better ways to find study evidence later.
- Package smoke is green, but the settings wording for local-only data and recovery should be checked in the packaged app before wider handoff.
- This keeps the core ONOKO rule intact: the app prompts observation, reflection, and recall before showing deeper study-sheet text.

Implementation outline:

1. Open packaged settings and confirm the local data wording, backup path, and recovery wording are clear.
2. Add the next history filter slice in this order: spread, note presence, question text, saved date.
3. Keep card filter as the default fast path and avoid turning Study Lens into a broad dashboard.
4. Run static check, web smoke, keyboard smoke, visual audit, Electron smoke, package smoke, and update `docs/design/GUI_OPTIMIZATION_KANBAN_2026-06-06.md`.

## Risk Notes

- Tarot meanings vary by tradition. Store ONOKO's interpretation as a local study system, and avoid pretending it is the only canonical reading.
- Reversal meanings should be nuanced.
- Study UI must not bury the table.
- Learning state should be separate from reading history to avoid migration risk.
- AI features, if added later, must be optional and should critique or prompt reflection rather than override the user's reading.
