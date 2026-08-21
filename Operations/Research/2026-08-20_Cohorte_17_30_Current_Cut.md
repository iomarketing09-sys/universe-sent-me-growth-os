---
title: "Corte actual de métricas de la cohorte 17–30 de agosto"
purpose: "Comparar el estado actual de las publicaciones reales de Facebook de la ola 17–30 con el corte anterior, separando P0 y evitando inferencias de ventanas no disponibles."
status: "Active"
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-20_Cohorte_17_30_Actual_Cut.md"
  - "Operations/Research/2026-08-19_P0_Corte_17_Agosto.md"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
organization: "Operations/Research"
---

# Estado de ejecución

El recordatorio operativo anterior era una ejecución única para el primer corte P0 y aparece actualmente pausado/expirado. Este corte se ejecutó manualmente en la sesión actual; no se reactivó ni se creó una tarea recurrente.

# Alcance
Se analizaron **19 publicaciones de imagen** visibles en Meta con fecha local entre el 17 y el 30 de agosto, excluyendo los cinco IDs del baseline P0 y separando 2 Reels. El agregado editorial registra **1095 interacciones observadas**: 811 reacciones, 44 comentarios y 240 compartidos.
Las cifras son acumulados lifetime observados al momento de consulta, no snapshots exactos de 24/72 horas. Los Reels se conservan en `reels_separate` y no se mezclan con el agregado editorial de imágenes.

## Resumen por fecha local

| Fecha | Publicaciones | Interacciones | Media | Mediana | Compartidos |
|---|---:|---:|---:|---:|---:|
| 2026-08-17 | 1 | 339 | 339.0 | 339.0 | 100 |
| 2026-08-18 | 6 | 196 | 32.7 | 31.5 | 41 |
| 2026-08-19 | 6 | 345 | 57.5 | 41.5 | 49 |
| 2026-08-20 | 6 | 215 | 35.8 | 32.5 | 50 |

## Resumen por horario

| Horario | Publicaciones | Interacciones | Media | Mediana |
|---|---:|---:|---:|---:|
| 10:00 | 3 | 132 | 44.0 | 49.0 |
| 11:00 | 3 | 154 | 51.3 | 57.0 |
| 13:30 | 3 | 93 | 31.0 | 30.0 |
| 16:00 | 3 | 97 | 32.3 | 26.0 |
| 17:00 | 3 | 236 | 78.7 | 40.0 |
| 19:00 | 4 | 383 | 95.8 | 20.5 |

## Cambio frente al corte anterior

El corte homogéneo anterior registraba 13 publicaciones de imagen y 731 interacciones. El cambio observado es de **6 publicaciones** y **364 interacciones** acumuladas. Las seis imágenes nuevas promedian 60.7 interacciones, pero la mediana global baja de 38 a 35; por tanto, el crecimiento agregado no equivale todavía a una mejora robusta de la publicación típica.

## Reels separados

- 2026-08-19T19:03:50-05:00 — https://www.facebook.com/reel/2210896633022235/ — campos observados: 2 reacciones, 0 comentarios, 0 shares; no se interpreta como rendimiento de imagen.
- 2026-08-20T18:04:21-05:00 — https://www.facebook.com/reel/2815726225473165/ — campos observados: 5 reacciones, 1 comentarios, 3 shares; no se interpreta como rendimiento de imagen.

## Cautelas

Este corte no debe compararse con P0 como si fueran ventanas temporales equivalentes. El baseline P0 se excluye del total y se conserva en su reporte separado. Los resultados de horario son descriptivos; no se debe inferir causalidad con franjas que tengan pocas observaciones. Afiliados y métricas de video permanecen fuera de este agregado editorial; los Reels solo se reportan de forma separada.

## Fuentes

- Meta Graph API v26, evidencia guardada en `Operations/Research/2026-08-20_Cohorte_17_30_Meta_Raw_Current.json`.
- Publication Log para enlazar IDs operativos y assets.
