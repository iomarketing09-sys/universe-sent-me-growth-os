---
title: "Validación cruzada de hipótesis — briefs comparables"
purpose: "Verificar colisiones de identificadores, solapamientos semánticos y contaminación con experimentos previos antes de generar assets."
status: Review
created: 2026-08-21
updated: 2026-08-21
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv"
  - "Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md"
  - "Operations/Production/2026-08-20_Wave1_Signal_Experiment_Design.csv"
  - "Operations/Research/2026-08-15_ExperimentLog.csv"
  - "GrowthOS/Integracion_Growth_OS.md"
  - "Operations/Production/validate_comparable_hypothesis_conflicts.py"
organization: "Operations/Research"
---

# Validación cruzada de hipótesis — briefs comparables

## Veredicto ejecutivo

No se detectaron colisiones directas de `Experiment_ID` ni de `Hypothesis_ID` contra los registros existentes para los cuatro briefs. El resultado es `4/4 sin conflicto duro`; sin embargo, `4` briefs quedan en `PASS_WITH_WARNINGS` porque sus hipótesis aún no están inscritas en el `HypothesisBank` local y usan el prefijo `H-COMP-*`, mientras la regla formal documentada utiliza `HB-###`.

> El resultado no debe interpretarse como autorización de generación. Antes de producir assets se debe resolver el registro/nomenclatura de las hipótesis y mantener separados los agregados que tienen solapamiento semántico con Wave 1.

## Matriz de verificación

| Brief_ID | Experiment_ID | Hypothesis_ID | Cell_ID | Estado | Conflicto directo | Advertencia de registro |
|---|---|---|---|---|---|---|
| `FUT-MICRO-005` | `EXP-2026-08-COMP-GAPS-01` | `H-COMP-MICRO3P-005` | `MICRO-STRICT-3P` | `PASS_WITH_WARNINGS` | `No` | Hypothesis_ID no registrado en HypothesisBank local y/o no cumple formato HB-### |
| `FUT-MICRO-006` | `EXP-2026-08-COMP-GAPS-01` | `H-COMP-MICRO3P-006` | `MICRO-STRICT-3P` | `PASS_WITH_WARNINGS` | `No` | Hypothesis_ID no registrado en HypothesisBank local y/o no cumple formato HB-### |
| `FUT-TRANS-003` | `EXP-2026-08-COMP-GAPS-01` | `H-COMP-TRANS-003` | `TRANS-UNIVERSE` | `PASS_WITH_WARNINGS` | `No` | Hypothesis_ID no registrado en HypothesisBank local y/o no cumple formato HB-### |
| `FUT-ACID-003` | `EXP-2026-08-COMP-GAPS-01` | `H-COMP-ACID-003` | `ACID-DIALOGUE` | `PASS_WITH_WARNINGS` | `No` | Hypothesis_ID no registrado en HypothesisBank local y/o no cumple formato HB-### |

## Solapamientos semánticos controlables

| Brief_ID | Solapamiento observado | Regla de separación |
|---|---|---|
| `FUT-MICRO-005` | FAM-03 / H-AUG-FAM03 (Conversación_Relacional): comparte contexto romántico/interpersonal; la celda sigue separada por estructura estricta de tres paneles y caption mínimo. | Mantener fuera del agregado FAM-03; usar `MICRO-STRICT-3P` como celda primaria y registrar el contexto romántico como confusor. |
| `FUT-MICRO-006` | FAM-02 / H-AUG-FAM02 (Relatable_Social) y FAM-03 / H-AUG-FAM03: comparte situación social/interpersonal; la secuencia exacta de tres paneles es la diferencia declarada. | No combinar automáticamente con FAM-02/FAM-03; conservar `MICRO-STRICT-3P` y `everyday_social_context` como definición primaria. |
| `FUT-TRANS-003` | FAM-05 / H-AUG-FAM05 (Personaje_Marcador) y HB-002 (Universe/formato Reel): comparte identidad visual de Universe, pero prueba transformación estática con preservación de gafas, no superioridad de personaje ni formato Reel. | No atribuir un resultado a Universe sin auditar identidad; mantener separado de FAM-05 y de HB-002, y excluir cambios de formato como explicación. |
| `FUT-ACID-003` | FAM-04 / H-AUG-FAM04 (Ácido_Interpersonal): solapamiento semántico directo de familia y métrica; la nueva celda restringe el caso a diálogo de dos voces con objetivo situacional seguro. | No mezclar en el mismo denominador sin declarar una subcelda; mantener `ACID-DIALOGUE` como estructura primaria y revisar que el ácido no sea genérico. |

## Conflictos con experimentos previos

La revisión cruzó los cuatro briefs contra los IDs presentes en `ExperimentLog`, los 15 registros conceptuales de `Wave_1_Signal_Experiment_Design.csv` y el `HypothesisBank` documentado en `Integracion_Growth_OS.md`. Los experimentos previos relevantes son `EXP-2026-08-BASELINE-01`, `EXP-2026-08-BASELINE-02`, `EXP-2026-08-BASELINE-03`, `EXP-2026-08-CAL-01` y `EXP-2026-08-FAM01-W1` a `EXP-2026-08-FAM05-W1`; ninguno coincide con `EXP-2026-08-COMP-GAPS-01`.

El principal riesgo no es una colisión de ID sino un solapamiento de variables. `FUT-ACID-003` es semánticamente próximo a `FAM-04`; `FUT-TRANS-003` comparte el marcador de Universe con `FAM-05` y el sujeto Universe con `HB-002`; `FUT-MICRO-005` se aproxima a `FAM-03`; y `FUT-MICRO-006` se aproxima a `FAM-02` y `FAM-03`. Las diferencias de `Cell_ID`, `Narrative_Structure` y controles de confusión permiten mantenerlos separados, pero los resultados no deben combinarse automáticamente.

El horario propuesto (`16:00`, `18:00`, `20:00`, `22:00`) se superpone con franjas usadas por Wave 1 y con la hipótesis histórica de horario `HB-003`. Por ello `Hora_Test` debe tratarse como covariable, no como resultado de estas hipótesis, y las piezas no deben presentarse como una prueba aislada del efecto horario.

## Acción requerida antes de generación

1. Resolver la nomenclatura de `H-COMP-*` frente a la regla `HB-###` y registrar las cuatro hipótesis en el `HypothesisBank`; no reutilizar un ID existente.
2. Mantener `EXP-2026-08-COMP-GAPS-01` como experimento separado de P0, `EXP-2026-08-CAL-01`, Wave 1, afiliados y reuse.
3. Conservar las cuatro celdas y no agrupar por familia Wave 1 solo porque comparten tema, personaje o métrica.
4. Revisar nuevamente `Caption_Treatment` y `Caption_Function` como variables distintas; el caption no debe absorber el efecto de la estructura visual.

## Reproducibilidad

El validador comparó 9 identificadores de experimento conocidos, 11 identificadores de hipótesis encontrados en ledgers/matrices y 5 entradas `HB-###` del bridge. Script: `Operations/Production/validate_comparable_hypothesis_conflicts.py`.

## Referencias

[1]: `Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv` — hipótesis y metadatos propuestos.
[2]: `Operations/Research/2026-08-15_ExperimentLog.csv` — experimentos y observaciones registrados.
[3]: `Operations/Production/2026-08-20_Wave1_Signal_Experiment_Design.csv` — matriz conceptual de Wave 1.
[4]: `GrowthOS/Integracion_Growth_OS.md` — HypothesisBank y ExperimentLog condensados.
[5]: `GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md` — convención de IDs y reglas de evidencia.
