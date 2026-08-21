---
title: "Preflight de briefs comparables aprobados"
purpose: "Validar reproduciblemente las especificaciones de los cuatro briefs aprobados para preflight y registrar los bloqueos antes de generación, calendario, publicación o CNT."
status: Active
created: 2026-08-21
updated: 2026-08-21
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md"
  - "Operations/Research/2026-08-21_Paquete_Revision_Humana_Briefs_Comparables.md"
  - "Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
organization: "Operations/Production"
---

# Preflight de briefs comparables aprobados

## Resultado ejecutivo

Los cuatro briefs pasan la validación de especificación y metadatos propuestos: `4/4` con `spec_status=PASS`. Esta salida confirma coherencia entre la matriz de aprobación, el diseño técnico y los campos previos a generación; **no confirma que exista un asset**, no genera imágenes y no autoriza calendario, publicación, reuse ni creación de CNT.

> La aprobación de Fernando es `Approve_Preflight_Only`. Cualquier paso que produzca un asset o lo acerque a publicación requiere una decisión humana separada.

## Matriz de preflight

| Brief_ID | Cell_ID | Experiment_ID | Hypothesis_ID | Caption_Treatment | Caption_Function | Humor_Function | Hora_Test | Theme_Confound | Reuse_Status | Especificación | Asset | Metadatos | Generación | Promoción |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `FUT-MICRO-005` | `MICRO-STRICT-3P` | `EXP-2026-08-COMP-GAPS-01` | `H-COMP-MICRO3P-005` | `caption_minimo` | `reaccion` | `romantic_absurd_reframe` | `18:00 (America/Matamoros)` | `romantic_context; character_novelty; panel_count; caption_treatment` | `New_Asset_Proposed` | `PASS` | PENDING — no asset generated | PASS — complete proposal | `Pending_Human_Approval` | BLOCKED — requires separate human approval |
| `FUT-MICRO-006` | `MICRO-STRICT-3P` | `EXP-2026-08-COMP-GAPS-01` | `H-COMP-MICRO3P-006` | `caption_refuerzo` | `refuerzo_semantico` | `everyday_social_reframe` | `20:00 (America/Matamoros)` | `everyday_social_context; relational_or_anxiety_risk; panel_count; caption_treatment` | `New_Asset_Proposed` | `PASS` | PENDING — no asset generated | PASS — complete proposal | `Pending_Human_Approval` | BLOCKED — requires separate human approval |
| `FUT-TRANS-003` | `TRANS-UNIVERSE` | `EXP-2026-08-COMP-GAPS-01` | `H-COMP-TRANS-003` | `caption_conversacional` | `pregunta_abierta` | `visual_identity_contrast` | `16:00 (America/Matamoros)` | `transformation_type; identity_legibility; background_dominance; caption_treatment` | `New_Asset_Proposed` | `PASS` | PENDING — no asset generated | PASS — complete proposal | `Pending_Human_Approval` | BLOCKED — requires separate human approval |
| `FUT-ACID-003` | `ACID-DIALOGUE` | `EXP-2026-08-COMP-GAPS-01` | `H-COMP-ACID-003` | `caption_minimo` | `reaccion` | `interpersonal_contradiction` | `22:00 (America/Matamoros)` | `acid_target; voice_clarity; relationship_context; caption_treatment` | `New_Asset_Proposed` | `PASS` | PENDING — no asset generated | PASS — complete proposal | `Pending_Human_Approval` | BLOCKED — requires separate human approval |

## Campos obligatorios antes de generar cualquier asset

Cada brief ya contiene una propuesta para los siguientes campos. Los valores son de diseño previo y deben revisarse antes de cualquier solicitud de generación; no constituyen autorización. La hora es una hora de prueba propuesta en `America/Matamoros`, no un slot reservado:

| Campo | Regla | Estado en este preflight |
|---|---|---|
| `Experiment_ID` | Propuesta completada; revisar antes de generación. | `PROPOSED_COMPLETE_NOT_AUTHORIZED` |
| `Hypothesis_ID` | Propuesta completada; revisar antes de generación. | `PROPOSED_COMPLETE_NOT_AUTHORIZED` |
| `Cell_ID` | Propuesta completada; revisar antes de generación. | `PROPOSED_COMPLETE_NOT_AUTHORIZED` |
| `Caption_Treatment` | Propuesta completada; revisar antes de generación. | `PROPOSED_COMPLETE_NOT_AUTHORIZED` |
| `Caption_Function` | Separado de Caption_Treatment; no asumir que una pregunta retórica es conversacional. | `PROPOSED_COMPLETE_NOT_AUTHORIZED` |
| `Narrative_Structure` | Propuesta completada; revisar antes de generación. | `PROPOSED_COMPLETE_NOT_AUTHORIZED` |
| `Humor_Function` | Propuesta completada; revisar antes de generación. | `PROPOSED_COMPLETE_NOT_AUTHORIZED` |
| `Character_Presence` | Propuesta completada; revisar antes de generación. | `PROPOSED_COMPLETE_NOT_AUTHORIZED` |
| `Hora_Test` | Propuesta completada; revisar antes de generación. | `PROPOSED_COMPLETE_NOT_AUTHORIZED` |
| `Theme_Confound` | Propuesta completada; revisar antes de generación. | `PROPOSED_COMPLETE_NOT_AUTHORIZED` |
| `Reuse_Status` | Debe registrar `New_Asset_Proposed`; no mezclar con reuse. | `PROPOSED_COMPLETE_NOT_AUTHORIZED` |

## Salvaguardas específicas

**FUT-MICRO-005 y FUT-MICRO-006.** La pieza debe tener exactamente tres paneles inequívocos, turnos legibles y remate autosuficiente. No se acepta el candidato histórico de cuatro paneles `1036844829507460_122127951885072582` dentro de `MICRO-STRICT-3P`.

**FUT-TRANS-003.** No se puede promover la pieza sin verificar visualmente al mismo Universe en ambos estados, gafas visibles en ambos estados y marcadores de identidad preservados. Un cambio de ropa aislado o la sustitución por otro personaje no cumple.

**FUT-ACID-003.** El objetivo ácido debe ser una situación, hábito o contradicción; las voces deben distinguirse en una lectura; `Safety_Flag` debe confirmar ausencia de coerción y de ataques a rasgos protegidos.

## Condiciones de promoción

El resultado de este documento es `preflight_specification_pass` con metadatos propuestos completos, no `generation_approved`. Antes de cualquier generación se necesita revisar estos valores y obtener aprobación humana explícita para producir assets. Antes de calendario, publicación o CNT se necesita una aprobación posterior e independiente.

## Reproducibilidad

Este reporte fue generado por `Operations/Production/run_comparable_briefs_preflight.py` a partir de la matriz CSV y de los criterios del diseño técnico. Los metadatos fueron completados por `Operations/Production/populate_comparable_brief_metadata.py`. No se consultaron APIs, no se modificó Facebook o Instagram y no se usó navegación externa.

## Referencias

[1]: `Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md` — criterios técnicos y estado de celdas.
[2]: `Operations/Research/2026-08-21_Paquete_Revision_Humana_Briefs_Comparables.md` — alcance de la aprobación humana.
[3]: `Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv` — matriz reproducible de decisiones y metadatos propuestos.
[4]: `Operations/Production/populate_comparable_brief_metadata.py` — llenado reproducible de los valores propuestos.
[5]: `GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md` — reglas de evidencia y captions.
