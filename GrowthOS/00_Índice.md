# Growth OS — Índice de Documentos

**Propósito:** Punto de entrada a toda la documentación operativa del Growth OS (calendario editorial, colas, automatizaciones, governance).
**Estado:** Active
**Fecha de creación:** 2026-07-31
**Última actualización:** 2026-08-14
**Versión:** 1.5
**Autor:** Manus AI
**Documentos relacionados:** `GrowthOS/Integracion_Growth_OS.md`, `../Studio_Governance.md`

---

## Documentación del Growth OS

| Documento | Propósito | Estado |
| :--- | :--- | :--- |
| [Changelog del Growth OS](00_01_Changelog_GrowthOS.md) | Registro de hitos, integraciones y cambios de versión. | Active |
| [Arquitectura del Calendario Escalable](01_00_Arquitectura_Calendario_Escalable.md) | Define metadatos, estados y reglas de negocio. | Active |
| [Calendario Editorial Semanal (W01)](01_01_Calendario_Semanal.md) | Tablero operativo de los próximos 7 días. | Active |
| [Formato del Calendario Semanal (CGO v3.0)](04_00_Formato_Calendario_Semanal_CGO.md) | Plantilla oficial por día de la semana, validada con datos de mayo 2026. | Active |
| [Calendario Oficial 4–9 de Agosto](05_02_Calendario_04_09_Agosto.md) | Calendario de la semana 4-9 agosto, aplicando la plantilla CGO v3.0. Declarado oficial por Fernando (2026-08-03). | Superseded |
| [Calendario 10–16 de Agosto](05_03_Calendario_10_16_Agosto.md) | Nueva semana: menos reuse (solo piezas top validadas), más contenido nuevo, horarios basados en datos reales de mediana horaria/diaria. | Active |
| [Content Backlog](01_02_Content_Backlog.md) | Lista maestra ordenada por prioridad. | Active |
| [Reuse Queue](01_03_Reuse_Queue.md) | Contenido con potencial de reutilización (regla 30 días). | Active |
| [Production Queue](01_04_Production_Queue.md) | Contenido que requiere producción nueva. | Active |
| [Approval Queue](01_05_Approval_Queue.md) | Contenido pendiente de revisión/aprobación. | Active |
| [Guía de Automatización con Make](02_00_Guia_Automatizacion_Make.md) | Estructura de campos, flujos y reglas para Make. | Active |
| [Sistema de Generación de Memes](03_00_Sistema_Generacion_Memes.md) | Flujo de ingesta (Drive), adaptación (Gemini) y archivo visual (GitHub). | Active |
| [Canon Contradictions Report](Canon_Contradictions_Report.md) | Contradicciones activas que bloquean producción. | Active |
| [Inventario de Contenido](Content_Inventory.csv) | CSV maestro con metadatos de las 25 piezas existentes. | Active |
| [Auditoría Higgsfield Grant](../Operations/Research/2026-08-02_Auditoria_Higgsfield_Grant.md) | Análisis estratégico para la candidatura del Filmmaker Grant. | Review |
| [Reporte Mensual Junio-Julio 2026](../Operations/Research/2026-08-08_Reporte_Mensual_Junio_Julio_2026.md) | Cierra el vacío de datos entre mayo y el análisis de 28 días de agosto. 61 días vía Windsor.ai, top días y posts por mes. | Active |
| [Métricas Baseline — FB & IG](08_00_Metricas_Baseline_Plataformas.md) | Datos reales de Windsor.ai: top 10 FB, tabla Reels, tabla IG, insights de canal. Actualizar cada domingo. | Active |
| [Estándar de Documentación Interna](09_00_Estandar_Documentacion_Interna.md) | Reglas permanentes para que Manus cree y actualice documentos en este repositorio. | Active |
| [Kit de Hashtags USM](10_00_Kit_de_Hashtags_USM.md) | Roster fijo de hashtags de marca (personaje, lugar, concepto) con firma USM. Evita typos y nombres no aprobados. | Active |
| [Estrategia Monetización Mercado Libre](11_00_Estrategia_Monetizacion_MercadoLibre.md) | Marco operativo para capitalizar la afiliación de Mercado Libre. | Active |
| [Sistema de Dos Capas: Contenido vs. Canon](12_00_Sistema_Dos_Capas_Contenido_Canon.md) | Separa la capa libre de memes/reels (algoritmo, exploración) de la capa de canon (Biblia, decisiones permanentes). Define mecanismo de promoción deliberada de meme a canon. | Active |
| [Pipeline de Publicación Local y Estándar CSV](13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md) | Documenta el script propio de Fernando, el estándar CSV y la Custom API de Meta configurada para Universe Sent Me. | Active |
| [Auditoría del Growth OS — 14 de agosto](../Operations/Research/2026-08-14_Auditoria_Growth_OS.md) | Evalúa la programación modificada, las integraciones, la automatización y el ciclo de aprendizaje. | Review |

---

## Flujo de Trabajo Semanal

1. **Domingo:** Make genera el borrador del calendario semanal (`Flujo 2`) a partir de las colas de `Aprobado` y `Reutilizado`. Claude revisa el caché de canon y Manus actualiza `Integracion_Growth_OS.md` si hay cambios.
2. **Lunes:** Fernando revisa y aprueba el calendario semanal. Comienza la producción de la `Production Queue`.
3. **Martes a Viernes:** Producción activa. **Revisión diaria** con Claude para validar contenido nuevo.
4. **Sábado:** Última publicación de la semana.
5. **Domingo siguiente:** Make ejecuta el `Flujo 4` (Análisis automático) para recopilar métricas de las piezas publicadas y actualizar el `HypothesisBank`.

---

## Governance y Revisiones

Las reglas de acceso, roles y calendario de revisiones viven en `../Studio_Governance.md`:
- **Revisiones diarias:** Todo contenido nuevo debe ser validado por Claude antes de entrar a producción.
- **Revisiones semanales:** Sincronización del caché de canon, revisión del `HypothesisBank` y confirmación de reglas de bloqueo.

---

## Reglas Operativas

1. Este directorio es la **fuente operativa** del calendario. Las colas (`Backlog`, `Reuse`, `Production`, `Approval`) son vistas del inventario completo.
2. El inventario completo de piezas se mantiene en la base de datos externa (Google Sheets / Airtable), no en el repositorio.
3. El repositorio GitHub contiene la **arquitectura**, las **reglas de negocio** y los **entregables semanales**.
4. Ninguna pieza puede publicarse sin pasar por la máquina de estados completa.
5. El campo `Bloqueado_Canon` es un bloqueo operativo, no una etiqueta informativa.
6. **Regla de Reutilización (30 días):** Ninguna pieza puede ser reutilizada si han pasado menos de 30 días desde su `Fecha_Ultima_Publicacion`.
