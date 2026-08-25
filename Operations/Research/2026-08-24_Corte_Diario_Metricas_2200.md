---
title: "Corte diario de métricas de Meta — 22:00 local"
purpose: "Registrar acumulados observables del feed real, separar formatos y alimentar una actualización descriptiva del Growth OS sin sustituir snapshots E24/E72."
status: Active
created: 2026-08-24
updated: 2026-08-24
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-21_Corte_Diario_Metricas_2200.md"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "Operations/Research/Metrics_Snapshot_Log.csv"
  - "Operations/Automation/run_daily_metrics_cut.py"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
organization: "Operations/Research"
---

# Alcance del corte

El corte se realizó el **2026-08-24T22:08:34.798395-05:00** en `America/Matamoros`, con una ventana desde **2026-08-24T00:00:00-05:00** hasta **2026-08-24T22:08:34.798395-05:00**. Meta devolvió **6 publicaciones**, de las cuales **6** están confirmadas como publicadas.
Las cifras son acumulados lifetime observables al momento de la consulta; no representan incrementos exactos de 24 horas ni sustituyen los snapshots contractuales E0/E24/E72.

## Resumen por formato

| Formato | Publicaciones | Interacciones conocidas | Media | Mediana | Reacciones | Comentarios | Shares |
|---|---:|---:|---:|---:|---:|---:|---:|
| Image_or_post | 6 | 155 | 25.83 | 27.0 | 104 | 5 | 46 |

## Detalle de publicaciones

| Hora local | Formato | CNT / pieza | Interacciones conocidas | Reacciones | Comentarios | Shares | Calidad | Cruce |
|---|---|---|---:|---:|---:|---:|---|---|
| 10:00:03 | Image_or_post | FUT-MICRO-006 | 25 | 20 | 1 | 4 | observable_lifetime_at_capture | Publication_Log_Meta_Post_ID_match |
| 11:00:00 | Image_or_post | 260518 - Kael.png | 18 | 15 | 0 | 3 | observable_lifetime_at_capture | Publication_Log_Meta_Post_ID_match |
| 13:30:00 | Image_or_post | FUT-MICRO-005 | 29 | 21 | 2 | 6 | observable_lifetime_at_capture | Publication_Log_Meta_Post_ID_match |
| 16:00:03 | Image_or_post | MEME-CAD-004 | 2 | 1 | 0 | 1 | observable_lifetime_at_capture | Publication_Log_Meta_Post_ID_match |
| 17:00:06 | Image_or_post | 2608053 - Universe - Quieras o no.jpeg | 32 | 25 | 1 | 6 | observable_lifetime_at_capture | Publication_Log_Meta_Post_ID_match |
| 19:00:00 | Image_or_post | 2607825 - Kael - Ser el malo de la historia (28-jun-26).png | 49 | 22 | 1 | 26 | observable_lifetime_at_capture | Publication_Log_Meta_Post_ID_match |

## Lectura para Growth OS

El corte actualiza el Growth OS dentro de la misma ejecución en modo **descriptivo y Draft**: registra el ranking observable y separa formatos, pero no cierra hipótesis, no proyecta métricas a `ExperimentLog` y no escribe valores E24/E72. La fuente maestra incorpora esta lectura como contexto operativo, no como evidencia suficiente para cambiar el estado de una hipótesis. Las decisiones editoriales deben esperar validación humana y, cuando se trate de experimentos, snapshots temporales válidos.

## Salvaguardas

- No se publicó, editó, reprogramó, canceló ni eliminó contenido.
- No se escribió `Metrics_Snapshot_Log.csv`; el E0 del caso productivo conserva su control independiente.
- No se asignaron CNT, personaje, familia o experimento a IDs que no tuvieran coincidencia explícita en `Publication_Log.csv`.
- Reels permanecen fuera de los promedios de imagen/post.

## Fuentes

- `Operations/Research/2026-08-24_Meta_Daily_Metrics_Raw.json` — respuesta raw sanitizada del feed Meta.
- `Operations/Research/2026-08-15_Publication_Log.csv` — cruce explícito de Meta Post ID.
- `Operations/Research/2026-08-21_Corte_Diario_Metricas_2200.md` — definición del corte y sus limitaciones.
