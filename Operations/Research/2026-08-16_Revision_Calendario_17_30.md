---
title: "Revisión del calendario experimental 17–30 de agosto"
purpose: "Auditar la propuesta de 74 slots contra el inventario de Drive y los ledgers de publicación antes de generar, aprobar o programar assets."
status: Review
created: 2026-08-16
updated: 2026-08-16
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-14_Propuesta_Calendario_17_30_Agosto.csv"
  - "Operations/Research/2026-08-14_Propuesta_Calendario_17_30_Agosto_con_Copys.csv"
  - "Operations/Research/2026-08-14_Propuesta_Calendario_17_30_Agosto_con_Copys.md"
  - "Operations/Research/2026-08-15_Inventario_Memes_Nuevos_Drive.csv"
  - "Operations/Research/2026-08-14_Reuse_Mayo_Ranking.csv"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "GrowthOS/Content_Inventory.csv"
  - "Operations/Research/2026-08-14_Revision_Reuse_Mayo_Junio.md"
organization: "Operations/Research"
---

# Revisión del calendario experimental 17–30 de agosto

## 1. Resultado ejecutivo

La propuesta contiene **74 slots en 14 días**: 46 espacios de contenido nuevo y 28 reuse. La estructura de frecuencia está completa y conserva la distribución horaria aprobada: seis publicaciones de lunes a jueves, cuatro el viernes y sábado, y cinco el domingo con slots nocturnos de 22:00.

La propuesta todavía no está lista para convertirse en calendario operativo porque requiere tres controles: excluir de la cola de generación los cinco assets nuevos ya publicados el 15–16, confirmar la representación de variantes con el mismo número de referencia y revisar los pares de reuse consecutivos antes de la aprobación final. No se modificó la propuesta vigente durante esta revisión.

## 2. Conciliación de fuentes

| Fuente | Resultado | Interpretación operativa |
|---|---:|---|
| Slots de la propuesta con copys | 74 | Estructura completa para 17–30 de agosto. |
| Slots `Nueva` | 46 | Permanecen como `PENDIENTE_GENERAR`; no se inventaron assets ni captions definitivos. |
| Slots `Reuse_Top` | 28 | Todos tienen filename y caption propuesto. |
| Inventario nuevo de Drive | 38 | Snapshot del 15 de agosto, todos con estado `Nuevo_Pendiente_Revision`. |
| Assets nuevos ya publicados en 15–16 | 5 | 2608030, 2608033, 2608036, 2608037 y 2608060; no deben volver a tratarse como disponibles para generación o reuse inmediato. |
| Assets nuevos aún no registrados como publicados | 33 | Cola real disponible según la conciliación contra `Publication_Log.csv`; requiere revisión visual/editorial antes de asignar slots. |
| Reuse por filename | 28 únicos | No hay filenames repetidos en la propuesta. |
| Reuse por número de referencia | 27 referencias únicas | El número 260508 aparece en dos archivos distintos; Drive confirmó checksums y contenidos visuales diferentes. |

La conciliación se hizo contra los Meta IDs y referencias reales del `Publication_Log.csv`. Los cinco assets consumidos no se asignaron a ningún slot futuro; la lista de 33 disponibles no equivale todavía a una lista aprobada para publicación.

## 3. Hallazgo sobre 260508

Drive contiene dos archivos distintos con el mismo número de referencia:

| Archivo | Drive ID | Evidencia |
|---|---|---|
| `260508 - Universe.jpg` | `1c_AQFPbigiR39cH7f39h2MzCFvQL799b` | JPG 1122×1402; Universe con el texto “Karen, tú eres cine, nunca lo dudes. Del dramático, pero cine al fin.” |
| `Universe - Existencial 260508.png` | `1eVre3AC1EjmEUPHKMjVRbQ3efXtYyh-8` | PNG 1194×1317; imagen de cerebro/corazón con el texto “El momento increíble cuando estos dos finalmente deciden sincronizarse”. |

No se deben fusionar ni eliminar. Para evitar ambigüedad, el calendario debe conservar el filename completo y, si se convierte en ledger operativo, registrar también el Drive ID.

## 4. Secuencia de reuse

La propuesta conserva 28 reuse sin repetir filenames. Sin embargo, la revisión cronológica detectó cinco pares de reuse consecutivos que conviene revisar para evitar fatiga inmediata:

| Slot anterior | Slot siguiente |
|---|---|
| 20 agosto 13:30 — `260659 - Universe.png` | 20 agosto 16:00 — `260508 - Universe.jpg` |
| 21 agosto 19:00 — `260614 - Universe.png` | 22 agosto 10:00 — `260589.png` |
| 23 agosto 22:00 — `260625.png` | 24 agosto 10:00 — `260518 - Kael.png` |
| 28 agosto 13:30 — `260590 - Maeve.png` | 28 agosto 19:00 — `260543 - Evan.png` |
| 28 agosto 19:00 — `260543 - Evan.png` | 29 agosto 10:00 — `741 - Elara+Maeve.png` |

El requisito histórico específico sobre `260528` sí está respetado: permanece en domingo 30 de agosto a las 22:00. El par entre los días 27 y 28 tampoco queda consecutivo porque el 27 termina con una pieza nueva a las 19:00.

## 5. Proporción y frecuencia

La propuesta usa 46 nuevas y 28 reuse, equivalente a **62.2% nuevo y 37.8% reuse**. Esto es ligeramente más contenido en reuse que una proporción estricta de 3 nuevas por cada 2 reuse, que con 28 reuse produciría 42 nuevas. Se conserva la propuesta de 74 slots porque la frecuencia fue aprobada como parte de la prueba; la diferencia debe registrarse como una decisión de diseño, no corregirse silenciosamente.

## 6. Bloqueos antes de aprobación

Los cinco pares de reuse ya fueron revisados y los cinco movimientos fueron aprobados. La revisión visual de 35 assets ya está hecha: 33 fueron aprobados previamente y 2 extras requieren aprobación específica. La versión operativa conserva 11 placeholders y captions de secuencias de múltiples emojis para los 35 nuevos. Los assets con contenido sexual, lenguaje fuerte o posible riesgo editorial se mantienen marcados individualmente.

El calendario no debe programarse todavía. La siguiente versión debe conservar los 74 slots, retirar de cualquier cola futura los cinco assets ya publicados y mantener `PENDIENTE_GENERAR` en los espacios donde todavía no exista un visual aprobado.

## 7. Decisión y siguiente acción recomendada

Fernando aprobó los cinco movimientos de reuse propuestos: `260508 - Universe.jpg`, `260589.png`, `260518 - Kael.png`, `260590 - Maeve.png` y `741 - Elara+Maeve.png`. La aprobación es parcial y no convierte los 11 placeholders restantes en assets autorizados.

Los extras `260661` y `2607831` ya fueron aprobados y están integrados en el lote de 35 assets. El siguiente control es que Fernando mueva manualmente los 35 archivos a `08 Agosto` sin copias. La programación permanece pendiente de los 11 slots que todavía requieren generación.
