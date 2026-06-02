# 1. Purpose

## 目的

Phase 1の「一枚引き占い卓」を、次の作業ターンで迷わずUE Editor上に成立させるため、実装前の接続前提、作業順、検証基準、Codex引き継ぎ情報を固定する。

## 背景

ONOKO ARCANAは、PC上で物理カードなしにタロット学習と一枚引き占いを行うアプリである。ユーザーは問いを入力し、カードを引き、まず自分の解釈を書き、その後に学習ガイドを表示して比較し、履歴として保存する。

前段階で、V5 Major Arcana 22枚と裏面は採用候補としてそろい、C++ Runtime層、SaveGame層、ViewModel層、HUD親クラスのsmoke testは通っている。残る主課題は、実際のUE Editor上でカードActor、TableController、UMG Widget Blueprintを接続し、ユーザー操作として縦断スライスを証明することである。

## 成功状態

- Codexが次回以降も同じ入口から作業を再開できる。
- UE Editorを開く前に、必要なファイル、Plugin、素材、既存テスト結果、既知リスクを機械的に確認できる。
- Blueprint/UMG配線時に、命名、接続先、押下フロー、SaveGame検証で迷わない。
- Python actor spawn crashを再踏破せず、手動Editor配線に集中できる。
