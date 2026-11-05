import csv

import pytest

from modules.intelligence.planner import META_IMPORT_FIELDS, Planner, ScheduleItem


def _item(
    date,
    time,
    asset="meme.png",
    caption="copy",
    type_="PHOTO",
    hypothesis_id="",
    experiment_id="",
):
    return ScheduleItem(
        tenant_id="universe",
        slot_id=f"universe-{date}-{time}",
        date=date,
        time=time,
        datetime_utc="",
        type=type_,
        asset_filename=asset,
        caption=caption,
        hypothesis_id=hypothesis_id,
        experiment_id=experiment_id,
    )


def _rows(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def test_write_meta_import_crea_calendario(tmp_path):
    target = tmp_path / "meta_import.csv"
    summary = Planner("universe").write_meta_import(
        [_item("2026-11-05", "19:00"), _item("2026-11-06", "10:00", asset="b.png")],
        target,
    )

    assert summary["written"] == 2
    rows = _rows(target)
    assert list(rows[0]) == META_IMPORT_FIELDS
    assert [row["Date (YYYY-MM-DD)"] for row in rows] == ["2026-11-05", "2026-11-06"]
    assert rows[0]["Timezone"] == "America/Matamoros"


def test_write_meta_import_es_idempotente_y_reemplaza_por_slot(tmp_path):
    target = tmp_path / "meta_import.csv"
    planner = Planner("universe")
    planner.write_meta_import([_item("2026-11-05", "19:00")], target)
    summary = planner.write_meta_import(
        [_item("2026-11-05", "19:00", caption="nuevo copy")], target
    )

    assert summary == {"written": 1, "replaced": 1, "total": 1, "path": str(target)}
    assert _rows(target)[0]["Caption"] == "nuevo copy"


def test_write_meta_import_rechaza_hora_invalida_y_no_escribe(tmp_path):
    target = tmp_path / "meta_import.csv"
    with pytest.raises(ValueError, match="fecha u hora inválida"):
        Planner("universe").write_meta_import([_item("2026-11-05", "25:00")], target)
    assert not target.exists()


def test_write_meta_import_rechaza_duplicado_y_sin_asset(tmp_path):
    target = tmp_path / "meta_import.csv"
    planner = Planner("universe")
    with pytest.raises(ValueError, match="slot duplicado"):
        planner.write_meta_import(
            [_item("2026-11-05", "19:00"), _item("2026-11-05", "19:00", asset="otro.png")],
            target,
        )
    with pytest.raises(ValueError, match="falta Media URL"):
        planner.write_meta_import([_item("2026-11-05", "19:00", asset="")], target)


def test_replace_reescribe_sin_mezclar(tmp_path):
    target = tmp_path / "meta_import.csv"
    planner = Planner("universe")
    planner.write_meta_import([_item("2026-11-05", "19:00")], target)
    summary = planner.write_meta_import(
        [_item("2026-11-06", "10:00")], target, merge=False
    )

    assert summary["total"] == 1
    assert _rows(target)[0]["Date (YYYY-MM-DD)"] == "2026-11-06"


def test_meta_import_lleva_pre_registro_de_hipotesis(tmp_path):
    target = tmp_path / "meta_import.csv"
    Planner("universe").write_meta_import(
        [_item(
            "2026-11-05",
            "19:00",
            hypothesis_id="HB-UNI-003",
            experiment_id="EXP-2026-11-HB-UNI-003-T",
        )],
        target,
    )

    row = _rows(target)[0]
    assert row["Hypothesis ID"] == "HB-UNI-003"
    assert row["Experiment ID"] == "EXP-2026-11-HB-UNI-003-T"
