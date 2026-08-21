---
title: "Impacto de reclasificaciones de captions — Ganso y Universe"
purpose: "Medir cuánto cambia la lectura agregada de engagement al mover Ganso a caption_minimo y confirmar Universe como caption_refuerzo, sin alterar métricas post-level."
status: Active
created: 2026-08-21
updated: 2026-08-21
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Audit.csv"
  - "Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Manual_Findings.md"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
organization: "Operations/Research"
---

# Impacto de las reclasificaciones

La reclasificación modifica únicamente la pertenencia descriptiva a un grupo de caption. No modifica interacciones, shares, comentarios, fecha, post, contenido ni el ExperimentLog.

## Cambio de asignaciones

| Caso | Antes de revisión | Después de revisión | Interacciones | Shares | Comentarios |
|---|---|---|---:|---:|---:|
| `1036844829507460_122134608507072582` (Ganso visual candidate) | `caption_refuerzo` | `caption_minimo` | 14 | 2 | 3 |
| `1036844829507460_122134055109072582` (Unidentified magical woman) | `caption_conversacional` | `caption_refuerzo` | 9 | 0 | 1 |
| `1036844829507460_122130324285072582` (Universe visual candidate) | `caption_conversacional` | `caption_refuerzo` | 7 | 0 | 0 |
| `1036844829507460_122133424479072582` (Silvio visual candidate) | `caption_conversacional` | `caption_refuerzo` | 5 | 1 | 0 |
| `1036844829507460_122130032151072582` (Wilfred visual candidate) | `caption_conversacional` | `caption_refuerzo` | 4 | 0 | 0 |
| `1036844829507460_122130196011072582` (Universe) | `caption_refuerzo` | `caption_refuerzo` confirmado | 164 | 42 | 2 |

## Comparación agregada antes/después

| Tratamiento | n antes | Interacciones antes | Shares antes | Comentarios antes | n después | Interacciones después | Shares después | Comentarios después |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `caption_conversacional` | 6 | 49 | 2 | 2 | 2 | 24 | 1 | 1 |
| `caption_minimo` | 7 | 65 | 5 | 6 | 8 | 79 | 7 | 9 |
| `caption_refuerzo` | 3 | 184 | 46 | 5 | 6 | 195 | 45 | 3 |
| `historical_unavailable` | 1 | 2 | 0 | 0 | 1 | 2 | 0 | 0 |

El total del subconjunto permanece en **300 interacciones, 53 shares y 13 comentarios**. El efecto directo solicitado es la transferencia de Ganso: 14 interacciones, 2 shares y 3 comentarios salen de `caption_refuerzo` y entran a `caption_minimo`. Universe no se mueve y sigue aportando 164 interacciones y 42 shares al grupo de refuerzo. La revisión completa también movió cuatro captions conversacionales a refuerzo; esos cambios deben analizarse por separado del efecto Ganso/Universe.

La mediana de `caption_refuerzo` cambia de 7 a 6.5 interacciones después de la revisión completa porque cuatro casos conversacionales entran al grupo y Ganso sale; el grupo final conserva el outlier de Universe. La diferencia es composicional y no significa que `caption_refuerzo` haya mejorado ni que `caption_minimo` haya empeorado.

## Decisión de uso

La reclasificación de Ganso debe conservarse como corrección taxonómica descriptiva. La confirmación de Universe debe conservarse como revisión manual del tratamiento, pero ninguno de los dos cambios autoriza una conclusión causal ni una actualización del ExperimentLog. La comparación de tratamientos permanece descriptiva porque el subconjunto no está balanceado por celda; la revisión manual completa no crea evidencia causal.
