# Bitácora — WhatsApp Cloud API Flexi (tenant `flexi`)

**Propósito:** registro vivo del proyecto WhatsApp para no perder contexto entre sesiones (ha habido caídas de sesión).
**Estado del setup:** `tenants/flexi/docs/WHATSAPP_SETUP_FLEXI.md` (doc de referencia).
**Changelog central:** `GrowthOS/00_01_Changelog_GrowthOS.md`.

---

## Sesión 2026-10-16

### Credenciales / conexión
- El cliente conectó WhatsApp Business a Meta Business y renovó `META_ACCESS_TOKEN` **con permisos de WhatsApp**.
- WABA `1087457280345914` ("Flexi Piedras Negras") · número `1327098437161178` (`+52 1 878 138 5284`) · `CLOUD_API` · `CONNECTED` · cuenta `APPROVED`.
- **Coexistencia confirmada** (`is_on_biz_app: true`): la sucursal conserva la app de WhatsApp Business en el teléfono. ⇒ **Nunca usar el flujo estándar de "registrar número".**
- Ubicación: **Piedras Negras, Coahuila**. Son **distribuidores oficiales de la marca**.

### Plantillas HSM — 6 creadas y APROBADAS por Meta ✅
| Plantilla | ID Meta | Categoría |
|---|---|---|
| `bienvenida` | `1419854380122296` | UTILITY |
| `confirmacion_pedido` | `2299930924141391` | UTILITY |
| `recordatorio_carrito` | `1143314561789158` | MARKETING |
| `oferta_especial` | `28964419769858511` | MARKETING |
| `satisfaccion_postcompra` | `1114575207649407` | UTILITY |
| `reenganche` | `2168676927394126` | MARKETING |

**Meta aprobó las 6 el 2026-10-16** (~25 minutos en `PENDING`, sin rechazos ni reenvíos). Ya se puede enviar con ellas; las 3 MARKETING necesitan opt-in del cliente.

**Rechazos aprendidos (importante para futuras plantillas):**
1. `subcode 2388072` — el **HEADER de texto no admite emojis** (ni asteriscos ni saltos de línea). Los 5 primeros envíos fallaron por eso; los emojis se movieron al **body** (ahí sí se permiten) y pasaron.
2. `subcode 2388299` — las **variables no pueden quedar al inicio ni al final** de la plantilla; un punto final no cuenta como texto, hay que cerrar con palabras ("…vence en {{5}}, ¡no la dejes pasar!").
3. `GET /{WABA}/message_templates` devuelve `[]` recién creadas (consistencia eventual) → verificar con `?name=<plantilla>`.
4. Nombres únicos por idioma: recrear falla; hay que editar/eliminar.

**Repo actualizado:** `tenants/flexi/templates/templates.json` (estado real + `meta_template_id`; antes decía `APPROVED` sin existir).

### Nombre para mostrar y formato de respuestas (misma sesión)

**Nombre para mostrar — NO se envía por API.**
- `verified_name` ya es "Flexi Piedras Negras"; `name_status=NON_EXISTS` y `new_name_status=NONE`.
- En coexistencia eso es **normal y no bloquea** el envío: Meta no da badge de cuenta oficial (OBA) ni verificación de negocio estándar a estos números.
- La revisión del nombre va atada al **registro** del número y, si se aprueba un cambio, exige **re-registrar en 14 días** ⇒ usar `POST /{id}?new_display_name=` apuntaría al flujo que **rompe la coexistencia**. Si se quiere cambiar, se hace desde la **app** o **WhatsApp Manager → Perfil**.
- **Perfil de negocio verificado (activo):** dirección "Calle Av. Industrial 203, Parque Industrial Piedras Negras, 26070", descripción "Distribuidor oficial Flexi 👢✨…", vertical `RETAIL`, foto definida; `about`, `email` y `websites` vacíos.

**Formato de respuestas de app — corregido.**
- WhatsApp **no** renderiza `**negrita**` (lo muestra literal); la negrita correcta es `*texto*`.
- Corregidas 13 líneas en `responses/1.txt`, `3_tallas.txt`, `4_promos.txt`, `6_ubicacion.txt` y 12 en `RESPUESTAS_WHATSAPP_FLEXI_COMPLETO.txt`. Las cursivas de un asterisco (ej. `*realmente*` en `0.txt`) se conservaron porque sí son válidas.

### Webhook solo-escucha, tier y datos canónicos (misma sesión)

- **Tier corregido:** el Administrador tenía razón → `whatsapp_business_manager_messaging_limit` = **`TIER_2K`** (2,000/24 h). El campo `messaging_limit_tier` (=`TIER_250`) está **deprecado** por Meta. Ojo: el límite es **por portafolio y compartido**; hoy vive en el portafolio personal de Fernando.
- **Ubicación canónica:** la del perfil de WhatsApp (Av. Industrial 203, Parque Industrial, 26070 Piedras Negras) → ya en `tenants/flexi/config.json` (`location` + `location_source`). Horario confirmado: Lun–Vie 9–20, Sáb 10–19, Dom 11–17 (ya coincidía con el repo).
- **Webhook solo-escucha montado:** `tenants/flexi/whatsapp/webhook/server.py` (solo librería estándar).
  - `GET /webhook` verifica con `WHATSAPP_VERIFY_TOKEN` (nuevo, en `tenants/flexi/.env`, no versionado); `POST /webhook` guarda payload + fila clasificada; `GET /health` liveness.
  - **No envía nada**: no existe ninguna llamada de escritura a Meta. Teléfonos hasheados. Logs en `whatsapp/webhook/logs/*.jsonl` (git-ignored).
  - Probado local y por URL pública: challenge ✅, POST simulado ✅ (clasificó `horario` y registró el eco de la app como `out_app`).
  - App "Universe Publicaciones" **suscrita al WABA** ✅.
  - ✅ **Callback URL verificado por Meta** (16:20, challenge `346360553`, HTTP 200) + campo `messages` suscrito → los eventos ya se entregan.
  - ⏳ Endurecer: validar `X-Hub-Signature-256` (requiere `META_APP_SECRET`) y aceptar `HEAD`/`OPTIONS`.
  - ✅ Resuelto: el receptor de producción es un **Cloudflare Worker con URL fija** (ver sección siguiente). El túnel `trycloudflare` del respaldo local es **efímero** y sus procesos **mueren al cerrar la sesión del agente**, por eso `webhook/server.py` quedó solo como respaldo.

### Migración a Cloudflare Worker — COMPLETADA ✅ (2026-10-16)

Se descartó Azure (los $200 de crédito caducan a los 30 días y el VM B1s gratuito no está disponible en su región).
Se eligió **Cloudflare Worker + D1**: costo $0 permanente, URL fija y sin servidor que mantener.

| Paso | Estado |
|---|---|
| Worker escrito y probado (`webhook-worker/`, 36/36 pruebas) | ✅ |
| Base D1 `flexi_whatsapp_obs` (`0128328b-7c24-4c40-b4f8-c2720c080d5f`) | ✅ |
| Esquema aplicado (`events`, `raw_events`, `verifications` + 5 índices, con dedupe por `message_id`) | ✅ |
| Publicar el Worker | ✅ `https://flexi-whatsapp-webhook.io-marketing-09.workers.dev` |
| Subir el verify token como secreto del Worker | ✅ |
| Cambiar el callback URL en Meta | ✅ 2026-10-16 |

El permiso que faltaba quedó corregido: el token de Cloudflare ya tiene `Account · Workers Scripts · Edit`
(antes la subida fallaba con *No access to the specified resource*).

Credenciales (no versionadas, en `tenants/flexi/.env`): `CLOUDFLARE_ACCOUNT_ID`
(cuenta `f3bf2309…`, subdominio de workers `io-marketing-09`), `CLOUDFLARE_API_TOKEN` y `WHATSAPP_VERIFY_TOKEN`.

**Garantía intacta:** el Worker **no hace ninguna llamada saliente a Meta** → no puede responder ni enviar;
teléfonos hasheados (SHA-256 truncado + últimos 4 dígitos) y clasificación por intención con pesos.
Endpoints: `GET /health`, `GET /webhook` (handshake), `POST /webhook`, `GET /stats?token=…`.

Verificación en vivo (2026-10-16, tras cambiar el callback en Meta): `/health` → `{"status":"ok","runtime":"cloudflare-worker","storage":"d1","listen_only":true}`;
`/stats` → `verificaciones_ok: 1` (Meta completó el handshake contra el Worker) y **0 mensajes todavía**, que es lo
normal antes de que entre tráfico real. **La Fase 0.5 quedó en vivo: ya no falta ningún paso de infraestructura.**

Notas del entorno (ya resueltas en `deploy.sh`): `wrangler` corre en el sandbox vía `npx` con
`XDG_CONFIG_HOME=/tmp/wrangler-config` y `WRANGLER_LOG_PATH=/tmp/wrangler-logs/wrangler.log`
(el `XDG_CONFIG_HOME` heredado apunta a `~/.config`, que no es escribible en este entorno). El **secreto se
sube después** del `deploy`, porque Cloudflare no permite secretos de un script que aún no existe.

### Limpieza de restos del receptor local y del túnel (2026-10-16)

Con el Worker en producción quedaron obsoletos los artefactos del respaldo local y del túnel efímero.
**Ojo: nada de `tenants/flexi/` está versionado en git (0 archivos rastreados)**, así que las bajas son
**irreversibles**; por eso se eliminó solo basura verificada.

| Eliminado | Por qué | Nota |
|---|---|---|
| `docs/.~lock.WHATSAPP_SETUP_FLEXI.md#` | lock de LibreOffice de una edición del 15:13 | basura |
| `whatsapp/webhook/__pycache__/` | caché de Python | regenerable |
| `whatsapp/webhook/logs/*.jsonl` (20 líneas) | datos **de prueba** del receptor local (timestamps simulados) | el registro real vive en D1 |
| `/tmp/cloudflared` (39 MB) + `cloudflared.log/.pid`, `cf.log`, `webhook.log` | túnel `trycloudflare` retirado | libera ~39 MB |
| `/tmp/az_*.html`, `gcp_*.html`, `cf_*.html`, `dn/ml/pn.html`, `prices.json` | scraping de la decisión Azure/GCP/Cloudflare (ya cerrada) | informes descartados |
| `/tmp/create_tpl*.py`, `verify_tpl.py`, `wa_*.py`, `tpl_results*.json`, `templates.backup.json` | scripts de un solo uso de las plantillas HSM | ya cumplieron su función |
| `/tmp/co01_fase_*.py`, `fase_b.patch`, `co01_fase_b_output.txt`, `coex.md`, `catalogo_flexi_confirmado.csv`, `deploy*.log` | materiales temporales de sesiones anteriores | la copia vigente está en el repo |

**Se conserva a propósito:** `whatsapp/webhook/server.py` (12 KB, respaldo para depurar sin dependencias),
`/tmp/wrangler-config` y `/tmp/wrangler-logs` (los usa `deploy.sh`), y el resto de `/tmp` que es de sistema o de otros trabajos.
**Pendiente de decisión del cliente:** retirar por completo `webhook/server.py` (ya no aporta), revisar
`docs/Catálogo disponibles/` (copia con nombres del cliente) y `docs/Flexi monetizacion1/` (material de marzo),
borrar `data/visual_assets_cache.backup_20261016.json` y, sobre todo, **versionar `tenants/flexi/`** para que
las bajas dejen de ser irreversibles.

### Pendientes de WhatsApp
- [x] Corregir formato `**` → `*` en respuestas de app (2026-10-16)
- [x] Nombre para mostrar: revisado — no aplica por API en coexistencia (ver arriba)
- [x] Confirmar aprobación de Meta y actualizar `status`/`approved_at` — ✅ las 6 `APPROVED` el 2026-10-16.
- [ ] Alinear el flujo del agente con la voz Flexi (hoy usa texto genérico).
- [x] Montar webhook solo-escucha + suscribir la app al WABA (2026-10-16).
- [x] Verificar el callback URL en Meta — ✅ 2026-10-16 16:20 (eventos activos).
- [x] Host durable para la observación de 2 semanas — Cloudflare Worker publicado (2026-10-16).
- [x] **Cambiar el callback URL en Meta al Worker** — ✅ 2026-10-16 (`verificaciones_ok: 1`); la observación arrancó.
- [ ] Revisar `/stats?token=…` 24 h después del cambio de callback (y `wrangler tail` la primera hora).
- [ ] Validar claims comerciales con el cliente (2×1, MSI, envío gratis >$1200, 15% cumpleaños).
- [ ] Recomendar/migrar a token de **System User** (el actual es de usuario y expira).

### Notas técnicas
- `agents/whatsapp_agent/skills/template_manager.py` mantiene un fallback `_create_default_templates()` con encabezados con emoji y `status="APPROVED"`; solo aplica si falta `templates.json`, pero queda como deuda (no se tocó).
- `agents/whatsapp_agent/agent.py` (`ConversationContext`) tiene campos duplicados `current_flow/current_step`.
