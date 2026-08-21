from pathlib import Path
import csv
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

root = Path('/home/ubuntu/universe-sent-me-growth-os')
source = root / 'Operations/Research/2026-08-20_Wave1_Eligible_Operational_Subset.csv'
out = root / 'Operations/Research/2026-08-20_Wave1_Caption_Treatment_Distribution.png'

with source.open(newline='', encoding='utf-8-sig') as f:
    data = list(csv.DictReader(f))

labels = ['caption_minimo', 'caption_refuerzo', 'caption_conversacional']
label_display = ['Mínimo', 'Refuerzo', 'Conversacional']
counts = Counter(r['Caption_Treatment_Propuesto'] for r in data)
families = ['FAM-01', 'FAM-02', 'FAM-03', 'FAM-04', 'FAM-05']
family_display = ['Difusión\nMinimal', 'Relatable\nSocial', 'Conversación\nRelacional', 'Ácido\nInterpersonal', 'Personaje\nMarcador']
matrix = np.array([[sum(1 for r in data if r['Family_ID_Final'] == f and r['Caption_Treatment_Propuesto'] == c) for c in labels] for f in families])

plt.style.use('seaborn-v0_8-whitegrid')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6), gridspec_kw={'width_ratios':[1, 1.45]})
fig.suptitle('Wave 1 — distribución de treatments de caption (n=9)', fontsize=16, fontweight='bold')

colors = ['#4C78A8', '#F58518', '#54A24B']
bars = ax1.bar(label_display, [counts[l] for l in labels], color=colors, width=0.62)
ax1.set_title('Conteo por treatment')
ax1.set_ylabel('Candidatos elegibles')
ax1.set_ylim(0, 5)
ax1.set_yticks(range(0, 6))
for bar, value in zip(bars, [counts[l] for l in labels]):
    ax1.text(bar.get_x()+bar.get_width()/2, value+0.12, str(value), ha='center', va='bottom', fontweight='bold')

im = ax2.imshow(matrix, cmap='Blues', vmin=0, vmax=max(1, matrix.max()))
ax2.set_title('Cruce familia × treatment')
ax2.set_xticks(range(3), label_display)
ax2.set_yticks(range(5), family_display)
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        ax2.text(j, i, str(matrix[i,j]), ha='center', va='center', color='white' if matrix[i,j] > 0 else '#444444', fontweight='bold')
ax2.set_xlabel('Treatment propuesto')
ax2.set_ylabel('Familia final')

fig.text(0.5, 0.01, 'Lectura: 4 refuerzo, 3 mínimo y 2 conversacional. La muestra no está balanceada entre familias.', ha='center', fontsize=10)
fig.tight_layout(rect=[0, 0.04, 1, 0.93])
fig.savefig(out, dpi=180, bbox_inches='tight')
print(out)
