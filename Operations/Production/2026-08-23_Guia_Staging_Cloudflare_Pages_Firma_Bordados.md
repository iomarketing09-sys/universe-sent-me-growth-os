---
title: "Guía de staging reversible en Cloudflare Pages — Firma Bordados"
purpose: "Definir los pasos técnicos para probar el sitio React/Vite de Firma Bordados en Cloudflare Pages sin modificar Wix, el DNS del dominio ni el sitio público actual; incluir el criterio para descartar o adoptar WordPress."
status: Review
created: 2026-08-23
updated: 2026-08-23
version: "1.0"
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
