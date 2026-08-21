---
title: "Preflight de briefs comparables aprobados"
purpose: "Validar reproduciblemente las especificaciones de los cuatro briefs aprobados para preflight y registrar los bloqueos antes de generación, calendario, publicación o CNT."
status: Active
created: 2026-08-21
updated: 2026-08-21
version: "1.0"
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

Los cuatro briefs pasan la validación de especificación: `4/4` con `spec_status=PASS`. Esta salida confirma coherencia entre la matriz de aprobación y el diseño técnico; **no confirma que exista un asset**, no genera imágenes y no autoriza calendario, publicación, reuse ni creación de CNT.

> La aprobación de Fernando es `Approve_Preflight_Only`. Cualquier paso que produzca un asset o lo acerque a publicación requiere una decisión humana separada.

## Matriz de preflight

| Brief_ID | Cell_ID | Caption_Treatment | Especificación | Asset | Metadatos | Promoción |
|---|---|---|---|---|---|---|
| `FUT-MICRO-005` | `MICRO-STRICT-3P` | `caption_minimo` | `PASS` | PENDING — no asset generated | PENDING — required before generation | BLOCKED — requires separate human approval |
| `FUT-MICRO-006` | `MICRO-STRICT-3P` | `caption_refuerzo` | `PASS` | PENDING — no asset generated | PENDING — required before generation | BLOCKED — requires separate human approval |
| `FUT-TRANS-003` | `TRANS-UNIVERSE` | `caption_conversacional` | `PASS` | PENDING — no asset generated | PENDING — required before generation | BLOCKED — requires separate human approval |
| `FUT-ACID-003` | `ACID-DIALOGUE` | `caption_minimo` | `PASS` | PENDING — no asset generated | PENDING — required before generation | BLOCKED — requires separate human approval |

## Campos obligatorios antes de generar cualquier asset

Cada brief debe completar los siguientes campos antes de una solicitud de generación. El preflight actual los marca como requisitos, pero no inventa valores de hora, función de caption ni identificadores experimentales:

| Campo | Regla | Estado en este preflight |
|---|---|---|
| `Experiment_ID` | Completar y revisar antes de generación. | `PENDING_BEFORE_GENERATION` |
| `Hypothesis_ID` | Completar y revisar antes de generación. | `PENDING_BEFORE_GENERATION` |
| `Cell_ID` | Completar y revisar antes de generación. | `PENDING_BEFORE_GENERATION` |
| `Caption_Treatment` | Completar y revisar antes de generación. | `PENDING_BEFORE_GENERATION` |
| `Caption_Function` | Separado de Caption_Treatment; no asumir que una pregunta retórica es conversacional. | `PENDING_BEFORE_GENERATION` |
| `Narrative_Structure` | Completar y revisar antes de generación. | `PENDING_BEFORE_GENERATION` |
| `Humor_Function` | Completar y revisar antes de generación. | `PENDING_BEFORE_GENERATION` |
| `Character_Presence` | Completar y revisar antes de generación. | `PENDING_BEFORE_GENERATION` |
| `Hora_Test` | Completar y revisar antes de generación. | `PENDING_BEFORE_GENERATION` |
| `Theme_Confound` | Completar y revisar antes de generación. | `PENDING_BEFORE_GENERATION` |
| `Reuse_Status` | Debe registrar `New_Asset_Proposed`; no mezclar con reuse. | `PENDING_BEFORE_GENERATION` |

## Salvaguardas específicas

**FUT-MICRO-005 y FUT-MICRO-006.** La pieza debe tener exactamente tres paneles inequívocos, turnos legibles y remate autosuficiente. No se acepta el candidato histórico de cuatro paneles `1036844829507460_122127951885072582` dentro de `MICRO-STRICT-3P`.

**FUT-TRANS-003.** No se puede promover la pieza sin verificar visualmente al mismo Universe en ambos estados, gafas visibles en ambos estados y marcadores de identidad preservados. Un cambio de ropa aislado o la sustitución por otro personaje no cumple.

**FUT-ACID-003.** El objetivo ácido debe ser una situación, hábito o contradicción; las voces deben distinguirse en una lectura; `Safety_Flag` debe confirmar ausencia de coerción y de ataques a rasgos protegidos.

## Condiciones de promoción

El resultado de este documento es `preflight_specification_pass`, no `generation_approved`. Antes de cualquier generación se necesita completar los campos obligatorios y obtener aprobación humana explícita para producir assets. Antes de calendario, publicación o CNT se necesita una aprobación posterior e independiente.

## Reproducibilidad

Este reporte fue generado por `Operations/Production/run_comparable_briefs_preflight.py` a partir de la matriz CSV y de los criterios del diseño técnico. No se consultaron APIs, no se modificó Facebook o Instagram y no se usó navegación externa.

## Referencias

[1]: `Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md` — criterios técnicos y estado de celdas.
[2]: `Operations/Research/2026-08-21_Paquete_Revision_Humana_Briefs_Comparables.md` — alcance de la aprobación humana.
[3]: `Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv` — matriz reproducible de decisiones.
[4]: `GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md` — reglas de evidencia y captions.
