---
title: "Paquete de revisión y preflight — briefs comparables aprobados"
purpose: "Registrar la aprobación de preflight y presentar una solicitud separada de autorización exclusiva para generar los cuatro assets comparables, manteniendo bloqueados calendario, publicación y CNT."
status: Active
created: 2026-08-21
updated: 2026-08-21
version: "1.3"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md"
  - "Operations/Production/2026-08-20_Plan_Experimentos_Agosto_5_Familias.md"
  - "Operations/Research/2026-08-20_Propuesta_Expansion_Celdas_Comparables.md"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
  - "Operations/Research/2026-08-21_Autorizacion_Generacion_Briefs_Comparables.csv"
  - "Operations/Production/validate_generation_authorization_matrix.py"
  - "Operations/Production/approve_generation_briefs.py"
  - "Operations/Production/2026-08-21_Prompts_Assets_Comparables.md"
  - "Operations/Production/2026-08-21_Generated_Comparable_Assets.csv"
  - "Operations/Production/2026-08-21_Control_Visual_Assets_Comparables.md"
  - "GrowthOS/Integracion_Growth_OS.md"
organization: "Operations/Research"
---

# Paquete de revisión y preflight — briefs comparables aprobados

## Estado de autorización

Este paquete contiene cuatro briefs aprobados para **preflight** y registra ahora la aprobación separada de Fernando para autorizar exclusivamente su generación. La decisión previa quedó registrada como `Approved_for_Preflight` y `Approve_Preflight_Only`; la nueva decisión del 2026-08-21 es `Approved_Generation_Only` para los cuatro briefs. Todavía no existe autorización de calendario, publicación, reuse ni creación de CNT.

> La decisión registrada en este paquete fue únicamente `Approved_Generation_Only`: producir un asset nuevo por brief. Los cuatro assets ya fueron generados y están en control visual. La autorización no permite programar, publicar, crear CNT, adjuntar afiliados ni modificar una publicación existente.

La microhistoria estricta permanece en `n=1`, la transformación de Universe en `n=2` y el diálogo ácido en `n=2`. Estos cuatro briefs cubren las brechas mínimas, pero los tratamientos de caption se mantienen como covariables y no como una prueba causal independiente. Las hipótesis formales son `HB-006` a `HB-009` y la validación cruzada está en `4/4 PASS`.

## Resumen para decisión

| Brief_ID | Celda | Tratamiento de caption | Caso propuesto | Estado actual |
|---|---|---|---|---|
| `FUT-MICRO-005` | `MICRO-STRICT-3P` | `caption_minimo` | Romance absurdo en tres paneles, dos personajes no canónicos | `Approved_for_Preflight` |
| `FUT-MICRO-006` | `MICRO-STRICT-3P` | `caption_refuerzo` | Conflicto cotidiano no romántico en tres paneles | `Approved_for_Preflight` |
| `FUT-TRANS-003` | `TRANS-UNIVERSE` | `caption_conversacional` | Transformación única del mismo Universe, con gafas preservadas | `Approved_for_Preflight` |
| `FUT-ACID-003` | `ACID-DIALOGUE` | `caption_minimo` | Diálogo ácido interpersonal con destinatario claro | `Approved_for_Preflight` |

## Autorización de generación registrada

La matriz `Operations/Research/2026-08-21_Autorizacion_Generacion_Briefs_Comparables.csv` contiene una fila por brief. Fernando aprobó las cuatro filas el 2026-08-21 y la validación confirmó `4/4`. Se generaron los cuatro assets, uno por brief, con `Generation_Authorization=Approved_Generation_Only`; el ledger de producción registra `Calendar_Change=No`, `CNT_Creation=No`, `Publication=No` y `Affiliate_Attachment=No`.

| Brief_ID | Hypothesis_ID | Solicitud | Asset propuesto | Bloqueos que permanecen |
|---|---|---|---|---|
| `FUT-MICRO-005` | `HB-006` | `Approve_Generation_Only` | 1 asset de exactamente 3 paneles | Sin calendario, CNT, publicación, reuse o afiliados |
| `FUT-MICRO-006` | `HB-007` | `Approve_Generation_Only` | 1 asset de exactamente 3 paneles | Sin calendario, CNT, publicación, reuse o afiliados |
| `FUT-TRANS-003` | `HB-008` | `Approve_Generation_Only` | 1 asset before/after del mismo Universe | Sin calendario, CNT, publicación, reuse o afiliados |
| `FUT-ACID-003` | `HB-009` | `Approve_Generation_Only` | 1 asset de diálogo ácido seguro | Sin calendario, CNT, publicación, reuse o afiliados |

La decisión registrada es `Approved` para los cuatro briefs, con `Decision_By=Fernando` y `Decision_Date=2026-08-21`. El alcance es exclusivamente generación; no se interpreta como aprobación global de calendario, CNT, reuse, afiliados o publicación.

## Brief `FUT-MICRO-005`

**Celda:** `MICRO-STRICT-3P`. **Hipótesis:** una microhistoria romántico-absurda con exactamente tres paneles, dos turnos y un remate de reencuadre puede producir una señal comparable sin depender de una identidad canónica. **Tratamiento:** `caption_minimo`. **Estado:** `Approved_for_Preflight`; alcance `Approve_Preflight_Only`.

El primer panel debe presentar una intención afectiva o una expectativa reconocible. El segundo debe mostrar una respuesta literal, excesivamente seria o inesperadamente práctica del segundo personaje. El tercer panel debe invertir la lectura y cerrar el chiste. La pieza debe tener exactamente tres paneles; no se acepta un cuarto panel, una tira de dos paneles ni una imagen única con globos superpuestos.

Los personajes deben ser genéricos o nuevos y no deben nombrar a Universe, Wilfred, Elara, Kiri, Silvio, Fantasma, Ganso u otro personaje del canon. La escena debe ser legible sin caption externo. El caption propuesto debe aportar entre cero y tres emojis o un remate mínimo, sin repetir el texto visual.

**Debe conservarse si** la secuencia es inequívoca, el tercer panel cambia la lectura y la imagen funciona sin explicación adicional. **Debe descartarse o regenerarse si** el romance depende de una amenaza, coerción, humillación o sexualidad explícita; si el segundo panel no avanza la acción; o si el remate necesita más de tres paneles.

**Campos de preflight:** `Narrative_Structure=dialogue_sequential_3_panel`; `Theme=romantic_absurd`; `Character_Presence=generic_pair`; `Caption_Treatment=caption_minimo`; `Theme_Confound=romantic_context`; `Reuse_Status=New_Asset_Proposed`.

## Brief `FUT-MICRO-006`

**Celda:** `MICRO-STRICT-3P`. **Hipótesis:** una microhistoria cotidiana no romántica puede generar comparabilidad estructural sin confundir el efecto de la secuencia con el tema amoroso. **Tratamiento:** `caption_refuerzo`. **Estado:** `Approved_for_Preflight`; alcance `Approve_Preflight_Only`.

El primer panel debe introducir un conflicto cotidiano, como llegar tarde, olvidar una tarea o responder mal un mensaje. El segundo debe ofrecer una justificación literal que parezca razonable. El tercer panel debe revelar que el problema real era una interpretación social inesperada. La construcción debe mantener exactamente tres paneles, turnos claros y un remate autosuficiente.

No debe utilizar un personaje canónico como vehículo principal, ni depender de sexualidad, ansiedad relacional o una referencia de plataforma. El caption de refuerzo debe ser una frase corta que ilumine la lectura sin repetir los globos ni convertir la publicación en una pregunta conversacional.

**Debe aprobarse si** el conflicto es universal, el reencuadre aparece en el tercer panel y el caption añade claridad sin explicar el chiste. **Debe revisarse o rechazarse si** el resultado es una sola escena, una moraleja, una conversación sin remate o una repetición del patrón romántico de `FUT-MICRO-005`.

**Campos de preflight:** `Narrative_Structure=dialogue_sequential_3_panel`; `Theme=everyday_social_conflict`; `Character_Presence=generic_pair`; `Caption_Treatment=caption_refuerzo`; `Theme_Confound=relational_or_anxiety_risk`; `Reuse_Status=New_Asset_Proposed`.

## Brief `FUT-TRANS-003`

**Celda:** `TRANS-UNIVERSE`. **Hipótesis:** una transformación visual única del mismo Universe puede ser comparable si preserva gafas y marcadores de identidad en los estados antes/después. **Tratamiento:** `caption_conversacional`. **Estado:** `Approved_for_Preflight`; alcance `Approve_Preflight_Only`.

La composición debe mostrar el mismo gato con gafas en un estado A y un estado B. El cambio debe ser único y visualmente verificable: transformación corporal, material o de escala. No se deben combinar mutación, cambio de vestuario, cambio de escenario y cambio de especie como si fueran una sola transformación.

Los campos obligatorios son `preserva_gafas_universe=Sí`, `preserva_marcadores_identidad=Sí`, `Transformation_Type`, `Before_State`, `After_State`, `Character_Presence=Universe_Confirmed` y `Theme_Confound`. Las gafas deben ser visibles en ambos estados y el rostro, la morfología felina o el marcador visual equivalente deben permanecer reconocibles.

**Debe aprobarse si** el antes/después es inequívoco, el sujeto es el mismo, las gafas están presentes en ambos estados y no existe un segundo cambio dominante. **Debe revisarse o rechazarse si** la imagen transforma a Ganso u otro personaje, cambia solo de ropa, no preserva gafas, presenta dos sujetos diferentes o deja que el fondo explique el supuesto cambio.

El caption conversacional debe abrir una invitación natural breve sin describir literalmente la transformación. No se debe añadir un producto afiliado ni un enlace en esta prueba.

**Campos de preflight:** `Narrative_Structure=visual_before_after`; `Theme=transformation_identity`; `Character_Presence=Universe_Confirmed`; `Caption_Treatment=caption_conversacional`; `preserva_gafas_universe=Sí`; `preserva_marcadores_identidad=Sí`; `Reuse_Status=New_Asset_Proposed`.

## Brief `FUT-ACID-003`

**Celda:** `ACID-DIALOGUE`. **Hipótesis:** un diálogo ácido con dos voces distinguibles, destinatario comprensible y remate interpersonal puede añadir una tercera observación comparable sin convertir cualquier conversación relacional en humor ácido. **Tratamiento:** `caption_minimo`. **Estado:** `Approved_for_Preflight`; alcance `Approve_Preflight_Only`.

La primera voz debe establecer una conducta, contradicción o afirmación reconocible. La segunda debe responder con un remate que pinche esa conducta. El ácido debe dirigirse a una situación, hábito o contradicción, no a una característica protegida, una amenaza, una humillación degradante o una dinámica de dominación.

La escena puede tener un panel con dos globos o dos paneles, siempre que los turnos sean inequívocos. El caption debe ser mínimo y no debe explicar el remate. Se excluyen coqueteo sin filo, ansiedad relacional, humor sexual sin destinatario claro y respuestas genéricas que podrían pertenecer a cualquier página.

**Debe aprobarse si** el destinatario del remate se entiende en una lectura, el intercambio tiene tensión cómica y el final no requiere contexto externo. **Debe revisarse o rechazarse si** el ácido se convierte en agresión gratuita, se apoya en sexualidad dominante, no distingue las voces o no contiene un remate reconocible.

**Campos de preflight:** `Narrative_Structure=interpersonal_dialogue`; `Theme=acid_interpersonal`; `Character_Presence=generic_pair_or_confirmed_character`; `Caption_Treatment=caption_minimo`; `Acid_Target=Situation_or_habit`; `Safety_Flag=No_coercion_no_protected_trait_attack`; `Reuse_Status=New_Asset_Proposed`.

## Matriz de aprobación registrada

| Brief_ID | Aprobar brief | Solicitud de ajuste | Rechazar | Comentario de Fernando |
|---|---|---|---|---|
| `FUT-MICRO-005` | ☐ | ☐ | ☐ | ______________________________ |
| `FUT-MICRO-006` | ☐ | ☐ | ☐ | ______________________________ |
| `FUT-TRANS-003` | ☐ | ☐ | ☐ | ______________________________ |
| `FUT-ACID-003` | ☐ | ☐ | ☐ | ______________________________ |

## Resultado de generación y secuencia posterior

La generación produjo cuatro archivos PNG, uno por brief. El control visual preliminar marca `Pass_visual_preliminar` para `FUT-MICRO-005`, `FUT-MICRO-006` y `FUT-ACID-003`. `FUT-TRANS-003` marca `Pass_visual_preliminar_con_identidad_consistente` porque las gafas son visibles en ambos estados y la comparación con la referencia compartida confirmó identidad consistente.

Cada asset pasará por control de identidad, texto, seguridad, `Cell_ID`, tratamiento de caption y hora experimental. La generación no modificó calendario, CNT ni plataformas. Solo una aprobación humana posterior e independiente podrá autorizar su inclusión en calendario, creación de CNT o publicación.

Si un brief recibe ajustes, se actualizará este paquete y se conservará la versión anterior en el historial del repositorio. Si se rechaza, quedará como `Rejected_Brief` y no se reutilizará la idea automáticamente.

## Referencias

[1]: `Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md` — diseño técnico de celdas y validación.
[2]: `Operations/Production/2026-08-20_Plan_Experimentos_Agosto_5_Familias.md` — arquitectura experimental de agosto.
[3]: `Operations/Research/2026-08-20_Propuesta_Expansion_Celdas_Comparables.md` — brechas y umbrales de comparabilidad.
[4]: `GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md` — reglas de evidencia y salvaguardas de identidad.
[5]: `Operations/Research/2026-08-21_Autorizacion_Generacion_Briefs_Comparables.csv` — matriz de decisión limitada a generación.
[6]: `Operations/Production/validate_generation_authorization_matrix.py` — validador de bloqueos operativos.
