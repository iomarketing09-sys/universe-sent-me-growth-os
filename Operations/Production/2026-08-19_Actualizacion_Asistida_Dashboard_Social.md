# Actualización asistida del dashboard social multicanal

**Propósito:** Definir el procedimiento reproducible para refrescar el dashboard de rendimiento de Universe Sent Me con un nuevo corte de datos de Windsor, preservando la trazabilidad de fuentes, ventanas, deduplicación y definiciones de métricas.

**Estado:** Active

**Fecha de creación:** 2026-08-19

**Última actualización:** 2026-08-19

**Versión:** 1.1

**Autor:** Manus AI

**Documentos relacionados:** `../../GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md`, `../../GrowthOS/08_00_Metricas_Baseline_Plataformas.md`, `../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`, `../Research/2026-08-19_Social_Performance_28D_Normalizado.json`, `../Research/2026-08-19_Retorno_Engagement_Esfuerzo_28D.json`, `../Research/2026-08-19_Historial_Reels_Consolidado.json`, `query_reel_insights.py`, `../../tools/normalize_social_dashboard_28d.py`, `../../tools/generate-dashboard-data.mjs`.

---

## Alcance y decisión operativa

El dashboard utiliza una **actualización asistida**, no un proceso autónomo. Cuando Fernando solicite un nuevo corte, el estudio extraerá los datos disponibles de Windsor para Facebook orgánico, Instagram, TikTok orgánico y YouTube; los normalizará; conservará el artefacto crudo o intermedio que corresponda; y actualizará el dataset que consume la interfaz. Esta decisión evita ejecutar consultas ocultas, mantiene control editorial sobre cada período y no requiere un servicio permanente.

> La actualización nunca debe sobrescribir evidencia previa sin conservar fecha de extracción, período, definición de métrica y ventana de comparabilidad.

## Secuencia de actualización

| Etapa | Acción requerida | Salida verificable |
|---|---|---|
| 1. Solicitud | Confirmar fecha de corte, período y plataformas incluidas. | Brief de extracción registrado en la tarea. |
| 2. Extracción | Consultar Windsor con campos validados por conector y cuenta. | Resultados fechados en `.mcp/tool-results/` o evidencia equivalente. |
| 3. Normalización | Deduplicar por `media_id`, `video_id`, `video` o `post_id`; mantener fuente y ventana. | Dataset `Social_Performance_<periodo>_Normalizado.json`. |
| 4. Control | No sumar snapshots lifetime de YouTube por día; no sustituir reach por views; no mezclar `post_engagements` de Windsor con la métrica canónica de Facebook. | Nota de comparabilidad dentro del dataset y baseline. |
| 5. Retorno | Recalcular engagement por pieza y, si hay horas/coste registrados, engagement por hora y por coste. | Artefacto `Retorno_Engagement_Esfuerzo_<periodo>.json`. |
| 6. Interfaz | Ejecutar el generador de datos del dashboard y validar filtros, tablas y gráficos. | Módulo de datos actualizado en el proyecto del dashboard. |
| 7. Versionado | Actualizar el baseline, registrar los cambios relacionados y publicar el commit. | GitHub como fuente única de verdad. |

## Reglas de normalización por plataforma

| Plataforma | Unidad de contenido | Métrica de engagement | Regla crítica |
|---|---|---|---|
| Facebook | `post_id` | `reacciones + comentarios + shares` | Mantener esta métrica canónica separada de `post_engagements` de Windsor. |
| Instagram | `media_id` | `media_engagement` | Tratar las métricas actuales como snapshot/lifetime salvo que la fuente entregue una ventana explícita. |
| TikTok | `video_id` | likes + comentarios + shares + favoritos | Eliminar filas repetidas nulas y conservar la fila de mayor cobertura métrica. |
| YouTube | `video` | likes + comentarios + shares de actividad diaria | Separar actividad diaria de `video_view_count`, que representa snapshot lifetime. |

## Cómo solicitar una actualización

La solicitud estándar es: **“Actualiza el dashboard social con un corte de [N] días hasta [fecha]”**. Si no se indica un período, se solicitará confirmación antes de extraer. Para proteger la coherencia analítica, cualquier nueva fuente, campo o cambio de definición se documentará antes de incluirlo en comparativos.

## Preflight del siguiente corte

Antes de iniciar la próxima extracción, el operador debe comprobar esta lista. Si una condición no se cumple, debe marcarse como `Pendiente` en el artefacto de corte; no debe rellenarse con valores inventados.

| Control | Evidencia requerida | Resultado esperado |
|---|---|---|
| Fecha de cierre y período | Solicitud explícita de Fernando. | Ventana ISO unívoca, por ejemplo `2026-07-23` a `2026-08-19`. |
| Plataformas | Facebook, Instagram, TikTok y YouTube confirmadas. | Consulta por plataforma y cuenta correcta. |
| Identidad analítica de nuevas piezas | `Concept_ID`, `Campaign_Label`, `Experiment_ID`, `Hypothesis_ID`, `Primary_Asset_ID`. | Valores previos a publicación o `Pendiente`; nunca retrospectivos inventados. |
| Cascada | `Platform_Content_ID` nativo por cada adaptación. | Vínculos en el historial consolidado o `Sin_cascada_confirmada`. |
| Esfuerzo | Coste y horas observadas cuando existan. | Retorno por MX$ y/o hora solo para filas con evidencia. |
| Control de comparabilidad | Fuente, ventana y definiciones de métrica. | Nota de límites dentro del JSON normalizado y dashboard. |

La plantilla de solicitud completa es: **“Actualiza el dashboard social con un corte de 28 días hasta [fecha]; aplica la convención `Concept_ID`/`Campaign_Label`/`Experiment_ID`/`Hypothesis_ID`; conserva `Pendiente` donde no haya evidencia.”**

## Datos de esfuerzo pendientes

La interfaz permite capturar **horas por pieza** y **coste por hora** como supuestos visibles. Esos valores no son evidencia oficial hasta que se registren con fecha, responsable, plataforma y criterio de cálculo. La siguiente evolución debe incorporar un ledger append-only de producción para transformar el proxy `engagement por pieza` en retorno de esfuerzo real.
