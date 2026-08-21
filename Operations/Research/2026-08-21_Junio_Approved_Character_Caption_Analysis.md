---
title: "Análisis descriptivo de captions — 17 casos aprobados de personajes"
purpose: "Medir la distribución de propuestas de tratamiento de caption y su rendimiento descriptivo, sin convertir reglas automáticas en etiquetas históricas finales."
status: Review
created: 2026-08-21
updated: 2026-08-21
version: "1.2"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Audit.csv"
  - "Operations/Research/2026-08-21_Junio_57_Approved_Character_Analysis.md"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
  - "Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Manual_Findings.md"
  - "Operations/Research/2026-08-21_Junio_Caption_Reclassification_Impact.md"
organization: "Operations/Research"
---

# Análisis descriptivo de captions — 17 casos aprobados de personajes

La auditoría conserva el texto exacto de Meta y registra tratamientos descriptivos después de una revisión manual de los 17 casos. Estas etiquetas no modifican el ExperimentLog ni demuestran un efecto causal del caption.

## Distribución por tratamiento propuesto

| Tratamiento propuesto | n | Interacciones totales | Mediana interacciones | Shares totales | Mediana shares | Comentarios totales |
|---|---:|---:|---:|---:|---:|---:|
| `caption_conversacional` | 2 | 24 | 12.0 | 1 | 0.5 | 1 |
| `caption_minimo` | 8 | 79 | 10.5 | 7 | 1.0 | 9 |
| `caption_refuerzo` | 6 | 195 | 6.5 | 45 | 0.5 | 3 |
| `historical_unavailable` | 1 | 2 | 2 | 0 | 0 | 0 |

La revisión manual de los 17 casos está completa. El corte queda distribuido en 8 `caption_minimo`, 2 `caption_conversacional`, 6 `caption_refuerzo` y 1 `historical_unavailable`. Todas las etiquetas tienen revisión documentada; las diferencias de confianza se conservan en el CSV.

## Decisiones revisadas manualmente

La revisión manual confirmó los 17 casos. Universe conserva `caption_refuerzo`; Ganso pasa a `caption_minimo`; la mujer mágica, Universe de reacción, Silvio y Wilfred interrogativo quedan como `caption_refuerzo`; los captions de hashtags, emojis o frases de acompañamiento quedan como `caption_minimo`; el roster mixto y Universe con CTA quedan como `caption_conversacional`; y Fantasma sin mensaje queda como `historical_unavailable`.

| Meta_ID | Propuesta | Confianza | Interacciones | Shares | Motivo de revisión |
|---|---|---|---:|---:|---|
| `1036844829507460_122130196011072582` | `caption_refuerzo` | Medium | 164 | 42 | Short declarative caption that may reinforce the visual reading; manual confirmation required. |
| `1036844829507460_122125544019072582` | `caption_minimo` | High | 18 | 2 | Short text dominated by emojis/hashtags or a minimal remate. |
| `1036844829507460_122125520661072582` | `caption_conversacional` | High | 15 | 1 | Question or invitation/CTA detected; manual confirmation required. |
| `1036844829507460_122134608507072582` | `caption_minimo` | High | 14 | 2 | Short declarative caption that may reinforce the visual reading; manual confirmation required. |
| `1036844829507460_122130329817072582` | `caption_minimo` | High | 13 | 1 | Short text dominated by emojis/hashtags or a minimal remate. |
| `1036844829507460_122128989885072582` | `caption_minimo` | High | 11 | 0 | Short text dominated by emojis/hashtags or a minimal remate. |
| `1036844829507460_122134065975072582` | `caption_minimo` | High | 10 | 1 | Short text dominated by emojis/hashtags or a minimal remate. |
| `1036844829507460_122131071243072582` | `caption_conversacional` | High | 9 | 0 | Question or invitation/CTA detected; manual confirmation required. |
| `1036844829507460_122134055109072582` | `caption_refuerzo` | Medium | 9 | 0 | Question or invitation/CTA detected; manual confirmation required. |
| `1036844829507460_122130324285072582` | `caption_refuerzo` | Medium | 7 | 0 | Question or invitation/CTA detected; manual confirmation required. |
| `1036844829507460_122126239515072582` | `caption_minimo` | High | 6 | 0 | Short text dominated by emojis/hashtags or a minimal remate. |
| `1036844829507460_122130309663072582` | `caption_refuerzo` | Medium | 6 | 2 | Short declarative caption that may reinforce the visual reading; manual confirmation required. |
| `1036844829507460_122133424479072582` | `caption_refuerzo` | Medium | 5 | 1 | Question or invitation/CTA detected; manual confirmation required. |
| `1036844829507460_122130032151072582` | `caption_refuerzo` | High | 4 | 0 | Question or invitation/CTA detected; manual confirmation required. |
| `1036844829507460_122133558903072582` | `caption_minimo` | High | 4 | 1 | Short text dominated by emojis/hashtags or a minimal remate. |
| `1036844829507460_122126670549072582` | `caption_minimo` | High | 3 | 0 | Short text dominated by emojis/hashtags or a minimal remate. |
| `1036844829507460_122125895013072582` | `historical_unavailable` | High | 2 | 0 | Meta raw contains no message text. |

## Lectura analítica

El grupo `caption_minimo` puede mostrar una mediana distinta de `caption_conversacional`, pero esa comparación está contaminada por la selección visual de personajes, fechas, temas y posibles diferencias de formato. No se debe concluir que un tratamiento funciona mejor. Para comparar tratamientos dentro de una celda se requieren al menos dos casos por tratamiento y una estructura comparable; estos 17 casos no cumplen ese balance.

La revisión completa permite usar las etiquetas como covariables descriptivas en el análisis de personajes, pero no como resultados causales. El grupo `caption_refuerzo` conserva una fuerte sensibilidad al outlier de Universe y no debe interpretarse como un efecto del tratamiento.

## Estado de los datos

Los 17 registros tienen `manual_review_status=Analyst_Reviewed`; `caption_confidence_final` queda en High o Medium según la evidencia. El tratamiento sigue fuera del ledger experimental principal porque el subconjunto no está balanceado por celda y la revisión no crea evidencia causal.
