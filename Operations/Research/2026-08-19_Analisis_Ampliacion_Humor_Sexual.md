---
title: "Ampliación del análisis de humor sexual — Junio"
purpose: "Ampliar la muestra de humor sexual mediante revisión visual de casos de alto rendimiento y separar explícito, sugerente y doble sentido textual."
status: "Review"
created: 2026-08-19
updated: 2026-08-19
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-19_Humor_Sexual_Acido_Codificado.csv"
  - "Operations/Research/2026-08-19_Humor_Sexual_Acido_Ampliado_Codificado.csv"
  - "Operations/Research/2026-08-19_Humor_Sexual_Acido_Ampliado_Resumen.csv"
  - "Operations/Research/2026-08-19_Hallazgos_Ampliacion_Humor_Sexual.md"
  - "Operations/Research/2026-08-19_Analisis_Humor_Sexual_Acido.md"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
organization: "Operations/Research"
---

# Ampliación del humor sexual

## Alcance

Se revisaron visualmente 20 casos de junio sin clasificación sexual previa, seleccionados por rendimiento dentro de la cola de casos sin match. La revisión se realizó únicamente con imágenes y métricas disponibles de Meta. No se rastreó el origen de los assets, no se crearon CNT, no se programaron publicaciones y no se modificó el canon.

La ampliación tenía dos objetivos: encontrar ejemplos adicionales de sexualidad explícita y reunir una muestra comparable de insinuación o doble sentido sexual. Romance, pareja, enamoramiento, cuerpo o “ligar” no se clasificaron automáticamente como humor sexual.

## Resultado agregado

| Categoría | n | Mediana de interacciones | Mediana de comentarios | Mediana de shares | Estado |
|---|---:|---:|---:|---:|---|
| Humor sexual explícito | 2 | 35 | 2 | 5 | Inconcluso |
| Humor sexual sugerente | 5 | 24 | 1 | 2 | Exploratorio |

El grupo explícito aumentó de un caso a dos: el caso anterior de hada y humano, y una infografía con terminología sexual explícita. La muestra todavía es demasiado pequeña para afirmar que el humor explícito genera más o menos difusión.

El grupo sugerente aumentó a cinco casos. La mediana exploratoria es de 24 interacciones y 2 shares, pero la dispersión es muy alta debido a un outlier de doble sentido textual que obtuvo 171 interacciones y 50 shares. Sin ese outlier, la muestra sugerente sería mucho más modesta; por ello no debe interpretarse como efecto general del humor sexual.

## Casos que ampliaron la muestra

| Meta ID | Subgrupo | Interacciones | Shares | Lectura |
|---|---|---:|---:|---|
| `122127661851072582` | Doble sentido relacional | 24 | 0 | Texto sugerente; no sexualidad visual |
| `122128989885072582` | Doble sentido corporal | 11 | 0 | Remate textual; no contacto visual |
| `122130216549072582` | Infografía sexual explícita | 23 | 6 | Sexualidad explícita en formato informativo/absurdo |
| `122130232503072582` | Relacional/calzones | 27 | 2 | Insinuación textual entre humano y hada |
| `122134147251072582` | Doble sentido verbal | 171 | 50 | Outlier de texto; no debe representar todo el grupo |

## Veredicto

La ampliación permite mantener tres conclusiones prudentes. Primero, el humor sexual debe permanecer separado del humor ácido porque utiliza mecanismos narrativos distintos. Segundo, el humor sexual sugerente ya tiene una muestra exploratoria, pero su resultado está dominado por un outlier y no constituye una regla de producción. Tercero, el humor sexual explícito continúa inconcluso con `n=2`.

La hipótesis más útil para una investigación posterior no es “el sexo funciona”, sino: **los dobles sentidos sexuales textuales pueden producir difusión cuando el remate es inmediatamente comprensible y relatable**. Esta hipótesis sigue abierta porque el outlier es único y no hay control compatible.

No se recomienda incorporar estos resultados al calendario activo de agosto hasta cerrar la prueba del 17–30. Tampoco se recomienda crear CNT nuevos solo para ampliar la muestra histórica.
