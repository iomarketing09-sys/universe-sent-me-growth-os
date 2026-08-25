---
title: "Bam in a Can — CAN-002: chequeo inicial y corte post-T+3"
purpose: "Preservar los cortes operativos iniciales de CAN-002, separando métricas autenticadas, cache de plataforma, evidencia directa e indexación pendiente."
status: "Active — TikTok e Instagram actualizados cerca de T+28; YouTube sigue sin fila Windsor"
created: 2026-08-23
updated: 2026-08-24
version: "1.8"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/Bam_In_A_Can_Distribution_Ledger.csv"
  - "Operations/Production/2026-08-21_Bam_In_A_Can_Semana01_Calendario_Publicacion.md"
  - "Operations/Production/2026-08-21_Bam_In_A_Can_Semana01_Paquete_Lanzamiento.md"
  - "Operations/Research/2026-08-21_Bam_CAN001_Snapshot_Temprano.md"
organization: "Operations/Research"
---

# Bam in a Can — CAN-002: chequeo inicial de visibilidad

## Propósito del corte

Este documento registra el primer chequeo de CAN-002 solicitado tras cerrar su cascada. El corte se declaró a las **20:12:20 CDT del 23 de agosto**. No corresponde a T+3 h en ninguna plataforma: TikTok tenía 1 h 12 min 37 s; Instagram Reels 51 min 43 s; y YouTube Shorts 15 min 20 s. Por ello, describe visibilidad e indexación iniciales, no rendimiento temprano comparable.

## Datos observados

| Plataforma | Edad al corte declarado | Fuente / hora de consulta | Métricas disponibles | Interpretación correcta |
|---|---:|---|---|---|
| TikTok | 1 h 12 min 37 s | Windsor.ai, `data_fetched_at` 01:12:41 UTC | 26 views; 0 likes; 0 comentarios; 0 shares; 0 favoritos; duración 9.73 s; avg. watch 3.03 s; total watch 72 s; full-watch rate 8.33 %. | El avg. watch equivale a **31.14 %** de la duración. Es una observación inicial de volumen mínimo, no una lectura de distribución. El caption recuperado por Windsor incluye `Original fiction. AI-made.`. |
| Instagram Reels | 51 min 43 s | Windsor.ai, consulta 01:13:21 UTC; permalink público 01:14:22 UTC | Windsor no devolvió fila. El permalink público confirma caption/disclosure y muestra **0 comentarios**. | La ausencia de fila no equivale a cero views, reach, likes, shares o saves. |
| YouTube Shorts | 15 min 20 s | Windsor.ai, consulta 01:13:53 UTC; Short público 01:14:36 UTC | Windsor no devolvió fila. La vista pública muestra **1 like** y **0 comentarios**; no expone views. | Es evidencia pública de interacción inicial, no un dataset completo. La fila autenticada sigue pendiente de indexación. |

## Lectura operativa

No se valida una hipótesis creativa, de audio o de plataforma en este corte. La pieza tiene menos de 75 minutos en TikTok y menos de una hora en Instagram, mientras que YouTube todavía no indexa sus métricas en Windsor.ai. Las dos versiones con audio nativo compartido y la versión de SFX no tienen edades equivalentes ni datos suficientes para comparar consumo o atribuir un efecto a `she share post (for blog)`.

El siguiente corte útil empieza después de que YouTube cumpla su propia ventana T+3 h, a las **22:57 CDT**. Se deben repetir las consultas autenticadas de las tres redes y conservar por separado las métricas de plataforma, la fuente y la edad real de cada post.

## Reconsulta tras confirmar conectores

Fernando confirmó que actualizó la conexión de Instagram en Windsor.ai. La reconsulta verificó que la cuenta `bam_inacan` permanece listada como cuenta activa de Instagram y que el canal `baminacan@gmail.com` permanece activo en YouTube. Sin embargo, la consulta de Instagram a las **20:38:53 CDT** y la de YouTube a las **20:40:32 CDT** continuaron devolviendo conjuntos vacíos para CAN-002. La conexión está disponible; las filas de contenido siguen pendientes de sincronización/indexación. No se registran métricas de cero por ese motivo.

### Validación con campos mínimos

Para respetar el límite de la cuenta gratuita, se ejecutaron consultas reducidas de cuatro campos por plataforma. Instagram usó `media_shortcode`, `media_views`, `media_reach` y `data_fetched_at` a las **20:46:42 CDT**; YouTube usó `video_title`, `views`, `likes` y `data_fetched_at` a las **20:46:59 CDT**. Ambas devolvieron conjuntos vacíos cuando se aplicó el filtro de fecha de la publicación. Esto no prueba que falten los contenidos: describe el comportamiento de esa forma de consulta.

### Diagnóstico confirmado — Instagram

La cuenta `bam_inacan` y sus capacidades de media/insights están operativas. Una consulta de inventario **sin filtro de fecha**, con solo `media_shortcode`, `media_caption` y `data_fetched_at`, devolvió CAN-001 y CAN-002 a las **20:51:19 CDT**. Una segunda consulta de CAN-002 por shortcode, también sin rango de fechas, devolvió **200 views** y **reach 34** a las **20:51:35 CDT**; un tercer bloque reducido devolvió **0 likes** y **0 comentarios** a las **20:51:47 CDT**.

La causa de los conjuntos vacíos de Instagram no fue el número de fields, ni una falta de permisos, ni la ausencia del Reel: fue el uso del rango de fechas junto con la consulta de media. A partir de ahora, para Reels individuales de Bam se debe consultar por `media_shortcode` **sin** `date_from`/`date_to`, mediante bloques de hasta cuatro fields. YouTube continúa sin fila incluso con campos mínimos y requiere una ruta de diagnóstico separada.

### Actualización de métricas de Instagram

El refresh conjunto de CAN-001 y CAN-002 mantuvo el filtro por shortcode sin rango de fechas. Para CAN-002, el bloque de views/reach conservó `data_fetched_at` **20:51:35 CDT**: **200 views** y **reach 34**. El bloque de interacciones devolvió 0 likes, 0 comentarios y 0 shares. El bloque de consumo devolvió `data_fetched_at` **20:57:54 CDT**, con avg. watch time raw `8536` y total watch time raw `290246`, documentados como **8.536 s** y **290.246 s** tras convertir de milisegundos.

El avg. watch equivale aproximadamente al **85 %** de los 10 segundos de CAN-002, pero no autoriza un veredicto creativo todavía: la pieza tiene menor alcance, el snapshot sigue temprano y no hay control cuantitativo de YouTube. La lectura correcta es que la retención inicial merece seguimiento, no que el audio ni el formato ya estén validados.

### Evidencia directa de YouTube Studio

Fernando aportó una captura de YouTube Studio para `-P8er9X9ggw`. El nombre del archivo indica **21:10:22 CDT**; usado como timestamp de registro, el Short tenía **1 h 13 min 22 s** desde su T0. Studio muestra **58 vistas**, **1 like** y **4 veces compartido**. La interfaz también presenta el mensaje cualitativo de que el Short mantuvo a usuarios viendo con repeticiones indefinidas; no expone en esta captura una cifra de retención, duración media ni porcentaje, por lo que ese mensaje no se convierte en una métrica numérica.

El conteo es una señal inicial de distribución y compartidos a seguir, no una validación de audio, formato ni hipótesis creativa. Tiene una edad muy corta, una muestra pequeña y una definición de métricas no equiparable con TikTok o Instagram. Windsor.ai todavía no devolvía una fila de este Short en la última consulta mínima, de modo que Studio queda registrado como la fuente manual provisional.

![Captura de YouTube Studio de CAN-002 a T+1 h 13 min 22 s](2026-08-23_Bam_CAN002_YouTube_Studio_T1h13m22s.jpg)

## Corte consolidado post-T+3 — 23 de agosto

Fernando autorizó la revisión al superar la ventana T+3 de YouTube. El corte se registró alrededor de **23:01 CDT**. La tabla conserva la edad real y no fuerza equivalencia entre las tres plataformas.

| Plataforma | Fuente y edad aplicable | Métricas disponibles | Lectura correcta |
|---|---:|---|---|
| TikTok | Windsor.ai, `data_fetched_at` 04:01:07 UTC / 23:01:07 CDT; **4 h 01 min 24 s** desde T0 | 117 views; 2 likes; 0 comentarios; 0 shares; 0 favoritos; avg. watch 2.64 s; total watch 329 s; full-watch rate 8 %. | Desde el primer corte sube de 26 a 117 views y de 0 a 2 likes. El avg. watch equivale aproximadamente a 27 % de los 9.73 s de duración conocidos. El incremento de alcance no compensa por sí solo la baja finalización; debe seguirse con más piezas. |
| Instagram Reels | Reconsulta de Windsor por shortcode realizada durante este corte; última cache con `data_fetched_at` 01:51:35/01:57:54 UTC, **1 h 37 min 17 s** desde T0 | 200 views; reach 34; 0 likes; 0 comentarios; 0 shares; avg. watch 8.536 s; total watch 290.246 s. | La reconsulta no refrescó el origen. Estos son los valores previos ya documentados, no un resultado nuevo de T+3. Se mantienen sin inferir crecimiento o estancamiento posterior. |
| YouTube Shorts | Evidencia directa de Studio recibida durante el corte; referencia de registro 23:01:18 CDT, aproximadamente **3 h 04 min 18 s** desde T0 | 90 views; 2 likes; 4 shares; mensaje cualitativo de repeticiones indefinidas. | Frente a la captura anterior (58 views, 1 like y 4 shares), hay +32 views y +1 like; los shares permanecen en 4. Studio no expone aquí una cifra de retención, por lo que el mensaje cualitativo no se traduce a porcentaje. |

La discrepancia de frescura de fuentes es parte del resultado: TikTok sí devolvió una fila nueva; Instagram respondió con cache anterior; YouTube continúa sin fila en Windsor, pero Studio proporciona la evidencia manual más reciente. Por ello, no se construye un ranking cross-platform ni se atribuye la diferencia al audio nativo `she share post (for blog)` o al control de SFX.

![Captura de YouTube Studio de CAN-002 alrededor de T+3 h](2026-08-23_Bam_CAN002_YouTube_Studio_T3h04m18s.jpg)

## Actualización de YouTube Studio — 24 de agosto

Fernando aportó una nueva captura de Studio, recibida a las **22:21:14 CDT**. La interfaz identifica el Short como publicado hace **1 día**, sin exponer una hora exacta de captura. Registra **255 vistas**, **3 likes** y **4 shares**; también lo presenta como el Short con más vistas de la cuenta en ese momento y muestra a **México con 75 %** dentro de las ubicaciones principales de audiencia.

Frente al corte de Studio cercano a T+3 (90 vistas, 2 likes y 4 shares), esto equivale a +165 vistas y +1 like; los shares permanecen en 4. La señal es positiva para la distribución inicial de CAN-002, pero no demuestra la causa: el reconocimiento de “más vistas” es relativo al catálogo actual de la cuenta, la muestra sigue siendo de una sola pieza y las demás plataformas no comparten la misma edad, métricas ni frescura de datos. Windsor continúa sin fila autenticada de YouTube.

![Captura de YouTube Studio de CAN-002 con edad relativa de un día](2026-08-24_Bam_CAN002_YouTube_Studio_relative_1d.jpg)

## Reconsulta TikTok e Instagram — 24 de agosto

Para sostener la siguiente prueba editorial, se reconsultaron ambas plataformas con la ruta correcta y bloques de hasta cuatro fields. TikTok devolvió `data_fetched_at` **2026-08-25T03:57:55Z / 22:57:55 CDT**; el post tenía **27 h 58 min 12 s**. Instagram devolvió `data_fetched_at` **2026-08-25T03:58:33Z / 22:58:33 CDT**; el Reel tenía **27 h 37 min 56 s**.

| Plataforma | Métricas frescas | Lectura interna |
|---|---|---|
| TikTok | 155 views; 2 likes; 0 shares; 0 favoritos; avg. watch 2.51 s; total watch 452 s; duración 9.73 s; full-watch rate 7.22 %. | El avg. watch equivale a 25.79 % de la duración. Frente a T+4 h, las views crecieron 32.47 %, pero el consumo por vista cayó de 2.64 s a 2.51 s y no aparecieron señales de distribución. Los comentarios no se reconsultaron en este bloque; su último valor confirmado era 0. |
| Instagram Reels | 324 views; reach 248; 0 likes; 0 comentarios; 0 shares; 0 saves; avg. watch 5.454 s; total watch 1,390.849 s. | Views y reach crecieron frente al corte previo, pero no hubo interacción activa. El avg. watch equivale a 54.54 % de 10 s y bajó 3.082 s frente al corte temprano; se interpreta como cambio de composición del alcance, no como prueba de una causa creativa. |

La reconsulta habilita ajustes de prueba de hook en TikTok y packaging de caption en Instagram, documentados en el Plan de lanzamiento de audiencia de Bam. No habilita un cambio de horario, audio ni volumen: solo hay una pieza reciente y las plataformas no son comparables entre sí.

## Límites y actualizaciones relacionadas

El ledger conserva el chequeo inicial como `pre-T3`, el corte post-T+3 y la reconsulta post-T+24 dentro de los snapshots por plataforma. Este documento actualiza la interpretación de lanzamiento de CAN-002; los documentos relacionados que requieren el mismo ajuste son el ledger de distribución y el Plan de lanzamiento de audiencia de Bam, modificados en este cambio. El paquete y el calendario de Semana 01 no requieren modificación porque no cambian el copy, los assets, el audio ni las ventanas planificadas.
