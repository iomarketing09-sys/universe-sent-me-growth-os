"""Reglas de la parrilla: reuse 2-3 por día, sin horas consecutivas, pilar."""

import csv

from modules.intelligence.planner import SLOT_HOURS, propose_week


def _new_assets(folder, count=8):
    folder.mkdir(parents=True, exist_ok=True)
    for index in range(count):
        (folder / f"26120{index:02d} - Universe - chiste nuevo {index}.jpg").write_bytes(b"x")


def _reuse_assets(folder, count=10):
    month = folder / "05 Mayo"
    month.mkdir(parents=True, exist_ok=True)
    for index in range(count):
        (month / f"2605{index:02d} - Wilfred.png").write_bytes(b"x")


def _proposal(tmp_path, days=2):
    assets = tmp_path / "nuevos"
    reuse = tmp_path / "reuse"
    _new_assets(assets)
    _reuse_assets(reuse)
    return propose_week(
        "universe",
        start_date="2026-11-05",
        days=days,
        hours=list(SLOT_HOURS),
        assets_dir=assets,
        reuse_dir=reuse,
        base_path=tmp_path,
    )


def test_parrilla_llena_todas_las_horas(tmp_path):
    proposal = _proposal(tmp_path)
    assert len(proposal["items"]) == len(SLOT_HOURS) * 2
    assert [item.time for item in proposal["items"][:6]] == list(SLOT_HOURS)


def test_reuse_dos_por_dia_y_nunca_consecutivo(tmp_path):
    proposal = _proposal(tmp_path)
    by_day = {}
    for item in proposal["items"]:
        by_day.setdefault(item.date, []).append(item)

    for items in by_day.values():
        flags = [item.origin == "reuse" for item in items]
        assert 2 <= sum(flags) <= 3
        assert not any(a and b for a, b in zip(flags, flags[1:]))


def test_hora_estelar_nunca_es_reuse(tmp_path):
    proposal = _proposal(tmp_path)
    star = [item for item in proposal["items"] if item.time == "13:30"]
    assert star and all(item.origin == "nuevo" for item in star)


def test_no_repite_asset_en_el_periodo(tmp_path):
    proposal = _proposal(tmp_path)
    names = [item.asset_filename for item in proposal["items"]]
    assert len(names) == len(set(names))


def test_cada_slot_trae_pilar(tmp_path):
    proposal = _proposal(tmp_path)
    assert all(item.pillar for item in proposal["items"])


def test_usa_transcripcion_cuando_el_nombre_no_trae_chiste(tmp_path):
    from modules.intelligence.planner import load_meme_text_index, reuse_assets

    tenant = tmp_path / "tenants" / "universe"
    tenant.mkdir(parents=True)
    (tenant / "assets_meme_text.csv").write_text(
        "asset_ref,filename,folder,meme_text,status,model,source\n"
        "260548,260548 - Wilfred.png,05 Mayo,ME VALE VRGA QUIEN LO ESTE HACIENDO,transcrito,auto/vision,vision\n",
        encoding="utf-8-sig",
    )
    reuse = tmp_path / "reuse" / "05 Mayo"
    reuse.mkdir(parents=True)
    (reuse / "260548 - Wilfred.png").write_bytes(b"x")

    index = load_meme_text_index("universe", base_path=tmp_path)
    assets = reuse_assets(tmp_path / "reuse", index)
    assert assets[0]["meme_text"] == "ME VALE VRGA QUIEN LO ESTE HACIENDO"


def test_el_nombre_gana_sobre_la_transcripcion(tmp_path):
    from modules.intelligence.planner import load_meme_text_index, reuse_assets

    tenant = tmp_path / "tenants" / "universe"
    tenant.mkdir(parents=True)
    (tenant / "assets_meme_text.csv").write_text(
        "asset_ref,filename,folder,meme_text,status,model,source\n"
        "2608001,2608001 - Wilfred - No vivas del que diran.jpeg,08 Agosto,OTRA COSA,transcrito,x,vision\n",
        encoding="utf-8-sig",
    )
    reuse = tmp_path / "reuse"
    (reuse / "08 Agosto").mkdir(parents=True)
    (reuse / "08 Agosto" / "2608001 - Wilfred - No vivas del que diran.jpeg").write_bytes(b"x")

    index = load_meme_text_index("universe", base_path=tmp_path)
    assets = reuse_assets(reuse, index)
    assert assets[0]["meme_text"] == "No vivas del que diran"
