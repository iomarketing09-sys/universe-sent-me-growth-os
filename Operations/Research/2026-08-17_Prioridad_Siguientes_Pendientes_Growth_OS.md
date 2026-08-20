---
title: "Prioridad de siguientes pendientes del Growth OS"
purpose: "Ordenar el trabajo posterior al análisis histórico y a la activación de monetización según impacto, urgencia, dependencia y criterio de cierre."
status: Active
created: 2026-08-17
updated: 2026-08-20
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-19_Auditoria_Integral_Growth_OS.md"
  - "Operations/Research/2026-08-19_Auditoria_Reels_y_Monetizacion.md"
  - "Operations/Research/2026-08-20_Cohorte_17_30_Actual_Cut.md"
  - "Operations/Production/2026-08-20_Segunda_Capa_Afiliados_Posts_Ganadores.md"
  - "Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md"
  - "Operations/Research/2026-08-17_Analisis_Julio_Taxonomia_y_Pendientes_Growth_OS.md"
  - "GrowthOS/00_01_Changelog_GrowthOS.md"
organization: "Operations/Research"
---

# Prioridad de siguientes pendientes del Growth OS

## Estado ejecutivo — 20 de agosto de 2026

El Growth OS está operativo en publicación, lectura de Meta, atención comunitaria y activación afiliada, pero todavía tiene una deuda de instrumentación y fuente maestra. El ciclo P0 de las cinco publicaciones del 17 de agosto ya no está pendiente de extracción básica: quedó **Cerrada_con_limitacion** porque Meta no entregó snapshots exactos de 24/72 horas. El aprendizaje se conserva como corte observado separado de la métrica contractual.

La prioridad actual no es abrir más frentes creativos, sino medir correctamente lo que ya está activo: la cohorte Facebook 17–30, el Reel con producto nativo, los diez links afiliados y los dos productos de la Capa 2. En paralelo, conviene corregir la reconciliación de inventario y los duplicados históricos sin crear CNT automáticos.

## Pendientes activos priorizados

| Prioridad | Carril | Pendiente | Dependencia | Criterio de cierre |
|---|---|---|---|---|
| P1 | Facebook / estadística | Continuar los cortes de la cohorte 17–30 y actualizar `Publication_Log.csv` conforme los posts pasen de `Programada` a publicados | Publicación real, Meta Post ID y fecha/hora local | Cada fila publicada tiene estado, permalink/Meta ID, interacciones observadas y clasificación separada de lifetime |
| P1 | Afiliados | Capturar snapshots por etiqueta para AFF-01–AFF-10, el Reel `usmfb20260819p01` y la Capa 2 `usmwin2608029w0820` / `usmwin260539ek0820` | Acceso manual a Central de Afiliados y paneles de 7/15/30 días | Ledger con cortes visibles, clics, unidades, ventas y comisión; `Not_Visible_No_Inference` cuando una etiqueta no aparezca |
| P1 | Reels | Completar la instrumentación del Reel `2210896633022235`: vistas, watch time, retención y, si es posible, shares/video insights compatibles | Campos Meta/Windsor compatibles y ledger separado por plataforma | Una fila reproducible con métricas de video, fuente, corte temporal y separación de afiliación |
| P1 | Fuente maestra | Crear alias `Asset_Ref ↔ filename operativo ↔ CNT/id ↔ Meta Post ID` y enlazar los cinco assets P0 al inventario o documentar su excepción | Reconciliación sin inventar CNT | La programación activa puede cruzarse con el inventario sin falsos huérfanos ni relaciones creadas por filename por sí solo |
| P1 | Histórico | Consolidar los cinco Meta IDs duplicados de junio antes de usar agregados o rankings acumulados | Comparación de fuentes y preservación de evidencia múltiple | Una publicación lógica por Meta ID, con fuentes y métricas no duplicadas |
| P2 | Histórico | Ampliar el análisis individual de julio solo con una pregunta concreta de rendimiento, empezando por shares, comentarios y taxonomía visual | Más reconciliación de assets y prioridad editorial | Nuevo lote con asset, Meta ID, métricas lifetime, taxonomía y pregunta de aprendizaje explícita |
| P2 | Multicanal | Convertir los cortes existentes de Instagram, TikTok y YouTube en ledgers append-only separados | Normalización de columnas por plataforma | Una fila por publicación y plataforma, sin mezclar audiencia, vistas o watch time entre canales |
| P2 | Comunidad | Mantener el monitoreo incremental de comentarios bajo aprobación humana; queda pendiente que Fernando publique manualmente la respuesta en el post externo de Skocaj Soledad | Acceso del perfil/página al post de tercero | Deltas revisados, respuestas aprobadas registradas y ninguna escritura no autorizada |
| P2 | Conocimiento | Revisar con Claude las hipótesis sustentadas por datos antes de modificar la Biblia o el canon | Evidencia histórica clasificada y changelog sincronizado | Cada regla queda como sustentada, compatible, contradicha o sin evidencia; no se canonizan outliers aislados |

## Aprobaciones o decisiones que pueden abrirse después

La propuesta `2026-08-20_Propuesta_Pieza02_MovimientoInusual_Universe.md` sigue como `DRAFT_NOT_AUTHORIZED`; no debe producirse ni publicarse hasta definir hipótesis, asset/export, canción y relación narrativa. La exploración de videoclip musical/desamor también permanece en propuesta con variables de canción y disponibilidad por plataforma pendientes.

La expansión de la Capa 2 afiliada no requiere una decisión inmediata: la primera ola ya está activa en `2608029` y `CNT-034 / 260539`. Cualquier nuevo producto debe esperar datos iniciales y conservar una etiqueta exclusiva; no se debe adjuntar automáticamente a otro post ganador solo por superar un umbral de interacciones.

## Pendientes documentales de mantenimiento

La auditoría integral de agosto conserva secciones históricas redactadas antes del cierre provisional P0 y antes de la activación afiliada. Debe actualizarse para que su semáforo y sus prioridades no vuelvan a describir P0 como pendiente de extracción ni Mercado Libre como diseño no verificado. El registro maestro de Reels también conserva una sección histórica de “Auditoría de Cascada Pendiente” que debe marcarse como histórica o reconciliarse con el consolidado de 45 registros.

La deuda de IDs nativos individuales de los productos afiliados adjuntados manualmente no bloquea la medición por etiqueta, pero debe conservarse como conciliación pendiente. Las horas exactas de adjunción tampoco deben inventarse.

## Cerrado o no pendiente actualmente

| Área | Estado real |
|---|---|
| P0 de cinco posts del 17 de agosto | Cerrado provisionalmente con limitación de ventanas exactas; no reabrir como extracción básica |
| Cohorte 15–16 | Análisis completado; no repetir salvo nueva pregunta de aprendizaje |
| P1 copy guidelines | Documentadas en la sección 16 de `06_00_Reglas_Aprendizaje_Tendencias.md` |
| Capa 2 afiliada | Activa en dos publicaciones con adjunción manual confirmada; medición pendiente |
| Movimiento Drive de 46 assets | Verificado como completado, `46/46` en `08 Agosto` |
| Scheduler histórico de Instagram 15–16 | Eliminado/pausado; no reactivar en este ciclo |
| CNT-004 | Diferido operativamente; no desarrollar ni usar como evidencia activa |
| Silvio / Payaso | Resuelto en canon; no abrir una nueva revisión por esa contradicción |
| Make | Solo trazabilidad histórica; no forma parte de la arquitectura activa |

## Secuencia CGO recomendada

Primero deben actualizarse los cortes de la cohorte 17–30 y el tracking afiliado porque son operaciones activas con valor de aprendizaje inmediato. Después conviene completar la extracción de video del Reel y corregir la documentación histórica de Reels. En tercer lugar debe construirse la tabla de alias y consolidarse la duplicación de junio; esa normalización hará más confiables los análisis de julio y la fuente maestra. Solo después conviene abrir nuevas piezas de Reel, ampliar la Capa 2 o revisar la Biblia con Claude.

No se debe mezclar lifetime histórico con 24/72 horas, convertir un outlier en regla, reactivar el scheduler de Instagram ni modificar el canon sin evidencia comparable y aprobación explícita.
