---
title: "Ajuste de experimentos sobre el calendario existente 17–30 de agosto"
purpose: "Integrar la primera ola experimental de cinco familias dentro de la programación ya existente, usando un overlay reversible y sin mover slots ni reemplazar el calendario operativo."
status: Review
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-16_Calendario_Operativo_17_30_Agosto.csv"
  - "Operations/Research/2026-08-20_Overlay_Wave1_Calendario_17_30.csv"
  - "Operations/Research/2026-08-20_Overlay_Wave1_Visual_Findings.md"
  - "Operations/Research/2026-08-20_Overlay_Wave1_Contact_Sheet.jpg"
  - "Operations/Research/2026-08-20_Overlay_Wave1_Review_Summary.json"
  - "Operations/Research/2026-08-20_Auditoria_Alineacion_Calendario_17_30_Familias.json"
  - "Operations/Production/2026-08-20_Plan_Experimentos_Agosto_5_Familias.md"
  - "Operations/Production/2026-08-20_Wave1_Signal_Experiment_Design.csv"
  - "Operations/Research/2026-08-20_Cohorte_17_30_Actual_Cut.md"
  - "Operations/Research/2026-08-19_P0_Corte_17_Agosto.md"
  - "Operations/Research/Affiliate_Link_Ledger.csv"
organization: "Operations/Research"
---

# Ajuste de experimentos sobre el calendario existente 17–30 de agosto

## Decisión de arquitectura

No se debe crear una programación paralela. El calendario operativo existente contiene **74 slots**: 35 de contenido nuevo, 36 de `Reuse_Top` y 3 de `Reuse_Reserve`. La recomendación es mantener ese calendario como fuente de programación y añadir una **capa overlay reversible** con `Overlay_ID`, familia, treatment de caption, métrica primaria y estado de aprobación.

El overlay no reemplaza `Experiment_ID=EXP-2026-08-CAL-01`, no cambia fechas, no mueve horas y no autoriza publicación. Su función es describir qué slots existentes pueden responder una pregunta experimental.

## Qué queda fuera

Los 39 slots de reuse —36 `Reuse_Top` y 3 `Reuse_Reserve`— permanecen fuera de `Wave_1_Signal`. Tienen una función distinta: medir el comportamiento de contenido histórico y, en algunos casos, dar seguimiento a afiliados. Mezclarlos con piezas nuevas impediría saber si la señal proviene de la familia o del reconocimiento previo del asset.

También queda fuera el baseline P0 del 17 de agosto. La cohorte actual ya registra 14 publicaciones reales visibles hasta el 19 de agosto, con 13 publicaciones de imagen interpretables y 731 interacciones acumuladas fuera de P0. El outlier `2608029` ya concentra 45.8% de esa cohorte; no debe utilizarse como control de una nueva ola.

## Overlay propuesto

Se seleccionaron **15 slots `Nueva` futuros**, sin crear filas nuevas en el calendario. Después de la revisión visual, la clasificación final no conserva exactamente tres casos por familia porque se corrigieron errores de categoría y se aplicaron holds editoriales. Todos permanecen con `P0_Eligible=No`, `Affiliate_Attachment=No`, `Reuse_Status=New_Test` y `Approval_Status=Pending` hasta revisión humana.

| Familia | Slots overlay | Treatments | Métrica primaria |
|---|---:|---|---|
| `FAM-01 Difusión_Minimal` | 3 | Mínimo, refuerzo, conversacional | Shares |
| `FAM-02 Relatable_Social` | 3 | Mínimo, refuerzo, conversacional | Shares |
| `FAM-03 Conversación_Relacional` | 3 | Mínimo, refuerzo, conversacional | Comentarios raíz y replies |
| `FAM-04 Ácido_Interpersonal` | 3 | Mínimo, refuerzo, conversacional | Shares y comentarios |
| `FAM-05 Personaje_Marcador` | 3 | Mínimo, refuerzo, conversacional | Shares |

### Resultado del corte visual

| Estado del overlay | Cantidad | Lectura |
|---|---:|---|
| `Reviewed_Eligible` | 9 | Puede entrar a la primera ola si se aprueba el tono |
| `Candidate_Review` | 4 | La familia provisional no coincide completamente con la función visual |
| `Editorial_Hold` | 2 | Requiere decisión explícita por coerción/sexualidad dominante |
| Total | 15 | La matriz conserva todos los casos para trazabilidad |

La matriz detallada conserva los 15 `Overlay_ID`. `2608053` y `2608059` quedaron en `Editorial_Hold` y Fernando aprobó mantenerlos fuera de Wave 1. `2608054`, `2608049`, `2608045` y `2608065` requieren revisión de subcelda porque son escenas textuales, monólogos, romance o humor observacional, no ejemplos puros de la familia inicialmente asignada. `2608035` quedó elegible, pero se reasignó de `Difusión_Minimal` a `Relatable_Social` por su función visual de estrés cotidiano. El corte visual completo está en `Operations/Research/2026-08-20_Overlay_Wave1_Visual_Findings.md`.

Los 15 casos seleccionados están en `Operations/Research/2026-08-20_Overlay_Wave1_Calendario_17_30.csv`. La selección ya tiene un corte visual inicial documentado, pero sigue en Review para aprobación humana. `Overlay_Eligibility=Eligible` identifica nueve casos; cuatro quedan como `Candidate_Review` y dos como `Hold`. La validación reproducible está en `Operations/Research/2026-08-20_Overlay_Wave1_Review_Summary.json` y devuelve `validation=PASS`.

## Por qué no se mueven las horas

El calendario actual no está distribuido principalmente en 18:00–22:00; utiliza 10:00, 11:00, 13:30, 16:00, 17:00 y 19:00, con algunos slots de 22:00. Mover ahora 15 publicaciones para perseguir el corredor histórico introduciría un nuevo cambio de calendario y confundiría la lectura con la ola ya aprobada.

En esta primera integración, la hora real queda como **covariable observada**. La familia y el treatment se superponen sobre slots existentes. Si una familia muestra una señal preliminar, la segunda ola podrá probar la misma familia en 18:00–22:00 frente a un control de 14:00–16:00.

## Qué debe cambiar después de aprobación

La aprobación de Fernando sobre los dos holds no implica publicar inmediatamente. Solo confirma que `2608053` y `2608059` quedan fuera del cálculo de Wave 1. Los nueve casos `Eligible` están disponibles como candidatos operativos en `Operations/Research/2026-08-20_Wave1_Eligible_Operational_Subset.csv`, pero conservan `Approval_Status=Pending` para cualquier decisión posterior de caption o publicación. Los cuatro `Candidate_Review` también permanecen fuera del cálculo principal.

Después de la aprobación editorial de cada asset, Fernando decide si se conserva el caption actual del calendario o se adopta el treatment propuesto. Cualquier cambio de caption debe documentarse antes de la programación y no debe modificar retrospectivamente posts ya publicados.

## Criterios de lectura

El overlay se considera una señal preliminar solo cuando una familia tiene tres casos comparables y al menos dos muestran la misma dirección frente al control comparable. Para una decisión operativa se requieren al menos cinco casos, dos días, dos franjas y revisión de outliers.

Los resultados de reuse, afiliados, P0 y Reels se reportan en sus ledgers separados. Ninguna conversión afiliada, alcance de Reel o interacción de P0 se incorpora al agregado del overlay editorial.

## Recomendación

La mejor adaptación es **overlay, no reprogramación**. Se conserva el calendario del 17–30, se excluyen reuse y P0, se etiquetan 15 piezas nuevas futuras y se deja el resto de las piezas nuevas como contenido operativo no experimental. Así se obtiene aprendizaje sin sacrificar la programación que Fernando ya aprobó.

Este documento y la matriz overlay están en `Review`. Se requiere aprobación humana antes de modificar captions, asignar treatments definitivos o alterar cualquier registro de programación.

## Referencias

[1]: `Operations/Research/2026-08-16_Calendario_Operativo_17_30_Agosto.csv` — calendario operativo fuente.
[2]: `Operations/Research/2026-08-20_Auditoria_Alineacion_Calendario_17_30_Familias.json` — auditoría reproducible de slots y tipos.
[3]: `Operations/Research/2026-08-20_Cohorte_17_30_Actual_Cut.md` — estado real de publicaciones hasta el 19 de agosto.
[4]: `Operations/Research/2026-08-20_Overlay_Wave1_Calendario_17_30.csv` — propuesta de overlay de 15 slots.
[5]: `Operations/Production/2026-08-20_Plan_Experimentos_Agosto_5_Familias.md` — arquitectura general de Wave 1 y Wave 2.
