---
title: "Playbook de tracking de afiliados Mercado Libre"
purpose: "Definir una configuración reproducible para atribuir enlaces, clics, ventas y comisiones de Mercado Libre a publicaciones concretas de Universe Sent Me."
status: "Review"
created: 2026-08-19
updated: 2026-08-18
version: "1.3"
author: "Manus AI (CGO)"
related_documents:
  - "GrowthOS/11_00_Estrategia_Monetizacion_MercadoLibre.md"
  - "Operations/Research/2026-08-19_Auditoria_Reels_y_Monetizacion.md"
  - "Operations/Research/Affiliate_Link_Ledger.csv"
  - "GrowthOS/07_00_Registro_Maestro_Reels.md"
organization: "Operations/Production"
---

# Playbook de tracking de afiliados Mercado Libre

## Principio de atribución

Mercado Libre ya ofrece el mecanismo principal de atribución: un link o ID de afiliado con una etiqueta. La Central de Afiliados y Creadores permite generar links, administrar etiquetas y medir su rendimiento [1]. La atribución de venta depende del último clic válido y de una ventana de 24 horas; la compra puede ser del producto recomendado o de otro producto elegible [2].

El tracking propio de Universe Sent Me no debe intentar reemplazar la atribución de Mercado Libre. Debe responder una pregunta diferente: **qué publicación, canal, personaje o CTA generó el enlace que luego aparece en los reportes de afiliado**.

## Arquitectura recomendada

La configuración mínima tiene cuatro capas:

| Capa | Función | Fuente de verdad |
|---|---|---|
| Link de Mercado Libre | Generar el enlace afiliado y su etiqueta | Central de Afiliados y Creadores |
| Registro editorial | Relacionar el link con Reel, post, comentario o campaña | `Affiliate_Link_Ledger.csv` |
| Clics y ventas | Consultar clics, ventas brutas, ventas aprobadas, productos e ingresos | Panel Métricas de Mercado Libre |
| Conciliación | Comparar lo publicado con el reporte de Mercado Libre cada 24 horas y después del periodo de revisión | Ledger + exportación del panel |

No se recomienda introducir primero un acortador externo ni una redirección propia. Añadir una capa intermedia puede romper la atribución, ocultar el dominio de destino o violar las reglas del programa. Primero deben usarse las etiquetas nativas de Mercado Libre.

## Verificación operativa del generador

La Central de Afiliados y Creadores fue verificada en sesión autenticada. El generador recibe una o más URLs normales de páginas de producto, permite seleccionar una etiqueta administrada por la cuenta y devuelve un link afiliado corto o completo. La URL normal del producto nunca debe registrarse como `ML_Link_or_ID` ni compartirse como si fuera el enlace afiliado.

Mercado Libre rechazó una etiqueta con mayúsculas; para este piloto se usarán únicamente etiquetas en minúsculas y números, sin espacios ni caracteres especiales. El primer link generado fue `https://meli.la/2zCoRix`, asociado a `usmfb2606440818`; quedó registrado como pendiente de adjunción nativa y no fue publicado.

## Convención de etiquetas

Cada etiqueta debe ser corta, estable y legible:

`USM_<CANAL>_<FORMATO>_<ASSET>_<MES>`

Ejemplos:

| Caso | Etiqueta |
|---|---|
| Reel de la lámpara de luna | `USM_FB_REEL_2608034_202608` |
| Comentario aprobado sobre ese Reel | `USM_FB_COM_2608034_202608` |
| Historia de Instagram | `USM_IG_STORY_2608034_202608` |
| Lista de productos de Wilfred | `USM_ML_LIST_WILFRED_202608` |

Debe existir **un link etiquetado por unidad de decisión**. Si el mismo producto aparece en un Reel y en un comentario, usar links o IDs etiquetados por separado cuando Mercado Libre lo permita. De lo contrario, se perderá la comparación entre superficies.

## Flujo operativo

### Flujo preferido: adjuntar el producto desde Facebook

Cuando Facebook permita agregar un producto afiliado desde el catálogo de Mercado Libre a una publicación ya publicada, ese flujo será la primera opción para el piloto. La publicación debe quedar identificada en el ledger antes de adjuntar el producto; después se registra el producto seleccionado, la fecha/hora de adjunción, la URL o ID que Facebook devuelva y una captura de confirmación. El enlace no se considera operativo hasta que la interfaz muestre que el producto quedó adjunto.

Este flujo se registra con `Surface=FACEBOOK_NATIVE_PRODUCT` y requiere, cuando estén disponibles, `Native_Product_Attachment_ID`, `Native_Product_Attached_At`, `Native_Product_URL` y `Native_Product_Status`. Si Facebook no expone un ID propio, se conserva la URL de la publicación, el producto elegido, la etiqueta de Mercado Libre y la evidencia de pantalla.

Como el producto puede agregarse después de publicar, `Published_Local` y `Native_Product_Attached_At` deben ser campos distintos. Nunca se debe tratar la fecha de publicación como fecha de inicio del tracking afiliado.

### Flujo alternativo: link manual aprobado

Si el catálogo nativo no está disponible, se puede usar un comentario o copy con el link generado en Mercado Libre, pero solo después de registrar la fila del ledger y obtener aprobación humana. La superficie será `POST_COMMENT` o `POST_COPY`, nunca `FACEBOOK_NATIVE_PRODUCT`.


### 1. Crear el link

Desde la Central de Afiliados y Creadores, generar el link del producto y agregar la etiqueta correspondiente. Registrar inmediatamente el URL o ID generado en `Affiliate_Link_Ledger.csv`.

### 2. Registrar el contexto editorial

Antes de publicar, completar `Publication_ID` o `Reel_ID`, plataforma, formato, personaje, CTA, fecha planeada y estado de aprobación. El link no debe publicarse si no tiene una fila de ledger y una aprobación humana del contenido.

### 3. Publicar y conservar evidencia

Guardar el permalink de la publicación, el comentario donde se colocó el link y la fecha/hora local de publicación. No responder automáticamente con links. Las respuestas públicas con afiliación requieren aprobación humana.

### 4. Leer las métricas

Mercado Libre indica que la sección Métricas se actualiza cada 24 horas y permite filtrar por etiquetas, consultar clics, ventas, productos, ingresos y ganancias confirmadas [3]. Registrar una captura o exportación por periodo, sin sobrescribir el histórico.

### 5. Conciliar la atribución

La revisión debe distinguir:

| Métrica | Significado |
|---|---|
| Clicks | Interés medido por Mercado Libre sobre el link/ID |
| Ventas brutas | Ventas atribuidas antes de la validación final |
| Ventas aprobadas | Ventas que superaron la revisión correspondiente |
| Ganancias en revisión | Comisión aún sujeta a devoluciones, cancelaciones o validación |
| Ganancias confirmadas | Comisión disponible según las condiciones del programa |

La conciliación diaria no debe marcar una venta como ingreso confirmado. Mercado Libre indica que la venta debe validarse y que el pago puede ocurrir hasta 60 días después, sujeto al mínimo y a las condiciones del programa [3] [4].

## Esquema del ledger

El archivo `Operations/Research/Affiliate_Link_Ledger.csv` debe conservar una fila por link etiquetado. Los campos de rendimiento se actualizan por fecha de corte, no se reemplaza la fila original.

Los campos mínimos son:

`Campaign_ID`, `Link_ID`, `ML_Link_or_ID`, `ML_Tag`, `Platform`, `Surface`, `Content_ID`, `Meta_Post_ID`, `Reel_ID`, `Character`, `Product_Key`, `Product_ID`, `Product_Title`, `Product_URL`, `Native_Product_Attachment_ID`, `Native_Product_Attached_At`, `Native_Product_Status`, `CTA`, `Created_Local`, `Published_Local`, `Approval_Status`, `Publication_Status`, `Status`, `Clicks`, `Gross_Sales`, `Approved_Sales`, `Units_Sold`, `Revenue_MXN`, `Commission_MXN`, `Confirmed_Commission_MXN`, `Last_Click_At`, `Metrics_Cutoff_Local`, `Source`, `Notes`.

La identidad del link se conserva en `Affiliate_Link_Ledger.csv`, una fila por link. La evolución de sus métricas se registra en `Affiliate_Metrics_Snapshots.csv`, una fila por link y fecha de corte. Nunca se reemplaza un snapshot anterior.

Cada etiqueta debe corresponder a una sola combinación `Campaign_ID + Content_ID + Product_Key + Surface`. Si el producto aparece en el copy y en un comentario, se crean links y etiquetas distintas. El nombre agregado `Links de facebook - universesentme` se conserva solo como evidencia histórica y no se reutiliza para nuevas campañas.

## Reglas de control

No usar UTM como sustituto del tracking nativo de Mercado Libre. UTM puede servir para un sitio propio, pero no es la fuente de atribución de ventas dentro del marketplace.

No comprar mediante los propios enlaces. No colocar links en grupos privados o superficies no declaradas. No impulsar los links con publicidad pagada hasta revisar las restricciones del programa. Mercado Libre señala expresamente restricciones sobre compras personales, promociones inadecuadas y publicidad pagada [4].

No declarar ROI, conversión o comisión cuando solo existen clics. La fórmula de conversión del ledger será:

`Conversion_Rate = Approved_Sales / Clicks`

Si los clics son cero, el valor debe quedar vacío y no ser `0%`. El RPM afiliado será:

`Affiliate_RPM = Confirmed_Commission_MXN / (Clicks / 1000)`

y solo se calculará cuando haya comisión confirmada y clics registrados.

## Piloto Facebook 18–30 de agosto

El piloto recomendado para la ola del 18–30 está documentado en `Operations/Production/2026-08-19_Piloto_Afiliados_Facebook_18_30_Agosto.md`. La propuesta aprobada se amplió a diez oportunidades distribuidas desde el 18 de agosto; mantiene sin cambios la frecuencia y el calendario P0, y utiliza como máximo un producto y un link por publicación. La primera opción operativa es `FACEBOOK_NATIVE_PRODUCT`, con aprobación humana antes de adjuntar.

## Estado consolidado de revisión — 18 de agosto de 2026

La revisión del repositorio confirma que el sistema está preparado a nivel de diseño, pero todavía no está operativo para la ola de diez publicaciones de Facebook. En `Affiliate_Pilot_Assignments.csv` existen diez oportunidades, cada una con una etiqueta granular creada (`usmfb2606440818` a `usmfb2605280830`), pero ninguna fila contiene todavía `Product_Key`, `ML_Link_or_ID`, `Native_Product_Attachment_ID` ni un estado de producto adjunto. Por tanto, las etiquetas no deben interpretarse como enlaces afiliados utilizables.

El único enlace afiliado generado que aparece documentado es `https://meli.la/2zCoRix`, asociado a `usmfb2606440818`. El propio registro indica que quedó pendiente de adjunción y que no fue publicado. Además, el ledger conserva un registro histórico agregado de Facebook (`Links de facebook - universesentme`) con 3 clics, 2 unidades vendidas, $322.65 MXN en ventas estimadas y $28.84 MXN de comisión en revisión; ese registro sirve como evidencia histórica, pero no permite atribuir resultados a una publicación concreta.

La conclusión operativa es que **todavía no hay una matriz de links afiliados lista para publicar**. El siguiente paso correcto es completar una fila por oportunidad con URL normal verificada, producto elegido, link corto devuelto por Mercado Libre, etiqueta correspondiente y evidencia de adjunción nativa en Facebook. La aprobación humana debe ocurrir después de verificar el encaje editorial del producto y antes de adjuntarlo o publicarlo.

La documentación relacionada que debe mantenerse sincronizada es `Operations/Research/Affiliate_Pilot_Assignments.csv`, `Operations/Research/Affiliate_Link_Ledger.csv`, `Operations/Research/2026-08-19_MercadoLibre_Facebook_Afiliados_Observacion.md` y `Operations/Production/2026-08-19_Piloto_Afiliados_Facebook_18_30_Agosto.md`. No se requiere crear un documento nuevo porque el hallazgo pertenece al playbook existente y los registros tabulares ya contienen el detalle operativo.

## Primer piloto recomendado

El primer piloto debe usar el Reel de la lámpara de luna de Elara, porque ya existe una pieza con CTA `LUNA`. La prueba debe crear una etiqueta única para el Reel y otra para cualquier comentario aprobado que contenga el link. No se deben utilizar todavía listas genéricas ni el mismo link en todas las publicaciones.

El piloto debe durar al menos siete días de medición de clics y debe conservar los cortes diarios. Las ventas y comisiones se revisarán después, respetando la ventana de atribución de 24 horas y el periodo de validación de Mercado Libre.

## Referencias

[1]: https://www.mercadolibre.com.mx/l/primerospasos-recorre-la-central-de-afiliados "Central de Afiliados y Creadores — Mercado Libre México"

[2]: https://www.mercadolibre.com.mx/l/como-se-calculan-tus-ganancias "Cálculo de Ganancias — Mercado Libre México"

[3]: https://www.mercadolibre.com.mx/l/haz-un-seguimiento-de-tus-metricas "Métricas del Afiliado — Mercado Libre México"

[4]: https://www.mercadolibre.com.mx/l/preguntas-frecuentes-afiliados "Preguntas Frecuentes — Mercado Libre México"
