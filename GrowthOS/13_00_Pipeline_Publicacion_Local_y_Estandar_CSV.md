---
estado: Active
version: "1.2"
ultima_revision: 2026-08-14
dependencias:
  - GrowthOS/01_00_Arquitectura_Calendario_Escalable.md
---

# Pipeline de Publicación Local (PyCharm + Gemini + Meta API) y Estándar de Exportación de Calendarios

**Propósito:** Documentar el pipeline de publicación real que usa Fernando (script propio en PyCharm, con Gemini, publicando vía Meta Graph API) y establecer el estándar de exportación CSV que cualquier calendario de Growth OS debe producir para poder alimentarlo directamente, sin reformateo manual.
**Estado:** Active
**Fecha de creación:** 2026-08-12
**Última actualización:** 2026-08-14
**Versión:** 1.2
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
- **Facebook:** integrado y funcional.
- **Instagram:** no integrado todavía en el script — pendiente. No hay columna de plataforma en la estructura vista; probablemente porque hasta ahora cada fila se publica en Facebook por default.
- **Ruta de imagen:** el archivo usa **dos columnas separadas** — `Archivo` (solo filename) y `Ruta_Completa` (ruta local absoluta). Un calendario de Growth OS que quiera ser exportable a este formato necesita poder producir ambas, y la ruta completa depende de la carpeta real donde Fernando tiene cada asset (que varía por mes/proyecto, como ya se vio con las carpetas `05 Mayo`, `flexi/Quirelli`, etc.).

## 3. Implicación directa para Growth OS

**A partir de este documento, cualquier calendario que se entregue como "listo para publicar" (no solo como tabla de planeación) debe poder exportarse a esta estructura de 8 columnas** — no basta con la tabla en markdown que se ha usado hasta ahora en los calendarios semanales (`05_02`, `05_03`, etc.). La tabla markdown sigue siendo útil para revisión y aprobación entre Fernando y Claude/Manus, pero el entregable final operativo es este formato.

**Regla práctica:** el valor de `Archivo` usado en cualquier calendario (ej. al referenciar un post de reuse por su código `260579.png`) debe coincidir exactamente con el nombre real del archivo tal como existe en la carpeta local de Fernando — nunca inventar o asumir un nombre distinto. La `Ruta_Completa` correspondiente debe confirmarse con Fernando o inferirse de la convención de carpetas ya vista (`Universe sent me/USM/Humor existencial/[Mes]/`), nunca asumirse a ciegas. Cuando el archivo no se ha visto directamente (solo se conoce su descripción), el CSV no debe generarse hasta confirmar el nombre exacto con Fernando.

## 4. Custom API de Meta configurada en Manus

El 2026-08-14 se creó y activó el conector **Universe Sent Me Meta API**, una Custom API REST para la página de Facebook de Universe Sent Me. El conector utiliza el entorno seguro de Manus para almacenar el secreto como `META_PAGE_ACCESS_TOKEN`; el token no forma parte de este repositorio ni debe copiarse a documentos, commits, capturas o mensajes públicos.

| Elemento | Configuración |
|---|---|
| Nombre del conector | `Universe Sent Me Meta API` |
| Tipo | Custom API / REST |
| URL base | `https://graph.facebook.com` |
| Autenticación | Encabezado `Authorization: Bearer $META_PAGE_ACCESS_TOKEN` |
| Verificación realizada | `GET /me?fields=id,name` |
| Resultado de verificación | HTTP 200; identidad devuelta: `Fernando Gdlr`, ID `2920605591459033` |
| Operaciones previstas | Identidad de página, publicaciones, insights y publicación en feed únicamente con solicitud explícita y confirmación previa |

> La creación del conector quedó confirmada por el usuario. La verificación posterior respondió correctamente con HTTP 200. La Custom API no autoriza por sí sola ninguna publicación: cualquier operación de escritura debe solicitarse expresamente y confirmarse antes de ejecutarse.

### Seguridad y mantenimiento

El token debe rotarse si se sospecha exposición, si cambia el administrador o si Meta lo invalida. Al actualizarlo, debe modificarse únicamente la credencial almacenada en el conector; este documento debe conservar solo el nombre de la variable y no el valor secreto. Los endpoints y campos no deben asumirse: deben comprobarse en la documentación oficial de [Graph API][1] y [Pages API][2], especialmente porque Meta puede retirar o cambiar métricas y permisos por versión.

## 5. Pendientes de definición (no resueltos en esta sesión)

1. **Valor exacto de `Marca` para Universe Sent Me** — no confirmado; los ejemplos vistos son de otro proyecto de Fernando (Quirelli/Flexi).
2. **Valores posibles de `Estado`** más allá de `BORRADOR` (¿aprobado, publicado, error?) — no confirmado.
3. **Valores esperados de `Categoria`** para USM — los ejemplos vistos (Producto, Estilismo, Social) son de un proyecto de e-commerce, probablemente no aplican directamente a memes/reels de USM. Necesita mapeo propio (ej. Meme, Reel, Carrusel) o confirmación de que la columna acepta cualquier texto libre.
4. **Multi-plataforma:** cómo se resolverá la publicación en Instagram una vez integrada — columna nueva, o pipeline separado. Fernando mencionó estar abierto a cambiar el formato de CSV a Markdown; no se definió si eso reemplazaría esta estructura o coexistiría con ella.
5. **Validación pre-publicación:** no se definió si el pipeline de Fernando valida que el archivo exista en `Ruta_Completa` antes de intentar publicar, o si eso quedaría como responsabilidad de quien arma el calendario.

## 6. Qué NO cambia por ahora

- El proceso de armar el calendario (elegir personaje, horario, copy, hashtags, reuse vs. nuevo) sigue siendo el mismo ya documentado en `01_00_Arquitectura_Calendario_Escalable.md` y aplicado en los calendarios semanales.
- Este documento no reemplaza ni automatiza nada todavía — solo dejar registrado el pipeline real de Fernando para que futuros calendarios se diseñen ya pensando en ser exportables a este formato, en vez de descubrir la incompatibilidad después.

---

## Referencias

[1]: https://developers.facebook.com/docs/graph-api/get-started/ "Meta for Developers — Get Started with Graph API"
[2]: https://developers.facebook.com/documentation/pages-api "Meta for Developers — Pages API"
