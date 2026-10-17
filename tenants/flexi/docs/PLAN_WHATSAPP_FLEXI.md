# Plan WhatsApp Flexi — observación y alcance por fases

**Tenant:** `flexi` (physical_cro) · **Aprobado:** 2026-10-16 · **Autor:** Codex/CGO
**Estado:** Fase 0.5 **en vivo** desde 2026-10-16 (receptor de producción recibiendo eventos; sin bot)

---

## 1. Criterio rector

La sucursal evaluará **la voz** antes de darnos responsabilidades mayores. Por eso:

1. **Una sola voz por evento.** La app de la sucursal ya tiene bienvenida, ausencia y mensajes flash
   (ubicación/horarios). Mientras esos automatismos estén activos, **no se prende ningún bot de API**:
   el cliente recibiría dos respuestas.
2. **Nada de inventario ni de precio.** El inventario confirmado (54 modelos / 75 variantes,
   `data/catalogo_flexi_confirmado.csv`) **no representa todo lo que hay en sucursal**; prometer
   disponibilidad, talla o precio por chat genera expectativas que la tienda tendría que cumplir.
3. **La voz es de la sucursal.** Durante la observación ellos pueden cambiar o agregar respuestas
   en la app; nosotros solo **medimos**.

## 2. Datos canónicos confirmados (2026-10-16)

| Dato | Valor canónico | Fuente |
|---|---|---|
| Ubicación | Calle Av. Industrial 203, Parque Industrial Piedras Negras, 26070 Piedras Negras, Coah., México | Perfil de WhatsApp (confirmado por el cliente) |
| Horario | Lun–Vie 9:00–20:00 · Sáb 10:00–19:00 · Dom 11:00–17:00 | App de la sucursal (confirmado por el cliente) |
| Límite de mensajería | `TIER_2K` = 2,000 conversaciones iniciadas por la empresa / 24 h | WhatsApp Manager (el campo viejo `messaging_limit_tier` está deprecado) |
| Número | `+52 1 878 138 5284` · Phone Number ID `1327098437161178` | Graph API |
| Coexistencia | `is_on_biz_app: true` — la app del teléfono se conserva | Graph API |

## 3. Fase 0.5 — Observación silenciosa (2 semanas)

**Objetivo:** decidir la Fase 1 con datos, no con supuestos.

- **Receptor solo-escucha (producción):** Cloudflare Worker + D1, código en `tenants/flexi/whatsapp/webhook-worker/`
  (`https://flexi-whatsapp-webhook.io-marketing-09.workers.dev/webhook`).
  - `GET /webhook` → verificación de Meta con `WHATSAPP_VERIFY_TOKEN` (secreto del Worker).
  - `POST /webhook` → guarda el payload en D1, clasifica la intención y registra el mensaje.
  - `GET /health` → liveness · `GET /stats?token=…` → métricas de la ventana.
- **Garantía dura:** el código **no contiene ninguna llamada de escritura a Meta**. Es imposible que
  envíe un mensaje al cliente.
- **Privacidad:** los teléfonos se guardan **hasheados** (`contact_hash` + últimos 4 dígitos), no en claro.
  Los datos viven en D1 (tablas `events`, `raw_events`, `verifications`), no en archivos locales.
- **Clasificación (heurística por palabras clave):** `ubicacion`, `horario`, `talla`, `precio`,
  `disponibilidad`, `promocion`, `pedido`, `saludo`, `otro`. Solo para el reporte; nunca para responder.
- **Modo app:** los mensajes que la sucursal manda desde la app (coexistencia) llegan como
  `smb_message_echoes` y se registran con `direction="out_app"` → sirven para copiar su tono real.

### Cómo se opera

```bash
cd /home/universe-sent-me/growth-os

# salud y métricas del receptor de producción
curl -s https://flexi-whatsapp-webhook.io-marketing-09.workers.dev/health
curl -s "https://flexi-whatsapp-webhook.io-marketing-09.workers.dev/stats?token=$WHATSAPP_VERIFY_TOKEN"

# eventos en vivo durante la primera hora de la ventana
npx wrangler tail flexi-whatsapp-webhook

# reporte de la ventana
npx wrangler d1 execute flexi_whatsapp_obs --remote --file tenants/flexi/whatsapp/webhook-worker/summary.sql
```

El verify token vive en `tenants/flexi/.env` (`WHATSAPP_VERIFY_TOKEN`), nunca en un archivo versionado;
el mismo archivo guarda `CLOUDFLARE_ACCOUNT_ID` y `CLOUDFLARE_API_TOKEN` para desplegar
(`bash tenants/flexi/whatsapp/webhook-worker/deploy.sh`).

**Respaldo local (solo depuración):** `python3 tenants/flexi/whatsapp/webhook/server.py --port 8787`.
El túnel efímero de `trycloudflare` se **retiró el 2026-10-16**: sus procesos morían al cerrar la sesión y la
URL cambiaba en cada arranque, así que no sirve para una ventana de 2 semanas.

## 4. Qué falta para que Meta entregue eventos

1. ✅ App suscrita al WABA (`POST /{WABA_ID}/subscribed_apps` → `success: true`).
2. ✅ **Callback URL verificado por Meta** (2026-10-16 16:20, challenge `346360553`, HTTP 200, todavía contra el
   receptor local) y campo `messages` suscrito desde *App Dashboard → WhatsApp → Configuration → Webhook*.
   Esa URL quedó **reemplazada por la del Worker** (ver paso 4 y §4.bis), que es la que hoy recibe los eventos.
   Como referencia, la vía API (`POST /{APP_ID}/subscriptions`) exige **app access token**
   (`{app_id}|{app_secret}`). Opciones contempladas:
   - **A (recomendada):** pegar la URL y el verify token en *App Dashboard → WhatsApp → Configuration →
     Webhook*, y suscribir el campo `messages`. Cero secretos compartidos por chat.
   - **B:** agregar `META_APP_SECRET` a `.env` y lo configuro por API; además habilitaría la
     validación de firma `X-Hub-Signature-256` de los webhooks entrantes (endurecimiento pendiente).
3. ✅ **Durabilidad resuelta (2026-10-16):** el receptor de producción es un **Cloudflare Worker + D1**
   (`tenants/flexi/whatsapp/webhook-worker/`), con URL estable
   `https://flexi-whatsapp-webhook.io-marketing-09.workers.dev/webhook`. No depende de esta sesión ni de
   ningún servidor que revivir. Se descartó Azure (crédito de $200 a 30 días y VM B1s fuera de su región)
   y se conserva `webhook/server.py` en local **solo como respaldo** para depurar.
4. ✅ **Callback de Meta apuntando al Worker** (2026-10-16): `/stats` → `verificaciones_ok: 1`. La Fase 0.5 está
   **en vivo**; no queda ningún paso de infraestructura pendiente (ver §4.bis).

## 4.bis Receptor de producción (Cloudflare Worker + D1)

| Dato | Valor |
|---|---|
| URL del webhook | `https://flexi-whatsapp-webhook.io-marketing-09.workers.dev/webhook` |
| Verify token | `WHATSAPP_VERIFY_TOKEN` en `tenants/flexi/.env` y como **secreto** del Worker |
| Base de datos | D1 `flexi_whatsapp_obs` (`0128328b-7c24-4c40-b4f8-c2720c080d5f`) |
| Tablas | `events` (mensajes/ecos/estados), `raw_events`, `verifications` |
| Métricas | `GET /stats?token=<verify_token>` |
| Reporte | `npx wrangler d1 execute flexi_whatsapp_obs --remote --file summary.sql` |
| Despliegue | `bash deploy.sh` (idempotente) |
| Pruebas | `npm test` → 36/36 |

Garantía: el Worker **no hace ninguna llamada saliente a Meta**; no puede responder ni enviar.
Los teléfonos se guardan hasheados (SHA-256 truncado + últimos 4 dígitos).

## 5. Criterios de entrada a la Fase 1 (bot acotado)

Se habilita **solo si** al cerrar las 2 semanas:

- El cliente aprueba la voz mostrada por la sucursal en la app.
- Los temas `ubicacion` + `horario` representan una proporción relevante del volumen (referencia: ≥50 %).
- No hubo quejas por promesas de inventario, precio o tiempos (deben ser cero).
- Existe regla anti-duplicado acordada: al prender el bot se **apaga** en la app el automatismo que duplique.

**Alcance máximo de la Fase 1:** ubicación, horarios, link de catálogo y "un asesor te atiende".
**Nunca responde:** talla/color/stock, precio, promociones (2×1, MSI, envío gratis, cumpleaños), tiempos,
cambios y devoluciones. Todo lo demás → handoff a humano y silencio para ese contacto.

Plantillas: solo `bienvenida` activa; las otras 5 permanecen dormidas hasta que exista caso de uso
(las MARKETING además requieren opt-in).

## 6. Métricas de las 2 semanas

| Métrica | Cómo se mide | Meta |
|---|---|---|
| Volumen por día y por hora | D1 `events` (`/stats` o `summary.sql`) | línea base |
| Mezcla de temas | campo `intent` en `events` | ubicación+horario ≥50 % |
| % resuelto sin humano | seguimiento de conversaciones | ≥70 % |
| Tiempo a primera respuesta humana | comparar `in` con el siguiente `out_app` | <15 min en horario |
| Quejas por inventario/precio | revisión manual | **0** |
| Uso real de la app por la sucursal | volumen `direction="out_app"` | creciente |

## 7. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Doble respuesta (app + bot) | bot apagado hasta que se apague el automatismo espejo |
| Inventario parcial tomado como catálogo completo | prohibido hablar de producto; el CSV es "inventario parcial confirmado" |
| Claims comerciales sin validar | bloqueados en plantillas y en chat hasta validación del cliente |
| Túnel efímero / proceso que muere | **Resuelto:** Cloudflare Worker + D1 con URL fija (2026-10-16) |
| Token de usuario y portafolio personal | migrar a System User + portafolio propio de Flexi (Fase 2) |
| Mensajes que nadie atiende | el handoff necesita un responsable y horario definidos por la sucursal |
