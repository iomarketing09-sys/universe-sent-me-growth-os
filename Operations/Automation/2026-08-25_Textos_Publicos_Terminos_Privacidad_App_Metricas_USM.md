---
title: "Textos públicos de términos y privacidad — App de métricas Universe Sent Me"
purpose: "Proveer el contenido mínimo, revisable y separado por marca para las URLs públicas requeridas por TikTok antes de autorizar la app local de métricas de Universe Sent Me."
status: Review
created: 2026-08-25
updated: 2026-08-25
version: "1.2"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-23_Diseno_Asistencia_Metricas_y_Respuestas_OmniRoute.md"
  - "Operations/Automation/2026-08-25_Guia_Piloto_Local_API_Oficial_Metricas_USM.md"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
  - "GrowthOS/todo.md"
organization: "Operations/Automation"
---

# Textos públicos de términos y privacidad — App de métricas Universe Sent Me

## Propósito

Estos textos están destinados a dos páginas públicas separadas dentro del sitio propio de **Universe Sent Me** en Wix. iO Marketing opera la aplicación descrita, que es un collector local privado para Universe Sent Me. No vende productos, no publica en TikTok y no se relaciona con Bam in a Can ni Firma Bordados.

> **Estado de publicación:** la URL de privacidad existente fue identificada; faltan confirmar la URL de términos, el correo público de contacto de iO Marketing y que ambas páginas correspondan a esta app. No sustituye revisión legal profesional.

## URLs existentes verificadas por Fernando

| Tipo | URL | Estado |
| :--- | :--- | :--- |
| Privacy Policy | `https://iomarketin.wixstudio.com/universesentme/privacypolicyusm` | Identificada; pendiente de revisión pública de contenido y alcance. |
| Terms of Service | Pendiente de URL exacta. | No usar la URL principal como sustituto. |

> **Bloqueo técnico de TikTok:** el método de verificación actual entrega un archivo de firma y exige que esté disponible bajo el prefijo de URL indicado. Wix documenta que no permite servir un archivo `.txt` arbitrario en una ruta de sitio controlada. No se debe subir el archivo al Media Manager ni pulsar `Verify` hasta elegir un host estático compatible. [1] [2]

## Alternativas de host pendientes de decisión

| Alternativa | Compatibilidad con archivo en ruta exacta | Separación de marcas | Consideración |
| :--- | :--- | :--- | :--- |
| GitHub Pages en repositorio público dedicado | Sí; publica archivos estáticos conservando la estructura de directorios. [3] | Repositorio nuevo exclusivo de Universe Sent Me. | Los contenidos publicados serían visibles y el repositorio debe ser público en GitHub Free. |
| Cloudflare Pages en proyecto/cuenta separada | Sí; despliega HTML y activos estáticos bajo un subdominio `*.pages.dev`. [4] | Proyecto de Universe Sent Me, sin usar el proyecto, host ni dominio de Firma Bordados. | Requiere una cuenta o proyecto distinto y autorización explícita para crearlo. |

No se creará ningún host, repositorio público o proyecto de Cloudflare por este documento.

## Página 1 — Terms of Service

**Page title:** `Terms of Service — Universe Sent Me Metrics App`

**Last updated:** `25 August 2026`

### 1. About this app

The Universe Sent Me Metrics App is a private, local analytics tool operated by iO Marketing for the Universe Sent Me brand. It is used only to review performance information for social accounts that the authorized operator controls.

The app does not publish content, edit videos, manage comments, send messages, run advertising campaigns, process payments, or act on behalf of unrelated brands.

## Referencias

[1]: https://developers.tiktok.com/doc/getting-started-create-an-app "TikTok for Developers — Register Your App"
[2]: https://support.wix.com/en/article/request-adding-a-txt-file-to-the-top-level-domain-for-google-analytics-verification "Wix Support — TXT file hosting limitation"
[3]: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site "GitHub Docs — Creating a GitHub Pages site"
[4]: https://developers.cloudflare.com/pages/framework-guides/deploy-anything/ "Cloudflare Pages Docs — Static HTML"

### 2. Authorized use

The app may be connected only to the Universe Sent Me social accounts authorized by their owner or administrator. The operator must not use the app to access third-party accounts without authorization.

### 3. Limited access

The app requests only the permissions needed to read account and video performance data. For TikTok, these include basic account authorization and public-video metrics. For YouTube, the app may read channel analytics and, where the channel is eligible, estimated monetization metrics.

The app does not request permissions to post, edit, delete, comment, message, manage advertising, or transfer funds.

### 4. Availability and accuracy

Analytics data is provided by the relevant platform and may be delayed, incomplete, unavailable, or corrected later. YouTube monetization values are estimates and may change after the platform's monthly adjustments. The app does not guarantee specific performance, reach, revenue, or business outcomes.

### 5. Suspension or revocation

The authorized operator may revoke platform authorization at any time through the relevant platform. The app may be paused or discontinued if access is no longer authorized, if an account does not belong to Universe Sent Me, or if platform rules change.

### 6. Contact

For questions about this app, contact iO Marketing at: **[public contact email to be confirmed before publication]**.

## Página 2 — Privacy Policy

**Page title:** `Privacy Policy — Universe Sent Me Metrics App`

**Last updated:** `25 August 2026`

### 1. Scope

This Privacy Policy applies only to the Universe Sent Me Metrics App, a local analytics tool operated by iO Marketing for the Universe Sent Me brand. It does not apply to Bam in a Can, Firma Bordados, or any other iO Marketing client or brand.

### 2. Information the app may access

After an authorized operator grants consent, the app may access the following information from the connected Universe Sent Me accounts:

| Source | Information used |
| :--- | :--- |
| TikTok | Basic authorization information and public-video identifiers, publication dates, titles, views, likes, comments and shares. |
| YouTube | Channel and video analytics such as views, engagement, watch time, audience-retention metrics, subscribers gained and, if available, estimated monetization and advertising-performance metrics. |
| Local operation logs | Technical collection status, extraction time, source, data availability and error status. |

The app is not designed to retrieve, store, or analyze private messages, passwords, payment instruments, full comments, advertising management data, or personal data from unrelated social accounts.

### 3. How information is used

The information is used only to measure Universe Sent Me content performance, maintain internal historical records, identify data-quality issues, and prepare internal growth-analysis drafts. The app does not sell personal information or use the connected data to publish content automatically.

### 4. Storage and security

Access tokens, OAuth client files and raw platform responses are stored locally on the authorized operator's computer in restricted directories outside the project repository. They are not placed in public pages, GitHub, chat messages, or OmniRoute prompts.

Only sanitized, minimum-necessary aggregate metrics may be used for internal analysis. Exact YouTube monetary amounts remain in the local financial layer unless separately authorized by the operator.

### 5. Sharing

The app does not share collected data with unrelated brands or clients. iO Marketing maintains separation between Universe Sent Me, Bam in a Can and Firma Bordados.

The social platforms themselves process information according to their own policies when authorization is granted. The iO Marketing website host may also process ordinary website technical data under its own policies.

### 6. Retention and deletion

The operator may revoke authorization through TikTok or Google at any time. Once authorization is revoked, the app stops future collection for that platform. The operator may delete local tokens and local raw evidence when no longer needed for the stated analytics purpose, subject to the need to preserve approved internal performance records.

### 7. Changes to this policy

This policy may be updated if the app's data access, security controls, platforms, or legal requirements change. The latest version will be published on this page.

### 8. Contact

For privacy questions or requests related to this app, contact iO Marketing at: **[public contact email to be confirmed before publication]**.

## Publicación en Wix

Crear dos páginas públicas y separadas dentro de `https://iomarketin.wixstudio.com/universesentme`, sin incluirlas necesariamente en la navegación principal del sitio:

| Página Wix | URL sugerida | Contenido fuente |
| :--- | :--- | :--- |
| Terms of Service — Universe Sent Me Metrics App | `https://iomarketin.wixstudio.com/universesentme/usm-metrics-terms` | Página 1 de este documento. |
| Privacy Policy — Universe Sent Me Metrics App | `https://iomarketin.wixstudio.com/universesentme/usm-metrics-privacy` | Página 2 de este documento. |

Tras publicar, abrir cada enlace en modo incógnito o sin iniciar sesión y confirmar que se visualiza públicamente. Esas URLs públicas son las que se pegarán en el formulario de TikTok.
