import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from growth.publication_tracker import (
    REQUIRED_COLUMNS,
    load_publications,
    pending_publications,
    summary,
)

CSV_FILE = ROOT / "publication_log.csv"

def test_csv_exists():
    assert CSV_FILE.is_file()

def test_schema():
    rows = load_publications(CSV_FILE)
    assert len(rows) == 25

def test_required_columns():
    with CSV_FILE.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        assert next(reader) == REQUIRED_COLUMNS

def test_pending_rows_detected():
    rows = pending_publications(CSV_FILE)
    assert len(rows) > 0

def test_summary():
    result = summary(CSV_FILE)
    assert result["total"] == 25
    assert result["pending"] > 0
