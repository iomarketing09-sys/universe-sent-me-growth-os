---
title: "Hallazgos visuales — expansión de celdas comparables, corte 01"
purpose: "Conservar la evidencia visual utilizada para promover o excluir candidatos de las celdas comparables de narrativa y humor."
status: Draft
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv"
  - "Operations/Research/2026-08-20_Propuesta_Expansion_Celdas_Comparables.md"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
organization: "Operations/Research"
---

# Hallazgos visuales — expansión de celdas comparables, corte 01

## Alcance

La revisión utilizó la hoja de contacto `2026-08-20_Expansion_Candidate_Contact_Sheet.jpg` y revisiones detalladas de los assets locales `2607787`, `2607816` y `2607828`. Estos hallazgos son de trabajo y no modifican el canon.

## Casos revisados

El caso `2607787` presenta una conversación visual clara entre Fantasma y Universe: dos globos de diálogo, turnos diferenciados y un remate ácido directo (“Eres muy callado” / “Gracias, intenté hablar varias veces, pero no cerrabas el hocico”). Es un candidato válido para **diálogo ácido**, no para microhistoria secuencial de tres tiempos. Universe conserva sus gafas redondas y el Fantasma oculta la mirada con gafas oscuras; la revisión visual es necesaria para distinguirlos. La fila se promovió a `Current_Comparable` en `DIA-002`.

`2607816` es un caso visualmente limpio de **observacional social/ácido**: Universe aparece sentado con gafas y el texto “Somos una sociedad de pecadores, juzgando a otros por pecar diferente a nosotros”. Es una observación social de una sola lectura, no una conversación ni autodesprecio. Se promovió a `Current_Comparable` en `OBS-004`, con nota de que combina tono moral/ácido y composición textual mínima.

`2607828` no es autodesprecio directo. La imagen muestra a Ganso siendo vestido con una camisa y el remate “Ya entendí la vida banda, yo soy el villano”. La función se describe mejor como **autopercepción absurda / identidad de antihéroe**. Se añadió como `SELF-005`, candidato de contraste para la celda autodesprecio/antihéroe, pero no se mezclará automáticamente con insulto/autodesprecio.

## Exclusiones y límites

`260731`, `260765` y `260775` son composiciones relacionales/sexuales sin evidencia suficiente de diálogo ácido. `260766` es una composición dividida de Universe ángel/demonio y no debe contarse como transformación corporal/material sin una definición más precisa. `2607837` y `2607823` son insinuación o infografía sexual, no humor ácido ni autodesprecio por defecto. `2607780` es Wilfred con remate textual ácido, pero no autodesprecio/antihéroe sin codificar la función del remate.

Los casos `260740`, `2607816`, `2607824` y `260552` son piezas de Universe con texto observacional, social o autorreflexivo. `260740` requiere cautela por sensibilidad diagnóstica; `2607816` es el candidato más limpio para observacional social; `2607824` es autoafirmación relacional; `260552` es observacional/ácido con remate sobre vulnerabilidad. Solo `2607816` fue promovido en este corte.

Existe una discrepancia de identificación que debe preservarse: el archivo local revisado se llama `2607828`, mientras que la fila histórica consolidada asociada al mismo Meta ID `1036844829507460_122134169481072582` registra `asset_ref=2607833`. Por seguridad, el `Meta_ID` funciona como clave primaria del candidato y la discrepancia queda abierta; no se renombra ni se crea CNT.

## Regla de captions

La revisión visual no permite inferir el tratamiento de caption de la publicación histórica. Los casos promovidos conservan `Caption_Treatment=Needs_Reconstruction` hasta recuperar un copy verificable. El texto dentro de la imagen no se utiliza como sustituto del caption publicado.

## Hallazgos de sensibilidad y observación adicional

`260740` es un caso de observación oscura con Universe y una infografía que usa términos de salud mental (“Psicosis”, “Paranoia”, “Esquizofrenia”, “Depresión”) como remates humorísticos. Aunque puede ser una observación social de alto rendimiento, su sensibilidad contextual es demasiado específica para incorporarla automáticamente a la celda observacional principal. Se mantiene como `Candidate_Review` y requiere una decisión editorial separada; no debe utilizarse como ejemplo genérico de humor observacional.

`260552` muestra a Universe con gafas y cuchillo, acompañado del remate “Hasta el alma más comprensiva necesita ser mierdilla de vez en cuando”. Es un caso claro de **humor ácido/autodepreciación o agresividad absurda**, pero la imagen introduce un arma como recurso visual. Puede servir como contraste de función, aunque no debe añadirse a la celda autodesprecio/antihéroe sin una revisión de seguridad editorial y sin confirmar si el remate es autodesprecio, agresión o personaje/pose. No se promueve en este corte.

## Revisión de candidatos restantes de autodesprecio/antihéroe

`2607797` muestra a Silvio frente a un espejo: una versión triste y otra sonriente, con el texto “Merecías amor, no manipulación disfrazada de cariño”. La función es **autocuidado/recuperación relacional**, no autodesprecio ni antihéroe. Se mantiene fuera de la celda principal; puede servir para una futura celda de autocuidado irónico o contraste relacional.

`2607795` muestra a un humano, una figura joven y Wilfred sentados en un sofá bajo el texto “Yo, mi ansiedad y mi guía espiritual intentando entender el universo”. La función es **ansiedad relacional/escena coral**, no autodesprecio ni antihéroe. Se mantiene como contraste y no se promueve a `Current_Comparable`.

El candidato `2607828`/Meta ID `1036844829507460_122134169481072582` sigue siendo el único de estos casos que puede aportar una variante de **autopercepción absurda/antihéroe**, aunque no es autodesprecio directo. La celda todavía necesita al menos un caso comparable adicional para una señal preliminar.
