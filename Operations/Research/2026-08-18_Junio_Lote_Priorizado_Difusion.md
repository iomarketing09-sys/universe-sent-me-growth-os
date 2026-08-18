---
title: "Lote prioritario de junio por difusión"
purpose: "Seleccionar el primer lote de publicaciones históricas de junio para revisión editorial, conversación, CNT selectivo y posible reuse."
status: "Review"
created: 2026-08-18
updated: 2026-08-18
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-17_Reporte_Final_Recopilacion_Junio.md"
  - "Operations/Research/2026-08-18_Junio_Lote_Priorizado_Difusion.csv"
  - "Operations/Research/2026-08-18_Junio_Lote_Priorizado_Difusion_Enriquecido.csv"
  - "Operations/Research/Historical_Performance_Individuals.csv"
  - "Operations/Research/June_Visual_Asset_Index.csv"
  - "GrowthOS/Content_Inventory.csv"
organization: "Operations/Research"
---

# Lote prioritario de junio por difusión

## Criterio

El lote inicial se seleccionó desde las 177 filas individuales de junio en `Historical_Performance_Individuals.csv`, ordenando primero por shares, después por interacciones y finalmente por comentarios. Esta es una cola de investigación, no una autorización automática de publicación, CNT o reuse.

La prioridad editorial debe favorecer piezas con shares altos, conversación visible, asset localizable y distancia suficiente desde su publicación anterior. Las métricas son lifetime históricas y no deben mezclarse con el experimento P0 de 24/72 horas.

## Resultado inicial

Se seleccionaron 25 filas. Doce referencias cuentan con un filename exacto único en el índice visual de junio; las demás requieren búsqueda manual, normalización del Asset_Ref o se mantienen como candidatos de investigación. El cruce se hará por Asset_Ref, filename, Meta ID y evidencia visual, sin inferir el personaje solo por la convención `Universe - Existencial`.

| Grupo | Uso inmediato |
|---|---|
| Top con asset/Meta/Drive confirmados | Revisar visualmente, completar taxonomía y analizar comentarios |
| Alto rendimiento sin match de Drive | Resolver manualmente antes de crear CNT |
| Reuse candidato | Verificar distancia de 30 días, contexto y continuidad antes de programar |
| Solo evidencia histórica | Mantener en el ledger; no crear CNT por defecto |

## Próxima secuencia

Primero se revisará visualmente el sublote con match único en Drive. Después se añadirá la taxonomía editorial normalizada y se decidirá cuáles piezas justifican análisis de comentarios. Solo las piezas aprobadas para uso futuro recibirán CNT o pasarán a una cola de reuse. Las decisiones de canon permanecen separadas y requieren revisión con Claude.

## Limitaciones

El ranking no prueba causalidad ni superioridad de personaje. Los shares lifetime pueden haber acumulado exposición durante periodos distintos y el orden sirve para priorizar trabajo, no para comparar directamente contra snapshots de 24/72 horas.
