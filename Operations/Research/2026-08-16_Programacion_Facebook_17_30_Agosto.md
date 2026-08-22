# Programación Facebook 17–30 de agosto — Meta Graph API

**Propósito:** Registrar la programación real de los 78 slots aprobados del calendario operativo de Universe Sent Me mediante la Meta Graph API y dejar trazabilidad de los Page Post IDs, Photo IDs, verificaciones, estado de Drive y alcance de Instagram.

**Estado:** Active
**Fecha de creación:** 2026-08-16
**Última actualización:** 2026-08-22
**Versión:** 1.4
**Autor:** Manus AI
**Documentos relacionados:** `2026-08-16_Calendario_Operativo_17_30_Agosto.csv`, `2026-08-16_Asignacion_Visual_Calendario_17_30_Agosto.csv`, `2026-08-15_Publication_Log.csv`, `2026-08-15_ExperimentLog.csv`, `2026-08-16_Manifiesto_Movimiento_35_Memes_Agosto.csv`, `GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md`

---

## Resultado ejecutivo

El 16 de agosto de 2026 se programaron **74 publicaciones de Facebook** para el periodo del 17 al 30 de agosto. El 22 de agosto se añadieron **4 slots** para recuperar la cadencia del 22 al 30, usando la Página `Universe Sent Me` (`1036844829507460`) y la API Graph v26.0. Meta documenta la programación mediante `published=false` y `scheduled_publish_time` en Pages API [1], el flujo de foto temporal y `temporary=true` en Page Photos [2], y la lectura de posts programados mediante `/scheduled_posts` [3]. Meta devolvió un Page Post ID y un Photo ID para cada slot; las 78 verificaciones posteriores confirmaron el `scheduled_publish_time` esperado, el mensaje correspondiente y `is_published=false`.

| Control | Resultado |
|---|---:|
| Slots programados | **78/78** |
| Page Post IDs reales | **78/78** |
| Photo IDs reales | **78/78** |
| Verificaciones de lectura posteriores | **78/78** |
| Errores finales | **0** |
| Assets excluidos | `260583` — no apareció en el lote |
| Movimientos en Drive | **0** |
| Copias creadas en Drive | **0** |
| Cambios en Instagram | **0** |

La distribución diaria quedó documentada en el calendario maestro: 6 posts el 17, 6 el 18, 6 el 19, 6 el 20, 4 el 21, 5 el 22, 6 el 23, 6 el 24, 6 el 25, 6 el 26, 6 el 27, 5 el 28, 5 el 29 y 5 el 30 de agosto. En el tramo 22–30 cada día queda dentro de la banda operativa de 5–6 publicaciones.

## Flujo técnico ejecutado

El flujo validado fue de dos pasos. Primero, cada imagen se cargó a `/{page_id}/photos` como foto temporal con `published=false` y `temporary=true`. Después, se creó el post en `/{page_id}/feed` utilizando `attached_media[0]`, `published=false`, `scheduled_publish_time` y `unpublished_content_type=SCHEDULED`. El Page Access Token se derivó en memoria desde `/me/accounts`; no se almacenaron tokens en el repositorio.

Una primera variante que intentaba enviar directamente `scheduled_publish_time` junto con la carga de la foto fue rechazada por Meta con un error genérico. Se sustituyó por el flujo oficial de foto temporal más post programado, que produjo **74/74 respuestas exitosas** y verificaciones correctas.

## Registro de hechos

Los registros completos se encuentran en `Operations/Research/2026-08-15_Publication_Log.csv` y `Operations/Research/2026-08-15_ExperimentLog.csv`. Cada fila de publicación contiene el archivo, Drive ID, fecha y hora planeadas, Page Post ID, Photo ID, permalink, estado `Programada` y la nota de que la publicación aún no se ha publicado. No se inventaron relaciones `CNT-####` para este lote; `ID_Pieza` permanece vacío hasta que exista una reconciliación documental explícita.

El log técnico bruto de las respuestas de Meta se conserva fuera del repositorio en `/home/ubuntu/facebook_schedule_api_results.jsonl` durante esta sesión. La fuente operativa permanente son los dos ledgers del repositorio y este informe.

## Drive e Instagram

Durante la programación, los archivos permanecieron en sus carpetas originales: no se movieron ni copiaron archivos en esa fase. Posteriormente, Fernando ejecutó el movimiento `MOVE_ONLY` de los 46 archivos a `08 Agosto`. La consulta posterior a Drive verificó 46/46 IDs en la carpeta destino y 0/46 restantes en las carpetas de origen; no se crearon copias. El manifiesto quedó en `MOVED_MANUALLY_VERIFIED`.

Instagram quedó fuera del alcance. No se llamó a la API de publicación de Instagram, no se modificó el scheduler `USM Instagram 15-16 Agosto` y no se generaron publicaciones para esa plataforma.

## Sustituciones comparables — 2026-08-21

Fernando autorizó los tres captions, la cancelación de las tres programaciones antiguas y la programación/publicación futura de los experimentos comparables en Facebook. Las tres programaciones antiguas fueron eliminadas y verificadas antes de crear los nuevos posts.

| Brief | Fecha/hora local | Meta Post ID | Meta Photo ID | Verificación |
|---|---|---|---|---|
| `FUT-MICRO-006` / `HB-007` | 2026-08-24 10:00, `America/Matamoros` | `1036844829507460_122154023721072582` | `122154023691072582` | `is_published=false`; horario confirmado |
| `FUT-MICRO-005` / `HB-006` | 2026-08-24 13:30, `America/Matamoros` | `1036844829507460_122154023781072582` | `122154023757072582` | `is_published=false`; horario confirmado |
| `FUT-ACID-003` / `HB-009` | 2026-08-27 16:00, `America/Matamoros` | `1036844829507460_122154023841072582` | `122154023817072582` | `is_published=false`; horario confirmado |

Los tres posts fueron añadidos a `2026-08-15_Publication_Log.csv` y al staging experimental. No se añadieron métricas, no se actualizó `ExperimentLog`, no se creó CNT y no se ejecutó Instagram, reuse ni afiliados.

## Sustituciones MEME-CAD — 22 de agosto de 2026

Fernando aprobó los cinco assets MEME-CAD y confirmó el reemplazo de tres reuse del calendario. Se cancelaron y verificaron como ausentes de `scheduled_posts` las tres publicaciones salientes; después se programaron los nuevos posts en Facebook con el mismo horario local y se verificó `is_published=false`.

| Fecha/hora local | Asset nuevo | Post saliente cancelado | Nuevo Meta Post ID | Nuevo Photo ID | Verificación |
|---|---|---|---|---|---|
| 2026-08-24 16:00 | `MEME-CAD-004_Wilfred_Tablero_v3.png` | `1036844829507460_122151376941072582` | `1036844829507460_122154732441072582` | `122154732411072582` | Horario correcto; `is_published=false`; saliente ausente |
| 2026-08-26 17:00 | `MEME-CAD-002_Fantasma_Sobrio_v1.png` | `1036844829507460_122151378063072582` | `1036844829507460_122154732501072582` | `122154732477072582` | Horario correcto; `is_published=false`; saliente ausente |
| 2026-08-27 17:00 | `MEME-CAD-003_Silvio_Karma_v3.png` | `1036844829507460_122151378573072582` | `1036844829507460_122154732567072582` | `122154732543072582` | Horario correcto; `is_published=false`; saliente ausente |

## Ampliación de cadencia 22–30 — 22 de agosto

Fernando aprobó aumentar la cadencia sin esperar al cierre mensual. Se añadieron cuatro slots sin cancelar filas existentes y Meta los verificó con `is_published=false`:

| Fecha/hora local | Asset | Tipo | Nuevo Meta Post ID | Nuevo Photo ID |
|---|---|---|---|---|
| 2026-08-22 22:00 | `Universe - Existencial 2607828.png` / `CNT-083` | Reuse adicional | `1036844829507460_122154733605072582` | `122154733581072582` |
| 2026-08-23 17:00 | `Universe - Existencial 2607787.png` / `CNT-081` | Reuse adicional | `1036844829507460_122154733665072582` | `122154733635072582` |
| 2026-08-28 16:00 | `MEME-CAD-001_Universe_Envidia_v1.png` | Nueva adicional | `1036844829507460_122154733719072582` | `122154733695072582` |
| 2026-08-29 16:00 | `MEME-CAD-005_Evan_Indirecta_Pregunta_v4.png` | Nueva adicional | `1036844829507460_122154733797072582` | `122154733755072582` |

La evidencia append-only completa está en `2026-08-22_Cadence_Expansion_22_30_Execution.json`. Instagram, Reels y afiliados permanecen fuera de esta ejecución.

## Próximas acciones

Después de que cada post se publique realmente, se debe completar `Fecha_Publicacion_Local` y `Hora_Publicacion_Local` en `Publication_Log.csv`, cambiar `Estado_Publicacion` a `Publicado`, registrar la hora real en `ExperimentLog.csv` y dejar que el reporte diario procese únicamente las filas elegibles. No se debe tratar el timestamp programado como una publicación ya realizada; las métricas de las cuatro adiciones se incorporarán desde el primer reporte diario posterior a su publicación.

## Referencias externas

[1]: https://developers.facebook.com/documentation/pages-api/posts "Meta Pages API — Posts"
[2]: https://developers.facebook.com/docs/graph-api/reference/page/photos/ "Meta Graph API v26.0 — Page Photos"
[3]: https://developers.facebook.com/docs/graph-api/reference/page/scheduled_posts/ "Meta Graph API v26.0 — Page Scheduled Posts"
