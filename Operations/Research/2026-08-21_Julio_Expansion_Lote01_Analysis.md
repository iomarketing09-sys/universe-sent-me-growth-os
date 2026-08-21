---
title: "Análisis de ampliación individual de julio — lote 01"
purpose: "Medir el valor descriptivo de 16 publicaciones de julio reconciliadas visualmente, aplicar taxonomía conservadora y preparar la siguiente fase de celdas comparables."
status: Review
created: 2026-08-21
updated: 2026-08-21
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-21_Julio_Expansion_Individual_Lote01.csv"
  - "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Visual_Findings.md"
  - "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Taxonomy_Reviewed.csv"
  - "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Comments_Analysis.md"
  - "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Schedule_Analysis.json"
  - "Operations/Research/2026-08-17_Analisis_Julio_Taxonomia_y_Pendientes_Growth_OS.md"
  - "Operations/Research/2026-08-20_Propuesta_Expansion_Celdas_Comparables.md"
organization: "Operations/Research"
---

# Análisis de ampliación individual de julio — lote 01

## Alcance

El lote fue construido como la unión de las 12 publicaciones de julio con más shares y las 12 con más comentarios, excluyendo los seis top posts ya reconciliados individualmente. De los 17 candidatos iniciales, 16 obtuvieron un match visual Meta→Drive de alta confianza; un caso permanece en `Candidate_Review`. Los 16 casos confirmados se integraron al ledger histórico sin crear CNT.

| Capa | Antes del lote | Después del lote | Lectura |
|---|---:|---:|---|
| Publicaciones de julio con métricas comparables | 207 | 207 | La base mensual ya estaba completa |
| Publicaciones de julio reconciliadas individualmente | 6 | 22 | La cobertura individual pasa de 2.9% a 10.6% |
| Casos con evidencia visual Meta→Drive | 6 | 22 | Incluye seis top previos y 16 nuevos |
| Casos con taxonomía visual revisada | 6 | 22 | Los 16 nuevos tienen revisión conservadora asistida |
| CNT nuevos creados | 0 | 0 | Se mantiene la regla de no creación masiva |

## Resultado de rendimiento del lote ampliado

El lote ampliado no es una muestra aleatoria de julio: fue seleccionado por shares y comentarios. Por eso sus medianas describen una cola de alto interés, no el rendimiento típico de todo el mes. Su utilidad es ampliar la evidencia individual y localizar casos comparables, no estimar uplift causal.

| Muestra | n | Interacciones totales | Mediana interacciones | Mediana shares | Mediana comentarios |
|---|---:|---:|---:|---:|---:|
| Seis top posts originales | 6 | 22840 | 3819.5 | 1395.0 | 17.0 |
| 16 nuevos matches | 16 | 25065 | 1473.5 | 388.5 | 13.0 |
| 22 casos individuales de julio | 22 | 47905 | 1977.0 | 527.5 | 13.5 |
| Julio completo, base comparable | 207 | 68024 | 43 | 7 | 2 |

### Personaje principal observado

| Grupo | n | Mediana interacciones | Mediana shares | Mediana comentarios |
|---|---:|---:|---:|---:|
| Kiri | 1 | 665 | 127 | 14 |
| No identificado | 8 | 1977.0 | 527.5 | 12.5 |
| Universe | 7 | 1338 | 335 | 13 |

### Rol narrativo

| Grupo | n | Mediana interacciones | Mediana shares | Mediana comentarios |
|---|---:|---:|---:|---:|
| Dúo o pareja | 5 | 1076 | 322 | 12 |
| Escena observacional | 3 | 1035 | 368 | 16 |
| Protagonista | 8 | 1651.0 | 415.5 | 11.5 |

### Tipo de humor; una publicación puede aparecer en más de una categoría

| Grupo | n | Mediana interacciones | Mediana shares | Mediana comentarios |
|---|---:|---:|---:|---:|
| Existencial o absurdo | 6 | 1001.5 | 268.0 | 13.5 |
| Fandom o referencia | 1 | 1035 | 368 | 16 |
| Humor ácido o negro | 7 | 1609 | 335 | 9 |
| Observacional social | 2 | 2721.5 | 699.5 | 28.0 |
| Relatable cotidiano | 15 | 1338 | 368 | 13 |
| Sexual o insinuación | 1 | 1982 | 505 | 7 |

### Potencial de etiquetado

| Grupo | n | Mediana interacciones | Mediana shares | Mediana comentarios |
|---|---:|---:|---:|---:|
| Alto | 14 | 1473.5 | 388.5 | 13.5 |
| Medio | 2 | 1324.0 | 323.5 | 9.5 |

## Lectura CGO

La ampliación mejora sustancialmente la cobertura individual de julio, pero mantiene un sesgo deliberado hacia publicaciones con shares o comentarios altos. La señal descriptiva más sólida sigue siendo la combinación de situación legible, difusión social y potencial de etiquetado; no se puede atribuir el resultado a Universe como personaje porque una parte importante de la muestra contiene recursos visuales no canónicos o personajes genéricos.

La taxonomía también confirma que el filename `Universe - Existencial` continúa siendo insuficiente. Los 16 casos nuevos incluyen Universe visualmente identificable, gatos no canónicos, objetos conceptuales, personajes genéricos, una referencia a Kiri y escenas de pareja. Esta mezcla es precisamente la razón por la que la clasificación debe conservar evidencia visual y nivel de confianza por fila.

El lote queda listo para la siguiente fase: revisar qué casos completan celdas comparables. No se deben declarar nuevas señales operativas todavía. Los tratamientos de caption se mantienen como `historical_unavailable` y no se estima su efecto.

## Conversación y comunidad

Meta devolvió **284 comentarios** en las 16 publicaciones nuevas. La extracción se realizó en modo lectura y no generó respuestas. La clasificación descriptiva detectó 57 comentarios de humor/juego, 28 de identificación, 14 preguntas, 9 menciones y 2 señales explícitas de etiquetado social. Los 189 restantes no aportaron una categoría suficiente con reglas ligeras y se conservan como texto crudo en la evidencia.

El volumen no justifica analizar los 284 comentarios uno por uno. La siguiente prioridad cualitativa se concentra en `122136562323072582` — 70 comentarios devueltos —, `122141376093072582` — 40 —, `122139232911072582` — 30 — y `122135607981072582` — 15 — porque combinan conversación alta con preguntas o identificación. Esta prioridad es para aprendizaje histórico, no para moderación ni publicación de respuestas.

## Horario y control de confusión

La muestra individual ampliada tiene una concentración deliberada en horas con posts de alto rendimiento; por tanto, no puede medir uplift horario. El dataset completo de julio sigue siendo la fuente para la distribución temporal: sus medianas más útiles aparecen en 18:00, 22:00, 15:00 y 16:00, pero el contenido y los outliers están mezclados con cada hora. La capa individual solo permite cruzar qué tipos de pieza aparecen dentro de esas franjas.

La decisión operativa es no cambiar reglas de calendario históricas a partir de este lote. Para futuras pruebas, la hora debe registrarse como covariable junto con `Cell_ID`, estructura visual, `Caption_Treatment`, potencial de etiquetado y condición nuevo/reuse.

## Limitaciones

Las métricas son lifetime históricas y no son ventanas de 24/72 horas. El lote no representa el promedio de julio, porque fue seleccionado por rendimiento social. La clasificación asistida fue revisada de forma conservadora; cualquier modificación canónica requiere revisión separada con Claude. El caso borderline `1036844829507460_122142624879072582` no está incluido en las 16 filas confirmadas.

## Referencias

[1]: `Operations/Research/2026-08-21_Julio_Expansion_Lote01_Visual_Findings.md` — evidencia visual y estado de los 17 candidatos.
[2]: `Operations/Research/2026-08-21_Julio_Expansion_Lote01_Taxonomy_Reviewed.csv` — taxonomía revisada de los 16 matches.
[3]: `Operations/Research/Historical_Performance_Individuals.csv` — ledger individual histórico actualizado.
[4]: `Operations/Research/2026-08-20_Comparativo_Crecimiento_Junio_Julio.json` — referencia comparable completa de julio.
[5]: `Operations/Research/2026-08-20_Propuesta_Expansion_Celdas_Comparables.md` — umbrales para completar las celdas narrativas.
[6]: `Operations/Research/2026-08-21_Julio_Expansion_Lote01_Comments_Analysis.md` — resumen descriptivo de comentarios.
[7]: `Operations/Research/2026-08-21_Julio_Expansion_Lote01_Schedule_Analysis.json` — cruce reproducible de horas y confusores.
