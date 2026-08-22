---
title: "Protocolo de instrumentación y medición de Reels"
purpose: "Resolver la ausencia intermitente de views, reach y retención en Meta mediante una arquitectura de medición por capas, incorporando las fuentes de lectura confirmadas para la celda HB-REEL-MOTION-POV-MEME-01 y futuras publicaciones de video."
status: Active
created: 2026-08-22
updated: 2026-08-22
version: "1.2"
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

La celda `HB-REEL-MOTION-POV-MEME-01` no debe depender de una sola respuesta de Insights de Meta. La auditoría del 22 de agosto confirmó que existen fuentes de lectura habilitadas: el conector `Universe Sent Me Meta API`, el conector integrado `Instagram`, Windsor.ai con `facebook_organic` e `instagram`, y `My Browser`. La estrategia se mantiene como **medición por capas**, pero deja de tratar la falta de views, reach y retención como una limitación general: ahora deben intentarse primero las fuentes autorizadas y registrarse los campos que realmente devuelvan.

El reporte diario continúa siendo la fuente principal de aprendizaje y el nivel mínimo es `L1_Engagement_Observable`. Windsor.ai queda habilitado como fuente de lectura para enriquecer `L2` y `L3`, mientras que Instagram integrado permite recuperar publicaciones e insights nativos de la cuenta `@universe_sent_me_0326`. La existencia de un campo en el catálogo no garantiza que cada publicación lo devuelva; por eso los valores ausentes siguen siendo `null`/`Unavailable`, nunca ceros inventados.

La ausencia de una métrica en una fuente no bloquea la producción ni el reporte diario, pero sí limita la afirmación correspondiente. Un Reel con solo interacciones básicas produce una **señal editorial de engagement**; un Reel con plays/reach validados puede producir una señal de descubrimiento; y solo una fila con consumo de video explícito puede entrar en una comparación de retención.

## 2. Niveles de evidencia

| Nivel | Qué contiene | Qué permite afirmar | Qué no permite afirmar |
|---|---|---|---|
| `L0_Identidad` | Page Post ID, Reel ID, permalink, fecha/hora real, plataforma, export y duración | Que la publicación existe y puede reconciliarse | Que tuvo buen rendimiento |
| `L1_Engagement_Observable` | Reacciones, comentarios, shares y respuestas capturados en el corte diario | Qué piezas generan interacción básica y qué piezas comparten más | Views, alcance, retención o completación |
| `L2_Discovery_Manual_or_Connector` | Views, reach, porcentaje de no seguidores y fuente de captura desde Meta Business Suite o un conector analítico validado | Señal de descubrimiento y distribución | Retención si no se captura explícitamente |
| `L3_Video_Retention` | Retención inicial, tiempo medio visto, porcentaje completado y duración del video | Comparación de consumo de video entre Reels comparables | Causalidad si cambian formato, duración, hook o plataforma |
| `L4_Comparable_Cell` | L2/L3 completos en al menos tres casos comparables, con controles de duración, hook, texto, caption y plataforma | Señal preliminar de la hipótesis | Veredicto operativo con menos de cinco casos |

Los seis Reels históricos confirmados permanecen principalmente en `L1_Engagement_Observable`; ninguno debe entrar automáticamente a una comparación de retención. MPM-001, MPM-002 y MPM-003 deben subir a `L2` o `L3` antes de usar expresiones como “mayor alcance”, “mejor retención” o “mejor descubrimiento”.

## 3. Estado de acceso y cobertura confirmada

La revisión de conectores se realizó en modo lectura. No se publicaron, modificaron ni programaron contenidos.

| Servicio o fuente | Estado confirmado | Cuenta o alcance | Cobertura útil para Reels | Uso operativo |
|---|---|---|---|---|
| `Universe Sent Me Meta API` | Habilitado y editable | Página `1036844829507460` | Identidad, feed de Página y engagement según endpoint; las métricas de video deben validarse por respuesta real | `L0`/`L1` y reconciliación de publicación |
| Instagram integrado | Habilitado | `@universe_sent_me_0326`, 44 seguidores, 470 posts al momento de la consulta | Lista de posts, likes, comentarios e insights nativos; la prueba devolvió `reach=4`, `views=7` para un Reel reciente | `L0`/`L1`/`L2` cuando el insight exista |
| Windsor.ai | Habilitado | `facebook_organic` → Page `1036844829507460`; `instagram` → `17841462696378190` (`universe_sent_me_0326`) | Lectura de campos de Reels/video y métricas orgánicas; se obtuvieron filas reales para ambos canales | Fuente preferida de enriquecimiento `L2`/`L3` |
| My Browser | Habilitado | Sesión del usuario | Captura manual de Business Suite u otras superficies autorizadas, si una métrica no aparece por API | Fallback manual validado |
| Meta Ads Manager | Habilitado | Conector disponible, sin usar para esta auditoría | Datos de anuncios, no sustituto de métricas orgánicas | Solo si una pieza tiene pauta documentada |
| TikTok for Business | Deshabilitado | Sin cuenta operativa confirmada | No forma parte del diagnóstico actual de Facebook/Instagram | No usar sin habilitación y autorización |
| Metricool, Supermetrics y otros conectores analíticos | Deshabilitados | Sin acceso confirmado | No deben tratarse como fuentes disponibles | No usar ni solicitar cambios sin necesidad explícita |

La prueba de Windsor para Facebook orgánico devolvió, entre otras, tres filas de Reels recientes con IDs `2815726225473165`, `2210896633022235` y `2005557463434064`. En esas filas estuvieron disponibles `blue_reels_play_count`, `fb_reels_total_plays`, `fb_reels_replay_count`, `reels_post_impressions_unique`, `post_video_avg_time_watched`, `post_video_complete_views_organic`, `post_video_view_time`, shares, comentarios y reacciones. La respuesta también incluyó una fila técnica con `id=null` y ceros; esa fila no representa una publicación y debe excluirse del análisis.

La prueba de Windsor para Instagram devolvió Reels e imágenes recientes. Para un Reel estuvieron disponibles `media_reach`, `media_reel_avg_watch_time`, `media_reel_total_watch_time`, `media_reel_total_interactions`, likes y comentarios. `media_impressions`, `media_plays`, `media_reel_video_views` y `media_follows` pueden llegar como `null`; el protocolo conserva ese estado y no lo transforma en cero.

La fuente Windsor se considera **conectada y utilizable**, no automáticamente completa. Cada captura debe conservar `data_fetched_at`, cuenta, campo, valor bruto y, cuando aplique, unidad de tiempo. Los campos de tiempo de reproducción se almacenan primero en su valor bruto; cualquier conversión a segundos debe quedar documentada y validarse contra `Duration_Seconds` antes de comparar casos.

## 4. Campos obligatorios por publicación

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
| `Series_ID` | Identificador de serie cuando aplique; para MPM-001: `ELARA-WALK-MUSIC-01`. |
| `Music_Variant_ID` | Identificador de la pista o dirección sonora; obligatorio si el Reel usa la capa musical. |
| `Audio_Source` | Original, licenciada, biblioteca de plataforma, ambiente o `Unavailable`; no inferir. |
| `Music_Reference` | Género, mood o referencia editorial usada para curar el audio; no equivale a una canción confirmada. |
| `Music_Hashtag` | Cero, uno o dos hashtags realmente vinculados con el audio usado; no llenar por costumbre. |
| `Visible_Music_Explanation` | `No` para la serie Elara Walk: el video no identifica artista, grupo o canción. |

## 5. Campos de métricas por corte diario

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

## 6. Estrategia operativa para MPM-001, MPM-002 y MPM-003

Los tres casos mantienen la misma plataforma primaria, duración corta, hook visible, movimiento físico y caption externo controlado. El ajuste no es volver a publicar los históricos: es **mejorar la instrumentación de los nuevos exports**.

### Antes de publicar

Se conserva el export final, su hash, duración y referencia de identidad. Se registra el texto exacto, el tratamiento de caption, la función del caption, el slot, la plataforma y el `Case_ID`. La revisión debe confirmar que el hook es legible sin audio y que el payoff sucede dentro del clip.

### Durante la publicación

Se guarda el Page Post ID, Reel ID, permalink y hora real. Si el endpoint devuelve un post padre y un Reel ID diferente, ambos deben conservarse. El export publicado debe ser el mismo archivo aprobado; si se reexporta o se edita después, recibe nuevo hash y no se trata como la misma unidad.

### En cada reporte diario

Se consulta primero el feed de la Página para actualizar identidad y engagement básico. Después se intenta una lectura de video con el conjunto mínimo de métricas soportadas por la fuente activa. Si la fuente no devuelve views/reach/retención, se conserva el resultado `L1_Engagement_only` y se busca una captura alternativa únicamente para ese Reel, no para todo el histórico.

La captura alternativa preferida es una lectura de Meta Business Suite mediante el navegador del usuario o un conector analítico validado. La captura debe conservar fecha/hora, nombre de la superficie, Reel ID, views, reach y cualquier métrica de retención visible. Si tampoco existe, el corte diario sigue siendo válido como L1 y la limitación se documenta.

## 7. Cómo interpretar la celda si faltan métricas

| Situación | Decisión |
|---|---|
| Los tres casos tienen L2/L3 | Se puede evaluar discovery, consumo y shares por caso; mínimo preliminar `n=3`. |
| Solo dos casos tienen L2/L3 | La celda queda incompleta; no se excluye el tercer caso, pero no se calcula una mediana de retención de `n=3`. |
| Los tres casos tienen solo L1 | Se puede comparar shares, comentarios y engagement básico dentro de Facebook; la hipótesis de movimiento/POV queda `No evaluable` en discovery/retención. |
| Un caso tiene L1 y otro L3 | No se mezclan como si tuvieran la misma evidencia. Se reportan capas separadas. |
| Meta devuelve cero o campo ausente | Se conserva `null`/`Unavailable` y se registra la respuesta raw; no se interpreta como rendimiento nulo. |

La celda no se cancela por falta de un campo. Se cambia el tipo de conclusión: de `Discovery/Retention` a `Engagement_Observable`. Esto permite que el Growth OS siga aprendiendo de shares y comentarios sin fabricar views o retención.

## 8. Ajustes creativos para aumentar la capacidad de diagnóstico

Los siguientes controles deben mantenerse constantes para que, cuando aparezcan métricas de video, la lectura sea interpretable:

| Control | Regla de la celda |
|---|---|
| Hook | Texto antes de 0.8 segundos y acción visible antes de 1.5 segundos. |
| Duración | 7–10 segundos, registrando duración real. |
| Payoff | Remate visual antes del final; no depender del caption. |
| Audio | Debe entenderse sin audio; MPM-001 puede usar música en post como capa emocional, pero el audio no debe ser el único hook ni revelar la canción en texto. |
| Texto | Un template común; el texto exacto se añade en postproducción. |
| Caption | Mismo tratamiento y función; no introducir CTA o afiliación. |
| Plataforma | Facebook primero; crossposts medidos como publicaciones independientes. |
| Reuse | Ningún repost idéntico; los históricos son referencias, no controles nuevos. |

No se deben crear múltiples versiones del mismo caso únicamente para “forzar” una métrica. Si una versión cambia el hook, duración o montaje, recibe otro `Case_ID` y responde otra pregunta.

## 9. Estado actual y próxima acción

El estado histórico de la familia continúa siendo `L1_Engagement_Observable` hasta que cada caso tenga una captura comparable; la existencia de Windsor no convierte automáticamente los seis Reels históricos en una celda `L2`/`L3`. La celda `HB-REEL-MOTION-POV-MEME-01` permanece como `Active_candidate_priority`, pero no como veredicto. MPM-001 ya cuenta con export y carpeta de Drive; MPM-002 y MPM-003 tienen referencias oficiales y permanecen pendientes de generación por cuota.

La próxima acción operativa para cualquier Reel publicado es ejecutar, en este orden, el corte diario de engagement, la lectura de Windsor para el canal correspondiente y la lectura integrada de Instagram cuando exista crosspost o publicación nativa. Para Facebook, el conjunto mínimo recomendado es `Reel_ID`, `created_time`, `reels_post_type`, `reels_permalink_url`, `blue_reels_play_count`, `fb_reels_total_plays`, `fb_reels_replay_count`, `reels_post_impressions_unique`, `post_video_avg_time_watched`, `post_video_complete_views_organic`, `post_video_view_time`, `post_video_social_actions_comment`, `post_video_social_actions_share`, `post_video_total_reactions`, `length` y `data_fetched_at`. Para Instagram, el conjunto mínimo es `media_id`, `timestamp`, `media_type`, `media_product_type`, `media_permalink`, `media_reach`, `media_reel_avg_watch_time`, `media_reel_total_watch_time`, `media_reel_total_interactions`, `media_like_count`, `media_comments_count`, `media_shares`, `media_saved`, `media_follows` y `data_fetched_at`.

MPM-001 debe registrar su identidad nativa cuando Fernando autorice la publicación; además debe conservar `Series_ID=ELARA-WALK-MUSIC-01`, `Music_Variant_ID`, `Audio_Source` y `Music_Hashtag` aunque el hashtag sea `None`. Después se debe capturar primero `L1` y, en el mismo corte diario, intentar `L2`/`L3` por Windsor. MPM-002 y MPM-003 deben seguir exactamente la misma plantilla cuando se generen y publiquen. La captura no autoriza ninguna publicación ni modificación del calendario.

## 10. Coherencia documental

Esta actualización añade campos de audio y serie musical para Reels, pero no modifica el calendario, el CNT, el canon, la taxonomía de personajes ni el ledger de afiliados. `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md` y `GrowthOS/07_00_Registro_Maestro_Reels.md` ya enlazan el protocolo y no requieren cambios estructurales en esta revisión; solo deberán recibir una actualización futura si se incorpora un nuevo campo permanente al esquema de sus ledgers. El changelog se actualiza con la evidencia de acceso y las reglas de prioridad de fuentes.

No se modifica calendario, no se crea CNT y no se publica contenido como parte de este protocolo. La programación o publicación requiere su aprobación humana separada.

## Referencias

- `Operations/Production/2026-08-22_Brief_Celda_Reels_Motion_POV_Meme_001.md` — controles, casos y blueprints de la celda.
- `Operations/Research/2026-08-21_Corte_Diario_Metricas_2200.md` — corte diario y limitaciones actuales de Meta.
- `Operations/Research/2026-08-22_Reels_Confirmed_Metric_Assessment.json` — evaluación de evidencia histórica y prioridad Motion + POV/Meme.
- `Operations/Research/2026-08-21_Analisis_Corte_Diario_Familias_Personajes.md` — separación de Reels, imágenes y afiliados en el análisis diario.
- `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md` — reporte diario como fuente principal de aprendizaje.
- `GrowthOS/00_01_Changelog_GrowthOS.md` — registro de sincronización entre agentes y decisiones operativas.
