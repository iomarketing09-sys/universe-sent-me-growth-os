# Receptor solo-escucha del webhook de WhatsApp — `flexi`

Fase 0.5 del `../../docs/PLAN_WHATSAPP_FLEXI.md`: **observar 2 semanas sin responder nada**.
Este Worker verifica el handshake de Meta y guarda los eventos en D1. No responde, no envía, no
marca como leído: **no existe ninguna llamada saliente a la API de Meta** en el código.

## Por qué un Worker y no un VM

| | Cloudflare Worker + D1 |
|---|---|
| Costo | $0 permanente (100k peticiones/día, 5M filas leídas/día, 5 GB) |
| URL | Fija, HTTPS, sin reconfigurar Meta |
| Operación | Ninguna: no hay SO que parchar ni proceso que revivir |
| Escala | Duerme solo cuando no hay tráfico |

## Arquitectura

```
WhatsApp (Meta)  ──HTTPS──▶  Worker: /webhook  ──▶  D1 `flexi_whatsapp_obs`
                                                  ├─ events        (una fila por mensaje/eco/status)
                                                  ├─ raw_events    (payload completo, depuración)
                                                  └─ verifications (intentos de handshake de Meta)
```

- **Entrantes** (`direction = "in"`): mensaje del cliente, con `intent` clasificado.
- **Ecos** (`direction = "out_app"`): lo que la sucursal contesta **desde la app del teléfono**
  (coexistencia). Meta los manda en `value.message_echoes` (mensaje plano); la doc oficial habla de
  `smb_message_echoes`. El worker acepta **ambos formatos** desde 2026-10-27. Sirve para medir
  tiempos de respuesta humana y copiar su tono.
- **Estados** (`direction = "status"`): `sent` / `delivered` / `read`.
- **Privacidad:** el teléfono se guarda como hash SHA-256 truncado + últimos 4 dígitos.
- **Autenticidad:** todo `POST /webhook` debe traer `X-Hub-Signature-256` válido, calculado por
  Meta con `META_APP_SECRET` sobre el cuerpo crudo. Sin firma válida no se parsea ni se escribe en D1.

## Endpoints

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/health` | Salud real: consulta D1 y comprueba que los secretos estén configurados. Devuelve `200` si todo está bien; `503` si está degradado. |
| GET | `/webhook` | Handshake de Meta (`hub.mode`, `hub.verify_token`, `hub.challenge`). |
| POST | `/webhook` | Valida `X-Hub-Signature-256` y guarda el evento. Firma ausente/incorrecta: `401`; secreto no configurado: `503`; escritura confirmada: `200`; fallo de D1: `500` para que Meta reintente. |
| GET | `/stats?token=<verify_token>` | Conteos agregados para el reporte. |

## Salud para el monitor externo

`/health` es el único endpoint público de lectura que debe usar el monitor
externo. No devuelve teléfonos, textos ni tokens; solo estado, checks y el
último `received_at` registrado en D1.

El monitor externo se configura desde `ops/external_monitors.yaml` y alerta al
grupo `Growth OS Ops`. No reemplaza al watchdog interno: el monitor mide
disponibilidad y el watchdog mide workflows.

## Despliegue

1. `META_APP_SECRET` es un secreto **de la app completa**, no del tenant. Colócalo en
   `growth-os/.env` (ignorado por git), junto a las demás credenciales de administración.
   Las credenciales de despliegue pueden vivir en `tenants/flexi/.env`; si faltan ahí,
   `deploy.sh` las busca en `growth-os/.env` (`CF_API_TOKEN` también sirve) y toma el
   `account_id` de `../config.json`:

   ```
   # growth-os/.env (recomendado para el App Secret)
   META_APP_SECRET=...

   # tenants/flexi/.env
   CLOUDFLARE_ACCOUNT_ID=...
   CLOUDFLARE_API_TOKEN=...
   WHATSAPP_VERIFY_TOKEN=...   # opcional: si falta, se conserva el secreto actual
   ```

   El App Secret se obtiene en **App Dashboard → Settings → Basic → App Secret**. No debe
   duplicarse en cada tenant: el despliegue lo busca primero en `growth-os/.env`.

   El token se crea en <https://dash.cloudflare.com/profile/api-tokens> → *Create Token* →
   plantilla **Edit Cloudflare Workers** (que ya incluye `Workers Scripts: Edit`), y añade
   `Account → D1 → Edit`. El Account ID está en la barra lateral de **Workers & Pages**.

   **Permisos mínimos necesarios:**

   | Permiso | Para qué |
   |---|---|
   | `Account · Workers Scripts · Edit` | Publicar el Worker y **gestionar sus secretos** |
   | `Account · D1 · Edit` | Crear la base y aplicar el esquema |
   | `Account · Account Settings · Read` | Que wrangler resuelva la cuenta |

   ⚠️ Sin `Workers Scripts: Edit` el despliegue falla con
   *"A request to the Cloudflare API (`/workers/scripts/.../secrets`) failed. No access to the
   specified resource."* — porque wrangler primero lista los secretos del script antes de subirlo.
   Síntoma típico de un token creado a mano solo con lectura.

2. Despliega:

   ```bash
   cd tenants/flexi/whatsapp/webhook-worker
   bash deploy.sh
   ```

   El script verifica credenciales, crea la base D1, aplica `schema.sql`, despliega y sube
   `WHATSAPP_VERIFY_TOKEN` y `META_APP_SECRET` como **secretos** (nunca al repo). Si falta
   `META_APP_SECRET`, aborta antes de desplegar para no dejar el webhook fail-closed.
   Los secretos existentes sobreviven al despliegue: si no hay verify token en el entorno,
   el paso 5 se omite en lugar de fallar. Meta reintenta los eventos que reciban `503`
   durante la ventana breve entre el despliegue y la carga del App Secret.
   La URL queda como `https://flexi-whatsapp-webhook.<subdominio>.workers.dev`.

3. En Meta: *App Dashboard → WhatsApp → Configuration → Webhook* →
   URL `https://…workers.dev/webhook`, el mismo verify token, y suscribe el campo `messages`.

## Pruebas

```bash
cd tenants/flexi/whatsapp/webhook-worker
npm test     # 47 comprobaciones: handshake, firma HMAC, hashes, clasificación y ecos
```

## Seguridad del webhook

- `META_APP_SECRET` se configura como secreto del Worker; nunca se escribe en `wrangler.toml` ni en el repo.
- El Worker calcula HMAC-SHA256 sobre los bytes crudos y usa `crypto.subtle.verify` para comparar la firma.
- Sin `META_APP_SECRET`, el endpoint responde `503` y no escribe en D1.
- Con firma ausente, malformada o incorrecta, responde `401` y no escribe en D1.
- Un cuerpo alterado después de firmar también se rechaza.

Con la URL desplegada:

```bash
curl "https://…workers.dev/health"
curl "https://…workers.dev/webhook?hub.mode=subscribe&hub.verify_token=$TOKEN&hub.challenge=123"
curl "https://…workers.dev/stats?token=$TOKEN"
```

## Reporte de las 2 semanas

```bash
npx wrangler d1 execute flexi_whatsapp_obs --remote --file summary.sql
```

## Archivos

| Archivo | Rol |
|---|---|
| `src/index.js` | Worker completo (sin dependencias). |
| `schema.sql` | Tablas + índices (incluye dedupe por `message_id`). |
| `summary.sql` | Consultas del reporte. |
| `deploy.sh` | Despliegue idempotente (credenciales del tenant o de la raíz). |
| `migrations/001_referral_columns.sql` | Columnas de atribución de anuncios, ya aplicadas. |
| `test/smoke.mjs` | Pruebas locales con D1 simulado. |
