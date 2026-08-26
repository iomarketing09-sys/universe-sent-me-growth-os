---
title: "Shadow ledger privado append-only de observaciones normalizadas — Universe Sent Me"
purpose: "Definir el ledger privado de validación para comprobar idempotencia, supersedencia e integridad de observaciones normalizadas antes de cualquier ledger canónico o vista derivada."
status: Review
created: 2026-08-25
updated: 2026-08-25
version: "1.0"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-25_Esquema_Normalizacion_Determinista_Multicanal_USM.md"
  - "Operations/Automation/2026-08-25_Guia_Piloto_Local_API_Oficial_Metricas_USM.md"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
  - "GrowthOS/todo.md"
organization: "Operations/Automation"
---

# Shadow ledger privado append-only de observaciones normalizadas — Universe Sent Me

## Propósito y estado

Este shadow ledger es una capa de validación **local y privada**. No es una fuente canónica, no modifica `Metrics_Snapshot_Log.csv`, no rellena una pestaña de Google Sheets y no abastece OmniRoute. Su función es demostrar que las observaciones normalizadas pueden conservar un historial append-only, evitar duplicados y representar correcciones mediante supersedencia antes de proponer cualquier materialización futura.

> **Estado:** `Review`. G-NORM-4 autoriza implementación y pruebas sintéticas del mecanismo. La inserción de observaciones reales privadas requiere una autorización posterior y no se activa por este documento.

## Ubicación y protección

| Activo | Ruta privada prevista | Permiso | Regla |
|---|---|---|---|
| Directorio del ledger | `~/.local/share/usm-metrics/shadow-ledger/` | `0700` | Nunca se versiona ni sincroniza a GitHub/Drive. |
| Archivo de eventos | `normalized_metric_observations.shadow.jsonl` | `0600` | Solo se abre con append atómico; no existe actualización in-place. |
| Fixture de prueba | `Operations/Automation/fixtures/shadow_ledger_synthetic.json` | Versionado | Solo datos sintéticos, sin IDs o evidencia reales. |

La ejecución con fixtures puede usar una ruta temporal definida por quien ejecuta la prueba. El script no inicia cron, no realiza red y no lee tokens, evidencia raw ni archivos de configuración.

## Contrato de eventos

Cada línea JSONL es un evento completo y autosuficiente. Existen dos tipos permitidos:

| `record_type` | Uso | Campos determinantes |
|---|---|---|
| `genesis` | Inicializa un archivo vacío con versión, marca y contrato. | `ledger_schema_version`, `brand`, `created_at_utc`. |
| `observation` | Registra una observación normalizada válida. | Campos del esquema multicanal, `observation_key`, `ledger_entry_key`, `transform_run_id`. |

El script no escribe eventos `update`, `delete` o `replace`. Cualquier corrección se expresa como una nueva observación con `supersedes_observation_key` apuntando a la observación anterior.

## Idempotencia y supersedencia

La identidad analítica de la métrica permanece en `observation_key`, conforme al esquema multicanal. Para que una corrección pueda existir sin reescribir el hecho anterior, el ledger define adicionalmente:

```text
ledger_entry_key = SHA-256(
  observation_key | evidence_fingerprint |
  transform_run_id | supersedes_observation_key
)
```

| Caso | Acción permitida | Resultado |
|---|---|---|
| Misma `ledger_entry_key` | Omitir. | `duplicate_skip`; no se agrega línea. |
| Misma `observation_key`, fingerprint diferente, sin supersedencia | Rechazar. | `requires_supersession`. |
| Nueva observación con `supersedes_observation_key` existente | Append. | Corrección append-only; el original permanece. |
| Supersedencia a clave inexistente o ya reemplazada | Rechazar. | No se agrega línea. |

El ledger no calcula ni reescribe `row_status = superseded` dentro de la fila histórica. Esa condición se reconstruye al leer eventos, preservando la evidencia original sin mutación.

## Validaciones y límites

El escritor aplica `NORM-01` a `NORM-12` antes de agregar una observación. Además, exige `brand = Universe Sent Me`, bloquea campos prohibidos y no permite valores financieros, rutas, URLs, captions, títulos, tokens, hashes de raw impresos ni datos de personas.

Para G-NORM-4, la entrada debe llevar `synthetic = true`. El mecanismo de inserción real no existe todavía. Cada ejecución imprime solo un resumen: conteos de eventos agregados, duplicados, rechazos y supersedencias; nunca imprime las filas del ledger.

## Pruebas obligatorias

| Prueba | Evidencia esperada |
|---|---|
| Inserción inicial | Un evento genesis y una observación sintética agregada. |
| Idempotencia | Reejecución idéntica con `duplicate_skip` y sin línea nueva. |
| Actualización in-place | No existe comando de actualización; una colisión no supersedida se rechaza. |
| Corrección | Nueva línea válida con `supersedes_observation_key`. |
| Sanitización | Entrada con campo prohibido o marca incorrecta queda rechazada. |

## Gates posteriores

G-NORM-5 solo podrá considerarse después de una revisión humana del shadow ledger sintético y, si se propone una inserción real, tras documentar un consentimiento específico para datos privados, retención, cifrado de disco, reconstrucción y rollback local. Aun en ese momento, la fuente canónica, Google Sheets y OmniRoute permanecerán fuera hasta un gate independiente.

## Referencias

[1] [Esquema determinista multicanal](2026-08-25_Esquema_Normalizacion_Determinista_Multicanal_USM.md)

[2] [Guía del piloto local de APIs oficiales](2026-08-25_Guia_Piloto_Local_API_Oficial_Metricas_USM.md)

[3] [Fuente maestra y ledgers del Growth OS](../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md)
