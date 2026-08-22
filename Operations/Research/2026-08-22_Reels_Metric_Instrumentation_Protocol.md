---
title: "Protocolo de instrumentación y medición de Reels"
purpose: "Resolver la ausencia intermitente de views, reach y retención en Meta mediante una arquitectura de medición por capas para la celda HB-REEL-MOTION-POV-MEME-01 y futuras publicaciones de video."
status: Active
created: 2026-08-22
updated: 2026-08-22
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Production/2026-08-22_Brief_Celda_Reels_Motion_POV_Meme_001.md"
  - "Operations/Research/2026-08-21_Corte_Diario_Metricas_2200.md"
  - "Operations/Research/2026-08-21_Analisis_Corte_Diario_Familias_Personajes.md"
  - "Operations/Research/2026-08-22_Reels_Confirmed_Metric_Assessment.json"
  - "GrowthOS/07_00_Registro_Maestro_Reels.md"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
organization: "Operations/Research"
---

# Protocolo de instrumentación y medición de Reels

## 1. Decisión estratégica

La celda `HB-REEL-MOTION-POV-MEME-01` no debe depender de una sola respuesta de Insights de Meta. El corte diario actual devuelve interacciones básicas para los Reels, pero no devuelve de manera utilizable `views`, `reach`, retención, tiempo medio visto ni completaciones. Por esa razón, la estrategia se ajusta a una **medición por capas**: se continúa aprendiendo diariamente, pero cada resultado se etiqueta según el nivel real de evidencia.

La ausencia de views o retención no bloquea la producción ni el reporte diario, pero sí impide afirmar que una pieza tuvo mejor descubrimiento o retención. En ese escenario, el Reel puede producir una **señal editorial de engagement**, no un veredicto de adquisición o retención.

## 2. Niveles de evidencia

| Nivel | Qué contiene | Qué permite afirmar | Qué no permite afirmar |
|---|---|---|---|
| `L0_Identidad` | Page Post ID, Reel ID, permalink, fecha/hora real, plataforma, export y duración | Que la publicación existe y puede reconciliarse | Que tuvo buen rendimiento |
| `L1_Engagement_Observable` | Reacciones, comentarios, shares y respuestas capturados en el corte diario | Qué piezas generan interacción básica y qué piezas comparten más | Views, alcance, retención o completación |
| `L2_Discovery_Manual_or_Connector` | Views, reach, porcentaje de no seguidores y fuente de captura desde Meta Business Suite o un conector analítico validado | Señal de descubrimiento y distribución | Retención si no se captura explícitamente |
| `L3_Video_Retention` | Retención inicial, tiempo medio visto, porcentaje completado y duración del video | Comparación de consumo de video entre Reels comparables | Causalidad si cambian formato, duración, hook o plataforma |
| `L4_Comparable_Cell` | L2/L3 completos en al menos tres casos comparables, con controles de duración, hook, texto, caption y plataforma | Señal preliminar de la hipótesis | Veredicto operativo con menos de cinco casos |

Los seis Reels históricos confirmados permanecen principalmente en `L1_Engagement_Observable`; ninguno debe entrar automáticamente a una comparación de retención. MPM-001, MPM-002 y MPM-003 deben subir a `L2` o `L3` antes de usar expresiones como “mayor alcance”, “mejor retención” o “mejor descubrimiento”.

## 3. Campos obligatorios por publicación

Cada Reel debe tener una fila de identidad y producción, aunque algunas métricas queden vacías:

| Campo | Regla |
|---|---|
| `Case_ID` | `MPM-001`, `MPM-002` o `MPM-003`. |
| `Experiment_ID` | `EXP-202608-REEL-MOTION-POV-MEME-001`. |
| `Hypothesis_ID` | `HB-REEL-MOTION-POV-MEME-01`. |
| `Platform_Content_ID` | ID nativo de la plataforma; no usar solo el nombre del archivo. |
| `Page_Post_ID` | ID del post padre cuando Meta lo entregue. |
| `Reel_ID` | ID nativo del Reel cuando Meta lo entregue. |
| `Permalink` | URL pública verificada. |
| `Published_At_Local` | Hora real de publicación en `America/Matamoros`. |
| `Export_SHA256` | Hash del export publicado para evitar confundir renders o reuploads. |
| `Duration_Seconds` | Duración real del export, no la duración objetivo. |
| `Hook_0_3s` | Sí/No: el hook aparece y se entiende en los primeros tres segundos. |
| `Motion_Legibility` | Alta/Media/Baja: la acción física se entiende sin audio. |
| `Caption_Treatment` | `caption_minimo`, `caption_refuerzo` o `caption_conversacional`. |
| `Caption_Function` | Función del caption, separada del tratamiento. |
| `CTA` | `None` para esta celda; no añadir afiliados. |
| `Reuse_Status` | Nuevo o adaptación con edad documentada; nunca repost idéntico. |

## 4. Campos de métricas por corte diario

El reporte diario es la entrada operativa principal. Para cada Reel publicado se captura, si la fuente lo entrega:

| Campo | Estado recomendado |
|---|---|
| `Metric_Capture_At_Local` | Siempre obligatorio. |
| `Metric_Source` | `Meta_Graph_Feed`, `Meta_Business_Suite_Manual`, `Windsor_or_Connector`, `Other_Validated`. |
| `Metric_Window_Type` | `Corte_Observado`, `lifetime_actual`, `snapshot_24h`, `snapshot_72h`. |
| `Views` | Número o `null`; nunca estimar. |
| `Reach` | Número o `null`; nunca estimar. |
| `Non_Follower_Share` | Porcentaje o `null`; nunca inferir desde shares. |
| `Retention_3s` | Porcentaje o `null`; no sustituir por views. |
| `Average_Watch_Time_Seconds` | Número o `null`. |
| `Completion_Rate` | Porcentaje o `null`. |
| `Reactions` | Número observable. |
| `Comments` | Número observable. |
| `Replies` | Número observable si la fuente lo permite. |
| `Shares` | Número observable. |
| `Followers_Gained` | Número o `null`. |
| `Video_Metrics_Status` | `Complete_L3`, `Discovery_L2`, `Engagement_L1_only`, `Unavailable`. |

Si Meta devuelve solo reacciones, comentarios y shares, el registro debe decir `Engagement_L1_only`. No se permite escribir `0 views`, `0 reach` o `0% retention` cuando la respuesta simplemente no incluyó el campo.

## 5. Estrategia operativa para MPM-001, MPM-002 y MPM-003

Los tres casos mantienen la misma plataforma primaria, duración corta, hook visible, movimiento físico y caption externo controlado. El ajuste no es volver a publicar los históricos: es **mejorar la instrumentación de los nuevos exports**.

### Antes de publicar

Se conserva el export final, su hash, duración y referencia de identidad. Se registra el texto exacto, el tratamiento de caption, la función del caption, el slot, la plataforma y el `Case_ID`. La revisión debe confirmar que el hook es legible sin audio y que el payoff sucede dentro del clip.

### Durante la publicación

Se guarda el Page Post ID, Reel ID, permalink y hora real. Si el endpoint devuelve un post padre y un Reel ID diferente, ambos deben conservarse. El export publicado debe ser el mismo archivo aprobado; si se reexporta o se edita después, recibe nuevo hash y no se trata como la misma unidad.

### En cada reporte diario

Se consulta primero el feed de la Página para actualizar identidad y engagement básico. Después se intenta una lectura de video con el conjunto mínimo de métricas soportadas por la fuente activa. Si la fuente no devuelve views/reach/retención, se conserva el resultado `L1_Engagement_only` y se busca una captura alternativa únicamente para ese Reel, no para todo el histórico.

La captura alternativa preferida es una lectura de Meta Business Suite mediante el navegador del usuario o un conector analítico validado. La captura debe conservar fecha/hora, nombre de la superficie, Reel ID, views, reach y cualquier métrica de retención visible. Si tampoco existe, el corte diario sigue siendo válido como L1 y la limitación se documenta.

## 6. Cómo interpretar la celda si faltan métricas

| Situación | Decisión |
|---|---|
| Los tres casos tienen L2/L3 | Se puede evaluar discovery, consumo y shares por caso; mínimo preliminar `n=3`. |
| Solo dos casos tienen L2/L3 | La celda queda incompleta; no se excluye el tercer caso, pero no se calcula una mediana de retención de `n=3`. |
| Los tres casos tienen solo L1 | Se puede comparar shares, comentarios y engagement básico dentro de Facebook; la hipótesis de movimiento/POV queda `No evaluable` en discovery/retención. |
| Un caso tiene L1 y otro L3 | No se mezclan como si tuvieran la misma evidencia. Se reportan capas separadas. |
| Meta devuelve cero o campo ausente | Se conserva `null`/`Unavailable` y se registra la respuesta raw; no se interpreta como rendimiento nulo. |

La celda no se cancela por falta de un campo. Se cambia el tipo de conclusión: de `Discovery/Retention` a `Engagement_Observable`. Esto permite que el Growth OS siga aprendiendo de shares y comentarios sin fabricar views o retención.

## 7. Ajustes creativos para aumentar la capacidad de diagnóstico

Los siguientes controles deben mantenerse constantes para que, cuando aparezcan métricas de video, la lectura sea interpretable:

| Control | Regla de la celda |
|---|---|
| Hook | Texto antes de 0.8 segundos y acción visible antes de 1.5 segundos. |
| Duración | 7–10 segundos, registrando duración real. |
| Payoff | Remate visual antes del final; no depender del caption. |
| Audio | No necesario para comprender; evitar que el audio sea el único hook. |
| Texto | Un template común; el texto exacto se añade en postproducción. |
| Caption | Mismo tratamiento y función; no introducir CTA o afiliación. |
| Plataforma | Facebook primero; crossposts medidos como publicaciones independientes. |
| Reuse | Ningún repost idéntico; los históricos son referencias, no controles nuevos. |

No se deben crear múltiples versiones del mismo caso únicamente para “forzar” una métrica. Si una versión cambia el hook, duración o montaje, recibe otro `Case_ID` y responde otra pregunta.

## 8. Estado actual y próxima acción

El estado de la familia es `L1_Engagement_Observable` para los Reels del corte diario. La celda `HB-REEL-MOTION-POV-MEME-01` permanece como `Active_candidate_priority`, pero no como veredicto. MPM-001 ya cuenta con export y carpeta de Drive; MPM-002 y MPM-003 tienen referencias oficiales y permanecen pendientes de generación por cuota.

La próxima acción operativa es registrar MPM-001 con su identidad nativa cuando se publique y añadir una fila de métricas `L1` en el reporte diario. En paralelo, se debe intentar una captura `L2` desde una fuente de video autorizada y documentar si Meta devuelve o no las métricas. MPM-002 y MPM-003 deben seguir exactamente la misma plantilla cuando se generen.

No se modifica calendario, no se crea CNT y no se publica contenido como parte de este protocolo. La programación o publicación requiere su aprobación humana separada.

## Referencias

- `Operations/Production/2026-08-22_Brief_Celda_Reels_Motion_POV_Meme_001.md` — controles, casos y blueprints de la celda.
- `Operations/Research/2026-08-21_Corte_Diario_Metricas_2200.md` — corte diario y limitaciones actuales de Meta.
- `Operations/Research/2026-08-22_Reels_Confirmed_Metric_Assessment.json` — evaluación de evidencia histórica y prioridad Motion + POV/Meme.
- `Operations/Research/2026-08-21_Analisis_Corte_Diario_Familias_Personajes.md` — separación de Reels, imágenes y afiliados en el análisis diario.
- `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md` — reporte diario como fuente principal de aprendizaje.
