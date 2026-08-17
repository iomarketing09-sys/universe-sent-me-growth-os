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

El cruce automático completo contra Graph API quedó limitado por permisos actuales: la consulta directa de publicaciones históricas devolvió el error Meta `(#10) pages_read_engagement/Page Public Content Access`. Por ello, no se afirma que los 196 assets tengan fecha confirmada mediante Graph. Se utilizó el dataset histórico ya versionado como fuente secundaria y se separaron las coincidencias fuertes de las que todavía necesitan evidencia de imagen o permiso API. La búsqueda visual local sí permitió resolver un asset individual: `Universe - Existencial 260724.png`.

## Subcarpeta Top

La captura muestra una publicación de Universe Sent Me titulada `Polvo de estrellas`, visible con fecha **7 de junio**, caption `✨✨✨`, y contadores aproximados de 4.4 mil reacciones, 143 comentarios y 1.4 mil shares. La imagen contiene la frase `“No conoces a nadie por accidente” / El Universo: / A ver cojan`.

El dataset histórico contiene una coincidencia fuerte para el caption `✨✨✨`:

| Campo | Evidencia disponible |
|---|---|
| Page Post ID | `1036844829507460_122127939543072582` |
| Fecha local | 2026-06-07 18:43:18, America/Matamoros |
| Métricas históricas | 25 reacciones, 1 comentario, 6 shares, 32 interacciones |
| Captura Top | Aproximadamente 4.4k reacciones, 143 comentarios y 1.4k shares |
| Filename/Drive ID | `Universe - Existencial 260724.png` / `1smMni1etHda5lhATT0XGtjE1EcAvIFYw` |
| CNT existente | **Creado en este lote: `CNT-068`** |

La coincidencia caption + fecha + pieza visual es fuerte para identificar el post, pero los contadores no son intercambiables: representan snapshots de distinta fecha o fuente. La captura por sí sola no mostraba el filename ni el Drive ID; la comparación visual contra los 196 assets resolvió ambos campos y permitió crear `CNT-068` con confianza alta.

## Comparación con posts ya integrados

Los cinco posts de junio ya integrados son `El gato: 😧`, `a ver... a ver... 🤨`, `yo Aura Fuerte 😏`, `Me da miedo ser el malo de la historia...` y `🤡`. La pieza de Top `✨✨✨` **no duplica ninguno de esos cinco**; ahora queda como un sexto post histórico confirmado, enlazado a `260724` y `CNT-068`.

## Clasificación operativa

| Resultado | Cantidad | Interpretación |
|---|---:|---|
| Assets en 06 Junio | 196 | Disponibles en Drive; sin fecha individual automática general. |
| Elementos en Top | 1 captura | Evidencia visual de un post. |
| Coincidencia fuerte Top→Meta/dataset | 1 | `✨✨✨`, 7 de junio, Meta ID y asset visual resueltos. |
| Nuevos CNT creados | 1 | `CNT-068` para `260724`. |
| Fechas confirmadas para los 196 por Graph live | 0 | Bloqueado por permiso Meta. |

## Conclusión CGO

La subcarpeta Top confirma un post histórico adicional que no estaba en los cinco registros individuales integrados. La búsqueda visual local resolvió el asset exacto: `Universe - Existencial 260724.png`, Drive ID `1smMni1etHda5lhATT0XGtjE1EcAvIFYw`. Se creó `CNT-068`, se vinculó el Meta ID `1036844829507460_122127939543072582` y se añadió el post a `Historical_Performance_Individuals.csv`. La limitación Graph sigue aplicando al resto de los 196 assets.

No se movieron ni copiaron archivos de Drive, no se modificaron `Publication_Log.csv` ni `ExperimentLog.csv`, y no se hicieron más llamadas a Meta después del bloqueo de permisos. `Content_Inventory.csv` sí recibió únicamente la nueva fila histórica `CNT-068`, sustentada por la coincidencia visual exacta y la evidencia del dataset.
