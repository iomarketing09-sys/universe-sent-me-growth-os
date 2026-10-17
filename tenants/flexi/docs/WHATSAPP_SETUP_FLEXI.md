# WhatsApp Cloud API — Estado y Configuración (Flexi)

**Tenant:** `flexi` · **Actualizado:** 2026-10-16 · **Fuente:** Graph API v20.0 (lectura + escritura autorizada para plantillas HSM)

---

## 1. Identificadores (no secretos)

| Dato | Valor |
|---|---|
| WABA ID | `1087457280345914` ("Flexi Piedras Negras") |
| Phone Number ID | `1327098437161178` |
| Número visible | `+52 1 878 138 5284` |
| Plataforma | `CLOUD_API` |
| Template namespace | `89ed08bd_a11b_4974_99c7_a878da60dd2d` |
| Business propietario | `1940942776222567` — "Fernando Galindo de los Reyes" (portafolio personal) |

## 2. Estado de la cuenta

| Campo | Valor | Comentario |
|---|---|---|
| `account_review_status` | **APPROVED** | ✅ |
| Número `status` | **CONNECTED** | ✅ |
| `platform_type` | CLOUD_API | ✅ (no es la app de teléfono) |
| **`is_on_biz_app`** | ✅ **true** | **Coexistencia activa: el número sigue funcionando en la app del teléfono** |
| `account_mode` | `LIVE` | En producción |
| Límite de mensajería | **`TIER_2K`** | 2,000 conversaciones iniciadas/24 h. El campo viejo `messaging_limit_tier` (=`TIER_250`) está **deprecado**; ver §2.e |
| `throughput` | `STANDARD` | |
| `code_verification_status` | ℹ️ **NOT_VERIFIED** | Esperado en coexistencia; no aplica verificación por SMS/llamada (el número ya vive en la app) |
| `name_status` | ℹ️ **NON_EXISTS** | **Esperado en coexistencia, no es bloqueante** — ver §2.d |
| Plantillas HSM en Meta | **6** | Las 6 creadas vía API y **APROBADAS por Meta** el 2026-10-16 (`PENDING` → `APPROVED` en ~25 min) |

## 2.b Coexistencia (App + API en el mismo número) — CONFIRMADO

El número opera en modo **Coexistence** (`is_on_biz_app: true`), habilitado vía Embedded Signup (disponible desde mayo 2025). Implica:

- La sucursal **sigue usando la app de WhatsApp Business** en el teléfono, sin perder historial ni contactos.
- Lo que envía la **API** aparece en la app; lo que la sucursal escribe en la **app** se refleja al webhook (`smb_message_echoes`).
- Mensajes enviados **desde la app son gratis**; los enviados por **API se cobran** por mensaje.
- Sigue aplicando la **ventana de servicio de 24 h** para mensajes de API.
- Sin badge de cuenta oficial (OBA) ni verificación de negocio estándar mientras esté en coexistencia.

> ⚠️ **No usar** el flujo estándar de "registrar número" de Cloud API: eso SÍ desconectaría la app. Todo cambio debe mantenerse dentro de coexistencia.

## 2.c Plantillas HSM creadas (2026-10-16)

Sometidas vía `POST /1087457280345914/message_templates` (`language: es_MX`):

| Plantilla | ID Meta | Categoría | Estado |
|---|---|---|---|
| `bienvenida` | `1419854380122296` | UTILITY | ✅ APPROVED |
| `confirmacion_pedido` | `2299930924141391` | UTILITY | ✅ APPROVED |
| `recordatorio_carrito` | `1143314561789158` | MARKETING | ✅ APPROVED |
| `oferta_especial` | `28964419769858511` | MARKETING | ✅ APPROVED |
| `satisfaccion_postcompra` | `1114575207649407` | UTILITY | ✅ APPROVED |
| `reenganche` | `2168676927394126` | MARKETING | ✅ APPROVED |

> Las 3 MARKETING requieren **opt-in** del cliente antes de enviarse. Meta aprobó las 6 el **2026-10-16** (menos de 30 minutos desde el envío); `templates.json` ya refleja ID, cuerpo, estado y `approved_at` reales.

## 2.d Nombre para mostrar y perfil de negocio

**Nombre (`verified_name`):** `Flexi Piedras Negras` · `name_status = NON_EXISTS` · `new_name_status = NONE`.

- `NON_EXISTS` **no es un bloqueante**: significa que el nombre nunca pasó por la revisión de nombres de Cloud API. En coexistencia Meta **no otorga badge de cuenta oficial (OBA) ni verificación de negocio estándar**.
- La revisión del nombre va atada al **registro** del número y, si se aprueba un cambio, Meta exige **re-registrar el número dentro de 14 días** — es decir, el registro que sí rompería la coexistencia. Por eso **no se envía por API** (`POST /{phone-number-id}?new_display_name=...`).
- Si el cliente quiere revisar o cambiar el nombre, se hace **desde la app de WhatsApp Business o WhatsApp Manager → Perfil** (respeta coexistencia).

**Perfil de negocio** (activo y poblado, verificado por API):

| Campo | Valor actual |
|---|---|
| `address` | Calle Av. Industrial 203, Parque Industrial Piedras Negras, 26070 Piedras Negras, Coah., México |
| `description` | "Distribuidor oficial Flexi 👢✨ / Calzado de calidad, comodidad y estilo para toda la familia. / Atención personalizada en Piedras Negras ✨" |
| `vertical` | `RETAIL` |
| `profile_picture_url` | ✅ definida |
| `about` | (vacío) |
| `email` / `websites` | (vacíos — se pueden completar por API sin riesgo) |

> Nota: la dirección del perfil de WhatsApp es más específica que la del repo (`tenants/flexi/config.json` dice solo "Piedras Negras, Coahuila, México"). Conviene decidir cuál es la canónica antes de tocar configs de otros canales (GBP, etc.).

## 2.e Límite de mensajería y portafolio (verificado 2026-10-16)

- Límite real: **2,000 conversaciones iniciadas por la empresa / 24 h** (`whatsapp_business_manager_messaging_limit = TIER_2K`), en ventana móvil y solo para mensajes **fuera** de la ventana de servicio de 24 h. Coincide con lo que muestra WhatsApp Manager.
- ⚠️ Los límites se cuentan **por portafolio de negocio**, no por número, y se **comparten**: el WABA de Flexi vive en el portafolio **personal** ("Fernando Galindo de los Reyes"). Si mañana se conecta otro número ahí (Country, Quirelli, otro tenant) comparten los 2,000, y la continuidad depende de ese perfil personal.
- Recomendación (Fase 2): mover el WABA a un **portafolio propio de Flexi** y operar con **System User token**.
- Del token: `debug_token` → app `Universe Publicaciones` (`26134666266196379`), tipo `USER`, `expires_at: 0` (hoy no expira) pero **`data_access_expires_at` ≈ 2027-01-15**: al vencer hay que reautorizar.

## 2.f Webhook de producción (Cloudflare Worker + D1) — ACTIVO

Plan relacionado: `PLAN_WHATSAPP_FLEXI.md`.

- ✅ **Receptor de producción:** **Cloudflare Worker + D1** en `https://flexi-whatsapp-webhook.io-marketing-09.workers.dev/webhook` (base `flexi_whatsapp_obs`), desplegado el 2026-10-16. Código en `tenants/flexi/whatsapp/webhook-worker/` (`GET /health`, `GET /webhook`, `POST /webhook`, `GET /stats?token=…`); pruebas `npm test` → 36/36.
- ✅ **Callback URL de Meta apuntando al Worker** (2026-10-16): `/stats` ya reporta `verificaciones_ok: 1` y el campo `messages` está suscrito → los eventos se entregan.
- **No envía nada:** el Worker no contiene ninguna llamada saliente a Meta (`listen_only: true`). Los teléfonos se guardan **hasheados** (SHA-256 truncado + últimos 4 dígitos).
- **Datos:** tablas `events` (campo `intent` por mensaje; los envíos de la sucursal desde la app entran como `direction="out_app"`), `raw_events` y `verifications`. Métricas: `GET /stats?token=<verify_token>`; reporte de la ventana: `summary.sql`.
- La app "Universe Publicaciones" quedó **suscrita al WABA** ✅ (`POST /{WABA_ID}/subscribed_apps` → `success: true`).
- 🧰 **Respaldo local (solo depuración):** `tenants/flexi/whatsapp/webhook/server.py` (sin dependencias) escucha en `127.0.0.1:8787`. Ya **no** es la ruta de producción y no debe exponerse con túneles efímeros; el túnel de `trycloudflare` se **retiró el 2026-10-16** (junto con sus restos en `/tmp`).
- ⏳ Endurecimiento pendiente: validar la firma `X-Hub-Signature-256` (requiere `META_APP_SECRET`) y aceptar `HEAD`/`OPTIONS` por si el validador de Meta los usa.

## 3. Hallazgos

1. El token de `.env` **ya incluye** `whatsapp_business_messaging` y `whatsapp_business_management` ✅ (también `pages_messaging` → Messenger/IG cubiertos por el mismo token).
2. El WABA vive en el **portafolio personal** ("Fernando Galindo de los Reyes"), no en un Business llamado "Flexi". Por eso `/wa/manage` a secas fallaba.
3. ℹ️ **Nombre para mostrar:** `name_status=NON_EXISTS` es el estado **esperado** en coexistencia y **no bloquea** el envío. **No** enviar `new_display_name` por API (ver §2.d).
4. ℹ️ **Código del número:** `code_verification_status=NOT_VERIFIED` — esperado en coexistencia; sin acción por ahora.
5. ✅ **Plantillas (resuelto 2026-10-16):** las 6 plantillas HSM se **crearon en Meta vía API** y **Meta las aprobó todas el mismo día** (~25 min en `PENDING`). El `templates.json` decía `APPROVED` sin existir; ahora tiene el `meta_template_id`, el estado y el `approved_at` reales.
6. El token es de **usuario** (expira); se recomienda token de **System User** para producción.
7. **Reglas de validación de Meta aprendidas al someter** (documentadas para futuras plantillas):
   - El **HEADER de texto NO admite emojis, asteriscos ni saltos de línea** (`subcode 2388072`). Los emojis en el **BODY sí** están permitidos. Las 5 plantillas rechazadas al primer intento traían emoji en el título → se movieron los emojis al cuerpo.
   - Las **variables no pueden quedar al principio ni al final** de la plantilla (`subcode 2388299`); un punto final no cuenta como texto. Hay que cerrar con palabras propias (p. ej. "…vence en {{5}}, ¡no la dejes pasar!").
   - `GET /{WABA}/message_templates` puede devolver `[]` justo después de crear (consistencia eventual); conviene confirmar con `?name=<plantilla>`.
   - Los nombres de plantilla son **únicos por idioma**: recrear uno existente falla, hay que editar o eliminar.
8. ✅ **Formato de las respuestas de app (resuelto 2026-10-16):** WhatsApp **no** renderiza negritas con `**texto**` (eso es Markdown de otros clientes); usa `*texto*`. Se corrigieron las 4 respuestas afectadas (`1.txt`, `3_tallas.txt`, `4_promos.txt`, `6_ubicacion.txt`) y el consolidado `RESPUESTAS_WHATSAPP_FLEXI_COMPLETO.txt` (se conservaron las cursivas de un solo asterisco, que sí son válidas).

9. ℹ️ **Límite de mensajería corregido:** WhatsApp Manager mostraba 2,000/24 h mientras la API vieja devolvía `TIER_250`. Se verificó que `messaging_limit_tier` está **deprecado** y el campo vigente devuelve **`TIER_2K`**. Los límites son **por portafolio** y compartidos (ver §2.e).
10. ✅ **Webhook solo-escucha montado, suscrito y verificado por Meta** (2026-10-16): app suscrita al WABA + callback URL validado (challenge `346360553`). Los eventos `messages` ya se entregan (ver §2.f). Alcance y criterios en `PLAN_WHATSAPP_FLEXI.md`.

## 4. Pendientes

- [x] Localizar WABA + Phone Number ID
- [x] Cablear IDs en `whatsapp/config.json`
- [x] Crear/someter las 6 plantillas HSM a revisión de Meta (2026-10-16, todas `PENDING`)
- [x] Corregir formato `**` → `*` en las respuestas de app (2026-10-16)
- [x] Nombre para mostrar: revisado — **no aplica por API en coexistencia** (§2.d)
- [x] Confirmar la aprobación de las 6 plantillas — ✅ **APPROVED** el 2026-10-16; `templates.json` actualizado
- [x] Definir ubicación canónica (perfil de WhatsApp) y horario (app) — confirmado por el cliente 2026-10-16
- [x] Corregir el tier de mensajería (`TIER_250` → **`TIER_2K`**; el campo viejo está deprecado)
- [x] Montar el webhook **solo-escucha** y suscribir la app al WABA (2026-10-16)
- [x] Verificar el callback URL en Meta — ✅ 2026-10-16 16:20 (eventos activos) — §2.f
- [x] Host durable para la ventana de 2 semanas — Cloudflare Worker publicado y callback de Meta apuntando ahí (2026-10-16)
- [ ] Correr la observación 2 semanas y cerrar métricas (`PLAN_WHATSAPP_FLEXI.md` §6)
- [ ] Fase 1 (bot acotado) solo si se cumplen los criterios de entrada (`PLAN_WHATSAPP_FLEXI.md` §5)
- [ ] Alinear el flujo del agente con la voz Flexi (hoy usa texto genérico) — sujeto al resultado de la observación
- [ ] Validar claims comerciales (2×1, MSI, envío gratis, 15% cumpleaños) con el cliente
- [ ] Migrar a token de System User y a un portafolio propio de Flexi
- [ ] Evaluar completar `email` / `websites` del perfil de WhatsApp por API (bajo riesgo)
- [ ] Alinear la dirección del Page/GBP con la ubicación canónica (hoy `meta.address` dice solo "Piedras Negras, Coahuila, México")

## 5. Configuración aplicada

- `tenants/flexi/whatsapp/config.json`: IDs reales + bloque `api_status` (antes `PENDING_VERIFICATION`).
- `tenants/flexi/.env.example`: bloque `WHATSAPP_*` + corrección de valores stale (page id, ubicación, web, correo).
- `tenants/flexi/templates/templates.json`: estado real de las 6 (el `APPROVED` original era falso) con `meta_template_id` y `approved_at` reales; encabezados sin emoji y cuerpos ajustados a lo aceptado por el validador de Meta.
- `tenants/flexi/whatsapp/responses/*.txt` + `RESPUESTAS_WHATSAPP_FLEXI_COMPLETO.txt`: `**` → `*`.
- `tenants/flexi/config.json`: `location` = dirección canónica del perfil de WhatsApp (+ `location_source`).
- `tenants/flexi/whatsapp/config.json`: bloque `webhook_*` (modo `listen_only`, referencia al verify token, ruta de logs).
- `tenants/flexi/whatsapp/webhook/server.py`: receptor nuevo, sin dependencias.
- `tenants/flexi/.env`: `WHATSAPP_VERIFY_TOKEN` (**no versionado**; antes vivía un valor falso en `config.json`).
- `.env` real: el token lo administra el cliente (con permisos de WhatsApp ya incluidos).
