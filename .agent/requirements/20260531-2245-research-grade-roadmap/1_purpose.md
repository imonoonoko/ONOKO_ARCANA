# ONOKO ARCANA Research-Grade Roadmap Purpose

## Problem

ONOKO ARCANAはUnreal Engine版の基礎と大アルカナ素材を持ち始めているが、カード裏面比率、背景透過漏れ、UE上の影との混同、AI生成後処理によるONOKO人物品質劣化が発生した。現状のまま全カードを量産すると、素材負債が増える。

## Target User

- タロットカードを持っていなくてもPCで占いたいユーザー。
- タロットの意味を、操作、記録、比較を通して学びたいユーザー。
- ONOKO世界観のサイバー占い卓で、リッチだが実用的な占いソフトを使いたいユーザー。
- 開発者として、Unreal Engineに取り込める一貫したカード素材とQA手順が必要な制作者。

## Current Workaround

- 既存の大アルカナPNGと透過処理済みPNGを個別に作り、UEへ手動/スクリプトで取り込んでいる。
- HTMLレポートとUnreal Phase 0 Mapで目視確認している。
- ただし、人物画質、alpha bbox、裏面幅、影、生成ハローが混ざり、合否基準がまだ不十分。

## Why Now

ユーザーが「UnrealEngine用に全てのONOKOタロットカードを再生成」と進めようとした直後に、透過漏れとキャラクター画質劣化が確認された。ここでロードマップを更新しないと、低品質素材を大量に作り直すリスクが高い。

## Desired Outcome

全カード生成へ進む前に、カード素材制作とUnreal取り込みの正式パイプラインを固定する。最初は大アルカナ22枚を本番品質へ持っていき、学習/占いの縦断スライスを完成させる。

## Success Definition

- v2ロードマップが `docs/roadmap/ONOKO_ARCANA_RESEARCH_GRADE_ROADMAP_V2_2026-05-31.md` として残る。
- 要件、範囲、実装ブリーフが `.agent/requirements/20260531-2245-research-grade-roadmap/` に残る。
- 次にやる作業が「V4 layered card pipeline prototype」として明確になる。

