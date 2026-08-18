---
title: "Corte P0 de las cinco publicaciones del 17 de agosto"
purpose: "Registrar la ejecución del extractor P0 sobre las cinco publicaciones confirmadas en Meta y documentar por qué aún no se escribieron métricas 24/72 horas."
status: "Active"
created: 2026-08-19
updated: 2026-08-19
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-17_P0_Baseline_Ola_Activa.csv"
  - "Operations/Research/2026-08-15_ExperimentLog.csv"
  - "Operations/Production/extract_metrics_24_72.py"
  - "Operations/Production/run_p0_baseline_cut.py"
  - "Operations/Production/extract_metrics_24_72_playbook.md"
organization: "Operations/Research"
---

# Resultado del corte P0

## Ejecución

El proceso se ejecutó el **18 de agosto de 2026 a las 03:26:12 UTC**, equivalente a **17 de agosto de 2026 a las 22:26:12 en America/Matamoros**. Se procesó explícitamente el baseline `EXP-2026-08-CAL-01` con sus cinco publicaciones confirmadas en Meta:

| Slot local | Asset | Meta Post ID | Edad aproximada al corte |
|---|---|---|---:|
| 10:00 | `260633` | `122151373701072582` | 12.4 h |
| 11:00 | `2608028` | `122151373761072582` | 11.4 h |
| 13:30 | `2608034- Elara` | `122151373833072582` | 9.0 h |
| 16:00 | `260642` | `122151373893072582` | 6.4 h |
| 17:00 | `2608027.jpeg` | `122151373953072582` | 5.4 h |

## Resultado técnico

| Campo | Resultado |
|---|---:|
| Filas candidatas | 5 |
| Ventanas 24h elegibles | 0 |
| Ventanas 72h elegibles | 0 |
| Escrituras exactas de métricas | 0 |
| Actualización del baseline | No requerida |
| Actualización del ExperimentLog | No requerida |
| Instagram tocado | No |
| Contenido publicado | No |

La ejecución no escribió métricas porque ninguna publicación había alcanzado todavía 24 horas desde su hora real de publicación. Esto es correcto y protege la comparabilidad del experimento. El corte no debe forzarse con `--now` artificial ni con timestamps planeados.

El extractor existente, si se ejecuta directamente sobre `Publication_Log.csv`, identifica principalmente las filas del lote 15–16 porque las cinco publicaciones del 17 de agosto están formalmente en el baseline P0 y todavía no tienen fecha real en el Publication Log. Para evitar procesar el lote equivocado, se creó el adaptador `run_p0_baseline_cut.py`, que apunta explícitamente al baseline de cinco filas y actualiza el ExperimentLog solo cuando una ventana está realmente vencida.

## Integridad de datos

Las cinco filas del baseline permanecen en `Pendiente_ventana`. `interactions_24h`, `comments_root_24h`, `shares_24h`, `interactions_72h`, `comments_root_72h`, `shares_72h` e `interactions_72h` siguen vacías. El ExperimentLog conserva sus valores vacíos y no recibió totales lifetime como sustitutos.

La evidencia JSON completa se conserva en `2026-08-19_P0_Corte_17_Agosto.json`. El siguiente corte válido será cuando al menos una de las cinco publicaciones haya superado 24 horas; el proceso deberá consultar Meta en modo lectura y, si la API vuelve a entregar únicamente acumulados lifetime, registrar la limitación sin llenar los campos estrictos de 24/72h.
