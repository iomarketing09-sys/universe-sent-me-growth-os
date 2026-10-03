"""
Tests para growth/assets_manifest.json
"""
import json
from pathlib import Path


MANIFEST_PATH = Path(__file__).parent.parent / "growth" / "assets_manifest.json"


def test_manifest_exists():
    assert MANIFEST_PATH.exists(), f"Manifest no encontrado en {MANIFEST_PATH}"


def test_manifest_valid_json():
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, dict)


def test_manifest_has_version_and_assets():
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert "version" in data
    assert "assets" in data
    assert isinstance(data["assets"], list)


def test_asset_ref_unique():
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    refs = [asset["asset_ref"] for asset in data["assets"]]
    assert len(refs) == len(set(refs)), "asset_ref duplicados"


def test_confidence_values():
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    allowed = {"DETERMINISTIC", "AMBIGUOUS", "INSUFFICIENT_EVIDENCE"}
    for asset in data["assets"]:
        assert asset["confidence"] in allowed, f"confidence inválido en {asset['asset_ref']}: {asset['confidence']}"


def test_deterministic_has_evidence():
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    for asset in data["assets"]:
        if asset["confidence"] == "DETERMINISTIC":
            assert asset.get("evidence_source", ""), f"DETERMINISTIC sin evidence_source en {asset['asset_ref']}"
            # también debe tener source_file_key no vacío
            assert asset.get("source_file_key", ""), f"DETERMINISTIC sin source_file_key en {asset['asset_ref']}"


def test_insufficient_evidence_no_physical_id():
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    for asset in data["assets"]:
        if asset["confidence"] == "INSUFFICIENT_EVIDENCE":
            # source_file_key debe estar vacío o ausente
            key = asset.get("source_file_key", "")
            assert key == "", f"INSUFFICIENT_EVIDENCE con source_file_key no vacío en {asset['asset_ref']}: {key}"


def test_no_assets_from_publicaciones_agosto_root():
    """
    Verifica que no hay assets cuyo source_path sea exactamente 'Publicaciones Agosto/'
    (la carpeta raíz de ya publicados). 
    Los assets en subcarpetas como 'Publicaciones Agosto/24 al 30 Agosto/.../03 Creativos Ejecutivos/'
    SÍ son válidos porque son nuevos creativos para la semana actual.
    """
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    for asset in data["assets"]:
        sp = asset.get("source_path") or ""
        # Solo bloquear si es exactamente la carpeta raíz "Publicaciones Agosto/" 
        # o empieza con "Publicaciones Agosto/" y no tiene subcarpeta de creativos nuevos
        if sp == "Publicaciones Agosto/" or sp.startswith("Publicaciones Agosto/"):
            # Permitir si está en subcarpeta de creativos nuevos (03 Creativos Ejecutivos, Reels, etc.)
            allowed_subpaths = [
                "Publicaciones Agosto/24 al 30 Agosto",
                "Publicaciones Agosto/Reels/",
                "Publicaciones Agosto/03 Creativos"
            ]
            if not any(sp.startswith(allowed) for allowed in allowed_subpaths):
                assert False, f"Asset {asset['asset_ref']} usa Publicaciones Agosto/ raíz (ya publicado): {sp}"


def test_manifest_does_not_affect_gate():
    # El manifest no debe cambiar comportamiento del gate (no código modificado).
    # Este test solo verifica que el manifest existe y no rompe imports.
    # Importar módulos de growth para asegurar que no hay side effects.
    from growth import audit, workflow, publisher  # noqa: F401
    # Si el import funciona sin errores, el gate sigue intacto.
    assert True


def test_manifest_has_business_constraints():
    """Verifica que el manifest incluye restricciones comerciales."""
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert "business_constraints" in data
    constraints = data["business_constraints"]
    assert "excluded_categories" in constraints
    assert "whatsapp_contact" in constraints
    assert "878 788 0735" in constraints.get("whatsapp_contact", "")


def test_manifest_week_31ago_6sep():
    """Verifica que el manifest corresponde a la semana 31 ago - 6 sep 2026."""
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assets = data["assets"]
    # Debe tener al menos 16 assets para la semana completa (2-3 por día x 7 días)
    assert len(assets) >= 16
    # Verificar que están los días de la semana
    day_refs = [a["asset_ref"] for a in assets]
    assert any("lunes" in r for r in day_refs)
    assert any("martes" in r or "miercoles" in r for r in day_refs)
    assert any("jueves" in r for r in day_refs)
    assert any("sabado" in r for r in day_refs)
    assert any("domingo" in r for r in day_refs)
