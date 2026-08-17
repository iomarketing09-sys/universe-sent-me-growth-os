---
title: "Índice visual de assets y reporte incremental de publicaciones"
purpose: "Definir una arquitectura persistente para analizar assets de Drive una sola vez y mantener reportes de publicaciones mediante actualizaciones incrementales, evitando búsquedas visuales completas repetidas."
status: "Review"
created: 2026-08-17
updated: 2026-08-17
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-17_Cruce_Assets_Junio_Meta_Top.md"
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

## Próximo paso propuesto

Construir el índice visual inicial de los 196 assets de junio, comenzando por dimensiones, hash visual y OCR. Después se revisarán primero los candidatos que tengan caption/fecha Meta y se actualizará solo la fila correspondiente. El reporte diario o de 48 horas se implementará únicamente después de validar el índice inicial y aprobar el formato del reporte.

No se crea ningún scheduler con este documento. La propuesta requiere aprobación antes de automatizar ejecuciones recurrentes.
