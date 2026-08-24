# Evaluación de migración Wix, hosting externo y trabajo de IA

**Propósito:** Evaluar si un sitio sencillo de un cliente —información empresarial, contacto y tres catálogos en PDF— puede reconstruirse fuera de Wix para reducir dependencia del plan actual y asignar cualquier presupuesto liberado únicamente mediante una propuesta y aprobación separadas.

**Estado:** Review

**Fecha de creación:** 2026-08-23

**Última actualización:** 2026-08-24

**Versión:** 3.0

**Autor:** Manus AI

**Organización:** `Operations/Production`

**Documentos relacionados:** [`2026-08-18_Piloto_Local_OmniRoute_Seguro.md`](2026-08-18_Piloto_Local_OmniRoute_Seguro.md), [`2026-08-19_Decision_Gateway_IA_OmniRoute.md`](2026-08-19_Decision_Gateway_IA_OmniRoute.md), [`2026-08-23_Guia_Staging_Cloudflare_Pages_Firma_Bordados.md`](2026-08-23_Guia_Staging_Cloudflare_Pages_Firma_Bordados.md) y [`2026-08-24_Backlog_Tecnico_Staging_Firma_Bordados.md`](2026-08-24_Backlog_Tecnico_Staging_Firma_Bordados.md).

---

## Conclusión ejecutiva

El sitio no puede exportarse desde Wix como el mismo sitio listo para ejecutarse en otro hosting. Wix explica que su editor utiliza una arquitectura SaaS propietaria y que el sitio debe permanecer alojado y operado en sus servidores; el contenido pertenece al usuario, pero la implementación depende de Wix. [1]

La alternativa viable es **reconstruir el sitio** como una página estática o como un sitio pequeño con un backend externo para el contacto. Después se puede probar en una URL temporal y conectar el dominio existente mediante DNS. Wix permite apuntar un dominio comprado en Wix a un sitio externo usando registros A y CNAME; no se debe cambiar DNS ni cancelar el plan hasta que el cliente apruebe la versión nueva y se comprueben sitio, PDFs, formularios, correo y SEO básico. [2]

El presupuesto que eventualmente se libere sigue siendo del cliente. No debe transferirse automáticamente a Universe Sent Me ni a OmniRoute. Si el cliente desea financiar funciones adicionales, debe existir una propuesta separada que indique alcance, horas, hosting, uso de IA, mantenimiento, propiedad de los entregables y autorización expresa.

## Resultado de la auditoría pública inicial

La revisión pública confirmó una página corporativa de una sola página con navegación superior, secciones de trabajos, información institucional, tres catálogos PDF y contacto. El contenido visible incluye una propuesta de servicios de bordado, experiencia de la empresa, dirección, teléfono, horario y un formulario básico. También se observó un botón flotante de chat y una imagen principal con un logotipo de tercero; cualquier marca o fotografía de cliente debe contar con autorización antes de reutilizarse.

La reconstrucción no debe ser una copia literal. La dirección aprobada es una modernización conservadora con una primera pantalla más clara, propuesta de valor y CTA de contacto; una galería de trabajos más ordenada; tarjetas para los tres catálogos; una sección de servicios o proceso; y un contacto accesible con teléfono, correo, horario, dirección y formulario simple. El rediseño debe priorizar móvil, contraste, foco de teclado, encabezados semánticos, texto alternativo, compresión de imágenes y navegación directa a catálogos y contacto.

La auditoría no envió el formulario, no interactuó con el chat, no descargó los PDFs y no modificó el sitio ni el DNS. Los tres PDFs suman aproximadamente 24.1 MB según el usuario; antes de elegir hosting se debe comprobar el tamaño de cada archivo, porque los límites se aplican por activo individual y no solo al total.

## Dirección de modernización y staging

El usuario confirmó que el sitio no necesita ser idéntico a la versión Wix. Primero se construyó una dirección corporativa-industrial, pero posteriormente aprobó una referencia visual **clara y colorida** como base para la evolución de staging. La dirección vigente se denomina **Color que Trabaja**: blanco cálido dominante; Azul Firma `#0D4C9E` para navegación y títulos; rojo `#DF2B2C` para la acción principal; y amarillo `#F3BD25` para detalle, trayectoria y categorías. Conserva claridad para compradores de maquiladoras internacionales sin una atmósfera naval-industrial dominante.

La arquitectura vigente usa una hero clara de dos columnas —mensaje comercial y fotografía de proceso—, capacidades con acentos de color, collage de evidencia de prendas y bordado, biblioteca de catálogos y contacto accesible. El staging reemplazó el monograma provisional por el logo oficial aprobado, mantuvo los tres catálogos y el contacto público, y usa un formulario que prepara un correo localmente; no almacena datos ni expone un backend. Las pruebas visuales en escritorio y móvil confirmaron legibilidad de logo, navegación, enlaces, contraste y formularios. No se modificó Wix ni DNS.

La consulta pasiva de los recursos públicos confirmó tamaños individuales aproximados de 13.6 MB, 3.8 MB y 5.8 MB para los tres PDFs. Cada archivo queda bajo el límite de 25 MiB por activo documentado por Cloudflare Pages Free, por lo que el conjunto es técnicamente apto para la alternativa de hosting estático, sujeto a volver a alojar los PDFs bajo control del cliente antes del corte definitivo. [3]

## Curaduría de activos visuales y estrategia de redes

La revisión autorizada de `My Drive/Firma Bordados` confirmó una identidad visual coherente para contenidos: azul marino, rojo, amarillo, blanco, prendas de trabajo, hilos y detalles de bordado. Las publicaciones verticales de uniforme, parche y nombres bordados son buenas referencias de paleta, producto y lenguaje visual; no deben colocarse completas en la web porque incluyen CTAs, encuadres de feed y textos de interacción propios de redes sociales.

La recomendación es conservar el logo oficial de Firma Bordados en la cabecera, pero solicitar un archivo vectorial o PNG con transparencia antes del corte definitivo. El usuario confirmó permiso para editar y publicar fotografías de trabajos de clientes; aun así, se deben preferir fotografías propias limpias de proceso o prendas terminadas, y usar referencias de terceros solo cuando su marca, licencia y propósito queden claros. Se identificaron fotografías y clips reales de bordado que sirven como evidencia visual. Los clips con maquinaria Tajima deben optimizarse y validarse antes de integrarse en web.

La carpeta de Reels incluye un clip vertical de aproximadamente cuatro segundos con una línea de máquinas de bordado en operación. El clip transmite capacidad industrial y podría funcionar como evidencia de proceso en una sección móvil o como Reel, pero no como hero panorámico. Cualquier uso web requerirá optimización, controles de reproducción, un poster estático y validación previa de las marcas visibles.

La estrategia de redes revisada define tres pilares: escolar, corporativo B2B y confianza/legado. El sitio debe priorizar el pilar B2B para maquiladoras internacionales y empresas, mientras que el bordado escolar debe mantenerse como capacidad secundaria o estacional. El protocolo actual de conversión dirige a sitio, teléfono, correo y mensajes directos, y prohíbe prometer WhatsApp; por tanto, la página no debe agregar un CTA de WhatsApp sin una autorización posterior. Las cuentas sociales todavía requieren confirmación de URL y propiedad antes de agregar iconos o enlaces.

El usuario aprobó el uso del logo oficial de Firma Bordados, confirmó permiso para editar y publicar fotografías de trabajos de clientes, y autorizó el uso prudente de IA como apoyo de composición, nunca como sustitución de la evidencia real de proceso o producto. El staging actualizado reemplaza el monograma provisional por el logo oficial, integra una fotografía de proceso autorizada y añade enlaces externos a las cuentas oficiales de Facebook (`https://www.facebook.com/firmabordadospiedras`), Instagram (`https://www.instagram.com/firmabordados/`) y X (`https://x.com/firmabordados`). Los tres perfiles se verificaron como cuentas coherentes de Firma Bordados. La navegación usa enlaces externos accesibles y no automatiza publicaciones.

La variante de staging ahora incorpora la referencia clara y colorida aprobada por el usuario: producto y bordado son la evidencia principal, los acentos azul/rojo/amarillo proceden del logo oficial, y los fondos claros mejoran cercanía sin retirar la información que necesita un comprador B2B. La versión no es una réplica de una maqueta generada; traduce su jerarquía —hero clara, módulos de producto, catálogo ordenado y contacto visible— a una implementación responsive con activos autorizados y contenido verificable.

## Hechos confirmados con el usuario

El usuario cuenta con autorización del cliente para preparar el staging. El dominio público es `firmabordados.com`, el sitio actual solo usa un formulario básico de contacto y no depende de correo empresarial ligado al dominio. La renovación de Wix no ocurre hasta diciembre de 2026. Los tres PDFs suman aproximadamente 24.1 MB y las comprobaciones individuales previas los situaron por debajo del límite de 25 MiB por activo de Cloudflare Pages. No se cambiará DNS ni se cancelará Wix mientras el staging, los activos y el contacto no sean aprobados por el cliente.

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

Cloudflare Pages documenta en su plan Free hasta 500 builds mensuales, hasta 100 dominios personalizados por proyecto, 20.000 archivos y un límite de 25 MiB por activo. [3] Netlify publica un plan Free de $0 con dominios personalizados y SSL, pero también muestra un sistema de créditos y límites de uso que deben revisarse antes de prometer costo cero. [5] GitHub Pages documenta el uso de dominios personalizados, pero no debe tratarse como un servicio de backend o de almacenamiento de secretos. [6]

## Recomendación preliminar

Para este caso, la mejor ruta de evaluación es **reconstrucción estática + Cloudflare Pages o GitHub Pages**, manteniendo inicialmente el dominio registrado en Wix. La página descrita tiene pocos contenidos dinámicos y los catálogos PDF pueden ser enlaces o descargas si cada archivo está dentro del límite del hosting elegido.

### Recomendación actual de hosting

La recomendación actual es **Cloudflare Pages en una cuenta propiedad del cliente**, con despliegue desde un repositorio separado del proyecto Universe Sent Me. El caso actual se ajusta a sus límites Free: Pages admite hasta 500 builds mensuales, 100 dominios personalizados y 20,000 archivos por sitio; cada PDF de Firma Bordados está debajo de su límite de 25 MiB por activo. [3] Cloudflare también ofrece SSL, CDN y protección DDoS en su plan Free. [8]

La transición debe seguir dos etapas. Primero, usar el dominio temporal de staging ya publicado o un subdominio como `staging.firmabordados.com`; Cloudflare Pages permite conectar un subdominio mediante un CNAME sin que el dominio sea una zona Cloudflare. [9] Después de la aprobación del cliente, para publicar el dominio raíz `firmabordados.com` en Cloudflare Pages será necesario agregar la zona y apuntar los nameservers del dominio a Cloudflare. [9] La ausencia de correo empresarial reduce el riesgo operativo, pero los registros DNS existentes se deben inventariar antes de ese cambio.

**Netlify Free** es la alternativa secundaria si se prioriza un flujo de dominio personalizado con SSL sin mover la zona DNS de inmediato. Su plan Free publica 300 créditos de uso y los despliegues de producción, el ancho de banda y los requests consumen créditos; por lo tanto, debe configurarse monitoreo y no prometer costo ilimitado. [5] No se recomienda GitHub Pages para este cliente: GitHub establece que Pages no está destinado ni permitido como servicio de hosting gratuito para un sitio dirigido a un negocio. [6] Tampoco se recomienda Vercel Hobby, ya que su plan gratuito está restringido a uso personal no comercial. [10]

El contacto debe resolverse de manera explícita. Si solo se necesita mostrar teléfono, correo o WhatsApp, se pueden usar enlaces directos autorizados. Si se requiere un formulario, se debe usar un endpoint/backend o servicio de formularios con política de privacidad, protección antispam, límites y almacenamiento controlado. No se deben poner API keys en el JavaScript público.

No se recomienda alojar OmniRoute dentro de la misma página estática. OmniRoute debe permanecer como un servicio privado separado. La página del cliente solo podría consumir una función de IA mediante un backend propio, después de que el cliente solicite y apruebe esa función como alcance adicional. La decisión vigente del proyecto mantiene el frontend fuera del acceso directo a OmniRoute y exige un backend privado para cualquier integración de producción. [7]

## Plan de migración reversible

1. Obtener autorización escrita del cliente para reconstruir una copia y confirmar quién posee textos, imágenes, PDFs, dominio y correo.
2. Exportar o recopilar manualmente el contenido permitido de Wix, descargar los tres PDFs y verificar tamaños, versiones y permisos.
3. Construir una copia estática en una URL temporal, sin modificar todavía DNS ni cancelar Wix.
4. Comprobar responsive design, accesibilidad básica, enlaces, descargas, formulario/contacto, títulos, favicon, HTTPS y redirecciones.
5. Ejecutar una revisión del cliente y corregir diferencias.
6. Preparar el cambio DNS. Wix indica que para apuntar a un host externo se actualizan registros A y CNAME; los cambios pueden tardar hasta 48 horas en propagarse. [2]
7. Mantener Wix activo durante la propagación y confirmar desde varios dispositivos que el nuevo sitio funciona.
8. Revisar correo empresarial y registros MX antes de cancelar cualquier servicio. Wix advierte que el correo necesita sus registros MX después de una transferencia de dominio. [4]
9. Cancelar o reducir el plan Wix únicamente después de que el cliente confirme por escrito que el nuevo sitio y el dominio funcionan.

La transferencia del dominio fuera de Wix es opcional. Si se realiza, Wix indica que el nuevo proveedor asumirá datos de contacto, DNS y renovaciones, que la transferencia suele tardar hasta siete días y que pueden aplicar bloqueos de transferencia de 60 días. [4] Para reducir riesgo, la primera versión debería mantener el dominio con Wix y solo apuntarlo por DNS al nuevo hosting, si el host lo permite.

## Separación del presupuesto y de los proyectos

El ahorro del plan Wix no es automáticamente presupuesto de Universe Sent Me. Debe presentarse al cliente una propuesta con al menos dos partidas separadas:

| Partida | Propietario | Ejemplos |
|---|---|---|
| Migración y operación del sitio del cliente | Cliente | Reconstrucción, PDFs, DNS, formulario, mantenimiento y hosting. |
| Trabajo adicional solicitado por el cliente | Cliente, con aprobación | Automatización editorial, copy, analítica o integración autorizada. |
| Desarrollo de Universe Sent Me | Universe Sent Me | OmniRoute, Growth OS, personajes, documentación y pruebas internas. |

Aunque el cliente quiera financiar trabajo adicional, no se deben reutilizar sus credenciales, PDFs, datos de contacto, audiencia, dominio o contenido para Universe Sent Me. Los proyectos deben tener repositorios, cuentas, claves, facturación y respaldos separados.

### Escenario de referencia: $2,000 MXN anuales liberados

Un ahorro potencial de Wix no crea automáticamente un presupuesto de Universe Sent Me. Hasta contar con una autorización contractual o escrita que indique que ese ahorro puede ser retenido y reasignado, el monto continúa siendo presupuesto del cliente y debe usarse solo para su sitio, mantenimiento, formulario o contingencias. La estimación siguiente aplica únicamente si el usuario dispone de **$2,000 MXN propios, separados y anuales** para Universe Sent Me después de cerrar esa decisión con el cliente.

| Escenario | Firma Bordados | OmniRoute / Universe Sent Me | Uso aproximado del presupuesto anual | Decisión |
|---|---|---|---:|---|
| Conservador — recomendado | Cloudflare Pages en cuenta del cliente, con hosting estático sin costo y Wix activo hasta aprobar el corte | Piloto local manual en el iMac; Groq/Gemini con límites gratuitos; reserva para un caso de uso probado | $0 de infraestructura recurrente; $2,000 MXN quedan como reserva propia de USM | **Prioritario** |
| Servidor mínimo experimental | Igual que el anterior, sin compartir cuentas ni DNS | VPS de 1 GiB para OmniRoute privado, acceso por backend/VPN y sin exposición de dashboard | Un VPS de referencia de $6 USD/mes equivale a ~ $1,219 MXN/año antes de impuestos; a un tipo de cambio indicativo de 16.9242 y 16% adicional, ~ $1,414 MXN, con ~ $586 MXN de reserva | **Solo piloto; no aprobar aún** |
| Servidor ultrabásico | Igual que el anterior | VPS de 512 MiB | ~$812 MXN/año antes de impuestos; ~$942 MXN con el mismo supuesto de 16% | **No recomendado:** el contenedor local ya observó ~448 MiB, sin margen operativo suficiente |
| Servidor con margen | Igual que el anterior | VPS de 2 GiB | ~$2,827 MXN/año con el mismo supuesto de tipo de cambio e impuesto | **Fuera del presupuesto de referencia** |

Las cifras son orientativas: el proveedor factura en USD y aplica su propia tributación; el banco o tarjeta puede utilizar otro tipo de cambio. DigitalOcean publica actualmente $6 USD/mes para 1 GiB y $12 USD/mes para 2 GiB; sus VPS son administrados por el cliente, no un servicio de operación incluida. [11] El tipo de cambio debe verificarse al momento de contratar con una fuente oficial o con el emisor de pago. [12]

El sitio estático de Firma Bordados no necesita compartir servidor con OmniRoute. Cloudflare Pages permite conectar dominio personalizado; para el dominio raíz se administrará la zona DNS en Cloudflare y para un subdominio basta un CNAME configurado después de asociarlo en el panel. [9] La cuenta, facturación y control del dominio deben ser del cliente. El presupuesto de Universe Sent Me no debe pagar ni condicionar esa decisión.

La recomendación de arquitectura y presupuesto permanece: primero migrar y validar el sitio en un entorno gratuito y separado; mantener OmniRoute local hasta que cinco pruebas de análisis/borradores demuestren valor; y solo después considerar un VPS privado. Pagar un VPS no mejora por sí mismo los modelos ni sus cuotas; solo aporta disponibilidad independiente del iMac y una ubicación apta para un backend privado.

La guía técnica completa de la prueba sin DNS está en `2026-08-23_Guia_Staging_Cloudflare_Pages_Firma_Bordados.md`. Define una rama `staging`, un proyecto Pages separado, una URL `*.pages.dev`, el reemplazo previo de rutas Manus/Wix por activos controlados por el cliente y un checklist verificable. También establece que WordPress no aporta valor inmediato al caso actual; se reconsidera únicamente si el cliente necesita edición frecuente autónoma, blog, múltiples autores o funciones CMS.

### Aclaración posterior: WordPress en vez de Cloudflare Pages

Fernando aclaró que desea evaluar **WordPress como alternativa al host Cloudflare Pages**, no solo como un CMS accesorio. La ruta prioritaria en Review pasa a ser WordPress.com bajo cuenta del cliente, usando primero un sitio temporal `*.wordpress.com` sin DNS. Esta alternativa es viable dentro del presupuesto de referencia con el plan Personal anual; no ofrece el staging nativo de WordPress.com, que queda limitado a Business/Commerce y supera ese presupuesto. La guía operativa separada es `2026-08-23_Ruta_Staging_WordPress_Firma_Bordados.md`.

La opción Cloudflare Pages continúa documentada como alternativa estática y reversible, pero no se iniciará mientras se evalúe la preferencia WordPress. Ninguna ruta autoriza mezclar infraestructura, credenciales, presupuesto o datos del cliente con Universe Sent Me u OmniRoute.

### Decisión vigente: Cloudflare Pages con movimiento ligero

Fernando confirmó posteriormente que Cloudflare Pages es la ruta preferida por coste y mantenimiento. El staging React/Vite recibió la actualización visual `Color que Trabaja` documentada en `2026-08-23_Actualizacion_Movimiento_Staging_Firma_Bordados.md`: una puntada SVG de entrada, revelados breves, microinteracciones de catálogo/CTA y reglas de bordado como sistema de identidad. La alternativa WordPress se conserva únicamente como referencia y no se ejecutará sin nueva decisión. No hubo cambios a Wix, DNS, contenido, catálogos ni formulario.

### Inventario autorizado de catálogos

La carpeta Drive compartida por Fernando contiene los tres catálogos que reemplazarán los enlaces temporales Wix durante una integración posterior. `2026-08-24_Inventario_Catalogos_Drive_Firma_Bordados.md` registra sus nombres, tamaños, páginas y portadas revisadas. Detecta tamaños desactualizados en las tarjetas Soul & Blues y M&O, además de ediciones declaradas 2019 y 2016 para BigBang/M&O; por ello los enlaces y metadatos del staging no se cambiarán hasta que el cliente confirme que las tres versiones son vigentes. Los servicios siguen pendientes y no se infieren de los catálogos.

Fernando confirmó la vigencia de los tres catálogos y la oferta comercial. El staging ahora los sirve como activos controlados del entorno de prueba, ajusta sus tamaños visibles y presenta digitalización, bordado, serigrafía, playeras, camisas, uniformes industriales y línea médica. La nota de alcance indica que no se realizan parches ni gorras. Los activos deberán volver a incorporarse al repositorio/almacenamiento del cliente antes del despliegue Cloudflare; Wix, DNS y el dominio no cambiaron.

### Canales de contacto y contenido pendiente

Fernando confirmó el correo `firmabordados@yahoo.com` y el WhatsApp `+52 878 788 0735`. El staging conserva el formulario que prepara un correo desde el dispositivo y añade un enlace visible de WhatsApp con mensaje inicial sobre prendas, bordado o serigrafía. El enlace se probó visualmente en móvil; no se enviaron mensajes. Materiales, tiempos de entrega y mínimos de pedido siguen pendientes de solicitud al cliente y no se incorporan hasta contar con información confirmada.

WhatsApp es ahora el CTA principal del hero y conserva catálogos como acción secundaria. La guía `2026-08-23_Guia_Staging_Cloudflare_Pages_Firma_Bordados.md` se amplió con pasos exactos para crear la cuenta Cloudflare y el repositorio GitHub privado del cliente, limitar el acceso de la aplicación Cloudflare Workers & Pages, preparar ramas y configurar el build. La ejecución de cuentas, repositorio, Cloudflare Pages y DNS sigue pendiente de realizarse con el cliente o con autorización explícita; no se modificó Wix ni el dominio público.

Fernando autorizó posteriormente una excepción temporal: el repositorio privado y el primer proyecto Pages se crearán bajo las cuentas actuales de Io Marketing. Esta excepción no autoriza un corte de dominio. La transferencia del repositorio/proyecto al cliente, o un acuerdo de operación administrada por Io Marketing, se vuelve un gate obligatorio antes de modificar DNS, renovar hosting o cancelar Wix.

El staging se desplegó exitosamente en `https://firma-bordados-staging.pages.dev` desde la rama privada `staging`, con build Vite reproducible y activos locales aprobados. La aplicación GitHub de Cloudflare se limitó a ese repositorio. La URL se verificó sin añadir dominio personalizado: conserva CTA de WhatsApp, contacto, servicios y catálogos; no afecta Wix, `firmabordados.com`, DNS ni nameservers.

### Mejoras técnicas independientes del contenido comercial

`2026-08-24_Backlog_Tecnico_Staging_Firma_Bordados.md` organiza mejoras de bajo riesgo mientras se esperan materiales, tiempos y mínimos: accesibilidad, noindex de staging, headers, carga diferida de imágenes, limpieza de runtime, CI y protección de ramas. No autoriza analytics, backend de formularios, precios, SEO estructurado definitivo ni cambio de dominio.

El paquete P0 del backlog se completó. Se añadió zoom, foco visible, enlace de salto, reducción de movimiento integral, noindex y headers estáticos; el build se validó y la URL Pages se comprobó en móvil. Pages conserva `main` como Production branch del sitio de staging, por lo que el commit aprobado se promovió desde `staging` a `main` en vez de cambiar el dominio o el proyecto. Este ajuste solo sincroniza el código de prueba y no modifica Wix, DNS o el dominio público.

El paquete P1 se cerró con una validación continua de GitHub sobre Pull Requests y pushes a `staging`/`main`, basada en el lockfile congelado, TypeScript y la build Vite. Después de corregir el orden de inicialización de pnpm en CI, las ejecuciones de `staging` y `main` terminaron correctamente y los commits validados `f49a344`/`beaaa8d` se promovieron por avance rápido a `main`. La landing redujo providers inactivos, retiró `next-themes` y `sonner`, aplicó carga diferida a imágenes no críticas y redujo el bundle principal de ≈562 kB a 451.78 kB sin comprimir (≈163 kB a 127.12 kB gzip). Se confirmó nuevamente la URL de staging, noindex, robots y headers; Wix, DNS, nameservers y `firmabordados.com` siguen sin modificaciones.

La protección formal de `main` no se habilitó durante P1 porque altera el flujo de colaboración de GitHub. La disciplina vigente es suficiente para el staging temporal: ramas de trabajo o `staging` → revisión + CI → promoción explícita a `main` → despliegue de Pages. Cualquier regla de protección debe aprobarse por separado antes de activarla.

La primera actualización comercial posterior a P1 se completó solo con información confirmada: serigrafía a partir de 12 piezas y tiempos que se confirman según cantidad, requerimiento y carga de trabajo. Se usó una visual exclusiva de prendas sin marcas externas y una adaptación fiel de la fachada autorizada, ambas optimizadas para la web. El cambio pasó CI, se integró en `staging` y se promovió al staging público servido desde `main`; la revisión visual confirmó servicios, catálogos, contacto y protecciones P0. El bloqueo sobre materiales permanece: no se describieron telas, gramajes, composiciones, acabados ni certificaciones.

La refinación posterior añadió una galería corta de procesos dentro de «Nuestro trabajo». Las fotografías de Drive con marcas de clientes se utilizaron solo como referencia; la versión pública usa una fotografía autorizada existente y dos visuales exclusivas sin marcas de terceros. También se agregó una frase sobre explorar opciones de prenda según la necesidad de presentación, en lugar de declarar materiales o calidades no documentados. El flujo de revisión, CI y promoción a `main` se mantuvo intacto; Wix, DNS, nameservers y el dominio público siguen sin cambios.

Tras detectarse una generación incompleta en la tarjeta «Detalle de bordado», se revirtió de forma puntual el uso de visuales externos y se sustituyeron por recursos locales comprobados. La corrección pasó CI en `staging` y `main`; tres solicitudes estáticas a los activos de la galería devolvieron HTTP 200 y la respuesta de la landing no contiene el marcador de fallo. La validación visual manual queda a cargo del usuario en Quick-seedless, sin volver a usar un navegador remoto de otra computadora.

## Integración futura de IA

Si el cliente solicita una función de IA, la primera versión debe ser un endpoint de borradores detrás de un backend privado, no una llamada desde el navegador. Debe aceptar un propósito limitado, validar tamaño y contenido, excluir secretos y datos personales, aplicar autenticación y rate limiting, registrar provider/modelo/latencia/estado y devolver una respuesta marcada como `Draft`. No debe publicar automáticamente ni escribir en los ledgers de Universe Sent Me.

El Combo `usm-groq-gemini-priority` pertenece al piloto de Universe Sent Me y no debe conectarse al sitio del cliente sin una separación de infraestructura y una aprobación específica. Si se necesita IA para el cliente, se debe decidir si conviene un provider directo o una instancia de OmniRoute separada con sus propias claves, volumen, logs y política de retención.

## Decisión pendiente

No iniciar una migración irreversible todavía. Ya se confirmó la autorización de reconstrucción, ausencia de correo empresarial vinculado al dominio, formulario básico, renovación de Wix en diciembre de 2026, redes sociales oficiales y permiso para editar y publicar fotografías de trabajos. Aún se necesita confirmar el costo actual de Wix, los servicios exactos y su prioridad comercial, la preferencia de hosting y la necesidad final del formulario antes de cualquier cambio DNS.

Si el inventario confirma que el sitio es realmente estático, se puede preparar una copia de prueba. La cancelación de Wix, transferencia del dominio y asignación de presupuesto para IA quedan bloqueadas hasta que el cliente apruebe el alcance, el costo y la nueva versión.

## Documentos que requieren actualización si se aprueba la integración

La evaluación no cambia todavía los ledgers ni el dashboard de Growth OS. Si se aprueba una integración de IA para el cliente, deberán crearse documentos operativos separados para esa cuenta y actualizarse la decisión de OmniRoute con el alcance, las credenciales separadas, el hosting, la retención y el responsable. No se deben mezclar los documentos canónicos del cliente con los de Universe Sent Me.

## Referencias

[1]: [Wix — Exporting or Embedding Your Wix Site Elsewhere](https://support.wix.com/en/article/exporting-or-embedding-your-wix-site-elsewhere)

[2]: [Wix — Connecting a Wix Domain to an External Site](https://support.wix.com/en/article/connecting-a-wix-domain-to-an-external-site)

[3]: [Cloudflare Pages — Limits](https://developers.cloudflare.com/pages/platform/limits/)

[4]: [Wix — Transferring Your Wix Domain Away from Wix](https://support.wix.com/en/article/transferring-your-wix-domain-away-from-wix-2477749)

[5]: [Netlify — Pricing](https://www.netlify.com/pricing/)

[6]: [GitHub Docs — Configuring a Custom Domain for GitHub Pages](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

[7]: [Universe Sent Me — Decisión de uso de OmniRoute](2026-08-19_Decision_Gateway_IA_OmniRoute.md)

[8]: [Cloudflare — Free Plan Overview](https://www.cloudflare.com/plans/free/)

[9]: [Cloudflare Pages — Custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/)

[10]: [Vercel — Hobby Plan](https://vercel.com/docs/plans/hobby)

[11]: [DigitalOcean — Droplet Pricing](https://www.digitalocean.com/pricing/droplets)

[12]: [Banco de México — Tipo de cambio](https://www.banxico.org.mx/tipcamb/main.do?page=tip&idioma=en)
