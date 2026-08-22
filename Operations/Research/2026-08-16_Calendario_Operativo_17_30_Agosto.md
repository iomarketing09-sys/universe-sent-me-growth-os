---
title: "Calendario operativo 17–30 de agosto — Facebook programado"
purpose: "Consolidar y registrar 40 assets nuevos, 35 reuse Top y 3 reuse Reserve programados en Facebook, incluyendo tres reemplazos MEME-CAD, cuatro slots adicionales de cadencia y el movimiento manual de los 46 assets en Drive."
status: Active
created: 2026-08-16
updated: 2026-08-22
version: "1.8"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-16_Revision_Visual_Asignacion_35_Memes_Nuevos.md"
  - "Operations/Research/2026-08-16_Calendario_Operativo_17_30_Agosto.csv"
  - "GrowthOS/10_00_Kit_de_Hashtags_USM.md"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "Operations/Research/2026-08-16_Asignacion_Visual_Calendario_17_30_Agosto.csv"
  - "Operations/Research/2026-08-16_Manifiesto_Movimiento_35_Memes_Agosto.csv"
  - "Operations/Research/2026-08-16_Propuesta_Completado_11_Reuse_Junio_Mayo.csv"
  - "Operations/Research/2026-08-16_Programacion_Facebook_17_30_Agosto.md"
  - "Operations/Research/2026-08-23_Propuesta_Cadencia_23_30_MEME-CAD_Review.md"
  - "Operations/Research/2026-08-22_MEME_CAD_Replacements_Execution.json"
organization: "Operations/Research"
---

# Calendario operativo 17–30 de agosto

> **Estado:** Active. El calendario conserva 78 slots: tres programaciones anteriores fueron canceladas y reemplazadas por tres memes MEME-CAD, y cuatro slots adicionales fueron añadidos y verificados en Facebook mediante Meta Graph API v26. Todas las nuevas filas están en `Programado_Meta_Verificado`. Los 46 archivos del manifiesto fueron movidos manualmente y verificados en `08 Agosto` sin copias. Instagram permanece separado.

La versión consolida **40 assets nuevos aprobados**, **35 reuse Top**, **3 reuse Reserve**, **78 slots asignados** y **7 operaciones nuevas verificadas en Facebook**: tres sustituciones y cuatro adiciones de cadencia. Las sustituciones no crean slots adicionales; las cuatro adiciones llevan los días del 22 al 30 a una banda de 5–6 publicaciones diarias. Las siete publicaciones tienen `is_published=false` y horario futuro confirmado por Meta. La proporción operativa actual es 40 nuevos y 38 reuse incluyendo reserve.

## Regla operativa de caption

Los captions de los nuevos evitan repetir el texto visual y usan una secuencia de dos a cuatro emojis como remate, seguida de hashtags del kit. En Facebook se mantiene un máximo de tres hashtags, priorizando personaje, concepto y `#UniverseSentMe`. Instagram queda fuera de esta fase: no se programan publicaciones ni se modifica el scheduler de Instagram. Cualquier cross-post selectivo se revisará por separado después de completar Facebook.

## Control de Drive

El destino verificado es `08 Agosto`, folder ID `11nuEUoU2Or8uc0oxXLu7-k6LChk8zQNf`, dentro de `Humor existencial`. El manifiesto actualizado contiene **46 Drive IDs**: 35 assets nuevos y 11 reuse. Todos están marcados `MOVE_ONLY`, `copy_allowed=NO` y `MOVED_MANUALLY_VERIFIED`; `copy_allowed=NO` se conserva. La consulta posterior a Drive encontró los 46 IDs dentro de `08 Agosto` y cero de esos IDs restantes en las carpetas de origen; no se crearon copias.

## Siguiente control

El movimiento de Drive está cerrado y verificado. Los tres reemplazos MEME-CAD y los cuatro slots adicionales de cadencia ya fueron programados y verificados como futuros; el siguiente control es verificar la publicación real en sus horarios, registrar `Fecha_Publicacion_Local` y extraer las métricas mediante el reporte diario sin inventar ventanas 24/72 horas. Instagram, CNT, afiliados y Reels permanecen separados.

## Sustituciones MEME-CAD — 22 de agosto

Fernando aprobó los cinco memes MEME-CAD y posteriormente aprobó la ampliación de cadencia con cuatro slots adicionales. Se cancelaron y verificaron como ausentes de `scheduled_posts` las filas salientes de `2026-08-24 16:00`, `2026-08-26 17:00` y `2026-08-27 17:00`. Los nuevos posts conservaron exactamente esos horarios locales en `America/Matamoros` y quedaron con `is_published=false`.

| Fecha/hora | Fila sustituida | Nuevo asset | Nuevo Meta Post ID | Estado |
|---|---|---|---|---|
| 24 ago, 16:00 | `260607 - Universe.png` | `MEME-CAD-004_Wilfred_Tablero_v3.png` | `1036844829507460_122154732441072582` | `Programado_Meta_Verificado` |
| 26 ago, 17:00 | `260590 - Maeve.png` | `MEME-CAD-002_Fantasma_Sobrio_v1.png` | `1036844829507460_122154732501072582` | `Programado_Meta_Verificado` |
| 27 ago, 17:00 | `260542 - Universe.png` | `MEME-CAD-003_Silvio_Karma_v3.png` | `1036844829507460_122154732567072582` | `Programado_Meta_Verificado` |

La evidencia de los reemplazos está en `2026-08-22_MEME_CAD_Replacements_Execution.json` y la evidencia de ampliación en `2026-08-22_Cadence_Expansion_22_30_Execution.json`. No se movieron originales en Drive, no se creó CNT, no se ejecutó Instagram, Reels ni afiliación.

## Ampliación de cadencia 22–30 — 22 de agosto de 2026

Fernando aprobó aumentar la cadencia del 22 al 30 de agosto para no esperar al cierre mensual. Se añadieron cuatro slots sin cancelar filas existentes: uno el sábado 22, uno el domingo 23, uno el viernes 28 y uno el sábado 29. El resultado es de 5 a 6 publicaciones programadas en cada día del tramo.

| Fecha/hora local | Tipo | Asset | Meta Post ID | Estado |
|---|---|---|---|---|
| 22 ago, 22:00 | `Reuse_Top` / `CNT-083` | `Universe - Existencial 2607828.png` | `1036844829507460_122154733605072582` | `Programado_Meta_Verificado` |
| 23 ago, 17:00 | `Reuse_Top` / `CNT-081` | `Universe - Existencial 2607787.png` | `1036844829507460_122154733665072582` | `Programado_Meta_Verificado` |
| 28 ago, 16:00 | `Nueva` / `MEME-CAD-001` | `MEME-CAD-001_Universe_Envidia_v1.png` | `1036844829507460_122154733719072582` | `Programado_Meta_Verificado` |
| 29 ago, 16:00 | `Nueva` / `MEME-CAD-005` | `MEME-CAD-005_Evan_Indirecta_Pregunta_v4.png` | `1036844829507460_122154733797072582` | `Programado_Meta_Verificado` |

La evidencia completa está en `2026-08-22_Cadence_Expansion_22_30_Execution.json`. No se cancelaron posts en esta ampliación, no se creó CNT, no se movieron originales en Drive y no se ejecutó Instagram, Reels ni afiliación.

## Referencias

[1]: 2026-08-16_Revision_Visual_Asignacion_35_Memes_Nuevos.md "Revisión visual aprobada"
[2]: ../../../GrowthOS/10_00_Kit_de_Hashtags_USM.md "Kit de hashtags USM"
