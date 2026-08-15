---
title: Auditoría directa de Instagram API — Universe Sent Me
purpose: Determinar por qué Instagram no se programó, separar el estado de Graph API del conector MCP y definir el flujo correcto para futuros posts.
status: Active
created: 2026-08-15
updated: 2026-08-15
version: 1.0
author: Manus AI
documents_related:
  - ../../GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md
  - ../../GrowthOS/10_00_Kit_de_Hashtags_USM.md
  - 2026-08-14_Recomendacion_Instagram_CGO.md
  - 2026-08-15_Calendario_15_16_Agosto.md
organization: Operations/Research
---

# Auditoría directa de Instagram API — Universe Sent Me

## Resumen ejecutivo

La auditoría se ejecutó **directamente contra Meta Graph API v26.0**, no mediante el conector MCP de Instagram. El resultado demuestra que la cuenta de Instagram no está desconectada de Graph API: el token identifica la Página correcta, encuentra la cuenta profesional vinculada, tiene los permisos de publicación declarados y puede leer media reciente.

El problema anterior fue de **separación de canales**. El mensaje `Instagram connector not connected` pertenecía al conector MCP, mientras que la API directa sí respondió correctamente. Además, en la operación del 15–16 de agosto solo se ejecutó el flujo de Facebook; no se creó un contenedor ni se llamó a `media_publish` para Instagram. Por eso Instagram no quedó programado.

## Evidencia de la auditoría

| Comprobación | Resultado |
|---|---|
| User Access Token | HTTP 200; `Fernando Gdlr` (`2920605591459033`) |
| Página derivada por `/me/accounts` | `Universe Sent Me` (`1036844829507460`) |
| Cuenta profesional vinculada | `universe_sent_me_0326` (`17841462696378190`) |
| Permisos | `instagram_basic`, `instagram_content_publish`, `pages_read_engagement`, `pages_manage_posts`, entre otros, en estado `granted` |
| Tareas de Página | `CREATE_CONTENT`, `MANAGE`, `MODERATE`, `ANALYZE`, entre otras |
| Lectura de identidad Instagram | HTTP 200; 42 seguidores y 460 piezas de media al momento de la auditoría |
| Lectura de media reciente | HTTP 200; devolvió Reels, imágenes y carruseles recientes |
| Cuota de publicación | HTTP 200; `quota_usage=0`, `quota_total=100`, `quota_duration=86400` |
| Publicación de Instagram el 15–16 | Prueba controlada ejecutada con 260583; `IG_CONTAINER_ID` y `IG_MEDIA_ID` registrados |

La cuenta, la vinculación y los permisos están operativos a nivel de Graph API. La cuota en cero no prueba por sí sola que una publicación sea posible, pero elimina saturación de cuota como causa del bloqueo observado.

## Causa del problema anterior

El flujo de Facebook se ejecutó correctamente con `/photos` y `/feed` usando el Page Access Token derivado de `/me/accounts`. El flujo de Instagram nunca llegó a ejecutarse. La columna `Instagram selectivo` del calendario funcionó como recomendación editorial, no como una orden independiente de publicación.

El intento posterior de verificar Instagram mediante el conector MCP devolvió `Instagram connector not connected`. Esa respuesta no contradice la auditoría de Graph API: son dos integraciones diferentes. Para futuros posts usaremos la API directa, como solicitó Fernando, y no dependeremos del conector MCP para publicar Instagram.

## Flujo correcto para futuros posts

Meta documenta, para Facebook Login, el uso de un **Facebook Page Access Token**, `instagram_basic`, `instagram_content_publish` y `pages_read_engagement`.[1] El usuario también debe tener tarea `MANAGE` o `CREATE_CONTENT` en la Página vinculada.[2]

El flujo operativo será el siguiente:

1. Resolver el Page Access Token en memoria mediante `/me/accounts` y seleccionar `Universe Sent Me` (`1036844829507460`).
2. Confirmar la cuenta profesional `17841462696378190` y consultar `content_publishing_limit` antes de crear contenedores.
3. Alojar el JPEG en una URL pública temporal. Meta indica que debe poder descargar el archivo desde un servidor público durante el intento.[1]
4. Crear un contenedor con `POST /{IG_ID}/media`, usando `image_url`, `caption` y los parámetros de formato necesarios.
5. Consultar el contenedor por `status_code` hasta que sea elegible.
6. Publicar con `POST /{IG_ID}/media_publish` y guardar el `IG_MEDIA_ID` devuelto.
7. Verificar la pieza publicada mediante `/media` y registrar permalink, estado y timestamp.
8. Solo después de confirmar el ID real, mover el original de Drive a la carpeta mensual, sin crear copias.

La API de Instagram documenta creación y publicación de contenedores, pero el calendario futuro no debe marcarse como `PROGRAMADO` solo por crear un contenedor. La prueba controlada creó el contenedor `17976335523089880`, alcanzó `FINISHED` y publicó correctamente el media `18105410684129991` en `https://www.instagram.com/p/DcDHxq5AMHh/`; PPA no bloqueó esta publicación. La prueba separada de programación futura con 2608030 para `2026-08-17T10:00:00-06:00` envió `scheduled_publish_time=1786982400` a `POST /17841462696378190/media` y Meta devolvió HTTP 400, código 3, `User must be on whitelist`. No se llamó a `media_publish`, no se publicó el asset y no se creó un contenedor.

## Checklist antes del primer post de prueba

| Control | Estado |
|---|---|
| API directa y token renovado | Confirmado |
| Página e Instagram vinculados | Confirmado |
| Permisos de publicación | Confirmado |
| Tarea `CREATE_CONTENT`/`MANAGE` | Confirmado |
| Cuota de publicación disponible | Confirmado |
| Page Publishing Authorization (PPA) | Superado en la prueba de 260583; no bloqueó la publicación |
| Prueba real de un asset aprobado | Completada con 260583; publicación verificada |
| Scheduler para ejecutar en horario futuro | Meta devolvió HTTP 400, código 3, `User must be on whitelist` al probar `scheduled_publish_time` |

La prueba de 260583 demuestra que PPA no bloqueó esta Página en esta operación. La respuesta `User must be on whitelist` indica que la capacidad de programación futura probada no está habilitada para esta ruta, app o cuenta; no es un fallo de permisos básicos ni de PPA. Por ahora, la única ruta confirmada es que Manus ejecute `media_publish` en el momento planificado mediante un scheduler externo autorizado.[1]

## Decisión operativa

Para futuros calendarios, Facebook e Instagram deben tener estados separados. Una fila con `Facebook; Instagram selectivo` no autoriza automáticamente ambas publicaciones. El CSV debe registrar `Meta_Post_ID` para Facebook y `IG_Container_ID`, `IG_Media_ID` y `IG_Permalink` para Instagram. Si Instagram no tiene un ID verificable, debe permanecer como `NO_EJECUTADO` o `PENDIENTE_PRUEBA`, nunca como `PROGRAMADO`.

## Referencias

[1]: https://developers.facebook.com/documentation/instagram-platform/content-publishing — Meta, Instagram Content Publishing.
[2]: https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-user/media_publish — Meta, IG User Media Publish.
[3]: https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-user/content_publishing_limit — Meta, IG User Content Publishing Limit.
