---
title: "Consentimiento y controles del piloto real privado de shadow ledger — Universe Sent Me"
purpose: "Proponer el alcance, retención, protección y rollback de una muestra real mínima en el shadow ledger privado antes de cualquier inserción de observaciones no sintéticas."
status: Draft
created: 2026-08-25
updated: 2026-08-25
version: "1.0"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-25_Shadow_Ledger_Privado_Append_Only_USM.md"
  - "Operations/Automation/2026-08-25_Esquema_Normalizacion_Determinista_Multicanal_USM.md"
  - "Operations/Automation/2026-08-25_Guia_Piloto_Local_API_Oficial_Metricas_USM.md"
  - "GrowthOS/todo.md"
organization: "Operations/Automation"
---

# Consentimiento y controles del piloto real privado de shadow ledger — Universe Sent Me

## Estado y propósito

Este documento propone los controles de un piloto de observaciones **reales pero privadas** en el shadow ledger local de Universe Sent Me. No otorga autorización por sí mismo: requiere confirmación explícita de Fernando sobre los controles de la sección 3. No habilita source of truth canónica, Google Sheets, GitHub, OmniRoute, cron, APIs de escritura, análisis por IA o uso de otras marcas.

> **Principio:** el objetivo es comprobar integridad append-only e idempotencia con datos reales mínimos, no construir un dataset, evaluar contenido ni automatizar decisiones.

## Alcance técnico propuesto

| Dimensión | Propuesta de límite | Excluido de forma estricta |
|---|---|---|
| Marca y cuentas | Solo Universe Sent Me; cuentas ya validadas en TikTok, YouTube, Facebook e Instagram. | Bam in a Can, Firma Bordados, clientes, cuentas personales o ambiguas. |
| Muestra | Máximo 4 observaciones: una métrica nativa no financiera por plataforma. | Lotes masivos, publicaciones completas, cohortes o datos de terceros. |
| Métricas | TikTok `views_native`; YouTube `views_native` de periodo cerrado; Facebook `reactions_native`; Instagram `likes_native`. | Monetización, reach/impressions incompatibles, métricas derivadas, comentarios y texto. |
| Contenido privado del ledger | ID nativo mínimo, fecha publicada, hora observada, métrica, valor, disponibilidad, fuente sanitizada y hash de evidencia. | Captions, títulos, URLs, paths, raw, tokens, handles, personas, importes financieros o respuestas de API. |
| Ejecución | Un único comando local con confirmación interactiva de alcance. | Cron, ejecución silenciosa, procesos de fondo o automatización de reintento. |

La mezcla de plataformas no se agregará ni comparará: cada observación conserva su `platform`, `window_type` y `comparability_tier` original. El piloto no crea rankings, hipótesis, conclusiones editoriales ni vistas derivadas.

## Protección, retención y recuperación propuestas

| Control | Propuesta | Condición de bloqueo |
|---|---|---|
| Ubicación | `~/.local/share/usm-metrics/shadow-ledger/normalized_metric_observations.shadow.jsonl`. | No se ejecuta si la ruta no tiene permisos `0700`/`0600`. |
| Cifrado de disco | El usuario debe confirmar que el disco local de Xubuntu está cifrado antes de insertar datos reales. | Si no está cifrado o no se sabe, el piloto permanece sintético. |
| Respaldo | No se habilita respaldo automático, sincronización cloud ni copia a Drive/GitHub. | Cualquier backup requiere un gate separado. |
| Retención | Máximo 30 días desde la primera inserción real, seguido de revisión humana. | No hay borrado automático ni retención indefinida aprobada. |
| Reconstrucción | Solo desde evidencia fuente local existente y el normalizador versionado; el proceso se documenta pero no se ejecuta de forma automática. | No se reconstruye si falta evidencia, hash o versión de normalizador. |
| Rollback | No existe mutación o borrado automático. Se puede crear un nuevo ledger vacío después de archivar localmente el anterior bajo aprobación humana. | Ningún script elimina eventos históricos. |

## Confirmaciones requeridas para activar G-NORM-4R

Fernando debe confirmar todas las siguientes condiciones antes de que exista un script de inserción real:

1. Aprueba el límite de **cuatro observaciones reales**, una por plataforma y con las métricas indicadas.
2. Confirma que Xubuntu usa cifrado de disco o que decide no continuar hasta activarlo.
3. Aprueba retención máxima de **30 días**, sin respaldo automático ni sincronización cloud.
4. Acepta que rollback significa detener el piloto y crear una nueva cadena de ledger bajo aprobación, no reescribir o borrar eventos existentes.
5. Confirma que los datos permanecerán exclusivamente en Xubuntu y no se enviarán a GitHub, Sheets, OmniRoute, Drive ni herramientas de IA.

Una vez confirmadas, se actualizará el estado a `Active` para el único propósito del piloto G-NORM-4R. La autorización será granular y no se extenderá a inserciones posteriores, volúmenes mayores, datos financieros o materialización canónica.

## Referencias

[1] [Shadow ledger privado append-only](2026-08-25_Shadow_Ledger_Privado_Append_Only_USM.md)

[2] [Esquema determinista multicanal](2026-08-25_Esquema_Normalizacion_Determinista_Multicanal_USM.md)

[3] [Guía del piloto local de APIs oficiales](2026-08-25_Guia_Piloto_Local_API_Oficial_Metricas_USM.md)
