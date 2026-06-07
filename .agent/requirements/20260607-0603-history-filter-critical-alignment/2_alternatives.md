# Alternatives

## A. Block on manual installer smoke

Reject for now. It requires a clean Windows user or VM that is not available in the current environment.

## B. Implement all filters at once

Reject for this slice. Spread, note, question, and date filters together would increase UI density and smoke complexity.

## C. Implement the first filter slice

Accept. Add spread and note-presence filters while preserving the existing card-specific review filter as the fast path. Leave question text and saved date filters for the next slice.
