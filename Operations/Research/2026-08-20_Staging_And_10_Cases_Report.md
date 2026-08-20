---
title: "Staging de aliases y opciones para los diez casos sin evidencia inicial"
purpose: "Preservar aliases visualmente verificados sin modificar Content_Inventory y proponer rutas de resolución para los diez casos que no aparecieron en la carpeta principal."
status: Active
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-20_17_30_Alias_Evidence_Enriched.csv"
  - "Operations/Research/2026-08-20_Inventory_Alias_Staging_17_30.csv"
  - "Operations/Research/2026-08-20_10_Cases_Resolution_Options.csv"
  - "GrowthOS/Content_Inventory.csv"
organization: "Operations/Research"
---

# Staging de aliases 17–30 y opciones de resolución

## Capa staging

Se crearon 33 filas staging para assets con identidad visual verificada en la carpeta principal. La capa conserva Alias ID, publicación, Meta Post ID, permalink, fecha/hora, ruta de evidencia y SHA-256. No asigna CNT, no modifica `Content_Inventory.csv` y no tiene impacto de canon.

| Campo de control | Resultado |
|---|---:|
| Assets staging | 33 |
| CNT creados | 0 |
| Inventario maestro modificado | No |
| Impacto de canon | Ninguno |

## Diez casos inicialmente sin evidencia local

La búsqueda inicial estaba limitada a `calendar_visual_review_20260816`. Una segunda búsqueda en carpetas locales amplió la evidencia: se localizaron archivos para los diez casos. Nueve tienen un asset local único; `260508` tiene dos variantes locales y dos candidatos de inventario.

| Estado posterior a la búsqueda amplia | Cantidad |
|---|---:|
| Evidencia local amplia + filename exacto a inventario | 2 filas/casos relacionados |
| Evidencia local amplia sin fila de inventario | 8 |
| Sin evidencia en ninguna ruta revisada | 0 |

### Opciones recomendadas

**Opción 1 — `260508`: resolver por filename exacto.** Validar `260508_universe.jpg` contra `CNT-042` y `260508_existencial.png` contra `CNT-043`; después actualizar únicamente los aliases `ALIAS-0036` y `ALIAS-0047`. No crear CNT.

**Opción 2 — Los otros ocho assets con archivo local único:** mantenerlos en una segunda capa staging de evidencia, con SHA-256, y crear posteriormente una fila de alias no-CNT o una fila de inventario aprobada. No se debe elegir un CNT por personaje o por parecido visual.

**Opción 3 — Si un archivo local no coincide con la publicación:** solicitar evidencia de Drive/Meta o una captura de la publicación. La ausencia de match no debe resolverse con una inferencia de filename.
