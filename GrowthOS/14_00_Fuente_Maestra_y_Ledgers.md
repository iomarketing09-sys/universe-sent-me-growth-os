---
title: "Fuente maestra y ledgers del Growth OS"
purpose: "Definir una arquitectura mínima y unificada para que inventario, publicaciones, calendarios y aprendizaje compartan IDs sin duplicar datos ni repetir consultas innecesarias."
status: Active
created: 2026-08-15
updated: 2026-08-17
version: "2.1"
author: "Manus AI (CGO)"
related_documents:
  - "GrowthOS/01_00_Arquitectura_Calendario_Escalable.md"
  - "GrowthOS/Integracion_Growth_OS.md"
  - "GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md"
  - "GrowthOS/Content_Inventory.csv"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "Operations/Research/2026-08-15_ExperimentLog.csv"
  - "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
  - "Operations/Research/2026-08-15_Community_Engagement_Log.md"
  - "Operations/Production/extract_metrics_24_72.py"
  - "Operations/Production/extract_metrics_24_72_playbook.md"
  - "Operations/Research/2026-08-15_Reconciliacion_Publicaciones_15_16_CNT.md"
  - "GrowthOS/00_Índice.md"
  - "Operations/Research/2026-08-17_Instagram_Publicacion_260633.json"
  - "Operations/Research/2026-08-17_Instagram_IDs_Duplicaciones_Confirmadas.json"
  - "Operations/Research/Historical_Performance_Snapshot.csv"
  - "Operations/Research/Historical_Performance_Individuals.csv"
  - "Operations/Research/2026-08-17_Integracion_CNT_Mayo_Reserve_Revision.md"
  - "Operations/Research/2026-08-17_Revision_Reserve_Mayo.json"
organization: "GrowthOS"
---

# Fuente maestra y ledgers del Growth OS

## 1. Decisión de arquitectura

La fuente maestra no debe ser un calendario gigante ni una tabla que repita una pieza cada vez que se publica en otra plataforma. Los agregados mensuales históricos viven en `Operations/Research/Historical_Performance_Snapshot.csv` como capa de referencia y las publicaciones individuales históricas verificables en `Operations/Research/Historical_Performance_Individuals.csv`; ninguna de las dos capas sustituye los ledgers append-only. La arquitectura recomendada para Universe Sent Me es **una fuente maestra de contenido más tres ledgers append-only**, cada uno con una función distinta: hechos de publicación, aprendizaje experimental y señales cualitativas de comunidad.

| Capa | Archivo canónico | Qué representa | Quién lo modifica |
|---|---|---|---|
| Identidad y estado de la pieza | `GrowthOS/Content_Inventory.csv` | Una fila por pieza creativa o concepto (`CNT-####`). Contiene personaje, formato, objetivo, hipótesis, canon, producción y elegibilidad de reuse. | Manus prepara; Fernando/Claude aprueban estados protegidos. |
| Historial de publicación | `Operations/Research/2026-08-15_Publication_Log.csv` | Una fila por publicación y plataforma. Conecta pieza, asset, fecha, cuenta, IDs de Meta, permalink, archivado y estado real. | Manus agrega después de cada orden o resultado de Meta. |
| Aprendizaje experimental | `Operations/Research/2026-08-15_ExperimentLog.csv` | Una fila por cohorte, publicación u observación de hipótesis. Contiene métricas, veredicto, conclusión y próxima acción. | Manus agrega datos; CGO/Manus redacta conclusión; Fernando aprueba decisiones de calendario. |
| Comunidad cualitativa | `Operations/Research/2026-08-15_Community_Engagement_Log.csv` | Una fila por comentario real que aporte señal, respuesta humana o decisión de moderación. No guarda identidades personales y complementa, pero no sustituye, el aprendizaje cuantitativo. | Manus agrega datos anonimizados; las respuestas públicas y acciones de moderación requieren aprobación humana. |

La idea clave es que **no todo debe vivir en una sola fila**. Una pieza puede publicarse muchas veces, en varias plataformas y bajo varios experimentos. Si todo se fuerza dentro de `Content_Inventory.csv`, aparecerán columnas repetidas, estados contradictorios y pérdida de historial. El inventario identifica la pieza; `Publication_Log` identifica el hecho de publicación; `ExperimentLog` identifica lo aprendido cuantitativamente; `Community_Engagement_Log` identifica señales cualitativas de conversación y cobertura de respuesta.

## 2. Qué queda como vista y qué deja de ser fuente

Los calendarios semanales, la `Reuse Queue`, la `Production Queue` y la `Approval Queue` deben tratarse como **vistas filtradas** del inventario y de los ledgers. Pueden existir como Markdown o CSV para revisión humana, pero no deben introducir un nuevo estado maestro ni duplicar el historial.

| Vista operativa | Regla de generación |
|---|---|
| Calendario semanal | Filtrar piezas `Aprobado`, sin bloqueo de canon, asignarlas a slots y exportar la orden de publicación. |
| Reuse Queue | Filtrar piezas reutilizables cuya última publicación cumpla la regla de 30 días y ordenar por rendimiento histórico. |
| Production Queue | Filtrar piezas en producción o pendientes de asset; no cambia el estado maestro sin una decisión registrada. |
| Approval Queue | Filtrar piezas con revisión de canon o aprobación de Fernando pendiente. |
| Reporte de aprendizaje | Agrupar `ExperimentLog` por `Experiment_ID`, `Hypothesis_ID`, plataforma, tipo y slot. |
| Reporte de comunidad | Agrupar `Community_Engagement_Log` por `Post_ID`, `CNT_ID`, `Tipo`, `Respuesta_Estado`, prioridad y ventana de revisión. |

El calendario 15–16 de agosto y la propuesta 17–30 permanecen como documentos de planeación/exportación. No deben convertirse en una segunda base de datos permanente.

## 3. IDs mínimos y relaciones

La relación mínima es:

```text
ID_Pieza (CNT-####)
   ├── Asset_Ref / nombre exacto / Drive_ID
   ├── Publicacion_ID → una fila por plataforma y fecha
   │      └── Meta_Post_ID o IG_Media_ID
   ├── Observacion_ID → una fila por experimento, cohorte o resultado
   │      └── Experiment_ID + Hypothesis_ID
   └── Comentario_ID → una fila cualitativa de comunidad, cuando exista
          └── Respuesta_Estado + Accion_Calendario
```

Los códigos `260####` son referencias de asset y no sustituyen automáticamente al `CNT-####`. Cuando todavía no exista una correspondencia confirmada, el campo `ID_Pieza` debe quedar vacío y anotarse como pendiente de reconciliación; no se debe inventar un vínculo.

## 4. Modelo mínimo recomendado

La fuente maestra debe conservar los campos narrativos y de flujo que ya existen en `Content_Inventory.csv`. La próxima migración debe añadir, sin borrar columnas históricas, los siguientes campos normalizados:

| Campo | Uso |
|---|---|
| `ID_Pieza` | Identidad estable de la pieza creativa. |
| `Asset_Ref` | Código `260####` o referencia de asset. |
| `Asset_Filename` | Nombre exacto del archivo. |
| `Drive_ID` | Identificador de Google Drive cuando exista. |
| `Estado_Canon` | `Libre`, `Revision`, `Aprobado`, `Bloqueado`. |
| `Estado_Produccion` | `Idea`, `En_Produccion`, `Asset_Listo`, `Pendiente_Revision`, `Diferido`. |
| `Estado_Publicacion` | `No_Publicada`, `Programada`, `Publicada`, `Archivada`, `Error`. |
| `Ultima_Sincronizacion` | Fecha de la última reconciliación del registro. |
| `Motivo_Revision_Normalizado` | Clasifica por qué una pieza permanece en `Revision` sin convertir el motivo en una aprobación de canon. |

Estos campos deben eliminar la necesidad de interpretar texto libre como “Draft v2”, “pendiente aprobación” o “bloqueado por continuidad” cada vez que se genere un calendario.

### 4.1 Distinción entre canon y reconciliación administrativa

`Estado_Canon` y `estado_canon_normalizado` expresan la condición canónica de la pieza, pero no deben absorber cualquier problema de inventario. `Motivo_Revision_Normalizado` separa las causas que mantienen un registro en revisión:

| Motivo | Uso |
|---|---|
| `Canon_Contradiccion_Sustantiva` | Existe una contradicción narrativa o de diseño que sí requiere revisión canónica. `CNT-004` conserva este motivo, aunque su desarrollo está diferido. |
| `Canon_Aprobacion_Administrativa` | La pieza espera una aprobación o ficha formal, sin que el inventario evidencie una contradicción sustantiva. |
| `Canon_Restriccion_No_Bloqueante` | Existe una regla de continuidad que debe observarse, pero no constituye por sí sola un bloqueo de canon para la capa libre. |
| `Canon_Resuelto_Reconciliacion_Pendiente` | La identidad canónica fue resuelta, pero falta cerrar la relación de inventario o asset. Actualmente: `CNT-009`, cuyo nombre Silvio está confirmado en `8e9fe9a`. |
| `Inventario_Reconciliacion_Pendiente` | Falta una coincidencia CNT↔260/Drive; no es una aprobación creativa. |
| `Identidad_Reconciliada_Sin_Conflicto_Canon_Evidente` | La pieza fue creada o reconciliada a partir de asset, caption y Meta ID, sin evidencia de contradicción canónica. Actualmente: `CNT-031`–`CNT-039`. |

La reclasificación del 15 de agosto dejó **1** registro en `Canon_Review_Required` (`CNT-004`), **4** en `Canon_Constrained`, **1** en `Canon_Partial` y **33** en `Canon_Clear_or_Unverified`. CNT-004 queda fuera de desarrollo por decisión operativa, pero conserva `Estado_Canon=Revision`; cualquier transición a `Aprobado` sigue reservada a Fernando o Claude. La evidencia completa está en `Operations/Research/2026-08-15_Reclasificacion_Canon_vs_Reconciliacion.json`.

## 5. Diseño de bajo consumo de tokens

La operación diaria no debe consultar toda la historia. Manus debe leer el inventario una vez, cargar el calendario del día y consultar únicamente las publicaciones nuevas o modificadas desde el último `Ultima_Sincronizacion`.

El flujo económico es el siguiente:

1. **Antes de publicar:** leer `Content_Inventory.csv` y el calendario aprobado; validar solamente las filas del lote actual.
2. **Durante la publicación:** registrar el resultado en `Publication_Log.csv`; no volver a inspeccionar todo el inventario.
3. **A las 24 y 72 horas:** consultar métricas solo para los `Meta_ID` nuevos del lote, idealmente en una llamada paginada o agrupada; no volver a pedir publicaciones históricas completas.
4. **Al cierre del ciclo:** agregar una observación consolidada a `ExperimentLog.csv`, actualizar el veredicto de la hipótesis y generar las colas como vistas.
5. **Para comentarios:** leer solo comentarios nuevos desde el último cursor o ventana; no revisar cada cinco minutos, deduplicar por `Comentario_ID` y no conservar identidades personales. Registrar las señales en `Community_Engagement_Log.csv`.

Esta arquitectura reduce llamadas repetidas, evita que el agente relea documentos largos y permite que cada sesión trabaje con un delta pequeño. El ahorro no proviene de eliminar el aprendizaje; proviene de **no recalcular ni volver a descargar lo que ya está registrado**.

### 5.1 Cadencia recomendada para métricas

La revisión operativa de métricas se hará **cada dos días** como lote, en lugar de consultar cada publicación diariamente. Para el experimento `EXP-2026-08-CAL-01`, la hora recomendada es **22:15 de America/Matamoros**, comenzando el 2026-08-16, porque a esa hora ya maduró el último slot del día anterior y se evita despertar durante la ventana activa de publicaciones. La ejecución debe leer únicamente las filas de `Publication_Log.csv` cuyo timestamp real ya haya alcanzado una ventana de 24 o 72 horas, agrupar los Meta Post IDs pendientes y actualizar ambos ledgers en una sola pasada.

La cadencia de 48 horas reduce despertares y lecturas repetidas, pero no cambia la definición de las ventanas. Cada fila conserva su hora real de publicación; no se sustituye una medición de 24 horas por el total acumulado disponible al segundo día. Cuando Meta permita una consulta temporal con `since`/`until`, se usará esa ventana; si el metric solicitado solo devuelve un total de lifetime o no permite reconstruir el snapshot, se registrará `24h_snapshot_unavailable` o `72h_snapshot_unavailable` en la nota y no se inventará el valor [7] [8].

El mismo procedimiento aplica a las publicaciones posteriores: registrar primero el Meta ID y la hora real, calcular `+24h` y `+72h`, seleccionar solo las filas vencidas en la siguiente revisión de dos días y mantener separadas las métricas de Facebook e Instagram. **Un solo despertar es suficiente para la operación del Growth OS**: el script procesa todas las filas vencidas en lote, no solo una publicación. Esto minimiza sesiones y consultas, aunque retrasa algunos snapshots respecto a la hora exacta; si se necesitara exactitud estricta a 24/72 horas, habría que usar dos ejecuciones o un proceso persistente determinista. Si Meta no permite reconstruir retrospectivamente el snapshot, se conserva la limitación y no se inventa el valor.

## 6. Primer estado implementado

El `ExperimentLog` contiene observaciones históricas, nueve publicaciones reales de Facebook del 15–16 de agosto y tres publicaciones activas confirmadas de Instagram: `2608030`, `2608036` y `2608060`. Además, registra seis IDs proporcionados por Fernando para duplicaciones Instagram 17–30 (`260633`, `260560`, `260614`, `260625`, `260613` y `260528`) con estado prudente `Programada`, sin permalink ni hora real inventados. La fila histórica de `260633` con media `17943879225288953` permanece como `Eliminada_Manualmente`; el nuevo ID `1564061365193135` se conserva como registro separado. Ninguna de estas filas recibe un CNT inventado; permanecen con `ID_Pieza` vacío hasta una reconciliación con evidencia suficiente. El `Publication_Log` enlaza las nueve publicaciones de Facebook con `CNT-031`–`CNT-039`, conserva intentos históricos de Instagram eliminados manualmente y separa publicaciones activas confirmadas de programaciones con ID proporcionado. Las métricas 24/72 horas de Facebook y los cortes observados de Instagram quedan pendientes de evidencia válida.

El `Community_Engagement_Log.csv` contiene 18 comentarios reales: nueve del primer lote, seis del delta del 16 de agosto, dos del delta del 17 de agosto y una revisión puntual de publicación. Las cuatro respuestas del primer lote y la respuesta puntual fueron aceptadas por Meta; la respuesta puntual tiene `Respuesta_Meta_ID=122148874563072582_1613678620282915`, aunque su verificación GET devolvió HTTP 403 por permisos. La muestra histórica de 67 comentarios se conserva como análisis agregado y no se transforma retroactivamente en filas. Las futuras revisiones deben recuperar solo el delta nuevo, deduplicar por `Comentario_ID` y mantener respuestas y moderación bajo aprobación humana.

El lote 1 de normalización cubrió inicialmente 28 filas y, tras resolver las excepciones, `Content_Inventory.csv` llegó a 30 registros. La reconciliación del calendario 15–16 añadió nueve piezas de identidad nuevas, por lo que el inventario llegó a 39 registros. La integración histórica de mayo añadió `CNT-040`–`CNT-067`, por lo que el inventario contiene ahora 67 registros. Se preservaron todas las columnas originales y se añadieron campos normalizados para estado operativo, estado de canon, asset confirmado, asset candidato, relaciones y trazabilidad de reconciliación. Los CNT históricos nuevos no constituyen aprobación canónica ni publicación activa.

`CNT-002 → 260509` quedó resuelto como `Resolved_Production_Set`: Meta identificó el post `1036844829507460_122143141185072582`, publicado el 30 de julio a las 14:16:47 UTC, con permalink `https://www.facebook.com/reel/911880681976378/`. El reel dura 17.39 segundos y su secuencia coincide con los tres videos de producción de Wilfred/caja/peluche localizados en Drive. El archivo 260509 de Drive corresponde a Universe existencial y se mantiene rechazado. No existe un render final `260####` confirmado, así que no se inventa uno.

`CNT-023` quedó resuelto como `Resolved_Asset_Set`: el episodio 2 de “¿Qué me llegó?” se relaciona con la carpeta de Drive `Elara - Lampara de luna`, que contiene 7 assets verificados: cuatro piezas de video/imagen de entrega y apertura de paquete, más tres renders de secuencia. El registro conserva los siete nombres en `asset_set`, no se fuerza a un único `260####` y se enlaza con `CNT-002`, el episodio 1. La publicación de Facebook quedó confirmada con Page Post ID `1036844829507460_122147352825072582`, Reel ID `1067337609170026`, permalink `https://www.facebook.com/reel/1067337609170026/` y fecha local 2026-08-08 19:19:54.

`CNT-029` y `CNT-030` fueron incorporados desde sus documentos reales de producción. CNT-029 es el reel “Pausa para ver qué piensa de ti”, con banco de 9 cuadros, hook de pausa y estado `Draft_Pending_Approval`; la búsqueda acotada de Meta del 14–17 de agosto no encontró una publicación coincidente. CNT-030 es su especificación dependiente de audio y montaje, también `Draft_Pending_Approval`, no una publicación independiente. Ambos quedan enlazados entre sí, conservan sus nombres de assets documentados y no reciben referencias 260 inventadas.

El preview actualizado está en `Operations/Research/2026-08-15_Reconciliacion_Lote_01_Preview.md` y el CSV detallado en `Operations/Research/2026-08-15_Reconciliacion_Lote_01_Preview.csv`. CNT-023 conserva además el `drive_reference_id` de la carpeta de producción, el listado exacto de sus siete assets y la publicación confirmada en `Publication_Log.csv`. CNT-029/CNT-030 conservan sus bancos de assets y no generan filas de publicación hasta que exista aprobación y un permalink real. La normalización es reversible porque `estado` y `bloqueado_canon` originales permanecen intactos. CNT-002 ya no tiene una excepción abierta a nivel de publicación ni de conjunto de producción. Solo queda registrada la ausencia del nombre del render final como archivo `260####`, lo cual no bloquea la integridad de los 39 registros actuales.

## 7. Estado de unificación — lote 1

El 15 de agosto de 2026 se aplicó el primer lote de unificación al inventario maestro. Después de reconciliar el calendario 15–16, `Content_Inventory.csv` conserva sus 39 filas y todos los campos históricos, y contiene siete campos canónicos derivados: `Asset_Ref`, `Asset_Filename`, `Drive_ID`, `Estado_Canon`, `Estado_Produccion`, `Estado_Publicacion` y `Ultima_Sincronizacion`.

| Campo canónico | Regla aplicada en el lote 1 |
|---|---|
| `Asset_Ref` | Copia únicamente de `asset_ref_confirmado`; queda vacío si no existe evidencia confirmada. |
| `Asset_Filename` | Usa el conjunto de assets documentado cuando existe; no convierte nombres de producción en un falso `260####`. |
| `Drive_ID` | Deriva de `drive_reference_id`. |
| `Estado_Canon` | Normaliza el estado existente a `Revision` o `Restringido`; no aprueba canon automáticamente. |
| `Estado_Produccion` | Normaliza ideas, producción pendiente, revisión, reuse, bloqueo y publicación sin borrar el texto original. |
| `Estado_Publicacion` | Marca `Publicada` solo cuando existe `meta_publication_id`; el resto queda `No_Publicada`. |
| `Ultima_Sincronizacion` | Fecha del lote: `2026-08-15`. |

La validación posterior al lote reconcilió 39 IDs únicos, 11 piezas con publicación Meta enlazada (`CNT-002`, `CNT-023` y `CNT-031`–`CNT-039`) y 28 piezas sin publicación confirmada. Se preservaron los estados históricos y no se confirmó ningún asset `260####` sin evidencia.

La unificación todavía no está completa. Los siguientes trabajos quedan explícitamente separados para evitar una migración riesgosa: completar métricas 24/72 horas en `Publication_Log`, cerrar el aprendizaje de `HB-003`, `HB-004` y `HB-005`, convertir calendarios/colas en exportaciones verificables del inventario y poblar progresivamente el `Community_Engagement_Log` con comentarios reales. `CNT-004` queda diferido y no forma parte del lote activo de desarrollo; si se retoma, requerirá revisión canónica y aprobación. El mapeo de las nueve órdenes del calendario 15–16 ya está cerrado mediante `CNT-031`–`CNT-039`. Estos pendientes restantes son de medición, integración, comunidad y aprobación; no deben resolverse inventando IDs.

## 8. Reglas de gobernanza

`Content_Inventory.csv` es la fuente de identidad de las piezas. `Publication_Log.csv` es el historial de hechos y no debe sobrescribirse para “limpiar” errores; se corrigen mediante una columna de nota o una nueva entrada de corrección. `ExperimentLog.csv` es el registro de aprendizaje y no debe llenarse con hipótesis inventadas ni con métricas estimadas. `Community_Engagement_Log.csv` es la capa cualitativa y no debe llenarse con identidades personales, comentarios inventados o respuestas no verificadas.

Los estados de canon y aprobación no se cambian automáticamente. Fernando o Claude conservan la autoridad sobre canon y aprobación final. Manus puede validar, agregar datos, preparar vistas y documentar resultados, pero no convertir una propuesta en canon ni marcar una pieza bloqueada como aprobada.

## Referencias

[1]: `01_00_Arquitectura_Calendario_Escalable.md` — Arquitectura de metadatos, estados y calendario como vista.
[2]: `13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md` — Formato de exportación y publicación mediante Meta Graph API.
[3]: `Integracion_Growth_OS.md` — HypothesisBank, ExperimentLog y puente con canon.
[4]: `Content_Inventory.csv` — Inventario actual de 39 piezas, estados históricos y campos canónicos derivados.
[5]: `../Operations/Research/2026-08-15_Publication_Log.csv` — Primer ledger de publicaciones implementado.
[6]: `../Operations/Research/2026-08-15_ExperimentLog.csv` — Primer ledger experimental implementado.
[7]: https://developers.facebook.com/docs/graph-api/reference/post/insights/ — parámetros `since`, `until`, `period` y métricas de Post Insights.
[8]: https://developers.facebook.com/documentation/pages-api/platforminsights/page — limitaciones y actualización de Page Insights.
[9]: `../Operations/Research/2026-08-15_Reclasificacion_Canon_vs_Reconciliacion.json` — distribución de motivos de revisión canónica y administrativa.
