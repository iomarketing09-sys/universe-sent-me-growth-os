---
title: "Auditoría Gate 3 — Dominio y DNS de Firma Bordados"
purpose: "Registrar el estado público de dominio y DNS, los riesgos, los datos faltantes y la secuencia de reversión requerida antes de una futura migración desde Wix."
status: Review
created: 2026-08-25
updated: 2026-08-25
version: "1.0"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-23_Evaluacion_Migracion_Wix_Hosting_IA.md"
  - "Operations/Production/2026-08-23_Guia_Staging_Cloudflare_Pages_Firma_Bordados.md"
  - "Operations/Production/2026-08-25_Propuesta_Cotizacion_Migracion_Mantenimiento_Firma_Bordados.md"
  - "Operations/Production/todo.md"
organization: "Operations/Production"
---

# Auditoría Gate 3 — Dominio y DNS de Firma Bordados

> **Auditoría pasiva — no es un cambio de DNS.** Esta revisión consultó únicamente datos públicos de `firmabordados.com`. No se inició sesión en Wix, no se alteró ningún registro, nameserver, dominio, cuenta ni facturación.

## 1. Resultado del inventario público

| Elemento | Hallazgo público al 2026-08-25 | Implicación para la migración |
| :--- | :--- | :--- |
| Dominio | `firmabordados.com` | El dominio debe seguir bajo control y renovación del cliente. |
| Nameservers | `ns14.wixdns.net` y `ns15.wixdns.net` | La zona DNS actual está administrada por Wix. Cambiar el dominio raíz a Cloudflare Pages requerirá una autorización independiente para mover la zona/nameservers a Cloudflare. |
| Registros A del dominio raíz | `185.230.63.171`, `185.230.63.107`, `185.230.63.186` | Son destinos de Wix que deben guardarse como estado de reversión; no deben copiarse como destino de la nueva página. |
| `www` | CNAME a `cdn1.wixdns.net` que resuelve, al momento de la consulta, hacia infraestructura Wix | Debe definirse si producción usará raíz o `www` como URL canónica y preparar su redirección. |
| MX/TXT/AAAA en el apex | La consulta pública no devolvió registros de esos tipos en el apex | La ausencia en la respuesta pública no demuestra que no existan subdominios o servicios dependientes. Debe revisarse/exportarse la zona completa desde Wix antes de cambiar nameservers. |
| Registro del dominio | RDAP público muestra registro el 2026-02-19 y vencimiento el 2027-02-19 | Es una referencia pública, no sustituye confirmar en Wix quién es registrante, quién paga y cuándo se cobra la renovación. |

## 2. Riesgo principal y decisión técnica

El riesgo principal no es Cloudflare Pages: es **perder o recrear de forma incompleta la zona DNS de Wix** al cambiar los nameservers. Aunque actualmente no se ven MX ni TXT en el apex, antes de un cambio se deben inventariar todos los registros y servicios: correo, verificaciones de terceros, redirecciones, subdominios, SPF/DKIM/DMARC, Search Console, píxeles y cualquier integración no visible en la página.

Para servir el dominio raíz en Cloudflare Pages, la zona debe estar configurada en Cloudflare; Cloudflare documenta que los dominios raíz requieren que Cloudflare sea el DNS autoritativo de la zona. Un subdominio puede conectarse por CNAME sin trasladar toda la zona, pero no sustituye el corte del dominio raíz.[3]

## 3. Datos que debe confirmar Firma Bordados antes de cerrar el gate

| Pregunta o evidencia requerida | Cómo obtenerla sin compartir credenciales | Estado |
| :--- | :--- | :--- |
| Quién es el registrante y quién autoriza cambios de dominio | Confirmación escrita del cliente | Pendiente |
| Fecha e importe de renovación del dominio y del plan Wix | Captura o dato visible del panel de Wix, sin mostrar contraseñas ni datos de pago | Pendiente |
| Inventario completo de zona DNS | Exportación, captura o lista de registros desde Wix: host, tipo, valor, prioridad y TTL | Pendiente |
| Servicios conectados al dominio | Confirmar correo, Google Workspace, Microsoft 365, formularios, CRM, Search Console y subdominios | Pendiente |
| URL canónica para producción | Decidir `firmabordados.com` o `www.firmabordados.com` y la redirección de la variante secundaria | Pendiente |
| Propietario de la operación | Confirmado: Io Marketing operará Cloudflare Pages y repositorio bajo acuerdo administrado; el dominio sigue siendo del cliente | Parcialmente confirmado |

## 4. Plan de corte propuesto — aún no autorizado

| Fase | Acción | Condición de entrada | Reversión |
| :--- | :--- | :--- | :--- |
| Preparación | Guardar la zona Wix completa, nameservers actuales y evidencias de rutas/contactos; fijar una versión aprobada en Git | Cliente aprobó contenido, operación y ventana | No hay cambio público; se detiene sin impacto. |
| Asociación | Añadir el dominio al proyecto Cloudflare Pages y revisar los valores requeridos, sin aplicarlos aún | Acceso autorizado a la cuenta operativa de Cloudflare | Quitar la asociación propuesta si el cliente no aprueba. |
| Aprobación | Presentar al cliente el cambio exacto de nameservers/DNS, hora de corte, URL canónica y contactos de contingencia | Inventario completo y confirmación de que no faltan servicios | No ejecutar si falta un dato. |
| Corte | Aplicar solo los valores aprobados y mantener Wix activo durante propagación | Confirmación explícita del cliente | Restaurar los nameservers Wix y el inventario previo si hay una falla crítica. |
| Validación | Probar raíz, `www`, HTTPS, catálogos, correo, WhatsApp, privacidad y 404 desde varias redes | Resolución hacia la nueva página | Mantener Wix disponible; volver a la zona previa si la validación falla. |
| Cierre | Retirar `noindex`, habilitar SEO de producción y aceptar el resultado por escrito | Estabilidad acordada y aceptación del cliente | Wix no se reduce ni cancela todavía. |

No se debe reducir ni cancelar Wix hasta completar un periodo de estabilidad acordado después del corte. Wix indica que al conectar un dominio de Wix a un sitio externo se modifican registros A y CNAME y que la propagación puede tardar hasta 48 horas.[4]

## 5. Estado del Gate 3

| Criterio | Estado |
| :--- | :--- |
| Inventario público de DNS | Completado de forma pasiva |
| Control de registrante, renovación y facturación | Pendiente de confirmación del cliente |
| Zona DNS completa y dependencias | Pendiente de evidencia desde Wix |
| Aprobación de cambio de nameservers/DNS | No solicitada; bloqueada |
| Plan de reversión documentado | Preparado, pendiente de completar con la zona real |
| Gate 3 listo para corte | **No** |

## Referencias

[1]: [Consulta DNS pública de `firmabordados.com`](https://cloudflare-dns.com/dns-query?name=firmabordados.com&type=NS)

[2]: [Registro RDAP público de `firmabordados.com`](https://rdap.verisign.com/com/v1/domain/firmabordados.com)

[3]: [Cloudflare Pages — dominios personalizados](https://developers.cloudflare.com/pages/configuration/custom-domains/)

[4]: [Wix — conectar un dominio Wix a un sitio externo](https://support.wix.com/en/article/connecting-a-wix-domain-to-an-external-site)
