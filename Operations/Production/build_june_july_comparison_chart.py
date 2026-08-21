from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

out = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-20_Comparativo_Junio_Julio_Medianas.png')
plt.style.use('seaborn-v0_8-whitegrid')
fig, axes = plt.subplots(1, 2, figsize=(12, 5.8), dpi=180)

months = ['Junio', 'Julio']
med_interactions = [10, 43]
med_shares = [1, 7]
colors = ['#7c8da6', '#c45b3c']

x = np.arange(2)
axes[0].bar(x, med_interactions, color=colors, width=.55)
axes[0].set_xticks(x, months)
axes[0].set_ylabel('Interacciones medianas por publicación')
axes[0].set_title('Distribución general')
for i, v in enumerate(med_interactions):
    axes[0].text(i, v + 1.5, f'{v}', ha='center', va='bottom', fontweight='bold')

axes[1].bar(x, med_shares, color=colors, width=.55)
axes[1].set_xticks(x, months)
axes[1].set_ylabel('Shares medianos por publicación')
axes[1].set_title('Difusión')
for i, v in enumerate(med_shares):
    axes[1].text(i, v + .25, f'{v}', ha='center', va='bottom', fontweight='bold')

fig.suptitle('Universe Sent Me — Junio vs. julio 2026', fontsize=16, fontweight='bold')
fig.text(0.5, 0.01, 'Fuente: base comparable de 509 publicaciones; interacciones = reacciones + comentarios + shares. Uso descriptivo; no implica causalidad.', ha='center', fontsize=8.5)
fig.tight_layout(rect=[0, 0.04, 1, 0.93])
fig.savefig(out, bbox_inches='tight')
print(out)
