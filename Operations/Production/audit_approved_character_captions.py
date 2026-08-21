#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UTILITY = ROOT / "Operations/Research/2026-08-21_Junio_57_Unmatched_Character_Utility.csv"
RAW = ROOT / "Operations/Research/2026-08-21_Junio_57_Unmatched_Meta_Raw.json"
OUT = ROOT / "Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Audit.csv"
SUMMARY = ROOT / "Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Audit_Summary.json"

with UTILITY.open(newline="", encoding="utf-8-sig") as handle:
    approved = [row for row in csv.DictReader(handle) if row.get("approval_status") == "Approved_Character_Analysis"]
raw = json.loads(RAW.read_text(encoding="utf-8"))
raw_by_id = {row["meta_id"]: row for row in raw.get("records", [])}

EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]")
QUESTION_RE = re.compile(r"[¿?]")
CTA_RE = re.compile(r"\b(comenta|dime|cu[aá]ntame|etiqueta|comparte|s[ií]gueme|cu[aá]l|qu[eé]|c[oó]mo)\b", re.I)


def normalize(text: str) -> str:
    return " ".join((text or "").replace("\n", " ").split())


def propose_treatment(text: str):
    normalized = normalize(text)
    if not normalized:
        return "historical_unavailable", "Low", "Meta raw contains no message text."
    words = normalized.split()
    emoji_count = len(EMOJI_RE.findall(normalized))
    hashtag_count = sum(token.startswith("#") for token in words)
    non_hashtag_words = [token for token in words if not token.startswith("#")]
    if len(non_hashtag_words) <= 3 and emoji_count + hashtag_count >= 1 and not QUESTION_RE.search(normalized):
        return "caption_minimo", "Medium", "Short text dominated by emojis/hashtags or a minimal remate."
    if QUESTION_RE.search(normalized) or CTA_RE.search(normalized):
        return "caption_conversacional", "Medium", "Question or invitation/CTA detected; manual confirmation required."
    if len(normalized) <= 120:
        return "caption_refuerzo", "Low", "Short declarative caption that may reinforce the visual reading; manual confirmation required."
    return "historical_unavailable", "Low", "Long or ambiguous historical caption; do not infer treatment automatically."

fields = [
    "meta_id", "date", "character_hypothesis", "interactions", "shares", "comments",
    "caption_queue", "caption_meta_exact", "caption_source", "meta_created_time", "permalink_url",
    "proposed_caption_treatment", "treatment_confidence", "classification_method", "rationale",
    "manual_review_status", "caption_confidence_final", "notes",
]
rows = []
for row in approved:
    record = raw_by_id.get(row["meta_id"], {})
    body = record.get("meta_body") or {}
    exact = body.get("message")
    if exact is None:
        exact = record.get("caption") or ""
        source = "Queue_caption_fallback"
    else:
        source = "Meta_Raw_message"
    treatment, confidence, rationale = propose_treatment(exact)
    rows.append({
        "meta_id": row["meta_id"],
        "date": row.get("date", ""),
        "character_hypothesis": row.get("character_hypothesis", ""),
        "interactions": row.get("interactions", ""),
        "shares": row.get("shares", ""),
        "comments": row.get("comments", ""),
        "caption_queue": row.get("caption", ""),
        "caption_meta_exact": exact,
        "caption_source": source,
        "meta_created_time": body.get("created_time", ""),
        "permalink_url": body.get("permalink_url", ""),
        "proposed_caption_treatment": treatment,
        "treatment_confidence": confidence,
        "classification_method": "Rule_based_proposal_v1",
        "rationale": rationale,
        "manual_review_status": "Pending_Manual_Caption_Review",
        "caption_confidence_final": "Unconfirmed",
        "notes": "Do not update ExperimentLog treatment until manual review confirms the proposal.",
    })

with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

summary = {
    "n_approved": len(rows),
    "caption_source_counts": {},
    "proposed_treatment_counts": {},
    "manual_review_status": "Pending_Manual_Caption_Review",
    "classification_method": "Rule_based_proposal_v1",
    "limits": [
        "The rule-based treatment is a proposal, not a verified historical label.",
        "The exact Meta message is preserved and must be reviewed before changing any experiment ledger.",
        "The selected character subset is not random and cannot support caption causality.",
        "historical_unavailable remains valid when the source is empty or ambiguous."
    ],
}
for row in rows:
    summary["caption_source_counts"][row["caption_source"]] = summary["caption_source_counts"].get(row["caption_source"], 0) + 1
    summary["proposed_treatment_counts"][row["proposed_caption_treatment"]] = summary["proposed_treatment_counts"].get(row["proposed_caption_treatment"], 0) + 1
SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"output": str(OUT), "summary": str(SUMMARY), **summary}, ensure_ascii=False, indent=2))
