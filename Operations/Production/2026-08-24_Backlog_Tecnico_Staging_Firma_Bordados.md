---
title: "Backlog técnico de bajo riesgo — Staging Firma Bordados"
purpose: "Priorizar mejoras de rendimiento, accesibilidad, seguridad técnica y operación del staging que no dependan de materiales, tiempos de entrega o mínimos de pedido."
status: Active
created: 2026-08-24
updated: 2026-08-24
version: "1.11"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-23_Guia_Staging_Cloudflare_Pages_Firma_Bordados.md"
  - "Operations/Production/2026-08-23_Evaluacion_Migracion_Wix_Hosting_IA.md"
  - "Operations/Production/2026-08-24_Inventario_Catalogos_Drive_Firma_Bordados.md"
  - "GrowthOS/00_01_Changelog_GrowthOS.md"
organization: "Operations/Production"
---

# Backlog técnico de bajo riesgo — Staging Firma Bordados

## 1. Estado auditado

El staging `https://firma-bordados-staging.pages.dev` construye correctamente desde la rama `main` y sirve activos locales, catálogos, WhatsApp y el formulario `mailto:` sin depender de Wix o Manus. La rama `staging` queda como integración y revisión antes de una promoción explícita a `main`. La interfaz ya respeta `prefers-reduced-motion` para sus revelados, y los catálogos se abren en una pestaña separada.

La auditoría identificó ajustes que no requieren información comercial adicional. La copia inicial generaba un JavaScript principal de aproximadamente 562 kB sin comprimir (≈163 kB gzip) y conservaba providers genéricos que no usaba la landing. Tras P1, el bundle principal quedó en 451.78 kB (127.12 kB gzip), una reducción aproximada de 19% sin comprimir y 22% comprimido. Ninguno de estos cambios altera servicios, precios, materiales, tiempos, mínimos, dominio o DNS.

## 2. Prioridades

| Prioridad | Ajuste | Beneficio | Dependencia | Riesgo de contenido |
| :--- | :--- | :--- | :--- | :--- |
| P0 | Paquete de accesibilidad: eliminar `maximum-scale=1`, añadir enlace de salto, estados `:focus-visible` y desactivar `scroll-behavior: smooth` con reducción de movimiento | Mejora teclado, zoom y comodidad sin cambiar la propuesta visual | Ninguna | Nulo |
| P0 | Añadir meta `robots=noindex,nofollow` al staging, además de `robots.txt` | Evita presentar la versión temporal como sitio final en buscadores | Ninguna | Nulo |
| P0 | Crear `client/public/_headers` con `X-Content-Type-Options`, `Referrer-Policy` y `Permissions-Policy` restrictiva | Endurece la respuesta estática sin introducir backend | Probar WhatsApp, PDFs y redes tras el cambio | Nulo |
| P1 aplicado | Marcar imágenes no críticas con `loading="lazy"` y `decoding="async"`; dar prioridad solo a la imagen hero | Reduce carga inicial percibida y preserva el hero | Ninguna | Nulo |
| P1 aplicado | Simplificar el núcleo React: retirar `ThemeProvider`, `TooltipProvider` y `Toaster` inactivos; medir el bundle antes de podar dependencias | Reduce superficie de runtime y facilita mantenimiento | Prueba visual y build | Nulo |
| P1 aplicado | Añadir CI de GitHub: `pnpm check` y `pnpm exec vite build` para cada Pull Request y push a `main`/`staging` | Evita que un cambio de contenido rompa el deploy | Repositorio privado Io Marketing | Nulo |
| P1 aplicado con límite de plan | Mantener `main` privado y formalizar el gate rama de trabajo → PR a `staging` → CI → promoción explícita a `main` → CI | Reduce cambios accidentales sin exponer activos ni elevar el plan | GitHub Pro/Team si se requiere enforcement nativo | Nulo |
| P2 | Añadir Open Graph, Twitter Card y JSON-LD de negocio local | Mejora previsualización y preparación SEO del futuro dominio | Validar nombre legal, teléfono preferido, dirección y horarios antes de declarar datos estructurados | Bajo |
| P2 | Añadir analítica de eventos para clics en WhatsApp, correo y PDFs | Mide intención comercial y ayuda a priorizar catálogo/CTA | Consentimiento de privacidad, herramienta y responsable de datos | Medio |
| P2 | Sustituir `mailto:` por formulario con backend | Recibe solicitudes aunque el cliente no tenga app de correo configurada | Aviso de privacidad, destinatario, antispam y proceso de respuesta | Medio |

## 3. Paquete P0 aplicado

El paquete **P0 de accesibilidad y protección de staging** se aplicó en el commit `b3754d0` y se promovió a la rama `main` que Cloudflare Pages usa para este sitio de prueba. Incluye zoom habilitado, estados de foco, enlace de salto, reducción de movimiento integral, meta noindex y encabezados estáticos. Se validó en build, escritorio y móvil, y no cambia la oferta comercial ni recaba datos.

## 4. Paquete P1 aplicado

El paquete **P1 de mantenimiento** se integró primero a `staging` en los commits `f49a344` y `beaaa8d`, pasó las validaciones locales y obtuvo ejecuciones exitosas de GitHub Actions tanto en `staging` como en `main`. La configuración añade `.github/workflows/validate.yml`, que instala el lockfile congelado y ejecuta `pnpm check` y `pnpm exec vite build` en Pull Requests y pushes a las ramas operativas. Un primer intento detectó que el cache de `setup-node` buscaba `pnpm` antes de activarlo; se corrigió retirando ese cache y la ejecución final terminó correctamente antes de promover a `main`.

La landing ya no monta `ThemeProvider`, `TooltipProvider` ni `Toaster`. Se retiraron `next-themes`, `sonner`, el módulo Sonner y el contexto de tema, y se mantuvo el límite de errores con una pantalla breve en español que no expone trazas. `@radix-ui/react-tooltip` se conserva por ahora: un componente de sidebar residual aún lo importa y TypeScript compila todo el árbol fuente aunque el sidebar no entre al bundle. Esta dependencia no se cargó en el runtime activo; una poda adicional exige retirar o modularizar ese código residual en una tarea separada.

También se dio prioridad de red a la imagen hero y se aplicó carga diferida/decodificación asíncrona a las fotografías de proceso y al logo del formulario, que aparecen fuera de la primera pantalla. Después de la build, el JavaScript principal pasó de ≈562 kB a 451.78 kB sin comprimir (≈19% menos) y de ≈163 kB a 127.12 kB gzip (≈22% menos). La promoción rápida a `main` dejó ambas ramas en `beaaa8d`; Pages sirvió un nuevo artefacto y se volvieron a confirmar `noindex,nofollow,noarchive`, `robots.txt` y los headers P0.

La protección técnica de `main` se evaluó tras la autorización de Fernando. GitHub rechazó branch protection y rulesets para el repositorio privado actual porque requieren GitHub Pro o una visibilidad pública. La visibilidad no se cambió y no se elevó el plan. En su lugar, se documentó y validó el gate operativo: rama de trabajo → Pull Request a `staging` → CI y build → promoción explícita a `main` → CI → despliegue en la URL pública de staging.

## 5. Mejoras comerciales recomendadas sin bloquear por materiales

| Prioridad | Mejora propuesta | Beneficio esperado | Dependencia | Estado recomendado |
| :--- | :--- | :--- | :--- | :--- |
| C1 aplicado | Crear una sección «Cómo solicitar» en tres pasos: compartir necesidad, elegir opción de prenda/catálogo y confirmar detalles con el equipo | Reduce incertidumbre para una primera consulta sin prometer precio ni plazo | Ninguna | Publicado en staging |
| C1 aplicado | Mejorar el mensaje inicial de WhatsApp con campos opcionales de prenda, técnica, cantidad aproximada y uso | Aumenta la calidad de los leads sin almacenar datos en el sitio | Validar solo la redacción | Publicado en staging |
| C1 aplicado | Añadir una franja de «Marcas disponibles por catálogo»: BigBang, M&O y Soul & Blues, con enlace a cada PDF | Convierte los catálogos en una razón visible para consultar y respalda la oferta con fuentes existentes | Dickies sigue fuera hasta recibir su catálogo | Publicado en staging |
| C2 aplicado | Añadir un FAQ breve: mínimo de serigrafía de 12 piezas, tiempos que se confirman por pedido/carga y categorías de prendas consultables | Resuelve objeciones frecuentes sin inventar condiciones | Ninguna | Publicado en staging |
| C2 aplicado | Ampliar el portafolio con fotografías reales autorizadas, ocultando o excluyendo marcas de clientes sin permiso | Aumenta confianza mediante evidencia de trabajo | Curaduría y permisos por imagen | Publicado con evidencia de digitalización |
| C3 aplicado | Añadir enlace de ubicación con indicaciones y revisar información de contacto visible | Reduce fricción para visitas o llamadas | Dirección confirmada y enlace técnico validado | Publicado en staging |
| P3 | Implementar formulario con backend y analítica de intención | Mejora captura y medición de solicitudes | Aviso de privacidad revisado, antispam, elección de ruta y proceso de respuesta | Bloqueado hasta decisión operativa |
| C1.1 aplicado | Cambiar el destino de «Cómo solicitar» a correo guiado y mantener WhatsApp como alternativa | Prioriza una consulta estructurada sin introducir captura de datos en el sitio | Ninguna; usa el `mailto:` ya confirmado | Publicado en staging |
| C4 aplicado | Añadir aviso de privacidad estático, enlazado desde el footer y marcado como revisión de staging | Hace visible el marco de privacidad antes de cualquier formulario servidor-side | Observación operativa del correo guiado; revisión de Firma Bordados antes de activación de formulario | Activo en staging |

### Decisión recomendada sobre GitHub Pro

GitHub Pro no es necesario hoy para el staging: existe un solo flujo de mantenimiento, CI ya valida build/tipos y el gate operativo reduce el riesgo sin coste adicional. Se vuelve recomendable cuando participen varios colaboradores, el cliente quiera aprobar Pull Requests desde GitHub, haya cambios frecuentes o se necesite impedir técnicamente los pushes directos a `main`. La protección nativa puede exigir Pull Requests, revisiones y checks antes de permitir cambios en una rama protegida.[1]

### Paquete C1 aplicado — 2026-08-25

El commit `9fd686e` añadió una sección «Cómo solicitar» en tres pasos, un CTA de WhatsApp que prellena campos opcionales de prenda, técnica, cantidad aproximada y uso, y una franja de marcas por catálogo. El Pull Request 5 pasó CI, se integró en `staging` y el merge `a6e1a21` se promovió a `main`. La verificación técnica del bundle publicado confirmó la sección de solicitud y la franja de marcas, y confirmó que Dickies no aparece hasta recibir su catálogo. El sitio no almacena datos del mensaje guiado, no añade precios ni tiempos y no modifica Wix, DNS ni el dominio público.

### Paquete C2 aplicado — 2026-08-25

El commit `2ca773f` incorporó un FAQ con los límites confirmados —serigrafía a partir de 12 piezas, tiempos según cantidad/requerimiento/carga, categorías de prenda consultables y exclusión de parches/gorras— y añadió una tarjeta de «Digitalización en proceso» al portafolio. El Pull Request 6 pasó CI, se integró a `staging` y el merge `67f3f1f` se promovió a `main`. La comprobación técnica encontró el FAQ y la tarjeta en el bundle publicado, y el activo local respondió HTTP 200. No se añadieron materiales, precios, plazos exactos, analytics, backend de formulario, Wix, DNS ni dominio público.

### Paquete C3 aplicado — 2026-08-25

El commit `b3e6f57` añadió un enlace «Cómo llegar» que construye indicaciones de Google Maps a partir de la dirección confirmada: Emilio Carranza #1021 Int. 113, Col. Burócratas, Piedras Negras, Coahuila. El Pull Request 7 pasó CI, se integró a `staging` y el merge `82be09b` se promovió a `main`. La comprobación técnica confirmó HTTP 200 del destino y encontró el enlace dentro del bundle público; se conservaron correo, WhatsApp, teléfonos y horario visibles. No se incorporó mapa embebido, geolocalización, backend, analítica, Wix, DNS ni dominio público.

### Ajuste C1.1 aplicado — 2026-08-25

El commit `ba952d9` cambió el CTA de la franja «Cómo solicitar» a un correo guiado dirigido a `firmabordados@yahoo.com`, con asunto y campos opcionales de prenda, técnica, cantidad aproximada y uso/requerimiento. El Pull Request 8 pasó CI, se integró a `staging` y el merge `c694741` se promovió por avance rápido a `main`. La comprobación HTTP del staging confirmó la sección, el enlace `mailto:`, la continuidad de WhatsApp y la ausencia de Dickies en el bundle. No se activaron backend, proveedor, Turnstile, secreto, almacenamiento, analítica, Wix, DNS ni dominio público.

La operación de privacidad ya confirmó el correo `firmabordados@yahoo.com` para solicitudes ARCO y una persona interna responsable de revisarlo. Se propone conservar las consultas hasta doce meses desde la última interacción, con eliminación o disociación posterior salvo obligación comercial, legal o contractual. Este criterio sigue sujeto a revisión antes de publicar el aviso. La ruta recomendada permanece: correo guiado ahora; proveedor gestionado solo con aprobación explícita si se requiere formulario antes de mover DNS; o Pages Function + Turnstile + Cloudflare Email Service tras una migración aprobada a Cloudflare DNS. No se activó ninguna integración.

### Paquete C4 aplicado — 2026-08-24

El commit `87ec478` añadió una página estática de aviso de privacidad en la ruta `/privacidad/`, con enlace desde el footer, responsable Firma Bordados, domicilio confirmado, correo ARCO, finalidades limitadas, política propuesta de doce meses y un aviso claro de que el staging no almacena datos del correo guiado. El Pull Request 9 pasó CI y se promovió a `main`; la ruta sin barra final reveló una redirección de Pages al inicio, por lo que el Pull Request 10 corrigió los enlaces y la regla de SPA a la ruta canónica con barra final. El merge `402cffe` se promovió a `main`; la comprobación HTTP final devolvió 200 para `/privacidad/`, confirmó el contenido, ausencia de nombres personales retirados y `robots.txt` bloqueado. No se activaron formulario servidor-side, backend, Turnstile, proveedor, secreto, analítica, almacenamiento, Wix, DNS, nameservers ni dominio público.

Fernando aprobó el texto del aviso para el staging y confirmó mantener el correo guiado como flujo de solicitud. Se propone revisar la operación tras 30 días calendario, sin analítica web: comprobar manualmente si el correo permite recibir datos suficientes, si el equipo responde de forma consistente y si existen consultas perdidas o incompletas. Solo si esa revisión evidencia fricción se reabrirá la decisión de formulario gestionado o backend propio.

### Decisión de alcance vigente — 2026-08-24

Fernando confirmó que, por ahora, el staging no incorporará materiales, composiciones, certificaciones, disponibilidad ni condiciones comerciales adicionales. El sitio se mantiene con servicios, mínimos, catálogos y condiciones que ya cuentan con confirmación documental. Esta decisión evita afirmar especificaciones o promesas sin respaldo; los datos pendientes podrán reabrirse solo cuando Firma Bordados los confirme y se autorice su inclusión.

### Prueba temporal de recepción — 2026-08-24

El commit `5c4a1e0` dirigió temporalmente el correo guiado y el formulario local del staging a `io.marketin.09@gmail.com` para comprobar la recepción desde un dispositivo real. El Pull Request 11 pasó CI, se integró a `staging` y el merge `41ed194` se promovió a `main`. El sitio muestra avisos de prueba y pide no enviar datos reales; WhatsApp, el correo directo y la página de privacidad conservan `firmabordados@yahoo.com`. La comprobación HTTP confirmó ambos destinos de página con 200, el buzón provisional únicamente en el flujo de prueba y el correo oficial dentro de privacidad. Tras confirmar la recepción, se debe restaurar inmediatamente `firmabordados@yahoo.com` como destino de correo guiado y del formulario local mediante el mismo flujo de revisión.

## 6. Límites hasta recibir la información del cliente

No se deben añadir precios, cotizadores, promesas de tiempo, mínimos de pedido, materiales, certificaciones, formularios que almacenen datos, analytics de terceros ni SEO estructurado definitivo. La URL `*.pages.dev` debe seguir marcada como staging y el dominio `firmabordados.com` no debe asociarse al proyecto hasta el gate de aprobación, transferencia/operación administrada y migración documentado.

## Referencias

[1]: [GitHub Docs — About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
