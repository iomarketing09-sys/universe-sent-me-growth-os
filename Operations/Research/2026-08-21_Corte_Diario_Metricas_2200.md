---
title: "Corte diario de métricas de Meta — 22:00 local"
purpose: "Registrar el estado editorial observable de las publicaciones reales recientes y separar Reels y afiliados de los totales de imágenes."
status: Active
created: 2026-08-21
updated: 2026-08-21
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-20_Cohorte_17_30_Actual_Cut.md"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "Operations/Research/Affiliate_Metrics_Snapshots.csv"
  - "GrowthOS/07_00_Registro_Maestro_Reels.md"
organization: "Operations/Research"
---

# Alcance del corte
Corte realizado el **2026-08-21T22:03:03.767659-05:00** en `America/Matamoros`, con ventana de publicaciones desde el 20 de agosto a las 00:00 hasta el momento de consulta. Se encontraron **12 publicaciones reales**, todas con `is_published=true`: **10 imágenes/posts** y **2 Reels**.
Las cifras que siguen son acumulados lifetime observables en Meta al momento de consulta. No son incrementos exactos desde ayer ni snapshots exactos de 24 horas; por tanto, sirven para seguimiento diario de estado y ranking, pero no deben sustituir los cierres comparables de 24/72 horas.

## Resumen editorial por formato
| Formato | Publicaciones | Interacciones | Media | Mediana | Reacciones | Comentarios | Shares |
|---|---:|---:|---:|---:|---:|---:|---:|
| Imagen/post | 10 | 475 | 47.5 | 42.5 | 329 | 18 | 128 |
| Reel | 2 | 20 | 10.0 | 10.0 | 14 | 2 | 4 |
| **Total editorial** | **12** | **495** | **41.25** | **35.0** | **343** | **20** | **132** |

## Resumen por fecha local
| Fecha | Posts | Interacciones | Media | Mediana | Shares |
|---|---:|---:|---:|---:|---:|
| 2026-08-20 | 7 | 316 | 45.14 | 36 | 82 |
| 2026-08-21 | 5 | 179 | 35.8 | 30 | 50 |

## Top 10 por interacciones observables
| # | Fecha/hora local | Formato | Pieza/asset | Interacciones | Reacciones | Comentarios | Shares |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | 2026-08-20T10:00:23-05:00 | Image_or_post | 2607794 - Universe - Aver.. A ver... (22-jun-26).png | 79 | 53 | 0 | 26 |
| 2 | 2026-08-20T11:00:54-05:00 | Image_or_post | 2608038- Ganso - Mejor pudriendome en dinero.jpeg | 78 | 52 | 2 | 24 |
| 3 | 2026-08-21T11:00:07-05:00 | Image_or_post | 260635 - Universe.png | 63 | 47 | 0 | 16 |
| 4 | 2026-08-21T10:00:10-05:00 | Image_or_post | 2607838 - Dios - Quien me creo a mi (29-jun-26).png | 57 | 38 | 0 | 19 |
| 5 | 2026-08-20T17:00:13-05:00 | Image_or_post | 260508 - Universe.jpg | 49 | 35 | 2 | 12 |
| 6 | 2026-08-20T13:30:00-05:00 | Image_or_post | 260659 - Universe.png | 36 | 26 | 5 | 5 |
| 7 | 2026-08-20T16:00:03-05:00 | Image_or_post | 2608056 - Wilfred - Analize tu contexto.jpeg | 34 | 22 | 3 | 9 |
| 8 | 2026-08-21T13:30:00-05:00 | Image_or_post | 2608049 - Elara - Tibio tu cafe.jpeg | 30 | 21 | 2 | 7 |
| 9 | 2026-08-20T19:00:05-05:00 | Image_or_post | 2608041 - Maeve+kael - No me averguenza amar.jpeg | 29 | 24 | 2 | 3 |
| 10 | 2026-08-21T19:00:05-05:00 | Image_or_post | 260614 - Universe.png | 20 | 11 | 2 | 7 |

## Lectura del corte
Las imágenes/posts concentran **475 de 495 interacciones observables** en esta ventana. Los Reels acumulan **20 interacciones básicas en dos publicaciones**, pero no hay views, reach ni retención en esta extracción; no se concluye que el formato de video sea inferior a partir de este denominador incompleto.
Los líderes del corte son piezas de imagen con shares relativamente altos. La lectura es descriptiva: la ventana contiene pocas observaciones y mezcla publicaciones de reuse, nuevas y video. No se canoniza una familia ni un horario.

## Reels
- **2026-08-21T16:30:59-05:00 — Universe viéndote Farmear Aura :** 9 interacciones básicas (7 reacciones, 1 comentarios, 1 shares). Views, reach y retención: **no disponibles en este corte**.
- **2026-08-20T18:04:21-05:00 — Hay personas que se quedan en el retrovisor aunque ya no vayan contigo.:** 11 interacciones básicas (7 reacciones, 1 comentarios, 3 shares). Views, reach y retención: **no disponibles en este corte**.

## Afiliados — capa separada
El último registro disponible del ledger de afiliados es `MANUAL-20260820-7D-AFF07`, capturado el **2026-08-20 20:51**. Conserva sus propios denominadores y no se suma al engagement editorial. Estado visible: `Sin ventas visibles`; calidad: `Manual_Screenshot`.

## Limitaciones y siguiente uso
Este corte no actualiza `ExperimentLog` porque no es un snapshot exacto de 24/72 horas y no cambia el estado de los experimentos comparables. El siguiente corte debe reutilizar esta definición, añadir únicamente las publicaciones nuevas y, cuando Meta exponga views/reach de video, anexar esas métricas en la capa de Reels sin combinarlas con imágenes.

## Fuentes
- Meta Graph API v26, feed de la Página, respuesta guardada en `2026-08-21_Meta_Daily_Metrics_Raw.json`.
- `Operations/Research/2026-08-15_Publication_Log.csv`, para el cruce de Meta Post ID con pieza/CNT.
- `Operations/Research/Affiliate_Metrics_Snapshots.csv`, para la capa separada de afiliados.
