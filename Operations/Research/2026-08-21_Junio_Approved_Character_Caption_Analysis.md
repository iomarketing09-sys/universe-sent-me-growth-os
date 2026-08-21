---
title: "Análisis descriptivo de captions — 17 casos aprobados de personajes"
purpose: "Medir la distribución de propuestas de tratamiento de caption y su rendimiento descriptivo, sin convertir reglas automáticas en etiquetas históricas finales."
status: Review
created: 2026-08-21
updated: 2026-08-21
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Audit.csv"
  - "Operations/Research/2026-08-21_Junio_57_Approved_Character_Analysis.md"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
  - "Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Manual_Findings.md"
organization: "Operations/Research"
---

# Análisis descriptivo de captions — 17 casos aprobados de personajes

La auditoría conserva el texto exacto de Meta y genera una propuesta de tratamiento mediante reglas explícitas. Esta clasificación sirve para detectar qué casos merecen revisión manual; no modifica el ExperimentLog ni demuestra un efecto causal del caption.

## Distribución por tratamiento propuesto

| Tratamiento propuesto | n | Interacciones totales | Mediana interacciones | Shares totales | Mediana shares | Comentarios totales |
|---|---:|---:|---:|---:|---:|---:|
| `caption_conversacional` | 6 | 49 | 8.0 | 2 | 0.0 | 2 |
| `caption_minimo` | 8 | 79 | 10.5 | 7 | 1.0 | 9 |
| `caption_refuerzo` | 2 | 170 | 85.0 | 44 | 22.0 | 2 |
| `historical_unavailable` | 1 | 2 | 2 | 0 | 0 | 0 |

Tras la revisión manual de cuatro casos, el corte queda distribuido en ocho `caption_minimo`, seis `caption_conversacional`, dos `caption_refuerzo` y uno `historical_unavailable`. Los otros 13 casos siguen pendientes porque varias etiquetas dependen de si el caption ilumina la imagen, repite el texto visual o solo añade hashtags.

## Casos que requieren revisión manual prioritaria

La revisión manual confirmó cuatro casos: el outlier de Universe queda como `caption_refuerzo`, el caso de Ganso pasa a `caption_minimo`, el Wilfred corto conserva `caption_refuerzo` con ambigüedad y el Fantasma sin mensaje queda como `historical_unavailable`. Los 13 restantes siguen pendientes; en particular, las propuestas `caption_conversacional` requieren comprobar que existe una invitación real y no solo una pregunta retórica o una palabra interrogativa.

| Meta_ID | Propuesta | Confianza | Interacciones | Shares | Motivo de revisión |
|---|---|---|---:|---:|---|
| `1036844829507460_122130196011072582` | `caption_refuerzo` | Medium | 164 | 42 | Short declarative caption that may reinforce the visual reading; manual confirmation required. |
| `1036844829507460_122134608507072582` | `caption_minimo` | High | 14 | 2 | Short declarative caption that may reinforce the visual reading; manual confirmation required. |
| `1036844829507460_122130309663072582` | `caption_refuerzo` | Medium | 6 | 2 | Short declarative caption that may reinforce the visual reading; manual confirmation required. |
| `1036844829507460_122125895013072582` | `historical_unavailable` | High | 2 | 0 | Meta raw contains no message text. |

## Lectura analítica

El grupo `caption_minimo` puede mostrar una mediana distinta de `caption_conversacional`, pero esa comparación está contaminada por la selección visual de personajes, fechas, temas y posibles diferencias de formato. No se debe concluir que un tratamiento funciona mejor. Para comparar tratamientos dentro de una celda se requieren al menos dos casos por tratamiento y una estructura comparable; estos 17 casos no cumplen ese balance.

La única decisión válida en este momento es descriptiva: cuatro casos ya tienen revisión manual documentada y 13 permanecen pendientes. Las etiquetas confirmadas podrán usarse como covariable descriptiva en el análisis de personajes, pero no como resultado causal.

## Estado de los datos

Cuatro registros tienen `manual_review_status=Analyst_Reviewed`; los otros 13 permanecen en `Pending_Manual_Caption_Review`. El tratamiento no se copia al ledger experimental principal hasta que exista una revisión humana completa o una regla documental aprobada para el histórico.
