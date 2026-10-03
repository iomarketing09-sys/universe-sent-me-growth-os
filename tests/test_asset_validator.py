from pathlib import Path

from growth.asset_validator import find_asset, validate_row


def _canonical_path(path: Path) -> Path:
    return path.resolve()


def _make_row(asset_filename):
    return {
        "date": "2026-08-31",
        "time": "08:30-09:30",
        "platform": "Facebook",
        "piece": "Some piece",
        "asset_filename": asset_filename,
        "status": "pending",
    }


def test_find_match_outside_folder(tmp_path, monkeypatch):
    asset = tmp_path / "VID-20260821-WA0002.mp4"
    asset.write_text("dummy")

    monkeypatch.setattr("growth.asset_validator.ASSET_ROOT", tmp_path)
    monkeypatch.setattr(
        "growth.asset_validator.EXCLUDED_DIR",
        tmp_path / "Publicaciones Agosto",
    )

    status, matches = find_asset("VID-20260821-WA0002.mp4")

    assert status == "MATCH"
    assert len(matches) == 1
    assert matches[0] == asset


def test_find_missing_nonexistent(tmp_path, monkeypatch):
    monkeypatch.setattr("growth.asset_validator.ASSET_ROOT", tmp_path)
    monkeypatch.setattr(
        "growth.asset_validator.EXCLUDED_DIR",
        tmp_path / "Publicaciones Agosto",
    )

    status, matches = find_asset("nonexistent.file")

    assert status == "MISSING"
    assert matches == []


def test_find_missing_empty_filename(tmp_path, monkeypatch):
    monkeypatch.setattr("growth.asset_validator.ASSET_ROOT", tmp_path)
    monkeypatch.setattr(
        "growth.asset_validator.EXCLUDED_DIR",
        tmp_path / "Publicaciones Agosto",
    )

    status, matches = find_asset("")

    assert status == "MISSING"
    assert matches == []


def test_find_missing_only_in_publicaciones(tmp_path, monkeypatch):
    excluded = tmp_path / "Publicaciones Agosto"
    excluded.mkdir()

    asset = excluded / "Firma Bordados 001.jpeg"
    asset.write_text("dummy")

    monkeypatch.setattr("growth.asset_validator.ASSET_ROOT", tmp_path)
    monkeypatch.setattr("growth.asset_validator.EXCLUDED_DIR", excluded)

    status, matches = find_asset("Firma Bordados 001.jpeg")

    assert status == "MISSING"
    assert matches == []


def test_find_ambiguous_multiple(tmp_path, monkeypatch):
    asset1 = tmp_path / "Pics" / "dup.jpg"
    asset1.parent.mkdir(parents=True)
    asset1.write_text("a")

    asset2 = tmp_path / "MORE" / "dup.jpg"
    asset2.parent.mkdir(parents=True)
    asset2.write_text("b")

    monkeypatch.setattr("growth.asset_validator.ASSET_ROOT", tmp_path)
    monkeypatch.setattr(
        "growth.asset_validator.EXCLUDED_DIR",
        tmp_path / "Publicaciones Agosto",
    )

    status, matches = find_asset("dup.jpg")

    assert status == "AMBIGUOUS"
    assert len(matches) == 2


def test_validate_row_returns_expected_for_match(tmp_path, monkeypatch):
    asset = tmp_path / "VID-20260821-WA0002.mp4"
    asset.write_text("dummy")

    monkeypatch.setattr("growth.asset_validator.ASSET_ROOT", tmp_path)
    monkeypatch.setattr(
        "growth.asset_validator.EXCLUDED_DIR",
        tmp_path / "Publicaciones Agosto",
    )

    row = _make_row("VID-20260821-WA0002.mp4")
    result = validate_row(row)

    assert result["status"] == "MATCH"
    assert result["asset_path"] == str(_canonical_path(asset))


def test_validate_row_empty_filename(tmp_path, monkeypatch):
    monkeypatch.setattr("growth.asset_validator.ASSET_ROOT", tmp_path)
    monkeypatch.setattr(
        "growth.asset_validator.EXCLUDED_DIR",
        tmp_path / "Publicaciones Agosto",
    )

    row = _make_row("")
    result = validate_row(row)

    assert result["status"] == "MISSING"
    assert result["asset_path"] == ""
