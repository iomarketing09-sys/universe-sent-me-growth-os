---
title: "Corte estadístico de la cohorte 17–30 de agosto"
purpose: "Medir las publicaciones reales de Facebook de la ola 17–30, separando explícitamente el baseline P0 del 17 de agosto."
status: "Active"
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-19_P0_Corte_17_Agosto.md"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "Operations/Research/2026-08-20_Cohorte_15_16_Analysis.md"
organization: "Operations/Research"
---

# Alcance
Se analizaron **14 publicaciones reales** visibles en Meta con fecha local entre el 17 y el 30 de agosto, excluyendo los cinco IDs del baseline P0. El corte registra **731 interacciones observadas**: 534 reacciones, 27 comentarios y 170 compartidos.
Las cifras son acumulados lifetime observados al momento de consulta, no snapshots exactos de 24/72 horas.

## Resumen por fecha local

| Fecha | Publicaciones | Interacciones | Media | Mediana | Compartidos |
|---|---:|---:|---:|---:|---:|
| 2026-08-17 | 1 | 335 | 335.0 | 335.0 | 100 |
| 2026-08-18 | 6 | 189 | 31.5 | 30.5 | 40 |
| 2026-08-19 | 7 | 207 | 29.6 | 34.0 | 30 |

## Resumen por horario

| Horario | Publicaciones | Interacciones | Media | Mediana |
|---|---:|---:|---:|---:|
| 10:00 | 2 | 74 | 37.0 | 37.0 |
| 11:00 | 2 | 91 | 45.5 | 45.5 |
| 13:30 | 2 | 62 | 31.0 | 31.0 |
| 16:00 | 2 | 60 | 30.0 | 30.0 |
| 17:00 | 2 | 96 | 48.0 | 48.0 |
| 19:00 | 3 | 348 | 116.0 | 10.0 |
| 19:03 | 1 | 0 | 0.0 | 0.0 |

## Lectura inicial de los líderes

El mejor post no-P0 del corte fue `2608029 - Wilfred - Quiero loquiar.jpeg`, publicado el 17 de agosto a las 19:00, con **335 interacciones**, 231 reacciones, 4 comentarios y 100 compartidos. Los siguientes fueron `260515 - Universe.png` con 61, `2608046 - Universe - Mis firmas no se parecen.jpeg` con 57, `260733 - Evan - Yo aura fuerte` con 57 y `260735 - Universe - dentro de ti hay dos payasos` con 55.

El resultado de `2608029` es otro outlier relevante: concentra 45.8% de las 731 interacciones no-P0 observadas. La ola activa todavía debe leerse como una distribución con outliers, no como un promedio estable. La señal provisional vuelve a favorecer piezas con personaje reconocible, remate fácil de compartir y alto potencial de identificación, pero todavía no permite atribuir el resultado únicamente a las 19:00.

## Cautelas

Este corte fue extraído el 20 de agosto a las 03:34 UTC y cubre publicaciones reales visibles hasta el 19 de agosto en hora local; la cohorte del 17–30 todavía no está completa porque los días 20–30 son futuros o no cuentan con publicaciones reales verificadas en este corte. No debe compararse con P0 como si fueran ventanas temporales equivalentes. El baseline P0 se excluye del total y se conserva en su reporte separado. Los resultados de horario son descriptivos; no se debe inferir causalidad con franjas que tengan pocas observaciones.

## Fuentes

- Meta Graph API v26, evidencia guardada en `Operations/Research/2026-08-20_Cohorte_17_30_Meta_Raw.json`.
- Publication Log para enlazar IDs operativos y assets.
