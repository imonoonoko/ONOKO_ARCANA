# Implementation Brief

## Recommended 60-Day Path

### Week 1: Lock Public Positioning

- Add `docs/strategy/ONOKO_IP_POSITIONING_2026-06-07.md` or equivalent public/internal strategy note.
- Choose one public tagline.
- Prepare 4-6 ARCANA screenshots.
- Write short store/release copy in Japanese first.

### Week 2: Release ARCANA Candidate

- Review current dirty tree.
- Commit release candidate.
- Push and wait for CI.
- Publish `v0.1.0`.
- Create a simple release/download page.

### Weeks 3-6: Run SNS Validation

- Use ONOKO Command Center to run 30 manual posts.
- Use 3 series only:
  - 今日の問い
  - ONOKO ARCANA card/study snippets
  - ORACLE world-noise snapshot teasers
- Record results in the existing analytics surface.
- Do not add more channels until the first 30 posts are logged.

### Weeks 7-8: Decide From Evidence

Decision options:

- Continue ARCANA if downloads and comments exist.
- Shift to SNS/character if posts get attention but downloads do not.
- Use ORACLE teaser if world-noise visuals outperform tarot content.
- Pause monetization if neither content nor app gets signal.

## Project Role Map

| Project | Role | Public Now? | Why |
|---|---|---:|---|
| ONOKO Command Center | IP operations cockpit | No | Internal planning, assets, publishing, analytics |
| ONOKO ARCANA | First public product | Yes, after CI | Concrete app with release candidate |
| ONOKO ORACLE | Signature lab/teaser | Partial | Strong identity, higher explanation burden |
| Yoitomoshi Art Generator | Production infrastructure | No | Personal generation/model workflow tool |
| ONOKO LoRA | Controlled asset source | No | License/IP/safety review needed |

## Copy Direction

Short product framing:

```text
ONOKO ARCANA is a local-first tarot study table from the ONOKO cyber-oracle world. Draw cards, write your own reading, compare with study notes, and revisit your history.
```

Short character framing:

```text
ONOKO turns noise into questions. She does not decide your future; she helps you notice what to look at next.
```

## Immediate Backlog

1. Confirm whether the first public store is GitHub Releases, itch.io, BOOTH, or a simple landing page.
2. Commit and publish ARCANA v0.1.0.
3. Prepare screenshots and one short demo clip.
4. Add ONOKO IP positioning copy to the ARCANA release page.
5. Start the 30-post validation cycle.
6. After 30 posts, review Command Center analytics and decide the next product slice.
