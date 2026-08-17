---
title: "Integración CNT de mayo y revisión Reserve"
purpose: "Documentar la creación de 28 registros CNT históricos para assets de mayo y clasificar los 95 registros Reserve sin convertir candidatos en publicaciones operativas."
status: "Review"
created: 2026-08-17
updated: 2026-08-17
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "GrowthOS/Content_Inventory.csv"
  - "Operations/Research/Historical_Performance_Individuals.csv"
  - "Operations/Research/2026-08-17_Reconciliacion_Historicos_Individuales.md"
  - "Operations/Research/2026-08-17_Revision_Reserve_Mayo.json"
  - "Operations/Research/2026-08-14_Reuse_Mayo_Ranking.csv"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
organization: "Operations/Research"
---

# Integración CNT de mayo y revisión Reserve

## Resultado ejecutivo

Se integraron **28 assets históricos de mayo** creando los registros `CNT-040` a `CNT-067` en `GrowthOS/Content_Inventory.csv`. Cada fila quedó enlazada con filename exacto, Drive ID, Meta publication ID, fecha histórica y métricas del ranking de reuse. No se creó ninguna relación canónica ni se modificaron los ledgers de publicación actuales.

Se revisaron también los **95 registros Reserve** del ranking de mayo. El cruce de solo lectura con la carpeta `05 Mayo` encontró **92 assets exactos disponibles en Drive** y **3 sin evidencia exacta localizada**. Los 95 permanecen como candidatos de reuse y no reciben CNT en este lote.

## CNT creados

| Rango | Cantidad | Evidencia | Estado operativo |
|---|---:|---|---|
| `CNT-040`–`CNT-067` | 28 | Filename exacto + Drive ID + Meta ID + ranking de mayo | `Historical_Reconciled` |

Los registros utilizan `Asset_Ref`, `Asset_Filename`, `Drive_ID`, `Meta_Post_ID`, `fecha_ultima_publicacion` y `reconciliacion_confianza=High`. El estado de publicación se marcó como `Historica`, no como publicación activa o programada. El campo de canon se dejó como `No evaluado`; crear un CNT administrativo no constituye aprobación canónica.

Dos archivos comparten la referencia `260508`: `260508 - Universe.jpg` y `Universe - Existencial 260508.png`. Se conservaron como dos CNT independientes porque los filenames y Drive IDs son distintos. No se fusionaron ni se eligió una variante por inferencia.

## Revisión de Reserve

| Clasificación | Cantidad | Acción |
|---|---:|---|
| `Drive_Exact_Ready_For_Review` | 92 | Candidatos aptos para un siguiente lote editorial; todavía no crear CNT automáticamente. |
| `Drive_Evidence_Pending` | 3 | Requieren localizar el archivo exacto o completar evidencia antes de integrarse. |
| CNT creados en Reserve | 0 | Mantener sin relación CNT hasta revisión editorial y deduplicación. |

La etiqueta `Drive_Exact_Ready_For_Review` significa que existe el archivo con filename exacto en `05 Mayo`; no significa que el asset esté aprobado para reuse, que no se haya publicado recientemente o que deba entrar al calendario. Antes de integrar un Reserve hay que comprobar distancia de 30 días, estado histórico, duplicación de concepto, disponibilidad editorial y cualquier bloqueo de canon.

## Controles preservados

Se mantuvieron todas las columnas históricas de `Content_Inventory.csv`. No se modificó el repositorio de canon, no se alteró `Publication_Log.csv`, no se alteró `ExperimentLog.csv`, no se publicaron assets, no se movió Drive y no se creó ninguna tarea de automatización.

## Siguiente lote recomendado

El siguiente trabajo debe ser una revisión editorial de los 92 Reserve con evidencia exacta en Drive. La prioridad no debe basarse únicamente en el ranking: hay que excluir piezas publicadas en los últimos 30 días, duplicados de concepto y assets que ya estén en la cola activa. Los tres registros sin evidencia exacta deben permanecer fuera hasta resolverlos.
