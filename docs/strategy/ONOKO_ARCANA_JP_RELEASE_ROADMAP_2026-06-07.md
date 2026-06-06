# ONOKO ARCANA Japan Release Roadmap

Date: 2026-06-07
Scope: Japanese-market release strategy for ONOKO ARCANA as free software, paid product, or early-access character-IP artifact.

## Decision

The best first Japanese-market release path is:

```text
GitHub Releases for transparent free distribution
+ BOOTH for Japanese creator-market landing, donations, and paid early-access
+ SNS validation through ONOKO Command Center
```

Do not start with Steam, DLsite, or Microsoft Store. They remain later expansion channels after there is evidence that users understand ONOKO ARCANA and want to download or support it.

## Why This Path

- ONOKO ARCANA is already close to a local packaged release, but the package is unsigned and still better framed as early-access/local-first software.
- BOOTH matches the Japanese creator/fan market and supports digital fan products better than a generic software marketplace.
- GitHub Releases gives public trust, version history, release notes, and checksums.
- The ONOKO project already has Command Center publishing and analytics workflows, so manual validation can start without building new infrastructure.
- Storefronts with stronger install trust should come later, after screenshots, copy, support policy, and demand are proven.

## Channel Strategy

| Channel | Use First? | Role | Notes |
|---|---:|---|---|
| GitHub Releases | Yes | Free transparent binary/archive distribution | Best for versioning, release notes, checksums, public trust. Not a sales channel. |
| BOOTH | Yes | Japanese landing + support/download sales | Best first monetization surface for creator/IP users. Use free download + paid support edition, or low-price early access. |
| itch.io | Optional | International indie mirror | Good for pay-what-you-want and early access, but weaker for Japan-first discovery than BOOTH. |
| DLsite | Later | Otaku/doujin marketplace | Strong marketplace, but user expectation and review context should be considered. Use after the product has clearer commercial packaging. |
| Microsoft Store | Later | Trust and install confidence | Useful after MSIX/store listing work. Helps with signing/update trust, but adds submission overhead. |
| Steam | Much later | Game-like product expansion | Requires stronger game/product framing, store assets, and Steam Direct fee. Not the first path. |

## Product Framing

Primary Japanese copy:

```text
ONOKO ARCANA は、ONOKOのサイバー・オラクル世界でタロットを学び、自分の読みを記録していくローカルファーストの占い卓アプリです。
```

Short positioning:

```text
未来を断言するアプリではなく、問いを立て、自分の読みを残し、あとで学び直すためのONOKO式タロット学習卓。
```

Avoid:

- "当たる占い"
- "未来を予測"
- "AIが運命を決める"
- "完全版"
- "インストーラー" when shipping the current unsigned folder package

Use:

- "早期版"
- "ローカル保存"
- "大アルカナ対応"
- "学習シート"
- "復習ノート"
- "ONOKOキャラIP連動"

## Recommended Release Shape

### Free Software Release

Use when the priority is adoption and feedback.

- GitHub Release: free Windows setup executable + SHA256, with zip fallback.
- BOOTH: free download page with "BOOST歓迎" and a supporter pack.
- Supporter pack: wallpapers, card contact sheet, PDF mini guide, development note.

Suggested price:

- Main app: free
- Supporter pack: 300-800 JPY

### Paid Product Release

Use only after screenshots, usage copy, support terms, and one short demo clip are ready.

- BOOTH: 500-1,200 JPY early-access price.
- GitHub: public release notes and checksums, but no primary paid download if paid exclusivity is needed.
- itch.io mirror if international users are expected.

Suggested first paid price:

- 500 JPY for early-access
- 800-1,200 JPY after signed installer, richer docs, and additional content

## Required Assets Before BOOTH

- 1 key visual
- 4-6 screenshots
- 1 short demo GIF or 30-60 second video
- Product description in Japanese
- "できること / できないこと"
- Setup instructions
- Windows unsigned app warning
- Local data and backup explanation
- License and asset reuse warning
- Support/contact policy
- Update policy

## 30-Day Roadmap

### Phase 0: Release Hygiene

Goal: make the current release candidate publishable without confusing users.

- Commit the release candidate intentionally.
- Push and confirm CI green.
- Publish `v0.1.0` on GitHub Releases.
- Attach setup executable, fallback zip, and SHA256 files.
- Confirm installer launch, shortcut icon, and fallback zip launch from a clean local folder.

Exit criteria:

- GitHub Release URL exists.
- Setup executable downloads, installs, and launches.
- Desktop/Start Menu shortcuts show the ONOKO ARCANA icon.
- Fallback zip downloads and launches.
- Release notes clearly say "unsigned installer".

### Phase 1: BOOTH Soft Launch

Goal: create a Japan-first landing surface.

- Create BOOTH shop/product page.
- Start as free + BOOST or 500 JPY early access.
- Add screenshots, demo clip, and disclaimer.
- Link GitHub Release for transparency if free.
- Add supporter pack if paid download is not used.

Exit criteria:

- BOOTH page can explain the product in 15 seconds.
- User can download without needing GitHub knowledge.
- Support/contact and update expectations are visible.

### Phase 2: ONOKO SNS Validation

Goal: test whether users care about ONOKO as a character-IP layer, not just tarot software.

Use 3 series only:

- 今日の問い
- ONOKO ARCANAカード紹介
- 制作ログ/更新ノート

Record:

- impressions
- likes
- comments
- saves/shares where available
- downloads
- BOOTH views
- BOOST/purchases
- qualitative comments

Exit criteria:

- 20-30 posts published.
- At least 10 downloads or wishlists.
- At least 3 qualitative comments or reactions that mention ONOKO, tarot, design, or usefulness.

### Phase 3: Decision Review

Goal: choose the next investment based on evidence.

Continue ARCANA if:

- People download it.
- Users understand the study/reflection use case.
- Screenshots/card posts get engagement.

Shift toward character content if:

- ONOKO posts perform better than app posts.
- People react to the character/design but not the software.

Pause paid expansion if:

- Downloads are low.
- No one understands the product.
- Support burden appears before signal.

### Phase 4: Store Expansion

Only after validation:

- Microsoft Store if trust/install friction is the main blocker.
- DLsite if the audience behaves like doujin/otaku software buyers.
- itch.io if international indie users respond.
- Steam only if the product becomes more game-like, with stronger trailer/store assets.

## Creative Production Tasks

Use Creative Production in this order:

1. Positioning
   - Clarify which angle wins: tarot study, ONOKO fan item, cyber-oracle tool, or creative reflection journal.
2. Offers
   - Test free app + supporter pack, paid early access, and bundle structures.
3. Ads
   - Create SNS image directions for X, BOOTH thumbnail, and release announcement.
4. Assets
   - Produce key visual, BOOTH header, screenshot captions, and supporter-pack images.

## Immediate Next Work

1. Finalize GitHub Release.
2. Create BOOTH product copy and image checklist.
3. Generate or capture screenshots.
4. Create BOOTH page draft.
5. Start 30-day SNS validation from ONOKO Command Center.
6. Review data after 30 days before building new major features.

## Source Notes

- BOOTH announced a service fee change to `5.6% + 45円` from 2025-10-28.
- DLsite circle registration and listing are free, and their example shows a 1,000 JPY product producing a 600 JPY wholesale amount plus tax paid to the circle.
- itch.io supports pay-what-you-want above a minimum price, including a zero minimum, and configurable open revenue sharing.
- Microsoft Store supports traditional desktop apps and revenue choices, including own commerce for non-gaming apps or Microsoft commerce fees.
- Steam Direct requires a 100 USD app fee per app, recoupable after 1,000 USD adjusted gross revenue.
