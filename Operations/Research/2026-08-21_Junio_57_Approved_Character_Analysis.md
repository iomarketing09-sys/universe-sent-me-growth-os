---
title: "Análisis cuantitativo — 17 casos aprobados de personajes en junio"
purpose: "Describir la distribución de lifetime interactions, shares y comments del subconjunto aprobado sin atribuir causalidad al personaje."
status: Active
created: 2026-08-21
updated: 2026-08-21
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-21_Junio_57_Unmatched_Character_Utility.csv"
  - "Operations/Research/2026-08-21_Junio_57_Unmatched_Visual_Findings.md"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
  - "Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md"
organization: "Operations/Research"
---

# Análisis cuantitativo — 17 casos aprobados de personajes en junio

Este corte es descriptivo. Los 17 casos fueron seleccionados por utilidad visual y no constituyen una muestra aleatoria; por lo tanto, sus medianas no pueden interpretarse como efecto causal de Universe, Wilfred, Ganso, Fantasma, Silvio u otro personaje.

## Comparación de grupos

| Grupo | n | Interacciones totales | Mediana interacciones | Shares totales | Mediana shares | Comentarios totales | Mediana comentarios |
|---|---:|---:|---:|---:|---:|---:|---:|
| 17 aprobados para personajes | 17 | 300 | 9 | 53 | 1 | 13 | 0 |
| 2 reservas de personaje | 2 | 5 | 2.5 | 0 | 0.0 | 1 | 0.5 |
| 36 controles de formato | 36 | 471 | 6.0 | 85 | 0.0 | 21 | 0.0 |
| 1 candidato de celda | 1 | 0 | 0 | 0 | 0 | 0 | 0 |

La lectura principal es que el subconjunto aprobado concentra señales visuales útiles, pero no puede competir limpiamente contra los controles porque fue seleccionado por legibilidad de personaje. El grupo se utiliza para validar identidad, rol y comparabilidad; no para declarar que un personaje rinde mejor.

## Confusores y sensibilidad descriptiva

El grupo Universe suma 201 de las 300 interacciones aprobadas (67.0%) y 44 de los 53 shares (83.0%). Esta concentración se debe principalmente al caso de 164 interacciones y 42 shares, por lo que cualquier lectura por personaje queda dominada por un outlier visual/estructural.
La razón shares/interacción es 17.7% en los 17 aprobados y 18.1% en los 36 controles. La diferencia es solo descriptiva: ambos grupos tienen distinta selección visual, distinta composición y no comparten control de hora, caption o temática.
El outlier 1036844829507460_122130196011072582 representa 54.7% de las interacciones y 79.2% de los shares del subconjunto aprobado. Sin ese caso, el grupo baja a 136 interacciones totales, mediana de 8.0 interacciones, 11 shares y mediana de 0.5 shares.

## Distribución por hipótesis visual

| Hipótesis visual | n | Mediana interacciones | Shares totales | Mediana shares | Comentarios totales |
|---|---:|---:|---:|---:|---:|
| Universe visual candidate | 5 | 11 | 44 | 1 | 5 |
| Wilfred visual candidate | 5 | 6 | 5 | 1 | 3 |
| Fantasma visual candidate | 2 | 7.5 | 1 | 0.5 | 0 |
| Ganso visual candidate | 1 | 14 | 2 | 2 | 3 |
| Mixed roster candidate; identities unconfirmed | 1 | 9 | 0 | 0 | 0 |
| Unidentified magical woman | 1 | 9 | 0 | 0 | 1 |
| Unknown woman + cat | 1 | 6 | 0 | 0 | 1 |
| Silvio visual candidate | 1 | 5 | 1 | 1 | 0 |

## Casos de mayor valor descriptivo

| Meta_ID | Hipótesis visual | Interacciones | Shares | Comentarios | Lectura |
|---|---|---:|---:|---:|---|
| `1036844829507460_122130196011072582` | Universe visual candidate | 164 | 42 | 2 | Prioridad descriptiva; no prueba causalidad |
| `1036844829507460_122125544019072582` | Wilfred visual candidate | 18 | 2 | 0 | Prioridad descriptiva; no prueba causalidad |
| `1036844829507460_122125520661072582` | Universe visual candidate | 15 | 1 | 1 | Prioridad descriptiva; no prueba causalidad |
| `1036844829507460_122134608507072582` | Ganso visual candidate | 14 | 2 | 3 | Prioridad descriptiva; no prueba causalidad |
| `1036844829507460_122130329817072582` | Fantasma visual candidate | 13 | 1 | 0 | Prioridad descriptiva; no prueba causalidad |
| `1036844829507460_122128989885072582` | Universe visual candidate | 11 | 0 | 2 | Prioridad descriptiva; no prueba causalidad |
| `1036844829507460_122134065975072582` | Wilfred visual candidate | 10 | 1 | 3 | Prioridad descriptiva; no prueba causalidad |
| `1036844829507460_122131071243072582` | Mixed roster candidate; identities unconfirmed | 9 | 0 | 0 | Prioridad descriptiva; no prueba causalidad |

## Conclusión operativa

Los 17 casos aprobados quedan listos para análisis de identidad y taxonomía, pero no justifican un ranking de personajes ni una regla de producción. La siguiente ampliación debe preguntar si una señal visual se mantiene dentro de una celda comparable, con controles de estructura y tema; no si un personaje es intrínsecamente mejor.

El candidato `1036844829507460_122127951885072582` se mantiene fuera de este corte de personajes porque su pregunta principal es estructural: cuatro paneles, turnos claros y remate. Su validación está definida por separado como `Pending_Cell_Validation`.

## Limitaciones

La selección no es aleatoria, los captions históricos no están disponibles de forma homogénea, el match Drive no está cerrado para estos 17 casos y no existe control equilibrado de hora. Por estas razones, este documento no modifica canon ni reglas de calendario.
