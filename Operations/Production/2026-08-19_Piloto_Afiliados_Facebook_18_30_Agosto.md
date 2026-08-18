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
  - "Operations/Research/Affiliate_Pilot_Assignments.csv"
  - "GrowthOS/11_00_Estrategia_Monetizacion_MercadoLibre.md"
  - "Operations/Research/2026-08-19_MercadoLibre_Facebook_Afiliados_Observacion.md"
organization: "Operations/Production"
---

# Piloto de afiliación Facebook 18–30 de agosto

## Recomendación CGO

Sí conviene probar enlaces en algunas publicaciones del 18 al 30, porque ya existe una señal agregada de monetización de Facebook: 3 clics, 2 unidades vendidas y $28.84 MXN de comisión estimada durante el corte observado. Sin embargo, no conviene insertar enlaces en toda la ola. La prueba debe ser pequeña, editorialmente natural y separada del P0 de frecuencia, contenido nuevo/reuse y mediana de interacciones.

La recomendación queda ajustada a **10 publicaciones**, con un máximo de un producto afiliado por publicación. El resto de la ola funciona como grupo sin enlace; no es un grupo experimental perfecto, pero permite observar si el enlace aparece asociado a una caída inusual de interacciones o comentarios.

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

El identificador de campaña será `USM-AFF-FB-20260818-30-P01`. Cada una de las 10 publicaciones elegidas tendrá un `Content_ID` interno, un `Meta_Post_ID`, un producto de Mercado Libre, una etiqueta exclusiva y, si Facebook lo expone, un `Native_Product_Attachment_ID`.

Para no volver a perder la granularidad, cada publicación debe usar **un link por producto y por post**. Si el link aparece en el copy, la superficie será `POST_COPY`; si aparece en un comentario aprobado, será `POST_COMMENT`. No se usará el mismo link en ambas superficies durante este primer piloto.

El piloto puede usar dos variantes, pero no deben mezclarse:

| Variante | Uso recomendado |
|---|---|
| `POST_COMMENT` | Primera opción para mantener el copy principal limpio y continuar el humor en el comentario. |
| `POST_COPY` | Solo cuando el producto es parte explícita del contenido o el CTA debe ser visible desde la publicación. |

La primera opción será utilizar el **flujo nativo de Facebook para agregar el producto afiliado a la publicación**, incluso cuando la publicación ya esté programada o publicada, siempre que la interfaz lo permita. Este método debe registrarse con la fecha/hora de adjunción y una evidencia de confirmación. El comentario o copy con link manual queda como alternativa de respaldo, no como opción principal.

Si Facebook no permite el flujo nativo en una candidata, se podrá usar un comentario aprobado, uno por publicación, con etiqueta y link separados. Esto no afirma que el comentario tenga mejor rendimiento; simplemente conserva el remate editorial y ofrece una alternativa controlada.

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

## Distribución temporal propuesta

La selección se distribuye desde el 18 hasta el 30 de agosto para evitar concentrar todas las oportunidades en los últimos cuatro días. Se eligieron slots con assets identificados en el calendario maestro y se dejó pendiente la búsqueda del producto hasta validar visualmente el encaje en el navegador.

| Oportunidad | Fecha | Hora | Asset del calendario | Personaje/identidad visible | Superficie prevista | Producto |
|---:|---|---:|---|---|---|---|
| AFF-01 | 18 ago | 17:00 | `260644 - Universe.png` | Universe | `FACEBOOK_NATIVE_PRODUCT` | Pendiente de búsqueda |
| AFF-02 | 19 ago | 13:30 | `260560 - Fantasma.png` | Fantasma | `FACEBOOK_NATIVE_PRODUCT` | Pendiente de búsqueda |
| AFF-03 | 20 ago | 13:30 | `260659 - Universe.png` | Universe | `FACEBOOK_NATIVE_PRODUCT` | Pendiente de búsqueda |
| AFF-04 | 21 ago | 11:00 | `260635 - Universe.png` | Universe | `FACEBOOK_NATIVE_PRODUCT` | Pendiente de búsqueda |
| AFF-05 | 22 ago | 19:00 | `260510 - Universe.png` | Universe / contexto nocturno | `FACEBOOK_NATIVE_PRODUCT` | Pendiente de búsqueda |
| AFF-06 | 24 ago | 10:00 | `260518 - Kael.png` | Kael | `FACEBOOK_NATIVE_PRODUCT` | Pendiente de búsqueda |
| AFF-07 | 26 ago | 13:30 | `260540 - Elara.png` | Elara | `FACEBOOK_NATIVE_PRODUCT` | Pendiente de búsqueda |
| AFF-08 | 28 ago | 13:30 | `260590 - Maeve.png` | Maeve | `FACEBOOK_NATIVE_PRODUCT` | Pendiente de búsqueda |
| AFF-09 | 29 ago | 10:00 | `741 - Elara+Maeve.png` | Elara + Maeve | `FACEBOOK_NATIVE_PRODUCT` | Pendiente de búsqueda |
| AFF-10 | 30 ago | 22:00 | `260528 - Universe.png` | Universe / noche | `FACEBOOK_NATIVE_PRODUCT` | Pendiente de búsqueda |

Se dejan libres los días 23, 25 y 27 para no sobrecargar la primera prueba y para conservar publicaciones sin afiliación como referencia operativa. La distribución no cambia la programación ni añade contenido; solo define dónde se intentará adjuntar un producto después de la aprobación.

La publicación del 18 es el primer candidato, como solicitó Fernando. Las URLs, etiquetas y productos se buscarán después de validar esta lista y el encaje visual de cada asset. Ningún enlace ha sido creado o adjuntado en esta fase.
