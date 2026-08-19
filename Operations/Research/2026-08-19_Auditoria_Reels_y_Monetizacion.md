---
title: "Auditoría de Reels y monetización"
purpose: "Separar el rendimiento histórico de Reels del experimento P0 de imágenes, verificar qué vías de monetización tienen evidencia real y establecer la cobertura documental del video corto en Instagram, Facebook, TikTok y YouTube."
status: "Review"
created: 2026-08-19
updated: 2026-08-19
version: "1.2"
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
organization: "Operations/Research"
---

# Auditoría de Reels y monetización

## Alcance y separación de métricas

Este informe no mezcla Reels con el experimento P0 de imágenes del 17 de agosto. Las métricas de este documento son acumulados actuales devueltos por objetos de publicaciones de video en Meta y sirven para comparar el carril histórico de Reels. No son ventanas 24/72 horas ni deben entrar en la mediana principal del P0.

La auditoría recuperó 12 publicaciones de video/Reel de la página `Universe Sent Me` mediante Meta Graph API v26.0. La API devolvió reacciones, comentarios y shares actuales; no devolvió vistas, watch time, retención o completaciones mediante la consulta de Insights intentada: las 12 consultas respondieron HTTP 400 por métrica de Insights inválida. Por eso las cifras de interacción son útiles para una primera lectura, pero no constituyen un análisis completo de distribución o retención.

## Cobertura multicanal dentro del Growth OS

La documentación existente cubre de forma operativa el rendimiento de **Instagram y Facebook** mediante Meta Graph API, Windsor, el conector de Instagram, registros manuales, auditorías de Reels, históricos de publicaciones, cruces de assets y el protocolo P0. La cobertura de Instagram mejoró: Windsor ya devuelve vistas, reach, engagement, guardados, shares y watch time de Reels. La deuda restante es consolidar un ledger uniforme y completar las métricas de distribución y retención de Facebook Reels y los snapshots 24/72 horas.

No se encontró dentro del repositorio un **ledger, histórico de rendimiento o protocolo específico para TikTok**. La nueva cuenta puede considerarse un canal abierto, pero su rendimiento aún no forma parte del Growth OS ni debe mezclarse con los datos de Meta.

Tampoco se encontró un **ledger, histórico de rendimiento o protocolo específico para YouTube**, incluidos Shorts. La cuenta debe registrarse como canal pendiente de instrumentación; antes de comparar resultados será necesario definir si se medirá por video, Short y canal, y conservar las ventanas temporales de YouTube Analytics separadas de las de Meta.

| Canal | Estado documental | Evidencia existente | Decisión operativa |
|---|---|---|---|
| Instagram | Parcialmente integrado | Registros, auditorías y cruces con Meta | Mantener separado por plataforma y añadir métricas de video |
| Facebook | Parcialmente integrado | Históricos, Meta Graph API, Insights y Reels | Mantener cortes comparables y no mezclar lifetime con 24/72 horas |
| TikTok | No integrado | No se encontró ledger ni histórico específico | Crear instrumentación antes de evaluar rendimiento |
| YouTube / Shorts | No integrado | No se encontró ledger ni histórico específico | Crear instrumentación antes de evaluar rendimiento |

La estructura correcta para el siguiente ciclo es un ledger de video corto con una fila por publicación y una columna explícita para `plataforma`. Los datos de Instagram y Facebook pueden compartir taxonomía, pero sus métricas deben permanecer separadas; TikTok y YouTube deben incorporarse como nuevos estratos cuando existan datos verificables.

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

La estrategia de Mercado Libre está documentada como un carril de **story-commerce** basado en `¿Qué me llegó?`, Wilfred, Universe, Elara y Silvio. Actualmente es una estrategia activa en documentación, pero no hay evidencia en los ledgers revisados de clics, ventas, conversiones, AOV, comisiones o RPM afiliado. Por ello su estado operativo es **Diseño activo / monetización no validada**.

El primer activo con señal comercial observable es el Reel de la lámpara de luna de Elara, que utilizó un CTA de comentario con la palabra `LUNA`. Sin embargo, la existencia de comentarios o interacción no demuestra clics ni ventas. Para cerrar el ciclo se necesita un enlace de afiliado trazable, un registro de clics y un ledger de conversiones. Los comentarios públicos no deben automatizarse con enlaces sin aprobación humana.

## Veredicto CGO

Reels no está fallando necesariamente por falta de potencial. La evidencia de Windsor muestra que Instagram sí tiene distribución medible y que los Reels dominan el reach y las views del canal durante el corte. Facebook Reels todavía está subinstrumentado en vistas y retención, y la medición entre plataformas necesita un ledger común con definiciones explícitas. La prioridad es consolidar esa tabla y no producir más Reels a ciegas.

La monetización nativa de Meta es una oportunidad futura, pero no debe tratarse como ingreso disponible hasta confirmar una invitación dentro de Business Suite. La monetización por afiliación puede probarse antes, pero requiere tracking real y una pieza piloto aprobada, no solo una estrategia escrita.

| Carril | Estado | Próxima acción |
|---|---|---|
| Reels Instagram | Amarillo | Consolidar el ledger de Windsor y validar muestras con el conector de Instagram |
| Monetización nativa Meta | Ámbar / No verificado | Revisar Business Suite > Monetization > Content monetization |
| Mercado Libre afiliados | Ámbar / No validado | Crear enlace trazable y ledger de clics, ventas y comisión |
| Reels Facebook | Ámbar | Completar vistas, retención y watch time mediante una extracción compatible |
| P0 imágenes | Separado | Esperar el primer corte 24h; no mezclar con este informe |

## Referencias

[1]: https://www.facebook.com/business/help/1049081556813520 "About Facebook Content Monetization for creators — Meta Business Help Center"

[2]: https://www.facebook.com/business/learn/lessons/understand-monetization-eligibility-status "Check and maintain your monetization eligibility status — Meta Blueprint"

[3]: https://creators.facebook.com/tools/facebook-content-monetization/ "Facebook Content Monetization — Facebook for Creators"
