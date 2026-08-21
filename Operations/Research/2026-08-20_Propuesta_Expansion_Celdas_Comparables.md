---
title: "Propuesta de expansión — celdas comparables de narrativa y humor"
purpose: "Diseñar el siguiente lote de análisis del Growth OS para completar cinco celdas comparables y registrar por separado los tratamientos de caption."
status: Review
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv"
  - "Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Summary.json"
  - "Operations/Production/enrich_expansion_candidates.py"
  - "Operations/Production/summarize_expansion_cells.py"
  - "Operations/Research/2026-08-18_Analisis_Lote_A_Estructuras_Narrativas.md"
  - "Operations/Research/2026-08-19_Analisis_Lote_Dialogo_Transformacion.md"
  - "Operations/Research/2026-08-19_Analisis_Subgrupos_Humor_Acido.md"
  - "Operations/Research/2026-08-19_Analisis_Ampliacion_Humor_Sexual.md"
  - "Operations/Research/2026-08-18_Filtro_Expansion_58_Casos_GrowthOS.md"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
organization: "Operations/Research"
---

# Propuesta de expansión de celdas comparables

## 1. Decisión metodológica

La ampliación debe comenzar como **revisión histórica controlada**, no como publicación inmediata. Primero se deben revisar los candidatos ya disponibles, confirmar su estructura visual y asignar una función de humor sin forzar categorías. Solo los casos que cumplan la definición de su celda entrarán en el denominador comparable.

La regla de muestra queda separada en dos niveles. Una celda alcanza una **señal preliminar** con al menos tres casos comparables. Un **veredicto operativo** requiere cinco casos comparables y una definición de métrica consistente. Estos umbrales no convierten una señal en canon; únicamente determinan cuánto peso puede tener en el Growth OS.

## 2. Cobertura actual y brechas

| Celda | Casos comparables actuales | Candidatos para revisión | No contar todavía | Faltan para señal `n=3` | Faltan para veredicto `n=5` |
|---|---:|---:|---:|---:|---:|
| Microhistoria secuencial | 1 | 0 | 2 borderlines | 2 | 4 |
| Transformación visual | 2 | 0 | 0 | 1 | 3 |
| Humor observacional | 2 | 2 | 0 | 1 | 3 |
| Diálogo ácido | 1 | 1 | 2 borderlines | 2 | 4 |
| Autodesprecio / antihéroe | 2 | 2 | 0 | 1 | 3 |

Los conteos anteriores son deliberadamente conservadores. Un candidato no se incorpora solo porque tenga muchas interacciones: debe existir evidencia visual y una justificación funcional. Los outliers se conservan dentro de la muestra, pero se reportan también con análisis de sensibilidad para que no se conviertan en benchmark normal.

## 3. Candidatos prioritarios

| Celda | Caso base ya comparable | Candidatos de revisión prioritarios | Decisión de revisión |
|---|---|---|---|
| Microhistoria secuencial | `122129404893072582` — 155 interacciones, 19 shares | No hay candidato elegible todavía; `122130232503072582` y `122130032151072582` quedan como borderlines | Revisar solo para confirmar exclusión; buscar dos casos nuevos con turnos visuales claros. |
| Transformación visual | `122130196011072582` — 164/42; `122130324285072582` — 7/0 | No hay candidato elegible; `122130411897072582` queda excluido porque no confirma transformación de Universe | Buscar al menos un caso nuevo de transformación de Universe y registrar preservación de gafas/marcadores. |
| Humor observacional | `122132375181072582` — 24/4; `122132371125072582` — 36/8 | `122129214813072582` — 924/214; `122133575895072582` — 393/87 | Revisar función del remate y sensibilidad contextual; no mezclar observacional oscuro con observacional social sin nota. |
| Diálogo ácido | `122134161303072582` — 521/185 | `122132365443072582` — 394/70; `122130032151072582` y `122130232503072582` quedan como borderlines | Revisar Universe/Fantasma; no incorporar los borderlines sin evidencia del mecanismo ácido. |
| Autodesprecio / antihéroe | `122134136793072582` — 1,308/392; `122132350563072582` — 351/109 | `122132711259072582` — 20/3; `122132695779072582` — 9/0 | Confirmar si el remate es autodesprecio o solo ansiedad/relación. Mantener outliers separados en el reporte. |

Los números `interacciones/shares` son lifetime históricos. No deben mezclarse con snapshots 24/72 horas de agosto ni utilizarse para reabrir el ciclo P0.

## 4. Reglas de inclusión y exclusión

Un caso entra a una celda cuando la revisión visual confirma la estructura o función descrita, el Meta ID es único y las métricas tienen una definición conocida. La fuente de identidad puede ser Meta/asset revisado, pero el nombre del archivo no puede decidir el personaje ni el tipo de humor.

Un caso queda como `Borderline_Not_Comparable` si tiene apariencia de diálogo, pero carece de turnos visuales; si el remate es sexual/relacional, pero no es ácido; si parece autodesprecio, pero la evidencia solo muestra ansiedad; o si la transformación no conserva marcadores de Universe y requiere primero una revisión canónica.

Los casos con métricas cero no se eliminan. Se conservan como observaciones, pero no se usan para declarar que una categoría falla hasta verificar si el cero es rendimiento real o ausencia de acumulación útil.

## 5. Registro de tratamientos de caption

La capa de caption debe ser explícita y separada de la estructura visual. Para publicaciones históricas, el valor por defecto es `Needs_Reconstruction`; no se debe inferir el tratamiento a partir del texto dentro de la imagen. El caption exacto y su fuente deben conservarse cuando exista en Meta, Publication Log o un export histórico.

| Campo | Valores | Regla |
|---|---|---|
| `Caption_Treatment` | `caption_minimo`, `caption_refuerzo`, `caption_conversacional`, `historical_unavailable` | Un único valor por publicación; usar `historical_unavailable` si no existe caption verificable. |
| `Caption_Text` | Texto exacto | No resumir ni corregir el copy histórico. |
| `Caption_Source` | `Meta_export`, `Publication_Log`, `Historical_Top15`, `User_confirmed`, `Unavailable` | Registrar la fuente de la transcripción. |
| `Caption_Confidence` | `High`, `Medium`, `Low` | Depende de la exactitud de la fuente, no del rendimiento. |

Para nuevos tests, `caption_minimo` significa una pieza cuyo caption aporta entre cero y tres emojis o un remate mínimo sin explicación; `caption_refuerzo` añade una frase corta que cambia o ilumina la lectura; `caption_conversacional` añade una invitación natural o pregunta breve. El caption no debe repetir el texto visual.

Registrar el tratamiento no significa que ya se vaya a comparar su efecto. Con tres casos por celda solo se obtiene una señal de estructura/humor y el tratamiento queda como covariable. Para comparar tratamientos dentro de una misma celda se necesitan al menos dos casos por tratamiento, es decir, seis casos por celda, distribuidos en `2 × caption_minimo`, `2 × caption_refuerzo` y `2 × caption_conversacional`.

## 6. Lote de trabajo recomendado

El primer lote debe ser de **revisión y codificación**, no de publicación:

| Fase | Trabajo | Criterio de cierre |
|---|---|---|
| A | Revisar visualmente los cinco candidatos `Candidate_Review` y, si es necesario, las cuatro filas borderline | Cada caso tiene `Included`, `Excluded` o `Borderline`, con razón explícita |
| B | Completar la cobertura mínima de cinco celdas | No contar más de tres casos para señal preliminar hasta confirmar evidencia |
| C | Recuperar captions verificables de los casos incluidos | Cada fila tiene tratamiento, texto, fuente y confianza; si no, `historical_unavailable` |
| D | Analizar medianas, shares y sensibilidad a outliers | Reportar resultado con y sin outliers cuando un caso concentre la celda |
| E | Diseñar la siguiente cohorte futura | Solo después de conocer qué celdas siguen incompletas; no publicar sin aprobación humana |

En la fase E, si la revisión histórica no aporta suficientes casos, se diseñarán nuevas piezas como tests explícitos. Cada pieza deberá recibir antes de publicarse `Experiment_ID`, `Hypothesis_ID`, `Cell_ID`, `Caption_Treatment`, estructura narrativa, tipo de humor y campos de identidad canónica cuando corresponda.

## 7. Estado recomendado

La propuesta queda en `Review`. No se crean CNT, no se modifica el calendario y no se publican piezas con base en esta selección. La siguiente acción concreta es aprobar el lote de revisión visual y codificación; después se actualizará la cola con los casos incluidos y excluidos.

## Referencias

[1]: `2026-08-18_Analisis_Lote_A_Estructuras_Narrativas.md` — comparación inicial de estructuras.
[2]: `2026-08-19_Analisis_Lote_Dialogo_Transformacion.md` — ampliación de diálogo y transformación.
[3]: `2026-08-19_Analisis_Subgrupos_Humor_Acido.md` — subgrupos de humor ácido y outliers.
[4]: `2026-08-19_Analisis_Ampliacion_Humor_Sexual.md` — criterios para no confundir sexualidad con romance o insinuación.
[5]: `2026-08-18_Filtro_Expansion_58_Casos_GrowthOS.md` — filtro de selección de casos.
[6]: `2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv` — cola de candidatos y estado de comparabilidad.
[7]: `2026-08-20_Expansion_Celdas_Comparables_Summary.json` — resumen reproducible de brechas por celda.
[8]: `../../GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md` — reglas de aprendizaje, caption y salvaguardas de identidad.
