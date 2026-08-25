---
title: "Diseño de formulario, privacidad y entrega de correo — Firma Bordados"
purpose: "Comparar rutas seguras para recibir consultas del sitio y definir los requisitos de privacidad, antispam, entrega de correo y aprobación antes de activar un backend."
status: Review
created: 2026-08-25
updated: 2026-08-25
version: "1.3"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-24_Borrador_Aviso_Privacidad_Firma_Bordados.md"
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

| Elemento | Confirmación recibida | Uso permitido en este diseño | Pendiente antes de publicar |
| :--- | :--- | :--- | :--- |
| Empresa responsable declarada | **Firma Bordados** | Identificar a la empresa responsable en el borrador interno del aviso | Confirmar la razón social únicamente si es distinta del nombre comercial que debe aparecer públicamente. |
| Domicilio del responsable | Emilio Carranza #1021 Int. 113, Col. Burócratas, Piedras Negras, Coahuila | Usar el domicilio operativo ya visible y confirmado del negocio | Confirmar que es el domicilio apropiado para el aviso y el medio de recepción de solicitudes ARCO. |

La implementación debe colocar junto al botón de envío un enlace visible al aviso simplificado y un enlace al aviso integral. El texto se elaborará con los datos reales del responsable y deberá revisarse por el cliente o asesor legal antes de activarse. Como contenido mínimo, debe declarar que los datos se usan para atender, dar seguimiento y, cuando proceda, cotizar la solicitud; identificar al responsable y un correo o medio ARCO; explicar el plazo de conservación; y revelar los proveedores que procesen la información en nombre del responsable.

### 3.1 Confirmaciones operativas — 2026-08-24

| Punto | Confirmación recibida | Aplicación documentada |
| :--- | :--- | :--- |
| Canal de privacidad y ARCO | `firmabordados@yahoo.com` | Será el correo indicado para consultas de privacidad, limitación de uso, revocación y solicitudes ARCO. |
| Atención del buzón | Firma Bordados asignará a una persona responsable de revisar esos correos | No se nombra a la persona públicamente; el equipo debe asegurar continuidad de atención. |
| Conservación | Se solicita un plazo razonable y practicable | Se propone conservar consultas **hasta 12 meses desde la última interacción** y después eliminarlas o disociarlas, salvo que se formalice una relación comercial o exista una obligación legal/contractual aplicable. La revisión legal debe validar este criterio antes de publicarlo. |
| Página del aviso | Se confirma crearla cuando exista un formulario | El aviso integral se publicará como página propia antes de activar la captura de datos; por ahora el correo guiado continúa sin backend. |

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

### Propuesta técnica recomendada — sin activación todavía

| Momento | Ruta propuesta | Por qué | Condición antes de ejecutar |
| :--- | :--- | :--- |
| **Ahora** | Mantener correo guiado y finalizar/revisar el aviso de privacidad | No captura datos en el sitio, no exige secretos ni DNS y conserva WhatsApp como alternativa | Publicar el aviso solo cuando la empresa apruebe la versión final. |
| **Si se requiere formulario antes de mover DNS** | Servicio gestionado de formularios, evaluado y aprobado por Firma Bordados | Evita construir un backend propio antes de disponer de un dominio remitente verificado | Aprobación explícita del proveedor, condiciones de tratamiento, retención, destinatario y antispam. |
| **Después de una migración aprobada de DNS/dominio** | Pages Function + Turnstile + Cloudflare Email Service | Mantiene la validación y el reenvío de correo dentro de la plataforma Cloudflare | Cloudflare DNS, dominio incorporado al servicio, widget Turnstile, secretos y pruebas de entrega aprobadas.[3] [5] |

La recomendación es **no sustituir el correo guiado todavía**. Cuando exista un formulario, debe recibir solo nombre, correo, empresa/teléfono opcionales y requerimiento; añadir honeypot, límites de longitud y tasa, y verificar Turnstile del lado del servidor en cada envío. El widget por sí solo no protege el endpoint; la validación `Siteverify` en servidor es obligatoria.[5] Resend no es la ruta preferida en la configuración actual porque exige un dominio registrado/verificado y registros DNS; no se tocarán DNS ni dominio sin una autorización separada.[2]

## 6. Decisiones necesarias antes de activar servicios

1. Confirmar la **razón social**, únicamente si es distinta de Firma Bordados, y que el domicilio del negocio es el medio apropiado para el aviso y solicitudes ARCO.
2. Confirmar el correo destinatario y las personas autorizadas para leer y responder consultas. **Confirmado:** `firmabordados@yahoo.com` y una persona responsable interna sin nombre público.
3. Aprobar finalidades, campos, periodo de conservación y medio para solicitudes ARCO. **Propuesta documentada:** doce meses desde la última interacción, sujeta a revisión legal.
4. Elegir: proveedor gestionado temporal o Function propia después de la migración/DNS. **Recomendación actual:** conservar correo guiado hasta tomar esa decisión.
5. Aprobar la creación de widget Turnstile, secretos y cualquier cuenta externa necesaria.
6. Definir si se medirán solo eventos técnicos agregados o se instalará analítica, con su aviso correspondiente.

## 7. Estado

La Etapa A está **aplicada**. Firma Bordados y el domicilio operativo del negocio quedaron registrados como datos declarados para preparar el aviso, pero no constituyen un aviso de privacidad definitivo ni una validación legal. No se ha activado backend, proveedor de correo, Turnstile, analítica, secreto, almacenamiento de consultas, cambio DNS ni migración de dominio. La recomendación de la Etapa B permanece en **Review** y requiere decisión explícita antes de cualquier integración externa.

El borrador de aviso integral y simplificado se creó en `2026-08-24_Borrador_Aviso_Privacidad_Firma_Bordados.md` con estado **Draft**. Su publicación sigue bloqueada por las validaciones operativas y legales enumeradas en dicho documento.

## Referencias

[1]: [Ley Federal de Protección de Datos Personales en Posesión de los Particulares — Cámara de Diputados](https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf)

[2]: [Send Emails With Resend — Cloudflare Workers Docs](https://developers.cloudflare.com/workers/tutorials/send-emails-with-resend/)

[3]: [Send emails — Cloudflare Email Service Docs](https://developers.cloudflare.com/email-service/get-started/send-emails/)

[4]: [Create a HTML form — Cloudflare Pages Docs](https://developers.cloudflare.com/pages/tutorials/forms/)

[5]: [Protect your forms — Cloudflare Turnstile Docs](https://developers.cloudflare.com/turnstile/tutorials/login-pages/)
