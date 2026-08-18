---
title: "Hipótesis de archivo fundacional para los casos de junio sin match"
purpose: "Definir por qué los casos sin Asset_Ref no deben descartarse y cómo reconstruir su relación histórica con Meta, Drive y la evolución visual de Universe."
status: "Review"
created: 2026-08-18
updated: 2026-08-18
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-17_Reporte_Final_Recopilacion_Junio.md"
  - "Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv"
  - "Operations/Research/Historical_Performance_Individuals.csv"
  - "Operations/Research/2026-08-17_Indice_Visual_Junio_Cierre.md"
  - "Operations/Research/2026-08-18_Junio_Lote_Priorizado_Difusion.md"
  - "GrowthOS/Content_Inventory.csv"
organization: "Operations/Research"
---

# Hipótesis de archivo fundacional para los casos sin match

## Hipótesis de trabajo

Los 58 registros de junio marcados como `Needs_Asset_Match` no deben interpretarse como contenido irrelevante o defectuoso. Representan una capa histórica de publicaciones con datos reales de Meta y valor editorial observable, independientemente de cuándo o dónde se creó cada asset. El Growth OS los utilizará por su rendimiento, formato, humor, personajes visibles y potencial de aprendizaje, sin intentar reconstruir su origen temporal.

La hipótesis no requiere clasificar los casos por mes de creación. Todos se tratarán como publicaciones históricas observables de junio y se analizarán por el valor que aportan al Growth OS.

La fecha de publicación en junio solo se utilizará como fecha de observación de rendimiento. No se inferirá una fecha de creación del asset ni se clasificará la pieza como reuse de otro mes salvo que exista evidencia ya documentada y necesaria para una decisión operativa.

## Qué evidencia conservan

Los 58 registros sí conservan, en distinto grado, `facebook_photo_id`, `meta_publication_id`, fecha local, caption y métricas históricas. Por tanto, pueden estudiarse como publicaciones reales aunque falte el archivo creativo. El primer filtro de valor debe ser shares, interacciones y comentarios, no la presencia de un personaje canónico.

## Protocolo de utilización histórica

Primero se ordenarán los 58 casos por shares e interacciones. Después se utilizarán los objetos multimedia y las imágenes de Meta para recuperar la evidencia visual disponible. Cada caso se enriquecerá con formato, composición, personajes observables, rol narrativo, tipo de humor, potencial de etiquetado y señales de conversación. Los casos sin coincidencia de asset permanecerán como `Historical_Unmatched`, pero seguirán siendo válidos para análisis de rendimiento y aprendizaje. No se hará rastreo de origen en otras carpetas o meses.

Cuando exista evidencia visual suficiente, el registro conservará la fecha de publicación en Meta, el nivel de confianza de la observación y los campos editoriales disponibles. No se añadirá una fecha de creación inferida. La ausencia de personajes de la Biblia no será motivo de descarte; se registrará como `Personaje_No_Canonico`, `Humano_No_Identificado` o `Sin_Personaje_Visible` según la evidencia.

## Criterio de integración

Un caso podrá integrarse al histórico individual cuando tenga Meta ID y evidencia de publicación. Podrá recibir Asset_Ref confirmado cuando exista una coincidencia visual o de Drive suficientemente sólida. Solo podrá recibir CNT cuando, además, tenga valor operativo para reuse o aprendizaje y exista aprobación editorial. Ningún hallazgo de rendimiento modificará el canon por sí solo.

## Hallazgos del primer lote

El top 15 recuperado desde Meta confirmó que la cola contiene varias señales de formación de Universe: Universe/gato con gafas, Wilfred/gnomo, Ganso, hadas, tarot, escenarios cósmicos y una mezcla de fotografía real con ilustración. El caso `122125544019072582` muestra a Wilfred en un bosque; `122127916017072582` combina hada, Wilfred, tarot y territorio esotérico; `122134608507072582` muestra a Ganso con traje; y `122130196011072582` muestra a Universe en una versión muscular absurda.

Los 15 casos recuperados desde Meta se tratarán como publicaciones históricas válidas aunque no exista una coincidencia de asset en Drive. La ausencia de `Asset_Ref` limita la integración del archivo creativo, pero no invalida las métricas, la revisión visual ni el aprendizaje editorial.

## Prioridad

La prioridad inicial será analizar el cuartil superior por shares e interacciones y los casos que aporten señales claras sobre personajes, formato, humor o conversación. El primer lote detallado ya está compuesto por `122127916017072582`, `122134608507072582`, `122130196011072582`, `122129404893072582` y `122125544019072582`. El siguiente paso será convertir sus señales en aprendizajes comparables del Growth OS y ampliar el análisis al resto de la cola solo cuando exista una pregunta concreta.
