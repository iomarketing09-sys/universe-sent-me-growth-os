import json
from pathlib import Path
path = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-20_Cohorte_17_30_Current_Cut.json')
data = json.loads(path.read_text(encoding='utf-8'))
rows = sorted(data['rows'], key=lambda r: r['interactions'], reverse=True)
print(json.dumps({'overall': data['overall'], 'comparison': data.get('comparison_to_previous_cut'), 'top5': [{k: r.get(k) for k in ['date_local','slot_local','asset_ref','publication_id','interactions','reactions','comments','shares','permalink_url']} for r in rows[:5]]}, ensure_ascii=False, indent=2))
