---
title: "Diseño de casos comparables para completar celdas bajo n=3"
purpose: "Definir las piezas históricas/futuras mínimas necesarias para completar microhistoria estricta, transformación visual de Universe y diálogo ácido, con criterios de inclusión y tratamientos de caption separados."
status: Review
created: 2026-08-21
updated: 2026-08-21
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-20_Propuesta_Expansion_Celdas_Comparables.md"
  - "Operations/Research/2026-08-21_Junio_57_Unmatched_Visual_Findings.md"
  - "Operations/Research/2026-08-21_Junio_57_Unmatched_Character_Utility.csv"
  - "Operations/Production/2026-08-20_Plan_Experimentos_Agosto_5_Familias.md"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
organization: "Operations/Production"
---

# Diseño de casos comparables para completar celdas bajo n=3

## Alcance y decisión previa

La matriz actual tiene tres celdas que siguen bajo `n=3`: **microhistoria estricta de tres paneles** (`n=1`), **transformación visual de Universe** (`n=2`) y **diálogo ácido** (`n=2`). La cola de junio aporta un candidato visual de microhistoria estricta, `1036844829507460_122127951885072582`, con cuatro paneles y turnos claros. Primero debe revisarse y, si se confirma como comparable, la necesidad de producción se reduce de dos casos estrictos a uno.

Los diseños siguientes son briefs de prueba, no publicaciones aprobadas. No generan assets, no modifican calendario y no asignan CNT. Su función es que la próxima pieza que se cree responda una brecha estadística concreta.

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
