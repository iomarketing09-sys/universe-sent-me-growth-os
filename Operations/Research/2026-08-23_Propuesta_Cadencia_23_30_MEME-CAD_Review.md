---
title: "Propuesta de cadencia 23–30 de agosto — MEME-CAD"
purpose: "Auditar y registrar la incorporación operativa de los cinco memes MEME-CAD y cuatro slots adicionales de cadencia dentro del bloque 22–30 de agosto, distinguiendo reemplazos, adiciones y estados de publicación futura."
status: Review
created: 2026-08-22
updated: 2026-08-22
version: "1.2"
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

# Propuesta y ejecución de cadencia 22–30 de agosto

## Veredicto ejecutivo

El lote completo de cinco memes **fue aprobado para alimentar la ola activa del playbook**. La decisión operativa de Fernando fue aumentar la cadencia sin esperar al cierre mensual. El tramo 22–30 tenía 46 filas; los días 22, 28 y 29 tenían cuatro slots y el domingo 23 tenía cinco. Se añadieron cuatro slots para llevar todo el tramo a la banda de 5–6 publicaciones.

La ejecución utilizó los cinco assets producidos una sola vez: tres reemplazos de reuse y dos slots nuevos. Además, se añadieron dos reuse aprobados para completar la recuperación de cadencia del 22 y 23. Los cuatro slots adicionales fueron programados y verificados en Facebook, sin cancelar ninguna fila existente. El tramo 22–30 queda con 50 filas y una cadencia diaria de 5–6 publicaciones.

La mezcla resultante del tramo 22–30 es de 26 filas `Nueva`, 21 `Reuse_Top` y 3 `Reuse_Reserve`, para 50 publicaciones y aproximadamente 5.56 por día. La proporción de nuevas es 52%; se priorizó recuperar volumen con assets reales y trazables, no forzar el objetivo futuro de 65–70% ni contar Reels como imágenes.

## Auditoría del calendario activo

La extracción reproducible del CSV actualizado encontró 50 filas entre el 22 y el 30 de agosto: 26 `Nueva`, 21 `Reuse_Top` y 3 `Reuse_Reserve`. Los cuatro slots adicionales quedaron `Programado_Meta_Verificado`; los tres reemplazos anteriores también conservan ese estado. El calendario fue ampliado sin cancelar filas existentes durante esta operación.

| Fecha | Día calendario calculado | Slots actuales | Nuevas | Reuse | Recomendación de volumen |
|---|---|---:|---:|---:|---|
| 22 ago | Sábado | 5 | 2 | 3 | Slot adicional ejecutado |
| 23 ago | Domingo | 6 | 2 | 4 | Slot adicional ejecutado |
| 24 ago | Lunes | 6 | 4 | 2 | Reemplazo ejecutado |
| 25 ago | Martes | 6 | 3 | 3 | Mantener |
| 26 ago | Miércoles | 6 | 4 | 2 | Reemplazo ejecutado |
| 27 ago | Jueves | 6 | 4 | 1 + reserve | Reemplazo ejecutado |
| 28 ago | Viernes | 5 | 2 | 3 | Slot adicional ejecutado |
| 29 ago | Sábado | 5 | 3 | 2 | Slot adicional ejecutado |
| 30 ago | Domingo | 5 | 2 | 2 + reserve | Mantener |

### Inconsistencias de día de semana

La columna `Día` del calendario activo contiene varias etiquetas que no coinciden con la fecha: por ejemplo, `2026-08-25` aparece como viernes, aunque corresponde a martes, y `2026-08-29` aparece como lunes, aunque corresponde a sábado. Este documento usa el día de semana calculado a partir de la fecha y no altera el CSV activo. Antes de aplicar cualquier cambio se debe decidir si se corrige esa columna en una revisión administrativa separada.

## Propuesta de incorporación de los cinco assets

El CSV asociado, [`2026-08-23_Propuesta_Cadencia_23_30_MEME-CAD_Review.csv`](2026-08-23_Propuesta_Cadencia_23_30_MEME-CAD_Review.csv), contiene las cinco filas MEME-CAD y sus estados de ejecución; los cuatro slots adicionales se registran en `2026-08-22_Cadence_Expansion_22_30_Execution.json`.

| Fecha y hora | Operación propuesta | Asset | Motivo |
|---|---|---|---|
| 24 ago, 16:00 | Reemplazar reuse | `MEME-CAD-004` Wilfred con tablero | El tablero y el caption conversacional encajan en una franja de tarde; conserva el personaje central del bloque sin añadir otro slot. |
| 26 ago, 17:00 | Reemplazar reuse | `MEME-CAD-002` Fantasma actuando normal | Introduce una pieza nueva de humor ácido en una franja vespertina; la captura fuente no se publica. |
| 27 ago, 17:00 | Reemplazar reuse | `MEME-CAD-003` Silvio arrojando piedra-kármica | Es una pieza de remate ácido; la piedra se entiende como amenaza cómica, sin violencia gráfica. |
| 28 ago, 16:00 | Añadir slot | `MEME-CAD-001` Universe con envidia | El viernes tiene cuatro slots; el quinto lo coloca dentro de la banda mínima sin desplazar un contenido ya programado. |
| 29 ago, 16:00 | Añadir slot | `MEME-CAD-005` Evan y la misma indirecta | El sábado tiene cuatro slots; la pieza social funciona como aprendizaje adicional sin mezclar Reels ni afiliación. |

Estas filas dejaron de ser sugerencias: Fernando autorizó la ampliación y los cuatro slots quedaron programados y verificados. No se cancelaron filas en esta ampliación; los tres reemplazos habían sido autorizados y ejecutados en una operación previa. Cualquier slot adicional fuera de estas cuatro filas requiere una nueva autorización por fila.

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

CNT-081 y CNT-083 fueron seleccionados para los slots adicionales del 23 y 22, respectivamente, después de confirmar filename, Drive ID, copy histórico, distancia mínima de 30 días y ausencia de duplicado en el tramo. CNT-080, CNT-082, CNT-084 y CNT-085 permanecen como candidatos de reserva; no se programaron.

## Gates obligatorios

Antes de cualquier aplicación, cada fila debe pasar los siguientes gates:

| Gate | Estado actual |
|---|---|
| Asset v1/v3/v4 presente en Drive | Sí; verificado en el inventario y en la Production Queue |
| Filename y Drive ID | Sí para los cinco assets nuevos; sí para CNT-080–085 |
| Copy exacto y tratamiento de caption | Verificado y registrado para las cuatro adiciones |
| Fecha, hora y zona `America/Matamoros` | Verificadas en Meta para las cuatro adiciones |
| Facebook | Única plataforma ejecutada |
| Instagram | Separado; no incluido |
| Reels | Separados; no incluidos |
| Afiliados | No incluidos |
| CNT | No creado |
| Cancelación o programación Meta | 3 reemplazos y 4 slots adicionales ejecutados y verificados |
| Aprobación humana por fila | 3 filas `APPROVED_REPLACEMENT`; 4 filas `APPROVED_ADDITIONAL_SLOT` |

## Registro de ejecución

El 22 de agosto de 2026 Fernando aprobó los cinco assets MEME-CAD y confirmó el reemplazo de las tres filas `MEME-CAD-PLAN-001` a `MEME-CAD-PLAN-003`. Se cancelaron los posts salientes `1036844829507460_122151376941072582`, `1036844829507460_122151378063072582` y `1036844829507460_122151378573072582`; una consulta posterior confirmó que los tres quedaron ausentes de `scheduled_posts`. En sus mismos horarios se programaron y verificaron los nuevos posts, todos con `is_published=false`:

| Fecha/hora local | Asset | Nuevo Meta Post ID | Meta Photo ID | Estado |
|---|---|---|---|---|
| 24 ago, 16:00 | `MEME-CAD-004_Wilfred_Tablero_v3.png` | `1036844829507460_122154732441072582` | `122154732411072582` | `Scheduled_Meta_Verified` |
| 26 ago, 17:00 | `MEME-CAD-002_Fantasma_Sobrio_v1.png` | `1036844829507460_122154732501072582` | `122154732477072582` | `Scheduled_Meta_Verified` |
| 27 ago, 17:00 | `MEME-CAD-003_Silvio_Karma_v3.png` | `1036844829507460_122154732567072582` | `122154732543072582` | `Scheduled_Meta_Verified` |

Los cuatro slots adicionales fueron aprobados y ejecutados: `CNT-083` el 22 a las 22:00, `CNT-081` el 23 a las 17:00, `MEME-CAD-001` el 28 a las 16:00 y `MEME-CAD-005` el 29 a las 16:00. Meta verificó los cuatro con `is_published=false`. No se movieron originales en Drive, no se creó CNT, no se ejecutó Instagram, Reels ni afiliación.

## Estado posterior a la ejecución

No queda una decisión pendiente dentro de este bloque. Los cuatro slots adicionales fueron autorizados y verificados. El siguiente pendiente es operativo: comprobar las publicaciones reales en sus horarios y dejar que el reporte diario capture métricas sin estimar resultados antes de la publicación.

## Referencias

[1]: 2026-08-16_Calendario_Operativo_17_30_Agosto.md "Calendario operativo activo 17–30"
[2]: 2026-08-16_Calendario_Operativo_17_30_Agosto.csv "CSV maestro del calendario activo"
[3]: 2026-08-18_Cola_Reuse_Junio_Aprobada.csv "Cola de reuse aprobada"
[4]: 2026-08-22_Drive_Memes_Seed_Inventory.csv "Inventario de semillas Drive/Memes"
[5]: ../Production/2026-08-22_Briefs_Cadence_Memes_Seed_Adaptations.md "Briefs de producción de los cinco memes"
[6]: ../../GrowthOS/01_04_Production_Queue.md "Cola de producción"
[7]: ../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md "Fuente maestra y ledgers"
