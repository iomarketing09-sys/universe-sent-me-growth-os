---
title: "Análisis descriptivo de captions — 17 casos aprobados de personajes"
purpose: "Medir la distribución de propuestas de tratamiento de caption y su rendimiento descriptivo, sin convertir reglas automáticas en etiquetas históricas finales."
status: Review
created: 2026-08-21
updated: 2026-08-21
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Audit.csv"
  - "Operations/Research/2026-08-21_Junio_57_Approved_Character_Analysis.md"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
organization: "Operations/Research"
---

# Análisis descriptivo de captions — 17 casos aprobados de personajes

La auditoría conserva el texto exacto de Meta y genera una propuesta de tratamiento mediante reglas explícitas. Esta clasificación sirve para detectar qué casos merecen revisión manual; no modifica el ExperimentLog ni demuestra un efecto causal del caption.

## Distribución por tratamiento propuesto

| Tratamiento propuesto | n | Interacciones totales | Mediana interacciones | Shares totales | Mediana shares | Comentarios totales |
|---|---:|---:|---:|---:|---:|---:|
| `caption_conversacional` | 6 | 49 | 8.0 | 2 | 0.0 | 2 |
| `caption_minimo` | 7 | 65 | 10 | 5 | 1 | 6 |
| `caption_refuerzo` | 3 | 184 | 14 | 46 | 2 | 5 |
| `historical_unavailable` | 1 | 2 | 2 | 0 | 0 | 0 |

La propuesta automática distribuye los casos en siete `caption_minimo`, seis `caption_conversacional`, tres `caption_refuerzo` y uno `historical_unavailable`. Sin embargo, la confianza final permanece sin confirmar: varias etiquetas dependen de si el caption ilumina la imagen, repite el texto visual o solo añade hashtags.

## Casos que requieren revisión manual prioritaria

Los tres casos propuestos como `caption_refuerzo` tienen confianza baja porque una frase breve puede estar reforzando la lectura o simplemente acompañando una imagen ya autosuficiente. Los seis casos propuestos como `caption_conversacional` requieren comprobar que existe una invitación real y no solo una pregunta retórica o una palabra interrogativa. El caso `historical_unavailable` no debe ser rellenado por inferencia.

| Meta_ID | Propuesta | Confianza | Interacciones | Shares | Motivo de revisión |
|---|---|---|---:|---:|---|
| `1036844829507460_122130196011072582` | `caption_refuerzo` | Low | 164 | 42 | Short declarative caption that may reinforce the visual reading; manual confirmation required. |
| `1036844829507460_122134608507072582` | `caption_refuerzo` | Low | 14 | 2 | Short declarative caption that may reinforce the visual reading; manual confirmation required. |
| `1036844829507460_122130309663072582` | `caption_refuerzo` | Low | 6 | 2 | Short declarative caption that may reinforce the visual reading; manual confirmation required. |
| `1036844829507460_122125895013072582` | `historical_unavailable` | Low | 2 | 0 | Meta raw contains no message text. |

## Lectura analítica

El grupo `caption_minimo` puede mostrar una mediana distinta de `caption_conversacional`, pero esa comparación está contaminada por la selección visual de personajes, fechas, temas y posibles diferencias de formato. No se debe concluir que un tratamiento funciona mejor. Para comparar tratamientos dentro de una celda se requieren al menos dos casos por tratamiento y una estructura comparable; estos 17 casos no cumplen ese balance.

La única decisión válida en este momento es de priorización: revisar primero los casos de confianza baja y conservar el texto Meta exacto. Una vez confirmadas manualmente las etiquetas, podrán usarse como covariable descriptiva en el análisis de personajes, pero no como resultado causal.

## Estado de los datos

Todos los registros permanecen en `Pending_Manual_Caption_Review` y `caption_confidence_final=Unconfirmed`. El tratamiento no se copia al ledger experimental principal hasta que exista una revisión humana o una regla documental aprobada para el histórico.
