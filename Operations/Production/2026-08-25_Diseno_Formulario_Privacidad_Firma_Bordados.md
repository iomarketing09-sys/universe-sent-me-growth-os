---
title: "Diseño de formulario, privacidad y entrega de correo — Firma Bordados"
purpose: "Comparar rutas seguras para recibir consultas del sitio y definir los requisitos de privacidad, antispam, entrega de correo y aprobación antes de activar un backend."
status: Review
created: 2026-08-25
updated: 2026-08-25
version: "1.1"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-23_Evaluacion_Migracion_Wix_Hosting_IA.md"
  - "Operations/Production/2026-08-23_Guia_Staging_Cloudflare_Pages_Firma_Bordados.md"
  - "Operations/Production/2026-08-24_Backlog_Tecnico_Staging_Firma_Bordados.md"
  - "Operations/Production/2026-08-24_Inventario_Catalogos_Drive_Firma_Bordados.md"
organization: "Operations/Production"
---

# Diseño de formulario, privacidad y entrega de correo — Firma Bordados

## 1. Decisión pendiente

El staging ya muestra un formulario que prepara un correo local y no almacena datos en un servidor. Fernando propuso que la ruta «Cómo solicitar» priorice correo en lugar de WhatsApp. Esta propuesta es compatible con el estado actual: un enlace `mailto:` prellenado guía la solicitud sin crear una base de datos ni activar un proveedor externo. WhatsApp debe conservarse como canal alternativo visible, no como el destino principal de esa ruta.

Un formulario con envío automático requiere una decisión separada, ya que empezaría a tratar datos personales de prospectos. No debe activarse en la cuenta temporal de Io Marketing, ni con secretos o proveedores externos, hasta confirmar responsable, destinatario, aviso de privacidad y operación posterior.

## 2. Datos mínimos y límites de captura

| Campo | Estado propuesto | Finalidad limitada | Regla |
| :--- | :--- | :--- | :--- |
| Nombre | Requerido | Identificar la consulta y responder | No pedir CURP, identificación ni datos sensibles. |
| Correo electrónico | Requerido para backend; opcional en `mailto:` | Responder la solicitud | No usar para newsletter o promociones sin finalidad y consentimiento separados. |
| Empresa | Opcional | Contextualizar una solicitud B2B | No convertirlo en perfil comercial automático. |
| Teléfono | Opcional | Canal alternativo de respuesta si la persona lo solicita | No usar para campañas masivas. |
| Mensaje / requerimiento | Requerido | Entender prenda, técnica y cantidad aproximada | Instruir al visitante a no incluir datos sensibles, financieros o personales de terceros. |

El formulario no debe pedir materiales de clientes, archivos, listas de personal, fotografías de identificaciones, datos de salud ni información financiera. Los archivos y cotizaciones se gestionarán solo después por el canal que el equipo defina.

## 3. Aviso de privacidad mínimo

La Ley Federal de Protección de Datos Personales en Posesión de los Particulares exige que el aviso informe, entre otros elementos, identidad y domicilio del responsable, datos tratados, finalidades, medios para limitar uso/divulgación, procedimientos ARCO y cómo se comunicarán cambios.[1] Cuando los datos se recaban electrónicamente, la modalidad simplificada debe estar disponible en ese momento e indicar dónde consultar el aviso integral.[1]

La implementación debe colocar junto al botón de envío un enlace visible al aviso simplificado y un enlace al aviso integral. El texto se elaborará con los datos reales del responsable y deberá revisarse por el cliente o asesor legal antes de activarse. Como contenido mínimo, debe declarar que los datos se usan para atender, dar seguimiento y, cuando proceda, cotizar la solicitud; identificar al responsable y un correo o medio ARCO; explicar el plazo de conservación; y revelar los proveedores que procesen la información en nombre del responsable.

> **Regla operativa:** el aviso no debe afirmar que no existen transferencias o procesadores si se usa un proveedor de formularios, correo o antispam. Esa relación debe identificarse correctamente antes de publicar el formulario.

## 4. Alternativas técnicas

| Alternativa | Flujo de datos | Antispam | Requisitos | Ventaja | Límite / decisión necesaria |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Correo guiado (`mailto:`)** | El navegador abre el cliente de correo del visitante; el staging no recibe ni guarda datos | Ninguno en el sitio | Ningún secreto, DNS ni proveedor | Es la ruta más prudente y disponible ahora | Depende de que el visitante tenga correo configurado; no permite métricas de envío. |
| **Servicio gestionado de formularios** | Visitante → proveedor de formularios → correo del negocio | Generalmente incluido por el proveedor; Turnstile puede añadirse | Aprobación de proveedor, términos, privacidad, destinatario y plan | Se implementa sin backend propio ni cambio inmediato de DNS | El proveedor se vuelve encargado del tratamiento; se requiere revisar su aviso/retención y documentarlo. |
| **Pages Functions + Turnstile + Resend** | Visitante → Function → verificación Turnstile → correo transaccional | Turnstile verificado en servidor | Cuenta Cloudflare, widget/secret Turnstile, dominio remitente verificado, cuenta Resend y secreto de API | Control de validación, datos mínimos y sin base de datos si solo se reenvía por correo | Resend requiere un dominio registrado/verificado y sus registros DNS; no procede mientras el dominio y DNS sigan fuera de la operación aprobada.[2] |
| **Pages Functions + Turnstile + Cloudflare Email Service** | Visitante → Function → verificación Turnstile → correo nativo Cloudflare | Turnstile verificado en servidor | Cloudflare DNS, dominio integrado al Email Service y binding de correo | Evita una API de correo de tercero en el runtime | Email Service exige usar Cloudflare DNS; queda para después del gate de migración del dominio.[3] |

Cloudflare Pages puede enrutar un `POST` hacia una Function y procesar el `FormData` en un Worker.[4] Turnstile requiere que el token se compruebe del lado del servidor y que la validación se ejecute al enviar el formulario, no antes.[5] No se deben enviar secretos al navegador ni poner llaves de correo en el repositorio.

## 5. Recomendación por etapas

### Etapa A — aplicada, sin backend

El 2026-08-25 se cambió la sección «Cómo solicitar» para abrir un correo prellenado a `firmabordados@yahoo.com`, con campos opcionales de prenda, técnica, cantidad aproximada y uso. WhatsApp se conserva como CTA del hero y canal alternativo de contacto. Este ajuste no recoge ni retiene información dentro del sitio, no activa proveedores ni secretos, y se publicó mediante Pull Request 8, CI en `staging` y `main`, y promoción explícita a la rama que sirve Pages.

### Etapa B — producción, tras decisión de operación

La ruta recomendada es **Pages Function + Turnstile + proveedor de correo verificado**, sin base de datos de consultas por defecto. El endpoint debe aceptar solo los campos definidos, aplicar límites de longitud, usar honeypot y rate limiting, verificar Turnstile en el servidor, enviar el correo al destinatario autorizado y devolver una respuesta genérica. Los secretos deben vivir exclusivamente en la configuración segura del proveedor, nunca en el repositorio o frontend.

Si el dominio se transfiere a Cloudflare DNS como parte de la migración final, se puede reevaluar Cloudflare Email Service. Si el cliente necesita el formulario antes de ese cambio, deberá aprobar expresamente un proveedor gestionado y sus condiciones de tratamiento de datos.

## 6. Decisiones necesarias antes de activar servicios

1. Confirmar quién será el **responsable** del tratamiento y su domicilio operativo para el aviso.
2. Confirmar el correo destinatario y las personas autorizadas para leer y responder consultas.
3. Aprobar finalidades, campos, periodo de conservación y medio para solicitudes ARCO.
4. Elegir: proveedor gestionado temporal o Function propia después de la migración/DNS.
5. Aprobar la creación de widget Turnstile, secretos y cualquier cuenta externa necesaria.
6. Definir si se medirán solo eventos técnicos agregados o se instalará analítica, con su aviso correspondiente.

## 7. Estado

La Etapa A está **aplicada**. No se ha activado backend, proveedor de correo, Turnstile, analítica, secreto, almacenamiento de consultas, cambio DNS ni migración de dominio. La recomendación de la Etapa B permanece en **Review** y requiere decisión explícita antes de cualquier integración externa.

## Referencias

[1]: [Ley Federal de Protección de Datos Personales en Posesión de los Particulares — Cámara de Diputados](https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf)

[2]: [Send Emails With Resend — Cloudflare Workers Docs](https://developers.cloudflare.com/workers/tutorials/send-emails-with-resend/)

[3]: [Send emails — Cloudflare Email Service Docs](https://developers.cloudflare.com/email-service/get-started/send-emails/)

[4]: [Create a HTML form — Cloudflare Pages Docs](https://developers.cloudflare.com/pages/tutorials/forms/)

[5]: [Protect your forms — Cloudflare Turnstile Docs](https://developers.cloudflare.com/turnstile/tutorials/login-pages/)
