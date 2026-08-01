# Growth OS — Índice de Documentos

**Propósito:** Punto de entrada a toda la documentación operativa del Growth OS (calendario editorial, colas, automatizaciones).
**Estado:** Active
**Fecha de creación:** 2026-07-31
**Última actualización:** 2026-07-31
**Versión:** 1.0
**Autor:** Manus AI
**Documentos relacionados:** `GrowthOS/Integracion_Growth_OS.md`

---

## Documentación del Growth OS

| Documento | Propósito | Estado |
| :--- | :--- | :--- |
| [Arquitectura del Calendario Escalable](01_00_Arquitectura_Calendario_Escalable.md) | Define metadatos, estados y reglas de negocio. | Active |
| [Calendario Editorial Semanal (W01)](01_01_Calendario_Semanal.md) | Tablero operativo de los próximos 7 días. | Active |
| [Content Backlog](01_02_Content_Backlog.md) | Lista maestra ordenada por prioridad. | Active |
| [Reuse Queue](01_03_Reuse_Queue.md) | Contenido con potencial de reutilización. | Active |
| [Production Queue](01_04_Production_Queue.md) | Contenido que requiere producción nueva. | Active |
| [Approval Queue](01_05_Approval_Queue.md) | Contenido pendiente de revisión/aprobación. | Active |
| [Guía de Automatización con Make](02_00_Guia_Automatizacion_Make.md) | Estructura de campos, flujos y reglas para Make. | Active |

---

## Flujo de Trabajo Semanal

1. **Domingo:** Make genera el borrador del calendario semanal (`Flujo 2`) a partir de las colas de `Aprobado` y `Reutilizado`.
2. **Lunes:** Fernando revisa y ajusta el borrador. Comienza la producción de la `Production Queue`.
3. **Martes a Viernes:** Producción activa. Las piezas pasan por `Pendiente Revisión Claude` → `Pendiente Aprobación Fernando` → `Aprobado`.
4. **Sábado:** Última publicación de la semana.
5. **Domingo siguiente:** Make ejecuta el `Flujo 4` (Análisis automático) para recopilar métricas de las piezas publicadas y actualizar el `HypothesisBank`.

---

## Reglas Operativas

1. Este directorio es la **fuente operativa** del calendario. Las colas (`Backlog`, `Reuse`, `Production`, `Approval`) son vistas del inventario completo.
2. El inventario completo de piezas se mantiene en la base de datos externa (Google Sheets / Airtable), no en el repositorio.
3. El repositorio GitHub contiene la **arquitectura**, las **reglas de negocio** y los **entregables semanales**.
4. Ninguna pieza puede publicarse sin pasar por la máquina de estados completa.
5. El campo `Bloqueado_Canon` es un bloqueo operativo, no una etiqueta informativa.
