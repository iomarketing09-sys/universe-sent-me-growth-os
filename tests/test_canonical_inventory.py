#!/usr/bin/env python3
"""
Fase 2A Test: Validates the CANONICAL inventory structure and C_REAL traceability.

This test verifies:
- 85 rows input → 85 rows CANONICAL
- 85 IDs preserved
- 46 columns matching CSVAdapter.COLUMN_ORDER[Piece]
- FREE_TEXT copied verbatim
- C_REAL fully traced in RECONCILIATION + OVERRIDES
- NONE_EMPTY treated as empty (not C)
- No automatic C_REAL conversion

Phase 2B (after human overrides resolve C_REAL) will verify:
- 85 Piece instances valid
- Round-trip export/import preserves IDs and critical fields
"""

import csv
import tempfile
from pathlib import Path
import pytest

# Import after setting up path
import sys
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from growthos.storage.csv_adapter import CSVAdapter
from growthos.core.models import Piece


class TestCanonicalInventoryPhase2A:
    """Phase 2A: Structural validation without requiring Piece instantiation."""
    
    @pytest.fixture(scope="class")
    def canonical_files(self):
        """Run the auditor and return paths to generated files."""
        from growthos.scripts.audit_inventory import InventoryAuditor
        
        source = REPO_ROOT / "GrowthOS/Content_Inventory.csv"
        output = REPO_ROOT / "GrowthOS"
        
        auditor = InventoryAuditor(source, output)
        stats = auditor.run()
        
        return {
            "canonical": output / "Content_Inventory_CANONICAL.csv",
            "reconciliation": output / "Content_Inventory_RECONCILIATION.csv",
            "overrides": output / "Content_Inventory_OVERRIDES.csv",
            "stats": stats,
        }
    
    def test_source_has_85_rows(self):
        """Verify the historical CSV has 85 rows."""
        source = REPO_ROOT / "GrowthOS/Content_Inventory.csv"
        with source.open(encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 85, f"Expected 85 rows, got {len(rows)}"
        
        # Verify unique IDs
        ids = [r["id"] for r in rows]
        assert len(set(ids)) == 85, "Source must have 85 unique IDs"
    
    def test_canonical_has_85_rows(self, canonical_files):
        """CANONICAL must have exactly 85 rows."""
        with canonical_files["canonical"].open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 85, f"CANONICAL must have 85 rows, got {len(rows)}"
    
    def test_canonical_preserves_85_ids(self, canonical_files):
        """All 85 IDs must be preserved in CANONICAL."""
        with canonical_files["canonical"].open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        ids = [r["id"] for r in rows]
        assert len(ids) == 85
        assert len(set(ids)) == 85, "CANONICAL must have 85 unique IDs"
        
        # Cross-reference with source
        with (REPO_ROOT / "GrowthOS/Content_Inventory.csv").open(encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            source_ids = {r["id"] for r in reader}
        
        assert set(ids) == source_ids, "CANONICAL IDs must match source exactly"
    
    def test_canonical_has_correct_columns(self, canonical_files):
        """CANONICAL must have exactly the 46 columns expected by CSVAdapter."""
        with canonical_files["canonical"].open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            columns = reader.fieldnames
        
        expected = CSVAdapter.COLUMN_ORDER[Piece]
        assert list(columns) == expected, \
            f"Columns mismatch.\nExpected: {expected}\nGot: {list(columns)}"
    
    def test_free_text_copied_verbatim(self, canonical_files):
        """FREE_TEXT columns must be copied exactly from source."""
        free_text_cols = {
            "id", "titulo", "personaje_principal", "personajes_secundarios", 
            "objetivo", "hipotesis", "fuente", "formato",
            "asset_ref_confirmado", "asset_ref_candidato",
            "reconciliacion_fuente", "reconciliacion_nota", "registro_relacionado",
            "drive_reference_id", "meta_publication_id", "meta_permalink", "asset_set",
            "Asset_Ref", "Asset_Filename", "Drive_ID", "Ultima_Sincronizacion",
            "personaje_principal_normalizado", "personajes_secundarios_normalizados",
            "rol_narrativo", "tipo_humor_normalizado", "potencial_etiquetado",
            "confianza_taxonomia", "fuente_taxonomia", "nota_taxonomia",
        }
        
        with (REPO_ROOT / "GrowthOS/Content_Inventory.csv").open(encoding="utf-8-sig") as f:
            src = {r["id"]: r for r in csv.DictReader(f)}
        
        with canonical_files["canonical"].open(encoding="utf-8") as f:
            can = {r["id"]: r for r in csv.DictReader(f)}
        
        for rid in src:
            for col in free_text_cols:
                assert can[rid][col].strip() == src[rid][col].strip(), \
                    f"FREE_TEXT mismatch for {rid}.{col}"
    
    def test_reconciliation_traces_all_fields(self, canonical_files):
        """RECONCILIATION must have one row per field per record (17 enum fields × 85 = 1445 rows)."""
        with canonical_files["reconciliation"].open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        # 17 enum fields × 85 records = 1445
        # Plus FREE_TEXT fields traced (optional, but we trace them too)
        assert len(rows) >= 85 * 17, \
            f"RECONCILIATION must trace all enum fields: got {len(rows)}, expected ≥{85*17}"
        
        # Every row must have required columns
        required_cols = ["id", "campo", "valor_original", "valor_canonico",
                         "categoria", "regla_aplicada", "confianza", "requiere_revision", "nota"]
        assert all(set(r.keys()) >= set(required_cols) for r in rows)
    
    def test_c_real_fully_traced_in_reconciliation(self, canonical_files):
        """Every C_REAL field must appear in RECONCILIATION with categoria='C_REAL' and requiere_revision=true."""
        with canonical_files["reconciliation"].open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        c_real_rows = [r for r in rows if r["categoria"] == "C_REAL"]
        
        # Should match stats: 593 C_REAL fields
        assert len(c_real_rows) == 548, \
            f"Expected 548 C_REAL rows in RECONCILIATION, got {len(c_real_rows)}"
        
        # All must require revision
        for r in c_real_rows:
            assert r["requiere_revision"] == "true", \
                f"C_REAL row missing requiere_revision: {r}"
            assert r["valor_canonico"] == "", \
                f"C_REAL must have empty valor_canonico: {r}"
    
    def test_c_real_represented_in_overrides(self, canonical_files):
        """Every C_REAL field must have an entry in OVERRIDES."""
        with canonical_files["overrides"].open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            overrides = list(reader)
        
        with canonical_files["reconciliation"].open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            c_real_recon = [r for r in reader if r["categoria"] == "C_REAL"]
        
        # Create sets of (id, campo) for comparison
        override_keys = {(r["id"], r["campo"]) for r in overrides}
        recon_keys = {(r["id"], r["campo"]) for r in c_real_recon}
        
        assert recon_keys == override_keys, \
            f"OVERRIDES must match C_REAL 1:1. Missing: {recon_keys - override_keys}, Extra: {override_keys - recon_keys}"
    
    def test_none_empty_not_counted_as_c(self, canonical_files):
        """NONE_EMPTY (optional fields empty) must NOT be C_REAL."""
        with canonical_files["reconciliation"].open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        none_empty = [r for r in rows if r["categoria"] == "NONE_EMPTY"]
        
        # Should match stats: 21 NONE_EMPTY
        assert len(none_empty) == 21, \
            f"Expected 21 NONE_EMPTY, got {len(none_empty)}"
        
        for r in none_empty:
            assert r["requiere_revision"] == "false"
            assert r["valor_canonico"] == ""
            assert r["valor_original"] == ""
    
    def test_no_automatic_c_real_conversion(self, canonical_files):
        """Verify no C_REAL was silently converted to A/B."""
        with canonical_files["reconciliation"].open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        # No C_REAL should have a non-empty valor_canonico
        c_real = [r for r in rows if r["categoria"] == "C_REAL"]
        for r in c_real:
            assert r["valor_canonico"] == "", \
                f"C_REAL silently converted: {r}"
        
        # No C_REAL should have regla_aplicada
        for r in c_real:
            assert r["regla_aplicada"] == "", \
                f"C_REAL has regla_aplicada (should be empty): {r}"
    
    def test_a_b_rules_deterministic(self, canonical_files):
        """A/B rules must be deterministic and auditable."""
        with canonical_files["reconciliation"].open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        a_rows = [r for r in rows if r["categoria"] == "A"]
        b_rows = [r for r in rows if r["categoria"] == "B"]
        
        # All A must have regla_aplicada
        for r in a_rows:
            assert r["regla_aplicada"], f"A row missing regla: {r}"
            assert r["confianza"] == "Alta"
            assert r["requiere_revision"] == "false"
        
        # All B must have regla_aplicada
        for r in b_rows:
            assert r["regla_aplicada"], f"B row missing regla: {r}"
            assert r["confianza"] in ("Alta", "Media")
            assert r["requiere_revision"] == "false"
        
        # Counts must match stats
        assert len(a_rows) == 765, f"A count mismatch: {len(a_rows)} != 765"
        assert len(b_rows) == 111, f"B count mismatch: {len(b_rows)} != 111"


class TestCanonicalInventoryPhase2B:
    """Phase 2B: Full Piece validation AFTER human overrides are complete.
    
    This test will only pass once OVERRIDES.csv has all C_REAL resolved.
    """
    
    @pytest.fixture(scope="class")
    def overrides_complete(self, canonical_files):
        """Check if OVERRIDES has all C_REAL resolved."""
        with canonical_files["overrides"].open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            overrides = list(reader)
        
        # All C_REAL must have 'resuelto' filled
        unresolved = [o for o in overrides if not o.get("resuelto")]
        return len(unresolved) == 0
    
    @pytest.mark.skipif(True, reason="Phase 2B: requires human OVERRIDES completion")
    def test_all_85_instantiate_piece(self, canonical_files, overrides_complete):
        """All 85 CANONICAL rows must instantiate Piece (Phase 2B)."""
        if not overrides_complete:
            pytest.skip("OVERRIDES incomplete")
        
        with canonical_files["canonical"].open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        for row in rows:
            # Map CSV columns to Piece fields
            mapped = {}
            for csv_col, model_field in CSVAdapter.CSV_TO_PIECE.items():
                v = row.get(csv_col, "")
                mapped[model_field] = None if v == "" else v
            
            # Should not raise
            Piece(**mapped)
    
    @pytest.mark.skipif(True, reason="Phase 2B: requires human OVERRIDES completion")
    def test_roundtrip_preserves_ids_and_critical_fields(self, canonical_files, overrides_complete):
        """Full round-trip: CANONICAL → Piece → export → verify 85 IDs + critical fields."""
        if not overrides_complete:
            pytest.skip("OVERRIDES incomplete")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            # Import all 85
            pieces = CSVAdapter.import_csv(Piece, canonical_files["canonical"])
            assert len(pieces) == 85
            imported_ids = [p.ID_Pieza for p in pieces]
            assert len(set(imported_ids)) == 85
            
            # Export
            export_path = tmpdir / "roundtrip.csv"
            CSVAdapter.export_piece_csv(pieces, export_path)
            
            # Re-import
            reimported = CSVAdapter.import_csv(Piece, export_path)
            reimported_ids = [p.ID_Pieza for p in reimported]
            
            # Verify
            assert len(reimported) == 85
            assert reimported_ids == imported_ids, "IDs must be preserved in order"
            
            # Verify critical fields preserved
            for orig, reimp in zip(pieces, reimported):
                assert orig.ID_Pieza == reimp.ID_Pieza
                assert orig.Titulo == reimp.Titulo
                assert orig.Estado == reimp.Estado
                assert orig.Plataforma == reimp.Plataforma
                assert orig.Tipo_Contenido == reimp.Tipo_Contenido


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


class TestOverrideEnumValidation:
    """Tests for override enum validation (FASE 3.6 critical fix)."""
    
    def test_override_valid_applies(self):
        """Valid override with resuelto matching enum → applies to CANONICAL and RECONCILIATION."""
        import csv
        import tempfile
        from pathlib import Path
        from growthos.scripts.audit_inventory import InventoryAuditor
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'campo', 'valor_original', 'propuesta', 'resuelto'])
            writer.writerow(['CNT-001', 'estado', 'Original', 'Propuesta', 'Publicado'])
            temp_path = Path(f.name)
        
        try:
            auditor = InventoryAuditor(REPO_ROOT / "GrowthOS/Content_Inventory.csv", REPO_ROOT / "GrowthOS", temp_path)
            stats = auditor.run()
            
            # Check override was applied
            assert ('CNT-001', 'estado') in auditor.overrides
            assert auditor.overrides[('CNT-001', 'estado')] == 'Publicado'
        finally:
            temp_path.unlink()
    
    def test_override_invalid_rejected(self):
        """Invalid override with resuelto not in enum → raises ValueError, no contamination."""
        import csv
        import tempfile
        from pathlib import Path
        from growthos.scripts.audit_inventory import InventoryAuditor
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'campo', 'valor_original', 'propuesta', 'resuelto'])
            writer.writerow(['CNT-001', 'estado', 'Original', 'Propuesta', 'Valor_Invalido'])
            temp_path = Path(f.name)
        
        try:
            auditor = InventoryAuditor(REPO_ROOT / "GrowthOS/Content_Inventory.csv", REPO_ROOT / "GrowthOS", temp_path)
            auditor.run()
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Override inválido" in str(e)
            assert "estado" in str(e)
            assert "Valor_Invalido" in str(e)
        finally:
            temp_path.unlink()
        
        # Verify no contamination in CANONICAL (by re-running without override)
        auditor_clean = InventoryAuditor(REPO_ROOT / "GrowthOS/Content_Inventory.csv", REPO_ROOT / "GrowthOS", None)
        stats_clean = auditor_clean.run()
        assert stats_clean["C_REAL"] == 548  # Original count unchanged
    
    def test_override_without_resuelto_not_applied(self):
        """Override with proposal but empty resuelto → tracked as pending, not applied."""
        import csv
        import tempfile
        from pathlib import Path
        from growthos.scripts.audit_inventory import InventoryAuditor
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'campo', 'valor_original', 'propuesta', 'resuelto'])
            writer.writerow(['CNT-001', 'estado', 'Original', 'Propuesta', ''])
            temp_path = Path(f.name)
        
        try:
            auditor = InventoryAuditor(REPO_ROOT / "GrowthOS/Content_Inventory.csv", REPO_ROOT / "GrowthOS", temp_path)
            stats = auditor.run()
            
            # Should NOT be in overrides
            assert ('CNT-001', 'estado') not in auditor.overrides
            
            # Should be in pending_overrides
            pending = [o for o in auditor.pending_overrides if o['id'] == 'CNT-001' and o['campo'] == 'estado']
            assert len(pending) == 1
            assert pending[0]['propuesta'] == 'Propuesta'
            
            # Stats should track pending
            assert stats.get('OVERRIDE_PENDING', 0) >= 1
        finally:
            temp_path.unlink()

