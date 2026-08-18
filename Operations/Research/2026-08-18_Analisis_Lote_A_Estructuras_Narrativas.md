---
title: "Análisis Lote A — Estructuras narrativas"
purpose: "Comparar estructuras narrativas observables en diez publicaciones históricas de junio y determinar qué señales justifican una ampliación del Growth OS."
status: "Review"
created: 2026-08-18
updated: 2026-08-18
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-18_Lote_A_Estructuras_Narrativas.csv"
  - "Operations/Research/2026-08-18_Lote_A_Resumen_Comparativo.csv"
  - "Operations/Research/2026-08-18_Filtro_Expansion_58_Casos_GrowthOS.md"
  - "Operations/Research/2026-08-18_Matriz_Aprendizajes_GrowthOS_Cinco_Casos.csv"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
organization: "Operations/Research"
---

# Análisis del Lote A — Estructuras narrativas

## Alcance

El Lote A fue diseñado para responder si la **estructura narrativa** ayuda a explicar la difusión histórica: meme textual simple, escena de personaje, microhistoria secuencial, transformación visual y composición de mundo. La muestra contiene diez publicaciones de junio con Meta ID, fecha y métricas lifetime disponibles. No se utilizaron ventanas 24/72h ni se comparó con la prueba activa de agosto.

La comparación es **exploratoria**. La muestra no fue diseñada como experimento controlado y varias celdas tienen un solo caso. Por ello, sus resultados sirven para decidir qué analizar después, no para cerrar una regla editorial.

## Muestra

| Grupo | n | Publicaciones incluidas | Mediana de interacciones | Mediana de shares |
|---|---:|---|---:|---:|
| Microhistoria | 1 | `122129404893072582` | 155 | 19 |
| Transformación | 1 | `122130196011072582` | 164 | 42 |
| Escena de personaje | 5 | `122130232503072582`, `122129952933072582`, `122134608507072582`, `122125520661072582`, `122125544019072582` | 18 | 2 |
| Control texto simple | 2 | `122125528653072582`, `122128512777072582` | 27.5 | 4.5 |
| Composición de mundo | 1 | `122127916017072582` | 14 | 1 |

## Lectura de los resultados

### Microhistoria secuencial

El caso de tres paneles —“Te extraño / ¿y eso? / eso también te extraña”— obtuvo 155 interacciones y 19 shares. Es una señal compatible con la hipótesis de que una microhistoria de tres tiempos puede generar más compartibilidad que un texto aislado, especialmente cuando el remate depende de una interpretación literal de un personaje fantástico.

Sin embargo, `n=1` impide llamarlo resultado comparativo. La clasificación correcta es **Señal prometedora, inconclusa**. El siguiente lote debe buscar más diálogos, carruseles o composiciones secuenciales para aumentar la celda.

### Transformación visual

Universe en versión muscular obtuvo 164 interacciones y 42 shares. La pieza conserva las gafas y la identidad felina, pero introduce una mutación corporal extrema. Es una señal fuerte de elasticidad visual y de combinación entre personaje reconocible, exageración y caption breve.

La clasificación es **Señal prometedora, inconclusa** por `n=1`. La señal merece ampliarse porque comparte una métrica de shares especialmente alta, pero no debe convertirse todavía en una regla de producción.

### Escena de personaje

Las cinco escenas de personaje tienen una mediana de 18 interacciones y 2 shares. El grupo es heterogéneo: incluye una escena relacional humano-hada, dos hombres en un mundo fantástico, Ganso con traje, Universe en cama y Wilfred en bosque. La dispersión sugiere que “escena de personaje” es una categoría demasiado amplia para explicar por sí sola el rendimiento.

La clasificación es **Sin señal agregada**. Conviene subdividirla por remate, relación entre personajes, densidad visual y presencia de diálogo antes de extraer conclusiones.

### Control de texto simple

Los dos controles de texto sobre fotografía tienen una mediana de 27.5 interacciones y 4.5 shares. Aunque superan a la mediana de la categoría amplia de escenas, `n=2` es insuficiente y los controles no están pareados por fecha, tema o horario.

La clasificación es **No comparable como control causal**. Sí sirven para recordar que la ilustración de personajes no garantiza mayor rendimiento y que el texto relatable puede ser competitivo.

### Composición de mundo

El cartel de hada, Wilfred y tarot obtuvo 14 interacciones y 1 share. Su valor histórico y de construcción de mundo es alto, pero en esta muestra no aparece como formato de alta difusión.

La clasificación es **Señal editorial, no señal de rendimiento**. La densidad visual puede fortalecer identidad, pero este caso no demuestra que incremente shares.

## Señales y decisiones

| Pregunta | Resultado actual | Clasificación | Acción |
|---|---|---|---|
| ¿La microhistoria genera más shares? | 19 shares en un caso | Prometedora, no concluyente | Ampliar con más diálogos y paneles |
| ¿La transformación de Universe conserva difusión? | 42 shares en un caso | Prometedora, no concluyente | Buscar más transformaciones con Universe |
| ¿La escena de personaje explica rendimiento? | Mediana 18/2, alta heterogeneidad | Sin señal agregada | Subdividir por relación y remate |
| ¿El texto simple rinde menos? | No demostrado; controles con 27.5/4.5 | No comparable | Crear controles pareados en futuros análisis |
| ¿La densidad de mundo aumenta shares? | No observado en este caso | Señal editorial | Mantener como recurso de identidad, no como palanca de difusión |

## Implicaciones para Growth OS

El Lote A no autoriza cambiar el calendario activo ni crear una regla de publicación. Sí permite mejorar la taxonomía: `estructura_narrativa` debe distinguir, como mínimo, `texto_simple`, `escena_caption_unico`, `duo_globo_texto`, `dialogo_secuencial`, `transformacion_visual` y `composicion_mundo`.

También muestra que las comparaciones futuras deben controlar por personaje y tipo de humor. Agrupar todas las ilustraciones como “escena” oculta diferencias relevantes entre una microhistoria romántica, un insulto seco de Wilfred y una imagen de Ganso vestido.

## Próximo lote recomendado

El siguiente lote debe completar las celdas con menos observaciones, en este orden: cuatro a seis casos de diálogo o secuencia; cuatro a seis transformaciones o variaciones de Universe; y un pequeño conjunto de escenas relacionales con caption único. Los casos se seleccionarán de los 58 restantes únicamente si aportan una de esas estructuras y conservan métricas Meta utilizables.

## Referencias

[1]: `Operations/Research/2026-08-18_Lote_A_Estructuras_Narrativas.csv` "Muestra codificada del Lote A"
[2]: `Operations/Research/2026-08-18_Lote_A_Resumen_Comparativo.csv` "Resumen de medianas por grupo"
[3]: `Operations/Research/2026-08-18_Filtro_Expansion_58_Casos_GrowthOS.md` "Filtro de expansión de los 58 casos"
[4]: `GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md` "Reglas y señales abiertas de aprendizaje"
