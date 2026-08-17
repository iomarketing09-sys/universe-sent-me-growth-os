---
title: "Playbook — Extractor de métricas 24/72 horas"
purpose: "Definir la ejecución agrupada, idempotente y de bajo consumo del extractor de métricas para EXP-2026-08-CAL-01 sin publicar contenido ni modificar Instagram."
status: Active
created: 2026-08-16
updated: 2026-08-17
version: "1.2"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Production/extract_metrics_24_72.py"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "Operations/Research/2026-08-15_ExperimentLog.csv"
  - "Operations/Research/2026-08-15_Metricas_24_72_Extraccion_01.json"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
  - "Operations/Research/2026-08-08_Ciclo_Diario_Metricas_24h.md"
  - "Operations/Research/2026-08-17_Investigacion_Ventanas_Temporales_Meta.md"
organization: "Operations/Production"
---

# Playbook — Extractor de métricas 24/72 horas

## 1. Propósito

Este playbook define la ruta operativa para la revisión agrupada del experimento `EXP-2026-08-CAL-01`. La tarea independiente debe despertar una sola vez cada 48 horas, a las 22:15 de `America/Matamoros`, y ejecutar `extract_metrics_24_72.py` sobre el lote completo. El proceso consulta solo publicaciones de Facebook del experimento que tengan Meta Post ID y una ventana vencida.

El extractor no publica contenido, no responde comentarios, no toca Instagram y no modifica el scheduler de Instagram. La unidad de idempotencia es `Publicacion_ID` junto con el marcador `METRICS-RUN:<run_id>` que se registra en los ledgers.

## 2. Contrato de datos

La fuente de hechos de publicación es `Operations/Research/2026-08-15_Publication_Log.csv`. La fuente de observaciones de aprendizaje es `Operations/Research/2026-08-15_ExperimentLog.csv`. El script conserva la hora real de publicación, calcula las ventanas `+24h` y `+72h` en la zona `America/Matamoros` y procesa todas las filas vencidas en una sola ejecución.

Los conteos actuales de `reactions`, `comments` y `shares` que Graph API devuelve sin una ventana temporal exacta se guardan únicamente dentro de la evidencia JSON. No se escriben como `Interacciones_24h` ni `Interacciones_72h`. Si la API no permite reconstruir el snapshot exacto, el script registra `24h_snapshot_unavailable` o `72h_snapshot_unavailable` y no inventa métricas.

## 3. Comando de ejecución

La ruta que espera la tarea es:

```text
/home/ubuntu/extract_metrics_24_72.py
```

La copia canónica del repositorio es:

```text
Operations/Production/extract_metrics_24_72.py
```

La ejecución normal debe generar evidencia en `Operations/Research/2026-08-16_Metricas_24_72_Extraccion.json` y actualizar únicamente las notas/conclusiones de las filas elegibles:

```bash
python3 /home/ubuntu/extract_metrics_24_72.py \
  --evidence /home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-16_Metricas_24_72_Extraccion.json
```

Para pruebas sin red ni escritura:

```bash
python3 /home/ubuntu/extract_metrics_24_72.py \
  --dry-run \
  --evidence /home/ubuntu/metrics_extraction_dry_run.json
```

La tarea debe proporcionar `META_PAGE_ACCESS_TOKEN`. El script deriva el Page Access Token de `Universe Sent Me` mediante `/me/accounts`; nunca imprime ni guarda tokens.

## 4. Resultado de validación

La prueba seca determinista con `--now 2026-08-18T04:00:00Z` encontró 9 candidatos y 9 ventanas de 24 horas elegibles, escribió 0 métricas, hizo 0 llamadas de red, no actualizó los ledgers, no publicó contenido y no tocó Instagram. Esto confirma que un solo despertar puede procesar el lote completo.

La primera ejecución real debe conservar la evidencia JSON y registrar la limitación de ventana si Meta solo devuelve totales acumulados. La extracción no debe cerrar `HB-003`, `HB-004` o `HB-005` hasta que existan métricas válidas o una decisión explícita de tratar las ventanas como no disponibles.

## 5. Diagnóstico de ventana temporal y diseño futuro

La revisión P0 del 17 de agosto confirmó que la lectura directa del objeto post devuelve acumulados lifetime. Las consultas de Post Insights v26.0 con `post_engagements`, `post_reactions_by_type_total`, `post_clicks` y `post_media_view` respondieron HTTP 200 pero `data=[]` para la publicación probada; `post_impressions` respondió como métrica inválida. Page Insights también respondió sin datos para `page_post_engagements` y `page_media_view` en los rangos probados. La página sí supera el requisito documentado de 100 likes, con 4,731 seguidores/likes al momento de la prueba.

Por lo tanto, este extractor conserva dos comportamientos: `legacy_lifetime_evidence` para publicaciones sin baseline histórica, que nunca escribe lifetime en campos 24/72h; y `snapshot_delta` para publicaciones futuras, que primero captura un baseline y luego calcula `Interacciones_24h`/`Interacciones_72h` como diferencia entre contadores acumulados. La investigación completa está en `Operations/Research/2026-08-17_Investigacion_Ventanas_Temporales_Meta.md`.

La cadencia actual de 48 horas reduce despertares, pero no garantiza una captura cercana a cada frontera de 24 horas. Si Fernando aprueba la nueva arquitectura, se recomienda un solo despertar diario que procese todas las filas vencidas y agrupe las lecturas en Batch Requests. Meta limita cada batch a 50 llamadas y sigue contando cada llamada interna para los límites de API; el batch reduce conexiones, no el número lógico de lecturas.

El lote histórico 15–16 permanece como `Snapshot_No_Disponible` cuando no existe baseline. No se cierran `HB-003`, `HB-004` ni `HB-005` con lifetime.

## 6. Programación confirmada

La tarea independiente quedó activa el 2026-08-16 para ejecutarse a las 22:15 de `America/Matamoros` con la expresión de seis campos `0 15 22 */2 * *`, que establece la cadencia de días alternos del calendario. El identificador de la tarea es `egAl6a7WZExBrDPd8tIY1B` y el schedule está limitado al conector `Universe Sent Me Meta API` (`76925630-05da-4aa7-878d-64a6a520ca6d`), sin heredar el conector de Instagram. El modo permanece en un solo despertar de la tarea actual (`runAsNewTask=false`): una ejecución recorre el lote completo y no crea un despertar por publicación.

El detalle operativo exige usar `/home/ubuntu/extract_metrics_24_72.py`, procesar únicamente Facebook y `EXP-2026-08-CAL-01`, actualizar solo los dos ledgers indicados y registrar la evidencia JSON. Las consultas de Meta son de lectura; queda prohibido publicar, usar o modificar Instagram y modificar su scheduler.

La copia canónica del extractor está en `Operations/Production/extract_metrics_24_72.py`, y la copia operativa solicitada existe en `/home/ubuntu/extract_metrics_24_72.py`. La programación fue verificada como `active` y con zona horaria `America/Matamoros`.

## Referencias

[1]: ../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md "Fuente maestra y ledgers del Growth OS"
[2]: ../Research/2026-08-15_Publication_Log.csv "Ledger de hechos de publicación"
[3]: ../Research/2026-08-15_ExperimentLog.csv "Ledger de aprendizaje experimental"
[4]: https://developers.facebook.com/documentation/pages-api "Meta Pages API"
[5]: ../../Operations/Research/2026-08-17_Investigacion_Ventanas_Temporales_Meta.md "Investigación de ventanas temporales de Meta"
