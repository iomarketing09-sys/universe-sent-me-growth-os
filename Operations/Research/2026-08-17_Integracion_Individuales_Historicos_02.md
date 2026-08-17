---
title: "Integración de publicaciones individuales históricas — lote 02"
purpose: "Incorporar publicaciones individuales verificables del ranking de reuse de mayo y de los top posts de junio–julio sin inventar CNT ni alterar los ledgers operativos actuales."
status: "Active"
created: 2026-08-17
updated: 2026-08-17
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/Historical_Performance_Snapshot.csv"
  - "Operations/Research/Historical_Performance_Individuals.csv"
  - "Operations/Research/2026-08-14_Reuse_Mayo_Ranking.csv"
  - "Operations/Research/2026-08-14_Reporte_Mensual_Junio_Julio_2026.md"
  - "Operations/Research/2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv"
  - "GrowthOS/08_00_Metricas_Baseline_Plataformas.md"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
organization: "Operations/Research"
---

# Integración de publicaciones individuales históricas — lote 02

## Resultado

El segundo lote histórico incorporó **39 publicaciones individuales verificables** en una capa de evidencia separada: **28 candidatos `Top28_Reuse_Candidate` de mayo** y **11 top posts de junio–julio** identificados por coincidencia de periodo, caption, Meta ID y métricas en el dataset comparativo.

Todos los registros tienen un Meta ID real y una fuente local explícita. Ninguno fue convertido automáticamente en `CNT-####`, y ningún registro se añadió al `Publication_Log.csv` operativo. La tabla histórica sirve para análisis, selección de reuse y formulación de hipótesis; no sustituye el historial append-only de publicaciones actuales.

## Composición del lote

| Grupo | Filas | Evidencia principal | Métrica |
|---|---:|---|---|
| Mayo — ranking de reuse | 28 | `2026-08-14_Reuse_Mayo_Ranking.csv`, con `best_post_id`, fechas y ranking. | `max_interactions` del ranking, con reacciones, comentarios y shares desglosados cuando están disponibles. |
| Junio — top posts | 5 | `2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv`, coincidencia por mes y texto del caption. | Reacciones + comentarios + shares. |
| Julio — top posts | 6 | `2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv`, coincidencia por mes y texto del caption. | Reacciones + comentarios + shares. |

## Top posts de junio–julio incorporados

| Periodo | Caption/concepto | Meta ID | Interacciones observadas en la fuente |
|---|---|---|---:|
| Junio | `El gato: 😧` | `1036844829507460_122132599809072582` | 1,128 |
| Junio | `a ver... a ver... 🤨` | `1036844829507460_122132690157072582` | 975 |
| Junio | `yo Aura Fuerte 😏` | `1036844829507460_122128723341072582` | 1,127 |
| Junio | `Me da miedo ser el malo de la historia...` | `1036844829507460_122134136793072582` | 1,308 |
| Junio | `🤡` | `1036844829507460_122129013585072582` | 785 |
| Julio | `🫣🫣` | `1036844829507460_122140003413072582` | 5,482 |
| Julio | `No es desinterés...` — Fantasma | `1036844829507460_122142779757072582` | 3,726 |
| Julio | `😭🫣` | `1036844829507460_122142627051072582` | 2,979 |
| Julio | `🥴🤯 escucho borroso....` | `1036844829507460_122140844349072582` | 3,913 |
| Julio | `😐` | `1036844829507460_122139999861072582` | 3,993 |
| Julio | `🙂‍↕️` | `1036844829507460_122141207841072582` | 2,747 |

## Reglas de interpretación

Los valores de mayo provienen de un ranking de reuse y no representan necesariamente el rendimiento total original del mes. Los valores de junio–julio provienen de una extracción comparativa con la definición `reacciones + comentarios + shares`; pueden diferir ligeramente de resúmenes narrativos anteriores por filtros, extracción o redondeo de la fuente. La discrepancia no se corrige inventando un valor: se conserva la fuente de cada fila.

Los nombres de formato se dejan como `Unknown_from_ranking` o `Unknown_from_dataset` cuando la fuente individual no los documenta explícitamente. El Meta ID y el asset/ref se conservan, pero el `CNT_ID` queda vacío hasta que exista reconciliación de inventario suficiente.

## Integración con el Growth OS

El CSV `Historical_Performance_Individuals.csv` se enlaza con `Historical_Performance_Snapshot.csv`, la baseline de plataformas y la fuente maestra. Estos datos alimentan tres usos permitidos: seleccionar reuse por evidencia, comparar patrones de copy/formato dentro de una misma definición métrica y formular hipótesis históricas. No alimentan directamente las columnas `Interacciones_24h` o `Interacciones_72h`, no cierran hipótesis actuales y no modifican los estados canónicos.

## Próximo lote

El siguiente lote puede reconciliar los top posts individuales contra `Content_Inventory.csv` y Drive, siempre que exista evidencia de filename/asset y no solo similitud textual. Después podrá ampliarse el conjunto individual de junio–julio, pero no es necesario para cerrar el objetivo del lote 02.
