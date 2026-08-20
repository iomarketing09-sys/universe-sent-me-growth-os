---
title: "Segunda capa de afiliación para posts ganadores"
purpose: "Definir un experimento separado para agregar productos afiliados de Mercado Libre a publicaciones de Facebook que ya demostraron rendimiento orgánico, sin confundir monetización con aprendizaje editorial ni sobrescribir el piloto de 10 oportunidades."
status: "Draft"
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Production/2026-08-19_Playbook_Tracking_Afiliados_MercadoLibre.md"
  - "Operations/Production/2026-08-19_Piloto_Afiliados_Facebook_18_30_Agosto.md"
  - "Operations/Production/12_00_Catalogo_Productos_MercadoLibre.md"
  - "Operations/Research/Affiliate_Link_Ledger.csv"
  - "Operations/Research/Affiliate_Metrics_Snapshots.csv"
  - "Operations/Research/2026-08-20_Cohorte_15_16_Analysis.md"
  - "Operations/Research/2026-08-20_Cohorte_17_30_Actual_Cut.md"
  - "Operations/Research/2026-08-19_P0_Corte_17_Agosto.md"
organization: "Operations/Production"
---

# Segunda capa de afiliación para posts ganadores

## Decisión CGO

Sí conviene crear una segunda capa, pero no como una ampliación automática de los diez links actuales. La segunda capa debe monetizar publicaciones que ya demostraron tracción orgánica, aunque originalmente no hayan sido seleccionadas para el calendario afiliado. Esto convierte el rendimiento editorial en un criterio de selección comercial, pero conserva la separación entre ambos experimentos.

> La publicación debe ganar primero por contenido; el producto se agrega después solo cuando existe un encaje narrativo evidente.

## 1. Separación de capas

| Capa | Función | Selección | Tracking | Estado |
|---|---|---|---|---|
| Capa 1: piloto 18–30 | Probar 10 oportunidades planeadas con producto desde el calendario | Selección previa a publicación | `USM-AFF-FB20260818-30-P01` | Activa |
| Capa 2: posts ganadores | Monetizar publicaciones que superan una señal orgánica y tienen producto natural | Selección posterior a publicación | `USM-AFF-FB-WINNERS-202608` | Draft |

La Capa 2 no debe cambiar los horarios, el copy, el asset ni el veredicto de P0. Si Facebook permite adjuntar un producto después de publicar, la fecha/hora de adjunción debe conservarse aparte de la fecha de publicación.

## 2. Candidatos iniciales

Los candidatos se priorizan por rendimiento observado, no se convierten automáticamente en reglas editoriales:

| Candidato | Evidencia observada | Razón para revisión comercial | Decisión inicial |
|---|---:|---|---|
| `2608028` — Universe, “El amor está en todos lados” | 636 interacciones; 172 compartidos; 81.0% de P0 | Alto alcance de compartición y escenario fantástico | Revisar encaje de producto; no adjuntar todavía |
| `2608029` — Wilfred, “Quiero loquiar” | 335 interacciones; 100 compartidos; 45.8% de cohorte 17–30 | Gancho coloquial, personaje reconocible y alta compartibilidad | Revisar encaje de producto; no adjuntar todavía |
| `CNT-034 / 260539` — Evan + Kiri | 227 interacciones; 52 compartidos; líder de cohorte 15–16 | Composición de personajes y fantasía romántica con fuerte potencial de compartir | Revisar encaje de producto; no adjuntar todavía |

Estos tres son **candidatos de revisión**, no publicaciones aprobadas para adjunción. La primera ola de Capa 2 debe elegir como máximo tres y conservar al menos un post ganador sin producto como control descriptivo.

## 3. Gate de elegibilidad

Una publicación solo puede pasar a Capa 2 si cumple los cinco gates siguientes:

| Gate | Regla operativa |
|---|---|
| Rendimiento relativo | Estar en el grupo superior de su cohorte o alcanzar aproximadamente 2× la mediana comparable; el outlier debe registrarse como hipótesis, no como regla universal. |
| Compartibilidad | Tener compartidos observables y una señal de shareability igual o superior a la mediana de su cohorte cuando el dato exista. |
| Historia primero | La publicación debe funcionar como meme o historia aunque se retire el producto. |
| Encaje de producto | El producto debe relacionarse naturalmente con personaje, escena o remate y superar el filtro de historia, personaje, potencial visual, ticket impulsivo y demanda. |
| Control y aprobación | Debe existir una fila nueva de ledger, una etiqueta nueva y aprobación humana explícita antes de adjuntar. |

La capa no debe monetizar un post ganador únicamente porque tenga muchas interacciones. Si el producto se siente aleatorio, se conserva el rendimiento editorial sin añadir afiliación.

## 4. Selección de productos

La búsqueda debe comenzar por el catálogo de productos y después verificarse en la Central de Afiliados. No se asigna un producto concreto a `2608028`, `2608029` o `260539` hasta revisar visualmente el encaje.

El filtro recomendado es: historia primero; personaje natural; potencial visual; ticket impulsivo; y demanda vigente. Cada post recibe como máximo un producto. No se debe adjuntar el mismo producto al post ganador y a otro post de la Capa 2 usando la misma etiqueta.

Los productos del piloto de Capa 1 no se reutilizan automáticamente en Capa 2. Si el mismo producto es narrativamente correcto para dos superficies, cada superficie debe recibir un link y una etiqueta distintos.

## 5. Tracking independiente

La campaña de Capa 2 será `USM-AFF-FB-WINNERS-202608`. Cada fila nueva conservará:

```text
Campaign_ID: USM-AFF-FB-WINNERS-202608
Link_ID: L2-FB-<Content_ID>-<secuencia>
ML_Tag: usmfbw<Content_ID><fecha>
Content_ID: <Meta o CNT ID>
Surface: FACEBOOK_NATIVE_PRODUCT o POST_COMMENT
Product_Key: <producto verificado>
```

El `Campaign_ID` será la marca de capa. No se sobrescriben los diez registros de `USM-AFF-FB20260818-30-P01`, y los snapshots de Capa 2 se agregan al mismo `Affiliate_Metrics_Snapshots.csv` con su campaña independiente.

La opción preferida sigue siendo `FACEBOOK_NATIVE_PRODUCT`. Si el flujo nativo no está disponible, un comentario aprobado debe utilizar una etiqueta y un link propios; nunca se reutiliza el link nativo del post ni se coloca el mismo producto en copy y comentario durante la misma prueba.

## 6. Diseño de la primera ola

La primera ola de Capa 2 debe tener tres candidatos como máximo, con dos adjunciones aprobadas y un control sin producto cuando el encaje de producto no sea claro. Esta estructura limita el riesgo de saturar publicaciones ganadoras y permite comparar monetización con una superficie editorial todavía natural.

Antes de adjuntar, se conserva un snapshot de interacciones orgánicas actual. Después de adjuntar se registran cortes afiliados a 24 horas, 48 horas y 7 días. Se guardan clics, unidades, ventas brutas, ventas aprobadas, comisión estimada y comisión confirmada. Si una etiqueta no aparece en el panel, se registra `Not_Visible_No_Inference`.

No se modifica el contenido que convirtió al post en ganador. La variable de Capa 2 es la presencia del producto y su superficie de tracking, no un nuevo caption, una nueva imagen o una republicación.

## 7. Regla de expansión

No se amplía la capa después de un solo clic o una sola venta. La expansión requiere varios links comparables, al menos dos productos con encaje claro y evidencia de que la adjunción no produce una caída editorial anómala. El resultado de Capa 2 se reporta separado de P0, P1 y de la mediana general de publicaciones.

## Documentos que requerirán actualización al activar la capa

Cuando Fernando apruebe candidatos y productos concretos, deberán actualizarse `Affiliate_Link_Ledger.csv`, `Affiliate_Metrics_Snapshots.csv`, `Affiliate_Pilot_Assignments.csv` si se reutiliza su estructura para la nueva campaña, el changelog y este documento de Draft a Active. No se debe adjuntar ningún producto mientras la fila, la etiqueta y la aprobación no estén registradas.

---
