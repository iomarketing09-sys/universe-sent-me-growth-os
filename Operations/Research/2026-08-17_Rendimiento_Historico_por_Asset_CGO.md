---
title: "Rendimiento histórico por asset para la biblia"
purpose: "Definir y comenzar una capa de evidencia que conecte assets de Universe Sent Me con publicaciones de Facebook, rendimiento y observaciones lifetime para alimentar la biblia."
status: "Review"
created: 2026-08-17
updated: 2026-08-17
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/Historical_Asset_Performance.csv"
  - "Operations/Research/June_Visual_Asset_Index.csv"
  - "Operations/Research/2026-08-17_Cruce_Assets_Junio_Meta_Top.md"
  - "Operations/Research/2026-08-17_Indice_Visual_Junio_Cierre.md"
  - "Operations/Research/2026-08-08_Reporte_Mensual_Junio_Julio_2026.md"
  - "GrowthOS/Content_Inventory.csv"
organization: "Operations/Research"
---

# Rendimiento histórico por asset para la biblia

## Dictamen CGO

La biblia necesita una capa que no existía cuando se creó: el rendimiento real de los personajes, imágenes, conceptos y estilos que nacieron en Facebook. El índice visual de junio resuelve la localización del archivo, pero no responde todavía qué publicación funcionó, cuándo se publicó ni qué escala alcanzó.

La solución correcta es construir una tabla de rendimiento histórico por asset, con una fila por combinación `asset + publicación + ventana métrica`. No se debe sobrescribir una extracción histórica con una captura lifetime posterior. Ambas son evidencia útil, pero responden preguntas diferentes.

## Primera capa construida

Se creó `Historical_Asset_Performance.csv`. Actualmente contiene siete observaciones de junio: seis publicaciones identificadas en la extracción histórica y una observación adicional de la captura Top para `260724`.

| Evidencia | Cobertura | Uso para la biblia |
|---|---:|---|
| Extracción histórica comparable | 6 posts de junio | Comparar interacciones dentro de la misma extracción. |
| Asset visual + CNT confirmado | 1 de esos posts: `260724` | Conectar rendimiento con el archivo y el inventario. |
| Snapshot lifetime observado en captura | 1 post: `260724` | Registrar la escala alcanzada posteriormente; no usarlo como 24/72h. |

Los cinco posts restantes tienen Meta ID, fecha y métricas, pero todavía no tienen `asset_ref` confirmado en la capa histórica. Por tanto, no deben atribuirse a personajes o assets concretos dentro de la biblia hasta completar el cruce visual.

## Caso `260724 — Polvo de estrellas`

El post `✨✨✨` es el primer caso completo. El asset `Universe - Existencial 260724.png` está en Drive, se enlazó con `CNT-068` y corresponde visualmente a la captura Top. La extracción histórica registra 25 reacciones, 1 comentario y 6 shares, para 32 interacciones en su corte. La captura posterior muestra aproximadamente 4.4 mil reacciones, 143 comentarios y 1.4 mil shares, cerca de 5,943 interacciones visibles.

La captura es información valiosa para la biblia porque demuestra que la pieza alcanzó una escala mucho mayor con el tiempo. Sin embargo, la fecha exacta del contador no está documentada como snapshot API; se trata de un corte lifetime observado en una captura guardada en Drive. Debe conservarse con `evidence_tier=C`, no mezclarse con la extracción histórica y no convertirse en métrica 24/72h.

## Modelo de evidencia

| Tier | Significado | Ejemplo |
|---|---|---|
| A | Asset, Drive ID, Meta ID, fecha y relación CNT confirmados. | `260724` / `CNT-068`. |
| B | Meta ID, fecha y métricas verificables, pero asset todavía no enlazado. | Cinco top posts restantes de junio. |
| C | Snapshot visual/lifetime posterior con fecha de captura o contexto, pero sin ventana API exacta. | Captura Top de `✨✨✨`. |
| D | Candidato basado solo en caption, similitud o filename; requiere validación. | Asset indexado sin Meta match. |

## Qué procede ahora

El siguiente trabajo debe ser la **reconciliación visual de los cinco top posts restantes de junio** contra `June_Visual_Asset_Index.csv`. Cuando cada uno tenga filename, Drive ID y Meta ID confirmados, se actualizará `Historical_Asset_Performance.csv` y se enlazará el CNT existente o se propondrá uno nuevo sin inventar relaciones.

Después se procesarán los demás posts de junio por prioridad: primero publicaciones con shares altos, luego publicaciones con interacciones altas y finalmente el resto del mes. El resultado para la biblia no será solo una tabla de números; incluirá patrones por personaje, formato, tono, copy, fecha, hora, reacciones, comentarios, shares, interacción total y evidencia de escala posterior.

El reporte operativo recomendado es incremental. No conviene generar un reporte diario completo: debe actualizarse cada 48 horas o bajo demanda, procesando solo assets nuevos, publicaciones nuevas y matches pendientes. La cadencia puede alinearse con la revisión P0 sin mezclar sus métricas estrictas.

No se modificó el canon de Claude. No se sustituyeron métricas 24/72h, no se publicaron contenidos, no se movieron archivos de Drive y no se alteraron los ledgers operativos de producción.
