---
title: "Corte diario de métricas de Meta — 22 de agosto de 2026, 22:02 local"
purpose: "Registrar el estado diario observable de Facebook, separar imágenes de Reel y documentar las limitaciones de exposición del corte."
status: Active
created: 2026-08-22
updated: 2026-08-22
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-21_Corte_Diario_Metricas_2200.md"
  - "Operations/Research/2026-08-22_Meta_Daily_Metrics_Raw.json"
  - "Operations/Research/2026-08-22_Analisis_Corte_Diario_Familias_Personajes.md"
  - "Operations/Research/2026-08-16_Calendario_Operativo_17_30_Agosto.csv"
  - "Operations/Research/2026-08-15_ExperimentLog.csv"
  - "Operations/Research/Affiliate_Metrics_Snapshots.csv"
organization: "Operations/Research"
---

# Alcance del corte

El corte se realizó el **22 de agosto de 2026 a las 22:02:24 en `America/Matamoros`**, consultando el feed de la Página `Universe Sent Me` mediante Meta Graph API v26. Se recuperaron **6 publicaciones reales del día**: **5 imágenes/posts y 1 Reel**. La extracción es de acumulados observables al momento de consulta, no un incremento exacto de 24 horas ni un cierre de retención.

> **Regla de interpretación:** el post de las 22:00 acababa de publicarse cuando se tomó el corte. Sus shares no fueron expuestos y no debe tratarse como una publicación con cero shares ni usarse para juzgar el slot.

## Resumen por formato

| Formato | Publicaciones | Interacciones conocidas | Media descriptiva | Mediana descriptiva | Reacciones conocidas | Comentarios conocidos | Shares conocidos |
|---|---:|---:|---:|---:|---:|---:|---:|
| Imagen/post | 5 | 127* | 25.4* | 28* | 90* | 21* | 16* |
| Reel | 1 | 18 | 18.0 | 18 | 14 | 2 | 2 |
| **Total editorial conocido** | **6** | **145** | — | — | **104** | **23** | **18** |

\*Las cifras de imagen son una suma de campos expuestos e incluyen el slot recién publicado de las 22:00 con 0 reacciones/0 comentarios y shares no expuesto; para una lectura más limpia, los cuatro posts anteriores al slot de las 22:00 acumulan **127 interacciones conocidas**, media **31.75**, mediana **34**, **90 reacciones**, **21 comentarios** y **16 shares**.

## Detalle del día

| Hora local | Formato | Asset o caso | Interacciones conocidas | Reacciones | Comentarios | Shares | Lectura |
|---|---|---|---:|---:|---:|---:|---|
| 10:00 | Imagen | 2608050 — nueva | 51 | 39 | 4 | 8 | Líder del corte; personaje/familia pendientes de reconciliación. |
| 11:00 | Imagen | 260589 — reuse histórico | 28 | 13 | 12 | 3 | Máximo de comentarios; inventario marca personaje no identificado. |
| 13:30 | Imagen | 2608063 — nueva | 40 | 31 | 5 | 4 | Segunda señal de interacción; taxonomía pendiente. |
| 17:23 | Reel | MPM-001 — Elara caminando con audífonos y Wilfred detrás | 18 | 14 | 2 | 2 | L1 observable; views/reach/retención no disponibles. |
| 19:00 | Imagen | 260510 — reuse histórico | 8 | 7 | 0 | 1 | Exposición corta; inventario confirma Universe con confianza alta. |
| 22:00 | Imagen | CNT-083 / 2607828 — reuse | 0 conocidos | 0 | 0 | No expuesto | Recién publicado; no evaluable. |

## Lectura de concentración

Entre los cuatro posts de imagen anteriores al slot de las 22:00, el asset de las 10:00 lidera con **51 interacciones conocidas**, seguido por el de las 13:30 con **40** y el de las 11:00 con **28**. Esos tres acumulan **119 de 127 interacciones conocidas** del bloque de imágenes observado antes de las 22:00. La concentración es descriptiva y está condicionada por horas de exposición desiguales; no demuestra que una sola variable explique el rendimiento.

Los comentarios muestran una señal distinta de los shares: el post de las 11:00 concentra **12 de 21 comentarios** de las imágenes con campos observables, mientras que el post de las 10:00 lidera shares conocidos con **8**. Esto sugiere que conversación y difusión deben seguir tratándose como métricas separadas.

## Familias y personajes

No se fuerza una clasificación para las dos piezas nuevas `2608050` y `2608063` porque todavía no tienen reconciliación taxonómica permanente en el inventario. `260589` permanece como personaje no identificado, `260510` como Universe con confianza alta y `CNT-083/2607828` como Ganso con confianza alta según el inventario. El Reel MPM-001 pertenece a la celda de movimiento + POV/meme y se mantiene en el carril propio de Reels; no se mezcla con el promedio de imágenes.

## Hipótesis y decisiones

| Hipótesis | Evidencia de este corte | Estado |
|---|---|---|
| TAX-02 — situación reconocible/transferible favorece difusión más que personaje aislado | Los shares conocidos de imágenes se concentran en 2608050 (8), 2608063 (4) y 260589 (3), pero la muestra es pequeña y la taxonomía de dos assets es incompleta. | Compatible direccionalmente; no confirmada. |
| HUM-06 — caption mínimo/emojis pueden favorecer difusión | Se observan shares y reacciones en piezas con copy mínimo, pero no existe control balanceado por familia, personaje y edad de exposición. | Compatible; no universal ni causal. |
| HUM-02 — conflicto o remate conversacional aumenta comentarios | 260589 concentra 12 comentarios y 2608063 registra 5, pero no hay comparación pareada ni clasificación completa de humor. | Exploratoria. |
| HB-REEL-MOTION-POV-MEME-01 | MPM-001 alcanza 18 interacciones básicas observables, pero no hay views, reach ni retención. | L1 observable; no evaluable como celda de vídeo. |

El corte no modifica el estado de P0 ni introduce métricas 24/72 horas. La decisión operativa es continuar con el reporte diario, mantener la cadencia aprobada y esperar suficiente exposición para evaluar el post de las 22:00. El siguiente aprendizaje debe provenir del comportamiento de los reportes diarios posteriores, no de una comparación exacta de ventanas inventadas.

## Afiliados

Afiliados permanece en una capa separada. No se capturó un nuevo snapshot en este corte; el último registro disponible sigue siendo `MANUAL-20260820-7D-AFF07`, con estado registrado previamente como sin ventas visibles. No se suma al engagement editorial.

## Fuentes

[1]: `2026-08-22_Meta_Daily_Metrics_Raw.json` — extracción bruta de Meta del corte.
[2]: `2026-08-22_Corte_Diario_Metricas_2200.csv` — normalización por publicación.
[3]: `2026-08-22_Analisis_Corte_Diario_Familias_Personajes.csv` — desglose estructurado.
[4]: `2026-08-16_Calendario_Operativo_17_30_Agosto.csv` — cruce de horarios y assets.
[5]: `Affiliate_Metrics_Snapshots.csv` — capa separada de afiliación.
