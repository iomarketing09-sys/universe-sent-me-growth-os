---
title: "Propuesta de calendario — experimentos comparables seleccionados"
purpose: "Proponer la sustitución controlada de tres slots futuros del calendario 17–30 de agosto por las variantes v3 seleccionadas de los experimentos comparables, sin ejecutar todavía cambios en Meta, Instagram o el calendario maestro."
status: Active
created: 2026-08-21
updated: 2026-08-21
version: "1.1"
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

El documento está en `Active`. Fernando aprobó los tres reemplazos el 2026-08-21 y las tres filas ya fueron actualizadas en `2026-08-16_Calendario_Operativo_17_30_Agosto.csv` con estado `Aprobado_Sustitucion_Pendiente_Meta`. `Publication_Log`, Meta, Instagram, CNT y afiliados todavía no fueron modificados.

## Slots candidatos propuestos

| Fecha | Hora | Brief seleccionado | Asset v3 | Slot actual a sustituir | Motivo | Confusor a registrar |
|---|---:|---|---|---|---|---|
| 2026-08-24 | 13:30 | `FUT-MICRO-005` / `HB-006` | `FUT-MICRO-005_HB-006_Microhistoria_Romantico_Absurd_3P_v3.png` | `2608048 - Universe - Inalcanzable para todos.jpeg` | Misma franja de 13:30 y contenido relacional ligero; permite probar microhistoria romántico-absurda sin crear un nuevo slot. | Tema romántico/coqueteo del slot reemplazado; separar por `Cell_ID` y registrar el reemplazo. |
| 2026-08-24 | 10:00 | `FUT-MICRO-006` / `HB-007` | `FUT-MICRO-006_HB-007_Microhistoria_Cotidiana_3P_v3.png` | `Universe - Existencial 260661.png` | Franja de 10:00, contenido de humor cotidiano/irreverente y separación de la prueba romántica del mismo día. | Personaje y tono del slot original; la microhistoria debe conservar `caption_refuerzo` y no heredar el caption anterior. |
| 2026-08-27 | 16:00 | `FUT-ACID-003` / `HB-009` | `FUT-ACID-003_HB-009_Dialogo_Acido_Situacional_v3.png` | `2608064 - Universe - Quieren hacer pendejo al que nacio asi.jpeg` | El slot original ya tiene clasificación lenguaje fuerte/ácido; es el alineamiento semántico más directo disponible en el calendario futuro. | La hora 16:00 no es la ventana nocturna preferida; registrar `Hora_Test=16:00` y no comparar directamente con casos de 19:00/22:00. |

## Decisión humana registrada

| Decisión | Responsable | Fecha | Alcance |
|---|---|---|---|
| Aprobar los tres reemplazos propuestos | Fernando | 2026-08-21 | Actualizar el calendario maestro; no autoriza todavía cancelar/programar en Meta, publicar, crear CNT, reuse, afiliados o cross-post a Instagram. |

## Alerta de integridad del calendario

El CSV fuente contiene algunas etiquetas de día que no coinciden con la fecha ISO, por ejemplo `2026-08-24` aparece como `Jueves` en el slot de 13:30 aunque la fecha corresponde a lunes. Las fechas ISO y la zona `America/Matamoros` fueron usadas como fuente primaria y el campo `Día` de las tres filas sustituidas ya fue normalizado. Antes de ejecutar Meta se debe repetir esta comprobación en el payload de programación; la alerta bloquea cualquier automatización basada únicamente en el nombre del día.

## Tratamiento operativo propuesto

Con la aprobación de Fernando ya registrada, las tres filas fueron actualizadas únicamente en el calendario maestro; el siguiente gate es validar captions y solicitar autorización operativa para cancelar/programar en Meta. El `Experiment_ID` será `EXP-2026-08-COMP-GAPS-01`, con `Hypothesis_ID` `HB-006`, `HB-007` y `HB-009`; se conservarán `Cell_ID`, `Caption_Treatment`, `Caption_Function`, `Narrative_Structure`, `Humor_Function`, `Character_Presence`, `Hora_Test`, `Theme_Confound` y `Reuse_Status=New_Asset_Proposed`.

Los captions deberán ser los registrados en la matriz de briefs, no los captions de los slots sustituidos. La publicación será Facebook primero, sin duplicación automática en Instagram. La programación mediante Meta Graph API y cualquier publicación requerirán una confirmación humana separada e inmediatamente anterior a la ejecución.

## Orden de aprobación y ejecución

Primero, Fernando debe aprobar los tres reemplazos de fecha, hora y slot. Después se actualiza el calendario maestro y se prepara el registro operativo de cada publicación. Antes de llamar a Meta, se valida que el asset v3, caption, `Experiment_ID`, `Hypothesis_ID`, `Cell_ID`, hora local `America/Matamoros` y estado de autorización coincidan. Finalmente, se solicitará una confirmación explícita para programar/publicar en Facebook.

Una vez publicados, los posts entrarán al seguimiento del experimento, pero no se mezclarán con P0, Wave 1, afiliados ni reuse. Instagram se decidirá en una fase posterior y separada.
