---
title: "Playbook — Extractor de métricas 24/72 horas"
purpose: "Definir la ejecución agrupada, idempotente y de bajo consumo del extractor de métricas para EXP-2026-08-CAL-01 sin publicar contenido ni modificar Instagram."
status: Active
created: 2026-08-16
updated: 2026-08-16
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Production/extract_metrics_24_72.py"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "Operations/Research/2026-08-15_ExperimentLog.csv"
  - "Operations/Research/2026-08-15_Metricas_24_72_Extraccion_01.json"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
  - "Operations/Research/2026-08-08_Ciclo_Diario_Metricas_24h.md"
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

## 5. Programación confirmada

La tarea independiente quedó activa el 2026-08-16 para ejecutarse a las 22:15 de `America/Matamoros` con la expresión de seis campos `0 15 22 */2 * *`, que establece la cadencia de días alternos del calendario. El identificador de la tarea es `egAl6a7WZExBrDPd8tIY1B` y el schedule está limitado al conector `Universe Sent Me Meta API` (`76925630-05da-4aa7-878d-64a6a520ca6d`), sin heredar el conector de Instagram. El modo permanece en un solo despertar de la tarea actual (`runAsNewTask=false`): una ejecución recorre el lote completo y no crea un despertar por publicación.

El detalle operativo exige usar `/home/ubuntu/extract_metrics_24_72.py`, procesar únicamente Facebook y `EXP-2026-08-CAL-01`, actualizar solo los dos ledgers indicados y registrar la evidencia JSON. Las consultas de Meta son de lectura; queda prohibido publicar, usar o modificar Instagram y modificar su scheduler.

La copia canónica del extractor está en `Operations/Production/extract_metrics_24_72.py`, y la copia operativa solicitada existe en `/home/ubuntu/extract_metrics_24_72.py`. La programación fue verificada como `active` y con zona horaria `America/Matamoros`.

## Referencias

[1]: ../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md "Fuente maestra y ledgers del Growth OS"
[2]: ../Research/2026-08-15_Publication_Log.csv "Ledger de hechos de publicación"
[3]: ../Research/2026-08-15_ExperimentLog.csv "Ledger de aprendizaje experimental"
[4]: https://developers.facebook.com/documentation/pages-api "Meta Pages API"
