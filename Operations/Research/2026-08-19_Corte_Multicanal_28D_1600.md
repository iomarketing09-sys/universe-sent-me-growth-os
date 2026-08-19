---
title: "Corte multicanal de 28 días — actualización 16:00"
purpose: "Registrar la extracción reciente de Facebook, Instagram, TikTok y YouTube, sus métricas nativas y los límites de comparabilidad para el dashboard de Universe Sent Me."
status: Active
created: 2026-08-19
updated: 2026-08-19
version: "1.0"
author: "Manus AI"
related_documents:
  - "2026-08-19_Social_Performance_28D_Normalizado.json"
  - "2026-08-19_Windsor_Facebook_Organic_28D_Normalizado.json"
  - "2026-08-19_Retorno_Engagement_Esfuerzo_28D.json"
  - "2026-08-19_Historial_Reels_Consolidado.json"
  - "../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
---

# Corte multicanal de 28 días — actualización 16:00

## Resultado

El corte cubre **22 de julio–18 de agosto de 2026**. Windsor actualizó Instagram, TikTok y YouTube; Facebook orgánico se extrajo en dos consultas de Windsor por el tiempo de respuesta del lote completo. La métrica de Facebook permanece como **reacciones + comentarios + shares**, no `post_engagements`.

| Plataforma | Piezas | Engagement nativo | Views | Lectura válida |
|---|---:|---:|---:|---|
| Facebook | 143 | 33,482 | — | 234.1 interacciones por publicación; métrica canónica de Meta. |
| Instagram | 34 | 56 | 1,650 | Snapshot lifetime actual de piezas del corte. |
| TikTok | 7 | 23 | 2,268 | Snapshot lifetime actual; una fila deduplicada por `video_id`. |
| YouTube | 6 | 36 | 5,022 | Actividad diaria acumulada; el snapshot lifetime se conserva aparte. |

Facebook sigue liderando el retorno operativo por publicación. Instagram tiene la mayor intensidad relativa por views observadas (**3.39 engagement por cada 100 views**) entre las plataformas con views comparables, pero esta señal no equivale a una comparación de alcance ni de ventana con TikTok o YouTube. El historial de Reels mantiene **45 registros**, **17 cascadas confirmadas** y **cero revisiones cross-platform pendientes**.

## Calidad de evidencia

Las métricas de Instagram, TikTok y YouTube son nativas de Windsor. Facebook se conserva en filas por publicación de Windsor y se cruza con Graph API para identidad/formato cuando haga falta; el Page feed se consultó como control de disponibilidad y no sustituye el dataset analítico. No se agregan views lifetime de YouTube a la actividad diaria.
