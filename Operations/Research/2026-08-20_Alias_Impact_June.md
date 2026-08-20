---
title: "Impacto de aliases actualizados en métricas de crecimiento de junio"
purpose: "Medir qué cambia en los agregados y qué cambia únicamente en la atribución editorial de inventario."
status: Active
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-20_Historical_Performance_Individuals_Consolidated.csv"
  - "Operations/Research/2026-08-20_Source_Alias_Table.csv"
  - "Operations/Research/2026-08-20_NonCNT_Inventory_Alias_Approval.csv"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
organization: "Operations/Research"
---

# Impacto de aliases actualizados en junio

## Resultado ejecutivo

La reconciliación no añade interacciones ni cambia los Meta IDs. Su efecto cuantitativo directo es **cero** sobre las métricas de las publicaciones. El efecto principal es de atribución: dos publicaciones con `Asset_Ref=260508` dejan de apuntar ambiguamente a `CNT-042;CNT-043` y pasan a una asignación exacta: la variante `260508 - Universe.jpg` a `CNT-042` y `Universe - Existencial 260508.png` a `CNT-043`.

## Control de agregados

| Medida | Filas fuente | Vista consolidada | Diferencia por duplicados |
|---|---:|---:|---:|
| Filas totales individuales | 211 | 206 | 5 |
| Filas de junio | 177 | 172 | 5 |
| Interacciones de junio | 22657 | 17334 | 5323 |
| Reacciones de junio | 17210 | 13198 | 4012 |
| Comentarios de junio | 425 | 384 | 41 |
| Shares de junio | 5022 | 3752 | 1270 |

La diferencia entre la fuente y la vista consolidada es un efecto de duplicación, no un efecto de los aliases. Los aliases solo hacen que la atribución a inventario sea más precisa.

## Impacto de 260508

| Publicación lógica | Interacciones | Atribución anterior | Atribución actual |
|---|---:|---|---|
| `1036844829507460_122117393139072582` — 260508 - Universe.jpg | 9 | `CNT-042;CNT-043` | `CNT-042` |
| `1036844829507460_122117731467072582` — Universe - Existencial 260508.png | 8 | `CNT-042;CNT-043` | `CNT-043` |

Las dos publicaciones suman 17 interacciones. Ese total no cambia; lo que cambia es que ahora cada fila puede entrar en análisis por CNT sin duplicar o repartir el rendimiento entre dos candidatos.

## Impacto en Growth OS

La cobertura de aliases Facebook 17–30 queda distribuida así: {'High': 33, 'Review': 41}. Los ocho aliases no-CNT aprobados administrativamente pertenecen a publicaciones de la programación 17–30 y mejoran la trazabilidad futura, pero no agregan métricas históricas de junio. Los cinco assets P0 mantienen dos asociaciones de alta confianza y tres excepciones documentadas.

La conclusión operativa es que la reconciliación **no reescribe el rendimiento de junio**; mejora la capacidad de responder qué asset/CNT produjo cada resultado y evita atribuciones ambiguas en reuse y rankings futuros. Los agregados deben continuar calculándose sobre la vista consolidada, no sobre las filas fuente duplicadas.
