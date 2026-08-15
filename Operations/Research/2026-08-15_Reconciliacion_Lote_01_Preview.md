# Preview de reconciliación — lote 1

**Estado:** Review  
**Fecha:** 2026-08-15  
**Regla:** los estados normalizados ya fueron añadidos de forma reversible a `Content_Inventory.csv`; no se asigna ningún `260####` como confirmado hasta aprobar la reconciliación.

## Distribución propuesta de estados

| Campo | Distribución |
|---|---:|
| Estado operativo `Reuse_Candidate` | 2 |
| Estado operativo `Production_Pending` | 3 |
| Estado operativo `Blocked_Operational` | 1 |
| Estado operativo `Pending_Approval` | 2 |
| Estado operativo `Idea` | 17 |
| Estado operativo `Draft_Pending_Approval` | 3 |
| Estado canon `Canon_Review_Required` | 13 |
| Estado canon `Canon_Clear_or_Unverified` | 13 |
| Estado canon `Canon_Constrained` | 1 |
| Estado canon `Canon_Partial` | 1 |

## Coincidencias CNT↔260 encontradas en la misma línea

| Archivo | Línea | CNT | Referencia 260 | Contexto |
|---|---:|---|---|---|
| GrowthOS/05_02_Calendario_04_09_Agosto.md | 34 | CNT-002 | 260509 | | **9:00 PM** | FB | Foto (Meme) | Universe | `260509.png` — "Pensamientos con groserías..." *(Corrección 2026-08-04: CNT-002 ya se publicó el 30-Jul, no se produce de nuevo — este slot vuelve a meme reutilizado)* | Reuse Queue | |
| Operations/Research/2026-08-12_Revision_Cambios_GrowthOS_Claude_Fernando.md | 47 | CNT-023 | 260801 | El Episodio 2 de CNT-023 ("¿Qué me llegó?") se reconcilió con la producción final de Lámpara Luna (storyboard de 9 escenas). El Backlog, Production Queue, Approval Queue e inventario CSV quedaron actualizados con las piezas de la semana 10– |

## Resultado aplicado al inventario

Se añadieron columnas normalizadas sin borrar ni sobrescribir `estado` o `bloqueado_canon`. Hay **0 assets confirmados**, **2 candidatos ambiguos** (`CNT-002 → 260509` y `CNT-023 → 260801`) y **26 filas sin coincidencia CNT↔260 confirmada**.

## IDs CNT encontrados fuera del inventario actual

Estos IDs deben reconciliarse después; no se deben borrar ni crear filas automáticamente.

CNT-029, CNT-030
