# universe-sent-me-growth-os

Repositorio operativo del **Growth OS** de Universe Sent Me — HypothesisBank, ExperimentLog, Calendario Editorial, colas de producción/aprobación y publicación controlada mediante Manus + Meta Graph API.

Gestionado principalmente por **Manus (Chief Growth Officer)**.

## Relación con el repo de canon

Este repositorio es **independiente** de `iomarketing09-sys/universe-sent-me-1` (la Biblia / repo de canon narrativo). Viven separados a propósito:

- **`universe-sent-me-1`** — canon narrativo (personajes, lugares, filosofía, cosmogonía, gobernanza del estudio). Manus tiene acceso de **solo lectura** ahí — puede consultar reglas, nunca escribir.
- **`universe-sent-me-growth-os`** (este repo) — todo lo operativo de crecimiento. Manus tiene acceso de lectura y escritura completo aquí.

El puente entre ambos es `GrowthOS/Integracion_Growth_OS.md`, que mantiene un caché fechado de las reglas de canon relevantes (con commit de referencia del repo de Biblia) para que Manus pueda generar hooks y programar contenido sin necesitar acceso directo al repo de canon. La operación vigente usa validación explícita de Manus y Meta Graph API; la guía de Make es únicamente histórica y archivada.

Las reglas completas de gobernanza — roles, permisos, flujo de trabajo, checklist previo a publicación, revisiones diarias y semanales con Claude — viven en `Studio_Governance.md` dentro de este mismo repositorio.

## Estructura

```
GrowthOS/
├── 00_Índice.md                              # punto de entrada
├── 01_00_Arquitectura_Calendario_Escalable.md
├── 01_01_Calendario_Semanal.md
├── 01_02_Content_Backlog.md
├── 01_03_Reuse_Queue.md
├── 01_04_Production_Queue.md
├── 01_05_Approval_Queue.md
├── 02_00_Guia_Automatizacion_Make.md          # referencia histórica archivada, no operativa
├── Content_Inventory.csv
├── Integracion_Growth_OS.md                  # documento puente con el canon
├── Canon_Contradictions_Report.md
└── USM_Growth_OS.xlsx

Studio_Governance.md                          # governance, roles, permisos, revisiones
```

## Regla de bloqueo (no negociable)

Ninguna pieza de contenido puede pasar a `Programado` o `Publicado` sin que su campo `Estado Canon` / `Bloqueado_Canon` diga `Aprobado` — y ese campo solo lo puede marcar **Fernando o Claude**, nunca Manus ni una automatización.
