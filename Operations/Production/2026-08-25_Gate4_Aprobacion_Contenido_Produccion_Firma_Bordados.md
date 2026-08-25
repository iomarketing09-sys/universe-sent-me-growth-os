---
title: "Gate 4 — Aprobación final de contenido para producción — Firma Bordados"
purpose: "Contrastar el contenido del staging contra las fuentes confirmadas y registrar los elementos que requieren aprobación o ajuste antes de publicar en firmabordados.com."
status: Review
created: 2026-08-25
updated: 2026-08-25
version: "1.0"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-24_Inventario_Catalogos_Drive_Firma_Bordados.md"
  - "Operations/Production/2026-08-24_Curacion_Activos_Web_Firma_Bordados.md"
  - "Operations/Production/2026-08-25_Diseno_Formulario_Privacidad_Firma_Bordados.md"
  - "Operations/Production/2026-08-23_Evaluacion_Migracion_Wix_Hosting_IA.md"
  - "Operations/Production/todo.md"
organization: "Operations/Production"
---

# Gate 4 — Aprobación final de contenido para producción — Firma Bordados

> **Revisión de contenido — no autoriza publicar el dominio.** Esta auditoría compara el staging con las fuentes confirmadas y no modifica Wix, DNS, nameservers, dominio, catálogos o el sitio público.

## 1. Contenido consistente con las confirmaciones

| Elemento visible | Estado de respaldo | Fuente / observación | Resultado Gate 4 |
| :--- | :--- | :--- | :--- |
| Logo e identidad visual | Confirmado | Logo oficial y dirección visual «Color que Trabaja» aprobados | Apto |
| Servicios | Confirmado | Digitalización, bordado, serigrafía, playeras, camisas, uniformes industriales y línea médica | Apto |
| Alcance negativo | Confirmado | No se realizan parches ni gorras | Apto |
| Serigrafía | Confirmado | Mínimo de 12 piezas; no se extiende a otros servicios | Apto |
| Entrega | Confirmado | Se confirma según cantidad, requerimiento y carga de trabajo; no se publica plazo exacto | Apto |
| Catálogos | Confirmado | BigBang 2019, Soul & Blues 2025 y M&O, con tamaños visibles 13.6 MB, 8.0 MB y 3.8 MB | Apto |
| Marcas por catálogo | Confirmado | Solo BigBang, M&O y Soul & Blues; Dickies sigue excluido | Apto |
| Portafolio y fachada | Confirmado | Activos locales curados; no se muestran marcas de clientes como afiliación | Apto |
| Contacto | Confirmado | `firmabordados@yahoo.com`, WhatsApp, teléfonos, dirección y horario confirmados | Apto |
| Privacidad | Confirmado para correo guiado | Aviso estático aprobado; canal Formspree real no se habilita | Apto con correo guiado |

## 2. Elementos que no deben entrar a producción sin acción

| Elemento actual del staging | Riesgo o falta de respaldo | Acción requerida antes del corte | Bloquea Gate 4 |
| :--- | :--- | :--- | :--- |
| Distintivo visual **«20+ años de experiencia»** | No existe una fuente canónica que confirme el número de años | Firma Bordados debe confirmar la cifra o autorizar retirar el distintivo | **Sí** |
| Formulario Formspree de pruebas sintéticas | Está visible en el staging, pero Gate 5 lo excluye de consultas reales hasta verificar el buzón oficial | Retirar/ocultar el piloto en la versión de producción y conservar correo guiado + WhatsApp; o verificar el buzón y aprobar su apertura por separado | **Sí** |
| Pie de página **«Staging de modernización · sin cambio DNS»** | Es correcto solo para la URL temporal | Sustituirlo por una versión de producción o retirarlo al preparar el corte | **Sí** |
| `noindex` y robots bloqueados | Correcto para staging, incorrecto para el sitio público | Cambiarse únicamente dentro del Gate 7 después de que el dominio resuelva en Cloudflare Pages | No en Gate 4; sí antes del cierre de producción |
| Materiales, composiciones, certificaciones, disponibilidad y condiciones nuevas | El cliente indicó no incluirlas todavía | Mantenerlas fuera hasta confirmación documental posterior | No; contenido deliberadamente excluido |

## 3. Checklist de aprobación del cliente

| Aprobación requerida | Estado |
| :--- | :--- |
| Logo, paleta e identidad de Firma Bordados | Pendiente de aprobación final para producción |
| Fotografías de fachada, proceso, bordado, digitalización y variedad de prendas | Pendiente de aprobación final para producción |
| Servicios, exclusiones, mínimo de serigrafía y texto de tiempos | Pendiente de aprobación final para producción |
| Teléfonos, WhatsApp, correo, dirección y horario | Pendiente de aprobación final para producción |
| Catálogos BigBang, Soul & Blues y M&O | Pendiente de aprobación final para producción |
| Aviso de privacidad y correo guiado como canal oficial | Pendiente de aprobación final para producción |
| Cifra de antigüedad o retiro del distintivo «20+ años» | Pendiente de decisión |
| Retiro del formulario de pruebas Formspree y texto de staging antes de producción | Pendiente de decisión |

## 4. Decisión de Gate 4

El contenido comercial confirmado está listo para ser aprobado, pero el Gate 4 queda en **Review** por tres acciones precisas: confirmar o retirar la afirmación de «20+ años», retirar/ocultar el formulario sintético antes de producción y sustituir el texto de staging en el footer. Una vez resueltas y tras una revisión visual final en Quick-seedless, Io Marketing podrá registrar la aprobación final de contenido sin necesidad de añadir materiales, certificaciones, precios, disponibilidad ni nuevos proveedores.
