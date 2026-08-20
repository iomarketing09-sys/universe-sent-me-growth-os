#!/usr/bin/env python3
from collections import Counter
from pathlib import Path
import csv

ROOT = Path('/home/ubuntu/universe-sent-me-growth-os')

def read(path):
    with path.open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

alias = read(ROOT / 'Operations/Research/2026-08-20_Source_Alias_Table.csv')
con = read(ROOT / 'Operations/Research/2026-08-20_Historical_Performance_Individuals_Consolidated.csv')
raw = read(ROOT / 'Operations/Research/Historical_Performance_Individuals.csv')

def assert_eq(label, a, b):
    if a != b:
        raise SystemExit(f'{label}: {a} != {b}')

assert_eq('alias_rows', len(alias), 98)
assert_eq('alias_high', sum(r['Confidence'] == 'High' for r in alias), 52)
assert_eq('alias_review', sum(r['Confidence'] == 'Review' for r in alias), 46)
assert_eq('consolidated_rows', len(con), 206)
assert_eq('raw_rows', len(raw), 211)
assert_eq('source_count_sum', sum(int(r['source_count']) for r in con), 211)
ids = [r['meta_id'] for r in con if r['meta_id']]
if len(ids) != len(set(ids)):
    raise SystemExit('consolidated meta_id values are not unique')
if any(r['metrics_consistent'] != 'Yes' for r in con):
    raise SystemExit('one or more consolidated rows has inconsistent metrics')
print('validation=PASS alias_rows=98 alias_high=52 alias_review=46 raw_rows=211 consolidated_rows=206 source_count_sum=211 unique_meta_ids=PASS metrics_consistent=PASS')
