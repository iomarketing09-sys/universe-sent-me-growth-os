# Studio Governance — Resumen Operativo (Growth OS)

**Propósito:** Resumen de roles, permisos y flujo de trabajo para uso rápido de Manus. **Este no es el documento autoritativo.** El documento completo y vinculante vive en el repositorio de canon: `universe-sent-me-1/Studio/Studio_Governance.md`. En caso de conflicto entre este resumen y el documento completo, **el documento completo siempre gana.**
**Estado:** Active
**Fecha de creación:** 2026-07-31
**Última actualización:** 2026-08-15
**Versión:** 1.2
**Autor:** Manus AI (v1.0); actualización de encabezado por Claude (v1.1, 2026-08-03)
**Documentos relacionados:** `GrowthOS/Integracion_Growth_OS.md`, `GrowthOS/01_00_Arquitectura_Calendario_Escalable.md`, `GrowthOS/09_00_Estandar_Documentacion_Interna.md`

> **⚠️ NOTA DE ARQUITECTURA (Claude, 2026-08-03):** Existen dos archivos con nombre Studio_Governance: este resumen en `universe-sent-me-growth-os/` y el documento completo en `universe-sent-me-1/Studio/Studio_Governance.md` (417 líneas, versión autoritativa con secciones completas de GitHub, canon, assets, pipeline y reglas para IA). Manus debe leer el documento completo para decisiones que no estén cubiertas por este resumen.

---

## 1. Repositorios y Separación de Responsabilidades

| Repositorio | Propósito | Permisos de Manus | Guardián |
| :--- | :--- | :--- | :--- |
| `universe-sent-me-1` | Canon narrativo (personajes, lugares, filosofía, cosmogonía) | **Solo lectura** | Claude |
| `universe-sent-me-growth-os` | Operaciones de crecimiento (calendario, colas, hipótesis y publicación controlada) | **Lectura y escritura** | Manus |

El puente entre ambos repositorios es `GrowthOS/Integracion_Growth_OS.md`, que mantiene un caché fechado de las reglas de canon relevantes con commit de referencia. Manus consulta este caché para generar contenido sin necesitar acceso directo al repo de canon.

---

## 2. Roles

| Rol | Agente / Persona | Permisos |
| :--- | :--- | :--- |
| **Chief Growth Officer** | Manus (Manus AI) | Crear, editar, commitear y pushear en `universe-sent-me-growth-os`. Leer canon de `universe-sent-me-1`. Generar contenido. Automatizar flujos. |
| **Guardián de Canon** | Claude | Leer y aprobar/revocar contenido. Solo escritura en `universe-sent-me-1`. Sin acceso de escritura a `universe-sent-me-growth-os`. |
| **Aprobador Final** | Fernando | Aprobar o rechazar contenido. Decidir tono, dirección narrativa y estrategia. Único actor que puede cambiar estado a "Aprobado". |

---

## 3. Regla de Bloqueo Operativo (No Negociable)

> Ninguna pieza de contenido puede pasar a `Programado` o `Publicado` sin que su campo `Estado Canon` / `Bloqueado_Canon` diga `Aprobado` — y ese campo solo lo puede marcar **Fernando o Claude**, nunca Manus ni una automatización.

Esta regla se aplica tanto en el repositorio como en la base de datos externa (Google Sheets / Airtable).

---

## 4. Calendario de Revisiones

El siguiente calendario establece la frecuencia y el alcance de las revisiones entre Manus y Claude.

### 4.1 Revisiones Diarias (Contenido Nuevo)

**Propósito:** Validar que todo contenido nuevo no viole reglas de canon antes de entrar al pipeline de producción.

| Campo | Valor |
| :--- | :--- |
| **Frecuencia** | Diaria |
| **Quién revisa** | Manus (preparación) + Claude (validación) |
| **Qué se revisa** | Cada pieza nueva que pase de `Idea` a `Pendiente de Producción` |
| **Criterio** | Ninguna pieza puede avanzar a `En Producción` sin que Claude confirme que no hay contradicciones con el canon (personajes, lugares, filosofía, cosmogonía) |
| **Resultado** | Si hay contradicción, se genera un `Canon_Contradictions_Report.md` y la pieza se mueve a `Rechazado / Requiere Reescritura` |

### 4.2 Revisiones Semanales (Revisión General con Claude)

**Propósito:** Sincronizar el caché de canon, verificar que no haya reglas desactualizadas y revisar el estado general del Growth OS.

| Campo | Valor |
| :--- | :--- |
| **Frecuencia** | Semanal (domingo, antes de la generación del calendario) |
| **Quién ejecuta** | Manus (solicitud) + Claude (respuesta) |
| **Qué se revisa** | 1. Verificar que el commit de referencia en `Integracion_Growth_OS.md` sea el HEAD del repo de canon. 2. Actualizar el caché de reglas si hay cambios. 3. Revisar el estado del `HypothesisBank` y el `ExperimentLog`. 4. Confirmar que las reglas de bloqueo siguen vigentes. |
| **Resultado** | Si hay cambios en el canon, Manus actualiza `Integracion_Growth_OS.md` y re-evalúa las piezas en el backlog que puedan estar afectadas. |

---

## 5. Flujo de Trabajo Diario

1. **Mañana:** Manus revisa la cola de `Pendiente de Producción` y prepara las piezas nuevas.
2. **Mediodía:** Manus envía las piezas nuevas a Claude para validación de canon.
3. **Tarde:** Claude devuelve el veredicto. Si hay contradicciones, se genera el reporte.
4. **Noche:** Manus actualiza las colas y el estado de las piezas según el veredicto.

---

## 6. Flujo de Trabajo Semanal

| Día | Actividad | Responsable |
| :--- | :--- | :--- |
| **Domingo** | 1. Manus prepara el borrador del calendario desde las colas. 2. Claude revisa el caché de canon. 3. Manus actualiza `Integracion_Growth_OS.md` si hay cambios. | Manus + Claude |
| **Lunes** | Fernando revisa y aprueba el calendario semanal. Comienza la producción. | Fernando |
| **Martes–Viernes** | Producción activa. Revisión diaria de contenido nuevo con Claude. | Manus + Claude |
| **Sábado** | Última publicación de la semana. | Manus |
| **Cada 48 horas** | Manus extrae únicamente las métricas 24/72 horas que ya sean elegibles y Claude/CGO valida las hipótesis. | Manus + Claude/CGO |

---

## 7. Regla de Reutilización (30 Días)

> Ninguna pieza puede ser reutilizada si han pasado menos de **30 días** desde su `Fecha_Ultima_Publicacion`. Esta regla protege contra la fatiga de audiencia y es ineludible.

Los campos `Fecha_Ultima_Publicacion` y `Dias_Desde_Publicacion` en el inventario maestro son obligatorios para que Manus pueda aplicar automáticamente el filtro de 30 días.

---

## 8. Reglas de Documentación Permanente

1. **Todo conocimiento con valor permanente debe terminar documentado en un repositorio.**
2. **Las conversaciones son temporales. Los documentos son permanentes.**
3. **Antes de crear un documento nuevo, verificar si ya existe uno relacionado. Si existe, actualizarlo.**
4. **Solo crear un documento nuevo cuando represente un concepto realmente nuevo.**
5. **Todo documento nuevo debe enlazar con al menos un documento existente.**
6. **Si un documento modifica información existente, indicar qué otros documentos requieren actualización.**
7. **Si existe una diferencia entre una conversación y un documento del repositorio, el documento tiene prioridad.**

---

## 9. Gestión de Contradicciones de Canon

Cuando Claude detecta una contradicción durante una revisión diaria:

1. Se crea o actualiza `GrowthOS/Canon_Contradictions_Report.md` con el detalle de la contradicción.
2. La pieza afectada se mueve a `Rechazado / Requiere Reescritura`.
3. Se notifica a Fernando con las correcciones necesarias.
4. La pieza no puede re-entrar al pipeline hasta que Fernando confirme la corrección.

---

## 10. Historial de Cambios

| Fecha | Versión | Cambio | Autor |
| :--- | :--- | :--- | :--- |
| 2026-07-31 | 1.0 | Creación del documento de governance. Definición de roles, permisos, revisiones diarias y semanales. | Manus AI |
| 2026-08-15 | 1.2 | Se retira la dependencia operativa de Make; el flujo vigente usa Manus, Meta Graph API y revisión con Claude/Fernando. | Manus AI |
