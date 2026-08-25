---
title: "Borrador de aviso de privacidad — Firma Bordados"
purpose: "Proponer un aviso de privacidad integral y un aviso simplificado para una futura captura de consultas, usando únicamente los datos confirmados y señalando los puntos que requieren validación antes de publicarse."
status: Review
created: 2026-08-24
updated: 2026-08-24
version: "0.3"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-25_Diseno_Formulario_Privacidad_Firma_Bordados.md"
  - "Operations/Production/2026-08-23_Guia_Staging_Cloudflare_Pages_Firma_Bordados.md"
  - "Operations/Production/2026-08-24_Backlog_Tecnico_Staging_Firma_Bordados.md"
  - "Operations/Production/todo.md"
organization: "Operations/Production"
---

# Borrador de aviso de privacidad — Firma Bordados

> **Borrador de trabajo — no publicar todavía.** Este texto no es asesoría legal ni sustituye la revisión de Firma Bordados o de un asesor legal. Debe validarse antes de ponerlo junto a un formulario, activar un backend o afirmar que describe la operación vigente.

## 1. Alcance del borrador

Este documento propone el contenido de un aviso integral y de su versión simplificada para una futura captura digital de consultas. La Ley Federal de Protección de Datos Personales en Posesión de los Particulares exige que el aviso incluya, al menos, identidad y domicilio del responsable, datos tratados, finalidades, medios para limitar uso o divulgación, mecanismos ARCO y la forma de comunicar cambios. Cuando los datos se recaban electrónicamente, la versión simplificada debe estar disponible al momento de recabarlos e indicar dónde consultar el aviso integral.[1]

El staging actual de Firma Bordados usa enlaces de correo guiado y no recibe ni almacena datos en un servidor. Esta versión se publicó únicamente para revisión en la ruta estática `/privacidad/` del staging. No activa una captura de datos, no sustituye la revisión legal y debe actualizarse antes de implementar cualquier formulario con backend o proveedor externo.

## 2. Datos que sustentan esta propuesta

| Elemento | Dato confirmado | Nota de publicación |
| :--- | :--- | :--- |
| Empresa responsable declarada | Firma Bordados | Confirmar la razón social únicamente si es distinta del nombre comercial que se mostrará públicamente. |
| Domicilio | Emilio Carranza #1021 Int. 113, Col. Burócratas, Piedras Negras, Coahuila | Confirmar que este domicilio se usará para el aviso y, en su caso, para solicitudes ARCO. |
| Correo de contacto | firmabordados@yahoo.com | Confirmado como canal para privacidad, ARCO, revocación y limitación de uso; Firma Bordados asignará atención interna. |
| Formulario/back-end | No activo | No declarar proveedor, Turnstile, analítica, transferencia ni almacenamiento hasta conocer la configuración real. |

## 3. Propuesta de aviso de privacidad integral

### Aviso de privacidad integral de Firma Bordados

**Última actualización propuesta:** 24 de agosto de 2026. **Versión:** borrador 0.1.

**Responsable.** Firma Bordados, con domicilio en Emilio Carranza #1021 Int. 113, Col. Burócratas, Piedras Negras, Coahuila, es responsable del tratamiento de los datos personales que se describen en este aviso. Antes de publicar este texto se confirmará la razón social solo si es distinta del nombre comercial que se mostrará públicamente.

**Datos personales que podrán tratarse.** Para atender una solicitud de información o cotización, Firma Bordados podrá tratar nombre, correo electrónico, teléfono, empresa —cuando la persona decida proporcionarlo— y los datos incluidos en la consulta, como tipo de prenda, técnica de interés, cantidad aproximada y uso o requerimiento. Firma Bordados no solicita datos personales sensibles, financieros, patrimoniales ni documentos de identificación para esta finalidad; se pide no enviarlos por el formulario o correo de consulta.

**Finalidades primarias.** Los datos se usarán para recibir y atender la consulta, comunicarse con la persona solicitante, comprender sus necesidades de prendas, bordado o serigrafía, preparar o dar seguimiento a una posible cotización y, si se contrata un servicio, gestionar la comunicación relacionada con ese servicio. Estas finalidades son necesarias para atender la solicitud iniciada por la persona titular.

**Finalidades secundarias.** En esta propuesta, Firma Bordados no usará los datos de consulta para campañas, boletines o publicidad. Si posteriormente se desea usar información para una finalidad secundaria, se deberá actualizar el aviso y recabar el consentimiento que resulte aplicable antes de hacerlo.

**Opciones para limitar uso o divulgación.** La persona titular podrá solicitar que sus datos no se usen para finalidades distintas de atender su consulta, o pedir que dejen de usarse conforme sea procedente, enviando un correo a `firmabordados@yahoo.com` con el asunto “Privacidad — limitar uso de datos”. Firma Bordados confirmó que asignará a una persona responsable de revisar estos correos. Esa persona no se identifica públicamente en este aviso.

**Derechos ARCO.** La persona titular puede solicitar acceso a sus datos, su rectificación si son inexactos o incompletos, su cancelación cuando proceda, u oponerse al tratamiento en los casos aplicables. Para iniciar una solicitud ARCO, deberá enviar un correo a `firmabordados@yahoo.com` con el asunto “Solicitud ARCO”, indicando su nombre, un medio para recibir respuesta, el derecho que desea ejercer y una descripción clara de los datos o la solicitud. Firma Bordados podrá solicitar la información necesaria para verificar identidad y dar trámite a la petición conforme a los plazos y requisitos aplicables. Se recomienda no enviar documentos de identidad ni datos sensibles por correo salvo que el responsable lo solicite por un canal adecuado.

**Revocación del consentimiento.** Cuando el tratamiento se base en consentimiento y sea procedente revocarlo, la persona titular podrá solicitarlo por el mismo correo, con el asunto “Privacidad — revocación de consentimiento”. La revocación no tendrá efectos retroactivos y podrá estar sujeta a las obligaciones legales o contractuales que correspondan.

**Conservación.** Como política operativa propuesta, las consultas se conservarán hasta por doce meses contados desde la última interacción y posteriormente se eliminarán o disociarán, salvo que se formalice una relación comercial o resulte aplicable una obligación legal o contractual de conservación. Este periodo debe ser confirmado por Firma Bordados y revisado antes de publicar el aviso definitivo.

**Transferencias y personas encargadas.** Con la información disponible al elaborar este borrador, no se contemplan transferencias de datos personales para fines comerciales. Antes de activar un formulario, servicio de correo transaccional, antispam, analítica o proveedor externo, Firma Bordados deberá revisar si ese tercero tratará datos por cuenta del responsable o si existe una transferencia que deba declararse y, de ser necesario, actualizar este aviso antes de iniciar la captura.

**Medidas de seguridad.** Firma Bordados procurará aplicar medidas administrativas, técnicas y físicas razonables, según la naturaleza de los datos y la operación vigente, para evitar su daño, pérdida, alteración, destrucción, uso, acceso o tratamiento no autorizado. Las personas que atiendan consultas deberán acceder solo cuando sea necesario para cumplir las finalidades descritas.

**Cambios al aviso.** Cualquier modificación relevante se comunicará mediante la sección de aviso de privacidad del sitio web de Firma Bordados o por el medio que se informe en la versión vigente. Antes de publicar se debe definir y mantener accesible la URL final del aviso integral.

**Contacto.** Para dudas sobre este aviso o sobre el tratamiento de datos, la persona titular podrá escribir a `firmabordados@yahoo.com` con el asunto “Privacidad — consulta”.

## 4. Propuesta de aviso de privacidad simplificado para un formulario futuro

> **Aviso de privacidad simplificado — borrador.** Firma Bordados, con domicilio en Emilio Carranza #1021 Int. 113, Col. Burócratas, Piedras Negras, Coahuila, tratará su nombre, correo, teléfono, empresa —si lo proporciona— y datos de su solicitud para atenderla, comunicarse con usted y preparar o dar seguimiento a una posible cotización. Puede solicitar limitar el uso de sus datos en `firmabordados@yahoo.com`. Consulte el aviso de privacidad integral en **[URL pendiente de definir antes de publicar]**.

El aviso simplificado debe aparecer junto al botón de envío del formulario futuro, con un enlace funcional al aviso integral. No debe usarse junto al correo guiado actual, porque esa ruta no captura datos en el sitio.

## 4.1 Publicación de revisión en staging

El 2026-08-24, el contenido integral de este borrador se adaptó a una página estática en `https://firma-bordados-staging.pages.dev/privacidad/`, accesible desde el pie de página. La publicación pasó Pull Request 9, CI en `staging` y `main`, y una corrección posterior de la ruta canónica pasó Pull Request 10 y CI. La comprobación HTTP confirmó respuesta 200 de la ruta con barra final, presencia del correo de privacidad, la política propuesta de doce meses, ausencia de nombres personales retirados y continuidad de `robots.txt` con bloqueo de indexación. No se activaron backend, formulario servidor-side, Turnstile, proveedor, secreto, analítica, almacenamiento, Wix, DNS, nameservers ni dominio público.

## 5. Validaciones pendientes antes de publicación

| Validación | Responsable de confirmar | Motivo |
| :--- | :--- | :--- |
| Razón social, si es distinta de Firma Bordados | Firma Bordados | Evitar presentar una identidad comercial o jurídica inexacta. |
| Buzón y personas autorizadas para privacidad/ARCO | Confirmado por Firma Bordados | El correo será atendido por una persona responsable interna no identificada públicamente. |
| Periodo de conservación y criterio de eliminación | Firma Bordados | Se propone doce meses desde la última interacción; requiere revisión antes de publicar. |
| URL pública del aviso integral | Equipo web, tras aprobación | Evitar enlazar a una página inexistente. |
| Proveedor de formulario, correo, antispam y analítica | Firma Bordados y equipo web | Declarar correctamente el tratamiento por terceros antes de capturar datos. |
| Revisión legal y autorización de publicación | Firma Bordados o asesor legal | Confirmar adecuación a la operación real antes de depender del aviso. |

## Referencias

[1]: [Ley Federal de Protección de Datos Personales en Posesión de los Particulares — Cámara de Diputados](https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf)
