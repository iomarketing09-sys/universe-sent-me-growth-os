---
title: "Cruce Instagram–Facebook 17–30 de agosto de 2026"
purpose: "Separar las publicaciones de Instagram que duplican una fila ya programada en Facebook de las que requerirían un scheduler independiente."
status: "Review"
created: 2026-08-17
updated: 2026-08-17
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-17_Calendario_Instagram_17_30_Propuesto.md"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "Operations/Research/2026-08-17_Cruce_Instagram_Facebook_17_30.json"
  - "Operations/Production/instagram_15_16_scheduler_playbook.md"
  - "Operations/Research/2026-08-14_Recomendacion_Instagram_CGO.md"
organization: "Operations/Research"
---

# Cruce Instagram–Facebook 17–30 de agosto de 2026

## Dictamen

El cruce exacto por referencia de asset `260###` contra el `Publication_Log.csv` confirma que **las seis filas de la primera ola de Instagram ya tienen una publicación equivalente programada en Facebook**. Por lo tanto, el resultado del cruce actual es **0 filas exclusivas de Instagram** y **6 duplicaciones manuales potenciales en Meta**.

La fila `260633` ya fue publicada manualmente en Instagram y no debe repetirse. Las otras cinco pueden duplicarse manualmente en Meta cuando Fernando confirme que desea ejecutarlas. No se recomienda crear un scheduler para ninguna de estas seis filas mientras la duplicación manual siga siendo viable.

| Orden | Fecha | Hora | Asset | Publicación Facebook | Page Post ID | Estado Facebook | Estado Instagram |
|---:|---|---:|---|---|---|---|---|
| 1 | 17 ago | 10:00 | `260633 - Universe.png` | `PUB-FB-17_30-01` | `1036844829507460_122151373701072582` | Programada | Ya publicada fuera de ventana; no repetir |
| 2 | 19 ago | 13:30 | `260560 - Fantasma.png` | `PUB-FB-17_30-15` | `1036844829507460_122151374655072582` | Programada | Pendiente; duplicación manual recomendada |
| 3 | 21 ago | 19:00 | `260614 - Universe.png` | `PUB-FB-17_30-28` | `1036844829507460_122151375843072582` | Programada | Pendiente; duplicación manual recomendada |
| 4 | 23 ago | 22:00 | `260625.png` | `PUB-FB-17_30-37` | `1036844829507460_122151376629072582` | Programada | Pendiente; duplicación manual recomendada |
| 5 | 25 ago | 17:00 | `260613 - Wilfred.png` | `PUB-FB-17_30-48` | `1036844829507460_122151377553072582` | Programada | Pendiente; duplicación manual recomendada |
| 6 | 30 ago | 22:00 | `260528 - Universe.png` | `PUB-FB-17_30-74` | `1036844829507460_122151379707072582` | Programada | Pendiente; duplicación manual recomendada |

## Recomendación operativa

La estrategia híbrida es razonable, pero con una precisión importante: **duplicar manualmente en Meta no significa publicar inmediatamente sin revisar la fecha**. Cada fila debe conservar su fecha, hora, caption y cuenta correctos. Antes de cada duplicación se debe confirmar que el asset exacto coincide con el archivo Facebook y que la fila de Instagram no tiene `IG_Media_ID`, permalink ni estado publicado.

Para las filas que no dupliquen una publicación de Facebook en el futuro, sí puede utilizarse un scheduler exacto de una sola ejecución por fila. Ese scheduler debe tener una zona horaria única (`America/Matamoros`), tolerancia máxima de ±2 minutos, regla `no-op_late`, playbook autocontenido e idempotencia. No debe utilizar polling recurrente ni recuperar slots atrasados por inferencia.

## Regla de decisión

| Situación | Acción |
|---|---|
| Asset de Instagram tiene una fila Facebook programada con el mismo `260###` | Duplicar manualmente en Meta, conservando fecha, hora y caption aprobados. |
| Asset de Instagram no tiene fila Facebook equivalente | Considerar scheduler exacto por fila, después de aprobar el playbook y la hora. |
| Fila ya tiene `IG_Media_ID` o permalink | No volver a publicar. |
| Fila está marcada `Eliminada_Manualmente` o es `260583` | No tocar ni republicar. |
| Hora planeada ya pasó | No recuperar automáticamente; convertirla en una nueva decisión editorial. |

El análisis no crea relaciones `CNT-####`; únicamente cruza referencias exactas de assets y conserva los Page Post IDs reales devueltos por Meta.

## Fuente y controles

La evidencia estructurada completa está en [`2026-08-17_Cruce_Instagram_Facebook_17_30.json`](2026-08-17_Cruce_Instagram_Facebook_17_30.json). El cruce utilizó `Operations/Research/2026-08-15_Publication_Log.csv` y la propuesta `Operations/Research/2026-08-17_Calendario_Instagram_17_30_Propuesto.md`. No se llamó a Meta durante este análisis, no se modificó Facebook, Instagram ni Drive y no se creó ninguna tarea programada.

## Documentos relacionados que requieren coherencia

La recomendación híbrida debe reflejarse en la recomendación CGO de Instagram y en el playbook del scheduler. La propuesta de calendario no debe marcar automáticamente las cinco filas como publicadas: cada duplicación manual deberá registrar su resultado real después de que Meta devuelva el ID y el permalink.
