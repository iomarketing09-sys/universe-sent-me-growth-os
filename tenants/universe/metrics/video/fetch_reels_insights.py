#!/usr/bin/env python3
"""
Extractor de métricas oficiales de Reels (Facebook e Instagram) para Universe Sent Me.
Lee PAGE_ACCESS_TOKEN y FB_PAGE_ID desde tenants/universe/.env.
"""

import os, sys, json, csv, requests
from pathlib import Path

def load_env(path: Path) -> dict:
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip("'\"")
    return env

def get_ig_insights(api_url, m_id, headers):
    for metric_set in ["views,reach,saved,shares,total_interactions", "plays,reach,saved,shares,total_interactions"]:
        url = f"{api_url}/{m_id}/insights"
        r = requests.get(url, headers=headers, params={"metric": metric_set})
        if r.status_code == 200:
            data = r.json().get("data", [])
            res = {}
            for item in data:
                vals = item.get("values", [{}])
                res[item.get("name")] = vals[0].get("value", 0) if vals else 0
            return res
    return {}

def main():
    base_dir = Path("/home/universe-sent-me/growth-os")
    env_path = base_dir / "tenants/universe/.env"
    env = load_env(env_path)

    page_id = env.get("FB_PAGE_ID")
    token = env.get("PAGE_ACCESS_TOKEN") or env.get("META_ACCESS_TOKEN")

    if not page_id or not token:
        print("Error: Faltan credenciales en tenants/universe/.env")
        sys.exit(1)

    api_url = "https://graph.facebook.com/v20.0"
    headers = {"Authorization": f"Bearer {token}"}
    reels_data = []

    print("=" * 65)
    print(" EXTRACTOR DE MÉTRICAS DE REELS (FACEBOOK & INSTAGRAM)")
    print(f" Page ID: {page_id}")
    print("=" * 65)

    # 1. FACEBOOK REELS
    print(f"\n1. Consultando Reels de Facebook (Página: {page_id})...")
    fb_res = requests.get(
        f"{api_url}/{page_id}/video_reels",
        headers=headers,
        params={"fields": "id,description,created_time,length,permalink_url", "limit": 30}
    )
    
    if fb_res.status_code == 200:
        items = fb_res.json().get("data", [])
        print(f"   -> Encontrados {len(items)} Reels en Facebook.")
        for item in items:
            v_id = item.get("id")
            desc = (item.get("description") or "").replace("\n", " ")[:40]
            created = (item.get("created_time") or "")[:10]
            length = item.get("length", 0)
            permalink = item.get("permalink_url", "")

            ins_res = requests.get(
                f"{api_url}/{v_id}/video_insights",
                headers=headers,
                params={"metric": "total_video_views,total_video_views_organic,post_video_avg_time_watched,total_video_reactions_by_type_total"}
            )
            
            views = 0
            watch_time = 0
            reactions = 0
            if ins_res.status_code == 200:
                for m in ins_res.json().get("data", []):
                    name = m.get("name")
                    vals = m.get("values", [{}])
                    v = vals[0].get("value", 0) if vals else 0
                    if name in ["total_video_views", "total_video_views_organic"] and not views:
                        views = v
                    elif name == "post_video_avg_time_watched":
                        watch_time = round(v / 1000, 2) if v > 100 else v
                    elif name == "total_video_reactions_by_type_total":
                        reactions = sum(v.values()) if isinstance(v, dict) else v
            else:
                v_node = requests.get(f"{api_url}/{v_id}", headers=headers, params={"fields": "views,likes.summary(true)"})
                if v_node.status_code == 200:
                    v_data = v_node.json()
                    views = v_data.get("views", 0)
                    reactions = v_data.get("likes", {}).get("summary", {}).get("total_count", 0)

            reels_data.append({
                "Fecha": created,
                "Plataforma": "Facebook Reels",
                "Video_ID": v_id,
                "Titulo_Concepto": desc or "(Sin caption)",
                "Duracion_Seg": length,
                "Plays_Views": views,
                "Watch_Time_Prom_Seg": watch_time,
                "Reacciones": reactions,
                "Shares": 0,
                "Comentarios": 0,
                "Permalink": permalink
            })

    # 2. INSTAGRAM REELS
    print("\n2. Consultando Reels de Instagram...")
    acc_res = requests.get(f"{api_url}/{page_id}?fields=instagram_business_account", headers=headers)
    ig_id = acc_res.json().get("instagram_business_account", {}).get("id") if acc_res.status_code == 200 else None

    if ig_id:
        print(f"   -> Cuenta Instagram detectada: {ig_id}")
        ig_res = requests.get(
            f"{api_url}/{ig_id}/media",
            headers=headers,
            params={"fields": "id,caption,media_type,media_product_type,timestamp,permalink,like_count,comments_count,shares_count,total_views_count", "limit": 30}
        )
        if ig_res.status_code == 200:
            media_items = ig_res.json().get("data", [])
            ig_reels = [m for m in media_items if m.get("media_product_type") == "REELS" or m.get("media_type") == "VIDEO"]
            print(f"   -> Encontrados {len(ig_reels)} Reels en Instagram.")

            for m in ig_reels:
                m_id = m.get("id")
                caption = (m.get("caption") or "").replace("\n", " ")[:40]
                created = (m.get("timestamp") or "")[:10]
                likes = m.get("like_count", 0)
                comments = m.get("comments_count", 0)
                permalink = m.get("permalink", "")

                views = m.get("total_views_count", 0) or 0
                shares = m.get("shares_count", 0) or 0

                reels_data.append({
                    "Fecha": created,
                    "Plataforma": "Instagram Reels",
                    "Video_ID": m_id,
                    "Titulo_Concepto": caption or "(Sin caption)",
                    "Duracion_Seg": "",
                    "Plays_Views": views,
                    "Watch_Time_Prom_Seg": "",
                    "Reacciones": likes,
                    "Shares": shares,
                    "Comentarios": comments,
                    "Permalink": permalink
                })

    # Guardar en CSV
    out_dir = base_dir / "tenants/universe/metrics"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "metrics_video_log.csv"

    fieldnames = ["Fecha", "Plataforma", "Video_ID", "Titulo_Concepto", "Duracion_Seg", "Plays_Views", "Watch_Time_Prom_Seg", "Reacciones", "Shares", "Comentarios", "Permalink"]
    existing_rows = {}
    if out_file.exists():
        with open(out_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row.get("Plataforma"), row.get("Video_ID"))
                existing_rows[key] = row
    for r in reels_data:
        key = (r["Plataforma"], r["Video_ID"])
        existing_rows[key] = r
    final_rows = list(existing_rows.values())
    final_rows.sort(key=lambda x: x.get("Fecha", ""), reverse=True)

    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_rows)

    print("\n" + "=" * 65)
    print(f"RESUMEN FINAL: {len(reels_data)} videos procesados")
    print(f"Archivo guardado en: {out_file}")
    print("=" * 65)
    for r in reels_data:
        print(f"[{r['Plataforma']}] {r['Fecha']} | Views: {r['Plays_Views']} | Likes: {r['Reacciones']} | Shares: {r['Shares']} | {r['Titulo_Concepto']}")

if __name__ == "__main__":
    main()
