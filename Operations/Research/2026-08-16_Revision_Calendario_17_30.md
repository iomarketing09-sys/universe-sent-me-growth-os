---
title: "Revisión del calendario experimental 17–30 de agosto"
purpose: "Auditar y dejar trazable la versión aprobada de 74 slots contra el inventario de Drive y los ledgers antes de programar en Facebook y mover manualmente los archivos."
status: Active
created: 2026-08-16
updated: 2026-08-16
version: "1.1"
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
  - "Operations/Research/2026-08-16_Calendario_Operativo_17_30_Agosto.csv"
  - "Operations/Research/2026-08-16_Manifiesto_Movimiento_35_Memes_Agosto.csv"
organization: "Operations/Research"
---

# Revisión del calendario experimental 17–30 de agosto

## 1. Resultado ejecutivo

La versión aprobada contiene **74 slots en 14 días**: 35 assets nuevos, 36 reuse Top y 3 reuse Reserve. La estructura de frecuencia conserva la distribución horaria aprobada: seis publicaciones de lunes a jueves, cuatro el viernes y sábado, y cinco el domingo con slots nocturnos de 22:00.

La versión ya está integrada en el calendario operativo y queda lista para programación en Facebook. Los cinco assets publicados el 15–16 permanecen fuera de la cola, las variantes con el número 260508 conservan filename completo y Drive ID, y los reuse incorporados quedan trazados en el manifiesto. Instagram permanece pendiente y no se modifica.

## 2. Conciliación de fuentes

| Fuente | Resultado | Interpretación operativa |
|---|---:|---|
| Slots de la propuesta con copys | 74 | Estructura completa para 17–30 de agosto. |
| Slots `Nueva` | 35 | Assets aprobados visualmente y asignados; cada uno conserva caption de secuencia de emojis. |
| Slots `Reuse_Top` | 36 | Incluye los 28 reuse aprobados previamente y 8 reuse verificados de `06 Junio/Top`. |
| Inventario nuevo de Drive | 38 | Snapshot del 15 de agosto, todos con estado `Nuevo_Pendiente_Revision`. |
| Assets nuevos ya publicados en 15–16 | 5 | 2608030, 2608033, 2608036, 2608037 y 2608060; no deben volver a tratarse como disponibles para generación o reuse inmediato. |
| Assets nuevos aún no registrados como publicados | 33 | Cola real disponible según la conciliación contra `Publication_Log.csv`; requiere revisión visual/editorial antes de asignar slots. |
| Slots `Reuse_Reserve` | 3 | `260571`, `260550` y `260617` de la raíz disponible de `05 Mayo`; se conservan como reserve por rendimiento histórico inferior al Top 28. |
| Total de reuse | 39 | 36 `Reuse_Top` + 3 `Reuse_Reserve`; no hay placeholders pendientes. |

La conciliación se hizo contra los Meta IDs y referencias reales del `Publication_Log.csv`. Los cinco assets consumidos no se asignaron a ningún slot futuro; la lista de 33 disponibles no equivale todavía a una lista aprobada para publicación.

## 3. Hallazgo sobre 260508

Drive contiene dos archivos distintos con el mismo número de referencia:

| Archivo | Drive ID | Evidencia |
|---|---|---|
| `260508 - Universe.jpg` | `1c_AQFPbigiR39cH7f39h2MzCFvQL799b` | JPG 1122×1402; Universe con el texto “Karen, tú eres cine, nunca lo dudes. Del dramático, pero cine al fin.” |
| `Universe - Existencial 260508.png` | `1eVre3AC1EjmEUPHKMjVRbQ3efXtYyh-8` | PNG 1194×1317; imagen de cerebro/corazón con el texto “El momento increíble cuando estos dos finalmente deciden sincronizarse”. |

No se deben fusionar ni eliminar. Para evitar ambigüedad, el calendario debe conservar el filename completo y, si se convierte en ledger operativo, registrar también el Drive ID.

## 4. Secuencia de reuse

La versión integrada contiene 39 reuse y conserva cinco pares consecutivos, el mínimo alcanzable bajo la distribución aprobada sin eliminar assets nuevos ni cambiar la frecuencia. El máximo teórico de reuse perfectamente alternados en 74 slots es 37; por tanto, cero pares no es posible con 39 reuse. Los cinco pares quedan documentados para la revisión de métricas:

| Slot anterior | Slot siguiente |
|---|---|
| 21 agosto 10:00 — `2607838 - Dios - Quien me creo a mi (29-jun-26).png` | 21 agosto 11:00 — `260635 - Universe.png` |
| 23 agosto 19:00 — `260757 - Maeve - Estas seguro¿ (14-jun-26).png` | 23 agosto 22:00 — `260625.png` |
| 25 agosto 11:00 — `Universe - Existencial 622.png` | 25 agosto 13:30 — `2607792 - fantasma+Universe - El gato ;o (21-jun-26).jpeg` |
| 28 agosto 10:00 — `260527 - Universe.png` | 28 agosto 11:00 — `260550 - Universe.png` (`Reuse_Reserve`) |
| 30 agosto 19:00 — `260617 - Elara+Kael.png` (`Reuse_Reserve`) | 30 agosto 22:00 — `260528 - Universe.png` |

El requisito histórico específico sobre `260528` sí está respetado: permanece en domingo 30 de agosto a las 22:00. El par entre los días 27 y 28 tampoco queda consecutivo porque el 27 termina con una pieza nueva a las 19:00.

## 5. Proporción y frecuencia

La versión aprobada usa 35 nuevas y 39 reuse, equivalente a **47.3% nuevo y 52.7% reuse**. Esto registra explícitamente la decisión de completar los 11 slots con reuse de junio y mayo, en lugar de generar 11 piezas nuevas. La proporción debe considerarse una condición experimental de esta quincena y evaluarse con métricas reales.

## 6. Bloqueos antes de aprobación

Los cinco pares de reuse y los movimientos necesarios fueron revisados. Fernando aprobó la completación con 8 reuse de junio y 3 reuse Reserve de mayo. La versión operativa contiene 35 assets nuevos, 39 reuse y cero placeholders. Los assets con contenido sexual, lenguaje fuerte o posible riesgo editorial se mantienen marcados individualmente. Instagram no se programa en esta fase.

El calendario queda listo para programarse únicamente en Facebook mediante la API Graph. Los archivos todavía permanecen en sus carpetas de origen; después de confirmar la programación, Fernando realizará el movimiento manual `MOVE_ONLY` al folder `08 Agosto`. No se deben crear copias ni modificar Instagram.

## 7. Decisión y siguiente acción recomendada

Fernando aprobó los cinco movimientos de reuse propuestos: `260508 - Universe.jpg`, `260589.png`, `260518 - Kael.png`, `260590 - Maeve.png` y `741 - Elara+Maeve.png`. La aprobación incluye la completación de los 11 slots: 8 reuse de junio y 3 reuse Reserve de mayo. Los 74 slots quedan asignados y autorizados para programación en Facebook.

Los extras `260661` y `2607831` siguen integrados en el lote de 35 assets nuevos. El manifiesto actualizado contiene 46 archivos y ordena movimiento manual posterior a la programación de Facebook; Instagram permanece pendiente.
