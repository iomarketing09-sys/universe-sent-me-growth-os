"""El experiment log se alimenta solo desde las capturas de métricas."""

from __future__ import annotations

import csv
from pathlib import Path

from modules.intelligence import experiment_log


def _read(tenant: Path) -> list[dict]:
    with (tenant / "tenants" / "demo" / "experiment_log.csv").open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_bank(root: Path, *, legacy: bool = False) -> Path:
    base = root / "tenants" / "demo"
    path = base / "hypothesis_bank.csv" if legacy else base / "experiments" / "hypothesis_bank.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "hypothesis_id,descripcion,metrica_principal,criterio_exito,estado,"
        "fecha_creacion,fecha_cierre,observaciones_ids,veredicto_final\n"
        "HB-001,Prueba,shares_por_interaccion,>15%,Activa,2026-11-05,,,\n",
        encoding="utf-8-sig",
    )
    return path


def _read_bank(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def test_sync_crea_una_fila_por_pieza(tmp_path):
    experiment_log.sync_observation(
        "demo",
        meta_id="123",
        plataforma="Instagram",
        contenido_referencia="Wilfred",
        fecha="2026-11-05",
        slot="10:00",
        window="E24",
        interacciones=7,
        base_path=tmp_path,
    )
    rows = _read(tmp_path)
    assert len(rows) == 1
    assert rows[0]["meta_id"] == "123"
    assert rows[0]["estado_publicacion"] == "Publicada"
    assert rows[0]["interacciones_24h"] == "7"
    assert rows[0]["interacciones_totales"] == "7"
    assert rows[0]["fuente"] == "metrics_snapshot"


def test_sync_actualiza_ventanas_sin_duplicar(tmp_path):
    for window, value in (("E24", 5), ("E72", 12), ("E72", 9)):
        experiment_log.sync_observation(
            "demo",
            meta_id="123",
            plataforma="Facebook",
            window=window,
            interacciones=value,
            base_path=tmp_path,
        )
    rows = _read(tmp_path)
    assert len(rows) == 1
    assert rows[0]["interacciones_24h"] == "5"
    assert rows[0]["interacciones_72h"] == "12"
    assert rows[0]["interacciones_totales"] == "12"


def test_sync_sin_meta_id_no_escribe(tmp_path):
    assert experiment_log.sync_observation("demo", meta_id="", base_path=tmp_path) is None
    assert not (tmp_path / "tenants" / "demo" / "experiment_log.csv").exists()


def test_sync_guarda_y_vincula_hypothesis_id(tmp_path):
    bank_path = _write_bank(tmp_path)

    observation = experiment_log.sync_observation(
        "demo",
        meta_id="123",
        hypothesis_id="HB-001",
        experiment_id="EXP-2026-11-HB-001",
        window="E24",
        interacciones=7,
        base_path=tmp_path,
    )

    assert observation is not None
    row = _read(tmp_path)[0]
    assert row["hypothesis_id"] == "HB-001"
    assert row["experiment_id"] == "EXP-2026-11-HB-001"
    bank = _read_bank(bank_path)[0]
    assert bank["observaciones_ids"] == observation.observacion_id


def test_hypothesis_bank_prefiere_experiments_y_respeta_legado(tmp_path):
    canonical = _write_bank(tmp_path)
    legacy = _write_bank(tmp_path, legacy=True)
    assert experiment_log.get_hypothesis_bank_path("demo", tmp_path) == canonical

    canonical.unlink()
    assert experiment_log.get_hypothesis_bank_path("demo", tmp_path) == legacy


def test_link_es_bidireccional_e_idempotente(tmp_path):
    bank_path = _write_bank(tmp_path)
    observation = experiment_log.sync_observation(
        "demo", meta_id="123", window="E24", interacciones=4, base_path=tmp_path
    )
    assert observation is not None

    assert experiment_log.link_observation_to_hypothesis(
        "demo", "HB-001", observation.observacion_id, base_path=tmp_path
    )
    assert experiment_log.link_observation_to_hypothesis(
        "demo", "HB-001", observation.observacion_id, base_path=tmp_path
    )

    assert _read(tmp_path)[0]["hypothesis_id"] == "HB-001"
    assert _read_bank(bank_path)[0]["observaciones_ids"] == observation.observacion_id


def test_close_por_meta_id_es_humano_y_deja_veredicto(tmp_path):
    observation = experiment_log.sync_observation(
        "demo", meta_id="123", window="E24", interacciones=4, base_path=tmp_path
    )
    assert observation is not None

    closed = experiment_log.close_observation_by_meta_id(
        "demo",
        "123",
        veredicto="L1 senal",
        conclusion="Direccion consistente, muestra chica",
        proxima_accion="Repetir 5+5",
        base_path=tmp_path,
    )

    assert closed is not None
    row = _read(tmp_path)[0]
    assert row["veredicto"] == "L1 senal"
    assert row["conclusion"] == "Direccion consistente, muestra chica"
    assert row["proxima_accion"] == "Repetir 5+5"


def test_run_capture_cycle_alimenta_el_log(tmp_path, monkeypatch):
    from modules.intelligence import metrics_snapshot as ms

    tenant = tmp_path / "tenants" / "demo"
    tenant.mkdir(parents=True)
    (tenant / "publication_log_week2.csv").write_text(
        "date,time,platform,piece,asset_filename,status,publication_id,hypothesis_id,experiment_id\n"
        "2026-11-05,10:00,Instagram,Wilfred,2608001.jpg,published,999,HB-001,EXP-2026-11-HB-001\n",
        encoding="utf-8",
    )

    snapshot = ms.MetricsSnapshot(
        publication_id="999",
        tenant_id="demo",
        platform="Instagram",
        window="E24",
        reactions=4,
        comments=1,
        status="Captured",
    )
    monkeypatch.setattr(ms, "load_tenant_env", lambda tenant_id: {"META_ACCESS_TOKEN": "t", "FB_PAGE_ID": "1"})
    monkeypatch.setattr(ms, "ensure_snapshots_for_publications", lambda tenant_id: [])
    monkeypatch.setattr(ms, "get_page_token", lambda *args: "pt")
    monkeypatch.setattr(ms, "get_ig_id", lambda *args: "ig")
    monkeypatch.setattr(ms, "get_pending_snapshots", lambda tenant_id: [snapshot])
    monkeypatch.setattr(ms, "capture_snapshot", lambda *args: snapshot)
    monkeypatch.setattr(ms, "upsert_snapshot", lambda *args: None)
    monkeypatch.setattr(ms, "load_page_metrics", lambda tenant_id: [])
    monkeypatch.setattr(ms, "capture_page_insights_daily", lambda *args: [])
    monkeypatch.setattr(ms, "load_publication_log", lambda tenant_id: [{
        "publication_id": "999",
        "platform": "Instagram",
        "piece": "Wilfred",
        "date": "2026-11-05",
        "time": "10:00",
        "hypothesis_id": "HB-001",
        "experiment_id": "EXP-2026-11-HB-001",
    }])

    import os

    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        result = ms.run_capture_cycle("demo")
    finally:
        os.chdir(cwd)

    assert result["observations"] == 1
    rows = _read(tmp_path)
    assert len(rows) == 1
    assert rows[0]["meta_id"] == "999"
    assert rows[0]["interacciones_24h"] == "5"
    assert rows[0]["hypothesis_id"] == "HB-001"
    assert rows[0]["experiment_id"] == "EXP-2026-11-HB-001"
