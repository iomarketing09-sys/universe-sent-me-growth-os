---
title: "Hallazgos visuales — cola prioritaria de reconciliación de junio"
purpose: "Conservar la revisión visual de los tres casos de mayor valor aún sin Asset_Ref y decidir cuáles pueden integrarse sin búsquedas masivas."
status: Active
created: 2026-08-21
updated: 2026-08-21
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv"
  - "Operations/Research/2026-08-21_Junio_Priority_Queue_Visual_Matches.csv"
  - "Operations/Research/2026-08-18_Drive_Assets_Junio_Listing.json"
  - "Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv"
organization: "Operations/Research"
---

# Hallazgos visuales — cola prioritaria de reconciliación de junio

## Método

Se eligieron los tres primeros casos de `Needs_Asset_Match` por prioridad de la cola de junio. Se recuperó una imagen de Meta por publicación y se comparó contra 161 miniaturas disponibles del inventario de Drive de junio. La similitud perceptual se utilizó como shortlist; la confirmación se hizo con el contact sheet visual.

## Resultado

| Prioridad | Meta_ID | Interacciones | Shares | Resultado visual | Decisión |
|---:|---|---:|---:|---|---|
| 24 | `1036844829507460_122134147251072582` | 171 | 50 | La imagen de Meta dice “A pesar de mi dislexia…”; el candidato Drive `2607818` muestra otro texto y otra composición | Mantener `Needs_Asset_Match` |
| 25 | `1036844829507460_122130196011072582` | 164 | 42 | La imagen de Meta muestra “La flojera que me da ligar”; el candidato Drive `2607782` no coincide visualmente | Mantener `Needs_Asset_Match` |
| 26 | `1036844829507460_122129404893072582` | 155 | 19 | La composición de tres paneles de Meta coincide con `Universe - Existencial 260746.png` en Drive | Promover a `Visual_Confirmed`; `Asset_Ref=260746` |

El caso `122129404893072582` es `MICRO-001`, la microhistoria estricta de tres paneles. La confirmación fortalece la evidencia de la celda narrativa, pero no crea un CNT nuevo de forma automática. El `Meta_ID` permanece como clave de publicación y el `Drive_ID` se registra como evidencia del asset.

La revisión no resuelve los otros 57 casos de junio sin match. Estos tienen un máximo de 171 interacciones y un total combinado de 936 interacciones, por lo que una búsqueda masiva no tiene prioridad analítica. Deben permanecer como reserva y reabrirse únicamente si una pregunta concreta de celdas, personaje, formato o reuse los convierte en evidencia necesaria.

## Limitaciones

Los candidatos descartados solo quedan descartados frente a los dos archivos sugeridos por similitud; no se afirma que el asset correcto no exista en Drive. El resultado no modifica el canon, el calendario ni la operación de publicación. Tampoco reconstruye ventanas de 24/72 horas.

## Evidencia

- `2026-08-21_Junio_Priority_Queue_Visual_Matches.csv`: shortlist reproducible.
- `2026-08-21_Junio_Priority_Queue_Visual_Contact_Sheet.jpg`: comparación Meta/Drive.
- `2026-08-17_Cola_Reconciliacion_Assets_Junio.csv`: cola de 230 publicaciones y estados previos.
