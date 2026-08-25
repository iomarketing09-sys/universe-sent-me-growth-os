---
title: "Gate 6 — Revisión técnica y visual para producción — Firma Bordados"
purpose: "Registrar las comprobaciones no destructivas de rutas, seguridad, compilación y activos del staging, y definir la revisión visual manual requerida antes de producción."
status: Review
created: 2026-08-25
updated: 2026-08-25
version: "1.0"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-25_Gate4_Aprobacion_Contenido_Produccion_Firma_Bordados.md"
  - "Operations/Production/2026-08-25_Diseno_Formulario_Privacidad_Firma_Bordados.md"
  - "Operations/Production/2026-08-25_Auditoria_Gate3_Dominio_DNS_Firma_Bordados.md"
  - "Operations/Production/2026-08-23_Evaluacion_Migracion_Wix_Hosting_IA.md"
  - "Operations/Production/todo.md"
organization: "Operations/Production"
---

# Gate 6 — Revisión técnica y visual para producción — Firma Bordados

> **Revisión no destructiva.** No se usó navegador remoto ni se modificó el staging, Wix, DNS, nameservers, dominio, proveedores o datos del cliente. Las comprobaciones visuales corresponden exclusivamente al usuario desde Quick-seedless.

## 1. Resultado técnico — 2026-08-25

| Comprobación | Resultado | Estado |
| :--- | :--- | :--- |
| Inicio `https://firma-bordados-staging.pages.dev/` | HTTP 200 | Correcto |
| Aviso de privacidad `/privacidad/` | HTTP 200 | Correcto |
| Variante `/privacidad` | HTTP 200 | Correcto |
| `robots.txt` | HTTP 200 y `Disallow: /` | Correcto para staging |
| Catálogo BigBang | HTTP 200 | Correcto |
| Catálogo Soul & Blues | HTTP 200 | Correcto |
| Catálogo M&O | HTTP 200 | Correcto |
| Headers | `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy` restrictiva | Correcto |
| Indexación de staging | Meta `noindex` y `robots.txt` bloqueado | Correcto para staging |
| Tipos y build | `pnpm check` y `pnpm exec vite build` exitosos | Correcto |
| Estado del repositorio web | Sin cambios locales al terminar la revisión | Correcto |

La compilación generó un bundle principal de 497.80 kB sin comprimir y 133.80 kB gzip. Es un dato de referencia de build, no una métrica de experiencia de usuario ni un bloqueo del corte. No se detectó una falla técnica de alta severidad en las rutas, activos o headers revisados.

## 2. Revisión visual manual requerida en Quick-seedless

| Área | Qué debe comprobar Io Marketing | Resultado esperado |
| :--- | :--- | :--- |
| Inicio, escritorio y móvil | Logo, hero, contraste, navegación y no desbordamiento horizontal | Contenido legible y navegación utilizable |
| WhatsApp y correo guiado | Abrir ambos botones sin enviar datos reales | WhatsApp/correo se abren con mensaje preparado y destinatario correcto |
| Catálogos | Abrir los tres PDF y comprobar portada/tamaño visible | BigBang 13.6 MB, Soul & Blues 8.0 MB y M&O 3.8 MB |
| Preguntas frecuentes | Revisar mínimo de serigrafía, tiempos, prendas y exclusiones | Texto coincide con lo aprobado; no aparecen precios ni materiales no confirmados |
| Portafolio y contacto | Fachada, cuatro tarjetas, teléfonos, dirección, horario y enlace “Cómo llegar” | Activos correctos; dirección lleva a Maps; no aparecen marcas de cliente no aprobadas |
| Privacidad | Abrir `/privacidad/` desde footer | Responsable Firma Bordados, correo ARCO y plazo propuesto visibles |
| Formspree sintético | Confirmar que sigue marcado como prueba y no se usa con datos reales | Correo guiado y WhatsApp permanecen como canales oficiales |

## 3. Estado de Gate 6

La revisión técnica está **aprobada**. El Gate 6 permanece en **Review** hasta que Io Marketing confirme la revisión visual manual de la tabla anterior desde Quick-seedless. Esta confirmación no autoriza todavía SEO/indexación de producción ni cambio de nameservers; esos pasos pertenecen a gates posteriores.
