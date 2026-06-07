# Packet C Result

Implemented:

- `historySpreadFilter`
- `historyNoteFilter`
- Compact filter controls in the existing history filter slot.
- Original history indexes preserved through filtered rows for restore/delete.
- Row data attributes for smoke verification.

Kept:

- Card-specific filter remains the study fast path.
- Card comparison blocks appear only for card-filter matches.
