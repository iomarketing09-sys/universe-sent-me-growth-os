---
title: "Deuda documental P2 — Growth OS"
purpose: "Clasificar el estado de los documentos operativos, históricos y de investigación del Growth OS para mantener una fuente de verdad clara sin borrar trazabilidad ni reactivar procesos retirados."
status: Active
created: 2026-08-15
updated: 2026-08-17
version: "1.5"
author: "Manus AI (CGO)"
related_documents:
  - "GrowthOS/09_00_Estandar_Documentacion_Interna.md"
  - "GrowthOS/00_Índice.md"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
  - "Operations/Research/2026-08-15_Auditoria_General_Growth_OS.md"
  - "Operations/Research/2026-08-15_Community_Engagement_Log.md"
organization: "Operations/Research"
---

# Deuda documental P2 — Growth OS

## 1. Propósito y alcance

Este registro convierte la deuda documental en una cola controlada. No pretende reescribir todo el repositorio en una sola sesión ni eliminar referencias históricas. La regla es separar tres situaciones: documentos que describen la operación vigente, documentos que conservan evidencia histórica y documentos que requieren una revisión futura de metadatos o contenido.

La auditoría delta del 15 de agosto identificó 20 archivos Markdown con marcadores explícitos de estado. La cifra no representa el total de documentos del repositorio: algunos archivos antiguos usan formatos de metadatos diferentes o no tienen encabezado normalizado. Por ello, la normalización se hará por prioridad y no mediante una edición masiva.

## 2. Clasificación vigente

| Clase | Tratamiento | Ejemplos |
|---|---|---|
| `Active_Control` | Debe reflejar la ruta Manus + Meta Graph API, los ledgers actuales y las reglas vigentes. Se valida con cada cambio operativo. | `README.md`, `Studio_Governance.md`, `GrowthOS/01_00_Arquitectura_Calendario_Escalable.md`, `GrowthOS/01_05_Approval_Queue.md`, `GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md`, `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md` |
| `Active_Research` | Puede mantener una hipótesis o auditoría abierta, pero debe distinguir datos verificados de pendientes. | `Operations/Research/2026-08-15_Auditoria_General_Growth_OS.md`, `Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md`, `Operations/Research/2026-08-15_Auditoria_API_Instagram.md` |
| `Active_Playbook_Paused` | Describe una operación preparada pero actualmente pausada; no implica que exista un schedule live. | `Operations/Production/instagram_15_16_scheduler_playbook.md` |
| `Archived_Traceability` | Conserva decisiones, pruebas o procesos retirados. No puede usarse como instrucción de ejecución. | `GrowthOS/02_00_Guia_Automatizacion_Make.md`, changelog y auditorías históricas |
| `Superseded` | Snapshot reemplazado por una fuente más reciente; se conserva para auditoría, pero el índice debe dirigir al documento vigente. | `Operations/Research/2026-08-15_Reconciliacion_Lote_01_Preview.md`, calendarios anteriores ya marcados en el índice |
| `Review_Metadata` | Documento útil que requiere completar título, propósito, estado, fechas, versión, autor, relacionados y organización. No debe cambiarse de contenido sin revisar su contexto. | Blueprints de producción y documentos antiguos sin encabezado completo |

## 3. Make: estado de las referencias restantes

Make está retirado de la operación. Las referencias que todavía aparezcan en el repositorio deben leerse como una de estas dos cosas: trazabilidad histórica o contexto de un blueprint creado cuando el proceso existía. Ninguna referencia restante autoriza la activación de Make ni sustituye la ruta vigente Manus + Meta Graph API.

La limpieza de documentos de control ya fue realizada. Las coincidencias restantes requieren clasificación puntual, no una eliminación global:

| Grupo | Tratamiento |
|---|---|
| `GrowthOS/02_00_Guia_Automatizacion_Make.md` | Mantener como guía histórica y marcar explícitamente `Archived` si el encabezado actual todavía no lo hace. |
| `GrowthOS/00_01_Changelog_GrowthOS.md`, `GrowthOS/00_Índice.md` y auditorías antiguas | Conservar menciones como trazabilidad de decisiones y retirarlas solo si se vuelven ambiguas para la operación vigente. |
| `Operations/Production/CNT023_Episodio2_QueMeLlego_Universe_Elara.md`, `ML_Reel_01_Storyboard_Blueprint.md` y `Showreel_Storyboard_Blueprint.md` | Revisar si la mención es histórica, una nota de contexto o una dependencia de producción. Sustituir una dependencia activa solo cuando el procedimiento alternativo esté documentado. |
| `Operations/Research/2026-08-02_Auditoria_Higgsfield_Grant.md` y `Operations/Research/2026-08-14_Auditoria_Growth_OS.md` | Conservar como evidencia histórica y marcar `Superseded` o `Archived` cuando corresponda. |
| `README.md`, `Studio_Governance.md` y `GrowthOS/11_00_Estrategia_Monetizacion_MercadoLibre.md` | Revisar las menciones históricas restantes para confirmar que ninguna frase presenta Make como ruta actual. |

## 4. Orden de trabajo

La normalización futura debe seguir este orden. El control P2 del 16 de agosto verificó que los documentos de entrada operativos describen Manus + Meta Graph API y que las menciones restantes de Make están clasificadas como trazabilidad histórica; no se requiere una limpieza destructiva adicional.

1. Revisar los documentos de control activos y confirmar que solo describen Manus + Meta Graph API, ledgers y aprobación humana.
2. Marcar como `Archived` la guía histórica de Make y como `Superseded` los snapshots que ya tienen una fuente vigente.
3. Completar metadatos únicamente en documentos activos o de investigación que todavía sean puntos de entrada frecuentes.
4. Añadir enlaces bidireccionales al índice y a los documentos relacionados; ningún documento nuevo debe quedar huérfano.
5. Ejecutar `git diff --check`, validar enlaces locales críticos y registrar el cambio en el changelog.

No se deben modificar automáticamente documentos canónicos administrados por Claude. Si un documento de Growth OS interpreta una regla de canon, el bridge debe citar el HEAD canónico recibido de Claude y separar la interpretación editorial de la autoridad de canon.

## 5. Relación con los P2

### 5.1 Estado del primer lote P2 de comunidad

El primer delta incremental se ejecutó el `2026-08-16T23:41:56Z` desde el cursor `2026-08-16T01:45:00Z`. Meta devolvió tres publicaciones propias y seis comentarios nuevos: cuatro vacíos y dos menciones automáticas `@seguidores`. Se añadieron las seis filas al ledger append-only, no hubo comentarios cualitativos que requirieran respuesta y no se realizó ninguna escritura en Meta. La evidencia mínima está en `Operations/Research/2026-08-16_P2_Comunidad_Delta_01.json`. El siguiente delta debe comenzar después del cursor `2026-08-16T23:41:56Z`, sin crear un scheduler adicional.

### 5.2 Siguiente orden de trabajo P2

| Orden | P2 | Estado | Criterio de cierre |
|---:|---|---|---|
| 1 | Comunidad | **Lote 1 ejecutado** | Ejecutar la siguiente ventana incremental cuando exista un nuevo delta; medir cobertura solo sobre comentarios cualitativos. |
| 2 | Baseline Facebook/Instagram | Pendiente de datos | Esperar métricas 24/72h válidas del lote 15–16, armonizar definiciones y actualizar la baseline separando canales. |
| 3 | Deuda documental | **Normalización P2 cerrada — 2026-08-17** | Se normalizaron estados Instagram, fuente maestra, calendario, índice, changelog y metadatos críticos; las menciones restantes de Make son trazabilidad histórica. Queda solo una cola residual de metadatos antiguos sin impacto operativo. |



El Community Engagement Log, la evidencia del primer delta y la preparación de baseline están documentados en las secciones anteriores. La comunidad ya tiene una ruta incremental y anonimizada; la baseline conserva su snapshot histórico porque las ventanas 24/72h del Facebook activo siguen vacías. CNT-004 queda fuera del lote activo por decisión operativa y conserva su revisión canónica pendiente. Este documento cubre la deuda de organización y los P2 activos; no sustituye el cierre del aprendizaje cuantitativo.

## Referencias

[1]: ../../GrowthOS/09_00_Estandar_Documentacion_Interna.md "Estándar de documentación interna"
[2]: ../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md "Fuente maestra y ledgers del Growth OS"
[3]: 2026-08-15_Auditoria_General_Growth_OS.md "Auditoría general del Growth OS"
