#!/usr/bin/env python3
"""Contract tests for the canonical GrowthOS content inventory."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "core" / "growthos-core"))

from growthos.core.models import Piece
from growthos.scripts.audit_inventory import InventoryAuditor
from growthos.storage.csv_adapter import CSVAdapter


SOURCE = REPO_ROOT / "GrowthOS" / "Content_Inventory.csv"
EXPECTED_COLUMNS = CSVAdapter.COLUMN_ORDER[Piece]
LEGACY_ALIASES = {
    "Asset_Ref": "asset_ref",
    "Asset_Filename": "asset_filename",
    "Drive_ID": "drive_id",
    "Estado_Canon": "estado_canon",
    "Estado_Produccion": "estado_produccion",
    "Estado_Publicacion": "estado_publicacion",
    "Ultima_Sincronizacion": "ultima_sincronizacion",
    "Motivo_Revision_Normalizado": "motivo_revision_normalizado",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_overrides(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("id", "campo", "valor_original", "propuesta", "resuelto"),
        )
        writer.writeheader()
        writer.writerows(rows)


@pytest.fixture(scope="module")
def canonical_files(tmp_path_factory: pytest.TempPathFactory) -> dict[str, object]:
    output = tmp_path_factory.mktemp("canonical-inventory")
    auditor = InventoryAuditor(SOURCE, output)
    stats = auditor.run()
    return {
        "canonical": output / "Content_Inventory_CANONICAL.csv",
        "reconciliation": output / "Content_Inventory_RECONCILIATION.csv",
        "overrides": output / "Content_Inventory_OVERRIDES.csv",
        "stats": stats,
        "auditor": auditor,
    }


def test_source_has_85_unique_ids() -> None:
    rows = read_rows(SOURCE)
    ids = [row["id"] for row in rows]
    assert len(rows) == 85
    assert len(ids) == len(set(ids))


def test_canonical_contract_has_47_snake_case_columns(canonical_files) -> None:
    with canonical_files["canonical"].open(encoding="utf-8", newline="") as handle:
        columns = csv.DictReader(handle).fieldnames

    assert columns == EXPECTED_COLUMNS
    assert len(columns) == 47
    assert all(column == column.lower() for column in columns)
    assert not set(LEGACY_ALIASES).intersection(columns)
    assert "es_historico" in columns


def test_canonical_preserves_all_ids(canonical_files) -> None:
    canonical_rows = read_rows(canonical_files["canonical"])
    source_rows = read_rows(SOURCE)

    canonical_ids = [row["id"] for row in canonical_rows]
    source_ids = [row["id"] for row in source_rows]
    assert len(canonical_rows) == 85
    assert canonical_ids == source_ids
    assert len(set(canonical_ids)) == 85


def test_reconciliation_traces_every_canonical_field(canonical_files) -> None:
    rows = read_rows(canonical_files["reconciliation"])
    stats = canonical_files["stats"]
    assert len(rows) == 85 * 47
    assert set(row["campo"] for row in rows) == set(EXPECTED_COLUMNS)

    categories = ("A", "B", "C_REAL", "NONE_EMPTY", "FREE_TEXT")
    counted = sum(1 for row in rows if row["categoria"] in categories)
    assert counted == len(rows)
    for category in categories:
        actual = sum(1 for row in rows if row["categoria"] == category)
        assert actual == stats[category]


def test_free_text_is_copied_verbatim(canonical_files) -> None:
    canonical = {row["id"]: row for row in read_rows(canonical_files["canonical"])}
    for row in read_rows(canonical_files["reconciliation"]):
        if row["categoria"] != "FREE_TEXT":
            continue
        assert canonical[row["id"]][row["campo"]] == row["valor_original"]
        assert row["regla_aplicada"] == "copy_verbatim"


def test_c_real_requires_human_override(canonical_files) -> None:
    rows = read_rows(canonical_files["reconciliation"])
    c_real = [row for row in rows if row["categoria"] == "C_REAL"]
    assert len(c_real) == canonical_files["stats"]["C_REAL"]

    for row in c_real:
        assert row["valor_canonico"] == ""
        assert row["regla_aplicada"] == ""
        assert row["requiere_revision"] == "true"


def test_a_b_and_none_empty_are_deterministic(canonical_files) -> None:
    rows = read_rows(canonical_files["reconciliation"])
    stats = canonical_files["stats"]
    for category in ("A", "B"):
        subset = [row for row in rows if row["categoria"] == category]
        assert len(subset) == stats[category]
        assert all(row["regla_aplicada"] for row in subset)
        assert all(row["requiere_revision"] == "false" for row in subset)

    none_empty = [row for row in rows if row["categoria"] == "NONE_EMPTY"]
    assert len(none_empty) == stats["NONE_EMPTY"]
    assert all(row["valor_original"] == "" for row in none_empty)
    assert all(row["valor_canonico"] == "" for row in none_empty)
    assert all(row["requiere_revision"] == "false" for row in none_empty)


def test_overrides_cover_all_current_c_real(canonical_files) -> None:
    reconciliation = read_rows(canonical_files["reconciliation"])
    overrides = read_rows(canonical_files["overrides"])
    c_real_keys = {
        (row["id"], row["campo"])
        for row in reconciliation
        if row["categoria"] == "C_REAL"
    }
    override_keys = {(row["id"], row["campo"]) for row in overrides}
    assert override_keys == c_real_keys


def test_legacy_headers_are_aliased_and_export_is_snake_case(tmp_path: Path) -> None:
    source = tmp_path / "legacy.csv"
    source.write_text(
        "id,Titulo,Asset_Ref,Estado_Canon\n"
        "CNT-9999,Pieza legacy,asset-001,Aprobado\n",
        encoding="utf-8",
    )

    pieces = CSVAdapter.import_csv(Piece, source)
    assert len(pieces) == 1
    assert pieces[0].titulo == "Pieza legacy"
    assert pieces[0].asset_ref == "asset-001"
    assert pieces[0].estado_canon == "Aprobado"

    exported = tmp_path / "exported.csv"
    CSVAdapter.export_csv(pieces, exported, model_type=Piece)
    with exported.open(encoding="utf-8", newline="") as handle:
        columns = csv.DictReader(handle).fieldnames
    assert columns == EXPECTED_COLUMNS
    assert "Asset_Ref" not in columns


def test_valid_override_applies_to_canonical_and_reconciliation(tmp_path: Path) -> None:
    output = tmp_path / "output"
    overrides = tmp_path / "overrides.csv"
    write_overrides(
        overrides,
        [
            {
                "id": "CNT-001",
                "campo": "estado",
                "valor_original": "Original",
                "propuesta": "Propuesta",
                "resuelto": "Publicado",
            }
        ],
    )

    auditor = InventoryAuditor(SOURCE, output, overrides)
    stats = auditor.run()

    assert auditor.overrides[("CNT-001", "estado")] == "Publicado"
    assert stats["OVERRIDE"] >= 1
    canonical = {row["id"]: row for row in read_rows(output / "Content_Inventory_CANONICAL.csv")}
    assert canonical["CNT-001"]["estado"] == "Publicado"


def test_invalid_override_is_rejected(tmp_path: Path) -> None:
    output = tmp_path / "output"
    overrides = tmp_path / "overrides.csv"
    write_overrides(
        overrides,
        [
            {
                "id": "CNT-001",
                "campo": "estado",
                "valor_original": "Original",
                "propuesta": "Propuesta",
                "resuelto": "Valor_Invalido",
            }
        ],
    )

    with pytest.raises(ValueError, match="Override inválido") as exc_info:
        InventoryAuditor(SOURCE, output, overrides).run()

    assert "estado" in str(exc_info.value)
    assert "Valor_Invalido" in str(exc_info.value)


def test_proposal_without_resuelto_stays_pending(canonical_files, tmp_path: Path) -> None:
    first_c_real = next(
        row
        for row in read_rows(canonical_files["reconciliation"])
        if row["categoria"] == "C_REAL"
    )
    output = tmp_path / "output"
    overrides = tmp_path / "overrides.csv"
    write_overrides(
        overrides,
        [
            {
                "id": first_c_real["id"],
                "campo": first_c_real["campo"],
                "valor_original": first_c_real["valor_original"],
                "propuesta": "Pendiente de decisión",
                "resuelto": "",
            }
        ],
    )

    auditor = InventoryAuditor(SOURCE, output, overrides)
    stats = auditor.run()

    assert (first_c_real["id"], first_c_real["campo"]) not in auditor.overrides
    assert stats["OVERRIDE_PENDING"] == 1
    saved = {
        (row["id"], row["campo"]): row
        for row in read_rows(output / "Content_Inventory_OVERRIDES.csv")
    }
    assert saved[(first_c_real["id"], first_c_real["campo"])]["propuesta"] == "Pendiente de decisión"


def test_existing_output_overrides_are_read_by_default(tmp_path: Path) -> None:
    output = tmp_path / "output"
    InventoryAuditor(SOURCE, output).run()

    overrides_path = output / "Content_Inventory_OVERRIDES.csv"
    write_overrides(
        overrides_path,
        [
            {
                "id": "CNT-001",
                "campo": "estado",
                "valor_original": "",
                "propuesta": "Aprobado por Fernando",
                "resuelto": "Publicado",
            }
        ],
    )

    auditor = InventoryAuditor(SOURCE, output)
    auditor.run()
    assert auditor.input_overrides_path == overrides_path
    assert auditor.overrides[("CNT-001", "estado")] == "Publicado"
    saved = {(row["id"], row["campo"]): row for row in read_rows(overrides_path)}
    assert saved[("CNT-001", "estado")]["resuelto"] == "Publicado"


def test_stale_empty_override_is_removed(tmp_path: Path) -> None:
    output = tmp_path / "output"
    InventoryAuditor(SOURCE, output).run()

    overrides_path = output / "Content_Inventory_OVERRIDES.csv"
    rows = read_rows(overrides_path)
    rows.append(
        {
            "id": "CNT-9999",
            "campo": "estado",
            "valor_original": "",
            "propuesta": "",
            "resuelto": "",
        }
    )
    write_overrides(overrides_path, rows)

    InventoryAuditor(SOURCE, output).run()
    saved = {(row["id"], row["campo"]) for row in read_rows(overrides_path)}
    assert ("CNT-9999", "estado") not in saved
