#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HISTORICAL = ROOT / "Operations/Research/Historical_Performance_Individuals.csv"
COMPARABLE = ROOT / "Operations/Research/2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv"
OUTPUT = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Schedule_Analysis.json"


def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def stats(rows):
    interactions = [int(float(row.get("metric_value") or row.get("interactions") or 0)) for row in rows]
    shares = [int(float(row.get("shares") or 0)) for row in rows]
    return {"n": len(rows), "median_interactions": statistics.median(interactions) if interactions else 0, "median_shares": statistics.median(shares) if shares else 0, "total_interactions": sum(interactions), "total_shares": sum(shares)}


def main():
    historical = [row for row in read_csv(HISTORICAL) if row.get("period") == "Julio_2026"]
    expanded = []
    for row in historical:
        if row.get("role") not in {"July top post", "July expansion lot 01"}:
            continue
        row = dict(row)
        row["hour_bucket"] = row.get("local_time", "")[11:13] or "Unknown"
        expanded.append(row)
    comparable = [row for row in read_csv(COMPARABLE) if row.get("month") == "2026-07"]
    all_by_hour = defaultdict(list)
    expanded_by_hour = defaultdict(list)
    for row in comparable:
        hour = str(int(float(row.get("hour") or 0))).zfill(2)
        all_by_hour[hour].append(row)
    for row in expanded:
        expanded_by_hour[row["hour_bucket"]].append(row)
    result = {
        "expanded_individual": {"n": len(expanded), "by_hour": {hour: stats(rows) for hour, rows in sorted(expanded_by_hour.items())}},
        "july_comparable": {"n": len(comparable), "by_hour": {hour: stats(rows) for hour, rows in sorted(all_by_hour.items())}},
        "interpretation": [
            "The expanded individual sample is selected by shares/comments and is not suitable for estimating hourly uplift.",
            "Use the full July comparable dataset for schedule distributions; use the individual layer only to cross-check visual/content cells.",
            "Do not infer that an hour caused performance without content balancing.",
        ],
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT), "expanded_rows": len(expanded), "expanded_hours": sorted(expanded_by_hour)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
