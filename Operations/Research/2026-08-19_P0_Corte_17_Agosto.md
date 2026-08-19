---
title: "Corte P0 de las cinco publicaciones del 17 de agosto"
purpose: "Registrar la ejecución del extractor P0 sobre las cinco publicaciones confirmadas en Meta y documentar por qué aún no se escribieron métricas 24/72 horas."
status: "Active"
created: 2026-08-19
updated: 2026-08-19
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-17_P0_Baseline_Ola_Activa.csv"
  - "Operations/Research/2026-08-15_ExperimentLog.csv"
  - "Operations/Production/extract_metrics_24_72.py"
  - "Operations/Production/run_p0_baseline_cut.py"
  - "Operations/Production/extract_metrics_24_72_playbook.md"
organization: "Operations/Research"
---

# Resultado del corte P0

## Ejecución

El proceso se ejecutó el **18 de agosto de 2026 a las 03:26:12 UTC**, equivalente a **17 de agosto de 2026 a las 22:26:12 en America/Matamoros**. Se procesó explícitamente el baseline `EXP-2026-08-CAL-01` con sus cinco publicaciones confirmadas en Meta:

| Slot local | Asset | Meta Post ID | Edad aproximada al corte |
|---|---|---|---:|
| 10:00 | `260633` | `122151373701072582` | 12.4 h |
| 11:00 | `2608028` | `122151373761072582` | 11.4 h |
| 13:30 | `2608034- Elara` | `122151373833072582` | 9.0 h |
| 16:00 | `260642` | `122151373893072582` | 6.4 h |
| 17:00 | `2608027.jpeg` | `122151373953072582` | 5.4 h |

## Resultado técnico

| Campo | Resultado |
|---|---:|
| Filas candidatas | 5 |
| Ventanas 24h elegibles | 0 |
| Ventanas 72h elegibles | 0 |
| Escrituras exactas de métricas | 0 |
| Actualización del baseline | No requerida |
| Actualización del ExperimentLog | No requerida |
| Instagram tocado | No |
| Contenido publicado | No |

La ejecución no escribió métricas porque ninguna publicación había alcanzado todavía 24 horas desde su hora real de publicación. Esto es correcto y protege la comparabilidad del experimento. El corte no debe forzarse con `--now` artificial ni con timestamps planeados.

El extractor existente, si se ejecuta directamente sobre `Publication_Log.csv`, identifica principalmente las filas del lote 15–16 porque las cinco publicaciones del 17 de agosto están formalmente en el baseline P0 y todavía no tienen fecha real en el Publication Log. Para evitar procesar el lote equivocado, se creó el adaptador `run_p0_baseline_cut.py`, que apunta explícitamente al baseline de cinco filas y actualiza el ExperimentLog solo cuando una ventana está realmente vencida.

## Integridad de datos

Las cinco filas del baseline permanecen en `Pendiente_ventana`. `interactions_24h`, `comments_root_24h`, `shares_24h`, `interactions_72h`, `comments_root_72h`, `shares_72h` e `interactions_72h` siguen vacías. El ExperimentLog conserva sus valores vacíos y no recibió totales lifetime como sustitutos.

La evidencia JSON completa se conserva en `2026-08-19_P0_Corte_17_Agosto.json`. El siguiente corte válido será cuando al menos una de las cinco publicaciones haya superado 24 horas; el proceso deberá consultar Meta en modo lectura y, si la API vuelve a entregar únicamente acumulados lifetime, registrar la limitación sin llenar los campos estrictos de 24/72h.


## Cierre provisional del ciclo de aprendizaje — corte observado del 19 de agosto

El alcance oficial de P0 es **el lote de cinco publicaciones del 17 de agosto**, no el lote de nueve publicaciones del 15–16. El lote del 15–16 (`CNT-031`–`CNT-039`) pertenece a la revisión histórica/operativa `HB-003|HB-004|HB-005` y no debe mezclarse con las cinco filas del baseline P0.

A las **03:14 UTC del 19 de agosto de 2026** se ejecutó el extractor general. Como su fuente operativa contiene primero el lote 15–16, produjo evidencia para nueve filas `PUB-FB-15_16-*`; esa salida se conserva como evidencia separada y **no se usa para cerrar P0**. A continuación se consultaron directamente los cinco Meta Post IDs del baseline P0 para obtener un corte observado actual.

| Slot local | Asset | Reacciones acumuladas observadas | Comentarios acumulados | Compartidos | Interacciones observadas |
|---|---|---:|---:|---:|---:|
| 10:00 | `260633` | 47 | 2 | 8 | 57 |
| 11:00 | `2608028` | 462 | 2 | 172 | 636 |
| 13:30 | `2608034- Elara` | 29 | 4 | 4 | 37 |
| 16:00 | `260642` | 2 | 0 | 2 | 4 |
| 17:00 | `2608027.jpeg` | 38 | 2 | 11 | 51 |
| **Total** | **5 publicaciones** | **578** | **10** | **197** | **785** |

Estas cifras son **totales acumulados observados al momento de la consulta**, no snapshots exactos de 24 o 72 horas. Por integridad metodológica no se escriben en los campos estrictos `interactions_24h` o `interactions_72h`.

### Veredicto provisional

El resultado está fuertemente concentrado en `2608028`, que reúne 636 de las 785 interacciones observadas. La señal provisional favorece una combinación de **identificación emocional amplia, composición visual clara y caption mínimo basado en emojis**, pero no permite atribuir causalidad a un solo factor. El segundo nivel —`260633` con 57 y `2608027` con 51— queda muy por debajo; `260642` fue el outlier de bajo rendimiento con 4 interacciones.

La hipótesis de trabajo queda **parcialmente respaldada como señal editorial**, no validada como regla de horario: hay una diferencia grande entre piezas, pero la muestra de cinco publicaciones no permite concluir que las 11:00 sean universalmente mejores ni que las 16:00 sean universalmente débiles.

### Estado del ciclo

El ciclo queda **cerrado provisionalmente con limitación de ventana temporal**. El aprendizaje es utilizable para orientar la siguiente ola, pero las métricas exactas de 24/72 horas siguen pendientes porque Meta entregó acumulados lifetime. No se modificó Instagram ni se publicó contenido durante este corte.


## Análisis del outlier 2608028 y ajustes para la siguiente ola

### Desglose cuantitativo

`2608028` registró **462 reacciones, 2 comentarios y 172 compartidos**, para **636 interacciones observadas**. Eso representa el **81.0%** de las interacciones del lote P0, el **79.9%** de las reacciones y el **87.3%** de los compartidos. Los otros cuatro posts juntos sumaron solo 149 interacciones.

El resultado no proviene de una conversación especialmente larga: sus 2 comentarios representan apenas el 20% de los comentarios del lote. La ventaja está principalmente en **reacciones y compartidos**, lo que sugiere identificación inmediata y voluntad de recomendar o redistribuir el contenido.

### Desglose creativo observable

El asset presenta a Universe como un gato reconocible con sus gafas distintivas, en un escenario fantástico de alto atractivo visual. La composición utiliza tres momentos secuenciales: una afirmación general sobre el amor, un acercamiento expresivo al rostro y un cierre contemplativo del personaje frente al paisaje. El texto es breve, legible y completa una idea en tres pasos: “Lo bueno del amor es que / si eres un buen observador / lo verás en todos lados”.

La pieza combina cinco ventajas que sí son observables: identidad fuerte de personaje, atractivo visual inmediato, progresión narrativa, frase universal y un remate emocional que no depende de conocer el canon. El caption publicado fue mínimo —`🥰🌎😂` más hashtags—, por lo que la imagen cargó casi todo el trabajo comunicativo y no compitió con un copy largo.

### Qué podemos afirmar y qué no

La evidencia respalda que esta combinación funcionó muy bien **en esta pieza y en este corte**. No demuestra que una imagen fantástica siempre superará a un meme simple, que las 11:00 sean siempre el mejor horario o que tres emojis sean la causa directa del resultado. El alto rendimiento puede incluir efectos de tema, calidad visual, familiaridad con Universe, hora, distribución algorítmica y compartibilidad.

### Ajustes recomendados para la siguiente ola

| Ajuste | Aplicación concreta | Medición de control |
|---|---|---|
| Replicar la estructura, no copiar el asset | Producir 2–3 piezas nuevas con personaje reconocible, frase universal, secuencia de 2–3 paneles y remate emocional | Comparar interacciones y compartidos contra la mediana de la ola |
| Mantener captions mínimos como tratamiento | Probar 1–3 emojis + hashtags en un subconjunto, no en toda la ola | Separar por tratamiento `Emoji_Minimo` vs `Frase_Corta` |
| Aumentar la capacidad de compartir | Priorizar frases que funcionen aunque el usuario no conozca el canon | Shares por publicación y proporción de shares sobre interacciones |
| Conservar variedad editorial | Mantener humor ácido, sexual, cotidiano y personajes secundarios como controles | Evitar que toda la ola se vuelva sentimental o fantástica |
| No sobreoptimizar el horario | Repetir la fórmula en al menos dos franjas distintas | Comparar por formato/tema y no solo por hora |
| Reservar capacidad para outliers | Incluir una pequeña cuota de piezas visualmente ambiciosas | Identificar si reaparece un resultado de cola alta en otra pieza |

La decisión operativa recomendada es **promover la fórmula creativa como hipótesis prioritaria**, no convertirla todavía en canon editorial. La siguiente ola debería contener un pequeño tratamiento de replicación: dos o tres piezas que compartan la estructura de 2608028 y un grupo de control que conserve la diversidad actual.
