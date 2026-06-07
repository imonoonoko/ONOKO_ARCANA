# ONOKO ARCANA critical roadmap alignment and history filters

## Goal
Align the roadmap with the critical current-state assessment, then implement the next locally verifiable history filter slice without depending on a clean Windows VM.

## Success Criteria
- Manual installer smoke is explicitly marked as external-environment pending rather than fully verified.
- The next local implementation slice adds history filtering by spread and note presence while preserving the existing card review filter.
- Requirements and workflow artifacts explain scope, non-goals, risks, and verification.
- Static check, web smoke, keyboard smoke, visual audit, Electron smoke, and package smoke are run or any skipped check is recorded with a reason.

## Current Context
- ONOKO ARCANA v1.x is locked to the Web/Electron 2D tabletop.
- GitHub Release v0.1.3 has automated installer/package evidence, but no clean Windows user/VM manual smoke.
- Card-specific history review, study sheet comparison, recall practice, slot drill, and local learning data controls are already verified.

## Constraints
- Do not publish, deploy, sign, or change external release state.
- Do not remove fallback zip language.
- Do not treat clean Windows manual installer behavior as verified in this environment.
- Do not start Minor Arcana, Unreal, MSIX, Store, auto update, or code signing work.

## Risks
- Filter UI can make the inspector feel like a dashboard instead of a reading table.
- Filtering visible rows by index can break restore/delete if original history indexes are not preserved.
- Documentation can overstate automated evidence as real-user installer evidence.

## Approval Required
No approval required for local non-destructive document edits, app edits, and verification. Approval would be required for publishing, signing, deleting user data, or changing release artifacts.

## Work Packets
- Packet A: Critical roadmap alignment and residual-risk wording.
- Packet B: Requirements for history filter slice.
- Packet C: Implementation of spread and note-presence filters.
- Packet D: Smoke/visual/keyboard verification and final integration.

## Integration Policy
Accept changes only when they keep card-specific review as the fast path, preserve original history indexes for restore/delete, and keep manual installer smoke as pending.

## Verification
Run the repo static check first, then web smoke. If those pass, run keyboard smoke, visual audit, Electron smoke, and package smoke because UI and history behavior changed.

## Reusable Artifacts
This workflow can be reused when a roadmap-critical assessment creates both status-document corrections and a small implementation slice.
