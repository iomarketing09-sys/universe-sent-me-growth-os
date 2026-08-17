---
title: "Cruce automático de assets de junio con Meta y análisis de Top"
purpose: "Determinar qué evidencia de fecha y publicación puede confirmarse para los assets de 06 Junio y comparar la subcarpeta Top con los posts históricos ya integrados."
status: "Review"
created: 2026-08-17
updated: 2026-08-17
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-17_Auditoria_Revision_Junio.md"
  - "Operations/Research/Historical_Performance_Individuals.csv"
  - "Operations/Research/2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv"
  - "Operations/Research/2026-08-17_Cruce_Assets_Junio_Meta_Top.json"
  - "GrowthOS/Content_Inventory.csv"
organization: "Operations/Research"
---

# Cruce automático de assets de junio con Meta y análisis de Top

## Resultado ejecutivo

La carpeta Drive `06 Junio` contiene **196 archivos de imagen** y una subcarpeta `Top`. La subcarpeta `Top` no contiene una colección de assets: contiene **una sola captura de pantalla**.

El cruce automático completo contra Graph API quedó limitado por permisos actuales: la consulta directa de publicaciones históricas devolvió el error Meta `(#10) pages_read_engagement/Page Public Content Access`. Por ello, no se afirma que los 196 assets tengan fecha confirmada mediante Graph. Se utilizó el dataset histórico ya versionado como fuente secundaria y se separaron las coincidencias fuertes de las que todavía necesitan evidencia de imagen o permiso API.

## Subcarpeta Top

La captura muestra una publicación de Universe Sent Me titulada `Polvo de estrellas`, visible con fecha **7 de junio**, caption `✨✨✨`, y contadores aproximados de 4.4 mil reacciones, 143 comentarios y 1.4 mil shares. La imagen contiene la frase `“No conoces a nadie por accidente” / El Universo: / A ver cojan`.

El dataset histórico contiene una coincidencia fuerte para el caption `✨✨✨`:

| Campo | Evidencia disponible |
|---|---|
| Page Post ID | `1036844829507460_122127939543072582` |
| Fecha local | 2026-06-07 18:43:18, America/Matamoros |
| Métricas históricas | 25 reacciones, 1 comentario, 6 shares, 32 interacciones |
| Captura Top | Aproximadamente 4.4k reacciones, 143 comentarios y 1.4k shares |
| Filename/Drive ID | No visible en la captura |
| CNT existente | No encontrado entre los cinco top posts ya integrados |

La coincidencia caption + fecha + pieza visual es fuerte para identificar el post, pero los contadores no son intercambiables: representan snapshots de distinta fecha o fuente. La captura tampoco permite conocer el filename ni el Drive ID, por lo que todavía no se debe crear CNT para esta pieza.

## Comparación con posts ya integrados

Los cinco posts de junio ya integrados son `El gato: 😧`, `a ver... a ver... 🤨`, `yo Aura Fuerte 😏`, `Me da miedo ser el malo de la historia...` y `🤡`. La pieza de Top `✨✨✨` **no duplica ninguno de esos cinco**; debe tratarse como un sexto candidato histórico separado, con Meta ID y fecha probable confirmados por el dataset, pero con asset pendiente.

## Clasificación operativa

| Resultado | Cantidad | Interpretación |
|---|---:|---|
| Assets en 06 Junio | 196 | Disponibles en Drive; sin fecha individual automática todavía. |
| Elementos en Top | 1 captura | Evidencia visual, no asset original. |
| Coincidencia fuerte Top→Meta/dataset | 1 | `✨✨✨`, 7 de junio, Meta ID localizado en dataset. |
| Nuevos CNT creados | 0 | No se modifica el inventario. |
| Fechas confirmadas para los 196 por Graph live | 0 | Bloqueado por permiso Meta. |

## Conclusión CGO

La subcarpeta Top confirma un post histórico adicional que no estaba en los cinco registros individuales integrados. Sin embargo, la fuente Top es una captura, no el archivo original, y la consulta Graph live no está autorizada por los permisos actuales. El siguiente paso correcto no es crear CNT, sino localizar el asset visual exacto de `✨✨✨` dentro de los 196 archivos de junio mediante comparación de imagen o aportar una exportación de Meta con attachments. Después se podrá enlazar la fecha, Meta ID, Drive ID y asset en una sola fila verificable.

No se movieron ni copiaron archivos de Drive, no se modificaron `Content_Inventory.csv`, `Publication_Log.csv` ni `ExperimentLog.csv`, y no se hicieron más llamadas a Meta después del bloqueo de permisos.
