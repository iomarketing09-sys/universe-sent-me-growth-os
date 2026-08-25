---
title: "Gate 7 — SEO e indexación para producción — Firma Bordados"
purpose: "Definir los cambios de SEO, canonical, sitemap e indexación que solo deberán aplicarse después de que firmabordados.com resuelva hacia la versión de producción aprobada."
status: Active
created: 2026-08-25
updated: 2026-08-25
version: "1.1"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-25_Gate6_Revision_Tecnica_Visual_Produccion_Firma_Bordados.md"
  - "Operations/Production/2026-08-25_Auditoria_Gate3_Dominio_DNS_Firma_Bordados.md"
  - "Operations/Production/2026-08-25_Gate4_Aprobacion_Contenido_Produccion_Firma_Bordados.md"
  - "Operations/Production/2026-08-23_Evaluacion_Migracion_Wix_Hosting_IA.md"
  - "Operations/Production/todo.md"
organization: "Operations/Production"
---

# Gate 7 — SEO e indexación para producción — Firma Bordados

> **Plan posterior al corte.** No retirar `noindex`, no cambiar `robots.txt`, no añadir canonical de producción ni enviar sitemap mientras `firmabordados.com` no resuelva de forma estable hacia Cloudflare Pages. El staging debe conservar sus bloqueos actuales.

## 1. Estado correcto mientras existe staging

El staging `firma-bordados-staging.pages.dev` debe conservar `noindex` y `robots.txt` bloqueado. Google explica que una regla `noindex` debe permanecer visible para el rastreador y no estar bloqueada por `robots.txt` para que pueda procesarse; por eso los bloqueos del staging no deben copiarse a producción ni alterarse de forma anticipada.[1]

## 2. Configuración propuesta después de que el dominio funcione

| Componente | Valor o acción propuesta | Condición antes de aplicar |
| :--- | :--- | :--- |
| URL canónica | `https://firmabordados.com/` | DNS, HTTPS y página raíz funcionando de forma estable |
| Variantes de dominio | Redirecciones permanentes desde `www.firmabordados.com`, `es.firmabordados.com` y `m.firmabordados.com` al dominio raíz | Gate 3 ejecutado y validado |
| `rel="canonical"` | Canonical absoluto y autorreferente para inicio; canonical absoluto para `/privacidad/` si se mantiene indexable | URL final y rutas estables; Google recomienda URL absoluta y canonical en el `<head>`.[2] |
| Meta robots | Retirar `noindex,nofollow,noarchive` del sitio público y permitir `index,follow` en las páginas aprobadas | Solo después de comprobar que el dominio apunta a la versión correcta |
| `robots.txt` | `User-agent: *`, `Allow: /` y referencia al sitemap; no usar robots para ocultar páginas | Sitemap público disponible; robots controla rastreo, no es un mecanismo fiable para ocultar resultados.[3] |
| `sitemap.xml` | Listar únicamente URLs canónicas aprobadas, con rutas absolutas `https://firmabordados.com/` y, si aplica, `/privacidad/` | Sitio estable; Google recomienda URLs absolutas y solo URLs que se desean mostrar en resultados.[4] |
| PDFs de catálogo | Mantener fuera del primer sitemap salvo que Io Marketing decida explícitamente buscarlos/indexarlos como activos individuales | Evita convertir catálogos de terceros en una prioridad SEO sin decisión comercial |
| Search Console | Verificar la propiedad del dominio y enviar el sitemap después del corte | Io Marketing, como registrante/operador, aprueba la cuenta y el método de verificación |
| Analítica | No instalar por defecto | Requiere decisión de herramienta, finalidad y aviso/consentimiento si aplica |

Los redirects, canonical autorreferente y sitemap con la misma URL canónica se refuerzan entre sí como señales de canonicalización, según Google.[2] La inclusión en sitemap es una señal, no una garantía de indexación.[4]

## 3. Metadatos propuestos para revisión

| Elemento | Propuesta | Estado |
| :--- | :--- | :--- |
| Título de inicio | `Firma Bordados | Bordado, serigrafía y uniformes en Piedras Negras` | **Aprobado por Fernando**; aplicar solo después del corte |
| Descripción de inicio | `Firma Bordados ofrece digitalización, bordado, serigrafía y opciones de playeras, camisas, uniformes industriales y línea médica en Piedras Negras, Coahuila. Consulte nuestros catálogos.` | **Aprobada por Fernando**; aplicar solo después del corte |
| Título de privacidad | `Aviso de privacidad | Firma Bordados` | Aprobado como texto de ruta; aplicar solo después del corte |
| Imagen Open Graph | Logo oficial o hero aprobado, sin marcas de clientes | Pendiente de decisión; no es requisito de indexación |
| Datos estructurados | Solo después de validar nombre comercial, dirección, teléfonos, horario y URL final | Pendiente; no se activará en este gate sin revisión adicional |

No se proponen palabras como “mejor”, precios, disponibilidad, materiales, certificaciones, tiempos exactos ni Dickies, porque no están autorizados como afirmaciones públicas.

## 4. Secuencia de ejecución y validación

| Orden | Acción | Evidencia requerida |
| :--- | :--- | :--- |
| 1 | Ejecutar Gate 3 y comprobar que el root HTTPS sirve la versión aprobada | HTTP 200, certificado válido, rutas y activos correctos |
| 2 | Preparar la versión técnica de producción: ocultar Formspree sintético y sustituir footer de staging | Pull Request, CI y revisión visual aprobada |
| 3 | Aplicar `index,follow`, canonical, sitemap y robots de producción | Pull Request, CI y verificación HTTP del dominio raíz |
| 4 | Verificar redirecciones de `www`, `es` y `m` al root | HTTP y pruebas desde varias redes |
| 5 | Verificar Search Console para el dominio y enviar sitemap | Confirmación del panel del titular autorizado |
| 6 | Solicitar rastreo de la URL principal solo después de validar contenido y canonical | Resultado de inspección de URL, sin depender de una promesa de indexación |
| 7 | Revisar durante el periodo de estabilización que no reaparezca Wix ni URLs duplicadas | Evidencia de redirecciones y cobertura de indexación |

## 5. Estado del Gate 7

Fernando aprobó título, descripción, canonical de raíz, sitemap inicial limitado a inicio/privacidad y redirecciones de variantes hacia el root. El Gate 7 está **activo y preparado documentalmente**, pero su implementación permanece bloqueada hasta que el Gate 3 se ejecute y el dominio raíz esté activo. Aún se requiere preparar la versión técnica que oculta el piloto Formspree y retira el texto de staging. No se añade analítica ni se cambia SEO del staging.

## Referencias

[1]: [Google Search Central — Bloquear indexación con `noindex`](https://developers.google.com/search/docs/crawling-indexing/block-indexing)

[2]: [Google Search Central — Consolidar URLs duplicadas con canonical](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)

[3]: [Google Search Central — Introducción a `robots.txt`](https://developers.google.com/search/docs/crawling-indexing/robots/intro)

[4]: [Google Search Central — Crear y enviar un sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
