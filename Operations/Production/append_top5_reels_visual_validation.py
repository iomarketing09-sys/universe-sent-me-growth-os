import csv
from pathlib import Path

path = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-21_Reels_Drive_Meta_Crossmatch_Review.csv')
with path.open(encoding='utf-8', newline='') as handle:
    rows = list(csv.DictReader(handle))
existing = {r['Review_ID'] for r in rows}
new = [
    {
        'Review_ID': 'XMR-006',
        'Asset_Drive_ID': '1tE84FJLyLNwqELa5E23_7Tn5dvDwN_WI',
        'Asset_Filename': 'Wilfred realista haciendo una posion.mp4',
        'Asset_Created_UTC': '2026-06-04T20:32:20Z',
        'Source_Analysis': 'Meta Reel 1020271167128162 is a stream landscape with text about psychologists; reviewed Drive candidate is Wilfred potion.',
        'Meta_Candidate_Post_ID': '1036844829507460_122125528653072582',
        'Meta_Reel_ID': '1020271167128162',
        'Meta_Published_UTC': '2026-06-01T16:08:45+0000',
        'Meta_Permalink': 'https://www.facebook.com/reel/1020271167128162/',
        'Decision': 'No_Match_In_Reviewed_Set',
        'Confidence': 'High',
        'Asset_Relationship': 'Not_a_match',
        'Editorial_Qualification': 'Pending_other_Drive_or_local_asset_search',
        'Notes': 'Reviewed Wilfred potion and relevant date-proximate image candidates; none matches the stream, reeds, exposed tree roots, or text overlay. This is not a global Drive exclusion.'
    },
    {
        'Review_ID': 'XMR-007',
        'Asset_Drive_ID': 'Universe Real - 001..008',
        'Asset_Filename': 'Universe Real - 001.mp4 through Universe Real - 008.mp4',
        'Asset_Created_UTC': '2026-06-06 to 2026-06-11',
        'Source_Analysis': 'Meta Reel 1303110198700919 is a night road with full moon and relationship text; Universe Real batch contains cyberpunk toast, selfies, a woman, and winged-cat cloud scenes.',
        'Meta_Candidate_Post_ID': '1036844829507460_122127661851072582',
        'Meta_Reel_ID': '1303110198700919',
        'Meta_Published_UTC': '2026-06-07T00:31:38+0000',
        'Meta_Permalink': 'https://www.facebook.com/reel/1303110198700919/',
        'Decision': 'No_Match_In_Reviewed_Set',
        'Confidence': 'High',
        'Asset_Relationship': 'Not_a_match',
        'Editorial_Qualification': 'Pending_other_Drive_or_local_asset_search',
        'Notes': 'All eight Universe Real videos were analyzed; no road, moon-through-windshield, or matching text sequence was present.'
    },
    {
        'Review_ID': 'XMR-008',
        'Asset_Drive_ID': 'Universe Real - 001..008; 15nHZZftnESgshlLevc0gK8N0zSqEq6Pp',
        'Asset_Filename': 'Universe Real family plus Universe sent me - 022.png',
        'Asset_Created_UTC': '2026-06-06 to 2026-06-11',
        'Source_Analysis': 'Meta Reel 1014879604586494 is a blue sky/cloud time-lapse with text Consejo del día: DESAPENDEJATE; reviewed Drive candidates show different characters/scenes or a different text image.',
        'Meta_Candidate_Post_ID': '1036844829507460_122128512777072582',
        'Meta_Reel_ID': '1014879604586494',
        'Meta_Published_UTC': '2026-06-09T15:36:25+0000',
        'Meta_Permalink': 'https://www.facebook.com/reel/1014879604586494/',
        'Decision': 'No_Match_In_Reviewed_Set',
        'Confidence': 'High',
        'Asset_Relationship': 'Not_a_match',
        'Editorial_Qualification': 'Pending_other_Drive_or_local_asset_search',
        'Notes': 'Universe Real 005-008 and Universe sent me - 022 were reviewed; none reproduces the sky scene and DESAPENDEJATE overlay.'
    },
    {
        'Review_ID': 'XMR-009',
        'Asset_Drive_ID': '1HFzRgE6keLuzBsH7LXFGhVi-cRxiqEAq',
        'Asset_Filename': '1 - Fantasma_frozen_in_forest_202608051814.mp4',
        'Asset_Created_UTC': '2026-08-05T23:14:53Z',
        'Source_Analysis': 'Meta Reel 4244177002465660 is a blue sky with clouds, text about people who know they are disliked, and a yellow arrow; reviewed Drive candidate is a ghost in a dark forest.',
        'Meta_Candidate_Post_ID': '1036844829507460_122123203887072582',
        'Meta_Reel_ID': '4244177002465660',
        'Meta_Published_UTC': '2026-05-23T16:30:34+0000',
        'Meta_Permalink': 'https://www.facebook.com/reel/4244177002465660/',
        'Decision': 'No_Match_In_Reviewed_Set',
        'Confidence': 'High',
        'Asset_Relationship': 'Not_a_match',
        'Editorial_Qualification': 'Pending_other_Drive_or_local_asset_search',
        'Notes': 'The August Fantasma video is visually distinct from the historical blue-sky Reel; do not attach it merely because the caption contains the word gente.'
    },
    {
        'Review_ID': 'XMR-010',
        'Asset_Drive_ID': '1tE84FJLyLNwqELa5E23_7Tn5dvDwN_WI',
        'Asset_Filename': 'Wilfred realista haciendo una posion.mp4',
        'Asset_Created_UTC': '2026-06-04T20:32:20Z',
        'Source_Analysis': 'Meta Reel 1314043717583273 is a rotating pastel circular background with text Se te nota en la voz que por dentro eres de colores; reviewed Drive candidate is Wilfred potion.',
        'Meta_Candidate_Post_ID': '1036844829507460_122125202205072582',
        'Meta_Reel_ID': '1314043717583273',
        'Meta_Published_UTC': '2026-06-01T03:35:20+0000',
        'Meta_Permalink': 'https://www.facebook.com/reel/1314043717583273/',
        'Decision': 'No_Match_In_Reviewed_Set',
        'Confidence': 'High',
        'Asset_Relationship': 'Not_a_match',
        'Editorial_Qualification': 'Pending_other_Drive_or_local_asset_search',
        'Notes': 'No gnome, cauldron, staff, or potion appears in the Meta Reel; this is a negative visual control.'
    },
]
for row in new:
    if row['Review_ID'] not in existing:
        rows.append(row)
fields = list(rows[0].keys())
with path.open('w', encoding='utf-8', newline='') as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
    writer.writeheader(); writer.writerows(rows)
print({'added': sum(r['Review_ID'] not in existing for r in new), 'total_rows': len(rows)})
