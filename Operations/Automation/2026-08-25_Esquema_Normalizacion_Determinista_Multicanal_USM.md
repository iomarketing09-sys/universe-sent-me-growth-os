---
title: "Esquema de normalización determinista multicanal de métricas — Universe Sent Me"
purpose: "Definir una estructura auditable que conserve métricas nativas de TikTok, YouTube, Facebook e Instagram, permita construir vistas derivadas sin falsa equivalencia y mantenga las fuentes, evidencias y decisiones humanas separadas."
status: Review
created: 2026-08-25
updated: 2026-08-25
version: "1.4"
author: "Manus AI"
related_documents:
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
  - "GrowthOS/08_00_Metricas_Baseline_Plataformas.md"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
  - "Operations/Automation/2026-08-25_Guia_Piloto_Local_API_Oficial_Metricas_USM.md"
  - "Operations/Automation/2026-08-25_Shadow_Ledger_Privado_Append_Only_USM.md"
  - "Operations/Production/2026-08-23_Diseno_Asistencia_Metricas_y_Respuestas_OmniRoute.md"
  - "GrowthOS/todo.md"
organization: "Operations/Automation"
---

# Esquema de normalización determinista multicanal de métricas — Universe Sent Me

## 1. Decisión de diseño

Universe Sent Me necesita una capa común para consultar métricas de TikTok, YouTube, Facebook e Instagram, pero **no una métrica universal** que borre las diferencias de definición, ventana, formato o semántica de las plataformas. El diseño propuesto normaliza identidad, procedencia, ventana, disponibilidad y unidades; conserva los contadores nativos como hechos independientes; y calcula una métrica derivada solamente cuando su fórmula, componentes y denominador sean explícitos.

> **Regla central:** una fila normalizada expresa una observación reproducible, no una verdad creativa, un ranking ni una recomendación. Las observaciones de vida, diarias, de intervalo y de ventana exacta no se sustituyen entre sí.

El diseño cubre exclusivamente `brand = Universe Sent Me`. Bam in a Can, Firma Bordados, clientes, cuentas ambiguas y datos de terceros quedan fuera antes de leer, transformar o agregar. No se activa por este documento un cron, una hoja derivada, un ledger nuevo, una escritura canónica ni un envío a OmniRoute.

## 2. Principios no negociables

| Principio | Regla determinista |
|---|---|
| **Fuente primero** | Conservar plataforma, sistema fuente, definición nativa y hora de observación antes de calcular cualquier agregado. |
| **Sin conversión implícita** | `views`, `reach`, `impressions`, `engaged_views` y `video_views` permanecen separados aunque tengan nombres parecidos. |
| **Ausencia explícita** | `null`, `not_available`, `missing_field`, `not_authorized`, `not_applicable` y `source_error` tienen significados distintos; ninguno equivale a cero. |
| **Ventana visible** | Todo contador lleva `window_type`; no se comparan acumulados de vida con actividad diaria, E24/E72 o periodos cerrados sin una etiqueta de comparabilidad. |
| **Append-only** | La normalización agrega observaciones o correcciones con relación de supersedencia; nunca sobrescribe la evidencia previa. |
| **Identidad no inferida** | Un `Concept_ID`, `CNT_ID`, personaje, hook o experimento solo se adjunta cuando ya existe vínculo explícito en los ledgers. |
| **Evidencia privada** | El archivo crudo, token, ruta local, URL privada y respuesta completa permanecen en Xubuntu. GitHub recibe, únicamente tras gate futuro, filas normalizadas y referencias sanitizadas. |
| **IA aislada** | OmniRoute recibe solo agregados revisados por cohorte, sin IDs nativos, filas crudas, datos financieros detallados, handles, URLs o evidencia. |

## 3. Modelo lógico de tres capas

```text
Evidencia privada local por fuente
    → Extracto tipado por plataforma
        → Observación normalizada append-only
            → Vista derivada por plataforma/cohorte
                → Brief agregado y sanitizado para OmniRoute (Draft)
```

| Capa | Unidad | Ubicación prevista | Qué puede contener | Qué no puede contener |
|---|---|---|---|---|
| **Evidencia fuente** | Respuesta o captura recuperada | `~/.local/share/usm-metrics/evidence/` | Respuesta oficial, IDs necesarios, hora, errores técnicos. | GitHub, Google Sheets, OmniRoute o credenciales. |
| **Extracto tipado** | Registro transformado por un adapter de plataforma | Memoria local durante el run o artefacto temporal privado. | Campos nativos validados y su disponibilidad. | Inferencias editoriales, totales cruzados o textos de contenido. |
| **Observación normalizada** | Una métrica para una publicación/cuenta y una ventana | Futuro `Normalized_Metric_Observation_Log` append-only, sujeto a aprobación. | Identidad mínima, métrica, valor, unidad, ventana, fuente, calidad y hash de evidencia. | Raw, tokens, captions, mensajes, URLs privadas, PII o interpretaciones IA. |
| **Vista derivada** | Cohorte de observaciones válidas | Futuro reporte o pestaña de consulta reconstruible. | Medianas, cobertura, distribución y limitaciones por plataforma. | Corrección de los hechos canónicos o mezcla de plataformas como audiencia única. |

El `Metrics_Snapshot_Log.csv` vigente mantiene su propósito contractual Meta E0/E24/E72. Este esquema no lo reemplaza ni lo reutiliza para almacenar activity diaria de YouTube, snapshots lifetime de TikTok o media de Instagram. Si se aprueba materialización, el nuevo ledger tendrá nombre, validación y gate propios.

## 4. Granularidad y llaves deterministas

La unidad base será una observación larga, no una fila ancha con decenas de columnas opcionales:

> `una métrica × una publicación o cuenta × una ventana × una hora de lectura × una fuente`

| Campo | Tipo | Regla |
|---|---|---|
| `observation_key` | string | `SHA-256` de los componentes estables de la observación. |
| `transform_run_id` | string | Identificador único y reproducible del run; no contiene token ni ruta privada. |
| `normalizer_version` | string | Versión semántica de la regla que produjo la fila. |
| `brand` | enum | Debe ser exactamente `Universe Sent Me`. |
| `platform` | enum | `facebook`, `instagram`, `tiktok` o `youtube`. |
| `entity_scope` | enum | `content`, `channel` o `account`; no se mezclan en la misma cohorte. |
| `platform_content_id` | string/null | ID nativo para deduplicar; obligatorio si `entity_scope = content`. |
| `publication_ref` | string/null | Relación a `Publication_Log` solo si existe explícitamente. |
| `concept_id`, `cnt_id`, `experiment_id`, `hypothesis_id` | string/null | Solo enlaces ya verificados; `null` es preferible a una asociación probable. |
| `metric_name` | enum | Nombre canónico de un solo contador o medición nativa. |
| `metric_value` | decimal/null | Valor sin redondeo destructivo; `null` si no existe o no es aplicable. |
| `metric_unit` | enum | `count`, `minutes`, `seconds`, `percentage`, `currency` o `ratio`. |
| `metric_definition` | string | Definición fuente y componentes cuando sea derivada. |
| `window_type` | enum | Semántica temporal obligatoria descrita en la sección 5. |
| `window_start_utc`, `window_end_utc` | timestamp/null | Obligatorios para actividad diaria, intervalo o ventana exacta; opcionales en lifetime. |
| `published_at_utc`, `observed_at_utc` | timestamp/null | Fecha nativa de publicación y hora de recuperación, sin inventar ninguna. |
| `source_system`, `source_endpoint` | enum/string | API y endpoint o reporte origen; no token, URL con query ni ruta local. |
| `source_schema_version` | string/null | Versión de API o adapter conocida. |
| `availability_status` | enum | Estado de disponibilidad, nunca deducido del valor. |
| `availability_reason` | string/null | Motivo corto y codificado del estado. |
| `comparability_tier` | enum | Límite de uso analítico definido en la sección 7. |
| `evidence_fingerprint` | string | Hash del artefacto local, no su ruta ni su contenido. |
| `row_status` | enum | `valid`, `partial`, `rejected`, `deferred` o `superseded`. |
| `supersedes_observation_key` | string/null | Solo para una corrección posterior append-only. |

La llave de idempotencia será:

```text
SHA-256(
  brand | platform | entity_scope | platform_content_id |
  metric_name | window_type | window_start_utc | window_end_utc |
  observed_at_utc | source_system | normalizer_version
)
```

Una llave idéntica es un duplicado y se omite. Si una fuente entrega una corrección posterior para la misma observación, se agrega una nueva fila con `supersedes_observation_key`; la fila anterior permanece como evidencia y pasa a `row_status = superseded` solo mediante un validador explícito.

## 5. Ventanas y estados de disponibilidad

| `window_type` | Uso permitido | Regla de comparación |
|---|---|---|
| `lifetime_at_capture` | Contador acumulado visible cuando se leyó. | Solo descriptivo o comparable entre publicaciones de madurez definida; no es delta. |
| `daily_activity` | Actividad agregada de un día de fuente, como Analytics de YouTube. | No sumar snapshots lifetime del mismo video ni mezclar con `lifetime_at_capture`. |
| `period_total` | Total de una consulta cerrada con fecha de inicio y fin, como Analytics de YouTube por video en un rango. | Solo comparar con la misma definición y rango; no etiquetar como actividad diaria. |
| `interval_delta` | Diferencia calculada entre dos observaciones válidas de la misma métrica. | Requiere mismo contenido, fuente, definición y límites temporales contiguos. |
| `exact_window` | E0/E24/E72 u otra ventana contractual con tolerancia aprobada. | Comparable dentro de plataforma, formato y cohorte cuando la ventana coincide. |
| `observed_cut` | Corte operativo de publicaciones maduras o modificadas. | Descriptivo; no se presenta como una ventana exacta. |
| `historical_snapshot` | Dataset anterior con metodología conocida. | Solo contexto; no mezcla con capturas locales nuevas sin reconciliación. |

| `availability_status` | Significado | `metric_value` |
|---|---|---|
| `available` | La fuente devolvió un valor válido. | Número. |
| `not_available` | La fuente consultada no expuso el campo para esa entidad o tipo de media. | `null`. |
| `missing_field` | El campo esperado no llegó en una respuesta que sí debía contenerlo. | `null`. |
| `not_authorized` | El token o permisos no permiten la lectura. | `null`. |
| `not_applicable` | La métrica no corresponde al tipo de contenido. | `null`. |
| `source_error` | Error técnico explícito de fuente. | `null`. |
| `deferred` | La lectura no se ejecutó o no terminó. | `null`. |

Los porcentajes nativos se preservan sin recorte. Por ejemplo, `average_view_percentage` de YouTube puede superar 100 por repeticiones; ese valor no es un error ni una tasa de finalización de TikTok o Instagram.

## 6. Taxonomía de métricas: común sin falsa equivalencia

### 6.1 Nombres canónicos permitidos

| Dominio | Métricas normalizadas | Regla |
|---|---|---|
| Exposición | `views_native`, `engaged_views_native`, `reach_native`, `impressions_native` | Nunca se sustituyen entre sí. |
| Acciones | `reactions_native`, `likes_native`, `comments_native`, `shares_native`, `saves_native`, `favorites_native`, `reposts_native` | Cada acción conserva el nombre y la definición de origen. |
| Video | `average_watch_time_seconds_native`, `average_view_percentage_native`, `completion_rate_native` | Solo comparar el mismo nombre, denominador y plataforma. |
| Audiencia | `followers_gained_native`, `subscribers_gained_native`, `subscribers_lost_native` | No combinar followers y subscribers como un mismo total. |
| Monetización | `estimated_revenue_preliminary`, `monetized_playbacks_native` | `financial_restricted = true`; nunca se envía importe a OmniRoute sin aprobación financiera separada. |
| Derivadas controladas | `actions_available_sum`, `actions_per_reach`, `actions_per_view`, `interval_delta` | Siempre incluyen fórmula, componentes, denominador y estado de cobertura. |

`engagement` no será una columna numérica universal. Si una fuente ofrece `native_engagement`, se almacena con su definición exacta. Si se necesita una suma de acciones, se generará `actions_available_sum` y declarará el conjunto de componentes empleado, por ejemplo `facebook: reactions_native + comments_native + shares_native`.

Una métrica derivada será `null` si falta un componente obligatorio o si el denominador es cero, ausente, incompatible o de otra ventana. El normalizador no compensará con cero un `saves_native` no disponible de Instagram ni un `reach_native` inexistente de YouTube.

### 6.2 Mapeo inicial por plataforma validada

| Plataforma | Campos fuente validados | Mapeo normalizado | Limitación que permanece visible |
|---|---|---|---|
| Facebook | `reactions`, `comments`, `shares`, `created_time`, `is_published` | `reactions_native`, `comments_native`, `shares_native`, `published_at_utc` | Son contadores lifetime al corte; shares puede faltar. |
| Instagram | `like_count`, `comments_count`, `saved_count`, `shares_count`, `total_views_count`, `reposts_count`, tipo y timestamp | `likes_native`, `comments_native`, `saves_native`, `shares_native`, `views_native`, `reposts_native`, tipo editorial nativo | `saved_count` y `total_views_count` pueden no estar disponibles por media. |
| TikTok | `view_count`, `like_count`, `comment_count`, `share_count`, `create_time` de Display API | `views_native`, `likes_native`, `comments_native`, `shares_native`, `published_at_utc` | No expone reach, favoritos, retención ni finalización en la ruta oficial actual. |
| YouTube | `views`, `engagedViews`, `likes`, `comments`, `shares`, `estimatedMinutesWatched`, `averageViewDuration`, `averageViewPercentage`, `subscribersGained` | `views_native`, `engaged_views_native`, `likes_native`, `comments_native`, `shares_native`, `estimated_watch_minutes_native`, `average_watch_time_seconds_native`, `average_view_percentage_native`, `subscribers_gained_native` | La salida de Analytics por rango debe usar `period_total` con inicio y fin reales; monetización puede ser `not_available`. |

## 7. Niveles de comparabilidad

| Nivel | Condición | Uso permitido | Uso prohibido |
|---|---|---|---|
| `C0_not_comparable` | Definición, ventana, denominador o formato no coinciden. | Mostrar de forma aislada con limitación. | Rankings, promedios cruzados o hipótesis. |
| `C1_same_platform_observed` | Misma plataforma y métrica, pero contadores lifetime con edades no alineadas. | Revisión operativa descriptiva. | Veredicto experimental o delta. |
| `C2_same_platform_cohort` | Misma plataforma, tipo, definición y cohorte de madurez acordada. | Mediana, rango y comparación direccional. | Causalidad o extrapolación interplataforma. |
| `C3_exact_window` | Misma plataforma, métrica, formato y ventana contractual válida. | Evaluación de una hipótesis definida. | Mezclar con activity diaria o lifetime. |
| `C4_cross_platform_directional` | Misma pieza o cohorte con campos semánticamente análogos, pero definiciones nativas distintas. | Matriz cualitativa de distribución y cobertura. | Sumar audiencias, elegir un ganador absoluto o calcular una tasa universal. |

El normalizador asigna el nivel más conservador. Una fila sin `published_at_utc`, sin origen o sin `window_type` queda `rejected` o `deferred`, no se asciende a `C1` por intuición.

## 8. Validaciones obligatorias

| ID | Validación determinista | Resultado ante fallo |
|---|---|---|
| `NORM-01` | `brand` debe ser exactamente Universe Sent Me. | `rejected`; no se lee ni transforma. |
| `NORM-02` | Plataforma permitida y cuenta objetivo confirmada. | `rejected`. |
| `NORM-03` | `platform_content_id` obligatorio para entidades de contenido. | `deferred`; no inventar identidad. |
| `NORM-04` | `observed_at_utc`, fuente, definición y ventana obligatorias. | `rejected`. |
| `NORM-05` | Valor numérico no negativo cuando esté disponible; porcentaje no se recorta. | `rejected` o `partial` con evidencia. |
| `NORM-06` | Todo valor `null` debe llevar estado de disponibilidad distinto de `available`. | `rejected`. |
| `NORM-07` | La métrica derivada declara componentes, fórmula y denominador. | `rejected`. |
| `NORM-08` | No mezclar `daily_activity`, `lifetime_at_capture`, `exact_window` u `observed_cut` en una misma agregación. | `rejected`. |
| `NORM-09` | `evidence_fingerprint` presente y sin ruta local o token. | `rejected`. |
| `NORM-10` | La clave de observación no duplica una fila existente; correcciones declaran supersedencia. | `duplicate_skip` o `partial`. |
| `NORM-11` | Importe monetario marcado `financial_restricted`. | `rejected` para briefs OmniRoute y vistas no financieras. |
| `NORM-12` | No existe texto de publicación, caption, comentario, URL o dato personal. | `rejected` y revisión de sanitización. |

## 9. Ejemplos sintéticos de filas normalizadas

Los ejemplos siguientes son deliberadamente sintéticos y no representan publicaciones reales, cuentas, resultados ni IDs de Universe Sent Me.

| Campo | Ejemplo Facebook | Ejemplo Instagram no disponible | Ejemplo YouTube diario |
|---|---|---|---|
| `platform` | `facebook` | `instagram` | `youtube` |
| `entity_scope` | `content` | `content` | `content` |
| `metric_name` | `shares_native` | `saves_native` | `views_native` |
| `metric_value` | `12` | `null` | `48` |
| `window_type` | `lifetime_at_capture` | `lifetime_at_capture` | `daily_activity` |
| `availability_status` | `available` | `not_available` | `available` |
| `metric_definition` | `Meta shares.count at capture` | `Meta saved_count field absent for media` | `YouTube Analytics views for requested day` |
| `comparability_tier` | `C1_same_platform_observed` | `C0_not_comparable` | `C0_not_comparable` |
| `row_status` | `valid` | `partial` | `valid` |

## 10. Destino de cada resultado y privacidad

| Destino | Puede recibir | No puede recibir |
|---|---|---|
| Evidencia privada Xubuntu | Respuestas oficiales, IDs necesarios, errores técnicos y token local protegido. | GitHub remoto, modelos, otras marcas. |
| Ledger normalizado futuro | Filas validadas, hashes de evidencia, disponibilidad y procedencia. | Tokens, raw, captions, comentarios, rutas privadas o datos financieros no aprobados. |
| Google Sheets derivada futura | Agregados reconstruibles por plataforma/cohorte y calidad de datos. | Corrección manual de hechos, raw o secretos. |
| OmniRoute local | Brief agregado y sanitizado de una cohorte `C2` o `C3`, más limitaciones. | IDs nativos, filas crudas, PII, URLs, tokens, comentarios íntegros, importes monetarios exactos. |

## 11. Gates de implementación posteriores

| Gate | Entregable | No autorizado aún |
|---|---|---|
| `G-NORM-1` | Revisión humana de este documento y de los mappings de plataforma. | Crear o llenar un ledger nuevo. |
| `G-NORM-2` | Normalizador local en modo `dry-run` con un registro sintético por plataforma y validaciones `NORM-01` a `NORM-12`. | Leer masivamente raw o escribir artefactos canónicos. |
| `G-NORM-3` | Piloto local privado con una muestra real limitada por plataforma y reporte de cobertura. | Google Sheets, cron, OmniRoute o actualización de hipótesis. |
| `G-NORM-4` | Aprobación explícita del nombre del ledger, esquema CSV/JSON, política de append-only e idempotencia. | Materializar observaciones canónicas. |
| `G-NORM-5` | Vista derivada reconstruible y brief sanitizado de cohorte madura. | Automatización productiva o publicación. |

Antes de `G-NORM-4` requerirán actualización coordinada `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`, `GrowthOS/08_00_Metricas_Baseline_Plataformas.md`, `GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md`, `GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md`, `Operations/Automation/2026-08-25_Guia_Piloto_Local_API_Oficial_Metricas_USM.md` y `GrowthOS/00_01_Changelog_GrowthOS.md`. Ningún script podrá materializar filas canónicas hasta que ese gate sea aprobado.

### Resultado de G-NORM-3

El piloto privado procesó en memoria un máximo de ocho registros fuente por plataforma a partir de evidencia local ya existente. Facebook procesó 8 de 25 registros fuente y normalizó 24 observaciones: 22 válidas y 2 parciales por shares no disponibles. Instagram procesó 8 de 25 y normalizó 48 observaciones: 37 válidas y 11 parciales; `saves_native` quedó no disponible en toda la muestra y `views_native` solo estuvo disponible en 5 de 8 media. TikTok procesó 8 de 9 registros y normalizó 32 observaciones válidas. YouTube procesó 8 de 8 filas de rendimiento y normalizó 72 observaciones válidas; monetización quedó totalmente excluida.

No hubo observaciones rechazadas ni duplicados en el piloto. El reporte no expuso IDs, textos, URLs, valores nativos, rutas, tokens, hashes o monetización, y el proceso no escribió evidencia, datos normalizados, ledgers, Google Sheets, OmniRoute ni cron. La cobertura valida los adaptadores y reglas de disponibilidad, pero no convierte el diseño en `Active`: G-NORM-4 requeriría una autorización separada para un shadow ledger privado append-only.

### Preparación de G-NORM-4

La implementación sintética de G-NORM-4 está descrita en `2026-08-25_Shadow_Ledger_Privado_Append_Only_USM.md`. `shadow_ledger_private.py` solo acepta fixtures con `synthetic = true`, inicializa un archivo JSONL privado con evento genesis y agrega observaciones completas como eventos inmutables. La batería sintética confirmó inserción inicial, repetición idempotente, rechazo de colisión no supersedida y corrección append-only. Esta preparación no activa la inserción de datos reales ni altera la condición `Review` del esquema.

### Cobertura sintética ampliada

La batería integrada `validate_synthetic_boundary_suite.py` amplió la cobertura de contrato. El normalizador preservó un porcentaje nativo de YouTube superior a 100 sin recorte, una observación de periodo cerrado `C3_exact_window`, una duración nativa en minutos y una ausencia válida de Instagram como parcial. El shadow ledger validó además el rechazo de una supersedencia que apunta a una observación inexistente.

La suite bloqueó `socket.socket` durante la ejecución y confirmó `synthetic_boundary_suite_passed` con NORM-01 a NORM-12, cinco pruebas append-only, ledger temporal y cero escrituras canónicas. Este resultado aporta confianza a la capa sintética, pero no cambia el estado `Review`, no activa almacenamiento real y no autoriza reparación automática ante corrupción.

Como siguiente control de lectura, `validate_shadow_ledger_corruption_synthetic.py` generó inconsistencias exclusivamente sintéticas: JSONL malformado, secuencia sin genesis y referencia de supersedencia inexistente. `inspect_shadow_ledger_synthetic.py` las detectó sin modificar los bytes de los archivos temporales. No se habilita recuperación automática, reconstrucción de hechos ni materialización de datos reales.

## Referencias

[1] [Fuente maestra y ledgers del Growth OS](../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md)

[2] [Métricas baseline por plataformas](../../GrowthOS/08_00_Metricas_Baseline_Plataformas.md)

[3] [Guía del piloto local de APIs oficiales](2026-08-25_Guia_Piloto_Local_API_Oficial_Metricas_USM.md)

[4] [Diseño de asistencia de métricas y respuestas con OmniRoute](../Production/2026-08-23_Diseno_Asistencia_Metricas_y_Respuestas_OmniRoute.md)

[5] [Meta Page Feed Reference](https://developers.facebook.com/docs/graph-api/reference/page/feed/)

[6] [Meta Instagram Media Reference](https://developers.facebook.com/documentation/instagram-platform/reference/instagram-media)
