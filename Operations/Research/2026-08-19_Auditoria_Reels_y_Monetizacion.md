---
title: "Auditoría de Reels y monetización"
purpose: "Separar el rendimiento histórico de Reels del experimento P0 de imágenes, verificar qué vías de monetización tienen evidencia real y establecer la cobertura documental del video corto en Instagram, Facebook, TikTok y YouTube."
status: "Active"
created: 2026-08-19
updated: 2026-08-20
version: "1.5"
author: "Manus AI (CGO)"
related_documents:
  - "GrowthOS/07_00_Registro_Maestro_Reels.md"
  - "GrowthOS/11_00_Estrategia_Monetizacion_MercadoLibre.md"
  - "Operations/Memories/deep_dive_reels_comparativo.md"
  - "Operations/Research/2026-08-19_Meta_Reels_Audit.json"
  - "Operations/Research/2026-08-19_Meta_Reel_Insights.json"
  - "Operations/Research/2026-08-19_Auditoria_Integral_Growth_OS.md"
  - "Operations/Research/2026-08-17_Protocolo_P0_Metricas_y_Veredictos.md"
  - "Operations/Research/2026-08-19_Windsor_Instagram_28D_Normalizado.json"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
  - "Operations/Research/Affiliate_Metrics_Snapshots.csv"
  - "Operations/Research/2026-08-20_Meta_Reel_2210896633022235_Metrics.json"
  - "Operations/Research/2026-08-20_MercadoLibre_Snapshot_7d_Etiquetas.png"
  - "Operations/Research/2026-08-20_MercadoLibre_Snapshot_Fecha.png"
organization: "Operations/Research"
---

# Auditoría de Reels y monetización

## Alcance y separación de métricas

Este informe no mezcla Reels con el experimento P0 de imágenes del 17 de agosto. Las métricas de este documento son acumulados actuales devueltos por objetos de publicaciones de video en Meta y sirven para comparar el carril histórico de Reels. No son ventanas 24/72 horas ni deben entrar en la mediana principal del P0.

La auditoría recuperó 12 publicaciones de video/Reel de la página `Universe Sent Me` mediante Meta Graph API v26.0. La API devolvió reacciones, comentarios y shares actuales; no devolvió vistas, watch time, retención o completaciones mediante la consulta de Insights intentada: las 12 consultas respondieron HTTP 400 por métrica de Insights inválida. Por eso las cifras de interacción son útiles para una primera lectura, pero no constituyen un análisis completo de distribución o retención.

## Cobertura multicanal dentro del Growth OS

La documentación existente cubre de forma operativa el rendimiento de **Instagram y Facebook** mediante Meta Graph API, Windsor, el conector de Instagram, registros manuales, auditorías de Reels, históricos de publicaciones, cruces de assets y el protocolo P0. La cobertura de Instagram mejoró: Windsor ya devuelve vistas, reach, engagement, guardados, shares y watch time de Reels. La deuda restante es consolidar un ledger uniforme y completar las métricas de distribución y retención de Facebook Reels y los snapshots 24/72 horas.

TikTok ya está conectado en Windsor y el primer corte del 22 de julio–18 de agosto devolvió siete videos deduplicables con views, reach, engagement, favoritos, watch time, finalización y seguidores ganados. Todavía no existe un ledger append-only específico; el dataset normalizado del corte es evidencia inicial y no debe mezclarse con Meta como una audiencia agregada.

YouTube ya está conectado en Windsor y el primer corte devolvió seis videos únicos con actividad diaria, views, likes, retención y suscriptores. Todavía no existe un ledger append-only específico; YouTube debe conservar separadas las filas diarias y los snapshots lifetime, y diferenciar videos largos de Shorts antes de comparar formatos.

| Canal | Estado documental | Evidencia existente | Decisión operativa |
|---|---|---|---|
| Instagram | Parcialmente integrado | Registros, auditorías y cruces con Meta | Mantener separado por plataforma y añadir métricas de video |
| Facebook | Parcialmente integrado | Históricos, Meta Graph API, Insights y Reels | Mantener cortes comparables y no mezclar lifetime con 24/72 horas |
| TikTok | Instrumentación inicial | Windsor devolvió siete videos deduplicables y métricas de video | Crear ledger append-only y mantener métricas nativas separadas |
| YouTube / Shorts | Instrumentación inicial | Windsor devolvió seis videos únicos y 24 filas diarias | Crear ledger append-only; separar actividad diaria, lifetime y tipo de video |

La estructura correcta para el siguiente ciclo es un ledger de video corto con una fila por publicación y una columna explícita para `plataforma`. El primer dataset multicanal reproducible está en `Operations/Research/2026-08-19_Social_Performance_28D_Normalizado.json`; debe convertirse progresivamente en un ledger append-only, no sobrescribirse como una tabla de sesión. Los datos de Instagram y Facebook pueden compartir taxonomía, pero sus métricas deben permanecer separadas; TikTok y YouTube deben incorporarse como nuevos estratos cuando existan datos verificables.

## Rendimiento observado de Reels

| Periodo | Reels | Mediana de interacciones | Media de interacciones | Interacciones totales |
|---|---:|---:|---:|---:|
| Julio 2026 | 4 | 25.5 | 21.5 | 86 |
| Agosto 2026, muestra recuperada | 8 | 17.0 | 15.62 | 125 |
| Total | 12 | 19.5 | 17.58 | 211 |

La muestra reciente confirma una señal de deterioro de interacción entre julio y agosto, pero no permite atribuirla únicamente al formato. Agosto contiene publicaciones con objetivos y contextos distintos, y faltan vistas y retención. La comparación correcta para la siguiente iteración debe separar al menos: duración, personaje principal, hook de los primeros segundos, presencia de producto, CTA, reutilización de un meme y publicación cruzada.

Los tres Reels con más interacciones actuales fueron:

| Concepto | Interacciones | Reacciones | Comentarios | Shares |
|---|---:|---:|---:|---:|
| Rock gótico vs. Juan Gabriel | 28 | 25 | 3 | 0 |
| Wilfred reseña su propio peluche | 26 | 21 | 4 | 1 |
| Mi gato sabe hacer de todo | 25 | 21 | 2 | 2 |

La evidencia histórica capturada el 1 de agosto reporta una señal más fuerte para `Fantasma paseando gatos`: 6,640 vistas de Facebook, 260 interacciones, 32 shares y 93.8% de audiencia no seguidora. Esa captura sigue siendo valiosa como evidencia histórica, pero no es directamente comparable con los 12 objetos actuales porque procede de una captura de Insights y no de la misma extracción API.

## Lectura estratégica de Reels

La hipótesis mejor sustentada hasta ahora es que los Reels con **hook visual inmediato, situación absurda reconocible y personajes claramente legibles** tienen más potencial de descubrimiento que las piezas abstractas. `Fantasma paseando gatos` funciona como caso de referencia, pero todavía no debe convertirse en una regla universal porque la muestra comparable es pequeña.

La caída de la mediana de interacciones de julio a agosto justifica reabrir el carril de Reels, no abandonarlo. El problema actual es de instrumentación: sabemos qué publicaciones existen y sus interacciones actuales, pero no tenemos una serie consistente de vistas, retención, tiempo promedio visto, completaciones y seguidores ganados para todo el archivo.

La próxima prueba de Reels debe usar una tabla propia, separada de `Publication_Log.csv` de imágenes, con una fila por Reel y estos campos mínimos: `Reel_ID`, `Meta_Post_ID`, `fecha_local`, `duracion_segundos`, `hook_0_3s`, `personaje_principal`, `tipo_de_formato`, `nuevo_o_reuse`, `CTA`, `vistas`, `alcance`, `retencion_3s`, `tiempo_promedio_visto`, `completaciones`, `shares`, `comentarios`, `seguidores_ganados` y `fuente_de_metrica`.

## Implicaciones para el análisis solicitado

La conclusión documental es que **sí existe una base de Growth OS para analizar Instagram y Facebook**, pero no una cobertura completa de Reels ni una base todavía preparada para TikTok y YouTube. Por ello, el primer análisis de rendimiento debe comenzar con Meta, usando los datos ya documentados, y después crear una línea base separada para los dos canales nuevos. No se deben inferir resultados de TikTok o YouTube a partir del rendimiento de Instagram o Facebook.

## Monetización nativa de Meta

Meta informa oficialmente que **Facebook Content Monetization es actualmente invite-only**. El programa unifica formatos y puede remunerar Reels, fotos, Stories y publicaciones de texto elegibles; la elegibilidad y el pago dependen de las políticas, las vistas calificadas y el watch time que Meta determine. Meta indica además que los Reels deben tener un mínimo de 10 segundos para ser elegibles y que no cuentan piezas con watch time inferior a 5 segundos. [1] [2]

En esta auditoría no fue posible verificar el estado específico de invitación, elegibilidad, restricciones o configuración de pagos de `Universe Sent Me` porque Meta Business Suite abrió una pantalla de inicio de sesión en la sesión disponible. Por tanto, el estado correcto es **No verificado**, no “no elegible”. La comprobación debe hacerse en Meta Business Suite, seleccionando la página y entrando en `Monetization > Content monetization`; Meta documenta esa ruta como la ubicación oficial para consultar el estado. [2]

La API Graph utilizada para publicaciones no expone por sí sola el estado completo de monetización de la página. No se debe inferir la elegibilidad a partir de seguidores, interacciones o número de Reels.

## Monetización por afiliación de Mercado Libre

La estrategia de Mercado Libre está documentada como un carril de **story-commerce**. El estado ya no es “diseño activo / monetización no validada” en términos de preparación: el piloto contiene **10 links afiliados con etiqueta granular**, y Fernando confirmó que los 10 productos/links fueron publicados o adjuntados en Facebook.

Además, existe un Reel nuevo de Facebook `2210896633022235` con el producto nativo `MLMU3833350067` —soporte para celular con forma de gato—, link exclusivo `https://meli.la/1AQ2upG` y etiqueta `usmfb20260819p01`. El Reel está registrado como `Published` y `Native_Product_Attached_User_Confirmed`.

Lo que todavía no está validado es el rendimiento comercial: faltan cortes de clics, ventas aprobadas, unidades, ingresos y comisión confirmada por etiqueta. La publicación de links demuestra activación del carril, no conversión. Las métricas afiliadas deben mantenerse separadas de P0 y de las interacciones editoriales.

## Veredicto CGO

Reels no está fallando necesariamente por falta de potencial. La evidencia de Windsor muestra que Instagram sí tiene distribución medible y que los Reels dominan el reach y las views del canal durante el corte. Facebook Reels todavía está subinstrumentado en vistas y retención, y la medición entre plataformas necesita un ledger común con definiciones explícitas. La prioridad es consolidar esa tabla y no producir más Reels a ciegas.

La monetización nativa de Meta es una oportunidad futura, pero no debe tratarse como ingreso disponible hasta confirmar una invitación dentro de Business Suite. La monetización por afiliación puede probarse antes, pero requiere tracking real y una pieza piloto aprobada, no solo una estrategia escrita.

| Carril | Estado | Próxima acción |
|---|---|---|
| Reels Instagram | Amarillo | Consolidar el ledger de Windsor y validar muestras con el conector de Instagram |
| Monetización nativa Meta | Ámbar / No verificado | Revisar Business Suite > Monetization > Content monetization |
| Mercado Libre afiliados | Activo / medición pendiente | Ejecutar cortes de métricas por etiqueta y conciliar clics, ventas, unidades e ingresos |
| Reels Facebook | Ámbar | Completar vistas, retención y watch time mediante una extracción compatible |
| P0 imágenes | Separado | Esperar el primer corte 24h; no mezclar con este informe |

## Corrección de estado — 2026-08-20

La versión anterior de esta auditoría decía que Mercado Libre era únicamente un diseño activo y que todavía no existían enlaces trazables. Esa descripción quedó obsoleta. El ledger actual contiene diez links cortos granulares y un Reel afiliado adicional con confirmación humana de producto nativo. Las horas exactas y los IDs nativos individuales de nueve oportunidades del piloto todavía deben conciliarse, pero no deben marcarse como “no publicados”.

El siguiente análisis prioritario para este carril es comercial: mantener `Affiliate_Metrics_Snapshots.csv` como ledger append-only y separar `Clicks`, `Gross_Sales`, `Approved_Sales`, `Units_Sold`, `Revenue_MXN` y `Confirmed_Commission_MXN` de las métricas de contenido.

### Snapshot manual confirmado — 2026-08-20

Fernando confirmó mediante capturas del panel de Mercado Libre que el periodo **Últimos 7 días**, actualizado a las **20:51**, mostraba 2 clics, 0 compradores, 0 órdenes, 0 productos/unidades, $0 de ventas brutas, $0 de ventas estimadas y $0 de comisión. La pestaña **Fecha** mostró que los 2 clics correspondían al 18 de agosto, con 0 unidades, 0% de conversión y $0 de aumento estimado.

En la pestaña **Etiquetas de seguimiento** solo fueron visibles dos filas: la etiqueta histórica agregada `Links de facebook - universesentme` con 1 clic y `usmfb2605400826` —AFF-07, publicación `260540` de Elara— con 1 clic. AFF-07 queda como la única oportunidad granular con actividad visible en este corte; no registró unidades ni ventas. La etiqueta del Reel `usmfb20260819p01` no apareció en la tabla visible. Se clasifica como `Not_Visible_No_Inference`, no como cero clics, porque la interfaz puede ocultar etiquetas sin actividad.

El resultado confirma activación mínima del tracking —el sistema registra clics—, pero todavía no evidencia conversión. La muestra es demasiado pequeña para declarar ganador a AFF-07 o evaluar el Reel comercialmente. El ledger actualizado conserva los cortes históricos, el corte por fecha, el corte de 7 días y la ausencia visible de la etiqueta del Reel sin inventar métricas.

La extracción de Meta permanece separada: el post de página `1036844829507460_122153090559072582`, asociado al Reel `2210896633022235`, devolvió 1 reacción, 0 comentarios y `shares` no expuesto en el corte de las 05:07 UTC.

## Referencias

[1]: https://www.facebook.com/business/help/1049081556813520 "About Facebook Content Monetization for creators — Meta Business Help Center"

[2]: https://www.facebook.com/business/learn/lessons/understand-monetization-eligibility-status "Check and maintain your monetization eligibility status — Meta Blueprint"

[3]: https://creators.facebook.com/tools/facebook-content-monetization/ "Facebook Content Monetization — Facebook for Creators"

## Optimización del tracking del Reel con producto nativo — 2026-08-20

El Reel `2210896633022235` debe conservar exclusivamente la etiqueta `usmfb20260819p01`. Aunque utiliza el mismo producto de gato que AFF-08, no debe compartir el link ni la etiqueta de AFF-08, porque eso impediría distinguir si el clic provino del Reel o de la publicación `260590` de Maeve.

La optimización recomendada es mantener el producto nativo como única llamada a la acción comercial del Reel y no añadir simultáneamente el mismo producto mediante un comentario. Si en el futuro se prueba un comentario, debe generarse una etiqueta distinta, por ejemplo una etiqueta de superficie `POST_COMMENT`, y registrarse como experimento separado. De esa forma se evita la competencia entre dos links y se conserva la atribución.

La medición debe registrar snapshots en tres momentos: 24 horas, 48 horas y 7 días. Como la interfaz disponible permite periodos de 7, 15 y 30 días, cada snapshot debe conservar la fecha de captura, el periodo seleccionado, la fila visible de la etiqueta, los clics, las unidades, la tasa de conversión, el aumento estimado y la comisión. Si la etiqueta no aparece, el estado correcto es `Not_Visible_No_Inference`, nunca cero automático.

El resultado actual es una señal de instrumentación, no de conversión: el panel mostró 2 clics totales y 0 unidades, con 1 clic granular visible para AFF-07. El Reel no tiene todavía una fila visible. No se debe cambiar el producto ni el copy por este resultado; primero se necesitan al menos varios clics atribuibles a la etiqueta del Reel para evaluar si la superficie nativa convierte.

---
