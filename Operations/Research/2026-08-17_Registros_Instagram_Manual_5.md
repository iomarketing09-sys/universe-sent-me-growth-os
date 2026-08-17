---
title: "Registros manuales Instagram — cinco duplicaciones Facebook 17–30"
purpose: "Preparar los datos exactos para que Fernando duplique manualmente en Meta cinco publicaciones ya programadas en Facebook."
status: "Review"
created: 2026-08-17
updated: 2026-08-17
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-17_Cruce_Instagram_Facebook_17_30.md"
  - "Operations/Research/2026-08-17_Calendario_Instagram_17_30_Propuesto.md"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
organization: "Operations/Research"
---

# Registros manuales de Instagram — cinco duplicaciones Facebook 17–30

## Instrucción operativa

Fernando puede duplicar manualmente en Meta las cinco filas siguientes. Manus no publicará, no programará y no llamará a Meta durante esta fase. La zona de referencia es `America/Matamoros`; cada fecha y hora debe conservarse tal como aparece en Facebook. Las cinco filas ya tienen un identificador proporcionado por Fernando. Se registran como `Programada` porque todavía no tenemos permalink ni una respuesta live de Meta que confirme el estado efectivo; no se inventa hora real ni se marca `Publicado`.

> `260633 - Universe.png` queda excluido: Fernando confirmó que fue eliminado manualmente. No republicar.

| Orden | Fecha | Hora | Asset | Caption exacto | Facebook Page Post ID | ID Instagram proporcionado | Estado registrado |
|---:|---|---:|---|---|---|---|---|
| 2 | 2026-08-19 | 13:30 | `260560 - Fantasma.png` | Esperando octubre… 👻 #UniverseSentMe | `1036844829507460_122151374655072582` | `1385059653723843` | `Programada` |
| 3 | 2026-08-21 | 19:00 | `260614 - Universe.png` | Analizando mi propio caos. 🧐 #UniverseSentMe | `1036844829507460_122151375843072582` | `1598897621792943` | `Programada` |
| 4 | 2026-08-23 | 22:00 | `260625.png` | El cambio da miedo… quedarse igual también. 😮‍💨 #UniverseSentMe | `1036844829507460_122151376629072582` | `2631450910602853` | `Programada` |
| 5 | 2026-08-25 | 17:00 | `260613 - Wilfred.png` | Wilfred sabe. 🌲 #UniverseSentMe | `1036844829507460_122151377553072582` | `1372611618180903` | `Programada` |
| 6 | 2026-08-30 | 22:00 | `260528 - Universe.png` | Ya duérmete… 🌙 #UniverseSentMe | `1036844829507460_122151379707072582` | `1406763488012220` | `Programada` |

## Controles de exclusión

No tocar `260583`, `260633`, `2608030`, `2608036` ni `2608060`. Los tres últimos ya tienen publicaciones activas documentadas; `260583` está prohibida y `260633` quedó eliminada manualmente.

## Registro posterior

Después de que Fernando confirme que cada fila quedó efectivamente publicada, se debe registrar el permalink, hora real y estado live en `Publication_Log.csv` y `ExperimentLog.csv`. Los identificadores actuales se conservan como datos proporcionados por Fernando; su tipo exacto no se presume sin verificación. Si una duplicación falla, se conserva el error completo y no se reintenta la creación del contenedor automáticamente. No se crean CNT nuevos con esta operación.

## Alcance de esta preparación

El cruce utilizó referencias exactas `260###` y Page Post IDs reales del ledger Facebook. Los seis identificadores fueron proporcionados por Fernando y se registraron sin llamadas adicionales a Meta. No se modificó Facebook, no se modificó Instagram, no se creó scheduler y no se movió Drive.
