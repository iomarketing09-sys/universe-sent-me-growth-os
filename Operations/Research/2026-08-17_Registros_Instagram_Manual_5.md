---
title: "Registros manuales Instagram — cinco duplicaciones Facebook 17–30"
purpose: "Preparar los datos exactos para que Fernando duplique manualmente en Meta cinco publicaciones ya programadas en Facebook."
status: "Review"
created: 2026-08-17
updated: 2026-08-17
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-17_Cruce_Instagram_Facebook_17_30.md"
  - "Operations/Research/2026-08-17_Calendario_Instagram_17_30_Propuesto.md"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
organization: "Operations/Research"
---

# Registros manuales de Instagram — cinco duplicaciones Facebook 17–30

## Instrucción operativa

Fernando puede duplicar manualmente en Meta las cinco filas siguientes. Manus no publicará, no programará y no llamará a Meta durante esta fase. La zona de referencia es `America/Matamoros`; cada fecha y hora debe conservarse tal como aparece en Facebook. Antes de confirmar cada duplicación, verificar que Instagram no tenga ya un `IG_Media_ID`, permalink o estado publicado para el asset.

> `260633 - Universe.png` queda excluido: Fernando confirmó que fue eliminado manualmente. No republicar.

| Orden | Fecha | Hora | Asset | Caption exacto | Facebook Page Post ID | Estado Instagram |
|---:|---|---:|---|---|---|---|
| 2 | 2026-08-19 | 13:30 | `260560 - Fantasma.png` | Esperando octubre… 👻 #UniverseSentMe | `1036844829507460_122151374655072582` | `Pendiente_Duplicación_Manual` |
| 3 | 2026-08-21 | 19:00 | `260614 - Universe.png` | Analizando mi propio caos. 🧐 #UniverseSentMe | `1036844829507460_122151375843072582` | `Pendiente_Duplicación_Manual` |
| 4 | 2026-08-23 | 22:00 | `260625.png` | El cambio da miedo… quedarse igual también. 😮‍💨 #UniverseSentMe | `1036844829507460_122151376629072582` | `Pendiente_Duplicación_Manual` |
| 5 | 2026-08-25 | 17:00 | `260613 - Wilfred.png` | Wilfred sabe. 🌲 #UniverseSentMe | `1036844829507460_122151377553072582` | `Pendiente_Duplicación_Manual` |
| 6 | 2026-08-30 | 22:00 | `260528 - Universe.png` | Ya duérmete… 🌙 #UniverseSentMe | `1036844829507460_122151379707072582` | `Pendiente_Duplicación_Manual` |

## Controles de exclusión

No tocar `260583`, `260633`, `2608030`, `2608036` ni `2608060`. Los tres últimos ya tienen publicaciones activas documentadas; `260583` está prohibida y `260633` quedó eliminada manualmente.

## Registro posterior

Después de que Fernando duplique cada publicación, se debe registrar el media ID de Instagram, permalink, hora real y estado en `Publication_Log.csv` y `ExperimentLog.csv`. Si una duplicación falla, se conserva el error completo y no se reintenta la creación del contenedor automáticamente. No se crean CNT nuevos con esta operación.

## Alcance de esta preparación

El cruce utilizó referencias exactas `260###` y Page Post IDs reales del ledger Facebook. En esta preparación no se llamó a Meta, no se modificó Facebook, no se modificó Instagram, no se creó scheduler y no se movió Drive.
