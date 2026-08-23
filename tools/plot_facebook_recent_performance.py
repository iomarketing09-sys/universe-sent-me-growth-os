#!/usr/bin/env python3
import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

ROOT=Path(__file__).resolve().parents[1]
summary=json.loads((ROOT/'Operations/Research/2026-08-23_Facebook_Performance_Summary.json').read_text(encoding='utf-8'))
top=summary['top_posts'][:10]
fmt=summary['by_format']

plt.style.use('seaborn-v0_8-whitegrid')
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(14,6),gridspec_kw={'width_ratios':[2.2,1]})
fig.patch.set_facecolor('#fbfaf8')
for ax in (ax1,ax2): ax.set_facecolor('#fbfaf8')

labels=[]
for p in top:
    date=p['created_time'][:10][5:]
    caption=p['message'] or '(sin caption)'
    clean=''.join(ch for ch in caption if ord(ch) < 128).strip()
    clean=clean[:26] if clean else '(sin caption visible)'
    labels.append(f"{date} | {clean}")
values=[p['engagement_public'] for p in top]
colors=['#5B4B8A' if i<2 else '#9C8BC4' for i in range(len(values))]
ax1.barh(labels[::-1],values[::-1],color=colors[::-1])
ax1.set_title('Top 10 de 20 publicaciones recientes',loc='left',fontweight='bold')
ax1.set_xlabel('Engagement público acumulado')
ax1.xaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
ax1.text(0,-0.14,f"Fuente: Meta Graph API v26.0 | corte {summary['retrieved_at'][:19].replace('T',' ')} UTC",transform=ax1.transAxes,fontsize=8,color='#555555')
for i,v in enumerate(values[::-1]): ax1.text(v+max(values)*0.01,i,f'{v:,.0f}',va='center',fontsize=8)

names=list(fmt.keys()); totals=[fmt[k]['total_engagement_public'] for k in names]
bar_colors=['#8A78B6' if 'Imagen' in k else '#D49A66' for k in names]
tick_names=[f"{k}\n(n={fmt[k]['n']})" for k in names]
ax2.bar(tick_names,totals,color=bar_colors,width=.55)
ax2.set_title('Por formato',loc='left',fontweight='bold')
ax2.set_ylabel('Engagement acumulado')
ax2.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
ax2.tick_params(axis='x',labelrotation=20)
for i,v in enumerate(totals):
    ax2.text(i,v+max(totals)*.03,f'{v:,.0f}',ha='center',fontsize=9)
fig.suptitle('Universe Sent Me — Facebook | snapshot de rendimiento reciente',x=.05,ha='left',fontsize=16,fontweight='bold',color='#2D2538')
fig.tight_layout(rect=[0,0,1,.94])
out=ROOT/'Operations/Research/2026-08-23_Facebook_Performance_Recent_Chart.png'
fig.savefig(out,dpi=180,bbox_inches='tight')
print(out)
