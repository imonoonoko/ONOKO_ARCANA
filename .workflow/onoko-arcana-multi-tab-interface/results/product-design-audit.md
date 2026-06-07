# Product Design Audit

作成日: 2026-06-07

## Source Baseline

- Current UI reference: `reports/ui-visual-audit-20260607-001202/desktop-celtic-cross.png`
- Current smoke screenshot: `reports/onoko-arcana-web-app-celtic-20260607-001121.png`
- Design anchor: `assets/design/onoko-arcana-design-kanban-v1-onoko.png`

## Findings

- 右 inspector は学習機能追加後に複数の作業目的が縦積みになり、Card Study Sheet と Study Lens と History Review が同時に存在する。
- 現行の ONOKO table / note / guide / history の思想は保てているため、画面全体の再設計ではなく inspector 内の情報構造整理が妥当。
- 学習 UI は dashboard 化せず、机上の補助ノートとして残す必要がある。

## Design Decision

右 inspector に `カード`、`学習`、`履歴` の3タブを追加し、既存 DOM をタブ面へ再配置する。中央卓と左設定パネルは変更しない。

## Result

- Desktop implementation screenshot: `reports/ui-visual-audit-20260607-004524/desktop-celtic-cross.png`
- Mobile implementation screenshot: `reports/ui-visual-audit-20260607-004524/mobile-relationship-line.png`
- Visual audit: `reports/ui-visual-audit-20260607-004524/report.json` (`issueCount: 0`)
- Design QA: `design-qa.md`
