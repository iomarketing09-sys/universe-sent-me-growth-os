---
title: "Piloto de afiliación Facebook 18–30 de agosto"
purpose: "Definir una prueba comercial pequeña y trazable para insertar enlaces de Mercado Libre en publicaciones seleccionadas de Facebook sin alterar el experimento P0 ni mezclar métricas editoriales y comerciales."
status: "Review"
created: 2026-08-19
updated: 2026-08-19
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Production/2026-08-19_Playbook_Tracking_Afiliados_MercadoLibre.md"
  - "Operations/Research/Affiliate_Link_Ledger.csv"
  - "Operations/Research/Affiliate_Metrics_Snapshots.csv"
  - "GrowthOS/11_00_Estrategia_Monetizacion_MercadoLibre.md"
  - "Operations/Research/2026-08-19_MercadoLibre_Facebook_Afiliados_Observacion.md"
organization: "Operations/Production"
---

# Piloto de afiliación Facebook 18–30 de agosto

## Recomendación CGO

Sí conviene probar enlaces en algunas publicaciones del 18 al 30, porque ya existe una señal agregada de monetización de Facebook: 3 clics, 2 unidades vendidas y $28.84 MXN de comisión estimada durante el corte observado. Sin embargo, no conviene insertar enlaces en toda la ola. La prueba debe ser pequeña, editorialmente natural y separada del P0 de frecuencia, contenido nuevo/reuse y mediana de interacciones.

La recomendación es seleccionar **entre cuatro y seis publicaciones**, con un máximo de un producto y un enlace por publicación. El resto de la ola funciona como grupo sin enlace; no es un grupo experimental perfecto, pero permite observar si el enlace aparece asociado a una caída inusual de interacciones o comentarios.

## Criterios de selección

Una publicación entra al piloto solo si cumple estas condiciones:

| Criterio | Regla |
|---|---|
| Encaje editorial | El producto debe tener relación clara con la escena, personaje o remate; no insertar productos aleatorios. |
| Formato | Priorizar imágenes o memes donde el comentario pueda continuar el chiste; no usar todos los Reels. |
| Intención | El contenido debe permitir una recomendación natural o un CTA aprobado. |
| Producto | Debe existir URL/ID de Mercado Libre y categoría elegible confirmada. |
| Trazabilidad | Debe existir fila de ledger antes de publicar. |
| Control | Máximo una etiqueta y un producto por publicación. |
| Aprobación | El texto del enlace y el comentario requieren aprobación humana antes de publicarse. |

El piloto no debe cambiar el horario ni la frecuencia del calendario 18–30. Si una publicación no tiene un producto que encaje de manera evidente, se deja sin enlace. La monetización no debe convertirse en una excusa para degradar la coherencia editorial.

## Diseño de la prueba

El identificador de campaña será `USM-AFF-FB-20260818-30-P01`. Cada publicación elegida tendrá un `Content_ID` interno, un `Meta_Post_ID` después de publicar, un producto de Mercado Libre y una etiqueta exclusiva.

Para no volver a perder la granularidad, cada publicación debe usar **un link por producto y por post**. Si el link aparece en el copy, la superficie será `POST_COPY`; si aparece en un comentario aprobado, será `POST_COMMENT`. No se usará el mismo link en ambas superficies durante este primer piloto.

El piloto puede usar dos variantes, pero no deben mezclarse:

| Variante | Uso recomendado |
|---|---|
| `POST_COMMENT` | Primera opción para mantener el copy principal limpio y continuar el humor en el comentario. |
| `POST_COPY` | Solo cuando el producto es parte explícita del contenido o el CTA debe ser visible desde la publicación. |

Para la primera ola recomiendo empezar con comentarios aprobados, uno por publicación, porque permiten mantener separados el remate editorial y el registro comercial. Esto no afirma que el comentario tenga mejor rendimiento; simplemente reduce el cambio visual en el contenido principal.

## Nomenclatura

Se utilizarán tres identificadores relacionados:

| Identificador | Ejemplo | Función |
|---|---|---|
| `Campaign_ID` | `USM-AFF-FB-20260818-30-P01` | Agrupa toda la prueba. |
| `Link_ID` | `AFF-FB-20260819-001` | Identifica de forma única el link generado. |
| `ML_Tag` | `USM_FB_CMT_260661_P01_AUG26` | Etiqueta visible en Mercado Libre para medir ese link. |

La etiqueta no debe depender del nombre largo del producto. El producto completo, el ID de Mercado Libre y la URL deben vivir en el ledger. La etiqueta solo necesita ser corta, única y legible.

Ejemplo de registro:

```text
Campaign_ID: USM-AFF-FB-20260818-30-P01
Link_ID: AFF-FB-20260819-001
ML_Tag: USM_FB_CMT_260661_P01_AUG26
Content_ID: 260661
Product_Key: ML-PROD-01
Surface: POST_COMMENT
```

## Registro obligatorio

`Affiliate_Link_Ledger.csv` conserva la identidad del link y no debe sobrescribirse cuando cambien las métricas. Cada fila debe incluir campaña, link, etiqueta, asset, Meta Post ID, superficie, producto, CTA, URL, aprobación y estado de publicación.

`Affiliate_Metrics_Snapshots.csv` conserva una fila por link y por fecha de corte. Ahí se registran clics, ventas brutas, ventas aprobadas, unidades, ingreso, comisión estimada, comisión confirmada y fuente. De esa forma se puede comparar el corte del día 1 con el del día 7 sin perder el histórico.

## Cadencia de medición

Mercado Libre actualiza sus métricas cada 24 horas. Para optimizar esfuerzo, la revisión operativa puede hacerse cada dos días, pero cada revisión debe guardar el corte visible. La primera lectura se realiza 24 horas después de publicar el link; la segunda, al cierre de siete días; la comisión confirmada se revisa posteriormente, respetando el periodo de validación de Mercado Libre.

No se deben mezclar las métricas afiliadas con `Interacciones_24h`, `Interacciones_72h` ni con el veredicto P0. El resultado comercial será un experimento paralelo con sus propias métricas: `Clicks`, `Approved_Sales`, `Conversion_Rate`, `Commission_MXN` y `Confirmed_Commission_MXN`.

## Veredicto esperado

El piloto no busca demostrar que un meme vende por sí solo. Busca responder tres preguntas concretas: si la audiencia hace clic cuando el producto encaja con el contenido; si una etiqueta por publicación permite identificar el origen de las ventas; y si el enlace genera ventas aprobadas después de la ventana de atribución.

Si hay clics sin ventas, se revisa el producto, el CTA y el encaje. Si hay ventas bajo una etiqueta específica, se puede repetir el patrón. Si no hay clics, no se concluye que Facebook no monetiza: se revisa el copy, la superficie y el producto. Solo se toma una decisión después de varios links comparables.
