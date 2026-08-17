---
title: "Índice visual de assets y reporte incremental de publicaciones"
purpose: "Definir una arquitectura persistente para analizar assets de Drive una sola vez y mantener reportes de publicaciones mediante actualizaciones incrementales, evitando búsquedas visuales completas repetidas."
status: "Active"
created: 2026-08-17
updated: 2026-08-17
version: "1.4"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-17_Cruce_Assets_Junio_Meta_Top.md"
  - "Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv"
  - "Operations/Research/2026-08-17_Auditoria_Revision_Junio.md"
  - "Operations/Research/Historical_Performance_Individuals.csv"
  - "GrowthOS/Content_Inventory.csv"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
  - "Operations/Production/extract_metrics_24_72_playbook.md"
organization: "Operations/Research"
---

# Índice visual de assets y reporte incremental de publicaciones

## Dictamen CGO

No es eficiente volver a buscar visualmente los 196 assets de `06 Junio` cada vez que aparezca una publicación histórica. Conviene separar el trabajo en dos capas: un **índice visual persistente** que se construye una vez por carpeta y un **reporte incremental** que solo procesa assets nuevos, modificados o todavía no reconciliados.

El índice no reemplaza `Content_Inventory.csv`. Su función es localizar evidencia visual y acelerar cruces; el inventario maestro sigue siendo la fuente de relaciones CNT y estados operativos.

## Índice visual propuesto

Cada fila debe representar un archivo de Drive y conservar `periodo`, `drive_id`, `filename`, `asset_ref`, `mime_type`, `modified_time`, `width`, `height`, `aspect_ratio`, `hash_visual`, `ocr_text`, `palette_summary`, `character_candidates`, `caption_candidates`, `folder`, `visual_status`, `meta_match_status`, `meta_post_id`, `publication_date_local`, `cnt_id`, `evidence_source` y `last_analyzed_at`.

Los estados deben distinguir entre `Asset_Indexed`, `Meta_Match_Confirmed`, `Meta_Match_Candidate`, `Date_Confirmed_Asset_Pending`, `Asset_Without_Post` y `Needs_Manual_Review`. Un hash visual o un OCR nunca debe crear un CNT por sí solo; la creación requiere evidencia conjunta de asset, publicación y relación editorial.

Para junio, el índice inicial tendría 196 filas de imagen. El caso `260724` demostraría el flujo completo: hash/OCR y composición visual apuntan al asset, el dataset aporta el Meta ID y fecha, y el inventario enlaza la relación como `CNT-068`.

## Reporte incremental recomendado

El reporte diario no debería volver a analizar toda la carpeta. Debe leer el índice existente, consultar solo cambios desde el último cursor y producir una tabla compacta con nuevos assets, nuevos matches, publicaciones con fecha confirmada, pendientes de evidencia y relaciones CNT que requieren revisión.

Si no hay cambios, el resultado debe ser `No new evidence` y no generar un análisis visual completo. Si aparece un archivo nuevo o cambia un asset, solo esa fila entra al análisis. El reporte también puede consumir el ledger de publicaciones, pero debe respetar la limitación actual de Meta: las métricas lifetime y las capturas históricas no son snapshots 24/72h.

## Opciones operativas

| Enfoque | Ventajas | Coste operativo | Complejidad |
|---|---|---:|---|
| Revisión manual bajo demanda | Cero scheduler; máxima revisión humana; adecuado para lotes pequeños. | Bajo por ejecución, alto si crece el volumen. | Baja |
| Índice inicial + reporte incremental cada 24 horas | Evita reanalizar assets; detecta cambios y deja un resumen diario. | Una ejecución diaria; consume créditos si se ejecuta como sesión completa. | Media |
| Índice persistente + proceso determinista de cambios | Actualiza hashes/metadatos sin despertar una sesión completa; escala mejor y puede generar el reporte diario. | Requiere un servicio persistente y configuración inicial. | Alta |

Para el tamaño actual de Universe Sent Me, la alternativa equilibrada es construir primero el índice visual de junio y ejecutar el reporte **bajo demanda o cada 48 horas**, alineado con la cadencia P0. Un reporte diario solo tiene sentido cuando haya publicaciones nuevas o cambios frecuentes en Drive; no aporta valor si únicamente se vuelve a confirmar la misma carpeta.

## Reglas de seguridad

El índice no debe mover ni copiar archivos de Drive. Debe guardar únicamente metadatos, hashes, OCR y referencias. La detección de una coincidencia será candidata hasta que exista una combinación verificable de filename/Drive ID, Meta ID y fecha o caption. `260583` permanece prohibido; los estados históricos deben preservarse; y ningún reporte puede convertir un snapshot lifetime en métrica 24/72h.

## Resultado de la reconciliación visual de top posts de junio

El 17 de agosto se revisaron visualmente los cinco top posts de junio directamente en Facebook y se compararon contra los 196 assets indexados de `06 Junio`. Se confirmó que la evidencia visual directa es más fuerte que el caption o la similitud temática. El único asset de junio previamente cerrado permanece como `260724` → `CNT-068` para `Polvo de estrellas` / `✨✨✨`.

La evidencia adicional de la carpeta `08 Agosto` resolvió los cinco casos que parecían pendientes. Los archivos habían sido movidos desde la carpeta histórica de junio durante la programación de reuse y por eso no aparecían en el lote local original de `06 Junio`. Las relaciones confirmadas son: `2607792` → `CNT-069` para `El gato: 😧`; `2607794` → `CNT-070` para `a ver... a ver... 🤨`; `260733` → `CNT-071` para `yo Aura Fuerte 😏`; `2607825` → `CNT-072` para `Me da miedo ser el malo de la historia...`; y `260735` → `CNT-073` para `🤡`. La confirmación conjunta usa la composición visual de Facebook, filename exacto, Drive ID, Meta ID y el manifiesto MOVE_ONLY. El layer `Historical_Asset_Performance.csv` conserva las métricas históricas sin mezclarlas con 24/72h.

## Estado real: recopilación de junio en curso

La auditoría confirma que junio ya tiene un núcleo histórico utilizable para el Growth OS: seis publicaciones individuales con Meta ID, asset y CNT reconciliados (`CNT-069` a `CNT-073`), además de `260724` → `CNT-068`, que conserva su snapshot histórico observado. Sin embargo, **junio no está cerrado**. Los 196 assets indexados representan una fuente de evidencia publicada que debe seguir cruzándose con Meta, Drive y los registros históricos antes de concluir el análisis.

El objetivo correcto es recuperar toda la información disponible de los assets que sí fueron publicados, no reconciliar ciegamente cada archivo de la carpeta. Para cada asset publicado se debe intentar obtener, en este orden, `Asset_Ref`, filename exacto, Drive ID, Meta ID, fecha, caption, formato, personajes, métricas lifetime y cualquier snapshot o comentario disponible. Los assets sin relación confirmada se mantienen como pendientes, no como descartados.

Junio y julio deben analizarse juntos como los meses de mejor referencia histórica identificados hasta ahora. La comparación posterior deberá usar sus datos reales para alimentar la Biblia y el Growth OS, sin mezclar snapshots lifetime con métricas 24/72h ni crear CNT por similitud temática.

## Cola exhaustiva de recopilación de junio

El dataset histórico contiene **230 publicaciones de junio**. Se generó `2026-08-17_Cola_Reconciliacion_Assets_Junio.csv`, ordenada por interacciones lifetime, para no limitar el análisis a los cinco top posts. Actualmente seis publicaciones ya están reconciliadas y quedan 224 en estado `Needs_Asset_Match`. La cola conserva Meta ID, fecha, caption, reacciones, comentarios, shares e interacciones, y define como siguiente evidencia el cruce visual con Drive/07 Junio y las carpetas operativas derivadas de movimientos `MOVE_ONLY`.

La prioridad de trabajo será descendente por interacciones. El siguiente lote recomendado comienza con `No sean asi.. 😆` (1,181 interacciones), `😏` del 29 de junio (1,069), `😎` del 11 de junio (924), `o pedir follows 🫣` (547) y los demás posts por encima de 500 interacciones. Así se recupera primero la información de mayor valor para la Biblia, sin abandonar después el resto de los assets que sí tengan evidencia publicada.

## Próximo paso propuesto

El siguiente lote debe ampliar la recopilación de junio usando los mismos principios que funcionaron con julio: localizar los assets publicados por `Asset_Ref`, revisar carpetas operativas derivadas de movimientos `MOVE_ONLY`, cruzar con Meta y registrar cada evidencia. Se priorizarán los posts de mayor rendimiento y después los assets publicados restantes con señales disponibles. El índice visual seguirá siendo persistente, pero no se considerará un cierre hasta completar la recuperación razonable de la información publicada.

No se crea ningún scheduler con este documento. La propuesta requiere aprobación antes de automatizar ejecuciones recurrentes.
