import html
import json
import os
from pathlib import Path


ROOT = Path("assets/generated/card-production-v5-full")
DATA = Path("data/major-arcana-cards.json")
AUDIT = ROOT / "reports" / "v5-alpha-audit.json"
OUT = ROOT / "reports" / "v5-full-major-review.html"


def rel(path: Path) -> str:
    return Path(os.path.relpath(path, OUT.parent)).as_posix()


def card_rows():
    cards = json.loads(DATA.read_text(encoding="utf-8"))
    rows = [
        {
            "label": "BACK / カード裏面",
            "stem": "card-back-onoko-v5",
            "raw": ROOT / "raw" / "card-back-onoko-v5-source.png",
            "alpha": ROOT / "alpha" / "card-back-onoko-v5-alpha.png",
            "kind": "back",
        }
    ]
    for card in cards:
        number = card["number"]
        slug = card["slug"]
        stem = f"major-{number}-{slug}-onoko-v5"
        rows.append(
            {
                "label": f"{number} {card['englishName']} / {card['japaneseName']}",
                "stem": stem,
                "raw": ROOT / "raw" / f"{stem}-source.png",
                "alpha": ROOT / "alpha" / f"{stem}-alpha.png",
                "kind": "front",
            }
        )
    return rows


def audit_by_name():
    if not AUDIT.exists():
        return {}
    payload = json.loads(AUDIT.read_text(encoding="utf-8"))
    items = {}
    for item in payload.get("results", []):
        items[Path(item["path"]).name] = item
    return items


def main():
    rows = card_rows()
    audit = audit_by_name()
    OUT.parent.mkdir(parents=True, exist_ok=True)

    cards_html = []
    for row in rows:
        alpha_name = row["alpha"].name
        a = audit.get(alpha_name, {})
        badge = "OK" if a.get("ok") else "CHECK"
        bbox = a.get("alphaBbox", [])
        visible_green = a.get("visibleGreenPixels", "?")
        strong_green = a.get("visibleStrongKeyPixels", "?")
        cards_html.append(
            f"""
            <article class="card {html.escape(row['kind'])}">
              <header>
                <h2>{html.escape(row['label'])}</h2>
                <span class="badge">{html.escape(badge)}</span>
              </header>
              <div class="media">
                <figure>
                  <img src="{html.escape(rel(row['alpha']))}" alt="{html.escape(row['label'])} alpha">
                  <figcaption>alpha PNG</figcaption>
                </figure>
                <figure>
                  <img src="{html.escape(rel(row['raw']))}" alt="{html.escape(row['label'])} raw">
                  <figcaption>raw chroma source</figcaption>
                </figure>
              </div>
              <dl>
                <dt>Size</dt><dd>{a.get('size', ['?', '?'])[0]} x {a.get('size', ['?', '?'])[1]}</dd>
                <dt>Alpha bbox</dt><dd>{html.escape(str(bbox))}</dd>
                <dt>Green leak</dt><dd>visible {visible_green} / strong-key {strong_green}</dd>
              </dl>
            </article>
            """
        )

    body = "\n".join(cards_html)
    html_text = f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ONOKO ARCANA V5 Major Arcana Review</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #0b0e13;
      --panel: #151923;
      --line: #2a3240;
      --text: #e9eef8;
      --muted: #9fb0c8;
      --blue: #37a3ff;
      --gold: #d6a94a;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", system-ui, sans-serif;
      background: var(--bg);
      color: var(--text);
    }}
    main {{
      width: min(1480px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 28px 0 48px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 28px;
      letter-spacing: 0;
    }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin: 20px 0 28px;
    }}
    .summary a, .summary div {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px 14px;
      background: var(--panel);
      color: var(--text);
      text-decoration: none;
    }}
    .summary strong {{
      display: block;
      color: var(--blue);
      font-size: 20px;
      margin-bottom: 4px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(330px, 1fr));
      gap: 18px;
    }}
    .card {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      padding: 14px;
    }}
    .card header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 12px;
    }}
    h2 {{
      margin: 0;
      font-size: 15px;
      line-height: 1.35;
      letter-spacing: 0;
    }}
    .badge {{
      flex: 0 0 auto;
      border: 1px solid var(--gold);
      color: var(--gold);
      border-radius: 999px;
      padding: 3px 8px;
      font-size: 12px;
      font-weight: 700;
    }}
    .media {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }}
    figure {{
      margin: 0;
      border-radius: 6px;
      overflow: hidden;
      background:
        linear-gradient(45deg, #b9bcc3 25%, transparent 25%),
        linear-gradient(-45deg, #b9bcc3 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, #b9bcc3 75%),
        linear-gradient(-45deg, transparent 75%, #b9bcc3 75%),
        #e7e8ec;
      background-position: 0 0, 0 10px, 10px -10px, -10px 0;
      background-size: 20px 20px;
    }}
    img {{
      display: block;
      width: 100%;
      height: auto;
    }}
    figcaption {{
      padding: 6px 8px;
      background: rgba(7, 10, 16, 0.82);
      color: var(--muted);
      font-size: 12px;
    }}
    dl {{
      display: grid;
      grid-template-columns: 90px 1fr;
      gap: 5px 10px;
      margin: 12px 0 0;
      color: var(--muted);
      font-size: 12px;
    }}
    dt {{ color: var(--text); }}
    dd {{ margin: 0; word-break: break-word; }}
    @media (max-width: 760px) {{
      .summary {{ grid-template-columns: 1fr 1fr; }}
      .media {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main>
    <h1>ONOKO ARCANA V5 Major Arcana Review</h1>
    <p>Clean-start V5 draft assets: 22 major arcana fronts plus one matching card back. Alpha QA checks size, transparent border, and chroma-key leakage.</p>
    <section class="summary">
      <div><strong>{len(rows)}</strong>assets</div>
      <div><strong>1024x1536</strong>canvas</div>
      <a href="{html.escape(rel(ROOT / 'reports' / 'v5-alpha-contact-sheet-major-00-21-back.png'))}">contact sheet</a>
      <a href="{html.escape(rel(ROOT / 'reports' / 'v5-character-crop-report-major-00-21.png'))}">crop QA sheet</a>
    </section>
    <section class="grid">
      {body}
    </section>
  </main>
</body>
</html>
"""
    OUT.write_text(html_text, encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
