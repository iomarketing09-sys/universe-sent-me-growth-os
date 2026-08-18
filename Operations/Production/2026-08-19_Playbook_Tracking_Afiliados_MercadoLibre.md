---
title: "Playbook de tracking de afiliados Mercado Libre"
purpose: "Definir una configuración reproducible para atribuir enlaces, clics, ventas y comisiones de Mercado Libre a publicaciones concretas de Universe Sent Me."
status: "Review"
created: 2026-08-19
updated: 2026-08-19
version: "1.0"
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

`Link_ID`, `ML_Link_or_ID`, `ML_Tag`, `Platform`, `Surface`, `Content_ID`, `Meta_Post_ID`, `Reel_ID`, `Character`, `Product_ID`, `Product_Title`, `CTA`, `Created_Local`, `Published_Local`, `Status`, `Clicks`, `Gross_Sales`, `Approved_Sales`, `Units_Sold`, `Revenue_MXN`, `Commission_MXN`, `Confirmed_Commission_MXN`, `Last_Click_At`, `Metrics_Cutoff_Local`, `Source`, `Notes`.

## Reglas de control

No usar UTM como sustituto del tracking nativo de Mercado Libre. UTM puede servir para un sitio propio, pero no es la fuente de atribución de ventas dentro del marketplace.

No comprar mediante los propios enlaces. No colocar links en grupos privados o superficies no declaradas. No impulsar los links con publicidad pagada hasta revisar las restricciones del programa. Mercado Libre señala expresamente restricciones sobre compras personales, promociones inadecuadas y publicidad pagada [4].

No declarar ROI, conversión o comisión cuando solo existen clics. La fórmula de conversión del ledger será:

`Conversion_Rate = Approved_Sales / Clicks`

Si los clics son cero, el valor debe quedar vacío y no ser `0%`. El RPM afiliado será:

`Affiliate_RPM = Confirmed_Commission_MXN / (Clicks / 1000)`

y solo se calculará cuando haya comisión confirmada y clics registrados.

## Primer piloto recomendado

El primer piloto debe usar el Reel de la lámpara de luna de Elara, porque ya existe una pieza con CTA `LUNA`. La prueba debe crear una etiqueta única para el Reel y otra para cualquier comentario aprobado que contenga el link. No se deben utilizar todavía listas genéricas ni el mismo link en todas las publicaciones.

El piloto debe durar al menos siete días de medición de clics y debe conservar los cortes diarios. Las ventas y comisiones se revisarán después, respetando la ventana de atribución de 24 horas y el periodo de validación de Mercado Libre.

## Referencias

[1]: https://www.mercadolibre.com.mx/l/primerospasos-recorre-la-central-de-afiliados "Central de Afiliados y Creadores — Mercado Libre México"

[2]: https://www.mercadolibre.com.mx/l/como-se-calculan-tus-ganancias "Cálculo de Ganancias — Mercado Libre México"

[3]: https://www.mercadolibre.com.mx/l/haz-un-seguimiento-de-tus-metricas "Métricas del Afiliado — Mercado Libre México"

[4]: https://www.mercadolibre.com.mx/l/preguntas-frecuentes-afiliados "Preguntas Frecuentes — Mercado Libre México"
