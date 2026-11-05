import csv
import json
from datetime import datetime, timedelta, timezone

from modules.intelligence.historical_baseline import rank_publications

FIELDS = [
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


def _tenant(tmp_path, snapshots, contexts=None, log_rows=None):
    tenant = tmp_path / "tenants" / "universe"
    (tenant / "metrics").mkdir(parents=True)
    with (tenant / "metrics" / "metrics_snapshot_log.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(snapshots)
    if contexts is not None:
        (tenant / "publication_contexts.json").write_text(
            json.dumps(contexts), encoding="utf-8"
        )
    if log_rows is not None:
        with (tenant / "publication_log_week2.csv").open(
            "w", encoding="utf-8-sig", newline=""
        ) as handle:
            writer = csv.DictWriter(
                handle, fieldnames=["date", "time", "publication_id"]
            )
            writer.writeheader()
            writer.writerows(log_rows)
    return tmp_path


def _snapshot(pid, window, interactions, *, days_ago=5, status="Captured"):
    target = datetime.now(timezone.utc) - timedelta(days=days_ago)
    return {
        "snapshot_id": f"{pid}-{window}",
        "publication_id": pid,
        "tenant_id": "universe",
        "platform": "Facebook",
        "window": window,
        "target_at_utc": target.isoformat(),
        "captured_at_utc": target.isoformat(),
        "comments": "1",
        "shares": "2",
        "saved": "3",
        "total_interactions": str(interactions),
        "status": status,
    }


def test_rank_usa_la_ventana_mas_completa_y_agrupa_personaje(tmp_path):
    base = _tenant(
        tmp_path,
        [
            _snapshot("p1", "E24", 10),
            _snapshot("p1", "LIFETIME_BACKFILL", 100),
            _snapshot("p2", "E72", 40),
        ],
        contexts={"p1": {"publication_id": "p1", "character": "Elara"}},
        log_rows=[{"date": "2026-10-30", "time": "09:30", "publication_id": "p1"}],
    )

    report = rank_publications("universe", base_path=base, days=30)

    assert report["publications"] == 2
    assert report["top"][0]["publication_id"] == "p1"
    assert report["top"][0]["window"] == "LIFETIME_BACKFILL"
    assert report["top"][0]["score"] == 100 + 2 + 3
    assert report["top"][0]["hour_band"] == "06-11"
    assert report["by_character"][0]["character"] == "Elara"


def test_rank_ignora_pendientes_y_fuera_de_rango(tmp_path):
    base = _tenant(
        tmp_path,
        [
            _snapshot("p1", "E24", 10),
            _snapshot("p2", "E24", 99, status="Pending"),
            _snapshot("p3", "E24", 500, days_ago=400),
        ],
    )

    report = rank_publications("universe", base_path=base, days=30)

    assert report["publications"] == 1
    assert report["top"][0]["publication_id"] == "p1"


def test_rank_sin_datos_reporta_nota(tmp_path):
    base = _tenant(tmp_path, [])
    report = rank_publications("universe", base_path=base)

    assert report["publications"] == 0
    assert report["notes"]
    assert report["top"] == []


def test_rank_respeta_ventana_forzada(tmp_path):
    base = _tenant(tmp_path, [_snapshot("p1", "E24", 10), _snapshot("p1", "E72", 90)])
    report = rank_publications("universe", base_path=base, window="E24")

    assert report["publications"] == 1
    assert report["top"][0]["window"] == "E24"
