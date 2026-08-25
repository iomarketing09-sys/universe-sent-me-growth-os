---
title: "Propuesta de cotización — Migración y mantenimiento administrado de Firma Bordados"
purpose: "Definir una base de cotización separada para el corte único desde Wix y el mantenimiento anual operado por Io Marketing, con alcances, exclusiones y supuestos verificables."
status: Draft
created: 2026-08-25
updated: 2026-08-25
version: "0.1"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-23_Evaluacion_Migracion_Wix_Hosting_IA.md"
  - "Operations/Production/2026-08-23_Guia_Staging_Cloudflare_Pages_Firma_Bordados.md"
  - "Operations/Production/2026-08-25_Diseno_Formulario_Privacidad_Firma_Bordados.md"
  - "Operations/Production/todo.md"
organization: "Operations/Production"
---

# Propuesta de cotización — Migración y mantenimiento administrado de Firma Bordados

> **Borrador comercial — requiere aprobación antes de usarse como cotización.** Los importes se expresan en pesos mexicanos (MXN), no incluyen impuestos aplicables, renovación del dominio, comisiones bancarias, tipo de cambio ni servicios externos de pago. No autoriza cambiar Wix, DNS, nameservers, dominio, cuentas ni facturación.

## 1. Modelo operativo propuesto

Firma Bordados conserva la titularidad del contenido, los catálogos, los datos de contacto y el dominio. Io Marketing opera el repositorio, Cloudflare Pages, despliegues y mantenimiento bajo un acuerdo administrado. Cualquier cambio de dominio, DNS, proveedor de formularios, analítica, factura o pago externo requiere aprobación específica del cliente.

La arquitectura base considera Cloudflare Pages estático, correo guiado y WhatsApp como canales de contacto. Este escenario tiene un costo técnico de hosting de USD 0 según la configuración actual; la renovación del dominio seguirá siendo una partida independiente hasta que el cliente confirme su precio y registrador.[1]

## 2. Costo único de migración propuesto

| Concepto | Alcance incluido | Importe propuesto |
| :--- | :--- | ---: |
| **Migración Wix → Cloudflare Pages** | Congelar la versión aprobada del staging, revisión final de contenido existente, inventario de DNS, plan de reversión, preparación del dominio en Cloudflare Pages, cambio DNS autorizado, validación desde varias redes, verificación de catálogo/contacto/HTTPS y hasta 7 días calendario de estabilización | **$6,000 MXN** |

El importe cubre **un dominio**, una ventana de corte, los activos y contenido ya aprobados en el staging, un plan de reversión y una ronda de correcciones de fallas directamente atribuibles al corte. La propuesta comercial recomendada es 50% al autorizar la preparación del corte y 50% cuando el cliente acepte que el dominio sirve la nueva versión correctamente.

| No incluido en la migración | Tratamiento propuesto |
| :--- | :--- |
| Renovación/transferencia de dominio, plan Wix, impuestos, cargos de registrador o servicios de terceros | Pagados directamente por el cliente o reembolsados contra comprobante, con aprobación previa. |
| Nuevo diseño, redacción adicional, sesión fotográfica, video, catálogos nuevos, materiales/certificaciones no confirmados o páginas adicionales | Se cotizan como cambio de alcance. |
| Formulario real de Formspree, backend propio, Turnstile, analítica, CRM, correo transaccional o integración de IA | Requieren propuesta y aprobación separadas. |
| Incidencias originadas por servicios de terceros, información incorrecta del cliente o cambios no autorizados durante el corte | Se evalúan y cotizan fuera del alcance. |

## 3. Mantenimiento anual administrado por Io Marketing

Los paquetes se pagan por adelantado al inicio del periodo anual o, si el cliente lo solicita, en una equivalencia mensual indicada solo como referencia. Una petición que exceda los cambios incluidos se revisará y cotizará antes de ejecutarse.

| Paquete | Alcance anual incluido | Precio anual propuesto | Equivalente mensual de referencia |
| :--- | :--- | ---: | ---: |
| **Esencial — recomendado** | Operación del repositorio y Cloudflare Pages; respaldo lógico del repositorio; hasta 4 cambios menores de texto, enlaces, teléfono, horario o PDF vigente; revisión funcional trimestral de inicio, contacto, catálogos y aviso; coordinación de una incidencia crítica de disponibilidad | **$4,800 MXN/año** | **$400 MXN/mes** |
| **Estándar** | Todo lo Esencial; hasta 12 cambios menores; revisión funcional mensual; una actualización anual de imagen/activo ya autorizado; informe breve semestral de cambios y estado | **$8,400 MXN/año** | **$700 MXN/mes** |

Un **cambio menor** es una sustitución o edición que no modifica la estructura, el diseño, la arquitectura, los proveedores ni el alcance legal/comercial del sitio. No se acumulan cambios no usados entre periodos y no incluyen la creación de nuevo contenido sin material confirmado. Io Marketing no garantiza respuesta comercial a consultas del cliente; su responsabilidad operativa se limita al sitio y sus canales técnicos autorizados.

## 4. Total estimado del primer año

| Escenario | Migración única | Mantenimiento anual | Total de servicio Io Marketing en el primer año | Partidas externas separadas |
| :--- | ---: | ---: | ---: | :--- |
| **Recomendado: Esencial** | $6,000 MXN | $4,800 MXN | **$10,800 MXN** | Renovación del dominio, impuestos y cualquier proveedor adicional aprobado. |
| **Estándar** | $6,000 MXN | $8,400 MXN | **$14,400 MXN** | Renovación del dominio, impuestos y cualquier proveedor adicional aprobado. |
| **Solo migración** | $6,000 MXN | $0 MXN | **$6,000 MXN** | El cliente asume operación posterior, dominio y cualquier mantenimiento. |

El segundo año no tendría costo de migración. Con el paquete Esencial, el costo de servicio de Io Marketing sería $4,800 MXN/año más renovaciones y servicios externos autorizados. Con Estándar, sería $8,400 MXN/año bajo los mismos supuestos.

## 5. Requisitos antes de emitir la cotización final

| Decisión pendiente | Responsable | Efecto en la cotización |
| :--- | :--- | :--- |
| Confirmar si el cliente desea Esencial o Estándar | Firma Bordados | Define el mantenimiento incluido. |
| Confirmar costo, fecha y control de renovación de `firmabordados.com` | Firma Bordados | Se agrega como partida externa o directa del cliente. |
| Definir facturación, impuestos aplicables y forma de pago | Io Marketing / cliente | Ajusta los importes finales y condiciones de pago. |
| Aprobar el checklist de producción y ventana de corte | Firma Bordados | Habilita la migración, sin obligar aún al cambio DNS. |
| Verificar si el formulario real seguirá pendiente o se activará después | Firma Bordados | Evita incluir un proveedor/servicio no aprobado. |

## 6. Recomendación comercial

La propuesta más equilibrada es **Migración única de $6,000 MXN + Mantenimiento Esencial de $4,800 MXN anuales**, para un primer año de **$10,800 MXN más partidas externas**. El cliente recibe una migración reversible y un nivel de operación suficiente para un sitio corporativo estático, sin pagar por formularios, backend o analítica que aún no necesita.

El presupuesto debe presentarse en dos líneas separadas: **servicio profesional de Io Marketing** y **costos de terceros a cargo del cliente**. Esto evita confundir hosting gratuito con mantenimiento sin costo y preserva la separación entre Firma Bordados, Io Marketing y Universe Sent Me.

## Referencias

[1]: [Cloudflare Pages Functions — precios](https://developers.cloudflare.com/pages/functions/pricing/)

[2]: [Cloudflare Registrar — renovaciones a costo](https://www.cloudflare.com/products/registrar/)
