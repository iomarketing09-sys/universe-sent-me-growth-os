# Evaluación de migración Wix, hosting externo y trabajo de IA

**Propósito:** Evaluar si un sitio sencillo de un cliente —información empresarial, contacto y tres catálogos en PDF— puede reconstruirse fuera de Wix para reducir dependencia del plan actual y asignar cualquier presupuesto liberado únicamente mediante una propuesta y aprobación separadas.

**Estado:** Review

**Fecha de creación:** 2026-08-23

**Última actualización:** 2026-08-23

**Versión:** 1.1

**Autor:** Manus AI

**Organización:** `Operations/Production`

**Documentos relacionados:** [`2026-08-18_Piloto_Local_OmniRoute_Seguro.md`](2026-08-18_Piloto_Local_OmniRoute_Seguro.md), [`2026-08-19_Decision_Gateway_IA_OmniRoute.md`](2026-08-19_Decision_Gateway_IA_OmniRoute.md).

---

## Conclusión ejecutiva

El sitio no puede exportarse desde Wix como el mismo sitio listo para ejecutarse en otro hosting. Wix explica que su editor utiliza una arquitectura SaaS propietaria y que el sitio debe permanecer alojado y operado en sus servidores; el contenido pertenece al usuario, pero la implementación depende de Wix. [1]

La alternativa viable es **reconstruir el sitio** como una página estática o como un sitio pequeño con un backend externo para el contacto. Después se puede probar en una URL temporal y conectar el dominio existente mediante DNS. Wix permite apuntar un dominio comprado en Wix a un sitio externo usando registros A y CNAME; no se debe cambiar DNS ni cancelar el plan hasta que el cliente apruebe la versión nueva y se comprueben sitio, PDFs, formularios, correo y SEO básico. [2]

El presupuesto que eventualmente se libere sigue siendo del cliente. No debe transferirse automáticamente a Universe Sent Me ni a OmniRoute. Si el cliente desea financiar funciones adicionales, debe existir una propuesta separada que indique alcance, horas, hosting, uso de IA, mantenimiento, propiedad de los entregables y autorización expresa.

## Resultado de la auditoría pública inicial

La revisión pública confirmó una página corporativa de una sola página con navegación superior, secciones de trabajos, información institucional, tres catálogos PDF y contacto. El contenido visible incluye una propuesta de servicios de bordado, experiencia de la empresa, dirección, teléfono, horario y un formulario básico. También se observó un botón flotante de chat y una imagen principal con un logotipo de tercero; cualquier marca o fotografía de cliente debe contar con autorización antes de reutilizarse.

La reconstrucción no debe ser una copia literal. La dirección aprobada es una modernización conservadora con una primera pantalla más clara, propuesta de valor y CTA de contacto; una galería de trabajos más ordenada; tarjetas para los tres catálogos; una sección de servicios o proceso; y un contacto accesible con teléfono, correo, horario, dirección y formulario simple. El rediseño debe priorizar móvil, contraste, foco de teclado, encabezados semánticos, texto alternativo, compresión de imágenes y navegación directa a catálogos y contacto.

La auditoría no envió el formulario, no interactuó con el chat, no descargó los PDFs y no modificó el sitio ni el DNS. Los tres PDFs suman aproximadamente 24.1 MB según el usuario; antes de elegir hosting se debe comprobar el tamaño de cada archivo, porque los límites se aplican por activo individual y no solo al total.

## Inventario previo obligatorio

Antes de elegir hosting, documentar sin publicar credenciales:

| Elemento | Qué verificar | Motivo |
|---|---|---|
| Páginas | Inicio, empresa, contacto y cualquier página oculta | Evitar perder contenido o enlaces existentes. |
| PDFs | Nombre, URL actual, tamaño, versión y derechos de uso | Confirmar que cada catálogo pueda hospedarse en el nuevo sitio. |
| Contacto | Formulario Wix, correo, teléfono, WhatsApp o CRM | Un sitio estático no reemplaza por sí solo el procesamiento seguro de formularios. |
| Dominio | Quién es registrante, renovación y método de gestión | Evitar perder el dominio o interrumpir renovaciones. |
| Correo | Registros MX y proveedor de correo empresarial | Cambiar DNS incorrectamente puede interrumpir el correo. |
| SEO | Títulos, descripciones, URLs, favicon, sitemap y Search Console | Reducir pérdida de visibilidad durante el cambio. |
| Analítica | Google Analytics, píxeles y consentimientos | Revisar qué scripts deben reconstruirse y con qué autorización. |
| Funciones Wix | Reservas, pagos, miembros, blog, apps o automatizaciones | Si existen, la reconstrucción estática podría no ser suficiente. |

## Opciones de hosting

| Opción | Ventaja | Limitación | Coste inicial | Complejidad |
|---|---|---|---:|---:|
| **Cloudflare Pages** | Adecuado para sitio estático, despliegues desde Git y dominio personalizado. | Para el dominio raíz normalmente requiere gestionar la zona y nameservers en Cloudflare; cada PDF debe respetar el límite de tamaño del plan. | $0 en el plan Free, sujeto a límites vigentes | Baja-media |
| **GitHub Pages** | Hosting estático sencillo con dominio personalizado y flujo basado en Git. | No es un backend de formularios; requiere resolver contacto y secretos fuera del repositorio. | $0 para la capacidad elegible, más dominio | Baja |
| **Netlify Free** | Despliegue sencillo, dominio personalizado con SSL y funciones disponibles dentro de su plan. | El plan usa límites de créditos/uso que deben vigilarse; no asumir costo cero ilimitado. | $0 en el plan Free, sujeto a límites | Baja |
| **Continuar en Wix** | No hay migración, DNS ni reconstrucción. | Se mantiene el costo del plan y no se reutiliza esa infraestructura para alojar OmniRoute. | Plan actual del cliente | Muy baja |

Cloudflare Pages documenta en su plan Free hasta 500 builds mensuales, hasta 100 dominios personalizados por proyecto, 20.000 archivos y un límite de 25 MiB por activo. [3] Netlify publica un plan Free de $0 con dominios personalizados y SSL, pero también muestra un sistema de créditos y límites de uso que deben revisarse antes de prometer costo cero. [4] GitHub Pages documenta el uso de dominios personalizados, pero no debe tratarse como un servicio de backend o de almacenamiento de secretos. [5]

## Recomendación preliminar

Para este caso, la mejor ruta de evaluación es **reconstrucción estática + Cloudflare Pages o GitHub Pages**, manteniendo inicialmente el dominio registrado en Wix. La página descrita tiene pocos contenidos dinámicos y los catálogos PDF pueden ser enlaces o descargas si cada archivo está dentro del límite del hosting elegido.

El contacto debe resolverse de manera explícita. Si solo se necesita mostrar teléfono, correo o WhatsApp, se pueden usar enlaces directos autorizados. Si se requiere un formulario, se debe usar un endpoint/backend o servicio de formularios con política de privacidad, protección antispam, límites y almacenamiento controlado. No se deben poner API keys en el JavaScript público.

No se recomienda alojar OmniRoute dentro de la misma página estática. OmniRoute debe permanecer como un servicio privado separado. La página del cliente solo podría consumir una función de IA mediante un backend propio, después de que el cliente solicite y apruebe esa función como alcance adicional. La decisión vigente del proyecto mantiene el frontend fuera del acceso directo a OmniRoute y exige un backend privado para cualquier integración de producción. [6]

## Plan de migración reversible

1. Obtener autorización escrita del cliente para reconstruir una copia y confirmar quién posee textos, imágenes, PDFs, dominio y correo.
2. Exportar o recopilar manualmente el contenido permitido de Wix, descargar los tres PDFs y verificar tamaños, versiones y permisos.
3. Construir una copia estática en una URL temporal, sin modificar todavía DNS ni cancelar Wix.
4. Comprobar responsive design, accesibilidad básica, enlaces, descargas, formulario/contacto, títulos, favicon, HTTPS y redirecciones.
5. Ejecutar una revisión del cliente y corregir diferencias.
6. Preparar el cambio DNS. Wix indica que para apuntar a un host externo se actualizan registros A y CNAME; los cambios pueden tardar hasta 48 horas en propagarse. [2]
7. Mantener Wix activo durante la propagación y confirmar desde varios dispositivos que el nuevo sitio funciona.
8. Revisar correo empresarial y registros MX antes de cancelar cualquier servicio. Wix advierte que el correo necesita sus registros MX después de una transferencia de dominio. [3]
9. Cancelar o reducir el plan Wix únicamente después de que el cliente confirme por escrito que el nuevo sitio y el dominio funcionan.

La transferencia del dominio fuera de Wix es opcional. Si se realiza, Wix indica que el nuevo proveedor asumirá datos de contacto, DNS y renovaciones, que la transferencia suele tardar hasta siete días y que pueden aplicar bloqueos de transferencia de 60 días. [3] Para reducir riesgo, la primera versión debería mantener el dominio con Wix y solo apuntarlo por DNS al nuevo hosting, si el host lo permite.

## Separación del presupuesto y de los proyectos

El ahorro del plan Wix no es automáticamente presupuesto de Universe Sent Me. Debe presentarse al cliente una propuesta con al menos dos partidas separadas:

| Partida | Propietario | Ejemplos |
|---|---|---|
| Migración y operación del sitio del cliente | Cliente | Reconstrucción, PDFs, DNS, formulario, mantenimiento y hosting. |
| Trabajo adicional solicitado por el cliente | Cliente, con aprobación | Automatización editorial, copy, analítica o integración autorizada. |
| Desarrollo de Universe Sent Me | Universe Sent Me | OmniRoute, Growth OS, personajes, documentación y pruebas internas. |

Aunque el cliente quiera financiar trabajo adicional, no se deben reutilizar sus credenciales, PDFs, datos de contacto, audiencia, dominio o contenido para Universe Sent Me. Los proyectos deben tener repositorios, cuentas, claves, facturación y respaldos separados.

## Integración futura de IA

Si el cliente solicita una función de IA, la primera versión debe ser un endpoint de borradores detrás de un backend privado, no una llamada desde el navegador. Debe aceptar un propósito limitado, validar tamaño y contenido, excluir secretos y datos personales, aplicar autenticación y rate limiting, registrar provider/modelo/latencia/estado y devolver una respuesta marcada como `Draft`. No debe publicar automáticamente ni escribir en los ledgers de Universe Sent Me.

El Combo `usm-groq-gemini-priority` pertenece al piloto de Universe Sent Me y no debe conectarse al sitio del cliente sin una separación de infraestructura y una aprobación específica. Si se necesita IA para el cliente, se debe decidir si conviene un provider directo o una instancia de OmniRoute separada con sus propias claves, volumen, logs y política de retención.

## Decisión pendiente

No iniciar una migración irreversible todavía. Primero se necesitan: costo actual y fecha de renovación de Wix, confirmación sobre correo empresarial, listado de funciones activas, tamaño de los tres PDFs, preferencia de hosting, necesidad real de formulario y autorización del cliente para reconstrucción y cambio DNS.

Si el inventario confirma que el sitio es realmente estático, se puede preparar una copia de prueba. La cancelación de Wix, transferencia del dominio y asignación de presupuesto para IA quedan bloqueadas hasta que el cliente apruebe el alcance, el costo y la nueva versión.

## Documentos que requieren actualización si se aprueba la integración

La evaluación no cambia todavía los ledgers ni el dashboard de Growth OS. Si se aprueba una integración de IA para el cliente, deberán crearse documentos operativos separados para esa cuenta y actualizarse la decisión de OmniRoute con el alcance, las credenciales separadas, el hosting, la retención y el responsable. No se deben mezclar los documentos canónicos del cliente con los de Universe Sent Me.

## Referencias

[1]: [Wix — Exporting or Embedding Your Wix Site Elsewhere](https://support.wix.com/en/article/exporting-or-embedding-your-wix-site-elsewhere)

[2]: [Wix — Connecting a Wix Domain to an External Site](https://support.wix.com/en/article/connecting-a-wix-domain-to-an-external-site)

[3]: [Wix — Transferring Your Wix Domain Away from Wix](https://support.wix.com/en/article/transferring-your-wix-domain-away-from-wix-2477749)

[4]: [Netlify — Pricing](https://www.netlify.com/pricing/)

[5]: [GitHub Docs — Configuring a Custom Domain for GitHub Pages](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

[6]: [Universe Sent Me — Decisión de uso de OmniRoute](2026-08-19_Decision_Gateway_IA_OmniRoute.md)
