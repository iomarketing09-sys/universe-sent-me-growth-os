---
title: "Propuesta de cadencia 23–30 de agosto — MEME-CAD"
purpose: "Auditar el calendario activo del 23 al 30 de agosto y registrar la incorporación parcial de cinco memes producidos, distinguiendo tres reemplazos ejecutados de dos slots adicionales aún pendientes de autorización."
status: Review
created: 2026-08-22
updated: 2026-08-22
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "2026-08-16_Calendario_Operativo_17_30_Agosto.md"
  - "2026-08-16_Calendario_Operativo_17_30_Agosto.csv"
  - "2026-08-18_Cola_Reuse_Junio_Aprobada.csv"
  - "2026-08-22_Drive_Memes_Seed_Inventory.csv"
  - "../Production/2026-08-22_Briefs_Cadence_Memes_Seed_Adaptations.md"
  - "../../GrowthOS/01_04_Production_Queue.md"
  - "../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
organization: "Operations/Research"
---

# Propuesta de cadencia 23–30 de agosto

## Veredicto ejecutivo

El lote completo de cinco memes **sí puede alimentar la siguiente ola del playbook**, pero no debe entrar automáticamente al calendario como si ya estuviera aprobado para publicación. El calendario activo del 23 al 30 contenía 42 filas, equivalentes a 5.25 slots diarios. Por lo tanto, no requería una expansión masiva; solo presentaba dos días por debajo de la banda objetivo: el 28 y el 29 tenían cuatro slots cada uno.

La propuesta de revisión humana utilizó los cinco assets producidos una sola vez: tres reemplazos de reuse y dos slots adicionales en los días de cuatro piezas. Fernando aprobó los cinco assets y confirmó únicamente los tres reemplazos. Los tres reemplazos ya fueron ejecutados y verificados en Facebook; los dos slots adicionales permanecen sin programar. El tramo ejecutado conserva 42 slots y mantiene Facebook como única plataforma.

La mezcla no alcanza todavía el objetivo futuro de 65–70% de piezas nuevas: al incorporar los cinco assets al tramo de 44 filas, la proporción estimada sería 24 nuevas y 20 reuse, aproximadamente 54.5% nuevas. Para alcanzar 65% en este mismo bloque harían falta más assets nuevos; no se deben fabricar slots conceptuales ni contar Reels como imágenes.

## Auditoría del calendario activo

La extracción reproducible del CSV activo encontró 42 filas entre el 23 y el 30 de agosto: 19 `Nueva`, 20 `Reuse_Top` y 3 `Reuse_Reserve`. Todas aparecen como `Programado`, salvo las tres filas comparables con `Programado_Meta_Verificado`. El calendario permanece vigente y no fue modificado.

| Fecha | Día calendario calculado | Slots actuales | Nuevas | Reuse | Recomendación de volumen |
|---|---|---:|---:|---:|---|
| 23 ago | Domingo | 5 | 2 | 3 | Mantener |
| 24 ago | Lunes | 6 | 3 | 3 | Mantener; candidato para reemplazo |
| 25 ago | Martes | 6 | 3 | 3 | Mantener |
| 26 ago | Miércoles | 6 | 3 | 3 | Mantener; candidato para reemplazo |
| 27 ago | Jueves | 6 | 3 | 3 | Mantener; candidato para reemplazo |
| 28 ago | Viernes | 4 | 1 | 3 | Añadir un slot para llegar a 5 |
| 29 ago | Sábado | 4 | 2 | 2 | Añadir un slot para llegar a 5 |
| 30 ago | Domingo | 5 | 2 | 3 | Mantener |

### Inconsistencias de día de semana

La columna `Día` del calendario activo contiene varias etiquetas que no coinciden con la fecha: por ejemplo, `2026-08-25` aparece como viernes, aunque corresponde a martes, y `2026-08-29` aparece como lunes, aunque corresponde a sábado. Este documento usa el día de semana calculado a partir de la fecha y no altera el CSV activo. Antes de aplicar cualquier cambio se debe decidir si se corrige esa columna en una revisión administrativa separada.

## Propuesta de incorporación de los cinco assets

El CSV asociado, [`2026-08-23_Propuesta_Cadencia_23_30_MEME-CAD_Review.csv`](2026-08-23_Propuesta_Cadencia_23_30_MEME-CAD_Review.csv), contiene las cinco filas propuestas con `Human_Approval=PENDING`.

| Fecha y hora | Operación propuesta | Asset | Motivo |
|---|---|---|---|
| 24 ago, 16:00 | Reemplazar reuse | `MEME-CAD-004` Wilfred con tablero | El tablero y el caption conversacional encajan en una franja de tarde; conserva el personaje central del bloque sin añadir otro slot. |
| 26 ago, 17:00 | Reemplazar reuse | `MEME-CAD-002` Fantasma actuando normal | Introduce una pieza nueva de humor ácido en una franja vespertina; la captura fuente no se publica. |
| 27 ago, 17:00 | Reemplazar reuse | `MEME-CAD-003` Silvio arrojando piedra-kármica | Es una pieza de remate ácido; la piedra se entiende como amenaza cómica, sin violencia gráfica. |
| 28 ago, 16:00 | Añadir slot | `MEME-CAD-001` Universe con envidia | El viernes tiene cuatro slots; el quinto lo coloca dentro de la banda mínima sin desplazar un contenido ya programado. |
| 29 ago, 16:00 | Añadir slot | `MEME-CAD-005` Evan y la misma indirecta | El sábado tiene cuatro slots; la pieza social funciona como aprendizaje adicional sin mezclar Reels ni afiliación. |

Estas son **sugerencias de ubicación**, no órdenes de cancelación, reemplazo ni programación. En los tres reemplazos primero se debe confirmar el asset, caption y estado de la fila saliente; después se necesita autorización explícita para cancelar/reprogramar. En los dos slots adicionales se necesita autorización explícita para ampliar la programación.

## Reuse verificado disponible como alternativa

La cola `2026-08-18_Cola_Reuse_Junio_Aprobada.csv` contiene seis candidatos con IDs de Drive y publicación Meta; la consulta de Drive confirmó nombres exactos y archivos no enviados a la papelera:

| CNT | Filename confirmado en Drive | Resultado operativo |
|---|---|---|
| CNT-080 | `Universe - Existencial 2607823.jpeg` | Candidato de prioridad alta; copy y plataforma aún requieren confirmación. |
| CNT-081 | `Universe - Existencial 2607787.png` | Candidato de prioridad alta; preservar dúo Universe+Fantasma y revisar caption. |
| CNT-082 | `Universe - Existencial 2607816.jpeg` | Candidato de prioridad media; revisar legibilidad y slot. |
| CNT-083 | `Universe - Existencial 2607828.png` | Candidato de prioridad media; conservar atribución a Ganso. |
| CNT-084 | `Universe - Existencial 260740.png` | Candidato de prioridad media; revisar copy por referencias a salud mental. |
| CNT-085 | `Universe - Existencial 2607837.png` | Reserva; revisar frecuencia de sexualización y plataforma. |

Estos reuse no se insertan automáticamente en esta propuesta porque el calendario activo ya tiene reuse asignado y la prioridad inmediata es ubicar los cinco assets nuevos sin sobrecargar la frecuencia. Pueden sustituir filas concretas solo mediante una revisión posterior con copy exacto y autorización por fila.

## Gates obligatorios

Antes de cualquier aplicación, cada fila debe pasar los siguientes gates:

| Gate | Estado actual |
|---|---|
| Asset v1/v3/v4 presente en Drive | Sí; verificado en el inventario y en la Production Queue |
| Filename y Drive ID | Sí para los cinco assets nuevos; sí para CNT-080–085 |
| Copy exacto y tratamiento de caption | Propuesto; pendiente de revisión humana |
| Fecha, hora y zona `America/Matamoros` | Propuestas; pendientes de aprobación |
| Facebook | Única plataforma propuesta |
| Instagram | Separado; no incluido |
| Reels | Separados; no incluidos |
| Afiliados | No incluidos |
| CNT | No creado |
| Cancelación o programación Meta | 3 reemplazos ejecutados y verificados; 2 slots adicionales sin ejecutar |
| Aprobación humana por fila | 3 filas `APPROVED_REPLACEMENT`; 2 filas `PENDING_ADDITIONAL_SLOT` |

## Registro de ejecución

El 22 de agosto de 2026 Fernando aprobó los cinco assets MEME-CAD y confirmó el reemplazo de las tres filas `MEME-CAD-PLAN-001` a `MEME-CAD-PLAN-003`. Se cancelaron los posts salientes `1036844829507460_122151376941072582`, `1036844829507460_122151378063072582` y `1036844829507460_122151378573072582`; una consulta posterior confirmó que los tres quedaron ausentes de `scheduled_posts`. En sus mismos horarios se programaron y verificaron los nuevos posts, todos con `is_published=false`:

| Fecha/hora local | Asset | Nuevo Meta Post ID | Meta Photo ID | Estado |
|---|---|---|---|---|
| 24 ago, 16:00 | `MEME-CAD-004_Wilfred_Tablero_v3.png` | `1036844829507460_122154732441072582` | `122154732411072582` | `Scheduled_Meta_Verified` |
| 26 ago, 17:00 | `MEME-CAD-002_Fantasma_Sobrio_v1.png` | `1036844829507460_122154732501072582` | `122154732477072582` | `Scheduled_Meta_Verified` |
| 27 ago, 17:00 | `MEME-CAD-003_Silvio_Karma_v3.png` | `1036844829507460_122154732567072582` | `122154732543072582` | `Scheduled_Meta_Verified` |

Los slots adicionales propuestos para el 28 (`MEME-CAD-001`) y el 29 (`MEME-CAD-005`) no fueron aprobados para ejecución y permanecen como `PENDING_ADDITIONAL_SLOT`. No se modificaron esos días, no se movieron originales en Drive, no se creó CNT, no se ejecutó Instagram, Reels ni afiliación.

## Decisión pendiente

La única decisión que permanece abierta en esta propuesta es si se desea añadir posteriormente `MEME-CAD-001` el 28 de agosto y `MEME-CAD-005` el 29 de agosto. Mientras no exista esa autorización específica, esas fechas conservan sus cuatro piezas actuales y no se rellenarán con capturas fuente ni reuse improvisado.

## Referencias

[1]: 2026-08-16_Calendario_Operativo_17_30_Agosto.md "Calendario operativo activo 17–30"
[2]: 2026-08-16_Calendario_Operativo_17_30_Agosto.csv "CSV maestro del calendario activo"
[3]: 2026-08-18_Cola_Reuse_Junio_Aprobada.csv "Cola de reuse aprobada"
[4]: 2026-08-22_Drive_Memes_Seed_Inventory.csv "Inventario de semillas Drive/Memes"
[5]: ../Production/2026-08-22_Briefs_Cadence_Memes_Seed_Adaptations.md "Briefs de producción de los cinco memes"
[6]: ../../GrowthOS/01_04_Production_Queue.md "Cola de producción"
[7]: ../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md "Fuente maestra y ledgers"
