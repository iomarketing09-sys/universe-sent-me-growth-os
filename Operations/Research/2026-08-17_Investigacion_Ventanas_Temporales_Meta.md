---
title: "Investigación — Ventanas temporales de Meta para interacciones 24/72h"
purpose: "Determinar por qué Meta no devuelve snapshots históricos exactos de 24 y 72 horas para el experimento de Facebook y definir una ruta verificable para futuras publicaciones."
status: "Review"
created: 2026-08-17
updated: 2026-08-17
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Production/extract_metrics_24_72.py"
  - "Operations/Production/extract_metrics_24_72_playbook.md"
  - "GrowthOS/08_00_Metricas_Baseline_Plataformas.md"
  - "Operations/Research/2026-08-17_Metricas_24_72_Extraccion_02.json"
  - "Operations/Research/2026-08-15_Auditoria_General_Growth_OS.md"
organization: "Operations/Research"
---

# Investigación — Ventanas temporales de Meta para interacciones 24/72h

## 1. Conclusión ejecutiva

El problema no se resuelve leyendo otra vez `reactions`, `comments` y `shares` del objeto del post. Esos campos representan acumulados actuales y no conservan automáticamente una fotografía histórica de cómo estaba la publicación exactamente a las 24 o 72 horas.

La solución operativa recomendada para el Growth OS es **capturar snapshots de contadores acumulados**, no intentar reconstruirlos retrospectivamente:

```text
E0  = reactions_0 + comments_0 + shares_0
E24 = reactions_24 + comments_24 + shares_24
E72 = reactions_72 + comments_72 + shares_72
Interacciones_24h = E24 - E0
Interacciones_72h = E72 - E0
```

Cada snapshot debe conservar los tres contadores sin procesar, la hora real de captura, la hora real de publicación, el Meta Post ID y el HTTP status. El resultado solo debe escribirse como ventana validada cuando la captura ocurra dentro de una tolerancia aprobada alrededor de `+24h` o `+72h`.

## 2. Qué permite oficialmente Meta

La referencia oficial de **Post Insights v26.0** documenta el endpoint `/{post-id}/insights`, el parámetro `metric`, los periodos `day`, `week`, `days_28`, `month`, `lifetime` y `total_over_range`, además de `since` y `until` como límites del rango temporal [1]. Sin embargo, que un parámetro exista en la interfaz no garantiza que una métrica concreta devuelva datos para cada publicación u objeto.

La referencia oficial de **Page Insights v26.0** indica que la mayoría de las métricas se actualizan aproximadamente cada 24 horas, que el histórico disponible es de hasta dos años, que `since` y `until` permiten consultar hasta 90 días y que `period` se calcula desde la recolección inicial del punto de datos [2]. También distingue métricas agregadas de Page y de Page post. `page_post_engagements` admite periodos diarios, pero es una métrica agregada de la página; no es una serie temporal atribuida automáticamente a cada publicación individual.

Meta también documenta que las interacciones de Reels no están incluidas en Page Insights [2]. La prueba actual se refiere a imágenes estáticas de Facebook, por lo que esta limitación no explica por sí sola el resultado, pero impide extender la misma ruta a Reels sin validación adicional.

## 3. Pruebas realizadas con Universe Sent Me

Las pruebas fueron de solo lectura y no modificaron ningún ledger, publicación, Instagram ni scheduler.

| Prueba | Resultado | Interpretación |
|---|---|---|
| Elegibilidad de Page Insights | `fan_count=4731`, `followers_count=4731` | La página supera el requisito documentado de 100 likes. |
| `/{post-id}/insights` con `post_engagements` | HTTP 200, `data=[]` para `lifetime` y `total_over_range` | El endpoint respondió, pero no entregó valores para este post/rango. |
| `/{post-id}/insights` con `post_reactions_by_type_total` | HTTP 200, `data=[]` | No ofrece un snapshot histórico utilizable en esta prueba. |
| `/{post-id}/insights` con `post_clicks` y `post_media_view` | HTTP 200, `data=[]` | No ofrece valores para este post/rango en la prueba. |
| `/{post-id}/insights` con `post_impressions` | HTTP 400, métrica inválida | La métrica está deprecada o no es válida en Graph API v26.0 para esta consulta. |
| `/{page-id}/insights` con `page_post_engagements` y `page_media_view` | HTTP 200, `data=[]` con rango y con `date_preset=last_3d` | La ruta agregada tampoco entregó datos en esta cuenta/rango. |
| Lectura directa del objeto post | HTTP 200 con reacciones, comentarios y shares | Devuelve acumulados lifetime actuales; no reconstruye el estado pasado. |

La evidencia de la extracción P0 del lote 15–16 está en `2026-08-17_Metricas_24_72_Extraccion_02.json`. En esa ejecución, cuatro publicaciones tenían ventana 24h elegible, pero Meta solo devolvió acumulados lifetime. Por ello se conservaron como evidencia y no se escribieron como `Interacciones_24h`.

## 4. Diagnóstico

Para las publicaciones ya pasadas del lote 15–16, el estado exacto de 24 y 72 horas **no puede recuperarse de forma confiable** a partir de los totales lifetime actuales. Restar una lectura actual contra cero, o usar el total lifetime como si fuera la ventana, sería metodológicamente incorrecto.

La consulta `since`/`until` tampoco debe considerarse una garantía de snapshot por publicación. Meta puede devolver una respuesta HTTP 200 con `data=[]`, puede entregar métricas agregadas de Page en lugar de una publicación individual y puede retrasar la actualización de la mayoría de las métricas aproximadamente 24 horas [2].

## 5. Solución recomendada para futuras publicaciones

### 5.1 Crear un baseline al publicar

Cuando un post de Facebook pase a publicado, el sistema debe capturar inmediatamente, o dentro de una tolerancia documentada de pocos minutos, los contadores actuales del objeto:

```text
snapshot_type = baseline
snapshot_at = hora real de captura
reactions_0
comments_0
shares_0
lifetime_interactions_0 = reactions_0 + comments_0 + shares_0
```

El baseline debe asociarse a `Publicacion_ID`, `Meta_Post_ID`, `CNT_ID` cuando exista y `Experiment_ID`.

### 5.2 Capturar +24h y +72h

Un único worker diario puede seleccionar todas las filas cuya ventana esté vencida y capturar los mismos contadores. La lectura debe clasificar la captura como `24h_snapshot` o `72h_snapshot` únicamente si cae dentro de la tolerancia acordada. El cálculo es:

```text
Interacciones_24h = lifetime_interactions_at_24h - lifetime_interactions_at_baseline
Interacciones_72h = lifetime_interactions_at_72h - lifetime_interactions_at_baseline
```

El sistema debe guardar tanto los valores crudos como los deltas. Si un contador disminuye por eliminación o ajuste de una interacción, la fila debe marcarse como anomalía y no ocultar el dato negativo sin explicación.

### 5.3 Cambiar la cadencia si se exige exactitud

La cadencia actual cada 48 horas minimiza despertares, pero **no garantiza** una lectura cercana a cada frontera de 24 horas. Para ventanas exactas, la mejor relación entre precisión y consumo es un solo despertar diario que procese todos los posts vencidos en lote. No se requieren 16 despertares ni una tarea por slot.

Meta permite agrupar hasta 50 llamadas Graph API en una petición batch, pero cada llamada interna sigue contando por separado para los límites de API y recursos [3]. El batch reduce conexiones HTTP y overhead, no el número lógico de lecturas.

### 5.4 Tratamiento del lote histórico

Para `CNT-031`–`CNT-039`, el Growth OS debe mantener `Snapshot_No_Disponible` donde no exista baseline histórica y no rellenar los campos 24/72h con lifetime. Las hipótesis `HB-003`, `HB-004` y `HB-005` no deben cerrarse usando esos totales.

## 6. Cambio recomendado al extractor

El extractor actual debe conservar dos modos separados:

| Modo | Uso | Escritura permitida |
|---|---|---|
| `legacy_lifetime_evidence` | Diagnóstico de publicaciones antiguas sin baseline | Solo evidencia JSON y marcador de indisponibilidad |
| `snapshot_delta` | Futuras publicaciones con baseline capturado | Snapshot ledger, deltas 24/72h y campos del ExperimentLog |

No se recomienda cambiar automáticamente el extractor ni modificar el scheduler hasta que Fernando apruebe el nuevo esquema de snapshots y la cadencia diaria. El siguiente paso técnico debe ser diseñar un `Metrics_Snapshot_Log.csv` separado, porque el `ExperimentLog` actual no conserva tres capturas crudas por publicación.

## 7. Estado de decisión

La solución propuesta queda en `Review`. No se ha alterado el schedule vigente, no se ha cambiado la definición histórica del experimento y no se han escrito métricas exactas que Meta no devolvió.

## Referencias

[1]: https://developers.facebook.com/docs/graph-api/reference/post/insights/ "Meta for Developers — Graph API Reference v26.0: Post Insights"

[2]: https://developers.facebook.com/docs/graph-api/reference/page/insights/ "Meta for Developers — Graph API Reference v26.0: Page Insights"

[3]: https://developers.facebook.com/docs/graph-api/batch-requests/ "Meta for Developers — Batch Requests"
