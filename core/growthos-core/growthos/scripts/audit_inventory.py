"""Deterministic audit and normalization for the GrowthOS content inventory."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

from growthos.core.enums import (
    BloqueadoCanon,
    DificultadProduccion,
    EstadoCanon,
    EstadoPieza,
    EstadoProduccion,
    EstadoPublicacion,
    MotivoRevision,
    Plataforma,
    Prioridad,
    ReconciliacionConfianza,
    ReconciliacionEstado,
    Reutilizable,
    TipoContenido,
)
from growthos.core.models import Piece
from growthos.storage.csv_adapter import CSVAdapter


CANONICAL_FIELDS: Tuple[str, ...] = tuple(CSVAdapter.COLUMN_ORDER[Piece])

ENUM_FIELDS = {
    "tipo_contenido": TipoContenido,
    "plataforma": Plataforma,
    "estado": EstadoPieza,
    "prioridad": Prioridad,
    "dificultad_produccion": DificultadProduccion,
    "reutilizable": Reutilizable,
    "bloqueado_canon": BloqueadoCanon,
    "estado_operacion_normalizado": EstadoProduccion,
    "estado_canon_normalizado": EstadoCanon,
    "reconciliacion_estado": ReconciliacionEstado,
    "reconciliacion_confianza": ReconciliacionConfianza,
    "estado_canon": EstadoCanon,
    "estado_produccion": EstadoProduccion,
    "estado_publicacion": EstadoPublicacion,
    "motivo_revision_normalizado": MotivoRevision,
}

DATE_FIELDS = {"fecha_ultima_publicacion"}


@dataclass(frozen=True)
class NormalizationResult:
    """Result of normalizing one inventory field."""

    value: str
    category: str
    rule: str = ""
    confidence: str = "Alta"
    note: str = ""


@dataclass
class AuditStats:
    """Statistics from an audit run."""

    total_rows: int = 0
    a_count: int = 0
    b_count: int = 0
    c_real_count: int = 0
    none_empty_count: int = 0
    free_text_count: int = 0
    override_applied_count: int = 0
    override_pending_count: int = 0

    def __getitem__(self, key: str) -> int:
        aliases = {
            "A": "a_count",
            "B": "b_count",
            "C_REAL": "c_real_count",
            "NONE_EMPTY": "none_empty_count",
            "FREE_TEXT": "free_text_count",
            "OVERRIDE": "override_applied_count",
            "OVERRIDE_PENDING": "override_pending_count",
        }
        field_name = aliases.get(key, key)
        if not hasattr(self, field_name):
            raise KeyError(key)
        return int(getattr(self, field_name))

    def get(self, key: str, default: int = 0) -> int:
        try:
            return self[key]
        except KeyError:
            return default


class InventoryAuditor:
    """Audit Content_Inventory.csv and generate canonical traceability files."""

    def __init__(
        self,
        source: Path,
        output: Path,
        overrides_path: Optional[Path] = None,
    ) -> None:
        self.source = Path(source)
        self.output = Path(output)
        self.canonical_path = self.output / "Content_Inventory_CANONICAL.csv"
        self.reconciliation_path = self.output / "Content_Inventory_RECONCILIATION.csv"
        self.overrides_path = self.output / "Content_Inventory_OVERRIDES.csv"
        self.input_overrides_path = (
            Path(overrides_path)
            if overrides_path
            else (
                self.overrides_path
                if self.overrides_path.exists()
                else None
            )
        )
        self.overrides: Dict[Tuple[str, str], str] = {}
        self.pending_overrides: List[Dict[str, str]] = []

    def run(self) -> AuditStats:
        """Run the audit and rewrite CANONICAL, RECONCILIATION and OVERRIDES."""
        source_rows = self._read_rows(self.source)
        self._validate_unique_ids(source_rows)
        input_overrides = self._load_input_overrides()

        canonical_rows: List[Dict[str, str]] = []
        reconciliation_rows: List[Dict[str, str]] = []
        stats = AuditStats(total_rows=len(source_rows))

        for source_row in source_rows:
            piece_id = source_row.get("id", "").strip()
            source_values = self._source_values(source_row)
            canonical_row: Dict[str, str] = {}

            for field in CANONICAL_FIELDS:
                original = source_values.get(field, "")
                result = self._classify(field, original)
                override_key = (piece_id, field)

                if override_key in self.overrides:
                    result = NormalizationResult(
                        value=self.overrides[override_key],
                        category="OVERRIDE",
                        rule="human_override",
                        confidence="Alta",
                    )

                canonical_row[field] = result.value
                reconciliation_rows.append(
                    {
                        "id": piece_id,
                        "campo": field,
                        "valor_original": original,
                        "valor_canonico": result.value,
                        "categoria": result.category,
                        "regla_aplicada": result.rule,
                        "confianza": result.confidence,
                        "requiere_revision": (
                            "true" if result.category == "C_REAL" else "false"
                        ),
                        "nota": result.note,
                    }
                )

                if result.category == "A":
                    stats.a_count += 1
                elif result.category == "B":
                    stats.b_count += 1
                elif result.category == "C_REAL":
                    stats.c_real_count += 1
                elif result.category == "NONE_EMPTY":
                    stats.none_empty_count += 1
                elif result.category == "FREE_TEXT":
                    stats.free_text_count += 1
                elif result.category == "OVERRIDE":
                    stats.override_applied_count += 1

            canonical_rows.append(canonical_row)

        self._write_rows(self.canonical_path, CANONICAL_FIELDS, canonical_rows)
        self._write_rows(
            self.reconciliation_path,
            (
                "id",
                "campo",
                "valor_original",
                "valor_canonico",
                "categoria",
                "regla_aplicada",
                "confianza",
                "requiere_revision",
                "nota",
            ),
            reconciliation_rows,
        )
        self._write_overrides(reconciliation_rows, input_overrides)
        stats.override_pending_count = len(self.pending_overrides)
        return stats

    def _load_input_overrides(self) -> Dict[Tuple[str, str], Dict[str, str]]:
        if self.input_overrides_path is None or not self.input_overrides_path.exists():
            return {}

        rows = self._read_rows(self.input_overrides_path)
        loaded: Dict[Tuple[str, str], Dict[str, str]] = {}
        for row in rows:
            piece_id = row.get("id", "").strip()
            field = row.get("campo", "").strip()
            if not piece_id or not field:
                continue

            key = (piece_id, field)
            resolved = row.get("resuelto", "").strip()
            if resolved:
                self.overrides[key] = self._validate_override(field, resolved)
            else:
                self.pending_overrides.append(dict(row))
            loaded[key] = dict(row)
        return loaded

    def _validate_override(self, field: str, resolved: str) -> str:
        if field in ENUM_FIELDS:
            enum_type = ENUM_FIELDS[field]
            valid_values = {member.value for member in enum_type}
            if resolved not in valid_values:
                raise ValueError(
                    f"Override inválido para {field}: {resolved!r}. "
                    f"Valores permitidos: {sorted(valid_values)}"
                )
            return resolved

        if field in DATE_FIELDS:
            if resolved.casefold() in {"no publicado", "sin fecha", "n/a", "na"}:
                return ""
            parsed = self._parse_date(resolved)
            if parsed is None:
                raise ValueError(
                    f"Override inválido para {field}: {resolved!r}. Se esperaba una fecha ISO."
                )
            return parsed

        raise ValueError(f"Override inválido: el campo {field!r} no es auditable.")

    def _write_overrides(
        self,
        reconciliation_rows: Iterable[Mapping[str, str]],
        input_overrides: Mapping[Tuple[str, str], Mapping[str, str]],
    ) -> None:
        recon_by_key = {
            (row["id"], row["campo"]): row
            for row in reconciliation_rows
            if row["categoria"] == "C_REAL"
        }
        keys = set(recon_by_key) | {
            key
            for key, override in input_overrides.items()
            if override.get("propuesta", "").strip()
            or override.get("resuelto", "").strip()
        }
        order = {field: index for index, field in enumerate(CANONICAL_FIELDS)}
        rows = []

        for key in sorted(keys, key=lambda item: (self._row_index(item[0]), order[item[1]])):
            recon = recon_by_key.get(key, {})
            existing = input_overrides.get(key, {})
            rows.append(
                {
                    "id": key[0],
                    "campo": key[1],
                    "valor_original": recon.get(
                        "valor_original", existing.get("valor_original", "")
                    ),
                    "propuesta": existing.get("propuesta", ""),
                    "resuelto": existing.get("resuelto", ""),
                }
            )

        self._write_rows(
            self.overrides_path,
            ("id", "campo", "valor_original", "propuesta", "resuelto"),
            rows,
        )

    def _row_index(self, piece_id: str) -> int:
        match = re.fullmatch(r"CNT-(\d+)", piece_id)
        return int(match.group(1)) if match else 10**9

    def _classify(self, field: str, original: str) -> NormalizationResult:
        if field in ENUM_FIELDS:
            return self._classify_enum(field, original)
        if field in DATE_FIELDS:
            return self._classify_date(original)
        return NormalizationResult(original, "FREE_TEXT", "copy_verbatim")

    def _classify_enum(self, field: str, original: str) -> NormalizationResult:
        value = original.strip()
        if not value:
            return NormalizationResult("", "NONE_EMPTY", "optional_empty_to_none")

        enum_type = ENUM_FIELDS[field]
        if value in {member.value for member in enum_type}:
            return NormalizationResult(value, "A", "exact_enum_match")

        normalized = self._normalize_enum_alias(field, value)
        if normalized is not None:
            canonical, rule = normalized
            return NormalizationResult(canonical, "B", rule, "Media")

        return NormalizationResult(
            "",
            "C_REAL",
            confidence="Baja",
            note="Valor ambiguo; requiere override humano.",
        )

    def _normalize_enum_alias(self, field: str, value: str) -> Optional[Tuple[str, str]]:
        folded = value.casefold()

        if field == "plataforma":
            return self._normalize_platform(value)

        if field == "estado":
            if folded.startswith("publicado"):
                return "Publicado", "published_variant_to_publicado"
            if folded == "pendiente de producción":
                return "Pendiente de Producción", "production_pending_alias"
            if "draft" in folded and "aprob" in folded:
                return "Pendiente Aprobación Fernando", "draft_to_pendiente_fernando"

        if field == "prioridad" and folded == "p1 histórico":
            return "Alta", "p1_historico_to_alta"

        if field == "dificultad_produccion":
            match = re.match(r"^(muy baja|baja|media|alta)\b", folded)
            if match:
                canonical = {
                    "muy baja": "Muy_Baja",
                    "baja": "Baja",
                    "media": "Media",
                    "alta": "Alta",
                }[match.group(1)]
                return canonical, "difficulty_prefix_to_enum"

        if field in {"reutilizable", "bloqueado_canon"}:
            if folded.startswith(("sí", "si")):
                return "Sí", f"{field}_flag_strip"
            if folded.startswith("no"):
                return "No", f"{field}_flag_strip"

        return None

    def _normalize_platform(self, value: str) -> Optional[Tuple[str, str]]:
        platform_map = {member.value.casefold(): member.value for member in Plataforma}

        if "," in value:
            parts = [part.strip().casefold() for part in value.split(",")]
            if parts and all(part in platform_map for part in parts):
                return "Multi", "multi_combo_to_Multi"
            return None

        if ";" in value:
            primary = value.split(";", 1)[0].strip().casefold()
            if primary in platform_map:
                return platform_map[primary], "conditional_to_primary"
            return None

        parenthetical = re.match(r"^([^()]+?)\s*\(", value)
        if parenthetical:
            primary = parenthetical.group(1).strip().casefold()
            if primary in platform_map:
                return platform_map[primary], "parenthetical_to_primary"

        return None

    def _classify_date(self, original: str) -> NormalizationResult:
        value = original.strip()
        if not value:
            return NormalizationResult("", "NONE_EMPTY", "optional_empty_to_none")
        if value.casefold() in {"no publicado", "sin fecha", "n/a", "na"}:
            return NormalizationResult("", "B", "no_publicado_to_none")

        parsed = self._parse_date(value)
        if parsed is not None:
            return NormalizationResult(parsed, "A", "iso_date_parse")
        return NormalizationResult(
            "",
            "C_REAL",
            confidence="Baja",
            note="Fecha ambigua; requiere override humano.",
        )

    @staticmethod
    def _parse_date(value: str) -> Optional[str]:
        match = re.match(r"^(\d{4}-\d{2}-\d{2})", value.strip())
        if match:
            try:
                return datetime.strptime(match.group(1), "%Y-%m-%d").date().isoformat()
            except ValueError:
                return None

        for fmt in ("%d/%m/%Y", "%m/%d/%Y"):
            try:
                return datetime.strptime(value.strip(), fmt).date().isoformat()
            except ValueError:
                continue
        return None

    @staticmethod
    def _source_values(row: Mapping[str, str]) -> Dict[str, str]:
        folded = {key.casefold(): value for key, value in row.items()}
        return {
            field: row.get(field, folded.get(field.casefold(), ""))
            for field in CANONICAL_FIELDS
        }

    @staticmethod
    def _validate_unique_ids(rows: Iterable[Mapping[str, str]]) -> None:
        ids = [row.get("id", "").strip() for row in rows]
        if not all(ids):
            raise ValueError("Todas las filas deben tener un id")
        if len(ids) != len(set(ids)):
            raise ValueError("Los ids del inventario deben ser únicos")

    @staticmethod
    def _read_rows(path: Path) -> List[Dict[str, str]]:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]

    @staticmethod
    def _write_rows(
        path: Path,
        fieldnames: Iterable[str],
        rows: Iterable[Mapping[str, Any]],
    ) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=list(fieldnames),
                lineterminator="\n",
            )
            writer.writeheader()
            writer.writerows(rows)


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Audit GrowthOS Content Inventory")
    parser.add_argument("--source", type=Path, required=True, help="Source CSV path")
    parser.add_argument("--output", type=Path, required=True, help="Output directory")
    parser.add_argument("--overrides", type=Path, help="Overrides CSV path")
    parser.add_argument("--print-stats", action="store_true", help="Print statistics")
    args = parser.parse_args()

    auditor = InventoryAuditor(args.source, args.output, args.overrides)
    stats = auditor.run()

    if args.print_stats:
        print(f"Total rows: {stats.total_rows}")
        print(f"A (exact match): {stats.a_count}")
        print(f"B (transformed): {stats.b_count}")
        print(f"C_REAL (needs human): {stats.c_real_count}")
        print(f"NONE_EMPTY: {stats.none_empty_count}")
        print(f"OVERRIDE (applied): {stats.override_applied_count}")
        print(f"OVERRIDE_PENDING: {stats.override_pending_count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
