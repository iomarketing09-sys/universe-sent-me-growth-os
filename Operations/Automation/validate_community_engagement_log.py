#!/usr/bin/env python3
"""Validate the append-only Community Engagement Log CSV."""

import argparse
import csv
import sys
from pathlib import Path

REQUIRED_COLUMNS = {
    "Comentario_ID",
    "Post_ID",
    "Fecha_Comentario",
    "Plataforma",
    "Respuesta_Estado",
    "Aprobacion_Estado",
    "Respuesta_Sugerida",
    "Respuesta_Fecha",
    "Respuesta_Meta_ID",
    "Moderacion_Estado",
    "Privacidad",
    "Fuente",
    "Ultima_Sincronizacion",
}
VALID_RESPONSE_STATES = {
    "Sin_Revisar",
    "No_Requiere_Respuesta",
    "Pendiente_Respuesta",
    "Respondido",
    "Escalado",
    "Archivado",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "csv_path",
        nargs="?",
        default="Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    )
    args = parser.parse_args()
    path = Path(args.csv_path)

    if not path.exists():
        print(f"ERROR: file not found: {path}")
        return 2

    errors = []
    ids = set()
    rows = 0
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            errors.append("missing header")
            reader.fieldnames = []
        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            errors.append(f"missing columns: {sorted(missing)}")

        expected_columns = len(reader.fieldnames or [])
        for line_number, row in enumerate(reader, start=2):
            rows += 1
            if None in row:
                errors.append(f"line {line_number}: wrong column count")
            comment_id = (row.get("Comentario_ID") or "").strip()
            if not comment_id:
                errors.append(f"line {line_number}: empty Comentario_ID")
            elif comment_id in ids:
                errors.append(f"duplicate Comentario_ID: {comment_id}")
            else:
                ids.add(comment_id)

            state = (row.get("Respuesta_Estado") or "").strip()
            if state and state not in VALID_RESPONSE_STATES:
                errors.append(f"line {line_number}: invalid Respuesta_Estado={state}")
            if state == "Respondido":
                if not (row.get("Respuesta_Fecha") or "").strip():
                    errors.append(f"line {line_number}: Respondido without Respuesta_Fecha")
                if not (row.get("Respuesta_Meta_ID") or "").strip():
                    errors.append(f"line {line_number}: Respondido without Respuesta_Meta_ID")
            if state == "Pendiente_Respuesta" and not (row.get("Respuesta_Sugerida") or "").strip():
                errors.append(f"line {line_number}: pending response without Respuesta_Sugerida")
            if (row.get("Privacidad") or "").strip() != "Anonimizado":
                errors.append(f"line {line_number}: Privacidad must be Anonimizado")

    print(f"ROWS={rows}")
    print(f"UNIQUE_COMMENT_IDS={len(ids)}")
    print(f"EXPECTED_COLUMNS={expected_columns}")
    if errors:
        print("VALIDATION=FAIL")
        for error in errors:
            print(f"ERROR={error}")
        return 1
    print("VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
