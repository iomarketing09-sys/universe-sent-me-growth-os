# universe-sent-me-growth-os

Repositorio operativo del **Growth OS** de Universe Sent Me — HypothesisBank, ExperimentLog, Calendario Editorial, colas de producción/aprobación y publicación controlada mediante CGO + Meta Graph API.

El **CGO (Codex)** es el operador técnico del repositorio. **Fernando** es el
accountable final y la única autoridad de canon.

## Relación con el repo de canon

Este repositorio es **independiente** de `iomarketing09-sys/universe-sent-me-1` (la Biblia / repo de canon narrativo). Viven separados a propósito:

- **`universe-sent-me-1`** — canon narrativo (personajes, lugares, filosofía, cosmogonía, gobernanza del estudio). El CGO tiene acceso de **solo lectura** ahí: puede consultar reglas, nunca escribir ni aprobar canon.
- **`universe-sent-me-growth-os`** (este repo) — todo lo operativo de crecimiento. El CGO tiene acceso de lectura y escritura aquí, sujeto a la aprobación de Fernando para canon y publicación.

El puente entre ambos es `GrowthOS/Integracion_Growth_OS.md`, que mantiene un caché fechado de las reglas de canon relevantes (con commit de referencia del repo de Biblia) para que el CGO pueda preparar hooks y contenido sin sustituir la validación de Fernando. La operación vigente usa validación explícita de Fernando y Meta Graph API; la guía de Make es únicamente histórica y archivada.

## Credenciales Meta

Los módulos de Meta resuelven sus variables mediante `modules/config/env.py` sin
modificar `os.environ`. La precedencia es: `.env` raíz, `.env` del tenant y
finalmente el entorno del proceso. Los valores del proceso siempre ganan.

Las reglas completas de gobernanza — roles, permisos, flujo de trabajo,
checklist previo a publicación y revisiones — viven en `Studio_Governance.md`.
La operación de timers, alertas y runbooks vive en `docs/OPERACION_COMPARTIDA.md`.

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

Ninguna pieza de contenido puede pasar a `Programado` o `Publicado` sin que su
campo `Estado Canon` / `Bloqueado_Canon` diga `Aprobado`. Ese campo solo lo puede
marcar **Fernando**, nunca el CGO, un owner funcional o una automatización.
