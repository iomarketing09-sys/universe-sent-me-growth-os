---
title: "Lista de confirmación manual de assets de julio"
purpose: "Acelerar la reconciliación de los top posts de julio mediante la captura manual del Asset_Ref y filename exactos visibles en Drive, sin inventar relaciones CNT."
status: "Review"
created: 2026-08-17
updated: 2026-08-17
version: "1.2"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/Historical_Performance_Individuals.csv"
  - "Operations/Research/Historical_Asset_Performance.csv"
  - "Operations/Research/2026-08-17_Reconciliacion_Historicos_Individuales.md"
  - "GrowthOS/Content_Inventory.csv"
organization: "Operations/Research"
---

# Lista de confirmación manual de assets de julio

## Propósito operativo

Esta lista contiene los **seis top posts de julio** que ya tienen Meta ID, fecha y métricas históricas, pero todavía no tienen un `Asset_Ref` confirmado en el inventario maestro. El usuario puede localizar cada imagen en la carpeta correspondiente de Drive y devolver el identificador numérico visible en el filename, por ejemplo `2607936`.

La confirmación manual debe registrar el `Asset_Ref` exacto y, de ser posible, copiar también el filename completo. No es necesario mover, copiar, renombrar ni modificar archivos de Drive. La relación solo se integrará después de comprobar que el archivo visual corresponde al post de Meta.

## Lista para completar

| # | Fecha | Caption o descripción del post | Meta ID | Interacciones | Reacciones | Comentarios | Shares | Asset_Ref manual | Filename exacto en Drive | Estado |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|
| 1 | 2026-07-18 | `🫣🫣 #UniverseSentMe` | `1036844829507460_122140003413072582` | 5,482 | 3,108 | 62 | 2,312 | **Por confirmar** | **Por confirmar** | Pending_Evidence |
| 2 | 2026-07-28 | `No es desinterés... #UnvierseSentMe #FantasmaUSM #humor #memesUSM` | `1036844829507460_122142779757072582` | 3,726 | 2,367 | 18 | 1,341 | **Por confirmar** | **Por confirmar** | Pending_Evidence |
| 3 | 2026-07-27 | `😭🫣 #UniverseSentMe #humoracido #memesUSM` | `1036844829507460_122142627051072582` | 2,979 | 2,249 | 16 | 714 | **Por confirmar** | **Por confirmar** | Pending_Evidence |
| 4 | 2026-07-21 | `🥴🤯 escucho borroso.... #UniverseSentMe #humor #memesenespañol #conversacion #relatable #vidareal #meditacion` | `1036844829507460_122140844349072582` | 3,913 | 2,290 | 102 | 1,521 | **Por confirmar** | **Por confirmar** | Pending_Evidence |
| 5 | 2026-07-18 | `😐` | `1036844829507460_122139999861072582` | 3,993 | 2,536 | 8 | 1,449 | **Por confirmar** | **Por confirmar** | Pending_Evidence |
| 6 | 2026-07-22 | `🙂‍↕️ #UniverseSentMe #humor #memesenespañol #relatable #vidareal #meditacion` | `1036844829507460_122141207841072582` | 2,747 | 1,722 | 10 | 1,015 | **Por confirmar** | **Por confirmar** | Pending_Evidence |

## Estado de la lista recibida

El usuario completó las seis filas con una referencia de asset y la carpeta `My Drive\\Universe sent me\\USM\\Humor existencial\\07 Julio`. Las referencias normalizadas son `260604`, `2607987`, `729`, `260504`, `728` y `2607966`. Como no se proporcionó el filename completo, la tabla conserva el texto original en `asset_ref_manual`, separa la carpeta en `drive_folder_manual` y añade `asset_ref_normalized`. El estado actual es `User_Provided_Ref_Folder`: suficiente para iniciar el cruce, pero no equivale todavía a `Confirmed_CNT`.

## Instrucciones para devolver la confirmación

La respuesta más eficiente puede tener este formato:

```text
1. Meta ID 1036844829507460_122140003413072582 → Asset_Ref 2607XXX → filename completo
2. Meta ID 1036844829507460_122142779757072582 → Asset_Ref 2607XXX → filename completo
...
```

Si un post no aparece en Drive o hay dos variantes parecidas, debe marcarse como `No encontrado` o `Ambiguo`; no se debe elegir por parecido de personaje, color o caption. La experiencia con los cinco posts de junio demuestra que los archivos históricos pueden haber sido movidos posteriormente a una carpeta operativa, por lo que la búsqueda debe incluir los manifiestos de movimiento y las carpetas de reuse.

## Resultado de la búsqueda automática en Drive

La carpeta `My Drive\\Universe sent me\\USM\\Humor existencial\\07 Julio` fue recorrida con los seis `Asset_Ref`. Se encontró exactamente un archivo para cada referencia; no hubo duplicados dentro de esa carpeta.

| Asset_Ref | Filename exacto | Drive ID | Tipo | Estado |
|---|---|---|---|---|
| `260604` | `Universe - Existencial 260604.png` | `1WXH7_KH4jdhFcqnGDYRGrHtKRNI6VD77` | PNG | Filename_Confirmed_Drive |
| `2607987` | `Universe - Existencial 2607987.jpeg` | `1CeJ4UYYlU1I7ecJtYtgLOYBzHXyVc9sm` | JPEG | Filename_Confirmed_Drive |
| `729` | `Universe - Existencial 729.png` | `1n9mj2FnGRv0kbEbEHk2RV1KKJDeSQTxk` | PNG | Filename_Confirmed_Drive |
| `260504` | `Universe - Existencial 260504.png` | `1V6q1qygkALahU-HqNSJP-rmIwI-t0m16` | PNG | Filename_Confirmed_Drive |
| `728` | `Universe - Existencial 728.png` | `1aV1bNoJpaXjtdZEQExebSj6i4SkXhVWr` | PNG | Filename_Confirmed_Drive |
| `2607966` | `Universe - Existencial 2607966.jpeg` | `1r6TG0yLNQAlVF8RL0XfqbevmobIVd89m` | JPEG | Filename_Confirmed_Drive |

La búsqueda confirma el archivo y su unicidad, pero todavía no demuestra por sí sola que la imagen sea la creatividad exacta del post de Meta. La relación editorial final se cerrará después de comparar el asset con la publicación y sus métricas.

## Regla de integración

Un `Asset_Ref` proporcionado aquí no crea automáticamente un CNT. Después de recibir la lista, se comprobarán filename, Drive ID, Meta ID, fecha y evidencia visual. La ausencia del filename manual no bloquea el proceso: puede recuperarse desde la carpeta de julio si el Asset_Ref es único. Solo entonces se actualizarán `Content_Inventory.csv`, `Historical_Asset_Performance.csv` y `Historical_Performance_Individuals.csv`.

## Referencias

[1]: Operations/Research/Historical_Performance_Individuals.csv "Ledger de publicaciones históricas individuales"
[2]: Operations/Research/Historical_Asset_Performance.csv "Capa de rendimiento histórico por asset"
[3]: Operations/Research/2026-08-17_Reconciliacion_Historicos_Individuales.md "Reconciliación histórica previa y regla de cierre"
[4]: GrowthOS/Content_Inventory.csv "Inventario maestro del Growth OS"
