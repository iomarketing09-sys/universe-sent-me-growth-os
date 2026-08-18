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

## Próximo paso requerido

Fernando debe aprobar o modificar el subgrupo recomendado. Después se crearán únicamente los CNT aprobados, se actualizará `Content_Inventory.csv` y se preparará una cola de reuse con distancia mínima de 30 días, contexto compatible y slot adecuado. Esta propuesta no autoriza publicaciones ni movimientos en Drive.
