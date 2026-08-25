---
title: "Inventario de catálogos de Drive — Firma Bordados"
purpose: "Registrar los PDFs autorizados en Drive y los límites comerciales confirmados para el staging de Firma Bordados, conservando origen, tamaño, estado de revisión y reglas prudentes de redacción."
status: Review
created: 2026-08-24
updated: 2026-08-25
version: "1.5"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-23_Guia_Staging_Cloudflare_Pages_Firma_Bordados.md"
  - "Operations/Production/2026-08-23_Evaluacion_Migracion_Wix_Hosting_IA.md"
  - "Operations/Production/2026-08-23_Actualizacion_Movimiento_Staging_Firma_Bordados.md"
organization: "Operations/Production"
---

# Inventario de catálogos de Drive — Firma Bordados

## Propósito operativo

La carpeta Drive autorizada `Catalogos` contiene tres PDFs. Se descargaron copias locales de revisión, sin modificar sus originales, para comprobar metadatos y portadas. Ninguno se ha incorporado todavía al proyecto de staging, a Cloudflare Pages ni al dominio público.

| Archivo en Drive | Tamaño | Páginas | Última modificación en Drive | Portada revisada | Estado |
| :--- | ---: | ---: | :--- | :--- | :--- |
| `CATÁLOGO_BIGBANG_2019.pdf` | 13,569,914 bytes (13.6 MB) | 61 | 2026-08-23 22:49 UTC | BigBang Corporate Apparel; equipo con prendas corporativas | Apto para revisión de versión final |
| `Catalogo MyO 3.pdf` | 3,811,880 bytes (3.8 MB) | 52 | 2025-06-25 22:45 UTC | M&O Playeras; prendas casuales | Apto para revisión de versión final |
| `SOUL&BLUES 2025.pdf` | 7,988,180 bytes (8.0 MB) | 23 | 2025-06-19 03:04 UTC | Soul & Blues Uniformes; prendas de trabajo y vestimenta corporativa | Apto para revisión de versión final |

## Discrepancias detectadas antes de integrar

| Tarjeta actual de staging | Metadato mostrado hoy | Dato confirmado en Drive | Acción requerida |
| :--- | :--- | :--- | :--- |
| BigBang | 13.6 MB | 13.6 MB | Conserva el tamaño al sustituir el enlace |
| Soul & Blues 2025 | 3.8 MB | 8.0 MB | Corregir el tamaño al sustituir el enlace |
| M&O | 5.8 MB | 3.8 MB | Corregir el tamaño al sustituir el enlace |

El nombre de BigBang declara edición 2019 y la portada de M&O declara 2016; Soul & Blues declara 2025. La existencia de una copia en la carpeta autorizada no prueba por sí misma que sea la edición comercial más reciente. Antes de publicar el nuevo sitio, el cliente debe confirmar que los tres son los catálogos vigentes que desea mostrar. Esta confirmación es independiente de la definición aún pendiente de los servicios exactos.

### Confirmación del cliente — 2026-08-24

Fernando confirmó que los tres catálogos son vigentes y están autorizados para el sitio. Se eliminó el bloqueo de vigencia; la siguiente actualización del staging debe sustituir sus enlaces temporales de Wix por copias controladas y ajustar los tamaños a 13.6 MB, 3.8 MB y 8.0 MB respectivamente.

## Oferta comercial confirmada

| Grupo | Servicios o líneas confirmadas | Regla de redacción para el sitio |
| :--- | :--- | :--- |
| Personalización | Digitalización, bordados y serigrafía | Presentar como capacidades de personalización, no como promesa de disponibilidad ilimitada |
| Prendas | Playeras, camisas, uniformes industriales y línea médica | Presentar como categorías de prenda para consulta comercial |
| Límites | No se realizan parches ni gorras | Comunicar de forma discreta como una nota de alcance en la sección de solicitud, no como mensaje dominante |

Los servicios fueron proporcionados por Fernando el 2026-08-24. No se infirieron prestaciones, plazos, precios, materiales, mínimos de pedido ni certificaciones adicionales.

### Condiciones comerciales confirmadas — 2026-08-24

| Tema | Dato confirmado | Regla de redacción para el sitio |
| :--- | :--- | :--- |
| Serigrafía | Mínimo de 12 piezas | Indicar «a partir de 12 piezas» exclusivamente dentro de la capacidad de serigrafía. No extender el mínimo a bordado, digitalización ni prendas. |
| Tiempos de entrega | Varían según el pedido y la carga de trabajo existente | Explicar que se confirman al revisar cantidad, requerimiento y carga de trabajo. No publicar un rango, fecha ni promesa de disponibilidad. |
| Materiales | Pendientes de confirmación | No describir telas, gramajes, composiciones, acabados ni calidades como hechos hasta recibir información del cliente. |

Estas condiciones se integraron al staging Cloudflare el 2026-08-24. La referencia al mínimo no equivale a cotización, disponibilidad garantizada ni capacidad máxima de producción.

### Marcas de prendas confirmadas por catálogo — 2026-08-25

Fernando confirmó que las playeras y uniformes que vende Firma Bordados corresponden a las marcas contenidas en sus catálogos autorizados. Para el sitio, las referencias comerciales confirmadas son **BigBang**, **M&O** y **Soul & Blues**, siempre mediante sus catálogos vigentes enlazados y sin presentar una talla, color, modelo o disponibilidad específica como inventario en tiempo real.

**Dickies** queda explícitamente pendiente: no se añadirá al texto, imágenes, catálogos ni metadata del staging hasta recibir su catálogo autorizado o una confirmación documental equivalente. Esta regla evita usar la marca sin una fuente operativa verificable.

Las marcas confirmadas se hicieron visibles en el paquete C1 del staging el 2026-08-25 mediante una franja enlazada a los PDFs existentes. La presentación se limita a las marcas de catálogo y no afirma disponibilidad de una prenda concreta, inventario, precio o relación de distribución exclusiva.

## Reglas de integración

Los PDFs deben conservarse como archivos bajo control de la cuenta del cliente antes de cualquier deploy Cloudflare. Los enlaces de Wix existentes se mantienen hasta que los archivos se incorporen al repositorio/almacenamiento aprobado y se prueben en staging. Los nombres comerciales se reflejarán en la interfaz como BigBang, M&O y Soul & Blues. Las capacidades comerciales se presentan únicamente con la confirmación anterior y sin inventar detalles a partir de los catálogos.

## Integración de staging — 2026-08-24

Las tres copias autorizadas se cargaron como activos del staging de Manus y reemplazaron los enlaces temporales de Wix. Se comprobó que BigBang, M&O y Soul & Blues responden correctamente al seguir sus redirecciones desde el staging. Los metadatos visibles se corrigieron a 13.6 MB, 3.8 MB y 8.0 MB.

También se sustituyó la sección genérica de capacidades por la oferta confirmada: digitalización, bordado, serigrafía y prendas/uniformes —playeras, camisas, uniformes industriales y línea médica—. La exclusión de parches y gorras aparece como nota de alcance discreta. No se añadieron precios, materiales, plazos, mínimos de pedido, certificaciones ni otros detalles no confirmados.

Los archivos de este staging están alojados temporalmente como activos de Manus. Antes de la migración a Cloudflare Pages se deberá volver a colocar la misma versión aprobada de cada PDF en el repositorio/almacenamiento bajo control del cliente; esta integración no altera Wix, DNS ni el dominio público.
