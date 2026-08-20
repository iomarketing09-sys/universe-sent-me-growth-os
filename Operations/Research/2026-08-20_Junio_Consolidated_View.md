---
title: "Vista consolidada del histórico individual de junio"
purpose: "Usar una fila lógica por Meta ID para rankings y agregados sin eliminar las filas de evidencia originales."
status: Active
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/Historical_Performance_Individuals.csv"
  - "Operations/Research/2026-08-20_Junio_Duplicate_Groups.md"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
organization: "Operations/Research"
---

# Vista consolidada del histórico individual de junio

La vista `2026-08-20_Historical_Performance_Individuals_Consolidated.csv` contiene una fila por publicación lógica. El archivo fuente original permanece intacto y conserva las filas que aportan evidencia desde diferentes procesos de integración.

| Métrica | Resultado |
|---|---:|
| Filas fuente | 211 |
| Filas consolidadas lógicas | 206 |
| Grupos duplicados | 5 |
| Filas reducidas por consolidación | 5 |

Los cinco grupos duplicados de Meta ID tienen métricas de reacciones, comentarios y shares consistentes. Por ello pueden usarse una sola vez en agregados y rankings. La columna `source_row_ids` conserva las filas de origen y `sources_observed` conserva las fuentes de evidencia. Esta vista no cambia el canon, no crea CNT y no reemplaza el histórico fuente.
