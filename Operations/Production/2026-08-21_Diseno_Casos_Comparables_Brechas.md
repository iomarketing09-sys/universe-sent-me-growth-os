---
title: "Diseño de casos comparables para completar celdas bajo n=3"
purpose: "Definir las piezas históricas/futuras mínimas necesarias para completar microhistoria estricta, transformación visual de Universe y diálogo ácido, con criterios de inclusión y tratamientos de caption separados."
status: Review
created: 2026-08-21
updated: 2026-08-21
version: "1.2"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-20_Propuesta_Expansion_Celdas_Comparables.md"
  - "Operations/Research/2026-08-21_Junio_57_Unmatched_Visual_Findings.md"
  - "Operations/Research/2026-08-21_Junio_57_Unmatched_Character_Utility.csv"
  - "Operations/Research/2026-08-21_Junio_57_Approved_Character_Analysis.md"
  - "Operations/Production/2026-08-20_Plan_Experimentos_Agosto_5_Familias.md"
  - "Operations/Research/2026-08-21_Paquete_Revision_Humana_Briefs_Comparables.md"
  - "Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
organization: "Operations/Production"
---

# Diseño de casos comparables para completar celdas bajo n=3

## Paquete de revisión humana y aprobación de preflight

Los cuatro briefs están preparados para revisión en `Operations/Research/2026-08-21_Paquete_Revision_Humana_Briefs_Comparables.md`, con la matriz estructurada en `Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv`. Cada brief tiene estado `Approved_for_Preflight`. La aprobación de Fernando autoriza pasar a preflight, pero no autoriza generar assets finales, mover calendario, publicar ni crear CNT.

## Alcance y decisión previa

La matriz actual tiene tres celdas que siguen bajo `n=3`: **microhistoria estricta de tres paneles** (`n=1`), **transformación visual de Universe** (`n=2`) y **diálogo ácido** (`n=2`). La cola de junio aportó `1036844829507460_122127951885072582`, pero la validación confirmó cuatro paneles. Por tanto, se excluye de la celda estricta y la necesidad de producción se mantiene en dos casos nuevos de tres paneles.

Los diseños siguientes son briefs de prueba aprobados para preflight, no publicaciones aprobadas. El preflight puede preparar especificaciones y validar riesgos, pero no genera assets finales, no modifica calendario y no asigna CNT. Su función es que la próxima pieza que se cree responda una brecha estadística concreta.

## Estado actual de las celdas comparables

| Cell_ID | Casos válidos actuales | Estado de evidencia | Requerimiento pendiente | Brief/preflight asociado |
|---|---:|---|---|---|
| `MICRO-STRICT-3P` | `n=1` | Insuficiente para señal preliminar; el candidato 4P está excluido | Dos piezas nuevas de exactamente tres paneles; una romántico-absurda y una cotidiana no romántica | `FUT-MICRO-005`, `FUT-MICRO-006` aprobados para preflight |
| `MICRO-SEQ-2P` | `n=3` | Señal preliminar estructural; aún no veredicto operativo | Dos casos adicionales para llegar a `n=5`, sin mezclar con 3P | Sin brief activo |
| `TRANS-UNIVERSE` | `n=2` | Bajo `n=3`; no hay señal preliminar | Una transformación nueva del mismo Universe, con gafas y marcadores preservados | `FUT-TRANS-003` aprobado para preflight |
| `OBSERVACIONAL` | `n=3` | Señal preliminar; sensible a outliers y tema | Dos casos adicionales para veredicto operativo `n=5`; mantener tema y estructura comparables | Sin brief activo |
| `ACID-DIALOGUE` | `n=2` | Bajo `n=3` | Un diálogo ácido nuevo con destinatario claro y remate seguro | `FUT-ACID-003` aprobado para preflight |
| `SELF-DEPRECATION/ANTIHERO` | `n=3` | Señal preliminar heterogénea | Dos casos adicionales para `n=5`; separar autodesprecio de simple tristeza o roast | Sin brief activo |

Los cuatro briefs aprobados no cierran ninguna celda por sí solos: autorizan únicamente preflight. La promoción de cada pieza requerirá confirmar `Cell_ID`, `Narrative_Structure`, `Caption_Treatment`, `Caption_Function`, `Character_Presence`, `Theme_Confound`, `Hora_Test`, seguridad y ausencia de confusores excluidos. Para una señal preliminar se mantiene `n=3`; para un veredicto operativo, `n=5`.

## Aprobación de análisis selectivo

Fernando aprobó la incorporación de los 17 casos visuales de personaje a la capa de análisis selectivo. La aprobación tiene alcance limitado: permite comparar presencia visual, rol narrativo, potencial de etiquetado y relación con celdas, pero no autoriza crear CNT, modificar canon, reutilizar assets ni mover publicaciones. El estado quedó registrado en `2026-08-21_Junio_57_Unmatched_Character_Utility.csv` con `approval_status=Approved_Character_Analysis`.

## Protocolo de validación del candidato `122127951885072582`

El candidato muestra cuatro paneles, dos interlocutores humanos visualmente consistentes, turnos telefónicos claros y un remate de baile en el último panel. Por esa razón **no debe entrar automáticamente a la celda estricta de tres paneles**, cuya definición exige exactamente tres paneles. Se conserva como candidato para una eventual subcelda `MICRO-SEQ-4P`, pero esa subcelda no se abre ni se mezcla con `MICRO-STRICT-3P` sin al menos tres casos comparables y una definición aprobada. Estado final: `Excluded_3P_Retain_4P_Candidate`.

| Parámetro | Regla de validación | Resultado actual |
|---|---|---|
| `Meta_ID` único | El identificador debe existir en la cola y no duplicarse en la matriz | Pasa: `1036844829507460_122127951885072582` |
| Evidencia visual | Imagen Meta disponible y legible | Pasa |
| Conteo de paneles | `MICRO-STRICT-3P` exige exactamente 3; `MICRO-SEQ-4P` exige exactamente 4 | Pasa para 4P; falla para 3P |
| Turnos narrativos | Cada panel debe avanzar la conversación/acción, no solo repetir composición | Pasa: llamada, respuesta, transición y baile |
| Remate | El último panel debe cambiar o completar la lectura | Pasa provisionalmente: el diálogo culmina en baile |
| Continuidad visual | Los interlocutores deben ser distinguibles y consistentes | Pasa provisionalmente |
| Caption histórico | No inferir tratamiento; usar `historical_unavailable` si no hay fuente | `historical_unavailable` |
| Métricas | Conservar lifetime, aunque sea cero; no eliminar por bajo rendimiento | Válidas; 0 interacciones en la cola |
| Asset/Drive | Requerido para integración de inventario/CNT, no para observar estructura narrativa | Pendiente; no se crea CNT |
| Promoción | Solo si coincide con la definición de la celda elegida | `Excluded_3P_Retain_4P_Candidate`; no abrir 4P todavía |

La decisión metodológica es conservar la estructura de cuatro paneles como aprendizaje negativo para la celda estricta: **una pieza puede ser una microhistoria válida y, aun así, no ser comparable con una celda definida por tres paneles**. Esto evita ampliar la definición después de ver el rendimiento o de necesitar completar `n=3`.

## Casos mínimos diseñados

| Test_ID | Cell_ID | Caso necesario | Tratamiento inicial | Por qué hace falta | Criterio de inclusión |
|---|---|---|---|---|---|
| `FUT-MICRO-005` | `MICRO-STRICT-3P` | Microhistoria romántico-absurda de tres paneles con dos personajes no canónicos | `caption_minimo` | Añade un caso distinto al base `MICRO-001` sin introducir una identidad canónica como confusor | Tres paneles inequívocos; un turno por panel; remate en el tercer panel; texto visual legible; caption de 0–3 emojis o remate mínimo |
| `FUT-MICRO-006` | `MICRO-STRICT-3P` | Microhistoria cotidiana de tres paneles con conflicto interpersonal no romántico | `caption_refuerzo` | Evita que la señal de microhistoria sea solo romance/relación y permite separar estructura de tema | Tres paneles; situación cotidiana universal; dos turnos visibles; último panel reencuadra; el caption no repite el diálogo |
| `FUT-TRANS-003` | `TRANS-UNIVERSE` | Transformación visual explícita del mismo Universe entre estado A y B | `caption_conversacional` | Lleva la celda de transformación de `n=2` a `n=3` sin contar vestuario de Ganso ni mutación de personaje genérico | Mismo sujeto en antes/después; gafas presentes en ambos estados; marcadores de identidad preservados; cambio corporal/material único; no mezclar con sexualidad dominante |
| `FUT-ACID-003` | `ACID-DIALOGUE` | Diálogo ácido de dos personajes con destinatario comprensible y remate interpersonal | `caption_minimo` | Lleva diálogo ácido de `n=2` a `n=3` sin convertir cualquier diálogo relacional en humor ácido | Dos voces distinguibles; destinatario claro; filo comprensible en una lectura; remate breve; sin coerción, humillación protegida o agresión gratuita |

## Especificación de cada caso

### `FUT-MICRO-005` — tres paneles, romance absurdo

El primer panel debe presentar una intención afectiva o una expectativa reconocible. El segundo debe mostrar una respuesta literal o excesivamente seria del segundo personaje. El tercero debe invertir la lectura sin añadir un cuarto panel ni depender de una explicación externa. La escena puede usar una persona y una criatura fantástica genérica, pero no debe nombrar a Kiri, Elara, Universe u otro personaje canonizado.

La variable visual principal es `Narrative_Structure=dialogue_sequential_3_panel`. Las covariables serán `Theme=romantic_absurd`, `Character_Presence=generic_pair`, `Hook_Type=colloquial_statement` y `Caption_Treatment=caption_minimo`. No se utilizará caption conversacional porque abriría una segunda pregunta distinta de la que responde la imagen.

### `FUT-MICRO-006` — tres paneles, conflicto cotidiano

El primer panel debe introducir un problema cotidiano —por ejemplo, llegar tarde, olvidar una tarea o responder un mensaje—. El segundo debe incluir una justificación literal que parezca razonable. El tercero debe revelar que el problema real era una interpretación social inesperada. La pieza no debe ser sexual ni depender de un personaje recurrente.

La variable visual será la misma `dialogue_sequential_3_panel`, pero `Theme=everyday_social_conflict`. El caption `caption_refuerzo` será una frase corta que ilumine la lectura sin repetir los globos. Si el caso histórico `1036844829507460_122127951885072582` se confirma como comparable, este caso será el único nuevo microestricto necesario para alcanzar `n=3`; el otro se conserva como backup.

### `FUT-TRANS-003` — transformación de Universe con identidad preservada

La composición debe mostrar al mismo gato con gafas antes y después de una transformación única: cambio corporal, material o escala, pero no una mezcla de mutación, vestuario y escenario. Las gafas deben aparecer claramente en ambos estados. El fondo puede cambiar de forma secundaria, pero no debe competir con el antes/después.

Los campos obligatorios son `preserva_gafas_universe=Sí`, `preserva_marcadores_identidad=Sí`, `Transformation_Type`, `Before_State`, `After_State`, `Theme_Confound` y `Character_Presence=Universe_Confirmed`. Se excluyen transformaciones de Ganso, personajes genéricos, sexualidad explícita y escenas que solo cambian de vestuario.

### `FUT-ACID-003` — diálogo ácido interpersonal

La pieza debe mostrar a dos participantes con roles visualmente distinguibles. El primer turno establece una conducta o afirmación; el segundo responde con un remate que pincha esa conducta. El ácido debe dirigirse a una situación o a una contradicción comprensible, no a una característica protegida ni a una amenaza. La composición puede ser de una escena con dos globos o de dos paneles, siempre que los turnos sean inequívocos.

Los campos obligatorios son `Acid_Target`, `Interpersonal_Conflict`, `Reframe_Type`, `Remate_Legibility`, `Safety_Flag` y `Character_Presence`. El caso no entra si únicamente es coqueteo, ansiedad, humor sexual o una respuesta relacional sin filo.

## Diseño de medición

Cada pieza futura debe registrarse antes de publicar con `Experiment_ID`, `Hypothesis_ID`, `Cell_ID`, `Caption_Treatment`, `Narrative_Structure`, `Humor_Function`, `Character_Presence`, `Hora_Test`, `Theme_Confound` y `Reuse_Status`. La hora debe rotarse entre casos para evitar atribuir la señal a una franja concreta. El contenido nuevo y el reuse no deben mezclarse dentro del mismo denominador.

| Medición | Uso |
|---|---|
| Interacciones lifetime | Métrica descriptiva histórica; no sustituye ventanas operativas |
| Shares | Indicador principal de difusión, reportado con mediana y sensibilidad a outliers |
| Comentarios | Indicador de conversación; revisar solo hilos que respondan una pregunta |
| Potencial de etiquetado | Covariable estructural, no resultado automático |
| Caption_Treatment | Covariable; no atribuir efecto con una sola pieza por tratamiento |
| Hora_Test | Covariable y posible confusor; rotar entre casos |

Para una señal preliminar, cada celda debe alcanzar `n=3`. Para un veredicto operativo se requieren `n=5`; para comparar los tres tratamientos de caption dentro de una celda se necesitan al menos seis casos balanceados, dos por tratamiento. Estos diseños solo cubren la próxima brecha mínima y no constituyen un veredicto.

## Orden de ejecución

Primero debe confirmarse visualmente `1036844829507460_122127951885072582`. Después se diseña `FUT-TRANS-003` y `FUT-ACID-003`, porque cada uno requiere solo un caso nuevo. La microhistoria estricta se resuelve con `FUT-MICRO-006` si el candidato histórico entra; si queda fuera, se producen tanto `FUT-MICRO-005` como `FUT-MICRO-006`.

Ningún caso se publica sin aprobación humana de Fernando. Antes de cualquier uso en calendario, el brief debe pasar por la revisión de assets, identidad visual y tratamientos de caption descrita en el plan de cinco familias.

## Referencias

[1]: `Operations/Research/2026-08-20_Propuesta_Expansion_Celdas_Comparables.md` — definiciones y umbrales de las celdas.
[2]: `Operations/Research/2026-08-21_Junio_57_Unmatched_Visual_Findings.md` — revisión de la cola sin match.
[3]: `Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv` — matriz de comparabilidad histórica.
[4]: `Operations/Production/2026-08-20_Plan_Experimentos_Agosto_5_Familias.md` — arquitectura de experimentos futuros.
[5]: `GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md` — reglas de evidencia y salvaguardas de identidad.
