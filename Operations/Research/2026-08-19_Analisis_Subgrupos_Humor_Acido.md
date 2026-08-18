---
title: "Análisis de subgrupos de humor ácido — Junio"
purpose: "Determinar qué funciones narrativas del humor ácido concentran el rendimiento y separar señales reproducibles de outliers históricos."
status: "Review"
created: 2026-08-19
updated: 2026-08-19
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-19_Humor_Sexual_Acido_Codificado.csv"
  - "Operations/Research/2026-08-19_Humor_Acido_Subgrupos_Codificado.csv"
  - "Operations/Research/2026-08-19_Humor_Acido_Subgrupos_Resumen.csv"
  - "Operations/Research/2026-08-19_Analisis_Humor_Sexual_Acido.md"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
organization: "Operations/Research"
---

# Análisis de subgrupos de humor ácido

## Alcance y método

Se analizaron las 13 publicaciones codificadas como `humor_acido` en la muestra histórica de junio. La métrica principal es la interacción total disponible en Meta; shares y comentarios se usan como señales secundarias. Las medianas se priorizan sobre las medias porque la muestra contiene tres publicaciones con rendimiento extraordinario.

La clasificación conserva las etiquetas editoriales ya revisadas. No se fusionaron categorías solo para aumentar artificialmente el tamaño de muestra y no se interpretaron subgrupos con `n=1` como efectos causales.

## Resultado agregado

La muestra completa tiene **13 publicaciones**, una mediana de **20 interacciones**, una media de **181.1** y un total de **2,354 interacciones**. La diferencia entre media y mediana confirma una distribución muy concentrada.

| Subgrupo | n | Mediana interacciones | Mediana shares | Lectura actual |
|---|---:|---:|---:|---|
| Relacional/antihéroe | 1 | 1,308 | 392 | Señal extraordinaria, no replicable todavía |
| Relacional/diálogo | 1 | 521 | 185 | Señal extraordinaria, no replicable todavía |
| Insulto/autodesprecio | 1 | 351 | 109 | Señal extraordinaria, no replicable todavía |
| Observacional | 2 | 30 | 6 | Mejor microseñal repetida de la muestra |
| Relacional | 2 | 22.5 | 4.5 | Exploratoria, rendimiento moderado |
| Autocuidado irónico | 1 | 20 | 3 | Inconclusa |
| Insulto relacional | 1 | 16 | 0 | Inconclusa |
| Ansiedad relacional | 1 | 9 | 0 | Inconclusa |
| Infografía absurda | 1 | 9 | 4 | Inconclusa |
| Romántico absurdo | 1 | 8 | 0 | Inconclusa |
| Ciclos relacionales | 1 | 7 | 0 | Inconclusa |

## Concentración y outliers

Los tres casos con mayor rendimiento pertenecen a funciones diferentes: relacional/antihéroe, relacional/diálogo e insulto/autodesprecio. En conjunto representan **2,180 de las 2,354 interacciones**, es decir, **92.6%** de toda la muestra. Por esta razón sería incorrecto concluir que una sola función explica el éxito.

Los tres casos también comparten una propiedad más útil que la etiqueta formal: presentan un remate relacional muy claro, alto contraste entre personajes o una forma de autodesprecio inmediatamente reconocible. Esa propiedad debe tratarse como hipótesis transversal, no como categoría confirmada.

Al retirar esos tres outliers, las diez publicaciones restantes tienen una mediana de **12.5 interacciones**, una media de **17.4** y una mediana de **2.5 shares**. Esto muestra que el rendimiento típico del humor ácido en esta muestra es modesto; la mediana de 20 de la muestra completa todavía está influida por la distribución de los casos exitosos, aunque mucho menos que la media.

## Aprendizaje comparable

La única microseñal que aparece más de una vez y supera claramente el centro de la distribución es el humor **observacional**, con `n=2`, mediana de 30 interacciones y 6 shares. La muestra es demasiado pequeña para declararlo ganador, pero sí permite formular una prueba futura.

Los tres outliers sugieren una segunda hipótesis: **el humor ácido puede amplificarse cuando el conflicto interpersonal se entiende en una sola lectura y la imagen ofrece una relación clara entre personajes**. No hay evidencia suficiente para afirmar que el mecanismo sea el insulto, el autodesprecio o el diálogo por separado, porque cada función aparece una sola vez entre los casos extremos.

## Veredicto CGO

El humor ácido mantiene una señal histórica exploratoria, pero no existe todavía una subcategoría ganadora validada. La estrategia recomendada es conservarlo como familia editorial y probar en futuras olas tres variantes controladas: observacional cotidiano, diálogo ácido entre dos personajes y autodesprecio/antihéroe. Cada variante necesita varios casos comparables antes de recibir una decisión de reuse o una regla de calendario.

No se recomienda declarar que “el humor ácido funciona” en abstracto ni usar los tres outliers como benchmark normal. Tampoco se recomienda modificar el canon. Este análisis solo alimenta el Growth OS y debe contrastarse con el experimento P0 de agosto, manteniendo separadas las métricas Lifetime históricas de las mediciones operativas a 24/72 horas.

## Dependencias documentales

Este análisis requiere mantener consistentes las categorías del CSV base, la taxonomía visual de junio y las reglas de aprendizaje. No requiere actualizar documentos de Canon, el calendario activo, Instagram ni la cola de reuse.
