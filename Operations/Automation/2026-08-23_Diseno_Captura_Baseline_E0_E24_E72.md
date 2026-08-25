# Diseño de captura automática de baseline E0 y ventanas E24/E72

**Propósito:** Definir una implementación automática y trazable para capturar el baseline E0 de cada publicación de Facebook inmediatamente después de su publicación real, y usarlo para calcular ventanas comparables E24/E72 sin convertir acumulados lifetime en métricas temporales.

**Estado:** Review
**Fecha de creación:** 2026-08-23
**Última actualización:** 2026-08-25
**Versión:** 1.1
**Autor:** Manus AI (CGO)
**Organización:** `Operations/Automation/`
**Documentos relacionados:** `../Research/2026-08-17_Investigacion_Ventanas_Temporales_Meta.md`, `../Research/2026-08-17_Protocolo_P0_Metricas_y_Veredictos.md`, `../Research/2026-08-22_Reels_Metric_Instrumentation_Protocol.md`, `../../GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md`, `../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`, `../../GrowthOS/08_00_Metricas_Baseline_Plataformas.md`, `../Research/2026-08-15_Publication_Log.csv`, `../Research/2026-08-15_ExperimentLog.csv`, `../Research/Metrics_Snapshot_Log.csv`, `record_metrics_snapshot.py`, `validate_metrics_snapshot_ledger.py`, `../Research/2026-08-25_Metrics_Snapshot_Ledger_Activation_Evidence.json`, `../Research/2026-08-25_Instagram_Route_Smoke_Test.json`

---

## 1. Decisión metodológica

El problema de `Unavailable_No_Baseline` se resuelve hacia adelante capturando tres contadores acumulados del mismo objeto de Facebook: reacciones, comentarios y shares. La investigación del Growth OS ya fijó la fórmula contractual:

```text
E0  = reactions_0  + comments_0  + shares_0
E24 = reactions_24 + comments_24 + shares_24
E72 = reactions_72 + comments_72 + shares_72

Interacciones_24h = E24 - E0
Interacciones_72h = E72 - E0
```

El baseline se toma **después de confirmar la publicación real**, no cuando se crea una programación futura. La API de Pages devuelve un Page Post ID al publicar y permite consultar el feed con `created_time` e ID; para publicaciones programadas, el sistema debe esperar a que `is_published=true` antes de registrar E0. [1] [2]

> Un snapshot lifetime actual es evidencia del estado en el momento de la captura. Solo se convierte en E0, E24 o E72 cuando conserva `captured_at_utc`, `published_at_utc`, el ID nativo, la fuente, los contadores crudos y el estado de tolerancia correspondiente.

El diseño completo permanece en **Review**: no activa schedules, no modifica el publicador de Fernando y no autoriza publicaciones. El bloque P0 de ledger y captura reproducible quedó implementado de forma acotada el 2026-08-25, con `Metrics_Snapshot_Log.csv`, el módulo `record_metrics_snapshot.py` y su validador. El hook posterior a una publicación real, el worker E24/E72 y la automatización recurrente permanecen pendientes de integración y decisión operativa.

## 2. Punto de enganche en el sistema actual

El pipeline vigente ya recibe el ID de Meta y, después de confirmar la publicación, registra ID, fecha/hora, plataforma, estado y métricas iniciales en `Publication_Log.csv`. Ese momento es el punto de enganche correcto para generar un evento E0. [7]

El flujo debe distinguir dos situaciones:

| Situación | Acción E0 |
|---|---|
| Publicación inmediata vía Graph API | Confirmar el objeto con una lectura posterior; capturar E0 en la misma ejecución, usando `created_time` real de Meta. |
| Publicación programada vía Graph API | Registrar el post como pendiente de activación; no capturar E0 al programarlo. Un worker debe confirmar posteriormente `is_published=true` y entonces capturar E0. |
| Publicación manual fuera del script | Detectarla mediante Webhook `feed` o mediante una reconciliación frecuente del feed; confirmar el objeto y crear E0. Si ninguna fuente la detecta dentro de la tolerancia, marcar `E0_Missing`, no reconstruirlo retrospectivamente. |
| Reintento o ejecución duplicada | Consultar primero la clave idempotente `Meta_Post_ID + snapshot_type`; si ya existe un E0 válido, no capturar ni escribir otra fila canónica. |

El `Publication_Log.csv` continúa representando el hecho de publicación. El `ExperimentLog.csv` continúa representando aprendizaje y veredicto. Las capturas crudas y sus intentos deben vivir en un ledger separado para no convertir el ExperimentLog en una tabla de transporte.

## 3. Alternativas de implementación

Las siguientes rutas son viables. La tabla presenta primero la alternativa más ligera y después las que ofrecen mayor cobertura de publicaciones programadas y manuales.

| Approach | Tradeoffs | Cost | Setup Complexity |
|---|---|---|---|
| **A. Hook en el publicador + worker de activación** | Precisión alta para publicaciones inmediatas; aprovecha el script que ya recibe el ID. Para posts programados necesita un worker que revise cuándo `is_published` cambia a `true`. No cubre por sí sola posts manuales ajenos al publicador. | Infraestructura adicional mínima; depende de dónde se ejecute el publicador. | **Media:** añadir captura, ledger, reintentos y una revisión de posts programados. |
| **B. Servicio web alojado con cola de publicaciones y ventanas** | Cubre publicaciones inmediatas, programadas y manuales mediante una cola y reconciliación del feed. Puede ejecutar E0 en cuanto confirma `is_published=true` y E24/E72 por `target_at_utc`. Requiere secretos, almacenamiento operativo y sincronización controlada con GitHub. | Coste de alojamiento y uso del servicio; no se ha activado ni presupuestado una instancia. | **Media-alta:** API, worker, almacenamiento, locking, health checks y sync al repositorio. |
| **C. Webhook `feed` de Meta + worker de confirmación** | Reduce la latencia para detectar publicaciones manuales y cambios del feed. Meta documenta el campo `feed`, el `post_id`, `created_time` e `is_published`; requiere una app configurada, endpoint HTTPS, permisos `pages_manage_metadata`/`pages_show_list` e instalación de la app en la Página. El webhook no sustituye la lectura posterior de contadores ni la reconciliación de seguridad. [3] [4] | Coste de ejecución bajo a moderado; mayor coste de configuración, permisos y mantenimiento. | **Alta:** app Meta, verificación del endpoint, suscripción `feed`, deduplicación, reintentos y fallback. |
| **D. Comando local post-publicación + worker agrupado** | Es la alternativa de menor infraestructura. Fernando o Manus ejecutan un comando después de cada publicación; el worker existente captura E24/E72. No es completamente automático para posts manuales y depende de que el comando se ejecute. | Sin servicio adicional; coste operativo humano por publicación. | **Baja:** ledger, comando, validación y procedimiento escrito. |

La comparación no elige una ruta irreversible. La recomendación de diseño es comenzar por **A** para las publicaciones que ya pasan por el publicador, añadir el worker de activación para programadas y mantener **C** como ampliación cuando sea necesario cubrir publicaciones manuales sin intervención. Si se desea independencia del equipo local y crecimiento a varias cuentas, **B** es la arquitectura más completa, pero requiere una fase de despliegue separada.

## 4. Esquema propuesto del ledger de snapshots

Se propone crear `Operations/Research/Metrics_Snapshot_Log.csv` como ledger append-only, separado de `Publication_Log.csv` y `ExperimentLog.csv`. Su función es conservar una fila por captura y permitir que el sistema seleccione una captura canónica sin perder intentos fallidos o anomalías.

| Campo | Regla |
|---|---|
| `Snapshot_ID` | Identificador único de la captura o intento. Nunca se reutiliza. |
| `Logical_Key` | `Meta_Post_ID + Snapshot_Type`; identifica el objetivo lógico E0, E24 o E72. |
| `Publicacion_ID` | ID del hecho de publicación en `Publication_Log.csv`. |
| `Experiment_ID` | Experimento asociado, cuando exista. |
| `ID_Pieza` / `CNT` | Identidad editorial; no inferirla desde el caption. |
| `Plataforma` | Para este diseño, `Facebook`; otras plataformas quedan separadas. |
| `Cuenta_ID` | `1036844829507460`. |
| `Meta_Post_ID` | ID nativo del post padre. Obligatorio para una captura aceptada. |
| `Meta_Photo_ID` / `Reel_ID` | Identificadores auxiliares cuando apliquen; no reemplazan el Page Post ID. |
| `Published_At_UTC` | `created_time` confirmado por Meta, no la hora planeada. |
| `Published_At_Local` | Conversión documentada a `America/Matamoros`. |
| `Snapshot_Type` | `baseline_e0`, `snapshot_24h`, `snapshot_72h` o `observed_lifetime`. |
| `Target_At_UTC` | Para E0 es `Published_At_UTC`; para E24/E72 es `Published_At_UTC + 24/72h`. |
| `Captured_At_UTC` | Hora real de la lectura. Nunca sustituirla por la hora objetivo. |
| `Age_Seconds` | `Captured_At_UTC - Published_At_UTC`. |
| `Tolerance_Seconds` | Tolerancia aplicada a la clasificación de la captura. |
| `Window_Status` | `Valid_E0`, `Valid_24h`, `Valid_72h`, `Late`, `Missing`, `API_Error`, `Anomaly`. |
| `Reactions` | Conteo crudo del objeto en la captura. `null` si el campo no llegó. |
| `Comments` | Conteo crudo según la consulta aprobada. `null` si el campo no llegó. |
| `Shares` | Conteo crudo del objeto. `null` si el campo no llegó. |
| `Lifetime_Interactions` | Suma de los tres contadores solo si los tres están disponibles; no es una ventana. |
| `Delta_From_E0` | Vacío en E0; `E24 - E0` o `E72 - E0` únicamente cuando ambos snapshots son válidos. |
| `Source` | `Meta_Graph_API`, `Meta_Webhook_then_Graph`, `Windsor` u otra fuente aprobada. |
| `HTTP_Status` | Código HTTP de la lectura de contadores. |
| `Raw_Evidence_Path` | Ruta del JSON raw inmutable asociado al intento. |
| `Idempotency_Key` | Clave estable para impedir duplicados. |
| `Anomaly_Code` | `counter_decreased`, `missing_counter`, `id_mismatch`, `late_capture`, `none` u otro código explícito. |
| `Notes` | Contexto operativo, reintentos y decisión de inclusión/exclusión. |

Los campos `Interacciones_24h` e `Interacciones_72h` de los ledgers actuales solo se rellenan después de que el selector encuentre un `Valid_24h` o `Valid_72h`, un E0 válido y los tres contadores necesarios. Si un contador disminuye, la captura se conserva como `Anomaly`; no se oculta el delta negativo ni se reescribe el histórico.

## 5. Tolerancias propuestas para aprobación

Las tolerancias deben ser explícitas antes de operar. La propuesta inicial es conservadora:

| Evento | Objetivo | Tolerancia propuesta | Estado si queda fuera |
|---|---|---:|---|
| E0 | Inmediatamente después de `is_published=true` | 10 minutos posteriores a `created_time` | `E0_Late` hasta 60 min; después `E0_Missing` |
| E24 | `Published_At_UTC + 24h` | ±60 minutos | `Late_24h`; no llenar campo contractual sin aprobación |
| E72 | `Published_At_UTC + 72h` | ±60 minutos | `Late_72h`; no llenar campo contractual sin aprobación |

Estas cifras son una propuesta de diseño, no una regla ya aprobada. Si el objetivo del experimento exige una tolerancia más estrecha, el worker tendrá que ejecutarse con mayor frecuencia que la revisión agrupada actual cada 48 horas. Un proceso de pocas ejecuciones diarias no garantiza por sí solo que cada frontera de 24/72 quede dentro de ±60 minutos.

Para evitar polling intensivo mediante sesiones completas, la captura frecuente debe ejecutarse en un servicio persistente o en trabajos cron de un servicio web; no se debe crear una tarea de Manus por publicación. La investigación previa confirma que un batch reduce conexiones, pero no elimina el coste lógico de cada lectura. [5]

## 6. Flujo detallado

### 6.1 Evento de publicación

1. El publicador crea o publica el contenido y recibe el ID de Meta. La respuesta del endpoint es solo una confirmación inicial.
2. El sistema ejecuta una lectura de verificación del post: `id`, `created_time`, `is_published` y `permalink_url` cuando estén disponibles.
3. Si `is_published=true`, captura inmediatamente los contadores con la consulta mínima aprobada:

```text
created_time,
reactions.limit(0).summary(true),
comments.limit(0).summary(true),
shares
```

4. Escribe el raw de la respuesta y una fila append-only en `Metrics_Snapshot_Log.csv` con `Snapshot_Type=baseline_e0`.
5. Actualiza `Publication_Log.csv` únicamente con la identidad y una nota de estado E0; no coloca todavía el valor E0 en `Interacciones_24h` ni `Interacciones_72h`.
6. Si falla la lectura, registra `E0_Pending` con el error y reintenta con backoff dentro de la tolerancia. Si se agota la tolerancia, registra `E0_Missing` y deja la publicación fuera de la comparación contractual.

### 6.2 Publicaciones programadas

Al crear una programación, el sistema guarda `Meta_Post_ID`, `scheduled_publish_time` y `publication_status=Programada_Meta_Verificada`. El worker consulta únicamente las filas pendientes; cuando la API confirma `is_published=true`, usa el `created_time` real de Meta para iniciar E0. La hora planeada nunca reemplaza la hora de publicación efectiva.

### 6.3 Ventanas E24/E72

El worker selecciona solo filas con E0 válido y cuyo `Target_At_UTC` esté cerca de la hora actual. Captura los mismos contadores, guarda un raw nuevo y calcula:

```text
E24_delta = lifetime_interactions_at_24h - lifetime_interactions_at_e0
E72_delta = lifetime_interactions_at_72h - lifetime_interactions_at_e0
```

El cálculo se ejecuta únicamente con la misma definición de contadores, el mismo Meta Post ID y un `Window_Status` válido. Los resultados válidos se proyectan a los campos contractuales del `ExperimentLog.csv`; el ledger de snapshots conserva la fuente cruda y el timestamp exacto.

### 6.4 Posts manuales y Webhook

Meta documenta que el objeto Page puede suscribirse al campo `feed`, cuyo payload puede incluir `post_id`, `created_time`, `is_published`, `message`, `item` y `verb`. La instalación de la app en la Página y los permisos `pages_manage_metadata` y `pages_show_list` son requisitos de la suscripción de feed. [3] [4]

El receptor no debe confiar en el payload para los contadores: debe validar la firma, deduplicar el evento, consultar el post por ID y ejecutar la misma función de captura E0. Si el endpoint no está disponible o el evento no produce una lectura válida, una reconciliación de seguridad consulta el feed y registra el intento sin inventar el baseline.

## 7. Idempotencia, concurrencia y recuperación

La clave primaria lógica es `Meta_Post_ID + Snapshot_Type`. El `Snapshot_ID` diferencia intentos. Antes de capturar, el worker debe consultar si existe una fila `Valid_E0`, `Valid_24h` o `Valid_72h` para esa clave. Si existe, la ejecución es `no-op` y no vuelve a escribir el ledger.

Las escrituras deben protegerse con un lock de proceso o transacción. Si dos workers reciben el mismo webhook o la misma fila pendiente, solo uno puede promover la captura a válida. Los raw nunca se reemplazan; un retry escribe un nuevo intento con su propio timestamp y referencia de error.

La recuperación mínima es:

| Falla | Registro | Recuperación |
|---|---|---|
| Meta devuelve HTTP 429/5xx | `API_Error` | Backoff exponencial y reintento dentro de la ventana. |
| Token inválido o permiso insuficiente | `API_Error` | Pausa de la cola; alerta operacional; no se calculan deltas. |
| Post ID no existe | `id_mismatch` | Revisar publicación y no asociar por caption. |
| Campo de contador ausente | `missing_counter` | Conservar `null`; no sumar ni cerrar la ventana. |
| Captura fuera de tolerancia | `Late` | Conservar como observado; excluir de métrica contractual salvo aprobación. |
| Contador menor que E0 | `counter_decreased` | Preservar ambos snapshots; no ocultar el delta ni imputar cero. |
| GitHub ocupado o conflicto | `sync_pending` | Mantener el intento en la cola; reintentar con lock y reconciliación antes de hacer push. |

GitHub continúa siendo la fuente oficial de verdad. El almacenamiento operativo de la cola, si se elige una arquitectura alojada, es solo un buffer de reintentos y no una fuente paralela de decisiones. Cada lote sincronizado al repositorio debe incluir el raw, el ledger append-only, el changelog y el resultado de validación.

## 8. Validaciones obligatorias

Antes de considerar resuelto `Unavailable_No_Baseline`, el validador debe comprobar:

1. Cada publicación `Publicado` que entra en la cohorte tiene una fila de identidad en `Publication_Log.csv`.
2. Cada E0 válido tiene `Meta_Post_ID`, `Published_At_UTC`, `Captured_At_UTC`, los tres contadores, `HTTP_Status=200` y `Window_Status=Valid_E0`.
3. Cada E24/E72 válido tiene un E0 válido con el mismo `Meta_Post_ID`, el timestamp dentro de tolerancia y un delta calculado con la misma definición.
4. No hay dos filas canónicas válidas para la misma combinación `Meta_Post_ID + Snapshot_Type`.
5. Las filas `observed_lifetime`, `Late`, `Missing` y `API_Error` no rellenan campos contractuales.
6. Los ledgers actuales conservan vacías las ventanas antiguas que no tenían baseline.
7. Cada raw referencia su fuente, fecha de extracción y respuesta HTTP; Windsor no se usa para inventar el E0 de interacciones si el contrato está basado en Meta.
8. El validador produce un informe de conteos por estado y una lista explícita de fallos.

## 9. Orden de implementación por retorno operativo

La automatización debe priorizar lo repetitivo y de mayor impacto:

| Prioridad | Entregable | Efecto operativo esperado | Dependencia |
|---:|---|---|---|
| P0 | Ledger `Metrics_Snapshot_Log.csv` + módulo de captura E0 | Elimina la causa principal de `Unavailable_No_Baseline` en publicaciones nuevas y evita reconstrucciones manuales. | Aprobación de esquema y tolerancia E0 |
| P1 | Hook de publicación inmediata y cola de posts programados | Captura E0 donde ya existe un ID verificable, sin añadir una tarea por publicación. | Acceso al publicador actual |
| P2 | Worker E24/E72 por `Target_At_UTC` | Convierte E0 en deltas contractuales y cierra las ventanas con timestamp controlado. | P0 + reloj/cron frecuente |
| P3 | Reconciliación de publicaciones manuales; opcionalmente Webhook | Aumenta cobertura fuera del publicador y reduce dependencias de intervención humana. | Endpoint, permisos y fallback |
| P4 | Sincronización, dashboard y alertas | Facilita operación y auditoría, pero no debe preceder a la captura correcta. | P0–P3 |

El ahorro semanal debe medirse durante un piloto de tres a cinco publicaciones: registrar cuántos reintentos manuales, reconciliaciones y sesiones de recuperación evita el flujo. No se debe afirmar un ahorro horario antes de observar esa cohorte.

## 10. Estado de implementación P0 y límites actuales

El P0 de registro quedó activo como componente reproducible: `Operations/Research/Metrics_Snapshot_Log.csv` contiene el encabezado aprobado; `Operations/Automation/record_metrics_snapshot.py` puede leer un payload guardado o consultar Meta con `META_PAGE_ACCESS_TOKEN`, escribir un raw por intento y registrar E0/E24/E72/observed_lifetime; y `Operations/Automation/validate_metrics_snapshot_ledger.py` comprueba esquema, campos, duplicados, raw, E0 y deltas. La evidencia de pruebas está en `Operations/Research/2026-08-25_Metrics_Snapshot_Ledger_Activation_Evidence.json`.

La prueba aislada registró un E0, un retry `no-op` y un E24 en un ledger temporal; el ledger productivo permanece con cero snapshots porque no se debe fabricar un E0 histórico. El siguiente post nuevo que pase por una ruta Meta verificable debe ejecutar el módulo inmediatamente después de confirmar `is_published=true` y producir la primera fila de producción.

La activación P0 **no incluye todavía** el hook dentro del publicador de Fernando, el worker por `Target_At_UTC`, una tarea recurrente, una suscripción Webhook ni la actualización automática de `Publication_Log.csv`/`ExperimentLog.csv`. Esos componentes siguen en las prioridades P1–P4 y requieren pruebas separadas.

## 11. Plan de piloto sin activación automática todavía

El piloto propuesto es deliberadamente acotado:

1. El esquema y la implementación P0 de `Metrics_Snapshot_Log.csv` quedan registrados; las tolerancias propuestas siguen sujetas a revisión operativa antes de convertirlas en reglas permanentes.
2. Se usa el módulo P0 para publicaciones de Facebook que pasen por una ruta Meta verificable; no se toca Instagram, TikTok ni la publicación de respuestas de comunidad.
3. Se prueban tres casos reales nuevos y, si existe una programación futura, un caso programado. Cada caso debe conservar Page Post ID, `created_time`, `is_published`, counters, raw y estado.
4. Se ejecutan validaciones de duplicados, IDs, timestamps, counters faltantes y `counter_decreased`.
5. Tras el piloto se decide si integrar el hook al publicador, ampliar a E24/E72 con worker frecuente y si vale la pena la suscripción Webhook.
6. La implementación P0 ya está documentada en el pipeline, la fuente maestra, el changelog y `2026-08-25_Metrics_Snapshot_Ledger_Activation_Evidence.json`; las siguientes actualizaciones dependerán de capturas productivas reales.

No se debe reutilizar el lote histórico de 2026-08-15 a 2026-08-23 para fabricar E0. Ese lote permanece `Unavailable_No_Baseline` y sigue siendo válido únicamente como evidencia de la limitación.

## 12. Coherencia documental

Este documento representa un diseño nuevo y enlaza con la investigación metodológica, el protocolo P0, el pipeline de publicación y la arquitectura de ledgers. Mientras permanezca en `Review`, los documentos relacionados deben conservar sus reglas actuales: lifetime separado de 24/72, publicación con aprobación humana y ningún scheduler nuevo activado. Si Fernando aprueba la implementación, deberán actualizarse como mínimo `Operations/Research/2026-08-17_Investigacion_Ventanas_Temporales_Meta.md`, `Operations/Research/2026-08-17_Protocolo_P0_Metricas_y_Veredictos.md`, `GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md`, `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`, `Operations/Research/2026-08-22_Reels_Metric_Instrumentation_Protocol.md` y `GrowthOS/00_01_Changelog_GrowthOS.md`.

## Referencias

[1]: https://developers.facebook.com/documentation/pages-api/posts "Meta for Developers — Pages API: Posts"
[2]: https://developers.facebook.com/documentation/pages-api "Meta for Developers — Facebook Pages API"
[3]: https://developers.facebook.com/docs/graph-api/webhooks/getting-started/webhooks-for-pages/ "Meta for Developers — Webhooks for Pages"
[4]: https://developers.facebook.com/docs/graph-api/webhooks/reference/page/ "Meta for Developers — Webhooks Reference: Page"
[5]: ../Research/2026-08-17_Investigacion_Ventanas_Temporales_Meta.md "Growth OS — Investigación de ventanas temporales de Meta"
[6]: ../Research/2026-08-17_Protocolo_P0_Metricas_y_Veredictos.md "Growth OS — Protocolo P0 de métricas comparables y veredictos"
[7]: ../../GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md "Growth OS — Pipeline de publicación local y estándar CSV"
[8]: ../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md "Growth OS — Fuente maestra y ledgers"
