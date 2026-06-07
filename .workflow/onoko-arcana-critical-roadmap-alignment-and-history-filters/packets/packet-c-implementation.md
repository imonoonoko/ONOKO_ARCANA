# Packet C: Implementation

Objective: Implement the first history filter slice.

Do:

- Add spread and note filters to the existing history filter slot.
- Preserve original history indexes for restore/delete.
- Update smoke coverage.

Do not:

- Change history schema.
- Delete or migrate user localStorage.
