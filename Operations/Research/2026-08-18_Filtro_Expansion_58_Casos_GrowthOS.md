---
title: "Filtro de expansión para los 58 casos históricos sin match"
purpose: "Evitar analizar los 58 casos indiscriminadamente y seleccionar únicamente los que puedan responder una pregunta concreta del Growth OS."
status: "Active"
created: 2026-08-18
updated: 2026-08-18
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-18_Matriz_Aprendizajes_GrowthOS_Cinco_Casos.csv"
  - "Operations/Research/2026-08-18_Analisis_Detallado_Cinco_Casos_Fundacionales_Junio.md"
  - "Operations/Research/2026-08-18_Hipotesis_Archivo_Fundacional_Junio.md"
  - "Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv"
  - "GrowthOS/Integracion_Growth_OS.md"
organization: "Operations/Research"
---

# Filtro de expansión para los 58 casos históricos

## Principio

Un caso entra a análisis ampliado únicamente si puede aportar evidencia a una pregunta concreta de rendimiento o contenido. La falta de `Asset_Ref` no invalida sus métricas ni su revisión visual, pero tampoco justifica procesarlo sin una finalidad analítica.

## Preguntas válidas

| ID | Pregunta | Variables mínimas | Resultado esperado |
|---|---|---|---|
| Q1 | ¿Las microhistorias o diálogos generan más shares que el meme textual simple? | Formato, paneles, shares, interacciones | Comparación de mediana por estructura narrativa |
| Q2 | ¿La presencia de un personaje reconocible mejora la difusión? | Personaje visible, shares, interacciones | Comparación personaje vs no identificado |
| Q3 | ¿Las transformaciones absurdas de Universe conservan reconocimiento y difusión? | Universe visible, mutación visual, shares | Subgrupo de elasticidad visual |
| Q4 | ¿Los personajes secundarios con rasgo visual distintivo sostienen interacción? | Wilfred, Ganso, hada u otro personaje visible; interacciones | Comparación de personajes y roles |
| Q5 | ¿El tipo de humor explica diferencias de shares? | Absurdo, seco, literal, sexual, relatable, interacciones | Distribución por humor |
| Q6 | ¿La densidad visual o complejidad de escena aporta compartibilidad? | Cartel/carrusel/escena, densidad visual, shares | Comparación descriptiva, no causal |
| Q7 | ¿La conversación cambia según la estructura del post? | Comentarios disponibles, replies si existen, formato | Señal cualitativa de conversación |

## Regla de selección

Un caso se selecciona si cumple al menos dos de estas condiciones: pertenece al cuartil superior de shares o interacciones; contiene una variable editorial que pueda codificarse visualmente; presenta un formato o estructura narrativa distinta; o ayuda a completar una celda con pocos ejemplos.

La prioridad no será necesariamente el rendimiento absoluto. También se seleccionarán casos de bajo rendimiento cuando sirvan como contraste directo para una hipótesis, siempre que la comparación sea razonable.

## Lotes recomendados

| Lote | Objetivo | Tamaño sugerido |
|---|---|---:|
| A | Estructura narrativa: diálogo, paneles y escena | 8–12 casos |
| B | Personaje visible frente a no identificado | 10–15 casos |
| C | Humor: absurdo, seco, literalidad, sexual y relatable | 10–15 casos |
| D | Densidad visual y formato | 8–12 casos |

Los lotes pueden solaparse. No se debe analizar el mismo caso cuatro veces si ya responde varias preguntas; una sola fila enriquecida debe alimentar todas las comparaciones compatibles.

## Campos de salida

Cada caso seleccionado debe registrar fecha Meta, Meta ID, interacciones, reacciones, comentarios, shares, formato observado, personaje principal observado, secundarios, rol narrativo, tipo de humor, potencial de etiquetado, pregunta(s) respondida(s), evidencia visual, nivel de confianza y limitación.

## Veredictos permitidos

El análisis puede producir `Señal`, `Sin señal`, `Inconcluso` o `No comparable`. No puede producir una regla de canon ni una decisión de calendario por sí solo. Las muestras pequeñas deben expresarse como hipótesis para probar, no como leyes del Growth OS.

## Decisión actual

Los cinco casos detallados ya alimentan Q1, Q2, Q3, Q4, Q5 y Q6. El siguiente lote recomendado es el **Lote A**, porque la diferencia entre meme textual, escena de personaje y diálogo de tres paneles es directamente observable en los datos disponibles de Meta.
