---
title: "Auditoría integral del Growth OS"
purpose: "Verificar que la documentación, ledgers, inventario, experimento P0, Meta Graph API, Instagram y schedules estén integrados y operando de forma coherente."
status: "Review"
created: 2026-08-19
updated: 2026-08-20
version: 1.2
author: "Manus AI (CGO)"
related_documents:
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
  - "GrowthOS/Content_Inventory.csv"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "Operations/Research/2026-08-15_ExperimentLog.csv"
  - "Operations/Research/2026-08-17_P0_Baseline_Ola_Activa.csv"
  - "Operations/Research/2026-08-17_Protocolo_P0_Metricas_y_Veredictos.md"
  - "Operations/Research/2026-08-16_Calendario_Operativo_17_30_Agosto.csv"
  - "Operations/Research/2026-08-19_Normalizacion_Documental_P2.md"
  - "Operations/Research/2026-08-18_Analisis_Rendimiento_28_Dias_Instagram_Facebook.md"
  - "Operations/Research/2026-08-19_Windsor_Instagram_28D_Normalizado.json"
organization: "Operations/Research"
---

# Auditoría integral del Growth OS

## Resumen ejecutivo

El Growth OS está **operativo pero no completamente integrado**. La ruta de publicación de Facebook mediante Meta Graph API funciona en modo lectura y escritura validada históricamente: el conector está habilitado, la página `Universe Sent Me` se resuelve correctamente y el feed reciente contiene las cinco publicaciones de la ola P0 del 17 de agosto. El schedule del primer corte P0 está activo, configurado para `America/Matamoros` y con una sola ejecución.

La principal deuda no es la conexión de Meta, sino la **unificación de datos**. El calendario operativo contiene 74 slots y el Publication Log contiene 98 filas, pero el inventario maestro solo tiene 85 filas y no contiene los 74 nombres de archivo usados por las publicaciones programadas. Los cinco assets del baseline P0 tampoco están integrados como filas de inventario mediante `Asset_Ref`. Esto no invalida la prueba, pero significa que el inventario maestro todavía no es una fuente única completa para la ola activa.

Las métricas temporales P0 aún no se han capturado: las cinco filas permanecen en `Pendiente_ventana` y las columnas 24/72 horas están vacías. Esto es correcto si la auditoría se realiza antes de vencer el corte, pero el cierre del experimento depende de ejecutar el extractor y escribir la evidencia en los ledgers correctos. El histórico está separado por periodos, aunque contiene cinco duplicados legítimos de Meta ID derivados de la integración inicial y visual confirmada de junio; conviene consolidarlos para evitar doble conteo en análisis posteriores.

## Semáforo general

| Área | Estado | Evidencia | Interpretación |
|---|---|---|---|
| GitHub como fuente oficial | Ámbar | Rama `main` alineada con `origin/main`, pero había 13 rutas sin seguimiento | La documentación nueva debe quedar publicada; la evidencia visual estaba local y no versionada |
| Meta Graph API | Verde | Página resuelta como `Universe Sent Me`; objeto de página HTTP 200; feed HTTP 200 | La lectura de página funciona con el token de página resuelto desde la cuenta autorizada |
| Facebook P0 | Verde operativo / Ámbar analítico | Cinco posts confirmados en Meta y baseline de cinco filas | La ola existe; todavía no hay métricas comparables 24/72h |
| Schedule P0 | Verde | Una tarea activa, una ejecución, `America/Matamoros` | No hay polling cada 5 minutos ni múltiples despertares activos |
| Publication Log | Ámbar | 98 filas: 80 programadas, 14 publicadas y 4 eliminadas manualmente | Está integrado operacionalmente, pero usa nombres de archivo en `Asset_Ref` y no siempre IDs normalizados |
| ExperimentLog | Ámbar | 101 filas; 98 tienen métricas agregadas vacías | Conserva la estructura, pero aún no cierra el aprendizaje de la ola activa |
| Inventario maestro | Rojo parcial | 85 filas; 74 `Asset_Ref` de publicaciones no tienen coincidencia en `Content_Inventory.csv` | El inventario no refleja todavía la totalidad de la programación 17–30 |
| Histórico individual | Ámbar | 211 filas: 177 junio, 28 mayo, 6 julio; cinco Meta IDs duplicados | La cobertura es útil, pero requiere deduplicación lógica antes de comparaciones agregadas |
| Instagram | Ámbar analítico / Verde en lectura Windsor | Windsor devolvió 34 piezas del corte con engagement, reach, views y watch time; el conector validó muestras | La medición histórica funciona; la publicación futura sigue controlada y separada |
| Make | Verde retirado | Las menciones halladas son históricas o de auditoría | No se detectó como dependencia activa en la ruta vigente |

## Hallazgos de integración

### Inventario y publicaciones

`Content_Inventory.csv` contiene 85 filas. Sus campos canónicos de identificación son `id`, `Asset_Ref`, `Asset_Filename`, `Drive_ID` y `meta_publication_id`; no existe una columna `CNT_ID`, por lo que los scripts no deben asumir ese nombre. La convención vigente utiliza `id` para valores como `CNT-001`.

El Publication Log tiene 98 filas sin duplicados exactos: 85 de Facebook y 13 de Instagram. Sus estados son 80 `Programada`, 14 `Publicado` y 4 `Eliminada_Manualmente`. Sin embargo, 74 nombres de archivo del log no coinciden con el campo `Asset_Ref` del inventario maestro. La causa parece ser una diferencia entre **filename operativo** y **referencia editorial/CNT**, no necesariamente una publicación huérfana. Debe resolverse mediante una tabla de alias o una columna normalizada, no mediante la creación automática de CNT.

Los cinco assets P0 tienen `Asset_Ref` numérico en el baseline (`260633`, `2608028`, `2608034- Elara`, `2608027.jpeg` y el quinto slot correspondiente), pero no están enlazados por el mismo campo en el inventario. La prueba puede continuar porque el baseline conserva Meta ID, slot, fecha, tipo de contenido y estado; aun así, la fuente maestra permanece incompleta.

### P0 y separación temporal

El baseline `EXP-2026-08-CAL-01` contiene cinco publicaciones de Facebook del 17 de agosto, todas con estado `Publicado_confirmado_Meta` y `Pendiente_ventana`. Las columnas `interactions_24h`, `comments_root_24h`, `shares_24h`, `interactions_72h` y equivalentes están vacías en las cinco filas. Esto respeta la regla de no inventar ventanas temporales ni sustituirlas con lifetime.

El ExperimentLog contiene 95 filas de `EXP-2026-08-CAL-01`, pero 98 de sus 101 filas tienen métricas agregadas vacías. La estructura está preparada, pero el ciclo de aprendizaje todavía no está cerrado. El extractor debe escribir únicamente las filas vencidas del baseline y dejar evidencia del `Corte_Observado` cuando Meta no permita reconstruir una ventana exacta.

### Histórico

`Historical_Performance_Individuals.csv` tiene 211 filas: 177 de junio, 28 de mayo y 6 de julio. Los cinco Meta IDs duplicados corresponden a la doble integración de los cinco top posts de junio: una fila del comparativo mensual y otra fila con relación visual confirmada. Las métricas coinciden en cada par, por lo que no parecen dos publicaciones distintas. Antes de usar sumas históricas agregadas, deben consolidarse como una sola publicación con múltiples fuentes de evidencia.

### Meta e Instagram

La llamada directa al endpoint `/me` devuelve el usuario autorizado, no la página. Esto no debe interpretarse como fallo del conector: `/me/accounts` devuelve la página `Universe Sent Me` y un token de página; con ese token, el objeto de página responde HTTP 200 y el feed responde HTTP 200. La operación correcta debe resolver explícitamente el token de página antes de consultar el feed o realizar una acción sobre la página.

Instagram permanece deliberadamente controlado para **publicación**, no para medición. El Publication Log registra pruebas eliminadas y duplicaciones manuales, pero no debe afirmar publicación automática efectiva sin permalink, media ID o evidencia Meta. Para rendimiento, Windsor devolvió 34 piezas del corte 22 de julio–18 de agosto con métricas de media, y el conector de Instagram coincidió con Windsor en dos Reels y una imagen. Graph API directa conserva la identidad y la publicación; su token actual todavía carece de `instagram_manage_insights`. No se recomienda reactivar el scheduler de Instagram dentro de esta auditoría.

## Correcciones aplicadas durante la auditoría

Se añadieron comprobadores reproducibles para integridad de ledgers, reconciliación de enlaces y lectura de la página Meta. También se incorporaron al repositorio las evidencias visuales locales generadas durante los análisis de junio, evitando que las conclusiones dependan exclusivamente de archivos temporales de la sesión.

No se crearon CNT, no se modificó el calendario, no se publicaron contenidos y no se alteró Instagram. La razón es que la deuda encontrada requiere una decisión de normalización de identificadores, no una reparación automática que pudiera crear duplicados o romper el freeze de reuse.

## Prioridades de reparación

| Prioridad | Acción | Motivo |
|---|---|---|
| P0 | Ejecutar el corte de métricas de las cinco filas baseline y escribir evidencia | Es el único bloqueo para cerrar la prueba activa |
| P1 | Crear una tabla de alias `Asset_Ref` ↔ filename operativo ↔ `id`/CNT | Resolverá los 74 falsos huérfanos sin crear nuevos CNT automáticamente |
| P1 | Consolidar los cinco Meta IDs duplicados del histórico de junio | Evitar doble conteo en medianas, rankings y reportes mensuales |
| P1 | Enlazar los cinco assets P0 al inventario maestro o documentar formalmente su excepción | Completar la fuente maestra de la ola activa |
| P2 | Separar o archivar las propuestas históricas de calendario para que no parezcan programación activa | Reducir riesgo de leer una propuesta antigua como estado operativo |
| P2 | Mantener Instagram manual hasta una nueva campaña con playbook autocontenido | Evitar duplicados, horarios nocturnos y publicaciones no verificadas |

## Estado final

El Growth OS está **funcionando en publicación y captura estructural**, pero **todavía no está debidamente integrado como fuente maestra única**. El siguiente trabajo debe ser de normalización de identificadores y cierre P0, no de crear más análisis históricos ni de modificar el canon.


## Actualización posterior al cierre provisional P0 — 2026-08-20

La sección inicial de esta auditoría fue redactada antes del corte observado del 19 de agosto. El estado vigente es el siguiente: el P0 de cinco publicaciones del 17 de agosto ya tiene un cierre provisional documentado en `2026-08-19_P0_Corte_17_Agosto.md`, con 785 interacciones observadas acumuladas. El campo de experimento queda `Cerrada_con_limitacion` porque Meta no entregó snapshots exactos 24/72h; los acumulados lifetime no sustituyen esas columnas.

Por lo tanto, P0 ya no es un pendiente de extracción básica. El pendiente estadístico real es **analizar el lote operativo de nueve publicaciones del 15–16 (`CNT-031`–`CNT-039`) como cohorte separada**, y continuar los cortes observados de la ola 17–30 sin mezclarla con el baseline P0. También deben mantenerse separados los aprendizajes de P0 basados en el outlier `2608028` de cualquier conclusión general de horario.

Los pendientes de integración que siguen vigentes son la reconciliación de `Asset_Ref`/filename del inventario maestro, la consolidación lógica de duplicados históricos y la medición controlada de Instagram. Instagram no debe reabrirse para publicación automática en este ciclo.


## Actualización de fuente maestra e histórico de junio — 2026-08-20

Se creó `Operations/Research/2026-08-20_Source_Alias_Table.csv` como capa reproducible entre `Publication_Log.csv` y `Content_Inventory.csv`. El primer corte cubre 98 filas: 52 coincidencias únicas de alta confianza, 46 filas en revisión o sin coincidencia y 3 filas sin clave numérica extraíble. La tabla conserva los nombres operativos, IDs de Meta, permalinks y estados sin crear CNT automáticos.

También se creó `Operations/Research/2026-08-20_Historical_Performance_Individuals_Consolidated.csv`. El archivo fuente de 211 filas permanece intacto; la vista consolidada contiene 206 publicaciones lógicas y cinco grupos duplicados de Meta ID. Los cinco grupos tienen métricas de reacciones, comentarios y shares consistentes, por lo que deben contarse una sola vez en agregados y rankings. Las filas originales se conservan como evidencia múltiple.

El estado correcto ya no es “sin tabla de aliases” ni “sin vista de consolidación”. La deuda restante es resolver las 46 filas de revisión, enlazar o exceptuar formalmente los cinco assets P0 y usar la vista consolidada para futuros agregados de junio. No se modificó canon ni se inventaron CNT.


## Actualización de asociación P0 y aliases 17–30 — 2026-08-20

Los cinco assets P0 fueron revisados contra el inventario y la evidencia local. `260633` quedó asociado a `CNT-062` y `260642` a `CNT-064`. `2608028`, `2608034- Elara` y `2608027.jpeg` conservan Meta Post ID y evidencia visual local, pero permanecen como excepciones sin fila en `Content_Inventory`; no se crearon CNT.

En la programación 17–30 se revisaron 81 filas: 43 permanecen en `Review`. De esas, 33 tienen archivo local que confirma la identidad del asset, aunque aún falta la asociación administrativa al inventario; 10 no tienen evidencia local y requieren una consulta posterior a Drive/Meta o confirmación humana. Este resultado sustituye la cifra genérica de aliases sin clasificar y no debe interpretarse como autorización para crear CNT.


## Actualización de staging de inventario y diez casos ampliados — 2026-08-20

Se creó `Operations/Research/2026-08-20_Inventory_Alias_Staging_17_30.csv` con 33 assets cuya identidad visual está confirmada por archivo local. La capa conserva evidencia y hashes, pero no crea CNT ni modifica `Content_Inventory.csv`.

Los diez casos que no aparecieron en la carpeta visual principal fueron buscados en rutas locales adicionales. El resultado fue: dos filas relacionadas con `260508` tienen filename exacto y candidatos de inventario existentes; ocho assets tienen evidencia local pero no fila de inventario. No quedó ningún caso sin archivo después de la búsqueda ampliada. El archivo `2026-08-20_10_Cases_Resolution_Options.csv` documenta las rutas seguras de resolución y sus riesgos.
