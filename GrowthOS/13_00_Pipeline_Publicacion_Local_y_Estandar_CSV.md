---
estado: Active
version: "1.8"
ultima_revision: 2026-08-23
dependencias:
  - GrowthOS/01_00_Arquitectura_Calendario_Escalable.md
  - GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md
  - Operations/Research/2026-08-15_Publication_Log.csv
  - Operations/Research/2026-08-15_ExperimentLog.csv
---

# Pipeline de Publicación Local (PyCharm + Gemini + Meta API) y Estándar de Exportación de Calendarios

**Propósito:** Documentar el pipeline de publicación real que usa Fernando (script propio en PyCharm, con Gemini, publicando vía Meta Graph API) y establecer el estándar de exportación CSV que cualquier calendario de Growth OS debe producir para poder alimentarlo directamente, sin reformateo manual.
**Estado:** Active
**Fecha de creación:** 2026-08-12
**Última actualización:** 2026-08-23
**Versión:** 1.49
**Autor:** Claude, documentando información provista por Fernando; actualización de Manus AI
**Documentos relacionados:** `01_00_Arquitectura_Calendario_Escalable.md`, `14_00_Fuente_Maestra_y_Ledgers.md`, `05_03_Calendario_10_16_Agosto.md` (y calendarios futuros), `Operations/Research/2026-08-15_Publication_Log.csv`, `Operations/Research/2026-08-15_ExperimentLog.csv`, `GrowthOS/00_01_Changelog_GrowthOS.md`, `GrowthOS/00_Índice.md`, `Operations/Automation/2026-08-23_Diseno_Captura_Baseline_E0_E24_E72.md`

---

## 1. Contexto — nuevos permisos de Meta API (2026-08-12)

Fernando confirmó la aprobación de los siguientes permisos de Meta for Developers (captura del panel de solicitud, 2026-08-12 01:07 CDT):

| Permiso | Habilita |
|---|---|
| `pages_manage_posts` | Publicar directamente en la página de Facebook vía API |
| `pages_show_list` | Listar páginas administradas (requisito técnico base) |
| `instagram_content_publish` | Publicar directamente en Instagram vía API |
| `pages_read_engagement` | Lectura ampliada de engagement |
| `public_profile` | Requisito técnico base |
| `instagram_basic` | Acceso base a la cuenta de Instagram vía API |
| `read_audience_network_insights` | Datos de audiencia más ricos (mencionado por Fernando, apareció junto con la aprobación anterior) |

Esto habilita técnicamente publicación automatizada real, no solo lectura de métricas.

## 2. Pipeline existente de Fernando

Fernando ya tiene un **script funcional en PyCharm, usando la API de Gemini, que publica de verdad vía Meta Graph API** — no es un prototipo, ya está en uso. Consume un archivo CSV/spreadsheet con la siguiente estructura confirmada (captura de pantalla provista 2026-08-12):

| Columna | Contenido | Ejemplo |
|---|---|---|
| `Fecha_Programada` | Fecha en formato M/D/AAAA | `4/8/2026` |
| `Hora` | Hora 24h | `10:00`, `16:30`, `18:00` |
| `Marca` | Marca/cuenta de destino — el pipeline es multi-marca, no exclusivo de Universe Sent Me | `Quirelli`, `Flexi` (ejemplos de otro proyecto de Fernando) |
| `Categoria` | Tipo de contenido | `Producto`, `Estilismo`, `Social` |
| `Archivo` | Solo el nombre del archivo, sin ruta | `IMG-20260318-WA0044.jpg`, `005_zapato_c1_quirelli_h.png` |
| `Ruta_Completa` | Ruta local completa del archivo en la carpeta de Drive sincronizada | `G:/My Drive/Universe sent me/flexi/Quirelli/...` |
| `Caption` | Texto del post | — |
| `Estado` | Estado de flujo del post | `BORRADOR` (visto en la muestra; probablemente existan otros estados como aprobado/publicado, no confirmado) |

**Nota importante:** el pipeline es **multi-marca** — Fernando lo usa para más de un proyecto (se vieron ejemplos de "Quirelli" y "Flexi", que no son Universe Sent Me). Esto significa que cualquier CSV generado para USM debe usar `Marca` = `Universe Sent Me` (o el valor exacto que Fernando ya usa para esa cuenta — no confirmado todavía) para que el script lo dirija a la cuenta correcta.

**Estado actual del pipeline:**
- **Ruta operativa:** Manus + Meta Graph API. Las guías de automatización heredadas no forman parte del flujo vigente.
- **Facebook Graph API:** programación real validada el 2026-08-15. El token de entorno se comporta como User Access Token; Manus deriva en memoria el Page Access Token mediante `/me/accounts`, selecciona la Página real `1036844829507460` y usa `/page_id/photos` para carga temporal seguida de `/page_id/feed` con `attached_media[0]`, `published=false`, `scheduled_publish_time` y `unpublished_content_type=SCHEDULED`. La primera prueba programó 9 posts correctamente y devolvió `is_published=false` en la verificación posterior.
- **Instagram Graph API:** auditoría directa completada el 2026-08-15. `@universe_sent_me_0326` (`17841462696378190`) responde HTTP 200, la Página está vinculada, `instagram_basic` e `instagram_content_publish` están concedidos, la Página devuelve `CREATE_CONTENT`/`MANAGE`, la lectura de media funciona y la cuota consultada está en `0/100` contenedores en 24 horas. La publicación inmediata de 260583 fue validada y luego eliminada manualmente; la programación nativa con `scheduled_publish_time` devolvió `User must be on whitelist`.
- **Ejecución:** Manus prepara, valida y ejecuta las órdenes de publicación mediante Graph API. En Facebook se usa la programación nativa de Page Feed. En Instagram se crea un contenedor en `/{ig_id}/media`, se verifica su estado y se publica mediante `/{ig_id}/media_publish`; cuando se requiera ejecución futura, este flujo se dispara mediante una tarea controlada en la hora `America/Mexico_City`. La tarea temporal del 15–16 quedó pausada después de la campaña, conserva el cron documentado, no tiene intervalo residual y mantiene solo Meta Graph API adjunta. El runner aplicó una ventana de 8 minutos y excluyó `260583` por `ELIMINADA_MANUALMENTE`. Las imágenes de campaña se alojaron una sola vez en URLs temporales; cada despertar reutilizó la URL preparada y no volvió a descargar, copiar ni subir archivos de Drive.
- **Token:** el conector contiene actualmente un token de usuario de larga duración. Manus deriva en memoria el Page Access Token de Universe Sent Me para llamadas de Página. Si el token expira o se revoca, la programación y lectura quedan bloqueadas hasta reemplazarlo.
- **Ruta de imagen:** el archivo usa **dos columnas separadas** — `Archivo` (solo filename) y `Ruta_Completa` (ruta local absoluta). Un calendario de Growth OS que quiera ser exportable a este formato necesita poder producir ambas, y la ruta completa depende de la carpeta real donde Fernando tiene cada asset (que varía por mes/proyecto, como ya se vio con las carpetas `05 Mayo`, `flexi/Quirelli`, etc.).

## 3. Archivado posterior a la publicación

La carpeta `My Drive/Universe sent me/USM/Humor existencial` es la entrada de memes nuevos. El archivo permanece en la raíz durante la preparación, aprobación y programación. Después de confirmar la publicación real mediante el ID de Meta, Manus registra `ID_Meta`, fecha y hora, plataforma, estado y métricas iniciales, y mueve el archivo a `Humor existencial/[Mes]`, conservando exactamente su nombre y número de referencia. En esa misma confirmación debe dispararse el evento de baseline E0: consultar `created_time` e `is_published`, leer los contadores actuales del objeto y registrar una fila `baseline_e0` en el ledger de snapshots. La hora planeada o la creación de una programación no constituyen E0.

Si la publicación falla o queda pendiente, el archivo no se mueve: permanece en la raíz con el estado correspondiente. Si una pieza se reutiliza en otro mes, se registra una nueva fila de publicación y el archivo se mueve a la carpeta del mes de la nueva publicación sin eliminar el historial anterior.

Este archivado organiza disponibilidad y trazabilidad, pero no sustituye el registro de Meta. Para decidir reuse, la fuente prioritaria sigue siendo el historial real de publicaciones y métricas, no únicamente la ubicación del archivo.

### 3.1 Enganche E0 y publicaciones programadas

El publicador debe emitir un evento interno posterior a la verificación de `is_published=true`. El consumidor del evento captura E0 con la misma identidad `Meta_Post_ID`, `Publicacion_ID`, `Experiment_ID` y `CNT`, y escribe primero en `Metrics_Snapshot_Log.csv`; después puede añadir una nota de estado a `Publication_Log.csv`. La clave idempotente es `Meta_Post_ID + baseline_e0`. Si el post fue programado, el evento queda pendiente hasta que Meta confirme la publicación efectiva; nunca se usa `scheduled_publish_time` como `Published_At_UTC`.

Los fallos de captura se registran como intentos separados con `E0_Pending`, `E0_Late` o `E0_Missing`. Un error de token, un campo de contador ausente o una captura fuera de tolerancia no autoriza a rellenar `Interacciones_24h`/`Interacciones_72h`; el worker E24/E72 solo puede calcular deltas cuando exista un E0 válido. El diseño completo, incluyendo el ledger, tolerancias, reintentos y fallback para publicaciones manuales, está en `Operations/Automation/2026-08-23_Diseno_Captura_Baseline_E0_E24_E72.md`.

## 4. Fuente maestra y registro de aprendizaje

La identidad de la pieza se conserva en `GrowthOS/Content_Inventory.csv`. Cada publicación ejecutada se agrega a `Operations/Research/2026-08-15_Publication_Log.csv`, una fila por plataforma y orden real de Meta. Las métricas de 24/72 horas y las conclusiones se agregan a `Operations/Research/2026-08-15_ExperimentLog.csv`. El calendario es una vista de planificación/exportación y no debe convertirse en una segunda base de datos.

Para minimizar consumo de tokens, la extracción post-publicación debe consultar solo los `Meta_ID` nuevos o modificados desde la última sincronización. La carpeta de Drive sirve para archivado físico; no sustituye `Publication_Log` ni el historial de Meta.

## 5. Implicación directa para Growth OS

**A partir de este documento, cualquier calendario que se entregue como "listo para publicar" (no solo como tabla de planeación) debe poder exportarse a esta estructura de 8 columnas** — no basta con la tabla en markdown que se ha usado hasta ahora en los calendarios semanales (`05_02`, `05_03`, etc.). La tabla markdown sigue siendo útil para revisión y aprobación entre Fernando y Claude/Manus, pero el entregable final operativo es este formato.

**Regla práctica:** el valor de `Archivo` usado en cualquier calendario (ej. al referenciar un post de reuse por su código `260579.png`) debe coincidir exactamente con el nombre real del archivo tal como existe en la carpeta local de Fernando — nunca inventar o asumir un nombre distinto. La `Ruta_Completa` correspondiente debe confirmarse con Fernando o inferirse de la convención de carpetas ya vista (`Universe sent me/USM/Humor existencial/[Mes]/`), nunca asumirse a ciegas. Cuando el archivo no se ha visto directamente (solo se conoce su descripción), el CSV no debe generarse hasta confirmar el nombre exacto con Fernando.

## 5. Custom API de Meta configurada en Manus

El 2026-08-14 se creó y activó el conector **Universe Sent Me Meta API**, una Custom API REST para Facebook e Instagram de Universe Sent Me. El valor entregado para el conector se comporta como un **Facebook User Access Token**: `GET /me` devuelve `Fernando Gdlr`, y `/me/accounts` permite obtener el Page Access Token de Universe Sent Me. Aunque la variable configurada se llama `META_PAGE_ACCESS_TOKEN`, su valor actual es el token de usuario; no debe asumirse que sirve directamente para todas las operaciones de la página. El secreto se almacena en el entorno seguro de Manus; no forma parte de este repositorio ni debe copiarse a documentos, commits, capturas o mensajes públicos.

| Elemento | Configuración |
|---|---|
| Nombre del conector | `Universe Sent Me Meta API` |
| Tipo | Custom API / REST |
| URL base | `https://graph.facebook.com` |
| Autenticación | Encabezado `Authorization: Bearer $META_PAGE_ACCESS_TOKEN` |
| Verificación realizada | `GET /me?fields=id,name` |
| Resultado de verificación | HTTP 200; identidad de usuario: `Fernando Gdlr`, ID `2920605591459033`; Página derivada: `Universe Sent Me`, ID `1036844829507460` |
| Operaciones previstas | Identidad de página, publicaciones, insights y publicación en feed únicamente con solicitud explícita y confirmación previa |
| Página Universe Sent Me | ID `1036844829507460`; tareas: `MODERATE`, `CREATE_CONTENT`, `MESSAGING`, `ANALYZE`, entre otras |
| Instagram vinculado | Cuenta profesional ID `17841462696378190` |
| Permisos efectivos concedidos | `pages_show_list`, `business_management`, `instagram_basic`, `instagram_content_publish`, `instagram_manage_comments`, `pages_read_engagement`, `pages_read_user_content`, `pages_manage_posts`, `pages_manage_engagement`, `read_audience_network_insights`, `public_profile` |
| Permiso no devuelto por el token actual para comentarios de Facebook | `pages_read_user_engagement` — la lectura real de comentarios sí respondió HTTP 200, por lo que queda como diferencia documentada y no como bloqueo activo |
| Prueba de lectura Facebook | HTTP 200 con comentarios de una publicación de Universe Sent Me |
| Prueba de lectura Instagram | HTTP 200 en el medio consultado; no había comentarios devueltos |


> La creación del conector quedó confirmada por el usuario. El 2026-08-15 se corrigió un diagnóstico inicial: `2920605591459033` es la identidad del usuario, no el ID de la Página. Usar ese ID en `/photos` produjo el error engañoso sobre `publish_actions`; la Página correcta es `1036844829507460`, derivada desde `/me/accounts`, con tareas `CREATE_CONTENT` y `MANAGE`. Con el Page Access Token correcto se programaron 9 publicaciones y se verificaron sus IDs. La Custom API no autoriza por sí sola ninguna publicación: cualquier operación de escritura debe solicitarse expresamente y confirmarse antes de ejecutarse.

### Comentarios: diagnóstico operativo

**Facebook:** el conjunto actual permite el flujo de lectura y deja preparada la moderación: `pages_manage_engagement` y `pages_read_engagement` están concedidos, la página devuelve las tareas `MODERATE` y `CREATE_CONTENT`, y se verificó HTTP 200 leyendo comentarios de publicaciones propias. En un escaneo de 20 publicaciones recientes se encontraron 67 comentarios, con comentarios en 16 publicaciones. La guía específica de Meta también menciona `pages_read_user_engagement`, que no aparece en el token actual; aun así, la lectura real funciona. Las respuestas, ocultamientos o eliminaciones aún no se han probado y deben ejecutarse solo con confirmación explícita.

**Instagram:** la auditoría de permisos del 2026-08-15 devolvió también `instagram_manage_comments` como concedido. Esto corrige el diagnóstico anterior de permiso ausente. La publicación y la moderación de Instagram siguen siendo flujos separados; no se automatizarán respuestas allí hasta diseñar y probar su propio playbook.

### Seguridad y mantenimiento

El token debe rotarse si se sospecha exposición, si cambia el administrador o si Meta lo invalida. Al actualizarlo, debe modificarse únicamente la credencial almacenada en el conector; este documento debe conservar solo el nombre de la variable y no el valor secreto. Los endpoints y campos no deben asumirse: deben comprobarse en la documentación oficial de [Graph API][1] y [Pages API][2], especialmente porque Meta puede retirar o cambiar métricas y permisos por versión.

## 6. Pendientes de definición (no resueltos en esta sesión)

1. **Valor exacto de `Marca` para Universe Sent Me** — no confirmado; los ejemplos vistos son de otro proyecto de Fernando (Quirelli/Flexi).
2. **Valores posibles de `Estado`** más allá de `BORRADOR` (¿aprobado, publicado, error?) — no confirmado.
3. **Valores esperados de `Categoria`** para USM — los ejemplos vistos (Producto, Estilismo, Social) son de un proyecto de e-commerce, probablemente no aplican directamente a memes/reels de USM. Necesita mapeo propio (ej. Meme, Reel, Carrusel) o confirmación de que la columna acepta cualquier texto libre.
4. **Multi-plataforma:** cómo se resolverá la publicación en Instagram una vez integrada — columna nueva, o pipeline separado. Fernando mencionó estar abierto a cambiar el formato de CSV a Markdown; no se definió si eso reemplazaría esta estructura o coexistiría con ella.
5. **Validación pre-publicación:** no se definió si el pipeline de Fernando valida que el archivo exista en `Ruta_Completa` antes de intentar publicar, o si eso quedaría como responsabilidad de quien arma el calendario.

## 7. Qué NO cambia por ahora

- El proceso de armar el calendario (elegir personaje, horario, copy, hashtags, reuse vs. nuevo) sigue siendo el mismo ya documentado en `01_00_Arquitectura_Calendario_Escalable.md` y aplicado en los calendarios semanales.
- Este documento no reemplaza ni automatiza nada todavía — solo dejar registrado el pipeline real de Fernando para que futuros calendarios se diseñen ya pensando en ser exportables a este formato, en vez de descubrir la incompatibilidad después.

---

## Referencias

[1]: https://developers.facebook.com/docs/graph-api/get-started/ "Meta for Developers — Get Started with Graph API"
[2]: https://developers.facebook.com/documentation/pages-api "Meta for Developers — Pages API"
[3]: https://developers.facebook.com/documentation/pages-api/comments-mentions "Meta for Developers — Comments and @mentions"
[4]: https://developers.facebook.com/documentation/instagram-platform/comment-moderation "Meta for Developers — Instagram Comment Moderation"
[5]: https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-media/comments "Meta for Developers — Instagram Media Comments"
[6]: https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-comment/replies "Meta for Developers — IG Comment Replies"
