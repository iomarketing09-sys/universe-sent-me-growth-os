"""Tests offline del merge de publicaciones de Universe."""

from __future__ import annotations

from tenants.universe.metrics.sync_publication_log import LOG_FIELDS, local_slot, merge_rows


def _row(**overrides: str) -> dict[str, str]:
    row = {field: "" for field in LOG_FIELDS}
    row.update(overrides)
    return row


def test_merge_rows_dedupes_by_publication_id_and_fills_blanks():
    existing = [_row(
        date="2026-10-28",
        time="10:00",
        platform="Instagram",
        asset_filename="ISAURA_142801_BEIGE_OI26_HERO.jpg",
        status="scheduled",
        publication_id="18129355670309228",
    )]
    incoming = [_row(
        date="2026-10-28",
        time="10:06",
        platform="Instagram",
        piece="ISAURA",
        status="published",
        publication_id="18129355670309228",
        published_at="2026-10-28T15:06:11+00:00",
    )]

    merged = merge_rows(existing, incoming)

    assert len(merged) == 1
    assert merged[0]["asset_filename"] == "ISAURA_142801_BEIGE_OI26_HERO.jpg"
    assert merged[0]["piece"] == "ISAURA"
    assert merged[0]["status"] == "published"
    assert merged[0]["published_at"] == "2026-10-28T15:06:11+00:00"


def test_merge_rows_keeps_distinct_ids_and_sorts_by_slot():
    rows = [
        _row(date="2026-10-29", time="19:00", platform="Facebook", publication_id="2"),
        _row(date="2026-10-28", time="10:00", platform="Instagram", publication_id="1"),
    ]

    merged = merge_rows(rows, [])

    assert [row["publication_id"] for row in merged] == ["1", "2"]


def test_merge_rows_uses_slot_key_when_id_is_missing():
    rows = [
        _row(date="2026-10-28", time="10:00", asset_filename="A.jpg", status="pending"),
        _row(date="2026-10-28", time="10:00", asset_filename="B.jpg", status="pending"),
    ]

    assert len(merge_rows(rows, [])) == 2


def test_local_slot_converts_to_matamoros_time():
    assert local_slot("2026-10-28T15:06:11+00:00") == (
        "2026-10-28",
        "10:06",
        "2026-10-28T15:06:11+00:00",
    )
    assert local_slot("") == ("", "", "")
