---
title: "Grupos duplicados del histórico de junio"
purpose: "Verificar duplicados lógicos de Meta ID antes de usar agregados históricos."
status: Active
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/Historical_Performance_Individuals.csv"
  - "Operations/Research/2026-08-20_Auditoria_Fuente_Maestra_Junio.json"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
organization: "Operations/Research"
---

# Grupos duplicados del histórico de junio

Se detectaron **5 grupos duplicados** dentro de `Historical_Performance_Individuals.csv`. Cada grupo comparte el mismo `meta_id` y contiene dos filas de fuentes históricas que deben representar una sola publicación lógica.

| Meta ID | Filas | Asset refs | Fechas | Métrica/valor | Reacciones | Comentarios | Shares | Fuentes |
|---|---:|---|---|---|---:|---:|---:|---|
| `1036844829507460_122128723341072582` | 2 | 260733; 260733 - Evan - Yo aura fuerte (10-jun-26) | 2026-06-09 | Reacciones + comentarios + shares=1127; Reactions + comments + shares=1127 | 896 | 20 | 211 | 2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv; 2026-08-17_Assets_Junio_FB_IDs.xlsx + Meta photo object + visual match |
| `1036844829507460_122129013585072582` | 2 | 260735; 260735 - Universe  - dentro de ti hay dos payasos (10-jun-26) | 2026-06-10 | Reacciones + comentarios + shares=785; Reactions + comments + shares=785 | 509 | 13 | 263 | 2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv; 2026-08-17_Assets_Junio_FB_IDs.xlsx + Meta photo object + visual match |
| `1036844829507460_122132599809072582` | 2 | 2607792; 2607792 - fantasma+Universe - El gato ;o (21-jun-26) | 2026-06-21 | Reacciones + comentarios + shares=1128; Reactions + comments + shares=1128 | 999 | 2 | 127 | 2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv; 2026-08-17_Assets_Junio_FB_IDs.xlsx + Meta photo object + visual match |
| `1036844829507460_122132690157072582` | 2 | 2607794; 2607794 - Universe - Aver.. A ver... (22-jun-26) | 2026-06-22 | Reacciones + comentarios + shares=975; Reactions + comments + shares=975 | 696 | 2 | 277 | 2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv; 2026-08-17_Assets_Junio_FB_IDs.xlsx + Meta photo object + visual match |
| `1036844829507460_122134136793072582` | 2 | 2607825; 2607825 - Kael - Ser el malo de la historia  (28-jun-26) | 2026-06-28 | Reacciones + comentarios + shares=1308; Reactions + comments + shares=1308 | 912 | 4 | 392 | 2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv; 2026-08-17_Assets_Junio_FB_IDs.xlsx + Meta photo object + visual match |

## Decisión de consolidación

Estos grupos deben conservarse como una sola publicación lógica para rankings y sumas. Las filas originales no se eliminan: se mantienen como fuentes de evidencia y se enlazan mediante `meta_id`. La vista consolidada debe conservar la lista de filas fuente, el asset/CNT confirmado y cualquier diferencia de definición métrica.
