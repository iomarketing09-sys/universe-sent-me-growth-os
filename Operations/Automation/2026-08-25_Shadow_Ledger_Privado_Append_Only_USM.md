---
title: "Shadow ledger privado append-only de observaciones normalizadas — Universe Sent Me"
purpose: "Definir el ledger privado de validación para comprobar idempotencia, supersedencia e integridad de observaciones normalizadas antes de cualquier ledger canónico o vista derivada."
status: Review
created: 2026-08-25
updated: 2026-08-26
version: "1.5"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-25_Esquema_Normalizacion_Determinista_Multicanal_USM.md"
  - "Operations/Automation/2026-08-25_Guia_Piloto_Local_API_Oficial_Metricas_USM.md"
  - "Operations/Automation/2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md"
  - "Operations/Automation/2026-08-25_Plan_Decision_Cifrado_Local_G-NORM-4R.md"
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
| Integridad de lectura | JSONL malformado, ausencia de genesis o supersedencia incoherente se reportan sin reescribir el archivo. |

## Gates posteriores

G-NORM-5 solo podrá considerarse después de una revisión humana del shadow ledger sintético y, si se propone una inserción real, tras documentar y revisar G-SEC-2: privacidad/minimización, retención/disposición, operación estrictamente read-only y consentimiento granular. Aun en ese momento, la fuente canónica, Google Sheets y OmniRoute permanecerán fuera hasta un gate independiente.

## Demostración local confirmada

La batería `validate_shadow_ledger_synthetic.py` se ejecutó en Xubuntu el 25 de agosto de 2026 y devolvió `shadow_ledger_synthetic_validation_passed`. Confirmó las cuatro pruebas contractuales: inserción inicial, repetición idempotente, rechazo de una colisión que intentaba modificar un evento existente y corrección por supersedencia append-only. Las garantías reportadas fueron `synthetic_only`, `private_temp_ledger`, `no_network` y `no_canonical_write`.

Esta demostración no creó el ledger persistente bajo `~/.local/share/usm-metrics/shadow-ledger/`; usó una ruta temporal eliminada al terminar. La inserción de cualquier observación real, incluso privada, sigue bloqueada hasta una aprobación separada.

## Simulación de corrupción sintética confirmada

La suite `validate_shadow_ledger_corruption_synthetic.py` generó tres fallas controladas dentro de un directorio temporal: una línea JSONL truncada, una secuencia que comienza con observación sin evento `genesis` y una supersedencia que apunta a una clave inexistente. El inspector `inspect_shadow_ledger_synthetic.py` detectó respectivamente `jsonl_invalid`, `genesis_missing_or_not_first` y `supersession_target_missing`.

Antes y después de cada inspección, la suite comparó los bytes completos del archivo temporal. La igualdad byte a byte confirmó que el inspector no agregó, eliminó, ordenó ni reparó ningún evento. La ejecución devolvió `shadow_ledger_corruption_synthetic_validation_passed` con sockets bloqueados, sin red, sin ledgers canónicos y sin datos reales. Este control detecta, pero no recupera ni normaliza, archivos inconsistentes.

### Validación semántica sobre JSONL formalmente válido

La misma suite amplió la cobertura con cuatro archivos JSONL sintéticos que se pueden leer como JSON, pero incumplen el contrato interno: `genesis` con marca incorrecta, tipo de evento desconocido, dos observaciones con la misma `observation_key` sin supersedencia y `ledger_entry_key` alterado. El inspector reportó respectivamente `genesis_contract_invalid`, `record_type_invalid`, `observation_key_collision` y `entry_key_invalid`.

Cada caso volvió a confirmar invariancia byte a byte durante la inspección. El resultado no elige una fila “correcta”, no recalcula llaves, no corrige el contrato ni añade eventos de reparación. La cobertura permanece exclusivamente sintética, temporal y sin efectos fuera del directorio de prueba.

## Revisión estructurada del contrato `Review`

La revisión humana de la matriz confirmó que las pruebas iniciales cubrían estructura JSONL, `genesis`, supersedencia, tipos de evento, colisiones de `observation_key` y coherencia de `ledger_entry_key`, pero dejaban dos controles de lectura implícitos. Se añadieron y validaron las siguientes reglas:

| Regla añadida | Detección | Propósito |
|---|---|---|
| Una observación ya escrita debe seguir cumpliendo NORM-01 a NORM-12 al leerse. | `observation_norm_invalid` | Detectar corrupción o deriva semántica de una fila persistida, sin corregirla. |
| Una `ledger_entry_key` solo puede aparecer una vez. | `ledger_entry_key_duplicate` | Detectar repetición exacta de un evento, incluso si también hay colisión de observación. |

La matriz ahora ejecuta diez controles: nueve detecciones y la invariancia byte a byte. La regresión integrada de normalizador y shadow ledger siguió pasando. El dictamen es **suficiencia limitada para el contrato sintético actual**: el estado permanece `Review`; G-NORM-4R, cualquier inserción real, ledger persistente, Google Sheets, Drive, GitHub como ledger y OmniRoute continúan bloqueados. Estas pruebas no sustituyen el requisito independiente de almacenamiento local cifrado y consentimiento granular.

## Dependencia G-SEC-2 diseñada

El documento `2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md` v2.0 define G-SEC-2 como el conjunto de controles previos al piloto real. Establece cuatro subgates independientes: minimización de datos y salidas, retención máxima de 30 días con revisión humana, operación local estrictamente read-only y una tarjeta de consentimiento por operación con vigencia de 24 horas.

El diseño no modifica este contrato ni habilita su escritor real. Antes de cualquier G-NORM-4R, los cuatro subgates deben pasar revisión humana y una prueba sintética específica de las barreras read-only. No se abrirán tokens, evidencia, collectors, API, cron, Docker, OmniRoute, Sheets, Drive, GitHub ni modelos como consecuencia de esta dependencia.

## Referencias

[1] [Esquema determinista multicanal](2026-08-25_Esquema_Normalizacion_Determinista_Multicanal_USM.md)

[2] [Guía del piloto local de APIs oficiales](2026-08-25_Guia_Piloto_Local_API_Oficial_Metricas_USM.md)

[3] [Fuente maestra y ledgers del Growth OS](../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md)
