#!/usr/bin/env python3
"""
Script de validación de publicaciones para Firma Bordados.

Uso:
    python validate_publications.py [csv_path]

Si no se proporciona csv_path, usa asset_inventory.csv por defecto.
"""
import sys
from pathlib import Path

from growth.audit import validate_publications_csv


def main():
    # Determinar CSV a auditar
    if len(sys.argv) > 1:
        csv_path = Path(sys.argv[1])
    else:
        csv_path = Path(__file__).parent / "asset_inventory.csv"

    print(f"🔍 Auditando: {csv_path}")
    print("-" * 50)

    result = validate_publications_csv(csv_path)

    if not result["success"]:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)

    print(f"✅ Auditoría completada")
    print(f"   Total de filas:      {result['total']}")
    print(f"   ❌ Missing:          {result['missing']}")
    print(f"   ⚠️  Ambiguous:       {result['ambiguous']}")
    print(f"   ✅ Match:            {result['total'] - result['missing'] - result['ambiguous']}")

    if result["problematic_rows"]:
        print(f"\n📋 Filas problemáticas ({len(result['problematic_rows'])}):")
        for row in result["problematic_rows"]:
            print(f"   Row {row['row_number']:3d} | {row['status']:10s} | {row['asset_filename']}")
            if row["detail"]:
                print(f"         └─ {row['detail']}")

    # Exit code: 0 si todo OK, 1 si hay missing/ambiguous
    if result["missing"] > 0 or result["ambiguous"] > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
