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
    "rule_based_treatment", "proposed_caption_treatment", "treatment_confidence", "classification_method", "rationale",
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
        "rule_based_treatment": treatment,
        "proposed_caption_treatment": treatment,
        "treatment_confidence": confidence,
        "classification_method": "Rule_based_proposal_v1",
        "rationale": rationale,
        "manual_review_status": "Pending_Manual_Caption_Review",
        "caption_confidence_final": "Unconfirmed",
        "notes": "Do not update ExperimentLog treatment until manual review confirms the proposal.",
    })

manual_decisions = {
    "1036844829507460_122130196011072582": {
        "proposed_caption_treatment": "caption_refuerzo",
        "treatment_confidence": "Medium",
        "manual_review_status": "Analyst_Reviewed",
        "caption_confidence_final": "Medium",
        "notes": "Visual review confirms a short self-description that reinforces the image; outlier remains excluded from causal caption inference.",
    },
    "1036844829507460_122134608507072582": {
        "proposed_caption_treatment": "caption_minimo",
        "treatment_confidence": "High",
        "manual_review_status": "Analyst_Reviewed",
        "caption_confidence_final": "High",
        "notes": "Caption repeats the visual text and adds hashtags; reclassified from caption_refuerzo to caption_minimo.",
    },
    "1036844829507460_122130309663072582": {
        "proposed_caption_treatment": "caption_refuerzo",
        "treatment_confidence": "Medium",
        "manual_review_status": "Analyst_Reviewed",
        "caption_confidence_final": "Medium",
        "notes": "Visual review confirms reinforcement; retain ambiguity note Short_reinforcement_vs_minimal.",
    },
    "1036844829507460_122125895013072582": {
        "proposed_caption_treatment": "historical_unavailable",
        "treatment_confidence": "High",
        "manual_review_status": "Analyst_Reviewed",
        "caption_confidence_final": "High",
        "notes": "No Meta message exists; do not infer a caption from the text embedded in the image.",
    },
    "1036844829507460_122125544019072582": {
        "proposed_caption_treatment": "caption_minimo",
        "treatment_confidence": "High",
        "manual_review_status": "Analyst_Reviewed",
        "caption_confidence_final": "High",
        "notes": "Hashtags only; no semantic addition beyond the visual remate.",
    },
    "1036844829507460_122125520661072582": {
        "proposed_caption_treatment": "caption_conversacional",
        "treatment_confidence": "High",
        "manual_review_status": "Analyst_Reviewed",
        "caption_confidence_final": "High",
        "notes": "Explicit Síguenos CTA and humorous conditional; conversational treatment confirmed.",
    },
    "1036844829507460_122130329817072582": {
        "proposed_caption_treatment": "caption_minimo",
        "treatment_confidence": "High",
        "manual_review_status": "Analyst_Reviewed",
        "caption_confidence_final": "High",
        "notes": "Short reaction plus hashtags; minimal accompaniment confirmed.",
    },
    "1036844829507460_122128989885072582": {
        "proposed_caption_treatment": "caption_minimo",
        "treatment_confidence": "High",
        "manual_review_status": "Analyst_Reviewed",
        "caption_confidence_final": "High",
        "notes": "Emoji-only reaction; visual carries the full meaning.",
    },
    "1036844829507460_122134065975072582": {
        "proposed_caption_treatment": "caption_minimo",
        "treatment_confidence": "High",
        "manual_review_status": "Analyst_Reviewed",
        "caption_confidence_final": "High",
        "notes": "Hashtags only; radio/music theme retained as a confounder.",
    },
    "1036844829507460_122131071243072582": {
        "proposed_caption_treatment": "caption_conversacional",
        "treatment_confidence": "High",
        "manual_review_status": "Analyst_Reviewed",
        "caption_confidence_final": "High",
        "notes": "Follower thank-you and explicit roster; conversational caption confirmed, but content is a mixed-roster control.",
    },
    "1036844829507460_122134055109072582": {
        "proposed_caption_treatment": "caption_refuerzo",
        "treatment_confidence": "Medium",
        "manual_review_status": "Analyst_Reviewed",
        "caption_confidence_final": "Medium",
        "notes": "Interrogative label reads as reaction/semantic reinforcement, not an invitation to reply; identity remains unconfirmed.",
    },
    "1036844829507460_122130324285072582": {
        "proposed_caption_treatment": "caption_refuerzo",
        "treatment_confidence": "Medium",
        "manual_review_status": "Analyst_Reviewed",
        "caption_confidence_final": "Medium",
        "notes": "Colloquial interpersonal reaction adds tone but no CTA; reinforcement confirmed.",
    },
    "1036844829507460_122126239515072582": {
        "proposed_caption_treatment": "caption_minimo",
        "treatment_confidence": "High",
        "manual_review_status": "Analyst_Reviewed",
        "caption_confidence_final": "High",
        "notes": "Emoji-only reaction; mixed subjects prevent primary-character inference.",
    },
    "1036844829507460_122133424479072582": {
        "proposed_caption_treatment": "caption_refuerzo",
        "treatment_confidence": "Medium",
        "manual_review_status": "Analyst_Reviewed",
        "caption_confidence_final": "Medium",
        "notes": "Resigned interpersonal phrase reinforces the visual self-deprecating remate; no CTA.",
    },
    "1036844829507460_122130032151072582": {
        "proposed_caption_treatment": "caption_refuerzo",
        "treatment_confidence": "High",
        "manual_review_status": "Analyst_Reviewed",
        "caption_confidence_final": "High",
        "notes": "Interrogative repeats and reinforces Wilfred's visual voice; not a public CTA.",
    },
    "1036844829507460_122133558903072582": {
        "proposed_caption_treatment": "caption_minimo",
        "treatment_confidence": "High",
        "manual_review_status": "Analyst_Reviewed",
        "caption_confidence_final": "High",
        "notes": "Hashtag only; visual text is self-contained.",
    },
    "1036844829507460_122126670549072582": {
        "proposed_caption_treatment": "caption_minimo",
        "treatment_confidence": "High",
        "manual_review_status": "Analyst_Reviewed",
        "caption_confidence_final": "High",
        "notes": "Short phrase, emoji and music hashtag add no new semantic layer; music retained as a confounder.",
    },
}
for row in rows:
    if row["meta_id"] in manual_decisions:
        row.update(manual_decisions[row["meta_id"]])
        row["classification_method"] = "Rule_based_proposal_v1_plus_manual_review"

with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

summary = {
    "n_approved": len(rows),
    "caption_source_counts": {},
    "proposed_treatment_counts": {},
    "manual_review_status_counts": {},
    "classification_method": "Rule_based_proposal_v1_plus_manual_review",
    "limits": [
        "The rule-based treatment is a proposal, not a verified historical label.",
        "The exact Meta message is preserved; treatment changes remain descriptive and no experiment ledger is updated.",
        "The selected character subset is not random and cannot support caption causality.",
        "historical_unavailable remains valid when the source is empty or ambiguous."
    ],
}
for row in rows:
    summary["caption_source_counts"][row["caption_source"]] = summary["caption_source_counts"].get(row["caption_source"], 0) + 1
    summary["proposed_treatment_counts"][row["proposed_caption_treatment"]] = summary["proposed_treatment_counts"].get(row["proposed_caption_treatment"], 0) + 1
    summary["manual_review_status_counts"][row["manual_review_status"]] = summary["manual_review_status_counts"].get(row["manual_review_status"], 0) + 1
SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"output": str(OUT), "summary": str(SUMMARY), **summary}, ensure_ascii=False, indent=2))
