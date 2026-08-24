---
title: "Ruta de staging WordPress para Firma Bordados"
purpose: "Definir una alternativa de hosting y administración basada en WordPress.com para Firma Bordados, sin modificar Wix ni DNS hasta que el cliente apruebe el sitio reconstruido."
status: Review
created: 2026-08-23
updated: 2026-08-23
version: "1.0"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-23_Evaluacion_Migracion_Wix_Hosting_IA.md"
  - "Operations/Production/2026-08-23_Guia_Staging_Cloudflare_Pages_Firma_Bordados.md"
  - "GrowthOS/00_01_Changelog_GrowthOS.md"
organization: "Operations/Production"
---

# Ruta de staging WordPress para Firma Bordados

## 1. Aclaración de arquitectura

Esta ruta sustituye **Cloudflare Pages como host principal** por **WordPress.com**. Cloudflare puede no utilizarse; no es requisito para alojar ni administrar el sitio en WordPress.com. Wix seguirá siendo el host público de `firmabordados.com` hasta la aprobación formal del cliente y el corte posterior.

No se debe instalar WordPress en el iMac, en OmniRoute, ni en una instancia de Universe Sent Me. El cliente necesita una cuenta propia de WordPress.com y una suscripción propia. El dominio puede conservarse registrado en Wix; conectar el dominio a WordPress.com no exige transferir su registro, pero sí requiere un cambio DNS cuando llegue el momento de producción. [1]

| Opción | Qué es | Encaje actual | Decisión de revisión |
| :--- | :--- | :--- | :--- |
| WordPress.com Personal | WordPress alojado por WordPress.com, con editor visual, 6 GB y conexión de dominio externo en plan anual | Suficiente para landing, fotos, tres PDFs y contacto básico | **Ruta WordPress prioritaria** |
| WordPress.com Business | Plan alojado con herramientas avanzadas y staging oficial de WordPress.com | El staging nativo es útil, pero su precio anual excede el presupuesto de referencia | No usar en la primera fase |
| WordPress.org en hosting administrado | WordPress instalado en un hosting externo con mayor libertad de temas/plugins | Añade proveedor, mantenimiento, renovaciones y migración de código; solo justificado por necesidades CMS más complejas | Alternativa futura |

La característica de staging nativo de WordPress.com está limitada a los planes Business y Commerce. Por ello, para una primera migración de bajo riesgo se usará un **sitio temporal completo** bajo una dirección `*.wordpress.com`, no el staging clonado de pago. Ese sitio se podrá revisar públicamente y, si el cliente lo aprueba, recibirá posteriormente el dominio existente. [2]

## 2. Presupuesto de referencia

El plan Personal anual de WordPress.com aparece actualmente a $4 USD/mes, equivalente a $48 USD/año y con 6 GB de almacenamiento. A un tipo de cambio indicativo de 16.9242 MXN/USD, son aproximadamente $812 MXN antes de impuestos o $942 MXN si se aplicara un 16% adicional. El plan Business anual aparece a $25 USD/mes: alrededor de $5,077 MXN antes de impuestos o $5,890 MXN con el mismo supuesto fiscal. Los precios, cargos bancarios e impuestos deben verificarse al momento de compra. [3] [4]

| Partida | Presupuesto de referencia de $2,000 MXN/año | Regla |
| :--- | ---: | :--- |
| WordPress.com Personal anual | ~ $942 MXN bajo el supuesto indicado | Viable para el sitio, si el cliente aprueba este gasto |
| Reserva de renovación/cambio/tarjeta | ~ $1,058 MXN | No consumir sin una partida autorizada del cliente |
| WordPress.com Business | ~ $5,890 MXN | Fuera del presupuesto de referencia |

El ahorro de Wix continúa perteneciendo al cliente salvo acuerdo escrito que indique otra cosa. Este presupuesto no financia OmniRoute ni Universe Sent Me.

## 3. Staging exacto sin DNS

### Fase A — crear una cuenta y un sitio temporal

1. Con el cliente presente o con autorización explícita, crear una cuenta WordPress.com a nombre del cliente y registrar correo de recuperación, autenticación de dos factores y método de pago bajo su control.
2. Crear un sitio nuevo con una dirección temporal, por ejemplo `firma-bordados-prueba.wordpress.com`. No agregar `firmabordados.com` en esta fase.
3. Configurar el sitio temporal como no indexable en los ajustes de privacidad de WordPress.com. Confirmar que la URL de prueba será compartida solo con el cliente y equipo de revisión.
4. Seleccionar un tema de bloques ligero y crear una sola página de inicio con secciones equivalentes al staging aprobado: hero, capacidades, prueba de proceso, catálogos, redes y contacto.
5. Reutilizar únicamente logo, fotos y textos autorizados. Subir medios al repositorio multimedia de la cuenta WordPress del cliente; no usar rutas `/manus-storage`, assets privados de Universe Sent Me ni enlaces temporales de Manus.
6. Subir versiones aprobadas de los tres PDFs, confirmar nombre, tamaño, lectura en móvil y derechos de uso. Los archivos actuales suman aproximadamente 24.1 MB, muy por debajo de los 6 GB del plan Personal, pero las versiones finales deben validarse una por una.
7. Para contacto, conservar enlaces visibles de teléfono y correo. Configurar un bloque de formulario solo después de confirmar destinatario, aviso de privacidad, antispam y quién recibe los mensajes; no activar integraciones de terceros sin autorización.
8. Añadir y comprobar los enlaces oficiales de Facebook, Instagram y X ya autorizados.

### Fase B — control de calidad y aprobación

| Control | Criterio de aceptación |
| :--- | :--- |
| Diseño | La versión WordPress conserva la dirección `Color que Trabaja`: fondo claro, azul/rojo/amarillo, evidencia de producto y foco B2B |
| Contenido | Servicios, contacto, horarios y catálogos confirmados por el cliente |
| Responsividad | Revisión en móvil, tablet y escritorio; menú, CTA y catálogos utilizables |
| Activos | Logo nítido, fotos con permiso, PDFs actualizados y sin dependencia de Wix/Manus |
| Contacto | Teléfono, correo, formulario si aplica y redes dirigen al destino correcto |
| SEO de corte | Título, descripción, favicon, texto alternativo y bloqueo de indexación en la URL temporal |
| Propiedad | Cliente conserva acceso de propietario a WordPress.com, dominio y respaldos/exportaciones |

El sitio React/Vite existente se conserva como referencia de diseño y fuente de contenido aprobado, pero no se convierte automáticamente en WordPress. La página debe recrearse con bloques/tema WordPress o con un tema propio; no se recomienda incrustar la aplicación React dentro de WordPress para este alcance.

## 4. Corte futuro del dominio — bloqueado hasta aprobación

Solo después de una aprobación escrita del cliente se realizará lo siguiente:

1. Exportar contenido y guardar una copia de respaldo del sitio WordPress temporal; conservar también el inventario de PDFs y medios.
2. Exportar/capturar el estado actual de Wix y guardar una copia de los registros DNS vigentes.
3. Contratar o activar un plan WordPress.com de pago en la cuenta del cliente. WordPress.com permite conectar un dominio existente en cualquier plan de pago. [1]
4. En WordPress.com: **Domains → Add domain name → Use a domain name I own → Connect your site address**. Mantener el dominio registrado en Wix durante esta fase.
5. Elegir actualización por registros DNS A/CNAME en vez de transferir el dominio. Esta opción conserva la administración DNS en el proveedor actual, pero reemplaza los A records raíz y agrega el CNAME `www` que WordPress.com indique. Conservar MX y otros registros ajenos; no realizar este paso sin revisión del inventario DNS. [5]
6. Esperar propagación, que WordPress.com documenta como hasta 72 horas; verificar HTTPS, la dirección primaria, catálogo, contacto, redirecciones y visualización en varios dispositivos. [1]
7. Mantener Wix activo durante la propagación. Solo cancelar o reducir su plan cuando el cliente valide formalmente que el dominio, contenido y contacto funcionan en WordPress.

## 5. Operación mínima posterior

WordPress.com reduce la administración de servidor, pero el cliente debe conservar una rutina: actualizar el núcleo/tema cuando corresponda, revisar cada cambio de contenido en vista previa, descargar una exportación periódica, mantener 2FA, eliminar usuarios que ya no colaboren y no instalar plugins o integraciones sin necesidad. Si el volumen de cambios aumenta, se documentará una política de roles, publicaciones, copias de seguridad y mantenimiento.

## 6. Decisión pendiente

La ruta WordPress.com Personal es viable y más coherente que Cloudflare Pages si la prioridad es que el cliente pueda editar su sitio desde un panel. No se ha contratado ningún plan, no se creó una cuenta, no se migró contenido, no se tocó DNS y no se canceló Wix. La ejecución requerirá confirmación del cliente para crear su cuenta y para el corte de dominio, en momentos separados.

## Referencias

[1]: [WordPress.com — conectar un dominio existente](https://wordpress.com/support/domains/connect-existing-domain/)

[2]: [WordPress.com — crear un sitio de staging](https://wordpress.com/support/how-to-create-a-staging-site/)

[3]: [WordPress.com — planes y precios](https://wordpress.com/pricing/)

[4]: [Banco de México — tipo de cambio](https://www.banxico.org.mx/tipcamb/main.do?page=tip&idioma=en)

[5]: [WordPress.com — conexión mediante registros DNS](https://wordpress.com/support/domains/connect-a-domain-alternative-method/)
