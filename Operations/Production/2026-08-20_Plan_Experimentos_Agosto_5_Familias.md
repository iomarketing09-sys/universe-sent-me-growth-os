---
title: "Plan de experimentos de agosto — cinco familias de contenido"
purpose: "Convertir los aprendizajes históricos de junio y julio en una secuencia controlada de experimentos para agosto, separada de P0, afiliados, reuse y cambios canónicos."
status: Review
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-20_Sintesis_Historica_Crecimiento_Junio_Julio.md"
  - "Operations/Research/2026-08-20_Comparativo_Crecimiento_Junio_Julio.json"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
  - "Operations/Research/2026-08-15_ExperimentLog.csv"
  - "Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv"
  - "Operations/Research/2026-08-20_Propuesta_Expansion_Celdas_Comparables.md"
  - "Operations/Production/2026-08-20_Wave1_Signal_Experiment_Design.csv"
  - "Operations/Production/2026-08-19_Piloto_Esfuerzo_y_Experimentacion.md"
organization: "Operations/Production"
---

# Plan de experimentos de agosto — cinco familias de contenido

## 1. Principio operativo

El plan no es un calendario automático. Es un **registro previo de hipótesis** que debe aprobarse antes de asignar assets o publicar. Su función es que cada publicación responda una pregunta concreta y que el Growth OS pueda distinguir si funcionó la familia de contenido, el caption, la hora, el personaje o una combinación accidental.

Junio y julio aportan evidencia histórica de alto valor, pero sus métricas son lifetime. Agosto se medirá con ventanas operativas estandarizadas y, cuando sea posible, con snapshots de 24 y 72 horas. Por eso el histórico se usa para diseñar tratamientos; no se mezcla directamente con los resultados de la cohorte activa.

## 2. Las cinco familias e hipótesis

| Family_ID | Familia | Hipótesis de agosto | Métrica primaria | Riesgo de confusión |
|---|---|---|---|---|
| `FAM-01` | `Difusión_Minimal` | Una imagen con remate visual fuerte y `caption_minimo` reduce fricción y eleva shares | Shares por publicación | El resultado puede venir de la imagen, no del caption |
| `FAM-02` | `Relatable_Social` | Una situación transferible a otra persona eleva shares, etiquetas y comentarios de identificación | Shares + etiquetas/comentarios | La temática puede ser más familiar que la familia en sí |
| `FAM-03` | `Conversación_Relacional` | Dos voces, pregunta/respuesta o tensión interpersonal abre más conversación | Comentarios raíz + replies | La conversación puede ser entre usuarios y no con la página |
| `FAM-04` | `Ácido_Interpersonal` | La ironía o conflicto interpersonal claro supera al “humor ácido” genérico | Shares + comentarios raíz | No mezclar sexual explícito, observacional oscuro y ácido relacional |
| `FAM-05` | `Personaje_Marcador` | Un personaje visualmente confirmado, con marcador reconocible y situación clara, sostiene difusión sin depender del filename | Mediana de shares + interacciones | Personaje y concepto pueden quedar completamente confundidos |

`FAM-05` no prueba que un personaje sea causalmente superior. Solo prueba si la **identidad visual confirmada** ayuda cuando la situación está controlada.

## 3. Tratamientos de caption

Los tres tratamientos se registran como variable independiente:

| Caption_Treatment | Definición | Uso |
|---|---|---|
| `caption_minimo` | Cero a tres emojis o un remate mínimo; no explica la imagen | Prioridad para `FAM-01`; también puede aparecer en otras familias |
| `caption_refuerzo` | Frase corta que ilumina o amplía la lectura sin repetir el texto visual | Prioridad para `FAM-02`, `FAM-04` y `FAM-05` |
| `caption_conversacional` | Pregunta, invitación o remate que abre una respuesta natural | Prioridad para `FAM-03` |

Para la primera ola no se deben asignar todos los `caption_minimo` a la mejor hora ni todos los `caption_conversacional` a la peor. El tratamiento debe rotarse entre franjas y días para evitar confundir caption con horario.

## 4. Arquitectura de cohortes

Se recomienda una estructura de dos etapas.

| Etapa | Tamaño | Objetivo | Qué permite concluir |
|---|---:|---|---|
| `Wave_1_Signal` | 15 posts; tres por familia | Una pieza por treatment dentro de cada familia | Señal preliminar de estructura; no atribución causal del caption |
| `Wave_2_Operational` | 30 posts; seis por familia | Dos piezas por cada treatment dentro de cada familia | Comparación inicial de treatments dentro de una familia |

La primera ola debe ser la prioridad porque permite aprender con un coste razonable. Cada familia recibe tres piezas: una con `caption_minimo`, una con `caption_refuerzo` y una con `caption_conversacional`. Si una familia no es compatible con un treatment, se marca `Not_Applicable` con una razón; no se fuerza una pregunta artificial.

La segunda ola solo se activa para las familias que sobrevivan al filtro preliminar. Allí cada familia recibe seis piezas, dos por treatment, distribuidas en al menos dos días y dos franjas. Para un veredicto operativo conviene llegar a cinco piezas comparables por familia, pero seis permiten además no confundir un único caption con el resultado de la familia.

## 5. Rotación de horarios y días

El corredor histórico prioritario es **18:00–22:00**, con un control secundario en **14:00–16:00**. Esto no es una regla de calendario; es una distribución inicial para que las cinco familias tengan exposición comparable.

La rotación mínima debe impedir que una familia reciba siempre la misma hora. Una secuencia de ejemplo para `Wave_1_Signal` sería:

| Familia | Caso A | Caso B | Caso C |
|---|---|---|---|
| `FAM-01` | 18:00 / `caption_minimo` | 20:00 / `caption_refuerzo` | 22:00 / `caption_conversacional` |
| `FAM-02` | 20:00 / `caption_minimo` | 22:00 / `caption_refuerzo` | 18:00 / `caption_conversacional` |
| `FAM-03` | 22:00 / `caption_minimo` | 18:00 / `caption_refuerzo` | 20:00 / `caption_conversacional` |
| `FAM-04` | 14:00 / `caption_minimo` | 18:00 / `caption_refuerzo` | 20:00 / `caption_conversacional` |
| `FAM-05` | 16:00 / `caption_minimo` | 14:00 / `caption_refuerzo` | 22:00 / `caption_conversacional` |

La tabla es un patrón de balance, no una autorización para programar. La fecha y hora reales se deben registrar después de aprobación humana y no deben moverse sin dejar constancia.

## 6. Registro previo de cada publicación

Antes de publicar, cada fila del `ExperimentLog` debe completar como mínimo los siguientes campos:

| Campo | Ejemplo | Regla |
|---|---|---|
| `Experiment_ID` | `EXP-2026-08-FAM-W1` | Identifica la ola, no el post individual |
| `Hypothesis_ID` | `H-AUG-FAM01` | Una hipótesis principal por pieza |
| `Cell_ID` | `FAM-01` | Una familia primaria; las etiquetas secundarias son opcionales |
| `Caption_Treatment` | `caption_minimo` | Registrar antes de publicar |
| `Format` | `Facebook_Image` | No mezclar con Reels en el mismo agregado |
| `Visual_Identity_Confirmed` | `Yes` | No derivar personaje desde filename |
| `Hour_Test` | `18:00` | Hora planeada y hora real por separado |
| `P0_Eligible` | `No` | Los posts de esta ola no deben entrar en P0 simultáneamente |
| `Affiliate_Attachment` | `No` | No adjuntar productos en la ola base |
| `Reuse_Status` | `New_Test` | No mezclar reuse con piezas nuevas |
| `Canon_Impact` | `None` | El experimento no modifica la Biblia |

## 7. Métricas y corte

La métrica primaria debe definirse antes de publicar. Para `FAM-01`, `FAM-02`, `FAM-04` y `FAM-05` la prioridad es shares; para `FAM-03`, comentarios raíz y replies. Las interacciones totales —reacciones + comentarios + shares— quedan como métrica secundaria común.

La evaluación debe usar medianas por familia y treatment, no solo medias. Se registrarán snapshots a 24 y 72 horas cuando Meta permita reconstruirlos de forma válida. Si la ventana exacta no es recuperable, se usará el corte disponible y se marcará `Window_Not_Exact`; ese caso no se mezclará con un corte exacto.

También deben registrarse comentarios raíz, replies, etiquetas, guardados o alcance cuando estén disponibles. Los afiliados se mantienen en su ledger separado y no se atribuye ninguna conversión a una familia editorial de esta ola.

## 8. Criterios de decisión

| Nivel | Requisito | Decisión |
|---|---|---|
| `Sin_Señal` | Menos de tres casos comparables o dirección inconsistente | No escalar; mantener como hipótesis abierta |
| `Señal_Preliminar` | Al menos tres casos comparables y al menos dos muestran la misma dirección frente al control histórico/agosto | Diseñar una segunda ola; no convertir en regla |
| `Señal_Replicable` | Al menos cinco casos comparables, dos franjas y dos días, con mediana de shares al menos 50% superior al control comparable | Considerar la familia para producción prioritaria, sujeto a guardas |
| `Tratamiento_Compatible` | Un treatment supera a otro dentro de la misma familia con al menos dos casos por treatment | Usarlo como hipótesis de copy; no declararlo universal |
| `Outlier_Dominante` | Una pieza concentra más de 40% de las interacciones de su familia o supera 2× el rango intercuartílico | Reportar con y sin outlier; no usarla como benchmark único |

Estos umbrales son operativos del Growth OS, no pruebas estadísticas definitivas. La lectura final debe incluir volumen, mediana, dispersión y calidad de conversación.

## 9. Guardas contra contaminación

La ola base no debe incluir publicaciones P0, enlaces afiliados, productos adjuntos, reuse, crosspost de Reel ni posts con cambios canónicos. Si por necesidad editorial una pieza cae en una de esas categorías, se etiqueta como `Contaminated` y se excluye del agregado principal.

Tampoco se deben comparar en la misma celda imágenes nuevas y reuse sin un campo de tratamiento. La hora real debe conservarse, y no se debe atribuir a caption un efecto que coincida con un cambio de día, personaje o formato.

Los personajes se codifican por revisión visual. El filename solo sirve como referencia de asset. Si una transformación no conserva los marcadores de identidad de Universe, se registra para revisión canónica y no se interpreta únicamente como fallo de rendimiento.

## 10. Secuencia recomendada

Primero se debe aprobar la matriz de `Wave_1_Signal` y seleccionar 15 piezas candidatas, sin publicarlas todavía. Después se completa el registro previo y se valida que no haya coincidencias con P0, afiliados o reuse. A continuación se publican únicamente los posts aprobados, se capturan los snapshots operativos y se actualiza el `ExperimentLog`.

Al cerrar las 15 piezas, se realiza el veredicto preliminar por familia. Solo las familias con `Señal_Preliminar` pasan a `Wave_2_Operational`. Si ninguna alcanza la señal, no se fuerza una segunda ola: se utiliza la información para modificar la hipótesis o cambiar la composición visual.

## Estado

Este documento queda en `Review`. No autoriza programación, publicación, modificación del calendario, adjuntar productos afiliados ni alterar P0. La siguiente acción requiere aprobación humana de la arquitectura de `Wave_1_Signal` y de las 15 asignaciones concretas. La matriz inicial se encuentra en `Operations/Production/2026-08-20_Wave1_Signal_Experiment_Design.csv`; todos los assets, fechas y aprobaciones permanecen en `TBD`/`Pending`.

## Referencias

[1]: `Operations/Research/2026-08-20_Sintesis_Historica_Crecimiento_Junio_Julio.md` — síntesis histórica y familias de contenido.
[2]: `Operations/Research/2026-08-20_Comparativo_Crecimiento_Junio_Julio.json` — base comparable y métricas históricas.
[3]: `Operations/Research/2026-08-15_ExperimentLog.csv` — esquema de registro de experimentos.
[4]: `GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md` — reglas de aprendizaje vigentes.
[5]: `Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv` — estado de celdas y guardas de identidad.
