#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "Operations/Research/2026-08-21_Junio_57_Unmatched_Meta_Raw.json"
OUT = ROOT / "Operations/Research/2026-08-21_Junio_57_Unmatched_Character_Utility.csv"
SUMMARY = ROOT / "Operations/Research/2026-08-21_Junio_57_Unmatched_Character_Utility_Summary.json"

# Manual visual coding from the four contact sheets. These labels are hypotheses,
# not canon assignments and never create CNTs.
CODING = {
    24: ("Format_Control", "No character; floating-island/cloud text composition.", "None", "None", "Keep_Reserve", "High", "High performance but no character evidence."),
    25: ("Character_Review", "Small cat with glasses paired with a muscular cat transformation.", "Universe visual candidate", "Transformation_University_Candidate", "Analyze_Character_No_CNT", "High", "Priority character signal; asset match still absent."),
    47: ("Format_Control", "Nature photograph with overlaid text; no character.", "None", "None", "Keep_Reserve", "High", "Format control."),
    60: ("Format_Control", "Two generic human figures in a relational scene; no named marker.", "Unknown human pair", "Relational_Control", "Keep_Reserve", "Medium", "Do not map to canon characters."),
    61: ("Format_Control", "Sexual infographic with body-part labels; no recurring character.", "None", "Sexual_Control", "Keep_Reserve", "High", "Content control, not character evidence."),
    64: ("Format_Control", "Night road photograph with text; no character.", "None", "None", "Keep_Reserve", "High", "Format control."),
    67: ("Format_Control", "Sexual infographic with labels; no recurring character.", "None", "Sexual_Control", "Keep_Reserve", "High", "Content control, not character evidence."),
    72: ("Format_Control", "Sky photograph with text; no character.", "None", "None", "Keep_Reserve", "High", "Format control."),
    74: ("Character_Review", "Bearded red-hatted forest gnome casting a spell.", "Wilfred visual candidate", "Personaje_Marcador", "Analyze_Character_No_CNT", "Medium", "Strong visual continuity candidate; low-volume post."),
    75: ("Format_Control", "Landscape photograph with caption; no character.", "None", "None", "Keep_Reserve", "High", "Format control."),
    87: ("Character_Review", "Cat with glasses lying in clouds.", "Universe visual candidate", "Personaje_Marcador", "Analyze_Character_No_CNT", "High", "Glasses are a visual marker but not a CNT assignment."),
    93: ("Format_Control", "Cosmic stone/platform with motivational text; no recurring character.", "None", "None", "Keep_Reserve", "High", "Format control."),
    95: ("Format_Control", "Spiritual-friends poster with generic illustrated figures.", "Unidentified spiritual figures", "Spirituality_Control", "Keep_Reserve", "Medium", "No named character marker."),
    98: ("Character_Review", "Duck/Ganso in a formal outfit being dressed.", "Ganso visual candidate", "Transformacion_Vestuario_Secundario", "Analyze_Character_No_CNT", "High", "Use as secondary-character evidence, not Universe transformation."),
    99: ("Character_Review", "White sheet-like forest figure with dark glasses/eyes.", "Fantasma visual candidate", "Personaje_Marcador", "Analyze_Character_No_CNT", "Medium", "Preserve candidate label; do not canonize from one image."),
    101: ("Format_Control", "Landscape photograph with relationship text; no character.", "None", "None", "Keep_Reserve", "High", "Format control."),
    107: ("Format_Control", "Generic human in a fantasy sky scene with text.", "Unknown human", "Relatable_Control", "Keep_Reserve", "Medium", "No recurring visual markers."),
    108: ("Character_Review", "Cat with glasses and sexual/relational caption.", "Universe visual candidate", "Personaje_Marcador; Sexual_Control", "Analyze_Character_No_CNT", "High", "Useful to separate visual identity from humor category."),
    111: ("Format_Control", "Generic human portrait with abrasive caption.", "Unknown human", "Humor_Control", "Keep_Reserve", "High", "No recurring character marker."),
    120: ("Character_Review", "Bearded red-hatted gnome operating a keyboard in a magical room.", "Wilfred visual candidate", "Personaje_Marcador", "Analyze_Character_No_CNT", "High", "Strongest Wilfred candidate in the queue by visual confirmation."),
    126: ("Character_Review", "Group scene around a campfire with several fantasy/generic figures and a cat.", "Mixed roster candidate; identities unconfirmed", "Roster_Group_Control", "Analyze_Character_No_CNT", "Medium", "Useful for roster continuity, not individual performance attribution."),
    128: ("Character_Review", "Woman in witch/podcast setting; no confirmed canonical marker.", "Unidentified magical woman", "Personaje_Marcador_Candidate", "Analyze_Character_No_CNT", "Low", "Do not map automatically to Elara."),
    133: ("Format_Control", "Sky photograph with text; no character.", "None", "None", "Keep_Reserve", "High", "Format control."),
    137: ("Format_Control", "Real-person/TikTok meme with no recurring character.", "Unknown real person", "Platform_Reference_Control", "Keep_Reserve", "High", "Format control."),
    145: ("Format_Control", "Sky photograph with text; no character.", "None", "None", "Keep_Reserve", "High", "Format control."),
    149: ("Character_Review", "Cat with glasses emerging from a torn wall.", "Universe visual candidate", "Personaje_Marcador", "Analyze_Character_No_CNT", "Medium", "Glasses support a candidate identity signal; no canon change."),
    153: ("Format_Control", "Cloud composition with relationship text; no recurring character.", "Unknown human", "Relational_Control", "Keep_Reserve", "High", "Format control."),
    155: ("Character_Review", "Woman and cat in a fantasy/relational scene; identities unclear.", "Unknown woman + cat", "Relational_Character_Review", "Analyze_Character_No_CNT", "Low", "Requires conservative labeling; no Kiri/Universe assignment."),
    156: ("Format_Control", "Street/sky photograph with text; no character.", "None", "None", "Keep_Reserve", "High", "Format control."),
    161: ("Character_Review", "Bearded red-hatted forest gnome with text.", "Wilfred visual candidate", "Personaje_Marcador", "Analyze_Character_No_CNT", "Medium", "Useful as a second Wilfred visual case."),
    163: ("Format_Control", "Nature photograph with text; no character.", "None", "None", "Keep_Reserve", "High", "Format control."),
    169: ("No_Visual_Evidence", "Meta returned no full_picture for this post.", "Unknown", "Unknown", "Keep_Reserve", "High", "Do not infer from caption alone."),
    170: ("Character_Review", "Purple-haired clown-like figure in a relational caption.", "Silvio visual candidate", "Personaje_Marcador", "Analyze_Character_No_CNT", "Medium", "Character evidence only; not a performance rule."),
    174: ("Character_Review", "Dreamy fantasy woman/mermaid-like figure; no named marker.", "Unidentified fantasy woman", "Personaje_Marcador_Candidate", "Keep_Reserve", "Low", "Not enough for Elara/Kiri assignment."),
    177: ("Character_Review", "Bearded red-hatted gnome in a forest.", "Wilfred visual candidate", "Dialogue_Borderline", "Analyze_Character_No_CNT", "Medium", "Already a borderline dialogue candidate; retain separately."),
    179: ("Character_Review", "Cat with glasses in clouds.", "Universe visual candidate", "Personaje_Marcador", "Analyze_Character_No_CNT", "Low", "Low performance but useful identity control."),
    180: ("Format_Control", "Real-person backstage/megaphone image; no canon marker.", "Unknown real person", "Format_Control", "Keep_Reserve", "High", "Format control."),
    181: ("Format_Control", "Generic shirtless human in fantasy clouds.", "Unknown human", "Relational_Control", "Keep_Reserve", "High", "No recurring marker."),
    183: ("Format_Control", "Vehicle floating in clouds with text.", "None", "None", "Keep_Reserve", "High", "Format control."),
    184: ("Character_Review", "Bearded red-hatted gnome making a playlist.", "Wilfred visual candidate", "Personaje_Marcador", "Analyze_Character_No_CNT", "Low", "Character continuity, not a cell signal."),
    185: ("Format_Control", "Real-person/nightlife photograph with text.", "Unknown real people", "Format_Control", "Keep_Reserve", "High", "Format control."),
    191: ("Format_Control", "Generic human in clouds with motivational text.", "Unknown human", "None", "Keep_Reserve", "High", "Format control."),
    195: ("Character_Review", "White sheet-like forest figure.", "Fantasma visual candidate", "Personaje_Marcador", "Analyze_Character_No_CNT", "Low", "Second Fantasma candidate; not enough for canon."),
    205: ("Format_Control", "Generic human with headphones in clouds.", "Unknown human", "Relational_Control", "Keep_Reserve", "High", "Format control."),
    206: ("Format_Control", "Generic couple in a fantasy cloud scene.", "Unknown couple", "Relational_Control", "Keep_Reserve", "High", "Format control."),
    208: ("Character_Review", "Bearded red-hatted gnome in forest with text.", "Wilfred visual candidate", "Personaje_Marcador", "Keep_Reserve", "Low", "Keep as low-performance identity reserve."),
    210: ("Format_Control", "Generic couple in fantasy clouds.", "Unknown couple", "Relational_Control", "Keep_Reserve", "High", "Format control."),
    211: ("Format_Control", "Generic meditating human on a floating island.", "Unknown human", "None", "Keep_Reserve", "High", "Format control."),
    212: ("Format_Control", "Generic relational/fantasy composition.", "Unknown human pair", "Relational_Control", "Keep_Reserve", "High", "Format control."),
    215: ("Format_Control", "Fantasy woman on rainbow with text.", "Unidentified fantasy woman", "Format_Control", "Keep_Reserve", "Medium", "No recurring character marker."),
    216: ("Format_Control", "Generic couple in cloud scene with caption.", "Unknown couple", "Relational_Control", "Keep_Reserve", "High", "Format control."),
    218: ("Format_Control", "Generic human with floating photos.", "Unknown human", "Relational_Control", "Keep_Reserve", "High", "Format control."),
    220: ("Format_Control", "Generic human with heart/relationship scene.", "Unknown human", "Relational_Control", "Keep_Reserve", "High", "Format control."),
    221: ("Format_Control", "Dreamy fantasy woman/mermaid-like figure.", "Unidentified fantasy woman", "Format_Control", "Keep_Reserve", "Low", "No named character marker."),
    223: ("Format_Control", "Generic human reclining on cloud with relationship silhouettes.", "Unknown human", "Relational_Control", "Keep_Reserve", "High", "Format control."),
    229: ("Cell_Candidate", "Four-panel dialogue/sequence with recurring human figures and speech bubbles.", "Unknown human pair", "Microhistoria_Estricta_Candidate", "Cell_Candidate_Review", "High", "Potential second strict microhistory; detailed original review required before counting."),
    230: ("Format_Control", "Real-person selfie with music/AI-art hashtags.", "Unknown real person", "Format_Control", "Keep_Reserve", "High", "Format control."),
}

raw = json.loads(RAW.read_text(encoding="utf-8"))
by_rank = {int(row["priority_rank"]): row for row in raw["records"]}
missing = sorted(set(by_rank) - set(CODING))
extra = sorted(set(CODING) - set(by_rank))
if missing or extra:
    raise RuntimeError(f"Coding mismatch missing={missing} extra={extra}")

fields = ["priority_rank", "meta_id", "date", "interactions", "shares", "comments", "utility_class", "visual_character_observation", "character_hypothesis", "cell_relevance", "recommended_action", "confidence", "notes"]
with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    for rank in sorted(by_rank):
        row = by_rank[rank]
        utility, observation, hypothesis, cell, action, confidence, notes = CODING[rank]
        writer.writerow({
            "priority_rank": rank,
            "meta_id": row["meta_id"],
            "date": row["date"],
            "interactions": row["interactions_queue"],
            "shares": row["shares_queue"],
            "comments": row["comments_queue"],
            "utility_class": utility,
            "visual_character_observation": observation,
            "character_hypothesis": hypothesis,
            "cell_relevance": cell,
            "recommended_action": action,
            "confidence": confidence,
            "notes": notes,
        })

summary = {"n": len(by_rank), "counts_by_utility": {}, "counts_by_action": {}, "character_candidates": [], "cell_candidates": []}
for rank, coding in CODING.items():
    utility, observation, hypothesis, cell, action, confidence, notes = coding
    summary["counts_by_utility"][utility] = summary["counts_by_utility"].get(utility, 0) + 1
    summary["counts_by_action"][action] = summary["counts_by_action"].get(action, 0) + 1
    if utility == "Character_Review":
        summary["character_candidates"].append({"rank": rank, "meta_id": by_rank[rank]["meta_id"], "hypothesis": hypothesis, "interactions": by_rank[rank]["interactions_queue"], "shares": by_rank[rank]["shares_queue"], "action": action})
    if utility == "Cell_Candidate":
        summary["cell_candidates"].append({"rank": rank, "meta_id": by_rank[rank]["meta_id"], "cell": cell, "action": action})
SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"output": str(OUT), "summary": str(SUMMARY), "n": len(by_rank), "counts_by_utility": summary["counts_by_utility"], "counts_by_action": summary["counts_by_action"]}, ensure_ascii=False, indent=2))
