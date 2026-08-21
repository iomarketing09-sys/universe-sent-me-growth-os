---
title: "Propuesta de calendario — experimentos comparables seleccionados"
purpose: "Registrar la sustitución controlada de tres slots del calendario 17–30 de agosto por las variantes v3 seleccionadas y documentar su programación verificada en Facebook."
status: Active
created: 2026-08-21
updated: 2026-08-21
version: "1.2"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-16_Calendario_Operativo_17_30_Agosto.md"
  - "Operations/Research/2026-08-16_Calendario_Operativo_17_30_Agosto.csv"
  - "Operations/Production/2026-08-21_Comparable_Identity_V3_Proposals.csv"
  - "Operations/Production/2026-08-21_Control_Visual_Assets_Comparables.md"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
organization: "Operations/Research"
---

# Propuesta de calendario — experimentos comparables seleccionados

## Estado y alcance

Las variantes v3 de `FUT-MICRO-005`, `FUT-MICRO-006` y `FUT-ACID-003` fueron seleccionadas por Fernando el 2026-08-21. Esta propuesta usa el calendario 17–30 existente como base y plantea **sustituciones**, no slots adicionales ni una programación paralela.

El documento está en `Active`. Fernando aprobó los tres reemplazos y los captions el 2026-08-21. Las tres filas fueron actualizadas en `2026-08-16_Calendario_Operativo_17_30_Agosto.csv`; las programaciones anteriores fueron canceladas y las nuevas quedaron `Programado_Meta_Verificado`. `Publication_Log` fue actualizado con los IDs de Meta; Instagram, CNT y afiliados permanecen sin cambios.

## Slots candidatos propuestos

| Fecha | Hora | Brief seleccionado | Asset v3 | Slot actual a sustituir | Motivo | Confusor a registrar |
|---|---:|---|---|---|---|---|
| 2026-08-24 | 13:30 | `FUT-MICRO-005` / `HB-006` | `FUT-MICRO-005_HB-006_Microhistoria_Romantico_Absurd_3P_v3.png` | `2608048 - Universe - Inalcanzable para todos.jpeg` | Misma franja de 13:30 y contenido relacional ligero; permite probar microhistoria romántico-absurda sin crear un nuevo slot. | Tema romántico/coqueteo del slot reemplazado; separar por `Cell_ID` y registrar el reemplazo. |
| 2026-08-24 | 10:00 | `FUT-MICRO-006` / `HB-007` | `FUT-MICRO-006_HB-007_Microhistoria_Cotidiana_3P_v3.png` | `Universe - Existencial 260661.png` | Franja de 10:00, contenido de humor cotidiano/irreverente y separación de la prueba romántica del mismo día. | Personaje y tono del slot original; la microhistoria debe conservar `caption_refuerzo` y no heredar el caption anterior. |
| 2026-08-27 | 16:00 | `FUT-ACID-003` / `HB-009` | `FUT-ACID-003_HB-009_Dialogo_Acido_Situacional_v3.png` | `2608064 - Universe - Quieren hacer pendejo al que nacio asi.jpeg` | El slot original ya tiene clasificación lenguaje fuerte/ácido; es el alineamiento semántico más directo disponible en el calendario futuro. | La hora 16:00 no es la ventana nocturna preferida; registrar `Hora_Test=16:00` y no comparar directamente con casos de 19:00/22:00. |

## Decisión humana registrada

| Decisión | Responsable | Fecha | Alcance |
|---|---|---|---|
| Aprobar reemplazos, captions y ejecución de Facebook | Fernando | 2026-08-21 | Cancelar las tres programaciones anteriores y programar los tres experimentos en Facebook; Instagram, CNT, reuse y afiliados excluidos. |

## Alerta de integridad del calendario

El CSV fuente contiene algunas etiquetas de día que no coinciden con la fecha ISO, por ejemplo `2026-08-24` aparece como `Jueves` en el slot de 13:30 aunque la fecha corresponde a lunes. Las fechas ISO y la zona `America/Matamoros` fueron usadas como fuente primaria y el campo `Día` de las tres filas sustituidas fue normalizado. La comprobación se repitió en el payload de programación antes de llamar a Meta; la alerta queda como guardrail para futuras automatizaciones.

## Tratamiento operativo propuesto

Con la aprobación de Fernando ya registrada, las tres filas fueron actualizadas en el calendario maestro, las programaciones antiguas fueron canceladas y los tres posts nuevos quedaron programados y verificados en Facebook. El siguiente gate es confirmar su publicación real y extraer métricas 24/72 horas. El `Experiment_ID` será `EXP-2026-08-COMP-GAPS-01`, con `Hypothesis_ID` `HB-006`, `HB-007` y `HB-009`; se conservarán `Cell_ID`, `Caption_Treatment`, `Caption_Function`, `Narrative_Structure`, `Humor_Function`, `Character_Presence`, `Hora_Test`, `Theme_Confound` y `Reuse_Status=New_Asset_Proposed`.

Los captions deberán ser los registrados en la matriz de briefs, no los captions de los slots sustituidos. La publicación será Facebook primero, sin duplicación automática en Instagram. La programación mediante Meta Graph API quedó ejecutada bajo la autorización explícita de Fernando. La publicación será futura según los horarios registrados; no se ejecutó cross-post a Instagram ni se creó CNT o afiliado.

## Orden de aprobación y ejecución

La aprobación de fecha, hora, slot, captions y ejecución ya quedó registrada. Se validó el asset v3, caption, `Experiment_ID`, `Hypothesis_ID`, `Cell_ID`, hora local `America/Matamoros` y estado de autorización antes de llamar a Meta. Meta devolvió `is_published=false` y `scheduled_publish_time` para los tres posts.

Una vez publicados, los posts entrarán al seguimiento del experimento, pero no se mezclarán con P0, Wave 1, afiliados ni reuse. Instagram se decidirá en una fase posterior y separada.
