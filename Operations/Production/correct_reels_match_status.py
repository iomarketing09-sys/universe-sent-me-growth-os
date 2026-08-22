import json
from pathlib import Path

path = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-19_Historial_Reels_Consolidado.json')
data = json.loads(path.read_text(encoding='utf-8'))
exact = {
    '1036844829507460_122123860587072582': ('Match_Visual_Exact', 'Single_asset_match'),
    '1036844829507460_122130226041072582': ('Match_Visual_Exact_Asset_Set', 'Asset_Set_Match'),
    '1036844829507460_122134608507072582': ('Match_Visual_Exact', 'Single_asset_match'),
}
changed = []
for r in data.get('records', []):
    if r.get('content_id') in exact:
        status, relationship = exact[r['content_id']]
        r['asset_match_status'] = status
        r['asset_relationship'] = relationship
        changed.append(r['content_id'])
data['last_updated'] = '2026-08-21'
data['version'] = '1.8'
data['match_status_correction'] = 'Exact Drive↔Meta matches are explicitly excluded from the pending asset queue.'
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print({'changed': changed, 'count': len(changed), 'version': data['version']})
