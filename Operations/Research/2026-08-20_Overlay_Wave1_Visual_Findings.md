---
title: "Hallazgos visuales del overlay Wave 1 — corte inicial"
purpose: "Registrar la revisión visual de los 15 slots del overlay y separar clasificación experimental de riesgos editoriales."
status: Review
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-20_Overlay_Wave1_Calendario_17_30.csv"
  - "Operations/Research/2026-08-20_Overlay_Wave1_Contact_Sheet.jpg"
  - "Operations/Research/2026-08-20_Ajuste_Experimentos_Calendario_17_30.md"
organization: "Operations/Research"
---

# Hallazgos visuales del overlay Wave 1 — corte inicial

## Revisión de hoja de contacto

La hoja confirma que los 15 candidatos son imágenes nuevas con una mezcla de composiciones de texto sobre imagen, personajes individuales, parejas y escenas relacionales. La asignación por filename es útil como punto de partida, pero la clasificación experimental debe conservar una columna de identidad visual confirmada y una nota de riesgo.

`2608053` muestra un gato blanco con gafas doradas sosteniendo una pistola aparentemente de juguete. El texto dice: “Me vas a dar tu amor quieras o no”. Visualmente es una pieza de personaje/marcador de Universe y el remate es claro, pero el conjunto combina coerción romántica y arma. No debe entrar automáticamente a `Relatable_Social` ni a `Ácido_Interpersonal`; queda como `Editorial_Hold` hasta aprobación explícita del tono.

Los casos de pareja de `2608042` y `2608045` tienen una lectura relacional clara, pero el texto visible es romántico o sugerente; pueden servir para `Conversación_Relacional` solo si la imagen muestra interacción comprensible y si el caption no intensifica el doble sentido. `2608049` es una composición de texto sobre una escena fantástica, por lo que primero debe confirmarse si hay diálogo real o solo una frase afectiva.

Los casos `2608065`, `2608064` y `2608055` necesitan separar sus funciones: el primero parece observacional/existencial con Fantasma; el segundo es un remate ácido de Universe; el tercero es una observación de ansiedad con Kiri. No deben agruparse automáticamente solo por contener lenguaje ácido, ansiedad o humor oscuro.

`2608057` confirma un personaje visual tipo Fantasma con texto de doble sentido. Puede servir para `Personaje_Marcador`, pero requiere mantener separado el riesgo de sexualidad. `2608044` muestra a Silvio en una escena visual de ligues y puede funcionar como marcador de personaje, siempre que la clasificación de humor no se use para afirmar que Silvio causa rendimiento.

## Regla provisional

La revisión visual no autoriza publicar, mover slots ni cambiar captions. Los estados deben distinguir `Candidate_Review`, `Editorial_Hold`, `Current_Comparable` y `Excluded_Not_Comparable`. En particular, una pieza puede ser buen candidato de una familia y, al mismo tiempo, necesitar un hold editorial por el tono.

## Revisión detallada adicional

`2608049` no es una conversación visual: es una escena de Elara junto a una fogata con un texto monológico y afectivo (“Tibio tu café… el romanticismo no murió porque yo sigo viva”). Se retira provisionalmente de `FAM-03 Conversación_Relacional` y se reclasifica como `FAM-02 Relatable_Social` o `Candidate_Review`, porque su fuerza está en una declaración relatable, no en turnos entre personajes. El treatment conversacional no es apropiado sin cambiar la función original.

`2608042` sí muestra una pareja en interacción física y un globo de texto (“t qiero besiquiar”), pero la función es romance directo, no conversación desarrollada. Puede permanecer como `FAM-03 Conversación_Relacional` únicamente como caso de relación/afecto de baja complejidad, con riesgo editorial `Sexual_Romantic_Low`. El caption no debe intensificar el contenido sexual ni crear una pregunta artificial.

## Revisión de pareja y ansiedad

`2608045` muestra a un humano y una hada abrazados, con el texto “A noche soñé contigo, no te voy a mentir, los vimos involucrados deliciosamente”. Es una escena romántica/sugerente con composición de pareja, pero no una conversación visual. Se mueve de `FAM-03` a `Candidate_Review` de `Relatable_Social` o `Personaje_Marcador`; no debe recibir `caption_conversacional` porque no hay una pregunta ni intercambio.

`2608055` sí es una pieza de observación relatable: Kiri aparece con expresión ansiosa y el texto describe correr para que no la atrape el monstruo cuando se apaga la luz. Se clasifica mejor como `FAM-02 Relatable_Social`, no como `Ácido_Interpersonal`. El caption conversacional podría abrir identificación, pero el tratamiento debe conservar el tono de ansiedad absurda sin intensificarlo.

## Revisión de doble sentido y marcador de personaje

`2608057` muestra claramente a Fantasma con gafas y un texto de doble sentido (“¿Sabes que me caería bien ahorita? Tú encima”). La identidad visual está confirmada, pero el humor sexual es el elemento dominante. Se mantiene como candidato de `FAM-05 Personaje_Marcador` solo con `Risk_Flag=Sexual_Double_Entendre` y no debe compararse con un marcador neutro sin esa etiqueta.

`2608059` muestra a Kael visualmente confirmado, con torso descubierto y el texto “Si la vida te da limones, pónmelos en la cara”. Es un caso de personaje/marcador con doble sentido sexual explícito en el remate. Se recomienda `Editorial_Hold` para la ola experimental si el objetivo es medir la identidad del personaje; de lo contrario, el resultado quedaría dominado por sexualidad y no por marcador visual.
