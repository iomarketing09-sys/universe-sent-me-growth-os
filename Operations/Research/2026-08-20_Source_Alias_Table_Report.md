---
title: "Reporte de tabla de aliases de fuente maestra"
purpose: "Documentar el cruce reproducible entre Publication Log e inventario mediante claves numéricas normalizadas, sin crear CNT automáticamente."
status: Active
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "GrowthOS/Content_Inventory.csv"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
organization: "Operations/Research"
---

# Reporte de tabla de aliases de fuente maestra

La tabla `2026-08-20_Source_Alias_Table.csv` cruza cada fila del Publication Log con el inventario mediante una clave numérica extraída de `Asset_Ref` o filename. La coincidencia no crea CNT ni sustituye una revisión editorial; solo hace explícita la relación operativa que puede verificarse.

| Métrica | Resultado |
|---|---:|
| Filas del Publication Log | 98 |
| Claves numéricas únicas observadas | 81 |
| Coincidencias únicas de alta confianza | 52 |
| Filas con revisión o sin match | 46 |
| Filas sin clave numérica extraíble | 3 |

Las filas `Review` deben resolverse mediante evidencia adicional de Drive/Meta o mantenerse como excepción. La tabla conserva el filename operativo, el `Meta_Post_ID`, el permalink y el estado de publicación para que la fuente maestra pueda completarse sin inventar relaciones.
