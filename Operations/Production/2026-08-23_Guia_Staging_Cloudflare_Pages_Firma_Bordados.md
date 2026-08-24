---
title: "Guía de staging reversible en Cloudflare Pages — Firma Bordados"
purpose: "Definir los pasos técnicos para probar el sitio React/Vite de Firma Bordados en Cloudflare Pages sin modificar Wix, el DNS del dominio ni el sitio público actual; incluir el criterio para descartar o adoptar WordPress."
status: Review
created: 2026-08-23
updated: 2026-08-24
version: "1.1"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-23_Evaluacion_Migracion_Wix_Hosting_IA.md"
  - "Operations/Production/2026-08-19_Decision_Gateway_IA_OmniRoute.md"
  - "GrowthOS/00_01_Changelog_GrowthOS.md"
organization: "Operations/Production"
---

# Guía de staging reversible en Cloudflare Pages — Firma Bordados

## 1. Alcance y decisión

Esta guía crea una prueba aislada del staging React/Vite existente en una URL `*.pages.dev`. **No modifica `firmabordados.com`, no mueve nameservers, no cancela Wix, no cambia el formulario en producción y no conecta el sitio del cliente con OmniRoute.** La cuenta Cloudflare, el repositorio del cliente y la facturación futura deben pertenecer al cliente.

> El staging sirve para que el cliente revise la nueva versión con una URL real y para validar build, activos, catálogos, enlaces y contacto. No es aún el corte de producción.

### Excepción temporal de propiedad — Io Marketing

Fernando autorizó que el primer staging use la cuenta actual de Cloudflare y GitHub de **Io Marketing**, con un repositorio privado. Esta excepción solo facilita la revisión técnica: no transfiere la propiedad del dominio ni convierte los activos del cliente en activos de Universe Sent Me.

Antes de asociar `firmabordados.com`, cambiar DNS, facturar hosting o cancelar Wix, se debe cumplir una de estas opciones: transferir el repositorio y proyecto Pages a una cuenta del cliente, o documentar expresamente que Io Marketing operará el hosting en nombre del cliente, con accesos, responsabilidad de renovación y un mecanismo de entrega definidos. El contenido, catálogos y contactos de Firma Bordados permanecen separados de Universe Sent Me y OmniRoute.

### Estado de configuración — 2026-08-24

La cuenta Cloudflare de Io Marketing fue verificada y no mostraba proyectos Pages existentes ni dominios agregados durante esta sesión. El repositorio privado temporal `iomarketing09-sys/firma-bordados-site` contiene una copia estática validada y las ramas `main` y `staging`. El flujo de Cloudflare se encuentra en la autorización de la aplicación GitHub, que debe limitarse a ese repositorio antes de crear `firma-bordados-staging`. No se ha modificado Wix, DNS, `firmabordados.com` ni la configuración de dominio de Cloudflare.

Durante la instalación limitada de **Cloudflare Workers and Pages** en GitHub, la redirección devolvió `Error connecting to git account`. Cloudflare indicó desinstalar completamente y reinstalar la aplicación. No se creó un proyecto Pages, no se concedió acceso a otros repositorios y no se modificó ningún dominio. El siguiente intento debe empezar revisando la instalación de GitHub y, si existe una instalación parcial, retirarla antes de repetir la autorización con el único repositorio `iomarketing09-sys/firma-bordados-site`.

### Resultado de staging — 2026-08-24

La verificación adicional de GitHub se completó y la aplicación **Cloudflare Workers and Pages** quedó limitada al único repositorio privado `iomarketing09-sys/firma-bordados-site`. La ruta correcta se realizó desde **Get started with Pages → Import an existing Git repository**, no desde el flujo de Worker.

| Configuración | Valor aplicado |
| :--- | :--- |
| Proyecto Pages | `firma-bordados-staging` |
| URL de staging | `https://firma-bordados-staging.pages.dev` |
| Repositorio | `iomarketing09-sys/firma-bordados-site` (privado) |
| Rama de producción del staging | `staging` |
| Comando de build | `pnpm exec vite build` |
| Directorio publicado | `dist/public` |
| Entorno de build | `NODE_VERSION=22.16.0` |
| Dominio personalizado | Ninguno |

El primer build terminó correctamente y se verificó que la URL sirve el hero, WhatsApp como CTA principal, capacidades, catálogos, contacto y los enlaces de PDF. La página contiene bloqueo de indexación de staging. Wix, `firmabordados.com`, DNS y nameservers permanecen sin cambios. Cualquier corte de dominio continúa bloqueado por la transferencia/operación administrada documentada y una aprobación expresa del cliente.

## 2. Estado de partida y preparación obligatoria

| Elemento | Estado actual | Acción antes de Cloudflare Pages |
| :--- | :--- | :--- |
| Aplicación | React 19 + Vite 7, con `pnpm-lock.yaml` | Mantener el proyecto en un repositorio privado independiente de Universe Sent Me |
| Compilación actual | `vite.config.ts` crea el sitio estático en `dist/public` | Configurar Pages con `pnpm exec vite build` y output `dist/public` |
| Imágenes y logo | El staging de Manus utiliza rutas `/manus-storage/...` | Copiar al repositorio del cliente versiones autorizadas y optimizadas en `client/public/media/`; reemplazar las rutas antes del deploy |
| Catálogos | El staging actual enlaza temporalmente a PDFs alojados en Wix | Descargar versiones autorizadas, validar nombre/tamaño/versión y subirlas en `client/public/catalogos/`; no depender de `firmabordados.com/_files/...` |
| Formulario | Prepara un `mailto:` y no guarda datos | Conservarlo igual durante staging; un formulario servidor-side se decide después con privacidad, antispam y responsable definidos |
| Dominio | Wix continúa atendiendo `firmabordados.com` | No tocar DNS ni nameservers durante esta fase |

El código de staging no debe conservar URLs de almacenamiento de Manus ni archivos del cliente que no estén autorizados para su repo. Antes de subir, buscar y sustituir rutas `"/manus-storage/"` y `"https://www.firmabordados.com/_files/"`. Los activos del cliente deben vivir bajo control de su cuenta/repo o en un almacenamiento que él posea.

## 2.1 Pasos exactos: cuenta Cloudflare y repositorio privado del cliente

Esta parte no modifica el dominio ni el DNS. El propietario de la cuenta debe ser el cliente; Fernando puede ser administrador técnico, pero no debe sustituir la propiedad del cliente. No compartir contraseñas, códigos 2FA, tokens ni datos bancarios por chat.

### A. Crear la cuenta del cliente en Cloudflare

1. El cliente abre `https://dash.cloudflare.com/sign-up` en su propio navegador e introduce un correo que controle a largo plazo.
2. El cliente crea la contraseña, verifica el correo y activa autenticación de dos factores desde **My Profile** → **Authentication**. Guardará sus códigos de recuperación en un lugar privado.
3. En esta fase debe **omitir** cualquier opción de “Add a website”, “Add a domain” o cambio de nameservers. La cuenta puede existir sin incorporar `firmabordados.com`.
4. El cliente invita a Fernando como miembro solamente si necesita apoyo continuo: **Manage account** → **Members** → **Invite members**. El cliente conserva el rol propietario; el acceso de Fernando se puede retirar después.
5. No se agregan métodos de pago, Workers, dominios, API tokens ni secretos para este staging estático.

### B. Crear el repositorio privado del cliente en GitHub

1. El cliente inicia sesión en `https://github.com` con una cuenta que controle o crea una nueva exclusivamente para Firma Bordados. Debe activar 2FA desde **Settings** → **Password and authentication**.
2. En la esquina superior derecha elige **+** → **New repository**.
3. Selecciona su usuario u organización como **Owner** y escribe exactamente `firma-bordados-site` como **Repository name**.
4. Selecciona **Private**. No usar **Public** porque el repositorio contendrá los PDF autorizados, fotografías y archivos de negocio.
5. Para una importación limpia por Git, deja desmarcadas las opciones **Add a README file**, **Add .gitignore** y **Choose a license**; después pulsa **Create repository**.
6. En **Settings** → **Collaborators and teams**, el cliente puede invitar a Fernando con el menor acceso que permita el trabajo acordado. No debe invitar cuentas desconocidas ni compartir su contraseña.

> Antes de enviar código al repositorio, se prepara una copia apta para Cloudflare. El proyecto actual contiene utilidades y rutas específicas de Manus (`/manus-storage`, collector y proxy local); esas partes no se copian como dependencia de producción. Se reemplazan por activos locales autorizados en `client/public/media/` y `client/public/catalogos/`, y se comprueba el build sin dependencias Manus.

### C. Ramas exactas para el staging

1. Se sube la copia limpia del proyecto a `main` como referencia controlada.
2. Desde `main`, se crea la rama `staging`. La URL principal de Pages de esta primera prueba seguirá los commits de `staging`.
3. Para cada modificación se crea una rama descriptiva, por ejemplo `feature/cta-whatsapp` o `fix/catalogo-myo`, desde `staging`.
4. Se abre un Pull Request hacia `staging`. Cloudflare genera una URL única de preview para ese Pull Request; tras aprobación se integra a `staging`.
5. `main` no se conecta al dominio público durante esta fase y `firmabordados.com` permanece en Wix.

## 3. Estructura de repositorio y ramas

1. Crear, en la cuenta u organización de GitHub del cliente, un repositorio privado llamado `firma-bordados-site`. No reutilizar el repositorio de Universe Sent Me ni el de un tercer cliente.
2. Importar una copia limpia del proyecto actual. Excluir `.manus-logs/`, archivos de configuración privada de Manus, secretos, descargas temporales y cualquier activo no autorizado.
3. Conservar `main` como rama candidata a la futura producción y crear una rama `staging`.
4. En `staging`, incorporar los activos propios en `client/public/media/` y los PDFs aprobados en `client/public/catalogos/`. En los componentes, usar rutas estáticas como `/media/logo-firma-bordados.png` y `/catalogos/bigbang.pdf`.
5. Añadir, solamente en la rama `staging`, un `robots.txt` que desautorice el rastreo y una meta etiqueta `noindex,nofollow` en `client/index.html`. Quitar ambos bloqueos antes de preparar un proyecto de producción. Las preview deployments reciben además `X-Robots-Tag: noindex` por defecto, pero el dominio de producción del proyecto `*.pages.dev` no debe depender de ese comportamiento. [3]
6. Ejecutar localmente `pnpm check` y `pnpm exec vite build`. Confirmar que existe `dist/public/index.html` y que ningún asset o catálogo produce error 404.

## 4. Crear el proyecto de staging en Cloudflare Pages

Estos pasos se realizan en la **cuenta Cloudflare del cliente**. Como conectan una cuenta externa y autorizan a Cloudflare a leer el repositorio seleccionado, deben hacerse con el cliente presente o mediante autorización explícita.

1. Entrar a **Workers & Pages** → **Create application** → **Pages** → **Connect to Git**.
2. Autorizar la aplicación de Cloudflare para acceder solo al repositorio privado `firma-bordados-site`; no autorizar todos los repositorios si no es necesario.
3. Seleccionar el repositorio y configurar el proyecto con estos valores exactos:

| Campo de Cloudflare Pages | Valor para este staging |
| :--- | :--- |
| Project name | `firma-bordados-staging` |
| Production branch | `staging` |
| Framework preset | React (Vite), o configuración manual equivalente |
| Root directory | Vacío; el proyecto está en la raíz del repositorio |
| Build command | `pnpm exec vite build` |
| Build output directory | `dist/public` |
| Build environment variables | `NODE_VERSION=22.16.0`; `PNPM_VERSION=10.11.1` |

4. Pulsar **Save and Deploy** y esperar un estado `Success`. Cloudflare Pages instala dependencias, ejecuta el build y publica el directorio configurado; una salida distinta de cero marca el build como fallido. [1] [2]
5. Abrir la URL generada, que tendrá la forma `https://firma-bordados-staging.pages.dev`. Esta URL es el staging compartible. No asociar aún ningún dominio personalizado.
6. En **Settings** → **General**, habilitar una política de acceso para previews si el cliente no desea que los enlaces de ramas sean públicos. Las previews son públicas por defecto. [3]

Cloudflare admite versiones específicas de Node y pnpm con variables de entorno. Fijarlas evita que una actualización de la imagen de compilación cambie la reproducción del build sin revisión. [4]

### D. Lista de comprobación en pantalla antes de pulsar `Save and Deploy`

| Control | Debe decir o mostrar |
| :--- | :--- |
| Cuenta Cloudflare | Cuenta propiedad del cliente, sin `firmabordados.com` agregado |
| Cuenta GitHub conectada | Cuenta/organización del cliente; app **Cloudflare Workers & Pages** con acceso solo a `firma-bordados-site` |
| Proyecto seleccionado | Repositorio privado `firma-bordados-site` |
| Rama elegida | `staging` como Production branch del proyecto de prueba |
| Project name | `firma-bordados-staging` |
| Root directory | Vacío |
| Build command | `pnpm exec vite build` |
| Build output directory | `dist/public` |
| Variables | `NODE_VERSION=22.16.0` y `PNPM_VERSION=10.11.1` |
| Dominio personalizado | Ninguno; solo se espera la URL `*.pages.dev` |

Cloudflare admite repositorios GitHub privados y recomienda limitar la aplicación de GitHub a los repositorios necesarios. Cada push a la rama conectada genera un build; los Pull Requests creados desde el mismo repositorio producen previews actualizables. [1] [7]

## 5. Pruebas técnicas antes de compartir el staging

| Prueba | Cómo comprobarla | Resultado esperado |
| :--- | :--- | :--- |
| Build | Revisar **Deployments** y logs de Cloudflare | Estado `Success`, sin errores de módulos, rutas o permisos |
| Activos propios | Abrir logo, hero, fotos y favicón | Todas las imágenes cargan desde `/media/`; ninguna petición a `/manus-storage/` |
| Catálogos | Abrir cada enlace en una pestaña privada | Cada PDF descarga/abre desde `/catalogos/`; no redirige a Wix |
| Navegación | Probar anclas, menú móvil, retorno al inicio y redes sociales | Sin enlaces rotos ni contenido superpuesto |
| Contacto | Validar que el formulario solo prepara el correo y que la dirección es correcta | No se almacenan datos en staging; no enviar pruebas al buzón sin acuerdo |
| Responsividad | Revisar al menos móvil de 375 px, tablet y escritorio | Texto legible, CTA alcanzable y catálogo utilizable |
| Privacidad y SEO | Ver fuente y `robots.txt`; confirmar meta `noindex,nofollow` | El staging no se presenta como sitio final ni se indexa intencionalmente |
| Independencia de Wix | Abrir staging con Wix aún activo | Ambos sitios coexisten; el dominio público sigue mostrando Wix |

Para cada cambio posterior, abrir una rama de trabajo desde `staging` y crear un Pull Request. Cloudflare Pages genera una URL única de preview para cada Pull Request y mantiene actualizada la preview cuando llegan nuevos commits; el staging principal no se altera hasta que el cambio se integre a la rama `staging`. [3]

## 6. Reversión y preparación del corte futuro

La reversión del staging es simple: dejar de compartir el enlace o eliminar el proyecto Pages. Como no existe dominio personalizado ni DNS asociado, Wix sigue intacto. Si algún día se conectara un dominio personalizado a Pages, primero se debe retirar el CNAME o configuración asociada antes de borrar el proyecto, para evitar apuntar un dominio a un proyecto inexistente. [1]

El corte futuro a `firmabordados.com` requiere una decisión separada del cliente. Incluye aprobar contenido y formulario, inventariar registros DNS, crear respaldo de la configuración Wix, asociar el dominio desde el panel Pages y, para el dominio raíz, gestionar la zona y los nameservers en Cloudflare. Un subdominio como `staging.firmabordados.com` puede añadirse más adelante mediante CNAME, pero asociar ese subdominio a una rama requiere un registro DNS proxied administrado por Cloudflare. [5] No realizar ese paso durante el staging de esta guía.

## 7. ¿WordPress sirve para este caso?

WordPress **sí puede servir**, pero no es la mejor primera opción para el alcance actual: una landing corporativa, tres catálogos PDF, imágenes, enlaces sociales y un contacto básico. La versión React/Vite estática elimina la necesidad de PHP, base de datos, administración de plugins y mantenimiento de un CMS. WordPress requeriría un hosting que mantenga PHP 8.3+, MariaDB 10.11+ o MySQL 8.0+, HTTPS y actualizaciones continuas. [6]

| Situación del cliente | Plataforma preferible | Motivo |
| :--- | :--- | :--- |
| Cambios esporádicos que tú administras; catálogo estable; una landing | Cloudflare Pages estático | Menor coste, menor superficie de mantenimiento y despliegues versionados |
| El cliente necesita editar textos, fotos, servicios o catálogos cada semana sin depender de ti | WordPress administrado | Panel editorial y roles de usuario pueden justificar el CMS |
| Blog frecuente, noticias, múltiples autores, campañas con landing pages o plugins de CRM | WordPress administrado o CMS equivalente | El contenido dinámico puede compensar el coste operativo |
| Tienda con stock, pagos, pedidos y operación comercial | Shopify o WooCommerce evaluado aparte | Requiere alcance, pagos, seguridad y operación distintos |

No se debe instalar WordPress en Cloudflare Pages ni en el servidor de OmniRoute: Pages no sustituye su PHP/base de datos y OmniRoute debe permanecer privado y separado. Si el cliente elige WordPress más adelante, deberá contratar un WordPress **administrado** en una cuenta propia, con copias de seguridad, actualizaciones, control de acceso y responsable de mantenimiento definidos. El staging React/Vite actual sigue siendo la opción más económica y reversible para esta primera migración.

## 8. Criterio de cierre de esta fase

La fase de staging queda lista cuando el cliente pueda visitar `firma-bordados-staging.pages.dev`, los activos/PDFs se sirvan desde recursos bajo control del cliente, el build sea reproducible desde Git y la lista de pruebas esté aprobada. Ninguno de esos pasos autoriza todavía cambiar DNS, cancelar Wix, migrar el dominio, activar un formulario con backend, contratar WordPress ni relacionar el sitio con OmniRoute.

## Referencias

[1]: [Cloudflare Pages — Git integration](https://developers.cloudflare.com/pages/get-started/git-integration/)

[2]: [Cloudflare Pages — Build configuration](https://developers.cloudflare.com/pages/configuration/build-configuration/)

[3]: [Cloudflare Pages — Preview deployments](https://developers.cloudflare.com/pages/configuration/preview-deployments/)

[4]: [Cloudflare Pages — Build image](https://developers.cloudflare.com/pages/configuration/build-image/)

[5]: [Cloudflare Pages — Add a custom domain to a branch](https://developers.cloudflare.com/pages/how-to/custom-branch-aliases/)

[6]: [WordPress.org — Requirements](https://wordpress.org/about/requirements/)

[7]: [Cloudflare Pages — GitHub integration](https://developers.cloudflare.com/pages/configuration/git-integration/github-integration/)
