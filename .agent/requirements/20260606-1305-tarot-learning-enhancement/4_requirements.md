# Requirements

## User Stories

1. As a beginner, I want to open one card and learn its upright/reversed meanings, symbols, and reflection questions.
2. As a learner, I want to guess a card's meaning before seeing the guide so I practice recall.
3. As a learner, I want to see which Major Arcana I have not encountered yet.
4. As a learner, I want to review every past reading involving a specific card.
5. As a learner, I want to compare my own notes with guide text after I write them.
6. As a learner, I want the app to suggest what to study next based on my history.
7. As a learner, I want simple quizzes that mix cards, orientations, and spread slots.
8. As a returning user, I want a review queue that brings back older cards before I forget them.

## Functional Requirements

- The app shall expose a Major Arcana study library reachable without disrupting the reading table.
- The app shall keep "write own interpretation first" as the default flow.
- The app shall render card-level study data from local structured data.
- The app shall compute study progress from local history and optional learning state.
- The app shall support card-specific review filters.
- The app shall support quiz/retrieval practice without requiring network access.
- The app shall preserve existing `onoko-arcana:desktop:history:v1` data.

## Data Requirements

Extend card data in a future schema without breaking current fields:

- `meaning.upright.short`
- `meaning.upright.long`
- `meaning.reversed.short`
- `meaning.reversed.long`
- `symbols[]`
- `reflectionQuestions[]`
- `commonMisreads[]`
- `historyNote`
- `learningPrompts[]`

Add a separate local learning state key rather than mixing study metadata into reading history:

- `onoko-arcana:desktop:learning:v1`

## Acceptance Criteria

- Existing Web smoke still passes.
- Visual audit remains issueCount 0.
- Existing history import/export remains compatible.
- Study surfaces are usable at desktop and mobile widths.
- The first implementation slice can ship without Minor Arcana data.

