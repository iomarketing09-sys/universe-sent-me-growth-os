---
title: "Revisión del Excel de assets de junio con IDs de Facebook"
purpose: "Registrar la cobertura y las discrepancias del archivo aportado por el usuario para acelerar la reconciliación de los assets publicados en junio."
status: "Review"
created: 2026-08-17
updated: 2026-08-17
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv"
  - "Operations/Research/2026-08-17_Indice_Visual_Assets_y_Reporte_Incremental.md"
  - "GrowthOS/Content_Inventory.csv"
  - "Operations/Research/Historical_Asset_Performance.csv"
organization: "Operations/Research"
---

# Revisión del Excel de assets de junio con IDs de Facebook

## Resultado de la inspección

El archivo recibido se llama `Julio2026-UniverseSentMe.xlsx`, pero su hoja se titula `Assets Junio` y contiene 189 registros de publicaciones del lote de junio. Por contenido, debe tratarse como una fuente de junio; el nombre del archivo no debe usarse para clasificar el periodo.

| Campo | Resultado |
|---|---:|
| Filas de publicaciones | 189 |
| Facebook IDs únicos | 189 |
| Registros con nombre o referencia de asset | 172 |
| Registros sin Asset_Ref utilizable | 17 |
| Asset_Ref que ya tienen CNT en el inventario | 6 |
| Coincidencias directas con la cola por Meta post ID | 0 |

## Hallazgo crítico sobre los identificadores

Los IDs de la columna `FB ID` no coinciden directamente con los Meta post IDs del ledger. Por ejemplo, el registro del asset `260724` usa el photo ID `122127939279072582`, mientras que el ledger histórico usa el post ID `1036844829507460_122127939543072582`.

Esto indica que la hoja probablemente contiene **IDs de foto/objeto multimedia**, no necesariamente el ID de la historia o publicación devuelto por `/Page/feed`. Por tanto, estos valores son evidencia útil para localizar el asset publicado, pero no deben sustituir automáticamente al `meta_publication_id` del ledger.

> Regla operativa: conservar el valor de la hoja como `facebook_photo_id` y mantener separado el `meta_publication_id` cuando Meta devuelva ambos objetos.

## Seis relaciones ya reconocidas

| Asset_Ref | CNT | Facebook photo ID del Excel | Meta post ID del ledger |
|---:|---|---|---|
| `260724` | `CNT-068` | `122127939279072582` | `1036844829507460_122127939543072582` |
| `260733` | `CNT-071` | `122128723263072582` | `1036844829507460_122128723341072582` |
| `260735` | `CNT-073` | `122129013543072582` | `1036844829507460_122129013585072582` |
| `2607792` | `CNT-069` | `122132599749072582` | `1036844829507460_122132599809072582` |
| `2607794` | `CNT-070` | `122132690097072582` | `1036844829507460_122132690157072582` |
| `2607825` | `CNT-072` | `122134136643072582` | `1036844829507460_122134136793072582` |

La diferencia sistemática entre el photo ID y el post ID refuerza que el Excel es una fuente de relación multimedia, no un reemplazo del ledger editorial.

## Registros sin Asset_Ref utilizable

Los 17 registros requieren una segunda fuente antes de crear CNT o marcar una relación confirmada:

| Facebook photo ID | Valor recibido |
|---:|---|
| `122125520649072582` | Vacío |
| `122125547073072582` | `humor3.8` |
| `122125569027072582` | `humor3.9` |
| `122125883445072582` | `humor3.15` |
| `122125894719072582` | `humor4.06` |
| `122125906773072582` | `humor4.19` |
| `122125918479072582` | `humor4.18.1` |
| `122126265039072582` | `humor3.20` |
| `122126283357072582` | `humor3.14` |
| `122126305431072582` | `humor4.08` |
| `122126653725072582` | `humor4.04` |
| `122126663925072582` | `humor3.10` |
| `122127191517072582` | `humor3.14` |
| `122127201195072582` | `humor3.11` |
| `122127216255072582` | `humor4.07` |
| `122127951507072582` | `719173071_1566453291668355_8292492705944895244_n` |
| `122133971079072582` | `N/A` |

Los valores `humor3.8`, `humor3.9`, etc. parecen nombres internos o referencias de clasificación, no Asset_Ref canónicos. No se convierten a CNT sin una relación adicional con filename, Drive ID o asset visual.

## Resultado de la localización automática

Meta permitió consultar los 172 objetos multimedia con los campos `id`, `created_time`, `link`, `name`, `album` y `from`. La consulta confirmó 172 objetos válidos: 168 fueron creados en junio y 4 en julio, aunque los cuatro últimos pertenecen al archivo aportado dentro del lote de junio y deben conservarse para revisión de periodo.

La comparación visual entre las imágenes de los photo objects y `full_picture` de las 230 publicaciones de la cola produjo 160 coincidencias visuales de alta confianza, 11 coincidencias cercanas que requieren revisión y 1 caso sin coincidencia concluyente. No hubo duplicación del mejor Meta post ID entre los 172 registros.

| Estado del mapeo | Registros | Acción |
|---|---:|---|
| `Visual_Confirmed` | 160 | Listos para reconciliación editorial; conservar photo ID y Meta post ID por separado |
| `Visual_Review` | 11 | Revisar manualmente antes de crear o actualizar CNT |
| `Manual_Review_Required` | 1 | No asignar relación todavía: `Universe sent me - 015` |

El mapeo completo quedó en `2026-08-17_Mapeo_Photo_ID_Post_Junio.csv`. El campo `visual_hamming_distance` registra la distancia visual usada para clasificar cada coincidencia. Los seis CNT ya existentes no se duplican.

## Próximo procedimiento

El Excel permite acelerar la reconciliación de junio porque ofrece una relación directa entre 172 assets y sus objetos multimedia de Facebook. El siguiente proceso debe conservar ambos identificadores: `facebook_photo_id` para el objeto multimedia y `meta_publication_id` para la publicación editorial. Los seis casos ya reconciliados se mantendrán sin duplicar CNT.

La cola histórica debe actualizarse después de revisar los 11 casos cercanos y el outlier, no antes. Cualquier registro sin Asset_Ref seguirá como pendiente de identificación editorial.

## Referencias

[1]: `Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv` "Cola de reconciliación histórica de junio"
[2]: `GrowthOS/Content_Inventory.csv` "Inventario maestro"
[3]: `Operations/Research/Historical_Asset_Performance.csv` "Capa de rendimiento histórico"
[4]: `Operations/Research/2026-08-17_Indice_Visual_Assets_y_Reporte_Incremental.md` "Índice visual de assets de junio"
