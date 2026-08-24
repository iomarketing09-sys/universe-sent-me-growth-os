---
title: "Backlog técnico de bajo riesgo — Staging Firma Bordados"
purpose: "Priorizar mejoras de rendimiento, accesibilidad, seguridad técnica y operación del staging que no dependan de materiales, tiempos de entrega o mínimos de pedido."
status: Active
created: 2026-08-24
updated: 2026-08-24
version: "1.0"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-23_Guia_Staging_Cloudflare_Pages_Firma_Bordados.md"
  - "Operations/Production/2026-08-23_Evaluacion_Migracion_Wix_Hosting_IA.md"
  - "Operations/Production/2026-08-24_Inventario_Catalogos_Drive_Firma_Bordados.md"
  - "GrowthOS/00_01_Changelog_GrowthOS.md"
organization: "Operations/Production"
---

# Backlog técnico de bajo riesgo — Staging Firma Bordados

## 1. Estado auditado

El staging `https://firma-bordados-staging.pages.dev` construye correctamente desde la rama `staging` y sirve activos locales, catálogos, WhatsApp y el formulario `mailto:` sin depender de Wix o Manus. La interfaz ya respeta `prefers-reduced-motion` para sus revelados, y los catálogos se abren en una pestaña separada.

La auditoría identificó ajustes que no requieren información comercial adicional. La copia inicial genera un JavaScript principal de aproximadamente 562 kB sin comprimir, conserva providers genéricos que no usa la landing y aún puede reforzar zoom, foco visible, noindex explícito y encabezados estáticos. Ninguno de estos cambios altera servicios, precios, materiales, tiempos, mínimos, dominio o DNS.

## 2. Prioridades

| Prioridad | Ajuste | Beneficio | Dependencia | Riesgo de contenido |
| :--- | :--- | :--- | :--- | :--- |
| P0 | Paquete de accesibilidad: eliminar `maximum-scale=1`, añadir enlace de salto, estados `:focus-visible` y desactivar `scroll-behavior: smooth` con reducción de movimiento | Mejora teclado, zoom y comodidad sin cambiar la propuesta visual | Ninguna | Nulo |
| P0 | Añadir meta `robots=noindex,nofollow` al staging, además de `robots.txt` | Evita presentar la versión temporal como sitio final en buscadores | Ninguna | Nulo |
| P0 | Crear `client/public/_headers` con `X-Content-Type-Options`, `Referrer-Policy` y `Permissions-Policy` restrictiva | Endurece la respuesta estática sin introducir backend | Probar WhatsApp, PDFs y redes tras el cambio | Nulo |
| P1 | Marcar imágenes no críticas con `loading="lazy"` y `decoding="async"`; dar prioridad solo a la imagen hero | Reduce carga inicial percibida y preserva el hero | Ninguna | Nulo |
| P1 | Simplificar el núcleo React: retirar `ThemeProvider`, `TooltipProvider` y `Toaster` si la landing no los usa; ejecutar análisis de bundle antes de podar dependencias | Reduce superficie de runtime y facilita mantenimiento | Prueba visual y build | Nulo |
| P1 | Añadir CI de GitHub: `pnpm check` y `pnpm exec vite build` para cada Pull Request | Evita que un cambio de contenido rompa el deploy | Repositorio privado Io Marketing | Nulo |
| P1 | Proteger `main`; mantener `staging` como rama de revisión mientras Wix continúe activo | Evita que un cambio no revisado se interprete como corte final | Decisión operativa de Io Marketing | Nulo |
| P2 | Añadir Open Graph, Twitter Card y JSON-LD de negocio local | Mejora previsualización y preparación SEO del futuro dominio | Validar nombre legal, teléfono preferido, dirección y horarios antes de declarar datos estructurados | Bajo |
| P2 | Añadir analítica de eventos para clics en WhatsApp, correo y PDFs | Mide intención comercial y ayuda a priorizar catálogo/CTA | Consentimiento de privacidad, herramienta y responsable de datos | Medio |
| P2 | Sustituir `mailto:` por formulario con backend | Recibe solicitudes aunque el cliente no tenga app de correo configurada | Aviso de privacidad, destinatario, antispam y proceso de respuesta | Medio |

## 3. Paquete P0 aplicado

El paquete **P0 de accesibilidad y protección de staging** se aplicó en el commit `b3754d0` y se promovió a la rama `main` que Cloudflare Pages usa para este sitio de prueba. Incluye zoom habilitado, estados de foco, enlace de salto, reducción de movimiento integral, meta noindex y encabezados estáticos. Se validó en build, escritorio y móvil, y no cambia la oferta comercial ni recaba datos.

El siguiente ajuste propuesto corresponde al paquete **P1 de mantenimiento**: CI GitHub, protección de rama y medición real de bundle antes de eliminar providers/dependencias. La meta no es perseguir un número de kilobytes, sino retirar código realmente inactivo con una build reproducible y revisión visual.

## 4. Límites hasta recibir la información del cliente

No se deben añadir precios, cotizadores, promesas de tiempo, mínimos de pedido, materiales, certificaciones, formularios que almacenen datos, analytics de terceros ni SEO estructurado definitivo. La URL `*.pages.dev` debe seguir marcada como staging y el dominio `firmabordados.com` no debe asociarse al proyecto hasta el gate de aprobación, transferencia/operación administrada y migración documentado.
