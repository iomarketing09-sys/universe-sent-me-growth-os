# Studio Governance — Resumen Operativo (Growth OS)

**Propósito:** Resumen operativo de roles, permisos y flujo de trabajo del Growth OS. **Este no es el documento autoritativo de canon.** El documento completo y vinculante vive en el repositorio de canon: `universe-sent-me-1/Studio/Studio_Governance.md`. En caso de conflicto entre este resumen y el documento completo, **el documento completo siempre gana.**
**Estado:** Active
**Fecha de creación:** 2026-07-31
**Última actualización:** 2026-11-02
**Versión:** 2.0
**Autor:** Manus AI (v1.0); actualización vigente por CGO (v2.0, 2026-11-02)
**Documentos relacionados:** `GrowthOS/Integracion_Growth_OS.md`, `GrowthOS/01_00_Arquitectura_Calendario_Escalable.md`, `GrowthOS/09_00_Estandar_Documentacion_Interna.md`

> **Nota de arquitectura:** Existen dos archivos con nombre Studio_Governance:
> este resumen operativo y el documento completo en
> `universe-sent-me-1/Studio/Studio_Governance.md`, que es la fuente autoritativa
> de canon. El CGO debe leer el documento completo para cualquier decisión que
> no esté cubierta por este resumen.

---

## 1. Repositorios y Separación de Responsabilidades

| Repositorio | Propósito | Permisos del CGO | Autoridad |
| :--- | :--- | :--- | :--- |
| `universe-sent-me-1` | Canon narrativo (personajes, lugares, filosofía, cosmogonía) | **Solo lectura** | Fernando |
| `universe-sent-me-growth-os` | Operaciones de crecimiento (calendario, colas, hipótesis y publicación controlada) | **Lectura y escritura** | Fernando (canon) / CGO (operación) |

El puente entre ambos repositorios es `GrowthOS/Integracion_Growth_OS.md`, que mantiene un caché fechado de las reglas de canon relevantes con commit de referencia. El CGO consulta este caché para preparar contenido, pero no puede modificar el canon ni aprobarlo.

---

## 2. Roles

| Rol | Agente / Persona | Permisos |
| :--- | :--- | :--- |
| **Chief Growth Officer (CGO)** | Codex | Operar el repo, timers, runbooks y automatizaciones. Preparar contenido y evidencia. Leer canon. No aprobar canon ni publicar sin instrucción explícita. |
| **Accountable y autoridad de canon** | Fernando | Aprobar o rechazar canon y contenido. Decidir tono, dirección narrativa, estrategia y publicación. Único actor que puede cambiar estado a `Aprobado`. |
| **Owners funcionales** | Comunicaciones, Growth, Datos, Monetización | Operar su edificio y responder por sus servicios. No pueden aprobar canon. |

La autoridad de canon que antes correspondía a Claude fue absorbida por
Fernando. Claude y Manus no tienen roles activos en el Growth OS.

---

## 3. Regla de Bloqueo Operativo (No Negociable)

> Ninguna pieza de contenido puede pasar a `Programado` o `Publicado` sin que su campo `Estado Canon` / `Bloqueado_Canon` diga `Aprobado` — y ese campo solo lo puede marcar **Fernando**, nunca el CGO, un owner funcional o una automatización.

Esta regla se aplica tanto en el repositorio como en la base de datos externa (Google Sheets / Airtable).

---

## 4. Calendario de Revisiones

El siguiente calendario establece la frecuencia y el alcance de las revisiones
entre el CGO y Fernando.

### 4.1 Revisiones Diarias (Contenido Nuevo)

**Propósito:** Validar que todo contenido nuevo no viole reglas de canon antes de entrar al pipeline de producción.

| Campo | Valor |
| :--- | :--- |
| **Frecuencia** | Diaria |
| **Quién revisa** | CGO (preparación y evidencia) + Fernando (validación y aprobación) |
| **Qué se revisa** | Cada pieza nueva que pase de `Idea` a `Pendiente de Producción` |
| **Criterio** | Ninguna pieza puede avanzar a `En Producción` sin que Fernando confirme que no hay contradicciones con el canon (personajes, lugares, filosofía, cosmogonía) |
| **Resultado** | Si hay contradicción, se genera un `Canon_Contradictions_Report.md` y la pieza se mueve a `Rechazado / Requiere Reescritura` |

### 4.2 Revisiones Semanales

**Propósito:** Sincronizar el caché de canon, verificar que no haya reglas desactualizadas y revisar el estado general del Growth OS.

| Campo | Valor |
| :--- | :--- |
| **Frecuencia** | Semanal (domingo, antes de la generación del calendario) |
| **Quién ejecuta** | CGO (preparación) + Fernando (decisión) |
| **Qué se revisa** | 1. Verificar que el commit de referencia en `Integracion_Growth_OS.md` sea el HEAD del repo de canon. 2. Actualizar el caché de reglas si hay cambios. 3. Revisar el estado del `HypothesisBank` y el `ExperimentLog`. 4. Confirmar que las reglas de bloqueo siguen vigentes. |
| **Resultado** | Si hay cambios en el canon, el CGO actualiza `Integracion_Growth_OS.md` con la decisión de Fernando y re-evalúa las piezas afectadas. |

---

## 5. Flujo de Trabajo Diario

1. **Mañana:** el CGO revisa la cola de `Pendiente de Producción` y prepara la evidencia.
2. **Mediodía:** el CGO presenta las piezas nuevas a Fernando para validación de canon.
3. **Tarde:** Fernando devuelve el veredicto. Si hay contradicciones, se genera el reporte.
4. **Noche:** el CGO actualiza las colas, pero solo Fernando cambia el estado protegido de canon.

---

## 6. Flujo de Trabajo Semanal

| Día | Actividad | Responsable |
| :--- | :--- | :--- |
| **Domingo** | 1. El CGO prepara el borrador del calendario desde las colas. 2. El CGO verifica el caché de canon. 3. Fernando valida cambios de canon; el CGO actualiza `Integracion_Growth_OS.md`. | CGO + Fernando |
| **Lunes** | Fernando revisa y aprueba el calendario semanal. Comienza la producción. | Fernando |
| **Martes–Viernes** | Producción activa. Revisión diaria de contenido nuevo y evidencia. | CGO + Fernando |
| **Sábado** | Última publicación de la semana. | Growth |
| **Cada 48 horas** | El CGO extrae las métricas 24/72 horas elegibles y Fernando valida las decisiones de hipótesis. | CGO + Fernando |

---

## 7. Regla de Medición de Campañas

> Toda campaña de Meta Ads con `meta_ids.json` y fecha de inicio debe capturar
> métricas por anuncio a las 24, 48 y 72 horas, cada 24 horas hasta su cierre y
> un corte final dos horas después del cierre. La captura es automática e
> idempotente; no depende de una ejecución manual.

La automatización mide y genera un plan local `recommendation_only`. No pausa
anuncios, no cambia presupuesto y no escribe en Meta. Como máximo propone
pausar anuncios individuales; pausar un ad set o la campaña completa requiere
una revisión humana explícita. Toda acción propuesta queda en estado `pending`
hasta que Fernando la apruebe, y la ejecución futura debe vivir en una
capacidad separada con auditoría. El detalle operativo vive en
`docs/REGLA_METRICAS_CAMPANAS.md`.

La captura puede reconciliar automáticamente los IDs publicados de
`campaign.json` contra la realidad observada en Meta. Esa reconciliación solo
modifica metadata local, deja historial del cambio y nunca ejecuta un `POST`.

---

## 8. Regla de Reutilización (30 Días)

> Ninguna pieza puede ser reutilizada si han pasado menos de **30 días** desde su `Fecha_Ultima_Publicacion`. Esta regla protege contra la fatiga de audiencia y es ineludible.

Los campos `Fecha_Ultima_Publicacion` y `Dias_Desde_Publicacion` en el inventario maestro son obligatorios para que el CGO pueda aplicar automáticamente el filtro de 30 días.

---

## 9. Reglas de Documentación Permanente

1. **Todo conocimiento con valor permanente debe terminar documentado en un repositorio.**
2. **Las conversaciones son temporales. Los documentos son permanentes.**
3. **Antes de crear un documento nuevo, verificar si ya existe uno relacionado. Si existe, actualizarlo.**
4. **Solo crear un documento nuevo cuando represente un concepto realmente nuevo.**
5. **Todo documento nuevo debe enlazar con al menos un documento existente.**
6. **Si un documento modifica información existente, indicar qué otros documentos requieren actualización.**
7. **Si existe una diferencia entre una conversación y un documento del repositorio, el documento tiene prioridad.**

---

## 10. Gestión de Contradicciones de Canon

Cuando el CGO detecta una posible contradicción durante una revisión diaria:

1. Se crea o actualiza `GrowthOS/Canon_Contradictions_Report.md` con el detalle de la contradicción.
2. La pieza afectada se mueve a `Rechazado / Requiere Reescritura`.
3. Se notifica a Fernando, única autoridad de canon, con las correcciones necesarias.
4. La pieza no puede re-entrar al pipeline hasta que Fernando confirme la corrección.

---

## 11. Historial de Cambios

| Fecha | Versión | Cambio | Autor |
| :--- | :--- | :--- | :--- |
| 2026-07-31 | 1.0 | Creación del documento de governance. Definición de roles, permisos, revisiones diarias y semanales. | Manus AI |
| 2026-08-15 | 1.2 | Se retira la dependencia operativa de Make; el flujo vigente usa Manus, Meta Graph API y revisión con Claude/Fernando. | Manus AI |
| 2026-10-30 | 1.3 | Se agrega la regla de captura automática E24/E48/E72/diaria/FINAL para campañas de Meta Ads. | CGO |
| 2026-10-30 | 1.4 | Se agrega el plan de cambios por corte: recomendaciones por anuncio, sin escritura en Meta y con aprobación humana obligatoria. | CGO |
| 2026-11-02 | 2.0 | Fernando absorbe la autoridad de canon; Codex queda como CGO operador técnico; Manus y Claude salen de los roles activos. | CGO |
