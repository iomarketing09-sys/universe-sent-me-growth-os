from pathlib import Path
import json
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path('/home/ubuntu/universe-sent-me-growth-os')
RESEARCH = ROOT / 'Operations' / 'Research'
DATA = json.loads((RESEARCH / '2026-08-22_Comparativa_Junio_Julio_Agosto_Datos.json').read_text(encoding='utf-8'))

labels = ['Junio\ncompleto', 'Julio\ncompleto', 'Agosto\n1–21']
keys = ['2026-06_images', '2026-07_images', '2026-08_1_21_images']
summary = DATA['summaries']
details = DATA['details']
colors = ['#8c6bb1', '#2b8cbe', '#e67e22']

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.titlesize': 13,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
})

fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=False)
fig.subplots_adjust(left=0.07, right=0.98, top=0.88, bottom=0.14, wspace=0.20, hspace=0.28)
metrics = [
    ('interactions_median', 'Mediana de interacciones por imagen', '{:.0f}'),
    ('posts_per_active_day', 'Imágenes por día activo', '{:.1f}'),
    ('interactions_per_active_day', 'Interacciones por día activo', '{:.0f}'),
    ('shares_per_interaction', 'Shares / interacciones', '{:.1%}'),
]
for ax, (field, title, fmt) in zip(axes.flat, metrics):
    vals = [summary[k][field] for k in keys]
    bars = ax.bar(labels, vals, color=colors, width=0.62)
    ax.set_title(title, fontweight='bold')
    ax.spines[['top', 'right']].set_visible(False)
    for bar, value in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), fmt.format(value), ha='center', va='bottom', fontsize=10, fontweight='bold')
    if field == 'shares_per_interaction':
        ax.set_ylim(0, max(vals) * 1.25)
    else:
        ax.set_ylim(0, max(vals) * 1.25)
fig.suptitle('Universe Sent Me — comparación de imágenes/posts', fontsize=17, fontweight='bold')
fig.text(0.5, 0.035, 'Junio y julio son meses completos; agosto acumula del 1 al 21. Interacciones = reacciones + comentarios + shares. Reels excluidos.', ha='center', fontsize=9)
fig.savefig(RESEARCH / '2026-08-22_Comparativa_Junio_Julio_Agosto_Rendimiento.png', dpi=180, bbox_inches='tight')
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=False)
fig.subplots_adjust(left=0.08, right=0.98, top=0.86, bottom=0.18)
x = np.arange(len(keys))
width = 0.34
top1 = [details[k]['top1_share_of_interactions'] for k in keys]
top5 = [details[k]['top5_share_of_interactions'] for k in keys]
b1 = ax.bar(x - width/2, top1, width, label='Top 1', color='#d95f02')
b2 = ax.bar(x + width/2, top5, width, label='Top 5', color='#1b9e77')
ax.set_xticks(x, labels)
ax.set_ylim(0, 0.8)
ax.set_ylabel('Proporción de interacciones del periodo')
ax.set_title('Concentración del rendimiento en outliers', fontsize=16, fontweight='bold')
ax.legend(frameon=False)
ax.spines[['top', 'right']].set_visible(False)
for bars in (b1, b2):
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.015, f'{bar.get_height():.1%}', ha='center', va='bottom', fontsize=10, fontweight='bold')
fig.text(0.5, 0.045, 'Agosto depende mucho más de pocos posts excepcionales; por eso su media y su mediana cuentan historias distintas.', ha='center', fontsize=9)
fig.savefig(RESEARCH / '2026-08-22_Comparativa_Junio_Julio_Agosto_Concentracion.png', dpi=180, bbox_inches='tight')
plt.close(fig)

print(RESEARCH / '2026-08-22_Comparativa_Junio_Julio_Agosto_Rendimiento.png')
print(RESEARCH / '2026-08-22_Comparativa_Junio_Julio_Agosto_Concentracion.png')
