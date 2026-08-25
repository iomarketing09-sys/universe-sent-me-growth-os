---
title: "Evaluación de migración del sitio Wix — Universe Sent Me"
purpose: "Separar el host técnico requerido para la verificación de TikTok de una futura migración completa del sitio de Universe Sent Me desde Wix."
status: Draft
created: 2026-08-25
updated: 2026-08-25
version: "1.0"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-23_Diseno_Asistencia_Metricas_y_Respuestas_OmniRoute.md"
  - "Operations/Automation/2026-08-25_Textos_Publicos_Terminos_Privacidad_App_Metricas_USM.md"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
  - "GrowthOS/todo.md"
  - "GrowthOS/00_01_Changelog_GrowthOS.md"
organization: "Operations/Production"
---

# Evaluación de migración del sitio Wix — Universe Sent Me

## Propósito y estado

Universe Sent Me tiene un sitio público en `https://iomarketin.wixstudio.com/universesentme`, administrado por iO Marketing. Esta evaluación surge porque TikTok exige servir un archivo de firma en una ruta estática exacta, algo que Wix no permite de forma compatible. La verificación de TikTok y una migración completa del sitio son **decisiones separadas**: resolver una no obliga a ejecutar la otra.

Este documento es un borrador de evaluación. No autoriza cambios en Wix, DNS, dominio, analítica, enlaces sociales, formularios, hospedaje, presupuesto ni contenido publicado.

## Inventario público inicial

La lectura pública del 25 de agosto identificó un sitio de marca con navegación y contenido editorial-portfolio; no es una tienda ni un sistema transaccional.

| Área observada | Estado de migración | Nota |
| :--- | :--- | :--- |
| Inicio y propuesta de marca | Reutilizable tras revisión editorial. | Presenta `Storytelling & AI`, arte, experiencias creativas y herramientas de diseño. |
| Portfolio / Projects | Requiere inventario de activos y enlaces. | La página muestra tres bloques de preguntas/respuestas que deben revisarse antes de conservarlos. |
| Contacto | Requiere confirmar canal y privacidad. | El sitio muestra el correo público de iO Marketing. |
| Redes sociales | Requiere validación de destinos. | Incluye Instagram y Facebook de Universe Sent Me. |
| Política de privacidad y términos | Existentes bajo una misma URL. | TikTok puede requerir URL y firma compatibles; el contenido debe revisarse para el collector local. |

## Decisiones separadas

| Decisión | Objetivo | Opción de menor alcance | Riesgo si se mezcla |
| :--- | :--- | :--- | :--- |
| Host técnico TikTok | Servir términos, privacidad y el archivo de firma en una ruta exacta. | Sitio estático dedicado, con contenido público mínimo. | Convertir una verificación simple en una migración apresurada. |
| Migración completa del sitio | Modernizar el sitio, controlar rutas y simplificar mantenimiento a futuro. | Auditoría primero, sin corte ni cambio de DNS. | Perder enlaces, SEO, formularios o activos por no inventariar. |

## Alternativas para la futura migración

| Ruta | Cuándo encaja | Ventajas | Validaciones previas |
| :--- | :--- | :--- | :--- |
| Mantener Wix y usar host técnico separado | El sitio actual sigue cumpliendo su función y el objetivo inmediato es TikTok. | Menor cambio, sin corte ni rediseño. | Verificar que los textos públicos del host separado describan correctamente la app local. |
| Migrar a sitio estático dedicado | Se desea más control de archivos, rutas, rendimiento y mantenimiento de contenido relativamente estable. | Un mismo sitio puede alojar portfolio, textos legales y archivos de verificación. | Inventario de páginas, activos, redes, contacto, SEO y dominio; staging visual antes de sustituir Wix. |
| Mantener Wix con CMS u otra plataforma | Se anticipa edición frecuente por múltiples autores o crecimiento editorial complejo. | Familiaridad operativa para el equipo. | Definir primero roles, frecuencia de edición y necesidad real de CMS. |

## Secuencia propuesta sin compromiso de ejecución

Primero, crear o elegir el host técnico exclusivo de Universe Sent Me y resolver la verificación de TikTok. Después, realizar una auditoría de migración con inventario de cada activo, URL, formulario, analítica, red social, texto legal, metadato SEO y dependencia de Wix. Solo después de aprobar ese inventario se debe construir un staging y comparar visualmente contra el sitio actual antes de cualquier cambio de dominio o publicación.

## Gates para una migración futura

La migración requiere una instrucción explícita de Fernando y los siguientes gates: definición de objetivo y audiencia; inventario de contenido y activos con permisos; propiedad y estado del dominio; SEO y redirecciones; canal de contacto; analítica; staging validado; plan de reversión; y autorización separada para el corte. Firma Bordados queda fuera de todos estos gates.

## Referencias

[1]: https://iomarketin.wixstudio.com/universesentme "Universe Sent Me — sitio público actual"
[2]: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site "GitHub Docs — Creating a GitHub Pages site"
[3]: https://developers.cloudflare.com/pages/framework-guides/deploy-anything/ "Cloudflare Pages Docs — Static HTML"
