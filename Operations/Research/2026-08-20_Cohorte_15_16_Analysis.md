---
title: "Análisis de la cohorte Facebook 15–16 de agosto"
purpose: "Comparar la cohorte de nueve publicaciones del 15–16 con evidencia observada de Meta, sin mezclarla con P0 ni sustituir ventanas 24/72h."
status: "Active"
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-19_P0_Next_Cut_Evidence.json"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "Operations/Research/2026-08-19_P0_Corte_17_Agosto.md"
organization: "Operations/Research"
---

# Resumen
La cohorte contiene **9 publicaciones** y registra **747 interacciones observadas**: 560 reacciones, 25 comentarios y 162 compartidos.
Estas cifras son acumulados lifetime observados en la consulta de Meta, no snapshots exactos de 24/72 horas.

## Desglose por publicación

| Publicación | CNT | Asset | Slot local | Reacciones | Comentarios | Compartidos | Interacciones |
|---|---|---|---:|---:|---:|---:|---:|
| PUB-FB-15_16-01 | CNT-031 | 2608030 - Universe - Que fibra tomas pa cagarla tanto.jpeg | 10:00 | 110 | 2 | 23 | 135 |
| PUB-FB-15_16-02 | CNT-032 | 260583 - Universe.png | 11:00 | 53 | 1 | 20 | 74 |
| PUB-FB-15_16-03 | CNT-033 | 2608033 - Fantasma - vendra primero mi boda o jesus.jpeg | 13:30 | 37 | 7 | 10 | 54 |
| PUB-FB-15_16-04 | CNT-034 | 260539 - Evan+Kiri.png | 19:00 | 172 | 3 | 52 | 227 |
| PUB-FB-15_16-05 | CNT-035 | 2608037- Universe - soñe que era un litrro de agua.jpeg | 10:00 | 75 | 2 | 15 | 92 |
| PUB-FB-15_16-06 | CNT-036 | 260673 - Universe.png | 13:30 | 42 | 3 | 11 | 56 |
| PUB-FB-15_16-07 | CNT-037 | 2608036- Elara+Evan - Nadie nos soporta.jpeg | 16:00 | 24 | 2 | 16 | 42 |
| PUB-FB-15_16-08 | CNT-038 | 2608060 - Kael+Maeve - gustos salvajones.jpeg | 19:00 | 29 | 2 | 6 | 37 |
| PUB-FB-15_16-09 | CNT-039 | humor4.16.png | 22:00 | 18 | 3 | 9 | 30 |

## Lectura estadística

La media fue de **83.0 interacciones por publicación** y la mediana de **56.0**. La diferencia entre media y mediana indica concentración en piezas de mayor rendimiento; no debe usarse la media sola para representar la cohorte.

## Cautelas

No se deben hacer inferencias causales sobre horario, formato o personajes sin una taxonomía completa y sin snapshots temporales equivalentes. Esta cohorte sirve como corte observado comparativo y como base para priorizar qué piezas merecen revisión editorial.

## Comparación con P0 del 17 de agosto

| Cohorte | Publicaciones | Interacciones observadas | Media por publicación |
|---|---:|---:|---:|
| 15–16 agosto | 9 | 747 | 83.0 |
| P0 del 17 agosto | 5 | 785 | 157.0 |

La media de P0 queda elevada por `2608028`, que registró 636 interacciones. Al excluir ese outlier, las otras cuatro piezas de P0 promedian **37.25 interacciones**, por debajo de la mediana de 56 de la cohorte 15–16. Esto evita una conclusión equivocada: P0 fue mejor por su outlier, pero la cohorte 15–16 fue más consistente que el resto de P0 sin `2608028`.

## Lectura por horario

La franja de **19:00** fue la más fuerte en esta cohorte, con 264 interacciones totales y una media de 132 en dos observaciones. La franja de **10:00** quedó en segundo lugar, con una media de 113.5 en dos observaciones. Las franjas de 13:30, 16:00 y 22:00 fueron menores, pero varias tienen solo una o dos observaciones y no permiten establecer una regla definitiva.

El mejor post de la cohorte fue `CNT-034 / 260539 - Evan+Kiri.png`, publicado a las 19:00, con 227 interacciones, 172 reacciones y 52 compartidos. Representa el 30.4% de las interacciones de la cohorte. Los dos mejores posts juntos representan 48.5%, una concentración relevante pero menos extrema que la de 2608028 en P0.

## Aprendizaje operativo

La evidencia respalda mantener **19:00 y 10:00 como franjas prioritarias para pruebas**, pero no autoriza a eliminar 13:30, 16:00 o 22:00. El dato más robusto no es solamente el horario: `CNT-034` muestra que una pieza de personajes y una composición con capacidad de compartir puede levantar una franja nocturna, mientras que `CNT-038` en la misma franja obtuvo 37. Por tanto, el contenido explica probablemente una parte importante de la diferencia.

La proporción de compartidos fue 21.7% de las interacciones observadas en la cohorte 15–16, frente a 25.1% en P0. La cohorte 15–16 tuvo más interacciones conversacionales relativas —25 comentarios sobre 747 interacciones— que P0 —10 sobre 785—, aunque esta comparación es descriptiva y no equivale a una tasa de alcance o impresiones.

### Ajuste para la siguiente ola

La siguiente ola debería reservar una cuota de piezas de alta compartibilidad en 19:00 y 10:00, mantener controles en 13:30 y 16:00, y no interpretar 22:00 a partir de una sola observación. Para validar el horario, se necesitan al menos dos piezas comparables por franja; para validar el formato, se necesita conservar la taxonomía de personajes, humor y estructura narrativa.

## Fuentes

- Evidencia de Meta conservada en `Operations/Research/2026-08-19_P0_Next_Cut_Evidence.json`.
- Registros operativos en `Operations/Research/2026-08-15_Publication_Log.csv`.
- Comparación reproducible en `Operations/Research/2026-08-20_Cohorte_15_16_vs_P0_Comparison.json`.
