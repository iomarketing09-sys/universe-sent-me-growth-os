---
title: "Protocolo P0 de métricas comparables y veredictos"
purpose: "Definir cómo medir la prueba activa, comparar sus resultados y cerrar el ciclo de aprendizaje sin mezclar lifetime histórico, cortes observados ni canales."
status: "Active"
created: 2026-08-17
updated: 2026-08-23
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-15_ExperimentLog.csv"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "GrowthOS/08_00_Metricas_Baseline_Plataformas.md"
  - "Operations/Research/2026-08-15_Auditoria_General_Growth_OS.md"
  - "Operations/Research/2026-08-17_Prioridad_Siguientes_Pendientes_Growth_OS.md"
  - "Operations/Automation/2026-08-23_Diseno_Captura_Baseline_E0_E24_E72.md"
organization: "Operations/Research"
---

# Protocolo P0 de métricas comparables y veredictos

## Principio rector

El ciclo de aprendizaje se cierra por hipótesis, no por sensación ni por un post viral. Cada publicación debe conservar su timestamp de publicación, plataforma, tipo de contenido, estado nuevo/reuse, slot horario, Asset_Ref, Meta ID y evidencia de extracción.

> **Regla:** lifetime histórico sirve para contexto y descubrimiento; no se escribe en campos de 24/72 horas ni se usa como sustituto de snapshots temporales.

## Unidad de comparación

La unidad mínima es `una publicación en una plataforma`. Facebook e Instagram se analizan en tablas separadas. No se combinan posts con Reels, ni contenido nuevo con reuse, salvo que la hipótesis lo especifique y el informe muestre los estratos separados.

Cada publicación debe tener un registro de baseline cercano a la publicación y, cuando sea posible, snapshots a 24 y 72 horas. El punto de captura E0 es posterior a la confirmación de `is_published=true` y `created_time` real de Meta; la hora planeada no sustituye la hora efectiva. La especificación de ledger, tolerancias e idempotencia está en `Operations/Automation/2026-08-23_Diseno_Captura_Baseline_E0_E24_E72.md`. Si Meta no entrega un snapshot exacto, el registro se marca como `Corte_Observado` y queda fuera de la métrica contractual de 24/72 horas.

## Métricas

| Nivel | Métrica | Uso |
|---|---|---|
| Principal | `interacciones_24h = reacciones_24h + comentarios_24h + shares_24h` | Comparar rendimiento temprano por publicación |
| Principal secundaria | `interacciones_72h` | Medir acumulación temprana y persistencia |
| Difusión | `shares_24h`, `shares_72h`, `share_rate` | Medir transferencia social y potencial de etiquetado |
| Conversación | `comentarios_raíz_24h`, `replies_72h`, `comment_rate` | Medir conversación real sin contar respuestas propias como interés independiente |
| Control | `mediana_por_publicación` | Evitar que un viral domine la conclusión |
| Contexto | `promedio`, `p90`, `mínimo`, `máximo` | Describir dispersión, no decidir por sí solo |

La métrica principal del veredicto será la **mediana de interacciones por publicación**. El promedio se mostrará solo como contexto. Para hipótesis de difusión se utilizará la mediana de shares; para hipótesis comunitarias, la mediana de comentarios raíz y la proporción de posts con al menos un comentario sustantivo.

## Reglas de comparabilidad

Un registro puede entrar en una comparación estricta solo si cumple estas condiciones:

| Condición | Regla |
|---|---|
| Canal | Mismo canal; Facebook e Instagram nunca se mezclan |
| Ventana | Exactamente 24h o 72h desde publicación, con timestamp UTC y hora local |
| Métrica | Misma definición de interacción en todos los registros |
| Formato | Imagen, Reel y carrusel se comparan por estratos |
| Tipo | Nuevo, reuse y respuesta se mantienen identificables |
| Horario | Se usa hora local `America/Matamoros` |
| Estado | Solo `Publicado` entra en resultados; `Programada` no es resultado |
| Evidencia | Cada valor tiene timestamp de extracción y fuente |

Los registros con lifetime únicamente se conservan en una capa histórica. Los registros sin snapshot exacto se pueden incluir en un anexo descriptivo `Corte_Observado`, pero no en el cálculo principal.

## Hipótesis de la prueba activa

| Hipótesis | Comparación | Métrica principal | Señal esperada |
|---|---|---|---|
| H1: mayor frecuencia aumenta la oportunidad de éxito | Mediana por publicación del experimento vs baseline comparable | `mediana_interacciones_24h` y `mediana_shares_24h` | Mejora sin caída severa de conversación por pieza |
| H2: la mezcla 3 nuevos : 2 reuse mantiene rendimiento y reduce fatiga | Nuevo vs reuse, con slots y formato separados | Medianas 24h y 72h por tipo | Nuevo no cae por debajo de reuse; reuse conserva difusión |
| H3: media mañana y noche temprana son ventanas prioritarias | Slots 10–11, 13–14 y 19–21 | Mediana por slot | Una o más ventanas superan la baseline sin depender de un único viral |
| H4: potencial de etiquetado mejora shares | Alto/medio/bajo según taxonomía | Mediana de shares 24h/72h | Alto supera bajo dentro del mismo formato y tipo |

## Sistema de veredictos

El veredicto se asigna por hipótesis y no por publicación individual.

| Veredicto | Criterio |
|---|---|
| `Validada` | Dirección esperada, uplift de mediana de al menos 20%, mínimo 5 publicaciones comparables por celda y sin dependencia de un solo outlier |
| `Parcialmente validada` | Dirección esperada, uplift entre 10% y 19%, o muestra menor a 5 pero con evidencia consistente |
| `No validada` | Dirección contraria o uplift menor a 10% con muestra comparable suficiente |
| `Inconclusa` | Faltan snapshots exactos, hay confusión de canal/formato, o la muestra no permite comparar |
| `Invalidada por diseño` | El experimento no respetó la condición predefinida o se contaminó con publicaciones no aprobadas |

Los umbrales son reglas operativas de decisión, no una prueba causal. Cuando el tamaño de muestra lo permita, se añadirá intervalo bootstrap de la mediana; con muestras pequeñas se priorizará el lenguaje de señal o hipótesis.

## Estructura mínima del registro

Cada fila de `ExperimentLog` debe conservar `experiment_id`, `hypothesis_id`, `publication_id`, `CNT`, `Asset_Ref`, `platform`, `format`, `content_type`, `is_new_or_reuse`, `slot_local`, `published_at_utc`, `published_at_local`, `baseline_captured_at`, `snapshot_24h_at`, `snapshot_72h_at`, `reactions`, `comments_root`, `shares`, `interactions`, `window_status`, `source`, `extraction_timestamp`, `outlier_flag` y `notes`.

## Cierre del ciclo

El ciclo se cierra solo cuando cada hipótesis tiene una tabla de resultados, una nota de comparabilidad, un veredicto, una explicación de limitaciones y una decisión operativa. La decisión debe ser una de estas: mantener, ajustar, abandonar o repetir con mejor control.

Los resultados se incorporan al Growth OS como aprendizaje. No modifican automáticamente el canon. Cualquier cambio en la Biblia requiere revisión con Claude y aprobación explícita.

## Aplicación inmediata

Para la ola activa de Facebook, se debe registrar primero el estado real de cada publicación, capturar baseline cuando sea posible y ejecutar las lecturas agrupadas cada 48 horas. Las filas sin ventana exacta permanecerán como `Corte_Observado`. El P0 no debe cerrarse con los nueve registros del lote 15–16 como si fueran 24/72h exactas: ese lote puede alimentar análisis descriptivo, pero no un veredicto contractual.
