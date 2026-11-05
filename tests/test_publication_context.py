"""El contexto de publicación se escribe al publicar, sin abrir imágenes."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

from modules.intelligence import publication_context
from modules.social import ig_scheduler
from modules.social.ig_scheduler import REUSE_NOT_APPLICABLE, IgScheduler, ScheduleItem
from modules.social.meta_publisher import MetaResponse, record_scheduled_publication


def _tenant(tmp_path: Path) -> Path:
    tenant = tmp_path / "tenants" / "universe"
    tenant.mkdir(parents=True)
    return tenant


def _contexts(tenant: Path) -> dict:
    return json.loads((tenant / "publication_contexts.json").read_text(encoding="utf-8"))


def test_record_publication_deriva_personaje_y_meme_text(tmp_path):
    tenant = _tenant(tmp_path)

    result = publication_context.record_publication(
        tenant,
        post_id="1036844829507460_122167383825072582",
        asset_filename="2608001 - Wilfred - No vivas del que diran.jpeg",
        caption="Wilfred acaba de darse cuenta de algo",
        published_at="2026-11-05T10:00:00-06:00",
    )

    assert result["character"] == "Wilfred"
    assert result["meme_text"] == "No vivas del que diran"
    stored = _contexts(tenant)["1036844829507460_122167383825072582"]
    assert stored["caption"] == "Wilfred acaba de darse cuenta de algo"
    assert stored["asset_ref"] == "2608001 - Wilfred - No vivas del que diran.jpeg"


def test_record_publication_conserva_contexto_visual_y_actualiza_alias(tmp_path):
    tenant = _tenant(tmp_path)
    full_id = "1036844829507460_122167383825072582"
    (tenant / "publication_contexts.json").write_text(
        json.dumps({
            full_id: {
                "publication_id": full_id,
                "asset_ref": "2608001 - Wilfred - No vivas del que diran.jpeg",
                "character": "Wilfred",
                "meme_text": "No vivas del que diran",
                "visual_context": "Wilfred mirando su sombra",
                "caption": "copy viejo",
                "published_at": "",
            },
            "122167383825072582": {
                "publication_id": full_id,
                "asset_ref": "2608001 - Wilfred - No vivas del que diran.jpeg",
                "character": "Wilfred",
                "meme_text": "No vivas del que diran",
                "visual_context": "Wilfred mirando su sombra",
                "caption": "copy viejo",
                "published_at": "",
            },
        }),
        encoding="utf-8",
    )

    publication_context.record_publication(
        tenant,
        post_id=full_id,
        asset_filename="2608001 - Wilfred - No vivas del que diran.jpeg",
        caption="copy nuevo",
        published_at="2026-11-05T10:00:00-06:00",
    )

    contexts = _contexts(tenant)
    assert set(contexts) == {full_id, "122167383825072582"}
    for value in contexts.values():
        assert value["visual_context"] == "Wilfred mirando su sombra"
        assert value["caption"] == "copy nuevo"
        assert value["published_at"] == "2026-11-05T10:00:00-06:00"


def test_record_publication_usa_transcripcion_si_el_nombre_no_trae_chiste(tmp_path):
    tenant = _tenant(tmp_path)
    with (tenant / "assets_meme_text.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["filename", "meme_text"])
        writer.writeheader()
        writer.writerow({
            "filename": "260503 - Evana+Kiri.png",
            "meme_text": "Silencio reconfortante",
        })

    result = publication_context.record_publication(
        tenant,
        post_id="short_123",
        asset_filename="260503 - Evana+Kiri.png",
        caption="",
    )

    assert result["meme_text"] == "Silencio reconfortante"


def test_ig_scheduler_escribe_contexto_al_publicar(tmp_path, monkeypatch):
    tenant = _tenant(tmp_path)
    scheduler = IgScheduler.__new__(IgScheduler)
    scheduler.base_path = tmp_path
    scheduler.persist_state = False
    scheduler._historical_baseline = MagicMock()
    publisher = MagicMock()
    publisher.publish.return_value = "122180013555072582"
    scheduler.publishers = {"universe": publisher}
    scheduler.historical_reuse_report = lambda *args, **kwargs: {
        "status": REUSE_NOT_APPLICABLE,
        "reason": "",
    }
    monkeypatch.setattr(
        ig_scheduler,
        "preflight_tenant",
        lambda *args, **kwargs: SimpleNamespace(ok=True, issues=[]),
    )
    item = ScheduleItem(
        tenant_id="universe",
        date_str="2026-11-05",
        time_str="10:00",
        media_filename="2608001 - Wilfred - No vivas del que diran.jpeg",
        caption="Wilfred acaba de darse cuenta de algo",
        post_type="photo",
        datetime_local=datetime(2026, 11, 5, 10, 0, tzinfo=timezone.utc),
        datetime_utc=datetime(2026, 11, 5, 16, 0, tzinfo=timezone.utc),
    )

    post_id = scheduler.process_item(item)

    assert post_id == "122180013555072582"
    stored = _contexts(tenant)[post_id]
    assert stored["character"] == "Wilfred"
    assert stored["meme_text"] == "No vivas del que diran"
    assert stored["caption"] == item.caption


def test_record_scheduled_publication_repara_contexto_si_el_log_ya_existe(tmp_path):
    tenant = _tenant(tmp_path)
    slot = {
        "datetime_utc": "2026-11-05T15:00:00+00:00",
        "description": "Wilfred acaba de darse cuenta de algo",
        "source_filename": "2608001 - Wilfred - No vivas del que diran.jpeg",
        "asset_ref": "2608001",
    }
    response = MetaResponse(success=True, status="scheduled", post_id="123")

    record_scheduled_publication(tenant, slot, response)
    (tenant / "publication_contexts.json").unlink()

    record_scheduled_publication(tenant, slot, response)

    stored = _contexts(tenant)["123"]
    assert stored["character"] == "Wilfred"
    assert stored["meme_text"] == "No vivas del que diran"
    assert stored["caption"] == slot["description"]
