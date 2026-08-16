# Programación Facebook 17–30 de agosto — Meta Graph API

**Propósito:** Registrar la programación real de los 74 slots aprobados del calendario operativo de Universe Sent Me mediante la Meta Graph API y dejar trazabilidad de los Page Post IDs, Photo IDs, verificaciones, estado de Drive y alcance de Instagram.

**Estado:** Active
**Fecha de creación:** 2026-08-16
**Última actualización:** 2026-08-16
**Versión:** 1.1
**Autor:** Manus AI
**Documentos relacionados:** `2026-08-16_Calendario_Operativo_17_30_Agosto.csv`, `2026-08-16_Asignacion_Visual_Calendario_17_30_Agosto.csv`, `2026-08-15_Publication_Log.csv`, `2026-08-15_ExperimentLog.csv`, `2026-08-16_Manifiesto_Movimiento_35_Memes_Agosto.csv`, `GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md`

---

## Resultado ejecutivo

El 16 de agosto de 2026 se programaron **74 publicaciones de Facebook** para el periodo del 17 al 30 de agosto, usando la Página `Universe Sent Me` (`1036844829507460`) y la API Graph v26.0. Meta documenta la programación mediante `published=false` y `scheduled_publish_time` en Pages API [1], el flujo de foto temporal y `temporary=true` en Page Photos [2], y la lectura de posts programados mediante `/scheduled_posts` [3]. Meta devolvió un Page Post ID y un Photo ID para cada slot; las 74 verificaciones posteriores confirmaron el `scheduled_publish_time` esperado, el mensaje correspondiente y `is_published=false`.

| Control | Resultado |
|---|---:|
| Slots programados | **74/74** |
| Page Post IDs reales | **74/74** |
| Photo IDs reales | **74/74** |
| Verificaciones de lectura posteriores | **74/74** |
| Errores finales | **0** |
| Assets excluidos | `260583` — no apareció en el lote |
| Movimientos en Drive | **0** |
| Copias creadas en Drive | **0** |
| Cambios en Instagram | **0** |

La distribución diaria quedó documentada en el calendario maestro: 6 posts el 17, 6 el 18, 6 el 19, 6 el 20, 4 el 21, 4 el 22, 5 el 23, 6 el 24, 6 el 25, 6 el 26, 6 el 27, 4 el 28, 4 el 29 y 5 el 30 de agosto.

## Flujo técnico ejecutado

El flujo validado fue de dos pasos. Primero, cada imagen se cargó a `/{page_id}/photos` como foto temporal con `published=false` y `temporary=true`. Después, se creó el post en `/{page_id}/feed` utilizando `attached_media[0]`, `published=false`, `scheduled_publish_time` y `unpublished_content_type=SCHEDULED`. El Page Access Token se derivó en memoria desde `/me/accounts`; no se almacenaron tokens en el repositorio.

Una primera variante que intentaba enviar directamente `scheduled_publish_time` junto con la carga de la foto fue rechazada por Meta con un error genérico. Se sustituyó por el flujo oficial de foto temporal más post programado, que produjo **74/74 respuestas exitosas** y verificaciones correctas.

## Registro de hechos

Los registros completos se encuentran en `Operations/Research/2026-08-15_Publication_Log.csv` y `Operations/Research/2026-08-15_ExperimentLog.csv`. Cada fila de publicación contiene el archivo, Drive ID, fecha y hora planeadas, Page Post ID, Photo ID, permalink, estado `Programada` y la nota de que la publicación aún no se ha publicado. No se inventaron relaciones `CNT-####` para este lote; `ID_Pieza` permanece vacío hasta que exista una reconciliación documental explícita.

El log técnico bruto de las respuestas de Meta se conserva fuera del repositorio en `/home/ubuntu/facebook_schedule_api_results.jsonl` durante esta sesión. La fuente operativa permanente son los dos ledgers del repositorio y este informe.

## Drive e Instagram

Durante la programación, los archivos permanecieron en sus carpetas originales: no se movieron ni copiaron archivos en esa fase. Posteriormente, Fernando ejecutó el movimiento `MOVE_ONLY` de los 46 archivos a `08 Agosto`. La consulta posterior a Drive verificó 46/46 IDs en la carpeta destino y 0/46 restantes en las carpetas de origen; no se crearon copias. El manifiesto quedó en `MOVED_MANUALLY_VERIFIED`.

Instagram quedó fuera del alcance. No se llamó a la API de publicación de Instagram, no se modificó el scheduler `USM Instagram 15-16 Agosto` y no se generaron publicaciones para esa plataforma.

## Próximas acciones

Después de que cada post se publique realmente, se debe completar `Fecha_Publicacion_Local` y `Hora_Publicacion_Local` en `Publication_Log.csv`, cambiar `Estado_Publicacion` a `Publicado`, registrar la hora real en `ExperimentLog.csv` y dejar que la extracción 24/72 horas procese únicamente las filas elegibles. El extractor fue actualizado para reconocer observaciones `OBS-FB-17_30-*`; no debe tratar el timestamp programado como una publicación ya realizada.

## Referencias externas

[1]: https://developers.facebook.com/documentation/pages-api/posts "Meta Pages API — Posts"
[2]: https://developers.facebook.com/docs/graph-api/reference/page/photos/ "Meta Graph API v26.0 — Page Photos"
[3]: https://developers.facebook.com/docs/graph-api/reference/page/scheduled_posts/ "Meta Graph API v26.0 — Page Scheduled Posts"
