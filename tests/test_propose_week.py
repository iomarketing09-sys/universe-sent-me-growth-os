import csv
import json
from datetime import datetime, timedelta, timezone

from modules.intelligence.planner import parse_asset_filename, propose_week


def _write_snapshots(tenant_dir, rows):
    (tenant_dir / "metrics").mkdir(parents=True, exist_ok=True)
    fields = [
        "snapshot_id",
        "publication_id",
        "tenant_id",
        "platform",
        "window",
        "target_at_utc",
        "captured_at_utc",
        "comments",
        "shares",
        "saved",
        "total_interactions",
        "status",
    ]
    with (tenant_dir / "metrics" / "metrics_snapshot_log.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for index, (publication_id, interactions) in enumerate(rows):
            target = datetime.now(timezone.utc) - timedelta(days=5)
            writer.writerow(
                {
                    "snapshot_id": f"s{index}",
                    "publication_id": publication_id,
                    "tenant_id": "universe",
                    "platform": "Facebook",
                    "window": "E72",
                    "target_at_utc": target.isoformat(),
                    "captured_at_utc": target.isoformat(),
                    "comments": "0",
                    "shares": "0",
                    "saved": "0",
                    "total_interactions": str(interactions),
                    "status": "Captured",
                }
            )


def test_parse_asset_filename_tolera_variantes():
    parsed = parse_asset_filename("2611002 - Evan+Kiri - Kiri: hola - chau.jpg")
    assert parsed["code"] == "2611002"
    assert parsed["characters"] == ["Evan", "Kiri"]
    assert parsed["meme_text"] == "Kiri: hola - chau"

    ganso = parse_asset_filename("2611004 - El Ganso - La gente subestima.jpg")
    assert ganso["characters"] == ["Ganso"]

    ancient = parse_asset_filename("Captura de pantalla 2026-08-10.png")
    assert ancient["code"] == ""
    assert ancient["characters"] == []


def test_propuesta_elige_banda_por_mediana_y_rota_personajes(tmp_path):
    tenant = tmp_path / "tenants" / "universe"
    tenant.mkdir(parents=True)
    _write_snapshots(tenant, [("p1", 1000), ("p2", 1), ("p3", 1)])
    _write_snapshots(
        tenant,
        [("p4", 30), ("p5", 30), ("p6", 30)],
    )
    with (tenant / "publication_log_week2.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=["date", "time", "publication_id"])
        writer.writeheader()
        for publication_id in ("p1", "p2", "p3"):
            writer.writerow({"date": "2026-10-20", "time": "09:00", "publication_id": publication_id})
        for publication_id in ("p4", "p5", "p6"):
            writer.writerow({"date": "2026-10-21", "time": "13:00", "publication_id": publication_id})
    (tenant / "publication_contexts.json").write_text(
        json.dumps(
            {
                "p4": {"publication_id": "p4", "character": "Wilfred"},
                "p5": {"publication_id": "p5", "character": "Maeve"},
                "p6": {"publication_id": "p6", "character": "Evan"},
            }
        ),
        encoding="utf-8",
    )

    assets = tmp_path / "assets"
    assets.mkdir()
    for name in (
        "2611005 - Wilfred - chiste uno.jpg",
        "2611003 - Maeve - chiste dos.jpg",
        "2611015 - Evan+Elara - chiste tres.jpg",
    ):
        (assets / name).write_bytes(b"x")

    proposal = propose_week(
        "universe",
        start_date="2026-11-05",
        days=3,
        assets_dir=assets,
        base_path=tmp_path,
    )

    assert proposal["hour"] == "13:30"
    assert proposal["band"] == "12-16"
    filenames = [item.asset_filename for item in proposal["items"]]
    assert len(filenames) == len(set(filenames)) == 3
    assert proposal["items"][0].date == "2026-11-05"
    assert proposal["items"][2].date == "2026-11-07"
    assert proposal["items"][0].hashtags.startswith("#WilfredUSM")


def test_propuesta_sin_assets_lo_reporta(tmp_path):
    tenant = tmp_path / "tenants" / "universe"
    tenant.mkdir(parents=True)
    proposal = propose_week(
        "universe", start_date="2026-11-05", days=2, assets_dir=tmp_path / "vacio", base_path=tmp_path
    )

    assert proposal["items"] == []
    assert any("Sin assets" in note for note in proposal["notes"])
