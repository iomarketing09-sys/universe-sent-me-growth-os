---
title: "Propuesta de CNT y reuse para el lote prioritario de junio"
purpose: "Convertir los hallazgos de rendimiento, revisión visual y comentarios en una propuesta selectiva de piezas que podrían recibir CNT o entrar a reuse."
status: "Review"
created: 2026-08-18
updated: 2026-08-18
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-18_Junio_Lote_Priorizado_Difusion.md"
  - "Operations/Research/2026-08-18_Junio_Lote_Priorizado_Taxonomia_Visual.csv"
  - "Operations/Research/2026-08-18_Analisis_Comentarios_Junio_Lote_Prioritario.md"
  - "Operations/Research/Historical_Performance_Individuals.csv"
  - "GrowthOS/Content_Inventory.csv"
organization: "Operations/Research"
---

# Propuesta de CNT y reuse para junio

## Principio

No se crearán CNT para todos los assets confirmados. Un asset recibe propuesta de CNT solo si tiene evidencia suficiente para producción futura: Meta ID, relación visual/editorial, taxonomía observada, contexto legible y una decisión clara de uso. La aprobación creativa sigue siendo necesaria antes de modificar el inventario maestro.

## Subgrupo recomendado para decisión

| Asset | Evidencia | Propuesta | Motivo |
|---|---|---|---|
| `2607823` | 99 shares, 27 comentarios en ledger, 26 recuperados, Universe visible | CNT candidato + reuse condicionado | Combina difusión y conversación; revisar copy sexual/relacional antes de programar |
| `2607787` | 70 shares, diálogo Universe/Fantasma | CNT candidato + reuse prioritario | Pieza conversacional y etiquetable; personajes visibles sin depender del filename |
| `2607816` | 87 shares, Universe visible | CNT candidato + reuse | Humor social/ácido con lectura clara |
| `2607828` | 185 interacciones, Ganso visible | CNT candidato; reuse secundario | Amplía evidencia más allá de Universe y aporta humor de identidad |
| `260740` | 214 shares, 14 comentarios, pieza textual | CNT candidato con revisión editorial | Alto rendimiento, pero requiere cuidado por referencias a salud mental |
| `2607837` | 200 interacciones, Universe visible | Mantener como evidencia; reuse condicionado | Alto rendimiento, pero el tono sexual requiere revisión de plataforma y frecuencia |

## Piezas que no deben recibir CNT todavía

Los assets con personaje humano no identificado, sin match único de Drive o con contexto editorial ambiguo deben permanecer en la cola de investigación. Esto incluye, por ahora, `260747`, `260731`, `260765`, `260775`, `2607783`, `2607786`, `2607825`, `2607794`, `260735`, `260646`, `2607792`, `2607838` y `260757` hasta completar evidencia de archivo y decisión editorial.

## CNT creados tras la aprobación

Los seis registros fueron añadidos al inventario maestro como `CNT-080` a `CNT-085`. Todos quedaron en estado `Reuse_Candidate`, con publicación histórica separada de cualquier programación futura.

| CNT | Asset | Uso propuesto |
|---|---:|---|
| `CNT-080` | `2607823` | Reuse prioritario; conversación alta |
| `CNT-081` | `2607787` | Reuse prioritario; dúo Universe + Fantasma |
| `CNT-082` | `2607816` | Reuse prioritario medio; humor social |
| `CNT-083` | `2607828` | Reuse medio; Ganso |
| `CNT-084` | `260740` | Reuse medio; revisar referencias a salud mental |
| `CNT-085` | `2607837` | Reuse medio; revisar tono sexual |

La cola operativa se encuentra en `Operations/Research/2026-08-18_Cola_Reuse_Junio_Aprobada.csv`. La creación de estos CNT no mueve archivos de Drive, no publica contenido y no modifica el calendario.

## Próximo paso requerido

La aprobación de Fernando fue otorgada el 18 de agosto de 2026. Los seis CNT ya fueron creados y la cola de reuse quedó preparada. El siguiente paso, si se desea utilizar alguna pieza, será seleccionar fechas y slots en un calendario aprobado. Esta propuesta no autoriza por sí sola publicaciones ni movimientos en Drive.
