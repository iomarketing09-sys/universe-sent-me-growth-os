---
title: "Análisis de ampliación de celdas comparables — ronda 2"
purpose: "Integrar dos nuevas microhistorias de dos paneles, evaluar la transformación de vestuario de Ganso y actualizar las señales comparables sin mezclar categorías no equivalentes."
status: Review
created: 2026-08-20
updated: 2026-08-21
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-20_Expansion_Round2_Candidatos.csv"
  - "Operations/Research/2026-08-20_Expansion_Round2_Summary.json"
  - "Operations/Research/2026-08-20_Expansion_Round2_Combined_Summary.json"
  - "Operations/Research/2026-08-21_Expansion_Celdas_Comparables_Post_Julio_Lote01.json"
  - "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Analysis.md"
  - "Operations/Research/2026-08-20_Expansion_Round2_Visual_Findings.md"
  - "Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv"
  - "Operations/Research/2026-08-20_Propuesta_Expansion_Celdas_Comparables.md"
  - "Operations/Research/2026-08-19_Analisis_Siguiente_Lote_Dialogo_Transformacion.md"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
organization: "Operations/Research"
---

# Análisis de ampliación de celdas comparables — ronda 2

## Resultado ejecutivo

La ronda 2 encontró **dos nuevas secuencias visuales de dos paneles**. Ambas son comparables entre sí, pero no deben mezclarse todavía con la microhistoria estricta de tres paneles. La mediana de estas dos piezas es de **361.5 interacciones y 39.5 shares**. Esto constituye una subcelda descriptiva prometedora, no un veredicto sobre la superioridad de dos paneles.

La ronda también confirmó que el caso de Ganso siendo vestido es una **transformación de vestuario de personaje secundario**, con 14 interacciones y 2 shares, no una nueva transformación corporal de Universe. La celda principal de transformación de Universe permanece en `n=2` y no alcanza la señal preliminar `n=3`.

## Celdas y brechas después de la ronda 2

| Celda | Casos comparables | Resultado de la ronda 2 | Faltan para señal `n=3` | Faltan para veredicto `n=5` |
|---|---:|---|---:|---:|
| Microhistoria estricta de tres paneles | 1 | Sin caso nuevo equivalente | 2 | 4 |
| Microhistoria de dos paneles | 2 | Subcelda nueva; mediana 361.5 interacciones / 39.5 shares | 1 | 3 |
| Transformación corporal/material de Universe | 2 | Sin caso nuevo de Universe | 1 | 3 |
| Transformación de vestuario secundario | 1 candidato | Ganso siendo vestido; señal aislada | 2 | 4 |
| Humor observacional | 3 | Mantiene señal preliminar, sin ampliar por sensibilidad de un caso de 924 interacciones | 0 | 2 |
| Diálogo ácido | 2 | Sin caso nuevo elegible | 1 | 3 |
| Autodesprecio/antihéroe | 2 + Ganso en revisión | Ganso puede ser autopercepción/antihéroe, no autodesprecio directo | 1 | 3 |

## Casos incorporados

`260731` contiene dos paneles y una secuencia relacional: una mujer comenta “Uff, qué buen ejercicio” y posteriormente dice “¡Gracias cariño!” mientras el hombre aparece agotado en la cama. El caso se registra como `MICRO2-001`, con 226 interacciones y 26 shares.

`260775` contiene dos paneles con una pregunta y una respuesta: “¿Y entonces qué somos?” seguido de “Mi máquina para hacer cardio”. El caso se registra como `MICRO2-002`, con 497 interacciones y 53 shares. Su función es relacional/sexual, no diálogo ácido.

Ambos casos tienen `Caption_Treatment=historical_unavailable`. El texto dentro de los paneles no se utiliza como sustituto del caption publicado.

## Casos que no se incorporan a las celdas principales

El candidato `122134608507072582` muestra a Ganso siendo vestido. Se conserva como `TRANS2-001`, candidato de una futura subcelda de transformación de vestuario secundario. No aporta evidencia adicional a la hipótesis de transformación de Universe.

`260766` muestra una composición simultánea de Universe dividido entre ángel y demonio. No demuestra una transformación temporal o un cambio de estado, por lo que queda excluido de la celda principal. `260728` es una escena de un solo panel y no cumple la secuencia mínima de dos paneles.

## Sensibilidad a outliers

La celda de diálogo ácido tiene dos casos actuales: 521 y 394 interacciones, con 185 y 70 shares. Su mediana es 457.5 interacciones y 127.5 shares; sin el caso marcado como outlier, la celda queda en `n=1`, con 394 interacciones y 70 shares. Por tanto, no existe todavía una señal estable.

La celda de autodesprecio/antihéroe tiene dos casos: 1,308 y 351 interacciones, con 392 y 109 shares. Su mediana es 829.5 interacciones y 250.5 shares; sin el outlier de 1,308 interacciones, queda en `n=1`, con 351 interacciones y 109 shares. La categoría sigue siendo una hipótesis, no una regla editorial.

La celda observacional conserva `n=3`, pero combina dos casos de 24 y 36 interacciones con un caso de 393. Por eso alcanza señal preliminar únicamente en el sentido de contar tres ejemplos visualmente comparables; no debe interpretarse como evidencia de que la categoría tenga rendimiento alto.

## Captions y límites

Los dos casos nuevos de microhistoria no tienen caption histórico recuperable en el Publication Log ni en el dataset de captions consultado. El análisis no estima ningún efecto de `caption_minimo`, `caption_refuerzo` o `caption_conversacional`. Para futuras publicaciones, estos tratamientos deben asignarse antes de publicar y mantenerse como una variable independiente de estructura, personaje y humor.

La ronda 2 confirma una regla operativa: **cuando aparece una nueva forma visual, primero debe abrirse una subcelda antes de incorporarla a una categoría existente**. Esto evita que una secuencia de dos paneles se convierta artificialmente en una secuencia de tres paneles o que una transformación de vestuario de Ganso se use como evidencia sobre la elasticidad visual de Universe.

## Estado posterior al lote 01 de julio

La ampliación individual de julio produjo cuatro candidatos funcionales para las celdas: `MICRO-004`, `OBS-005`, `SELF-006` y `SELF-007`. Solo `MICRO-004` se promovió a la subcelda de microhistoria de dos paneles, que ahora cuenta con tres casos comparables. `SELF-005` (Ganso) se promovió a la celda amplia de autodesprecio/antihéroe como subvariante de autopercepción absurda; la celda alcanza `n=3`, pero debe reportarse con sensibilidad porque sus casos son heterogéneos y uno tiene solo 15 interacciones.

`OBS-005` no se añade al denominador principal porque la celda observacional ya tiene `n=3`; se conserva para sensibilidad y comparación de escala. `SELF-006` y `SELF-007` permanecen como `Candidate_Review` porque podrían ser aislamiento o humor relacional, pero no demuestran por sí solos autodesprecio/antihéroe. Ningún candidato del lote 01 aportó evidencia suficiente para elevar transformación de Universe o diálogo ácido a `n=3`.

| Celda | Estado actual | Lectura operativa |
|---|---:|---|
| Microhistoria estricta de tres paneles | `n=1` | Sigue inconclusa; faltan dos casos comparables |
| Microhistoria de dos paneles | `n=3` | Señal preliminar descriptiva; no mezclar con tres paneles |
| Transformación corporal/material de Universe | `n=2` | Falta un caso; la búsqueda histórica revisada no produjo otro caso elegible |
| Humor observacional | `n=3` | Señal preliminar, sensible al outlier de 393 interacciones; `OBS-005` queda fuera del denominador |
| Diálogo ácido | `n=2` | Falta un caso; no se fuerza con escenas relacionales o captions sexuales |
| Autodesprecio/antihéroe | `n=3` | Señal preliminar heterogénea; Ganso se separa como autopercepción/antihéroe |

El snapshot reproducible de este corte está en `2026-08-21_Expansion_Celdas_Comparables_Post_Julio_Lote01.json`. La evidencia sigue siendo histórica y lifetime; no cambia calendario, CNT, canon ni la prueba de agosto.

## Decisión

La ampliación histórica queda documentada, pero ninguna celda nueva alcanza un veredicto operativo. La siguiente expansión no debe continuar buscando indiscriminadamente en el mismo pool: debe obtener casos comparables adicionales para la microhistoria de dos paneles, la transformación de Universe, el diálogo ácido y el autodesprecio/antihéroe. Si no existen más casos históricos con evidencia suficiente, esos faltantes deben convertirse en pruebas futuras explícitas con `Experiment_ID`, `Cell_ID`, hipótesis y tratamiento de caption registrados antes de la publicación.
