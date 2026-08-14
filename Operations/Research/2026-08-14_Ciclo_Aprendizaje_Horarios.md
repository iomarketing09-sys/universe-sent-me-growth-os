# Ciclo de Aprendizaje de Horarios — 4–14 de Agosto de 2026

**Propósito:** Reconstruir y documentar el ciclo de aprendizaje que motivó la ampliación y redistribución de horarios en el calendario del 10–16 de agosto, conectando la evidencia histórica, la decisión editorial, los primeros resultados y las condiciones necesarias para cerrar la hipótesis.

**Estado:** Review  
**Fecha de creación:** 2026-08-14  
**Última actualización:** 2026-08-14  
**Versión:** 1.0  
**Autor:** Manus AI  
**Documentos relacionados:** [`GrowthOS/05_03_Calendario_10_16_Agosto.md`](../../GrowthOS/05_03_Calendario_10_16_Agosto.md), [`GrowthOS/08_00_Metricas_Baseline_Plataformas.md`](../../GrowthOS/08_00_Metricas_Baseline_Plataformas.md), [`Operations/Research/2026-08-08_Reporte_Mensual_Junio_Julio_2026.md`](2026-08-08_Reporte_Mensual_Junio_Julio_2026.md), [`Operations/Research/2026-08-08_Ciclo_Diario_Metricas_24h.md`](2026-08-08_Ciclo_Diario_Metricas_24h.md), [`GrowthOS/Integracion_Growth_OS.md`](../../GrowthOS/Integracion_Growth_OS.md), [`Operations/Research/2026-08-14_Ciclo_Aprendizaje_Horarios_Datos.csv`](2026-08-14_Ciclo_Aprendizaje_Horarios_Datos.csv)

---

## 1. Dictamen actual

El ciclo **todavía no está cerrado**, pero ahora sí queda reconstruido y documentado. La modificación del horario fue una intervención válida como prueba exploratoria: el calendario pasó a cubrir más franjas del día y redujo el peso del contenido reutilizado para dar espacio a piezas nuevas. Sin embargo, la intervención no fue registrada en el momento con una hipótesis, un grupo de control, un identificador de experimento ni un criterio de decisión.

Los datos disponibles ofrecen una **señal preliminar, no una conclusión causal**. En las publicaciones de Facebook recuperadas para el periodo local del 4 al 14 de agosto, las 33 publicaciones del periodo previo al cambio tuvieron una mediana de 26 interacciones por publicación, mientras que las 17 publicaciones del 10 al 14 de agosto tuvieron una mediana de 37. Esto representa una señal positiva de nivel típico, pero no demuestra que el horario haya causado la mejora porque también cambiaron los personajes, copys, formatos, días incluidos y la proporción de contenido nuevo.

> **Estado de la hipótesis HB-003:** En prueba. No validada ni invalidada.

## 2. Qué cambio se reconstruye

La versión actual del calendario del 10–16 de agosto declara explícitamente una estructura base de **10:00, 15:00 y 18:00, más un Reel diario variable**, pero la tabla real utiliza además slots de 13:00, 16:00, 17:00, 22:00 y espacios de Reel determinados de forma ad hoc. La intención reconstruida es ampliar la cobertura horaria, comparar ventanas de mañana, tarde y noche, y dejar de concentrar toda la programación en las pocas franjas que se habían usado antes.

La segunda parte de la intervención fue editorial: se redujo el reuse a un máximo de una pieza por día y se incorporaron 14 piezas nuevas de personajes del elenco extendido. Por tanto, el experimento de horarios no fue un cambio aislado; fue una intervención combinada de **hora + día + contenido nuevo/reutilizado + personaje + copy**.

| Elemento | Situación reconstruida | Efecto sobre la lectura |
|---|---|---|
| Ventana temporal | Periodo previo: 4–9 de agosto; periodo posterior: 10–14 de agosto disponible hasta la extracción | Permite una comparación inicial, todavía corta |
| Horarios | Mayor cobertura de mañana, tarde y noche | Variable principal de HB-003 |
| Contenido | Menos reuse y más piezas nuevas | Confusor fuerte |
| Personajes | Maeve, Kael, Silvio, Evan, Kiri, Elara, Universe y combinaciones | Confusor fuerte |
| Copy | Varios memes minimalistas, preguntas y frases narrativas | Confusor fuerte |
| Métrica principal | Reacciones + comentarios + shares | Métrica consistente con los ciclos recientes, pero no alcance |
| Criterio original | No quedó documentado en el momento | Debe formalizarse ahora |

## 3. Evidencia histórica que motivó el cambio

La evidencia previa mostraba que Facebook era el canal principal y que las imágenes estáticas con copy minimalista superaban a los Reels en distribución. El análisis de junio y julio también mostró que el rendimiento se concentraba en ciertos días y franjas, pero con una diferencia metodológica importante: algunos reportes usaban engagement rate normalizado y otros usaban volumen absoluto de interacciones. Por eso el calendario eligió trabajar con medianas de interacciones y no con promedios, intentando evitar que unos pocos posts virales dominaran la decisión.

El baseline histórico registró como mejores horas por mediana las franjas de 15:00, 18:00, 20:00 y, con menor evidencia, 10:00. También registró una discrepancia entre sábado como mejor día por mediana de volumen y domingo como mejor día por engagement rate. Esa discrepancia no fue resuelta antes de la intervención, por lo que el cambio de horario se diseñó como exploración, no como optimización definitiva.

## 4. Resultado preliminar de la comparación

Los datos actuales fueron extraídos de la Página de Facebook mediante Graph API el 14 de agosto de 2026. Se conservaron 100 filas recientes y se analizaron 50 publicaciones con fecha local entre el 4 y el 14 de agosto, usando la zona horaria `America/Mexico_City`. El snapshot reproducible está en [`2026-08-14_Ciclo_Aprendizaje_Horarios_Datos.csv`](2026-08-14_Ciclo_Aprendizaje_Horarios_Datos.csv).

| Periodo | Publicaciones | Mediana de interacciones | Promedio | Total |
|---|---:|---:|---:|---:|
| 4–9 agosto, previo al cambio | 33 | 26 | 178.70 | 5,897 |
| 10–14 agosto, posterior al cambio | 17 | 37 | 148.59 | 2,526 |

El promedio posterior cae aunque la mediana mejora porque el periodo previo contiene un outlier excepcional del 4 de agosto con 4,103 interacciones. Esta diferencia demuestra por qué la mediana es más adecuada para describir el comportamiento típico, pero también muestra que no se debe elegir una métrica sin fijar por adelantado qué pregunta responde cada una.

| Franja local aproximada | Periodo previo: n / mediana | Periodo posterior: n / mediana | Lectura provisional |
|---|---:|---:|---|
| 00:00–11:59 | 9 / 23 | 6 / 43 | Señal positiva, muestra pequeña y mezcla de contenidos |
| 12:00–14:59 | 2 / 61.5 | 5 / 33 | No confirma una mejora |
| 15:00–17:59 | 8 / 33 | 5 / 37 | Señal levemente positiva, insuficiente |
| 18:00–20:59 | 13 / 24 | 0 / — | No hay comparación posterior equivalente |
| 21:00–23:59 | 1 / 64 | 1 / 669 | No interpretable por n=1 en cada periodo |

Los mejores resultados individuales del periodo posterior fueron una publicación del martes 11 a las 21:00 con 669 interacciones y una publicación del miércoles 12 a las 09:30 con 489. Ambos casos son útiles para formular la siguiente prueba, pero no bastan para afirmar que 21:00 o 09:30 sean horarios ganadores. El contenido, el personaje y el copy también fueron diferentes.

## 5. Hipótesis formalizada

**HB-003 — Horario ampliado:** La distribución de horarios en ventanas de mañana, tarde y noche mejora la interacción típica frente a una programación concentrada en pocas franjas, controlando por tipo de contenido, personaje y día de publicación.

La variable independiente es la franja horaria local. La métrica primaria será la **mediana de interacciones por publicación** a las 24 horas y, como confirmación, a las 72 horas. Las métricas secundarias serán shares por publicación y `shares / interacciones`. Alcance e impresiones no se usarán como requisito único mientras Graph API no los entregue de forma consistente para esta página.

La hipótesis no puede cerrarse con el resultado actual porque no existió asignación aleatoria ni control de contenido. La lectura correcta es: **el periodo posterior contiene señales prometedoras en mañana y tarde, pero la evidencia está mezclada con una intervención editorial más amplia**.

## 6. Cómo cerrar el ciclo correctamente

El siguiente ciclo debe probar horarios con una matriz controlada, sin volver a cambiar simultáneamente reuse, personajes y estilo de copy. Se recomienda seleccionar un formato homogéneo —imagen estática/meme de Facebook— y repartir piezas comparables entre tres franjas: 09:30–10:00, 15:00–17:00 y 20:00–21:00. Cada franja debe recibir al menos seis publicaciones comparables, idealmente en días equivalentes durante dos semanas.

La decisión debe registrarse antes de publicar. Cada pieza necesita un `Experiment_ID`, una `Hypothesis_ID`, la franja asignada, el día, el personaje, el tipo de copy, si es reuse o nueva, y la fecha/hora exacta de extracción a 24 y 72 horas. El criterio provisional de cierre será una diferencia de al menos **25% en la mediana** frente a la franja de referencia, con al menos seis observaciones por grupo y sin que un único post explique la diferencia. Si ninguna franja supera ese umbral, la hipótesis se mantiene abierta y se vuelve a probar con otra variable controlada.

| Campo que debe registrarse | Ejemplo |
|---|---|
| `Experiment_ID` | `EXP-2026-08-HORARIO-01` |
| `Hypothesis_ID` | `HB-003` |
| `Slot_Local` | `09:30`, `15:00`, `20:00` |
| `Plataforma` | `Facebook` |
| `Formato` | `Imagen estática` |
| `Tipo_Contenido` | `Nueva` o `Reuse` |
| `Personaje` | `Universe`, `Wilfred`, etc. |
| `Métrica_24h` | Reacciones, comentarios, shares, interacciones |
| `Métrica_72h` | Reacciones, comentarios, shares, interacciones |
| `Decisión` | Mantener, descartar o repetir |

## 7. Dependencias y documentos que requieren sincronización

Este documento actualiza la interpretación de HB-003 y debe mantenerse coherente con `Integracion_Growth_OS.md`, donde la hipótesis queda registrada en el `HypothesisBank`. El calendario `05_03_Calendario_10_16_Agosto.md` no se modifica todavía; solo queda vinculado como evidencia de la intervención. Antes de cambiarlo, deberán revisarse la discrepancia entre versión y fecha, la tabla de slots y la separación entre programación editorial y prueba experimental.

El `ExperimentLog` aún debe recibir una fila por publicación cuando existan las mediciones de 24 y 72 horas. El baseline de métricas también debería incorporar este snapshot o, como mínimo, enlazarlo como una extracción posterior comparable por metodología.

## 8. Estado del ciclo

| Etapa | Estado | Evidencia |
|---|---|---|
| Observación del patrón histórico | Completa | Baseline y reporte mensual |
| Decisión de ampliar horarios | Reconstruida | Calendario 10–16 agosto |
| Hipótesis formal | Completa | HB-003 |
| Ejecución de la intervención | Parcialmente observada | 50 publicaciones del 4–14 agosto |
| Medición a 24/72 horas por pieza | Incompleta | No existe registro sistemático |
| Control de variables | No realizado | Cambio simultáneo de horario y contenido |
| Veredicto | Abierto | Requiere experimento controlado |

### Referencias

[1]: ../../GrowthOS/08_00_Metricas_Baseline_Plataformas.md — Baseline de métricas de plataformas.
[2]: 2026-08-08_Reporte_Mensual_Junio_Julio_2026.md — Reporte mensual de junio y julio.
[3]: 2026-08-08_Ciclo_Diario_Metricas_24h.md — Ciclo diario de métricas y aprendizaje.
[4]: ../../GrowthOS/05_03_Calendario_10_16_Agosto.md — Calendario que contiene la intervención de horarios.
[5]: ../../GrowthOS/Integracion_Growth_OS.md — HypothesisBank y ExperimentLog del Growth OS.
[6]: 2026-08-14_Ciclo_Aprendizaje_Horarios_Datos.csv — Snapshot de 100 publicaciones utilizado en este análisis.
