---
title: "Reconciliación de históricos individuales con inventario y Drive"
purpose: "Clasificar los 39 registros individuales históricos frente a Content_Inventory.csv y Drive, y detectar lotes históricos adicionales pendientes de integración sin inventar relaciones CNT."
status: "Archived"
created: 2026-08-17
updated: 2026-08-17
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/Historical_Performance_Individuals.csv"
  - "Operations/Research/2026-08-17_Integracion_Individuales_Historicos_02.md"
  - "Operations/Research/2026-08-17_Reconciliacion_Historicos_Individuales.json"
  - "GrowthOS/Content_Inventory.csv"
  - "Operations/Research/2026-08-14_Reuse_Mayo_Ranking.csv"
  - "Operations/Research/2026-08-14_Revision_Reuse_Mayo_Junio_Datos.csv"
  - "Operations/Research/2026-08-14_Reuse_Mayo_Meta_Cruce_Datos.csv"
  - "Operations/Research/2026-08-14_Reuse_Mayo_Unmatched_Review.csv"
organization: "Operations/Research"
---

# Reconciliación de históricos individuales con inventario y Drive

> **Estado del documento:** Este informe conserva el corte previo a la creación de CNT. La decisión posterior integró los 28 assets de mayo como `CNT-040`–`CNT-067`; el informe vigente para esa integración es `2026-08-17_Integracion_CNT_Mayo_Reserve_Revision.md`.

## Dictamen

La reconciliación no encontró coincidencias CNT confirmadas para los 39 registros en `Content_Inventory.csv`. Sí encontró **28 assets exactos en la carpeta `05 Mayo` de Drive**, todos correspondientes al bloque de reuse de mayo. Los 11 top posts de junio–julio tienen Meta ID y métricas verificables, pero no tienen evidencia de archivo individual localizada en la carpeta `05 Mayo`, lo cual es esperable porque no son necesariamente assets de mayo.

En el corte original, por seguridad, **no se modificó `Content_Inventory.csv`**. Esa decisión fue posteriormente reemplazada por la integración controlada de los 28 assets de mayo, documentada por separado. El hecho de que un `260###` exista en Drive y tenga un Meta ID no basta para crear o asignar un `CNT-####`; falta una relación de inventario explícita o evidencia suficiente de que el asset corresponde a un concepto CNT existente.

## Resultado de los 39 registros

| Clasificación | Cantidad | Interpretación |
|---|---:|---|
| Coincidencia exacta en Drive | **28** | Filename/ref `260###` coincide con un archivo real en `05 Mayo`; incluye Drive ID. |
| CNT confirmado en Content_Inventory | **0** | El inventario actual solo contiene referencias exactas `260583`, `260539` y `260673`, ninguna del lote de 39. |
| Top posts junio–julio sin archivo Drive en `05 Mayo` | **11** | Tienen Meta ID y métricas, pero requieren evidencia de asset/Drive en sus carpetas históricas o una relación documental adicional. |
| CNT creados o modificados | **0** | No se inventaron vínculos. |

Los 28 Drive IDs quedan en la evidencia estructurada de reconciliación. Esto permite una futura incorporación controlada cuando se confirme el concepto creativo o se encuentre un CNT existente por filename, asset set o documento de producción.

## Lotes históricos adicionales pendientes

La revisión de datasets identificó los siguientes lotes que todavía pueden aportar publicaciones individuales:

| Dataset | Filas | Estado recomendado |
|---|---:|---|
| `2026-08-14_Reuse_Mayo_Ranking.csv` — `Reserve` | **95** | Pendiente secundario; ya contiene Meta ID y métricas, pero debe priorizarse solo si el asset sigue disponible y aporta valor para reuse. |
| `2026-08-14_Reuse_Mayo_Unmatched_Review.csv` | **8** | Pendiente de revisión documental; no integrar hasta completar la evidencia de filename/asset. |
| `2026-08-14_Reuse_Mayo_Meta_Cruce_Datos.csv` | **205** | Fuente amplia de posts de mayo; requiere deduplicación contra las 28 filas Top28 y clasificación de assets antes de añadir filas. |
| `2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv` | **508** | Fuente amplia de junio–agosto; ya se extrajeron 11 top posts, pero todavía contiene posts individuales no priorizados. |
| `2026-08-14_Revision_Reuse_Mayo_Junio_Datos.csv` | **133** | Inventario de assets de Drive; debe usarse como evidencia de disponibilidad, no como prueba automática de publicación. |

## Qué requiere aprobación o evidencia adicional

Las 28 filas de mayo pueden avanzar a una fase de reconciliación de inventario porque tienen filename exacto, Drive ID, Meta ID y métricas del ranking. Sin embargo, todavía no deben recibir CNT automáticamente. Primero hay que comprobar si el inventario debe representar cada meme como pieza individual o si algunos son variantes/repeticiones del mismo concepto.

Los 11 top posts de junio–julio deben cruzarse en una fase separada con sus carpetas históricas de Drive y con los filenames reales. La coincidencia por caption y Meta ID demuestra que la publicación existió, pero no prueba por sí sola qué archivo creativo la originó.

Los 95 registros `Reserve` y los 8 `Unmatched_Review` son trabajo adicional, no parte del lote confirmado. Los 205 cruces amplios y las 508 filas comparativas deben deduplicarse antes de incorporarse; añadirlos ahora duplicaría evidencia y contaminaría la lectura histórica.

## Regla de cierre

Un registro individual podrá enlazarse a un `CNT-####` solo si existe al menos una de estas combinaciones: (a) `Asset_Ref` y filename exactos ya presentes en `Content_Inventory.csv`; (b) documento de producción que nombre explícitamente el asset y el concepto CNT; o (c) reconciliación aprobada basada en Meta ID, filename/Drive ID y contexto editorial inequívoco. Mientras no se cumpla una combinación, el estado correcto es `Pending_Evidence` o `Filename_Candidate`, no `Confirmed_CNT`.

## Referencias

[1]: 2026-08-14_Reuse_Mayo_Ranking.csv "Ranking de reuse de mayo"
[2]: 2026-08-14_Reuse_Mayo_Meta_Cruce_Datos.csv "Cruce de publicaciones Meta de mayo"
[3]: ../../GrowthOS/Content_Inventory.csv "Inventario maestro del Growth OS"
