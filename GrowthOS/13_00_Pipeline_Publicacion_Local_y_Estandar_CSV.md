---
estado: Active
version: "1.7"
ultima_revision: 2026-08-15
dependencias:
  - GrowthOS/01_00_Arquitectura_Calendario_Escalable.md
---

# Pipeline de Publicación Local (PyCharm + Gemini + Meta API) y Estándar de Exportación de Calendarios

**Propósito:** Documentar el pipeline de publicación real que usa Fernando (script propio en PyCharm, con Gemini, publicando vía Meta Graph API) y establecer el estándar de exportación CSV que cualquier calendario de Growth OS debe producir para poder alimentarlo directamente, sin reformateo manual.
**Estado:** Active
**Fecha de creación:** 2026-08-12
**Última actualización:** 2026-08-14
**Versión:** 1.5
**Autor:** Claude, documentando información provista por Fernando; actualización de Manus AI
**Documentos relacionados:** `01_00_Arquitectura_Calendario_Escalable.md`, `05_03_Calendario_10_16_Agosto.md` (y calendarios futuros), `GrowthOS/00_01_Changelog_GrowthOS.md`, `GrowthOS/00_Índice.md`

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
- **Make:** retirado de la estrategia operativa. La guía histórica se conserva en `02_00_Guia_Automatizacion_Make.md` con estado `Archived`.
- **Facebook Graph API:** programación real validada el 2026-08-15. El token de entorno se comporta como User Access Token; Manus deriva en memoria el Page Access Token mediante `/me/accounts`, selecciona la Página real `1036844829507460` y usa `/page_id/photos` para carga temporal seguida de `/page_id/feed` con `attached_media[0]`, `published=false`, `scheduled_publish_time` y `unpublished_content_type=SCHEDULED`. La primera prueba programó 9 posts correctamente y devolvió `is_published=false` en la verificación posterior.
- **Instagram Graph API:** auditoría directa completada el 2026-08-15. `@universe_sent_me_0326` (`17841462696378190`) responde HTTP 200, la Página está vinculada, `instagram_basic` e `instagram_content_publish` están concedidos, la Página devuelve `CREATE_CONTENT`/`MANAGE`, la lectura de media funciona y la cuota consultada está en `0/100` contenedores en 24 horas. La publicación inmediata de 260583 fue validada y luego eliminada manualmente; la programación nativa con `scheduled_publish_time` devolvió `User must be on whitelist`.
- **Ejecución:** Manus prepara, valida y ejecuta las órdenes de publicación mediante Graph API. En Facebook se usa la programación nativa de Page Feed. En Instagram se crea un contenedor en `/{ig_id}/media`, se verifica su estado y se publica mediante `/{ig_id}/media_publish`; la ejecución futura se resuelve disparando este flujo mediante un scheduler externo en la hora `America/Mexico_City`. El scheduler temporal de 15–16 está activo hasta `2026-08-17T04:30:00Z`, con cron `0 0,30 11,14,17,20 15,16 8 *` en `America/Matamoros`, equivalente a los cinco slots aprobados en `America/Mexico_City`. El runner aplica una ventana de 8 minutos y excluye `260583` por `ELIMINADA_MANUALMENTE`.
- **Token:** se usan tokens temporales. El token almacenado en el conector es un token de usuario; Manus deriva en memoria el Page Access Token de Universe Sent Me para llamadas de Página. Si el token expira, la programación y lectura quedan bloqueadas hasta reemplazarlo.
- **Ruta de imagen:** el archivo usa **dos columnas separadas** — `Archivo` (solo filename) y `Ruta_Completa` (ruta local absoluta). Un calendario de Growth OS que quiera ser exportable a este formato necesita poder producir ambas, y la ruta completa depende de la carpeta real donde Fernando tiene cada asset (que varía por mes/proyecto, como ya se vio con las carpetas `05 Mayo`, `flexi/Quirelli`, etc.).

## 3. Archivado posterior a la publicación

La carpeta `My Drive/Universe sent me/USM/Humor existencial` es la entrada de memes nuevos. El archivo permanece en la raíz durante la preparación, aprobación y programación. Después de confirmar la publicación real mediante el ID de Meta, Manus registra `ID_Meta`, fecha y hora, plataforma, estado y métricas iniciales, y mueve el archivo a `Humor existencial/[Mes]`, conservando exactamente su nombre y número de referencia.

Si la publicación falla o queda pendiente, el archivo no se mueve: permanece en la raíz con el estado correspondiente. Si una pieza se reutiliza en otro mes, se registra una nueva fila de publicación y el archivo se mueve a la carpeta del mes de la nueva publicación sin eliminar el historial anterior.

Este archivado organiza disponibilidad y trazabilidad, pero no sustituye el registro de Meta. Para decidir reuse, la fuente prioritaria sigue siendo el historial real de publicaciones y métricas, no únicamente la ubicación del archivo.

## 4. Implicación directa para Growth OS

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
| Permisos efectivos concedidos | `pages_show_list`, `business_management`, `instagram_basic`, `instagram_content_publish`, `pages_read_engagement`, `pages_read_user_content`, `pages_manage_posts`, `pages_manage_engagement`, `read_audience_network_insights`, `public_profile` |
| Permiso ausente para comentarios de Instagram | `instagram_manage_comments` |
| Prueba de lectura Facebook | HTTP 200 con comentarios de una publicación de Universe Sent Me |
| Prueba de lectura Instagram | HTTP 200 en el medio consultado; no había comentarios devueltos |


> La creación del conector quedó confirmada por el usuario. El 2026-08-15 se corrigió un diagnóstico inicial: `2920605591459033` es la identidad del usuario, no el ID de la Página. Usar ese ID en `/photos` produjo el error engañoso sobre `publish_actions`; la Página correcta es `1036844829507460`, derivada desde `/me/accounts`, con tareas `CREATE_CONTENT` y `MANAGE`. Con el Page Access Token correcto se programaron 9 publicaciones y se verificaron sus IDs. La Custom API no autoriza por sí sola ninguna publicación: cualquier operación de escritura debe solicitarse expresamente y confirmarse antes de ejecutarse.

### Comentarios: diagnóstico operativo

**Facebook:** el conjunto actual es suficiente para el flujo principal de moderación y respuesta a comentarios de la página: `pages_manage_engagement` está concedido, la página devuelve la tarea `MODERATE` y se verificó con HTTP 200 la lectura de comentarios usando el Page Access Token derivado desde `/me/accounts`. La documentación actual de Meta también menciona `pages_read_engagement` y, según el flujo, `pages_read_user_engagement`; si una operación concreta devuelve un error de permisos sobre contenido generado por usuarios, habrá que revisar esa diferencia porque el token actual muestra `pages_read_user_content`, no `pages_read_user_engagement`.

**Instagram:** la cuenta profesional está vinculada y `instagram_basic` está concedido, pero falta **`instagram_manage_comments`**, que Meta exige para leer, gestionar y responder comentarios mediante la API de Instagram con Facebook Login. Por tanto, **todavía no debemos automatizar respuestas en Instagram**. Para habilitarlo, hay que solicitar/conceder `instagram_manage_comments` en la aplicación de Meta y volver a generar o reautorizar el token con ese permiso. La respuesta documentada por Meta usa `POST /<IG_COMMENT_ID>/replies` para responder a un comentario, con `instagram_basic`, `instagram_manage_comments` y `pages_read_engagement`.

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
