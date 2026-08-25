---
title: "Diseño de formulario, privacidad y entrega de correo — Firma Bordados"
purpose: "Comparar rutas seguras para recibir consultas del sitio y definir los requisitos de privacidad, antispam, entrega de correo y aprobación antes de activar un backend."
status: Review
created: 2026-08-25
updated: 2026-08-24
version: "1.7"
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

### Comparación actual de costo, proveedor y privacidad — 2026-08-24

> Los precios siguientes son tarifas públicas en **USD**, sujetas a impuestos, tipo de cambio y ajustes del proveedor. No constituyen una autorización de compra ni una estimación garantizada. Los equivalentes anuales son una multiplicación de la tarifa mensual pública, no un precio anual contratado.

| Ruta | Costo publicado | Equivalente anual orientativo | Requisitos técnicos | Privacidad y antispam | Viabilidad con las restricciones actuales |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Correo guiado actual | Sin cargo adicional de proveedor | USD 0 | `mailto:`; el visitante pulsa Enviar en su cliente | El sitio no recibe ni almacena datos; aviso actual ya cubre el flujo | **Activa y recomendada mientras funcione** |
| Formspree gestionado | Gratis hasta 50 envíos/mes para pruebas; Personal USD 10/mes por 200 envíos; Professional USD 20/mes por 2,000 envíos.[6] | USD 0 / 120 / 240, respectivamente | Cuenta de Formspree y endpoint del formulario; no exige migrar DNS para enviar al buzón existente | Formspree recibe y archiva consultas; el aviso debe nombrarlo como encargado y reflejar retención. Ofrece filtrado básico, reCAPTCHA, honeypot y restricción por dominio; el control avanzado requiere Professional/Business.[6] [8] | **Posible solo con aprobación explícita de proveedor y condiciones de datos** |
| Pages Function + Cloudflare Email Service | Workers Paid: mínimo USD 5/mes; 3,000 correos/mes incluidos y luego USD 0.35 por 1,000.[3] [9] | Desde USD 60 | Pages Function, Workers Paid, dominio incorporado a Cloudflare Email Service, destino verificado y Cloudflare DNS | Turnstile Free permite hasta 20 widgets y desafíos ilimitados; se debe validar en servidor. El aviso debe reflejar la Function, el manejo de errores y cualquier retención.[4] [5] [10] | **Bloqueada:** Email Service exige Cloudflare DNS y no se permite tocar DNS/nameservers sin autorización separada.[3] |
| Pages Function + Resend | Resend Free: USD 0, hasta 3,000 correos/mes y 100/día; Pro USD 20/mes por 50,000 correos.[11] | USD 0 / 240, más cualquier costo de Function aplicable | Backend, secreto de API y dominio propio verificado en Resend | Resend actúa como encargado; el aviso debe declararlo y ajustar retención. Antispam sigue siendo responsabilidad de la Function: Turnstile validado en servidor, honeypot, límites de longitud/tasa y sin archivos inicialmente.[11] [12] | **Bloqueada:** Resend requiere verificar un dominio propio mediante DNS, que no se modificará sin autorización separada.[12] |

La página de precios de Formspree muestra opciones de facturación mensual y anual, pero sus precios anuales no se exponen de forma estática en la fuente consultada; se deben confirmar en el checkout antes de pagar. Cloudflare Workers se cobra mensualmente; Resend reserva sus suscripciones anuales para Enterprise.[9] [13] No se recomienda asumir que el gasto será anual ni cargarlo contra el presupuesto del cliente sin revisar la pantalla de compra, impuestos y divisa.

**Recomendación actual:** mantener correo guiado por USD 0 adicional. Si se requiere envío directo antes de una migración de DNS, evaluar Formspree primero en el plan Free con consultas sintéticas, sin archivos y con el aviso actualizado, pero solo después de aprobarlo expresamente como encargado de datos. Si más adelante se autoriza una migración de DNS, la opción de mayor control es Pages Function + Turnstile + Cloudflare Email Service; su costo base público sería USD 5/mes y no requiere introducir otro proveedor de envío.

### Propuesta de piloto Formspree Free — pendiente de aprobación

> **No iniciado.** Esta sección describe el único alcance propuesto para decidir si se crea o no una cuenta. No se ha creado cuenta, endpoint, secreto, formulario de envío directo ni flujo de datos hacia Formspree.

| Elemento | Propuesta de piloto | Límite de seguridad y privacidad |
| :--- | :--- | :--- |
| Cuenta y control | Una cuenta de Formspree destinada a Firma Bordados, con acceso limitado a quien atiende el buzón y a la persona autorizada para mantenimiento web | No crear la cuenta hasta recibir autorización expresa; no compartir contraseñas ni incluir credenciales en repositorio. |
| Destino | `firmabordados@yahoo.com`, confirmado como buzón operativo y ARCO | Verificar el buzón mediante el flujo del proveedor; no añadir destinatarios secundarios sin confirmación. |
| Campos | Nombre y correo obligatorios; empresa y teléfono opcionales; mensaje/requerimiento obligatorio | Sin archivos, imágenes, documentos, CURP, datos financieros, sensibles ni listas de personal. |
| Volumen | Formspree Free: hasta 50 envíos por mes; archivo del proveedor de hasta 30 días.[6] | Mantener el flujo de correo guiado como alternativa si se alcanza el límite; no contratar automáticamente. |
| Antispam | Formshield básico del proveedor, restricción al dominio del staging/sitio, honeypot y validación de longitud en frontend | No activar reCAPTCHA de Google en el piloto sin actualizar la revisión de proveedores del aviso; reevaluar si aparece spam. |
| Conservación | Buzón oficial: hasta 12 meses desde la última interacción, conforme a la política operativa propuesta; archivo del proveedor: máximo 30 días en el plan Free.[6] | El aviso debe diferenciar la retención interna de la retención técnica del proveedor. |
| Confirmación al visitante | Pantalla de agradecimiento sin exponer datos enviados; sin autorespuesta en el plan Free | No prometer plazo de respuesta ni registrar analítica de conversión. |

Antes de ejecutar este piloto, Firma Bordados debe aprobar expresamente: **(1)** crear la cuenta de Formspree y aceptar sus términos; **(2)** que Formspree procese los cinco campos anteriores como proveedor/encargado; **(3)** actualizar el aviso para informar el uso del proveedor, su archivo técnico y el canal ARCO; **(4)** verificar `firmabordados@yahoo.com` como destinatario; y **(5)** mantener el límite de 50 envíos/mes sin compra automática. Si alguna condición no se aprueba, se conserva el correo guiado actual.

### Estado del piloto sintético — publicado con destinatario oficial pendiente

El endpoint público `https://formspree.io/f/meajblbz` se integró exclusivamente como piloto de pruebas sintéticas mediante el commit `4378bec`, Pull Request 13 y promoción a `main` con el merge `9522527`. El formulario exige nombre, correo y requerimiento de prueba; empresa y teléfono son opcionales; incluye honeypot `_gotcha`, confirmación obligatoria de que no se enviarán datos reales, ausencia de archivos y un enlace visible al correo guiado oficial. La página de privacidad declara que Formspree participa únicamente en el piloto.

La verificación técnica del staging confirmó HTTP 200 en inicio y privacidad, endpoint presente, aviso de pruebas sintéticas, `firmabordados@yahoo.com` aún visible, ausencia del buzón provisional anterior y `robots.txt` bloqueado. El destinatario `firmabordados@yahoo.com` aún no está verificado dentro de Formspree. Por ello, **no se aceptan consultas reales** ni se debe describir el formulario como canal oficial hasta que el negocio complete la verificación y se haga una revisión separada.

## 6. Decisiones necesarias antes de activar servicios

1. Confirmar la **razón social**, únicamente si es distinta de Firma Bordados, y que el domicilio del negocio es el medio apropiado para el aviso y solicitudes ARCO.
2. Confirmar el correo destinatario y las personas autorizadas para leer y responder consultas. **Confirmado:** `firmabordados@yahoo.com` y una persona responsable interna sin nombre público.
3. Aprobar finalidades, campos, periodo de conservación y medio para solicitudes ARCO. **Propuesta documentada:** doce meses desde la última interacción, sujeta a revisión legal.
4. Elegir: proveedor gestionado temporal o Function propia después de la migración/DNS. **Recomendación actual:** conservar correo guiado hasta tomar esa decisión.
5. Aprobar la creación de widget Turnstile, secretos y cualquier cuenta externa necesaria.
6. Definir si se medirán solo eventos técnicos agregados o se instalará analítica, con su aviso correspondiente.

## 7. Estado

La Etapa A está **activa en staging**. La página estática se publicó en `https://firma-bordados-staging.pages.dev/privacidad/`, se enlaza desde el pie de página y su texto fue aprobado por Fernando el 2026-08-24. El correo guiado se mantiene como canal de solicitud. Un piloto sintético de Formspree quedó publicado, pero no sustituye el correo guiado ni acepta consultas reales hasta verificar el destinatario oficial. Durante los próximos 30 días calendario se observará de forma operativa si las consultas llegan completas, se atienden sin fricción y no se pierden; no se añadirá analítica web para ello. Firma Bordados y el domicilio operativo del negocio quedaron registrados como datos declarados para el aviso. No se ha activado backend propio, Turnstile, analítica, secreto, almacenamiento propio de consultas, cambio DNS ni migración de dominio. La recomendación de la Etapa B permanece en **Review** y requiere decisión explícita antes de cualquier integración externa adicional.

El borrador de aviso integral y simplificado se creó en `2026-08-24_Borrador_Aviso_Privacidad_Firma_Bordados.md` con estado **Draft**. Su publicación sigue bloqueada por las validaciones operativas y legales enumeradas en dicho documento.

## Referencias

[1]: [Ley Federal de Protección de Datos Personales en Posesión de los Particulares — Cámara de Diputados](https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf)

[2]: [Send Emails With Resend — Cloudflare Workers Docs](https://developers.cloudflare.com/workers/tutorials/send-emails-with-resend/)

[3]: [Send emails — Cloudflare Email Service Docs](https://developers.cloudflare.com/email-service/get-started/send-emails/)

[4]: [Create a HTML form — Cloudflare Pages Docs](https://developers.cloudflare.com/pages/tutorials/forms/)

[5]: [Protect your forms — Cloudflare Turnstile Docs](https://developers.cloudflare.com/turnstile/tutorials/login-pages/)

[6]: [Formspree — planes y límites](https://formspree.io/plans)

[7]: [Formspree — seguridad y privacidad](https://formspree.io/security/)

[8]: [Formspree — prevención de spam](https://help.formspree.io/articles/troubleshooting/how-to-prevent-spam)

[9]: [Cloudflare Email Service — precios](https://developers.cloudflare.com/email-service/platform/pricing/)

[10]: [Cloudflare Turnstile — planes](https://developers.cloudflare.com/turnstile/plans/)

[11]: [Resend — precios de correo transaccional](https://resend.com/pricing)

[12]: [Resend — dominios verificados](https://resend.com/docs/dashboard/domains/introduction)

[13]: [Resend — periodicidad y planes anuales](https://resend.com/docs/knowledge-base/what-is-resend-pricing)
