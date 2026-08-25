---
title: "Auditoría Gate 3 — Dominio y DNS de Firma Bordados"
purpose: "Registrar el estado público de dominio y DNS, los riesgos, los datos faltantes y la secuencia de reversión requerida antes de una futura migración desde Wix."
status: Review
created: 2026-08-25
updated: 2026-08-25
version: "1.1"
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
| Registros A del dominio raíz | `185.230.63.107`, `185.230.63.186`, `185.230.63.171`; TTL 1 hora | Confirmados desde el panel Wix como estado de reversión; no deben copiarse como destino de la nueva página. |
| `www` | CNAME a `cdn1.wixdns.net`; TTL 1 hora | La URL canónica confirmada será el dominio raíz; `www` debe redirigir al raíz después del corte. |
| `es` | CNAME a `cdn1.wixdns.net`; TTL 1 hora | Alias Wix actual. Se propone redirigirlo al dominio raíz en producción, sujeto a aprobación en el corte. |
| `m` | CNAME a `www247.wixdns.net`; TTL 1 hora | Alias móvil Wix actual. Se propone redirigirlo al dominio raíz en producción, sujeto a aprobación en el corte. |
| MX/TXT/AAAA en el apex | No hay registros en la zona Wix aportada | El cliente confirmó que no hay servicios ligados al dominio; no obstante, se conserva esta zona como referencia de reversión. |
| Renovación del dominio | Io Marketing paga $470 MXN; fecha de renovación 19 de febrero | Incluir como partida externa anual y verificar el registrante público/autoridad antes de cualquier transferencia o cambio de cuenta. |
| Registro del dominio | RDAP público muestra registro el 2026-02-19 y vencimiento el 2027-02-19 | Coincide con la fecha anual confirmada por Io Marketing; falta identificar por escrito quién figura como registrante y autoriza transferencias. |

## 2. Riesgo principal y decisión técnica

El riesgo principal no es Cloudflare Pages: es **perder o recrear de forma incompleta la zona DNS de Wix** al cambiar los nameservers. Aunque actualmente no se ven MX ni TXT en el apex, antes de un cambio se deben inventariar todos los registros y servicios: correo, verificaciones de terceros, redirecciones, subdominios, SPF/DKIM/DMARC, Search Console, píxeles y cualquier integración no visible en la página.

Para servir el dominio raíz en Cloudflare Pages, la zona debe estar configurada en Cloudflare; Cloudflare documenta que los dominios raíz requieren que Cloudflare sea el DNS autoritativo de la zona. Un subdominio puede conectarse por CNAME sin trasladar toda la zona, pero no sustituye el corte del dominio raíz.[3]

## 3. Datos que debe confirmar Firma Bordados antes de cerrar el gate

| Pregunta o evidencia requerida | Cómo obtenerla sin compartir credenciales | Estado |
| :--- | :--- | :--- |
| Quién es el registrante y quién autoriza cambios de dominio | Confirmación escrita del cliente | Pendiente: Io Marketing paga renovación, pero el registrante aún no se ha identificado. |
| Fecha e importe de renovación del dominio y del plan Wix | Confirmación recibida: Io Marketing paga $470 MXN; renovación el 19 de febrero | Confirmado; falta separar el importe exacto de cualquier plan Wix si sigue activo antes del corte. |
| Inventario completo de zona DNS | Lista recibida desde Wix con A, CNAME y NS; TTL de 1 hora para A/CNAME y 1 día para NS | Confirmado para la zona reportada. |
| Servicios conectados al dominio | Cliente confirma que no hay servicios ligados al dominio | Confirmado. |
| URL canónica para producción | `firmabordados.com`; `www` redirige al raíz | Confirmado. |
| Propietario de la operación | Confirmado: Io Marketing operará Cloudflare Pages y repositorio bajo acuerdo administrado; el dominio sigue siendo del cliente | Parcialmente confirmado |

## 4. Plan de corte propuesto — aún no autorizado

| Fase | Acción | Condición de entrada | Reversión |
| :--- | :--- | :--- | :--- |
| Preparación | Guardar el inventario confirmado: tres A del root, CNAME `www`, `es`, `m`, nameservers Wix y TTL; fijar una versión aprobada en Git | Cliente aprobó contenido, operación y ventana | No hay cambio público; se detiene sin impacto. |
| Asociación | Añadir `firmabordados.com` y `www.firmabordados.com` al proyecto Cloudflare Pages y obtener de Cloudflare los nameservers exactos de la zona nueva, sin aplicarlos aún | Acceso autorizado a la cuenta operativa de Cloudflare | Quitar la asociación propuesta si el cliente no aprueba. |
| Aprobación | Presentar al cliente los nameservers de Cloudflare, ventana, contactos, raíz como URL canónica y redirecciones de `www`, `es` y `m` hacia la raíz | Identificación del registrante/autoridad y aprobación explícita | No ejecutar si falta un dato. |
| Corte | Reemplazar solo los nameservers Wix por los valores que genere Cloudflare, recrear registros indispensables si aparecen durante la asociación y mantener Wix activo durante propagación | Confirmación explícita del cliente | Restaurar `ns14.wixdns.net` y `ns15.wixdns.net`; la zona Wix guardada vuelve a ser autoritativa. |
| Validación | Probar raíz, `www`, `es`, `m`, HTTPS, catálogos, correo, WhatsApp, privacidad y 404 desde varias redes | Resolución hacia la nueva página | Mantener Wix disponible; volver a nameservers Wix si la validación falla. |
| Cierre | Retirar `noindex`, habilitar SEO de producción y aceptar el resultado por escrito | Estabilidad acordada y aceptación del cliente | Wix no se reduce ni cancela todavía. |

No se debe reducir ni cancelar Wix hasta completar un periodo de estabilidad acordado después del corte. Wix indica que al conectar un dominio de Wix a un sitio externo se modifican registros A y CNAME y que la propagación puede tardar hasta 48 horas.[4]

## 5. Estado del Gate 3

| Criterio | Estado |
| :--- | :--- |
| Inventario público de DNS | Completado de forma pasiva |
| Control de registrante, renovación y facturación | Renovación confirmada: Io Marketing paga $470 MXN el 19 de febrero; registrante pendiente |
| Zona DNS completa y dependencias | Confirmada por el cliente: A/CNAME/NS reportados y sin servicios ligados al dominio |
| Aprobación de cambio de nameservers/DNS | No solicitada; bloqueada |
| Plan de reversión documentado | Preparado con nameservers y registros Wix confirmados |
| Gate 3 listo para corte | **No** — falta identificar registrante/autoridad y autorizar explícitamente el cambio de nameservers |

## Referencias

[1]: [Consulta DNS pública de `firmabordados.com`](https://cloudflare-dns.com/dns-query?name=firmabordados.com&type=NS)

[2]: [Registro RDAP público de `firmabordados.com`](https://rdap.verisign.com/com/v1/domain/firmabordados.com)

[3]: [Cloudflare Pages — dominios personalizados](https://developers.cloudflare.com/pages/configuration/custom-domains/)

[4]: [Wix — conectar un dominio Wix a un sitio externo](https://support.wix.com/en/article/connecting-a-wix-domain-to-an-external-site)
