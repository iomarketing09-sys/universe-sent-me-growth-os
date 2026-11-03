"""Plantilla HTML A4 del reporte de cliente.

Autocontenida: sin dependencias externas ni fuentes remotas, para que el HTML
se imprima igual desde cualquier navegador (A4, listo para guardar como PDF).
"""

from __future__ import annotations

import html
from datetime import date
from typing import Any, Dict, List

from modules.intelligence.campaign_report import ad_names, _short_name


INK = "#1B2029"
PAPER = "#FBF7EF"
ORANGE = "#D66E12"
DEEP = "#8F4209"
RULE = "#DCD3C2"
MUTED = "#5B564C"
GOLD = "#FDE9C4"


def _money(value: float) -> str:
    return f"${value:,.2f}"


def _pct(part: float, whole: float) -> float:
    return (part / whole * 100) if whole else 0


def _numbers(bundle: Dict[str, Any]) -> Dict[str, Any]:
    capture = bundle["capture"]
    meta_ids = bundle["meta_ids"]
    conversations = bundle["conversations"]
    spend = float(capture.get("total_spend") or 0)
    wa = int(conversations.get("total") or 0)
    latest = int((bundle.get("conversations_latest") or conversations).get("total") or 0)
    return {
        "spend": spend,
        "budget": float((meta_ids.get("campaign") or {}).get("lifetime_budget") or 0) / 100,
        "impressions": sum(int(ad.get("impressions") or 0) for ad in capture.get("ads") or []),
        "clicks": sum(int(ad.get("clicks") or 0) for ad in capture.get("ads") or []),
        "meta_conv": int(capture.get("total_conversations") or 0),
        "meta_cpa": float(capture.get("blended_cost_per_conversation") or 0),
        "wa": wa,
        "cost_person": spend / wa if wa else 0,
        "latest": latest,
        "cost_latest": spend / latest if latest else 0,
        "depth": conversations.get("depth") or {},
        "start": str((meta_ids.get("campaign") or {}).get("start_time", ""))[:10],
        "stop": str((meta_ids.get("campaign") or {}).get("stop_time", ""))[:10],
    }


def _rows(bundle: Dict[str, Any]) -> List[Dict[str, Any]]:
    capture = bundle["capture"]
    conversations = bundle["conversations"].get("per_ad") or {}
    names = ad_names(bundle["meta_ids"])
    rows = []
    for ad in capture.get("ads") or []:
        ad_id = str(ad.get("ad_id"))
        spend = float(ad.get("spend") or 0)
        wa = int(conversations.get(ad_id, 0))
        rows.append(
            {
                "name": html.escape(names.get(ad_id) or _short_name(str(ad.get("ad_name") or ad_id))),
                "spend": spend,
                "meta_conv": int(ad.get("conversations") or 0),
                "meta_cpa": float(ad.get("cost_per_conversation") or 0),
                "wa": wa,
                "cost": spend / wa if wa else 0,
            }
        )
    return sorted(rows, key=lambda row: row["spend"], reverse=True)


def _reading(bundle: Dict[str, Any], numbers: Dict[str, Any], rows: List[Dict[str, Any]]) -> List[str]:
    minimum = max(3, round(numbers["wa"] * 0.1))
    eligible = [(row["cost"], row["name"], row["wa"]) for row in rows if row["wa"] >= minimum]
    notes = []
    if eligible:
        cost, name, count = min(eligible)
        notes.append(
            f"<strong>{name}</strong> fue el creativo más eficiente: {_money(cost)} por persona, "
            f"con {count} conversaciones."
        )
    low = [row["name"] for row in rows if 0 < row["wa"] < minimum]
    if low:
        notes.append(
            f"{' y '.join(low)} recibieron poca entrega: su costo todavía no es una conclusión."
        )
    top = max(rows, key=lambda row: row["wa"], default=None)
    if top and top["wa"]:
        notes.append(
            f"<strong>{top['name']}</strong> concentró {top['wa']} conversaciones, "
            f"el {_pct(top['wa'], numbers['wa']):.0f}% del total atribuido."
        )
    deep = int(numbers["depth"].get("3+", 0))
    if deep:
        notes.append(
            f"{deep} de {numbers['wa']} conversaciones pasaron de tres mensajes: "
            "el interés no se quedó en el clic."
        )
    return notes


def render_client_html(bundle: Dict[str, Any]) -> str:
    capture = bundle["capture"]
    numbers = _numbers(bundle)
    rows = _rows(bundle)
    notes = _reading(bundle, numbers, rows)
    title = html.escape(str(capture.get("campaign_name") or bundle["slug"]))
    max_spend = max((row["spend"] for row in rows), default=1) or 1
    today = date.today().isoformat()

    ad_rows = "\n".join(
        f"""<tr>
  <td class="ad">{row['name']}<span class="bar"><i style="width:{_pct(row['spend'], max_spend):.0f}%"></i></span></td>
  <td>{_money(row['spend'])}</td>
  <td>{row['meta_conv']}</td>
  <td>{_money(row['meta_cpa']) if row['meta_conv'] else '—'}</td>
  <td>{row['wa']}</td>
  <td class="strong">{_money(row['cost']) if row['wa'] else '—'}</td>
</tr>"""
        for row in rows
    )

    note_items = "\n".join(f"<li>{note}</li>" for note in notes)

    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Reporte · {title}</title>
<style>
  @page {{ size: A4; margin: 16mm 15mm; }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  body {{
    font-family: "DejaVu Sans", "Segoe UI", system-ui, sans-serif;
    color: #1B2029;
    background: #FBF7EF;
    font-size: 10.5pt;
    line-height: 1.5;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .sheet {{ max-width: 180mm; margin: 0 auto; padding: 4mm 0 0; }}
  header {{ display: flex; justify-content: space-between; align-items: flex-start;
            border-bottom: 2px solid #1B2029; padding-bottom: 8px; }}
  .brand {{ font-family: "DejaVu Serif", Georgia, serif; font-size: 15pt;
            letter-spacing: .18em; text-transform: uppercase; }}
  .brand span {{ color: #D66E12; }}
  .meta {{ text-align: right; font-size: 8.5pt; color: #5B564C; line-height: 1.7; }}

  .hero {{ display: grid; grid-template-columns: 1.15fr .85fr; gap: 10mm;
           padding: 12mm 0 10mm; align-items: end; }}
  .hero h1 {{ font-family: "DejaVu Serif", Georgia, serif; font-size: 25pt;
              font-weight: normal; line-height: 1.15; margin: 0 0 6px; }}
  .hero p {{ margin: 0; color: #4A463E; max-width: 34ch; }}
  .figure {{ border-left: 3px solid #D66E12; padding-left: 6mm; }}
  .figure .n {{ font-family: "DejaVu Serif", Georgia, serif; font-size: 52pt;
                line-height: .95; color: #D66E12; }}
  .figure .l {{ font-size: 9pt; letter-spacing: .04em; color: #4A463E; }}

  .kpis {{ display: grid; grid-template-columns: repeat(4, 1fr);
           border-top: 1px solid #DCD3C2; border-bottom: 1px solid #DCD3C2; }}
  .kpi {{ padding: 5mm 0 5mm 4mm; border-left: 1px solid #E6DFD0; }}
  .kpi:first-child {{ border-left: 0; padding-left: 0; }}
  .kpi .v {{ font-family: "DejaVu Serif", Georgia, serif; font-size: 17pt; }}
  .kpi .k {{ font-size: 8.3pt; color: #5B564C; }}

  section {{ padding-top: 9mm; }}
  h2 {{ font-family: "DejaVu Serif", Georgia, serif; font-size: 13pt; font-weight: normal;
        margin: 0 0 4mm; padding-bottom: 2mm; border-bottom: 1px solid #DCD3C2; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 9.5pt; }}
  th {{ text-align: right; font-weight: normal; font-size: 8.2pt; color: #5B564C;
        padding: 0 0 2mm; border-bottom: 1px solid #DCD3C2; }}
  th:first-child, td:first-child {{ text-align: left; }}
  td {{ text-align: right; padding: 2.4mm 0; border-bottom: 1px solid #EDE7DA; }}
  td.ad {{ width: 34%; }}
  td.strong {{ font-weight: bold; }}
  .bar {{ display: block; height: 3px; background: #EFE7D6; margin-top: 4px; }}
  .bar i {{ display: block; height: 3px; background: #D66E12; }}

  .two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 9mm; }}
  ul.notes {{ margin: 0; padding-left: 5mm; }}
  ul.notes li {{ margin-bottom: 3mm; }}
  .callout {{ background: #FDE9C4; border-left: 3px solid #D66E12; padding: 4mm 5mm; }}
  .callout p {{ margin: 0; }}
  .small {{ font-size: 8.4pt; color: #5B564C; }}

  footer {{ margin-top: 12mm; padding-top: 3mm; border-top: 1px solid #DCD3C2;
            display: flex; justify-content: space-between; font-size: 8pt; color: #6B655A; }}
</style>
</head>
<body>
<div class="sheet">
  <header>
    <div class="brand">Flexi<span>.</span></div>
    <div class="meta">
      {title}<br>
      {numbers['start']} — {numbers['stop']}<br>
      Reporte al {today}
    </div>
  </header>

  <div class="hero">
    <div>
      <h1>Lo que la campaña<br>trajo a la tienda</h1>
      <p>Anuncios con botón directo a WhatsApp para Piedras Negras. El resultado no es
      el clic: es la conversación que empieza después.</p>
    </div>
    <div class="figure">
      <div class="n">{numbers['wa']}</div>
      <div class="l">personas escribieron desde un anuncio</div>
    </div>
  </div>

  <div class="kpis">
    <div class="kpi"><div class="v">{_money(numbers['spend'])}</div><div class="k">invertidos de {_money(numbers['budget'])}</div></div>
    <div class="kpi"><div class="v">{numbers['impressions']:,}</div><div class="k">personas alcanzadas</div></div>
    <div class="kpi"><div class="v">{_money(numbers['meta_cpa'])}</div><div class="k">por conversación (Meta)</div></div>
    <div class="kpi"><div class="v">{_money(numbers['cost_person'])}</div><div class="k">por persona (WhatsApp)</div></div>
  </div>

  <section>
    <h2>Los creativos</h2>
    <table>
      <thead>
        <tr><th>Anuncio</th><th>Inversión</th><th>Conv. Meta</th><th>Costo Meta</th><th>Personas WA</th><th>Costo WA</th></tr>
      </thead>
      <tbody>
        {ad_rows}
      </tbody>
    </table>
  </section>

  <section class="two">
    <div>
      <h2>Lo que dicen los números</h2>
      <ul class="notes">
        {note_items}
      </ul>
    </div>
    <div>
      <h2>Cómo se mide</h2>
      <p class="small">Meta reporta {numbers['meta_conv']} conversaciones al corte de 72 horas.
      WhatsApp registra {numbers['wa']} personas que escribieron en esa misma ventana.
      Son dos definiciones distintas y aquí se muestran sin ajustar.</p>
      <div class="callout">
        <p>Al día de hoy el número subió a <strong>{numbers['latest']} personas</strong>,
        con un costo de {_money(numbers['cost_latest'])} por persona.</p>
      </div>
    </div>
  </section>

  <footer>
    <span>Flexi · Piedras Negras</span>
    <span>Campaña {numbers['start']} — {numbers['stop']}</span>
  </footer>
</div>
</body>
</html>
"""
