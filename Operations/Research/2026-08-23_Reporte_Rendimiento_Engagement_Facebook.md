# Reporte de rendimiento y engagement — Facebook

**Propósito:** Presentar el rendimiento reciente de la Página de Facebook Universe Sent Me usando datos nativos de Meta y auditar si la información está integrada correctamente en el Growth OS.

**Estado:** Active
**Fecha de creación:** 2026-08-23
**Última actualización:** 2026-08-23
**Versión:** 1.1
**Autor:** Manus AI  
**Organización:** `Operations/Research/`  
**Documentos relacionados:** `GrowthOS/Integracion_Growth_OS.md`, `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`, `GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md`, `Operations/Research/2026-08-22_Analisis_Semanal_20260816_20260822.md`, `Operations/Research/2026-08-15_Publication_Log.csv`, `Operations/Research/2026-08-15_ExperimentLog.csv`, `Operations/Research/2026-08-23_Facebook_Performance_Meta_API.json`, `Operations/Research/2026-08-23_Facebook_Performance_Summary.json`, `Operations/Research/2026-08-23_Facebook_Growth_Integration_Audit.json`, `Operations/Research/2026-08-23_Facebook_Post_Reconciliation.json`, `Operations/Research/2026-08-23_Facebook_Performance_Recent_Chart.png`

---

## 1. Resumen ejecutivo

El snapshot vivo de Meta Graph API v26.0 incluye las **20 publicaciones más recientes** de Universe Sent Me, publicadas entre el 20 de agosto a las 15:00 UTC y el 23 de agosto a las 18:30 UTC. Al momento de la extracción, esas publicaciones acumulaban **4,081 interacciones públicas observables**, calculadas como reacciones + comentarios + shares. La mediana fue **45.5** por publicación y la media **204.05**; la diferencia muestra una distribución muy concentrada y dominada por un outlier. [1]

El post filosófico con el mensaje visible `☁️✨🤔`, asociado al ID `1036844829507460_122151375549072582`, acumuló **2,846 interacciones** y representa **69.7%** del total del snapshot. Los dos primeros posts representan **76.3%**. Por tanto, el rendimiento reciente no debe interpretarse con la media simple: la señal central es mucho más baja y la difusión está concentrada en pocas piezas. [1]

La integración con el Growth OS está **bien definida a nivel de arquitectura y parcialmente ejecutada a nivel operativo**. El proyecto ya tiene una definición métrica, ledgers de publicación y experimentos, HypothesisBank y reportes semanales. Sin embargo, el snapshot actual de Meta aún no cierra automáticamente las ventanas 24/72 horas ni contiene alcance o retención utilizables. Antes de esta ronda, tres Reels no estaban enlazados a los ledgers principales; la reconciliación posterior dejó **20 de 20 publicaciones recientes** con coincidencia por ID. El sistema ya tiene el crosswalk corregido, pero todavía no puede considerarse una integración completa de extremo a extremo por la brecha de ventanas e insights nativos. La primera prioridad de identidad quedó cerrada sin convertir snapshots lifetime en ventanas temporales. [1] [3] [4] [5] [6]

## 2. Alcance y definición métrica

La extracción se realizó en modo lectura el 23 de agosto de 2026 a las 20:04:20 UTC sobre las 20 publicaciones más recientes de la Página. El periodo visible de publicación va del 20 al 23 de agosto; no es una ventana fija de 24 o 72 horas y los valores son acumulados al momento de consulta. [1]

| Campo | Valor |
|---|---:|
| Publicaciones incluidas | 20 |
| Periodo de publicación visible | 2026-08-20 15:00 UTC – 2026-08-23 18:30 UTC |
| Engagement público total | 4,081 |
| Media por publicación | 204.05 |
| Mediana por publicación | 45.5 |
| Reacciones | 2,927 |
| Comentarios | 126 |
| Shares | 1,028 |
| Definición usada | Reacciones + comentarios + shares |
| Tasa de engagement | No calculable: Meta no entregó impresiones o alcance utilizables |

Las shares representan aproximadamente **25.2%** del engagement observable, los comentarios **3.1%** y las reacciones **71.7%**. La proporción de shares es una señal descriptiva de difusión, no una tasa de compartibilidad, porque el denominador correcto —alcance o impresiones— no está disponible en este snapshot. [1]

![Top 10 de publicaciones recientes y engagement por formato](2026-08-23_Facebook_Performance_Recent_Chart.png)

## 3. Rendimiento por formato

El snapshot clasificó 17 piezas como Imagen/Foto y 3 como Video/Reel según los adjuntos expuestos por Meta. Las imágenes reunieron **4,033 interacciones**, con mediana de **58**; los tres videos/Reels reunieron **48**, con mediana de **12**. [1]

| Formato | N | Engagement total | Media | Mediana | Reacciones | Comentarios | Shares |
|---|---:|---:|---:|---:|---:|---:|---:|
| Imagen/Foto | 17 | 4,033 | 237.24 | 58 | 2,889 | 122 | 1,022 |
| Video/Reel | 3 | 48 | 16.00 | 12 | 38 | 4 | 6 |

Esta diferencia **no es un veredicto causal contra Reels**. Las unidades tienen distinta madurez, distribución y tamaño de muestra, y Meta no entregó alcance, impresiones, reproducciones o retención utilizables para los posts individuales. El resultado correcto es que Facebook tiene una señal de imágenes mucho más sólida en este corte y una brecha de instrumentación para video, no que el formato de imagen sea universalmente superior. [1] [2]

## 4. Evolución por día de publicación

| Fecha UTC | Posts | Engagement | Media | Mediana | Lectura |
|---|---:|---:|---:|---:|---|
| 20 ago | 6 | 307 | 51.17 | 49.0 | Nivel moderado y relativamente estable. |
| 21 ago | 5 | 3,102 | 620.40 | 39.0 | Total dominado por el outlier de 2,846. |
| 22 ago | 5 | 546 | 109.20 | 58.0 | Mejor mediana que el 21; requiere más casos. |
| 23 ago | 4 | 126 | 31.50 | 22.0 | Menor acumulado y piezas más recientes; exposición inmadura. |

El 21 de agosto no debe declararse como “el mejor día” por su total. Sin el outlier, el día habría quedado en **256 interacciones** y la media habría sido **64** por publicación. La mediana diaria muestra que el 22 de agosto tuvo un centro superior en este snapshot, aunque la comparación no controla por formato, hora ni antigüedad. [1]

## 5. Top de publicaciones recientes

| Posición | Fecha UTC | ID de publicación | Mensaje visible | Reacciones | Comentarios | Shares | Engagement |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | 21 ago | `1036844829507460_122151375549072582` | `☁️✨🤔` | 2,029 | 52 | 765 | **2,846** |
| 2 | 22 ago | `1036844829507460_122151376083072582` | `😏🙈😂` | 221 | 14 | 33 | **268** |
| 3 | 21 ago | `1036844829507460_122151375627072582` | `🙂‍↔️` | 122 | 1 | 48 | **171** |
| 4 | 22 ago | `1036844829507460_122151375843072582` | `Analizando mi propio caos. 🧐` | 103 | 3 | 37 | **143** |
| 5 | 20 ago | `1036844829507460_122151375111072582` | `💸🪿😂` | 54 | 2 | 25 | **81** |

El top 5 suma **3,509 interacciones**, equivalente a **86.0%** de las 4,081 del snapshot. El dato más útil para el Growth OS no es copiar el outlier, sino estudiar qué elementos pueden ser transferibles: claridad inmediata del planteamiento, potencial de conversación, capacidad de compartir y reconocimiento del tono del universo de marca. El análisis no prueba que un único personaje, caption o horario haya causado el resultado. [1]

## 6. Disponibilidad de insights nativos

La API aceptó algunos nombres de métricas con respuesta HTTP 200, pero devolvió listas vacías, por lo que no se deben convertir en ceros. Las métricas de impresiones, alcance único y usuarios engaged devolvieron error de métrica no válida en este contexto. [1]

| Nivel | Métrica | Resultado actual |
|---|---|---|
| Por publicación | Impresiones, impresiones únicas, usuarios engaged | No disponibles; HTTP 400 por métrica no válida. |
| Por publicación | Clicks, reacciones por tipo, views de video, tiempo promedio de video | HTTP 200, pero sin valores utilizables. |
| Página | `page_post_engagements`, reacciones totales | HTTP 200, pero sin valores en la ventana solicitada. |
| Página | Impresiones, alcance, usuarios engaged, comentarios y shares por acción | No disponibles o métrica no válida en esta consulta. |

En consecuencia, este reporte sí puede comparar **engagement público acumulado por publicación**, pero no puede calcular engagement rate, alcance por pieza, retención de video, completions, CTR ni eficiencia por impresión. La ausencia de datos es una limitación de instrumentación, no evidencia de rendimiento cero.

## 7. ¿Está integrado correctamente en el Growth OS?

La respuesta es **sí a nivel de diseño; todavía no completamente a nivel de operación**. El Growth OS documenta una fuente maestra, un Publication Log por hecho de publicación, un ExperimentLog por hipótesis y observación, un HypothesisBank y una regla de actualización post-publicación. La integración conceptual está por encima de un reporte aislado: existe una ruta prevista desde Meta hacia publicación, experimento, hipótesis y próxima acción. [5]

La ejecución actual presenta cuatro brechas concretas:

| Área | Evidencia actual | Evaluación |
|---|---|---|
| Snapshot vivo | Se conserva el JSON completo del 23 de agosto con 20 posts y métricas públicas. | **Correcto**, pero todavía separado del artefacto normalizado histórico de 28 días. |
| Identidad de publicaciones | Los 20 de 20 IDs recientes coinciden ahora con Publication Log y ExperimentLog; los tres faltantes fueron reconciliados desde el inventario de Reels y el registro maestro. | **Corregido para este corte**; el crosswalk principal ya está completo. |
| Ventanas 24/72 horas | En las 30 filas operativas recientes del ExperimentLog y las 38 publicaciones de Facebook del Publication Log, no hay valores 24h ni 72h no vacíos; la observación de reconciliación de Reels también conserva ambos campos nulos. | **Insuficiente** para análisis temporal limpio; predominan cortes lifetime u observaciones pendientes. |
| Insights de alcance y video | El snapshot no entrega valores utilizables de impresiones, alcance, reproducciones o retención. | **Brecha de instrumentación**; Reels no puede subir de evidencia parcial sin otro origen nativo. |

La base histórica también está correctamente documentada, pero no está fresca: el artefacto normalizado de Facebook de 28 días contiene 143 filas y cubre del 22 de julio al 18 de agosto, con extracción del 19 de agosto. El reporte semanal 16–22 de agosto ya integró 42 publicaciones y 3,464 interacciones básicas observables, pero declaró expresamente que eran acumulados observables y que Reels carecía de views, reach y retención por publicación. El snapshot actual extiende la lectura hasta el 23 de agosto, pero aún no reemplaza ni actualiza automáticamente ese ciclo semanal. [1] [2]

## 8. Acciones prioritarias de integración

1. **Mantener el crosswalk reconciliado**: los 20 IDs recientes ya están enlazados con Publication Log, ExperimentLog e inventario especializado de Reels. No atribuir nuevas publicaciones a contenido, personaje, horario o hipótesis sin una identidad operativa verificable.
2. **Conservar el snapshot vivo como evidencia primaria** y generar una tabla normalizada por publicación con fecha de extracción, ventana, reacciones, comentarios, shares, impresiones, alcance y retención, usando valores nulos cuando Meta no entregue datos.
3. **Separar lifetime de 24/72 horas** en el Publication Log y ExperimentLog. Un acumulado actual no debe rellenar una ventana temporal que no fue capturada.
4. **Cerrar el circuito de hipótesis**: cada corte debe producir un veredicto explícito —señal, inconcluso o no evaluable— y una próxima acción conectada con HB-003, HB-004, HB-005 o la hipótesis de video correspondiente.
5. **Mantener el lenguaje de causalidad disciplinado**: el outlier filosófico es un caso prioritario de estudio; no valida por sí solo una regla de contenido, personaje, día u horario.

## 9. Veredicto

El Growth OS **sí está integrado como sistema documental y analítico**, pero **no está completamente integrado como pipeline automático de datos recientes**. La arquitectura, los ledgers, la definición métrica y las hipótesis están presentes. La prioridad no es crear otro dashboard, sino conectar este snapshot vivo con la identidad de publicación, conservar ventanas temporales honestas y cerrar el paso desde observación hasta veredicto y próxima acción.

## Referencias

[1]: `2026-08-23_Facebook_Performance_Meta_API.json` "Snapshot vivo de Meta Graph API v26.0, 20 publicaciones recientes"
[2]: `2026-08-22_Analisis_Semanal_20260816_20260822.md` "Análisis semanal de Facebook del 16 al 22 de agosto de 2026"
[3]: `2026-08-15_ExperimentLog.csv` "Ledger append-only de hipótesis y observaciones"
[4]: `2026-08-15_Publication_Log.csv` "Ledger append-only de publicaciones por plataforma"
[5]: `../../GrowthOS/Integracion_Growth_OS.md` "Documento de integración del Growth OS"
[6]: `2026-08-23_Facebook_Post_Reconciliation.json` "Reconciliación de tres Page Post IDs de Meta con los ledgers del Growth OS"
