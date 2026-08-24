---
title: "Curaduría de activos web — Firma Bordados"
purpose: "Registrar la procedencia, evaluación y uso previsto de fotografías autorizadas para actualizar de forma reversible el staging Cloudflare de Firma Bordados."
status: Active
created: 2026-08-24
updated: 2026-08-24
version: "1.0"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-23_Guia_Staging_Cloudflare_Pages_Firma_Bordados.md"
  - "Operations/Production/2026-08-23_Evaluacion_Migracion_Wix_Hosting_IA.md"
  - "Operations/Production/2026-08-24_Inventario_Catalogos_Drive_Firma_Bordados.md"
  - "Operations/Production/2026-08-24_Backlog_Tecnico_Staging_Firma_Bordados.md"
organization: "Operations/Production"
---

# Curaduría de activos web — Firma Bordados

## 1. Alcance

Esta curaduría aplica únicamente al staging `firma-bordados-staging.pages.dev`. No autoriza publicar en `firmabordados.com`, cambiar Wix, DNS, nameservers ni reutilizar los activos de Firma Bordados dentro de Universe Sent Me u OmniRoute.

Fernando autorizó revisar la carpeta Drive compartida y proporcionó dos fotografías propias para una actualización del sitio: una exhibición interior de playeras de colores y una fotografía de la fachada del negocio. Las imágenes pueden editarse para la web cuando sea necesario, respetando su contenido real, procedencia y contexto.

## 2. Hallazgos iniciales de Drive

Se revisó una muestra no destructiva de la carpeta `Firma Bordados - 2026`, enlazada desde la carpeta principal compartida. La estructura incluye fotografías de prendas/trabajos, recursos de identidad y piezas de redes sociales. Las publicaciones con texto social o layouts de feed se reservan como referencia de paleta, producto y lenguaje; no deben incrustarse directamente en la web como si fueran fotografías de portafolio.

| Activo revisado | Procedencia | Hallazgo | Uso recomendado |
| :--- | :--- | :--- | :--- |
| `IMG-20260821-WA0003.jpg` | Drive, 2026 | Camisa azul de tejido fino con bordado corporativo visible; vertical y con marca del cliente final. | Evidencia de detalle de bordado; puede usarse en recorte vertical o como referencia para una imagen exclusiva, sin sugerir afiliación con la marca visible. |
| `FB_IMG_1787256206553.jpg` | Drive, 2026 | Acercamiento de un bolsillo gris con bordado corporativo; vertical, sin composición panorámica. | Evidencia secundaria de textura y precisión; mejor como referencia o recorte de detalle, no como hero. |
| `FB_IMG_1785701725314.jpg` | Archivo proporcionado por Fernando | Exhibición interior de playeras de colores. La imagen prueba variedad de color, pero su encuadre incluye entorno doméstico y una pared dominante. | Editar o usar como referencia para una visual exclusiva de la sección de prendas/colores; no utilizar como hero tal cual. |
| `454445192_1033697188764689_1636449595553068132_n.jpg` | Archivo proporcionado por Fernando | Fachada real del negocio y escaparate con identidad visible. | Recurso de confianza/ubicación; usar con una edición ligera que mantenga fielmente el edificio y el letrero. |

## 3. Decisión visual aplicada

La actualización conserva **Color que Trabaja** y refuerza dos pruebas concretas de capacidad: variedad de prendas y presencia física local. La exhibición de playeras autorizada se usó solo como referencia para crear una imagen exclusiva de prendas sin logos, textos ni marcas de terceros. Esta visual ocupa un módulo secundario de la sección «Nuestro trabajo» y se etiqueta «Variedad para consultar»; no equivale a inventario disponible ni a catálogo de existencias.

La fotografía de fachada recibió una adaptación conservadora: se ajustaron encuadre, perspectiva, exposición y contraste sin modificar edificio, letrero, identidad ni entorno comercial. Se presenta en el bloque de contacto como prueba de atención local en Piedras Negras. Ambas imágenes se optimizaron en WebP para la web (≈59 kB para prendas y ≈214 kB para fachada), se integraron en la rama revisada y se publicaron tras validación de TypeScript/Vite y CI de GitHub.

Las fotos de bordado de terceros de Drive permanecen como referencia o detalle secundario, no como afirmación de relación comercial ni certificación. La selección final se validó junto con los enlaces de contacto, el CTA WhatsApp, el mínimo confirmado de serigrafía y la nota prudente sobre tiempos variables.
