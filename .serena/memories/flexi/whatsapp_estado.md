# Flexi — WhatsApp Cloud API: estado operativo (actualizado 2026-10-16)

## Identificadores (no secretos)
- WABA `1087457280345914` "Flexi Piedras Negras"; business `1940942776222567`
- Phone Number ID `1327098437161178` · `+52 1 878 138 5284` · `CLOUD_API` · `CONNECTED` · cuenta `APPROVED`
- App Meta: "Universe Publicaciones" `26134666266196379` (suscrita al WABA)
- **Coexistencia activa** (`is_on_biz_app: true`): la app del teléfono de la sucursal se conserva.
  **Nunca** usar el flujo "registrar número". `name_status=NON_EXISTS` y `code_verification_status=NOT_VERIFIED`
  son esperados y NO bloquean.
- Límite: `whatsapp_business_manager_messaging_limit` = `TIER_2K` (2,000/24 h). El campo `messaging_limit_tier`
  (`TIER_250`) está **deprecado**. El límite es **por portafolio y compartido**; hoy vive en el portafolio
  personal de Fernando → recomendado portafolio propio de Flexi + System User.

## Datos canónicos
- Dirección = la del perfil de WhatsApp: Calle Av. Industrial 203, Parque Industrial Piedras Negras, 26070, Coah.
- Horario: Lun–Vie 9–20, Sáb 10–19, Dom 11–17.
- Distribuidores oficiales de la marca; sucursal Piedras Negras.
- El inventario NO es el catálogo completo → prohibido prometer disponibilidad en WhatsApp.

## Plantillas HSM (6 APROBADAS por Meta el 2026-10-16)
`bienvenida` 1419854380122296 · `confirmacion_pedido` 2299930924141391 ·
`satisfaccion_postcompra` 1114575207649407 (UTILITY) · `recordatorio_carrito` 1143314561789158 ·
`oferta_especial` 28964419769858511 · `reenganche` 2168676927394126 (MARKETING).
Las 3 MARKETING requieren opt-in. Reglas del validador: HEADER de texto sin emojis/asteriscos/saltos
(`2388072`); variables no al inicio ni al final (`2388299`); `GET message_templates` puede devolver `[]` recién creadas.

## Receptor de producción: Cloudflare Worker + D1 (DESPLEGADO)
- URL: `https://flexi-whatsapp-webhook.io-marketing-09.workers.dev/webhook`
- Código: `tenants/flexi/whatsapp/webhook-worker/` (sin dependencias). Pruebas `npm test` → 36/36 OK.
- D1 `flexi_whatsapp_obs` id `0128328b-7c24-4c40-b4f8-c2720c080d5f`; tablas `events`, `raw_events`,
  `verifications` + 5 índices (dedupe por `message_id`).
- Endpoints: `GET /health`, `GET /webhook` (handshake), `POST /webhook`, `GET /stats?token=<verify_token>`.
- **Garantía:** el Worker no hace ninguna llamada saliente a Meta → no puede responder ni enviar.
  Teléfonos hasheados (SHA-256 truncado + últimos 4).
- Secretos y credenciales en `tenants/flexi/.env` (no versionado): `CLOUDFLARE_ACCOUNT_ID`
  (cuenta `f3bf2309372ceb3d0fa04838d9c1ebef`, subdominio workers `io-marketing-09`), `CLOUDFLARE_API_TOKEN`,
  `WHATSAPP_VERIFY_TOKEN`.
- Gotchas de wrangler: forzar `XDG_CONFIG_HOME=/tmp/wrangler-config` y `WRANGLER_LOG_PATH=/tmp/wrangler-logs/wrangler.log`;
  el secreto se sube DESPUÉS del deploy; el token necesita `Account · Workers Scripts · Edit`.
- Respaldo local: `tenants/flexi/whatsapp/webhook/server.py` (sus procesos y el túnel mueren al cerrar la sesión).

## Fase aprobada: 0.5 "observación silenciosa" (2 semanas)
- Doc: `tenants/flexi/docs/PLAN_WHATSAPP_FLEXI.md`. Regla dura: mientras la app tenga bienvenida/ausencia/flash
  activos, **no se prende bot** (evita doble respuesta).
- Fase 1 (bot acotado a ubicación/horario/asesor) solo si se cumplen los criterios de entrada del §5.
- Métricas: volumen/día, mezcla de intenciones (ubicación+horario ≥50%), % resuelto sin humano ≥70%,
  primera respuesta <15 min, **0** quejas por inventario/precio.

## Pendientes
1. ~~Cambiar el callback URL en Meta~~ **HECHO el 2026-10-16**: el callback apunta al Worker y `/stats` reporta `verificaciones_ok: 1`. **La Fase 0.5 está EN VIVO** (0 mensajes aún, normal antes de tráfico real).
2. Verificar con `GET /stats?token=…` que lleguen eventos reales; `wrangler tail` la primera hora.
3. Endurecer: `META_APP_SECRET` + validación `X-Hub-Signature-256`.
4. Migrar a System User + portafolio propio de Flexi.
5. Validar claims comerciales con el cliente (2×1, MSI, envío gratis >$1200, 15% cumpleaños).
6. Alinear `meta.address` del Page/GBP con la dirección canónica.
7. Reporte de 2 semanas con `summary.sql`.

## Referencias
- `tenants/flexi/docs/PLAN_WHATSAPP_FLEXI.md`, `WHATSAPP_SETUP_FLEXI.md`, `BITACORA_WHATSAPP_FLEXI.md`
- `GrowthOS/00_01_Changelog_GrowthOS.md` (entrada 6.09.00)
- Patrón Graph: `META_ACCESS_TOKEN` de `growth-os/.env`, base `https://graph.facebook.com/v20.0/...`
