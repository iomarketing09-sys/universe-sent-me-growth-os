---
title: "Propuesta de expansión — celdas comparables de narrativa y humor"
purpose: "Diseñar el siguiente lote de análisis del Growth OS para completar cinco celdas comparables y registrar por separado los tratamientos de caption."
status: Review
created: 2026-08-20
updated: 2026-08-21
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv"
  - "Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Summary.json"
  - "Operations/Production/enrich_expansion_candidates.py"
  - "Operations/Production/summarize_expansion_cells.py"
  - "Operations/Production/build_expansion_round2_contact_sheet.py"
  - "Operations/Production/analyze_expansion_round2.py"
  - "Operations/Production/analyze_expansion_round2_combined.py"
  - "Operations/Research/2026-08-18_Analisis_Lote_A_Estructuras_Narrativas.md"
  - "Operations/Research/2026-08-19_Analisis_Lote_Dialogo_Transformacion.md"
  - "Operations/Research/2026-08-19_Analisis_Subgrupos_Humor_Acido.md"
  - "Operations/Research/2026-08-19_Analisis_Ampliacion_Humor_Sexual.md"
  - "Operations/Research/2026-08-20_Expansion_Visual_Findings_01.md"
  - "Operations/Research/2026-08-20_Expansion_Round2_Candidatos.csv"
  - "Operations/Research/2026-08-20_Expansion_Round2_Analysis.md"
  - "Operations/Research/2026-08-20_Expansion_Round2_Visual_Findings.md"
  - "Operations/Research/2026-08-20_Filtro_Expansion_58_Casos_GrowthOS.md"
  - "Operations/Research/2026-08-21_Junio_57_Unmatched_Visual_Findings.md"
  - "Operations/Research/2026-08-21_Junio_57_Unmatched_Character_Utility.csv"
  - "Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md"
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
| Microhistoria estricta de tres paneles | 1 | 1 | 2 borderlines | 2 | 4 |
| Microhistoria secuencial — dos paneles | 3 | 0 | 0 | 0 | 2 |
| Transformación visual | 2 | 0 | 0 | 1 | 3 |
| Humor observacional | 3 | 2 | 0 | 0 | 2 |
| Diálogo ácido | 2 | 0 | 2 borderlines | 1 | 3 |
| Autodesprecio / antihéroe | 3 | 2 | 0 | 0 | 2 |

Los conteos anteriores son deliberadamente conservadores. Un candidato no se incorpora solo porque tenga muchas interacciones: debe existir evidencia visual y una justificación funcional. Los outliers se conservan dentro de la muestra, pero se reportan también con análisis de sensibilidad para que no se conviertan en benchmark normal.

## 3. Candidatos prioritarios

| Celda | Caso base ya comparable | Candidatos de revisión prioritarios | Decisión de revisión |
|---|---|---|---|
| Microhistoria secuencial | `122129404893072582` — 155 interacciones, 19 shares | `122127951885072582` — cuatro paneles con turnos telefónicos y baile; `122130232503072582` y `122130032151072582` quedan como borderlines | `Pending_Cell_Validation`: excluido de `MICRO-STRICT-3P` por contar cuatro paneles; retener como posible subcelda 4P y no reducir todavía el diseño de dos casos estrictos. |
| Transformación visual | `122130196011072582` — 164/42; `122130324285072582` — 7/0 | No hay candidato elegible; `122130411897072582` queda excluido porque no confirma transformación de Universe | Buscar al menos un caso nuevo de transformación de Universe y registrar preservación de gafas/marcadores. |
| Humor observacional | `122132375181072582` — 24/4; `122132371125072582` — 36/8; `122133575895072582` — 393/87 | `122129214813072582` — 924/214 | La revisión visual ya confirma tres casos comparables; revisar sensibilidad de `260740` antes de incorporarlo. |
| Diálogo ácido | `122134161303072582` — 521/185; `122132365443072582` — 394/70 | No hay candidatos elegibles adicionales; `122130032151072582` y `122130232503072582` quedan como borderlines | Falta un caso para señal `n=3`; no incorporar los borderlines sin evidencia del mecanismo ácido. |
| Autodesprecio / antihéroe | `122134136793072582` — 1,308/392; `122132350563072582` — 351/109 | `122134169481072582` — 15/1 | La revisión visual excluyó Silvio y ansiedad relacional; queda Ganso como autopercepción absurda/antihéroe, con discrepancia local `2607828` vs histórico `2607833`. |

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
| A | Revisar visualmente los dos candidatos restantes `Candidate_Review` y, si es necesario, las cuatro filas borderline | Cada caso tiene `Included`, `Excluded` o `Borderline`, con razón explícita; dos casos ya fueron promovidos en el corte 01 |
| B | Completar la cobertura mínima de cinco celdas | No contar más de tres casos para señal preliminar hasta confirmar evidencia |
| C | Recuperar captions verificables de los casos incluidos | Cada fila tiene tratamiento, texto, fuente y confianza; si no, `historical_unavailable` |
| D | Analizar medianas, shares y sensibilidad a outliers | Reportar resultado con y sin outliers cuando un caso concentre la celda |
| E | Diseñar la siguiente cohorte futura | Solo después de conocer qué celdas siguen incompletas; no publicar sin aprobación humana |

En la fase E, si la revisión histórica no aporta suficientes casos, se diseñarán nuevas piezas como tests explícitos. Cada pieza deberá recibir antes de publicarse `Experiment_ID`, `Hypothesis_ID`, `Cell_ID`, `Caption_Treatment`, estructura narrativa, tipo de humor y campos de identidad canónica cuando corresponda.

## 7. Resultado de la ronda 2

La ronda 2 incorporó una subcelda de `Microhistoria secuencial — dos paneles` con dos casos comparables: `260731` y `260775`. Su mediana descriptiva es de 361.5 interacciones y 39.5 shares. No se mezclan con la celda estricta de tres paneles, que permanece en `n=1`.

También se registró `TRANS2-001` como candidato de transformación de vestuario secundario para Ganso. No se considera evidencia de transformación de Universe. `260766` quedó excluido porque presenta dualidad simultánea, no transformación temporal, y `260728` quedó excluido por ser una escena de un solo panel.

El informe completo y la matriz de ronda 2 están en `Operations/Research/2026-08-20_Expansion_Round2_Analysis.md` y `Operations/Research/2026-08-20_Expansion_Round2_Candidatos.csv`. Los tratamientos de caption de los casos nuevos permanecen como `historical_unavailable`; no se estimó efecto de caption.

## 8. Estado recomendado

La propuesta sigue en `Review`. El corte visual 01 promovió `2607787` a diálogo ácido comparable y `2607816` a observacional comparable; añadió `2607828`/Meta ID `1036844829507460_122134169481072582` como candidato de autopercepción/antihéroe y excluyó Silvio y ansiedad relacional de esa celda. La ronda 2 añadió dos casos de microhistoria de dos paneles como subcelda separada. El lote 01 de julio añadió cuatro candidatos: `MICRO-004` fue promovido y la subcelda de dos paneles llegó a `n=3`; `OBS-005` quedó en revisión para sensibilidad observacional; `SELF-006`/`SELF-007` permanecen en revisión y Ganso fue promovido a la celda amplia de autodesprecio/antihéroe, que llegó a `n=3`. La revisión de los 57 posts sin match añadió `122127951885072582` como candidato de microhistoria estricta de cuatro paneles, sujeto a revisión funcional. La microhistoria estricta de tres paneles, transformación de Universe y diálogo ácido siguen bajo `n=3`; el diseño de casos mínimos está en `Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md`. No autoriza publicación, creación de CNT, modificación de calendario ni reuse.

## 9. Diseño de casos futuros para las brechas

El documento `Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md` define cuatro briefs condicionales: dos microhistorias estrictas de tres paneles como respaldo, una transformación de Universe con gafas y marcadores preservados, y un diálogo ácido interpersonal. La validación actual de `122127951885072582` confirma una microhistoria de cuatro paneles, pero no la promueve a la celda estricta; por prudencia se mantienen los dos briefs de tres paneles hasta que exista una definición separada de 4P. Estos casos no están aprobados para publicación y deben registrarse con `Cell_ID`, `Caption_Treatment`, `Hora_Test`, `Theme_Confound` y salvaguardas de identidad antes de entrar a calendario.

## Referencias

[1]: `2026-08-18_Analisis_Lote_A_Estructuras_Narrativas.md` — comparación inicial de estructuras.
[2]: `2026-08-19_Analisis_Lote_Dialogo_Transformacion.md` — ampliación de diálogo y transformación.
[3]: `2026-08-19_Analisis_Subgrupos_Humor_Acido.md` — subgrupos de humor ácido y outliers.
[4]: `2026-08-19_Analisis_Ampliacion_Humor_Sexual.md` — criterios para no confundir sexualidad con romance o insinuación.
[5]: `2026-08-18_Filtro_Expansion_58_Casos_GrowthOS.md` — filtro de selección de casos.
[6]: `2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv` — cola de candidatos y estado de comparabilidad.
[7]: `2026-08-20_Expansion_Celdas_Comparables_Summary.json` — resumen reproducible de brechas por celda.
[8]: `../../GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md` — reglas de aprendizaje, caption y salvaguardas de identidad.
