---
title: "Auditoría de Reels y monetización"
purpose: "Separar el rendimiento histórico de Reels del experimento P0 de imágenes, verificar qué vías de monetización tienen evidencia real y establecer la cobertura documental del video corto en Instagram, Facebook, TikTok y YouTube."
status: "Active"
created: 2026-08-19
updated: 2026-08-21
version: "1.6"
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


## 10. Auditoría del inventario y operación de Reels — 2026-08-21

### 10.1 Resultado ejecutivo

La auditoría confirma que **sí existe una base histórica de Reels**, pero estaba fragmentada y desactualizada como vista operativa. El historial estructurado se actualizó de 45 a **48 registros por plataforma**: Facebook 19, Instagram 16, TikTok 7 y YouTube 6. Estos registros representan publicaciones, no piezas únicas; corresponden a **21 conceptos identificables** y **17 grupos cross-platform**.

| Área auditada | Estado |
|---|---|
| Inventario histórico | **Integrado y actualizado** a `2026-08-21` en `Historial_Reels_Consolidado.json` v1.5 |
| Lista operativa visible | **Actualizada** en `GrowthOS/07_00_Registro_Maestro_Reels.md` v2.6 |
| Reel más reciente de Meta | **Publicado y verificado:** `Universe viéndote Farmear Aura` |
| Reels programados en Facebook | **47 posts programados**, todos de imagen; **0 videos/Reels** en el scheduler consultado |
| Maeve | **En revisión de producción**, no publicado como Reel verificable |
| Experimentación formal | Solo 1 de 48 registros tiene `Experiment_ID` y `Hypothesis_ID` explícitos |
| Métricas de video | Parciales; Facebook no devolvió views/reach/retención en el corte actual |

### 10.2 Reel publicado hoy

Meta devolvió el Reel **`Universe viéndote Farmear Aura`** con Page Post ID `1036844829507460_122154017667072582`, Reel ID `2005557463434064`, permalink `https://www.facebook.com/reel/2005557463434064/`, hora de publicación `2026-08-21 21:30:59 UTC` y `is_published=true`. Esto equivale aproximadamente a las 16:30 en `America/Matamoros`. La consulta de comentarios devolvió un único comentario de la propia Página (`@seguidores Universe Sent Me`), no una conversación de comunidad.

El Reel está publicado, pero **todavía no está medido**: la consulta de Insights devolvió HTTP 400 con `The value must be a valid insights metric`, y no se deben convertir las interacciones actuales en una ventana 24/72 horas. El estado correcto es `Publicado_Metricas_Pendientes`, no `Programado` ni `ExperimentLog_Cerrado`.

La consulta de `/{page_id}/scheduled_posts` devolvió 47 registros, todos con attachment `photo` y `is_published=false`; ninguno era un video. Por ello, el Reel de hoy no quedó en el scheduler de Facebook en el momento del corte: ya estaba publicado en el feed. Si Fernando lo programó previamente, Meta ya lo convirtió en publicación real y el registro debe conservar ambas etapas solo si existe evidencia de programación anterior.

### 10.3 Reels recientes incorporados al inventario

Se integraron tres publicaciones de Facebook que no estaban en el corte estructurado anterior:

| Concepto | Meta Post / Reel | Estado documental |
|---|---|---|
| `Doble Check → Universe` | `1036844829507460_122153090559072582` / `2210896633022235` | Publicado en cascada; `EXP-202608-REALUNIVERSE-01`, `HB-REEL-01`; métricas separadas de imágenes |
| `Remote Control` | `1036844829507460_122153750763072582` / `2815726225473165` | Cascada completa confirmada; snapshot 24h pendiente |
| `Farmear Aura` | `1036844829507460_122154017667072582` / `2005557463434064` | Facebook confirmado; crosspost y asset fuente pendientes de evidencia |

`Remote Control` y `Doble Check` ya tienen documentación de producción/cascada. `Farmear Aura` solo tiene por ahora evidencia de Meta; no se crea CNT ni se infiere una relación con un asset de Drive o con una publicación en otra plataforma.

### 10.4 Estado de Maeve

El proyecto de Maeve localizado en el repositorio es `Crave You — Maeve entre todas las miradas` y su variante `La habitación de las plumas`. El documento de producción permanece en `REVIEW`; no existe un export de video ni un `Platform_Content_ID` asociado dentro del Growth OS actual. Por lo tanto, se registra como **`En_Produccion/Pendiente_Revision`**, no como Reel publicado, programado ni medido.

Si el Reel de Maeve que Fernando menciona es otro archivo o una producción iniciada fuera del repositorio, el próximo dato mínimo necesario será uno de estos tres elementos: nombre exacto del archivo, fecha/hora de publicación o ID nativo de la plataforma. Con cualquiera de ellos se puede reconciliar sin crear un duplicado.

### 10.5 Diagnóstico de cobertura

La cobertura histórica es suficiente para afirmar que el estudio lleva meses produciendo y publicando video corto, pero todavía no es suficiente para un análisis de Growth OS plenamente comparable. De los 48 registros, 29 tienen evidencia de asset en Drive, 33 tienen alguna cifra de engagement, 27 tienen views, 14 tienen reach y ninguno tiene una serie completa y uniforme de views, retención, tiempo promedio visto, completaciones y seguidores ganados en las cuatro plataformas. Facebook concentra 19 registros, pero el corte actual tiene 0/19 con views o reach recuperables.

La principal deuda no es “crear más Reels”, sino formalizar el estado y la medición de cada publicación. El inventario debe separar cinco estados: `Idea`, `En_Produccion`, `Pendiente_Revision`, `Programada`, `Publicada_Metricas_Pendientes` y `Medida_24_72h`. El `ExperimentLog` solo se actualiza cuando exista una hipótesis explícita y una ventana de métricas verificable.

### 10.6 Próxima corrección operativa

A partir de este corte, cada Reel nuevo debe registrarse antes de producirse con `Concept_ID`, `Primary_Asset_ID`, `Platform`, `Experiment_ID` si aplica, `Hypothesis_ID` si aplica, `Production_Status`, `Publication_Status`, `Platform_Content_ID`, `Publication_Local`, `Crosspost_Status`, `Source_Window` y `Metrics_Status`. El Reel de Maeve debe permanecer en la cola de producción hasta que Fernando apruebe la dirección y exista un export; el Reel de hoy debe entrar a la cola de medición, no a una nueva cola creativa.

## 11. Puente de transferencia Facebook → Reels — 2026-08-21

Los experimentos comparables de imágenes sí pueden alimentar el carril de Reels, pero únicamente como **fuente de hipótesis editoriales y de diseño**. Sus interacciones, shares, medianas, horarios y veredictos no se trasladan como resultados de video. La plataforma, el formato y la unidad de consumo son distintos; por eso la transferencia correcta convierte una señal visual o narrativa en una hipótesis nueva, con un `Experiment_ID`, un `Hypothesis_ID` y métricas nativas de video propios.

| Aprendizaje de imágenes | Traducción válida a Reel | No debe transferirse directamente | Métrica de validación en Reel |
|---|---|---|---|
| Situación humana reconocible y emoción legible | Abrir con conflicto visible en 0–1.2 s, sin depender del audio | El número de interacciones del post estático | Retención inicial, reach de no seguidores y completaciones |
| Microhistoria de tres tiempos | Convertirla en setup → reacción → payoff/loop en 5–10 s | Tratar tres paneles como equivalente automático a tres segundos o a una duración fija | Retención por tramo, completación y shares |
| Transformación visual de Universe | Usar una transición real → Universe conservando gafas y marcadores de identidad | Heredar el resultado histórico de la imagen o atribuirlo al personaje aislado | Retención de transición, completación y shares |
| Humor observacional o ácido | Mostrar el conflicto en una lectura y resolverlo con una reacción seca o un diálogo breve | Mezclar humor ácido, autodesprecio, doble sentido y conversación como una sola familia | Shares, comentarios raíz, replies y mediana de interacciones |
| `caption_minimo`, `caption_refuerzo`, `caption_conversacional` | Registrar por separado copy de apoyo, texto en pantalla y CTA de publicación | Concluir que un tratamiento ganador en imágenes también gana en video | Comparación dentro de una celda de video balanceada |
| Hora de prueba | Usarla como covariable y distribuir casos comparables en más de una franja | Interpretar una hora ganadora sin controlar hook, duración y situación | Resultado ajustado por cohorte y franja |

### 9.1 Cómo aprovecharlo sin contaminar los carriles

El flujo recomendado es de **traducción, no de mezcla**. Primero se registra el experimento o publicación de Facebook como fuente (`Source_Experiment_ID`, `Source_Post_ID`, `Source_Cell_ID`, `Source_Learning_Type` y `Source_Window`). Después se redacta un brief de Reel nuevo que conserva la idea que se quiere probar, pero define una hipótesis de video independiente. Si el resultado de la imagen aún no tiene publicación o ventana métrica cerrada, la fuente solo puede clasificarse como `Design_Input`, nunca como `Performance_Learning`.

El Reel debe recibir antes de producción su propio `Concept_ID`, `Campaign_Label`, `Experiment_ID`, `Hypothesis_ID`, `Primary_Asset_ID`, duración, hook de 0–3 segundos, `Narrative_Structure`, `Caption_Treatment`, `Caption_Function`, `Character_Presence`, `Crosspost_Status` y estado de reuse. Si se convierte un meme histórico en Reel, debe respetarse la regla de reutilización de al menos 30 días desde la última publicación y debe registrarse como adaptación, no como repost idéntico.

La primera traducción recomendada, una vez que existan resultados de los comparables, es `FUT-TRANS-003` hacia una subfamilia de **transformación visual real → Universe**. La segunda es convertir `FUT-MICRO-005` o `FUT-MICRO-006` en una microhistoria audiovisual de tres beats. La tercera es traducir `FUT-ACID-003` a un diálogo ácido de 5–7 segundos. Estas tres rutas no deben entrar automáticamente en `HB-REEL-01`, que actualmente prueba la familia `REAL → UNIVERSE / REACCIÓN`; cada ruta debe tener hipótesis propia o una ampliación aprobada de la celda.

### 9.2 Instrumentación mínima del puente

El ledger de video debe conservar una fila por publicación y plataforma. Para cada Reel se deben capturar snapshots de 24 y 72 horas con `views`, `reach`, `retention_3s`, `avg_watch_time_seconds`, `completion_rate`, `shares`, `comments`, `replies`, `followers_gained` y `source_of_metric`. Las filas de Instagram, Facebook, TikTok y YouTube pueden compartir el mismo `Concept_ID` y `Primary_Asset_ID`, pero nunca deben sumarse como una audiencia o una mediana multicanal única.

La afiliación se mantiene como carril comercial separado. Si un Reel lleva producto nativo o enlace de Mercado Libre, se registra `Affiliate_Attachment`, etiqueta, link, producto y hora de adjunción en el ledger afiliado; las ventas, clics y conversiones no se mezclan con el veredicto editorial de hook, retención o compartibilidad.

### 9.3 Criterio de aprendizaje

Una imagen con buen rendimiento genera una **hipótesis candidata** para video, no una garantía de éxito. El Reel se clasifica como `WIN`, `SIGNAL`, `FAIL` o `NO_LEARNING` únicamente después de verificar la ventana, la instrumentación y la estabilidad de las variables. Para una señal preliminar se requieren al menos tres casos de video comparables; para un veredicto operativo, cinco. Los outliers deben reportarse con mediana, sensibilidad sin outlier y tamaño de muestra limpio y contaminado.

La decisión operativa actual es no programar una ola nueva de Reels únicamente por los tres posts comparables de Facebook. Primero se cierran sus ventanas de publicación y se registra qué hipótesis visual o narrativa sobrevivió a la evidencia. Después se prepara un lote de Reels separado, con control de duración, hook, personaje, CTA y producto, para comprobar si el aprendizaje cruza realmente de imagen a video.
