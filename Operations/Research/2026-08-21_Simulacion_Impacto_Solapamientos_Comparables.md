---
title: "Simulación de impacto de solapamientos semánticos — briefs comparables"
purpose: "Cuantificar sensibilidad de métricas y denominadores cuando los briefs comparables se mezclan indebidamente con celdas o familias de experimentos previos."
status: Active
created: 2026-08-21
updated: 2026-08-21
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-21_Validacion_Cruzada_Hipotesis_Briefs_Comparables.md"
  - "Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv"
  - "Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv"
  - "Operations/Production/2026-08-20_Wave1_Signal_Experiment_Design.csv"
  - "Operations/Research/simulate_comparable_overlap_impact.py"
organization: "Operations/Research"
---

# Simulación de impacto de solapamientos semánticos

## Alcance y método

Esta simulación no inventa resultados futuros ni intenta estimar causalidad. Usa los valores históricos observados en las celdas comparables como escenarios de sensibilidad para un caso nuevo: `cell_median`, `cell_mean` y `cell_max`. El escenario limpio agrega una sola pieza nueva; el escenario contaminado agrega la misma pieza dos veces, simulando una doble asignación al mismo denominador. Para Wave 1 se cuantifica únicamente la inflación de `n`, porque sus outcomes todavía están pendientes.

## Veredicto ejecutivo

Los cuatro briefs muestran `0` conflictos directos de IDs, pero la simulación confirma que los solapamientos sí pueden producir contaminación operativa. Cada asignación indebida de un brief a una familia Wave 1 de tres casos eleva artificialmente su denominador de `n=3` a `n=4`, un **+33.33%**, y hace que el caso duplicado represente `25.00%` del denominador contaminado. La simulación métrica de las celdas muestra que el sesgo de media depende de la distancia entre el caso nuevo y la distribución histórica; la mediana suele ser más estable, pero no debe considerarse inmune con muestras tan pequeñas.

> La decisión operativa es mantener cada brief en su `Cell_ID` primaria, no sumarlo a FAM-02/FAM-03/FAM-04/FAM-05 y no interpretar el cambio de media/mediana como efecto de contenido si existe doble pertenencia.

## Impacto de denominador por familia Wave 1

| Brief_ID | Familia solapada | n limpio | n contaminado | Inflación del denominador | Peso del duplicado | Hora compartida | Caption compartido |
|---|---|---:|---:|---:|---:|---|---|
| `FUT-MICRO-005` | `FAM-03` | 3 | 4 | 33.33% | 25.00% | Yes | Yes |
| `FUT-MICRO-006` | `FAM-02` | 3 | 4 | 33.33% | 25.00% | Yes | Yes |
| `FUT-MICRO-006` | `FAM-03` | 3 | 4 | 33.33% | 25.00% | Yes | Yes |
| `FUT-TRANS-003` | `FAM-05` | 3 | 4 | 33.33% | 25.00% | Yes | Yes |
| `FUT-ACID-003` | `FAM-04` | 3 | 4 | 33.33% | 25.00% | Yes | Yes |

La asignación de `FUT-MICRO-006` tiene dos proximidades semánticas (`FAM-02` y `FAM-03`), por lo que una clasificación indiscriminada podría contaminar dos denominadores en lugar de uno. La simulación no suma esos denominadores entre sí: los reporta como dos riesgos separados.

## Sensibilidad métrica por celda

| Brief_ID | Celda | Métrica | Escenario | n limpio | n contaminado | Media limpia | Media contaminada | Sesgo de media | Mediana limpia | Mediana contaminada | Sesgo de mediana |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `FUT-MICRO-005` | `MICRO-STRICT-3P` | `Interacciones` | `cell_median` | 2 | 3 | 155.00 | 155.00 | 0.00% | 155.00 | 155.00 | 0.00% |
| `FUT-MICRO-005` | `MICRO-STRICT-3P` | `Interacciones` | `cell_mean` | 2 | 3 | 155.00 | 155.00 | 0.00% | 155.00 | 155.00 | 0.00% |
| `FUT-MICRO-005` | `MICRO-STRICT-3P` | `Interacciones` | `cell_max` | 2 | 3 | 155.00 | 155.00 | 0.00% | 155.00 | 155.00 | 0.00% |
| `FUT-MICRO-005` | `MICRO-STRICT-3P` | `Shares` | `cell_median` | 2 | 3 | 19.00 | 19.00 | 0.00% | 19.00 | 19.00 | 0.00% |
| `FUT-MICRO-005` | `MICRO-STRICT-3P` | `Shares` | `cell_mean` | 2 | 3 | 19.00 | 19.00 | 0.00% | 19.00 | 19.00 | 0.00% |
| `FUT-MICRO-005` | `MICRO-STRICT-3P` | `Shares` | `cell_max` | 2 | 3 | 19.00 | 19.00 | 0.00% | 19.00 | 19.00 | 0.00% |
| `FUT-MICRO-006` | `MICRO-STRICT-3P` | `Interacciones` | `cell_median` | 2 | 3 | 155.00 | 155.00 | 0.00% | 155.00 | 155.00 | 0.00% |
| `FUT-MICRO-006` | `MICRO-STRICT-3P` | `Interacciones` | `cell_mean` | 2 | 3 | 155.00 | 155.00 | 0.00% | 155.00 | 155.00 | 0.00% |
| `FUT-MICRO-006` | `MICRO-STRICT-3P` | `Interacciones` | `cell_max` | 2 | 3 | 155.00 | 155.00 | 0.00% | 155.00 | 155.00 | 0.00% |
| `FUT-MICRO-006` | `MICRO-STRICT-3P` | `Shares` | `cell_median` | 2 | 3 | 19.00 | 19.00 | 0.00% | 19.00 | 19.00 | 0.00% |
| `FUT-MICRO-006` | `MICRO-STRICT-3P` | `Shares` | `cell_mean` | 2 | 3 | 19.00 | 19.00 | 0.00% | 19.00 | 19.00 | 0.00% |
| `FUT-MICRO-006` | `MICRO-STRICT-3P` | `Shares` | `cell_max` | 2 | 3 | 19.00 | 19.00 | 0.00% | 19.00 | 19.00 | 0.00% |
| `FUT-TRANS-003` | `TRANS-UNIVERSE` | `Interacciones` | `cell_median` | 3 | 4 | 85.50 | 85.50 | 0.00% | 85.50 | 85.50 | 0.00% |
| `FUT-TRANS-003` | `TRANS-UNIVERSE` | `Interacciones` | `cell_mean` | 3 | 4 | 85.50 | 85.50 | 0.00% | 85.50 | 85.50 | 0.00% |
| `FUT-TRANS-003` | `TRANS-UNIVERSE` | `Interacciones` | `cell_max` | 3 | 4 | 111.67 | 124.75 | 11.72% | 164.00 | 164.00 | 0.00% |
| `FUT-TRANS-003` | `TRANS-UNIVERSE` | `Shares` | `cell_median` | 3 | 4 | 21.00 | 21.00 | 0.00% | 21.00 | 21.00 | 0.00% |
| `FUT-TRANS-003` | `TRANS-UNIVERSE` | `Shares` | `cell_mean` | 3 | 4 | 21.00 | 21.00 | 0.00% | 21.00 | 21.00 | 0.00% |
| `FUT-TRANS-003` | `TRANS-UNIVERSE` | `Shares` | `cell_max` | 3 | 4 | 28.00 | 31.50 | 12.50% | 42.00 | 42.00 | 0.00% |
| `FUT-ACID-003` | `ACID-DIALOGUE` | `Interacciones` | `cell_median` | 3 | 4 | 457.50 | 457.50 | 0.00% | 457.50 | 457.50 | 0.00% |
| `FUT-ACID-003` | `ACID-DIALOGUE` | `Interacciones` | `cell_mean` | 3 | 4 | 457.50 | 457.50 | 0.00% | 457.50 | 457.50 | 0.00% |
| `FUT-ACID-003` | `ACID-DIALOGUE` | `Interacciones` | `cell_max` | 3 | 4 | 478.67 | 489.25 | 2.21% | 521.00 | 521.00 | 0.00% |
| `FUT-ACID-003` | `ACID-DIALOGUE` | `Shares` | `cell_median` | 3 | 4 | 127.50 | 127.50 | 0.00% | 127.50 | 127.50 | 0.00% |
| `FUT-ACID-003` | `ACID-DIALOGUE` | `Shares` | `cell_mean` | 3 | 4 | 127.50 | 127.50 | 0.00% | 127.50 | 127.50 | 0.00% |
| `FUT-ACID-003` | `ACID-DIALOGUE` | `Shares` | `cell_max` | 3 | 4 | 146.67 | 156.25 | 6.53% | 185.00 | 185.00 | 0.00% |

## Confusores adicionales

Las horas propuestas de los cuatro briefs (`16:00`, `18:00`, `20:00` y `22:00`) aparecen dentro de las franjas planificadas por Wave 1: `14:00, 16:00, 18:00, 20:00, 22:00`. Asimismo, los cuatro tratamientos (`caption_minimo`, `caption_refuerzo` o `caption_conversacional`) ya aparecen en la matriz Wave 1. Por ello, si una pieza se incorpora al calendario activo, `Hora_Test` y `Caption_Treatment` deben registrarse como covariables compartidas; no deben usarse como evidencia de que el solapamiento semántico causó el resultado.

El archivo de candidatos contiene muestras pequeñas y heterogéneas: la celda de transformación mezcla `164` y `7` interacciones; diálogo ácido mezcla `521` y `394`; microhistoria estricta tiene `n=1`. Los escenarios altos no son expectativas: solo muestran cuánto puede moverse la media cuando se duplica un caso extremo.

## Decisión operativa

1. Mantener `Cross_Validation_Status=PASS`. El registro formal de HB-006 a HB-009 no autoriza generación; cualquier cambio a `PASS_WITH_WARNINGS` vuelve a bloquear la promoción.
2. Mantener `MICRO-STRICT-3P`, `TRANS-UNIVERSE` y `ACID-DIALOGUE` fuera de los agregados Wave 1 aunque compartan tema, personaje, caption u horario.
3. No combinar `FUT-MICRO-006` con FAM-02 y FAM-03 simultáneamente; si se estudia la proximidad, elegir una sola celda primaria y registrar la otra como riesgo semántico.
4. Reportar siempre métricas con y sin outlier, además de `n` limpio y `n` contaminado; no cerrar ninguna hipótesis con esta simulación.

## Limitaciones

La simulación no produce outcomes de Wave 1, no estima conversiones, no corrige diferencias de calidad visual y no sustituye una prueba balanceada. Su función es demostrar el costo de una doble pertenencia y señalar qué variables deben mantenerse separadas en el análisis futuro.

## Referencias

[1]: `Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv` — outcomes históricos por celda.
[2]: `Operations/Production/2026-08-20_Wave1_Signal_Experiment_Design.csv` — familias, horarios y tratamientos planificados.
[3]: `Operations/Research/2026-08-21_Validacion_Cruzada_Hipotesis_Briefs_Comparables.md` — conflictos y solapamientos identificados.
