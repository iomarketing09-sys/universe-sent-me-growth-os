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

Los 58 registros de junio marcados como `Needs_Asset_Match` no deben interpretarse como contenido irrelevante o defectuoso. Es plausible que representen una capa temprana del archivo creativo que impulsó la página antes de que se consolidaran los personajes, la estética de animación, los escenarios y la nomenclatura de Universe.

La hipótesis distingue tres etapas, sin asumirlas como hechos hasta recuperar evidencia:

| Etapa | Posible función histórica |
|---|---|
| Marzo–abril | Memes fundacionales o experimentos iniciales que ayudaron a descubrir el tono y la respuesta de audiencia |
| Mayo | Consolidación de una identidad visual más consistente y comienzo de la reutilización organizada |
| Junio | Expansión de la frecuencia y mezcla de memes que alimentaron el crecimiento, incluyendo piezas aún no enlazadas a Drive |

La fecha de publicación en junio no implica que el asset haya sido creado en junio. Un post de junio puede ser un reuse de marzo, abril o mayo, o una pieza que quedó fuera de la organización mensual.

## Qué evidencia conservan

Los 58 registros sí conservan, en distinto grado, `facebook_photo_id`, `meta_publication_id`, fecha local, caption y métricas históricas. Por tanto, pueden estudiarse como publicaciones reales aunque falte el archivo creativo. El primer filtro de valor debe ser shares, interacciones y comentarios, no la presencia de un personaje canónico.

## Protocolo de reconstrucción

Primero se ordenarán los 58 casos por shares y por interacciones. Después se consultarán los objetos multimedia y las imágenes de Meta para recuperar la evidencia visual. Los candidatos se cruzarán contra los índices de Drive de marzo, abril, mayo y junio mediante perceptual hash, dimensiones, filename parcial, caption y similitud visual. Los casos sin coincidencia permanecerán como `Historical_Unmatched`, no se convertirán en CNT automáticamente.

Cuando exista coincidencia visual suficiente, el registro conservará tres capas separadas: fecha de publicación en Meta, posible fecha o carpeta de creación del asset y nivel de confianza de la relación. La ausencia de personajes de la Biblia no será motivo de descarte; se registrará como `Personaje_No_Canonico`, `Humano_No_Identificado` o `Sin_Personaje_Visible` según la evidencia.

## Criterio de integración

Un caso podrá integrarse al histórico individual cuando tenga Meta ID y evidencia de publicación. Podrá recibir Asset_Ref confirmado cuando exista una coincidencia visual o de Drive suficientemente sólida. Solo podrá recibir CNT cuando, además, tenga valor operativo para reuse o aprendizaje y exista aprobación editorial. Ningún hallazgo de rendimiento modificará el canon por sí solo.

## Hallazgos del primer lote

El top 15 recuperado desde Meta confirmó que la cola contiene varias señales de formación de Universe: Universe/gato con gafas, Wilfred/gnomo, Ganso, hadas, tarot, escenarios cósmicos y una mezcla de fotografía real con ilustración. El caso `122125544019072582` muestra a Wilfred en un bosque; `122127916017072582` combina hada, Wilfred, tarot y territorio esotérico; `122134608507072582` muestra a Ganso con traje; y `122130196011072582` muestra a Universe en una versión muscular absurda.

El listado de `05 Mayo` contiene 128 assets y ya utiliza nombres consistentes de personajes como Universe, Wilfred, Fantasma, Kiri, Elara, Maeve y Kael. Sin embargo, los 15 casos fundacionales recuperados desde Meta no tienen todavía coincidencia de filename directa en esa lista. Esto no descarta una relación visual: puede tratarse de assets antiguos con nombres distintos, archivos fuera de la carpeta mensual o publicaciones creadas antes de que se normalizara la nomenclatura.

La evidencia actual sostiene que estos casos son un archivo de evolución creativa, pero **no demuestra todavía que provengan de marzo o abril**. Esa afirmación requiere cruzar imágenes o hashes con las carpetas y publicaciones anteriores.

## Prioridad

La prioridad inicial será reconstruir los casos del cuartil superior por shares y los que tengan personajes o territorios visuales de formación. El orden recomendado es `122127916017072582` (hada/Wilfred/tarot), `122134608507072582` (Ganso), `122130196011072582` (Universe), `122129404893072582` (hada y diálogo) y `122125544019072582` (Wilfred). Después se procesarán las fotografías y memes textuales tempranos si el cruce histórico muestra valor.
