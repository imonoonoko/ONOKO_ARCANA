# UE Card Transparency Regeneration Discussion Log

## Replan Trigger - 2026-05-31 20:43

### User Input
> 背景透過が上手くできないようなので徹底的に調査して画像生成段階から再計画

### Finding
Initial card alpha failures were not only UE material issues. The generated images carried edge halos/background remnants, and the first local chroma-key cleanup made the problem worse by removing skin/hand pixels that were color-similar to the key.

### Decision
- Stop bulk generation until the alpha pipeline is validated.
- Generate cards on a flat chroma-key background, but do not globally remove all key-like pixels.
- Use connected-background detection only for locating the card body.
- Use a fixed rounded card mask for final alpha.
- Audit every UE-ready PNG before Unreal import.

---

## Character Quality Correction - 2026-05-31 20:50

### User Input
> ちなみにその生成画像だとONOKOのキャラクターイラスト部分の画質が酷い事になってます

### Finding
The v3 source images were not the primary cause of the worst white speckling. The previous alpha cleanup created transparent holes in ONOKO skin and hands. A source-vs-alpha crop proved the damage happened during post-processing.

### Decision
- Reject global chroma similarity deletion.
- Keep RGB content intact after card-body fitting.
- Replace only extreme visible magenta edge spill with black.
- Preserve fixed alpha bbox across cards.

