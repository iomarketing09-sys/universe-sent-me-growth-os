import csv
from pathlib import Path

REQUIRED_COLUMNS = [
    "date", "time", "platform", "piece", "asset_filename",
    "status", "publication_id", "published_at", "reach",
    "interactions", "DMs", "leads",
]

def load_publications(csv_path):
    path = Path(csv_path)
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != REQUIRED_COLUMNS:
            raise ValueError(
                f"Columnas inválidas. Esperadas: {REQUIRED_COLUMNS}; "
                f"encontradas: {reader.fieldnames}"
            )
        return list(reader)

def pending_publications(csv_path):
    return [
        row for row in load_publications(csv_path)
        if row.get("status", "").strip().lower() == "pending"
    ]

def summary(csv_path):
    rows = load_publications(csv_path)
    return {
        "total": len(rows),
        "pending": sum(
            row.get("status", "").strip().lower() == "pending"
            for row in rows
        ),
        "published": sum(
            row.get("status", "").strip().lower() == "published"
            for row in rows
        ),
    }
