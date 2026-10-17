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
  (coexistencia → `smb_message_echoes`). Sirve para medir tiempos de respuesta humana y copiar su tono.
- **Estados** (`direction = "status"`): `sent` / `delivered` / `read`.
- **Privacidad:** el teléfono se guarda como hash SHA-256 truncado + últimos 4 dígitos.

## Endpoints

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/health` | Liveness. Devuelve `listen_only: true`. |
| GET | `/webhook` | Handshake de Meta (`hub.mode`, `hub.verify_token`, `hub.challenge`). |
| POST | `/webhook` | Guarda el evento. Siempre responde 200 (si no, Meta reintenta y duplica). |
| GET | `/stats?token=<verify_token>` | Conteos agregados para el reporte. |

## Despliegue

1. Pega las credenciales en `tenants/flexi/.env` (ignorado por git):

   ```
   CLOUDFLARE_ACCOUNT_ID=...
   CLOUDFLARE_API_TOKEN=...
   ```

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

   El script verifica credenciales, crea la base D1, aplica `schema.sql`, sube el
   `WHATSAPP_VERIFY_TOKEN` como **secreto** (nunca al repo) y despliega.
   La URL queda como `https://flexi-whatsapp-webhook.<subdominio>.workers.dev`.

3. En Meta: *App Dashboard → WhatsApp → Configuration → Webhook* →
   URL `https://…workers.dev/webhook`, el mismo verify token, y suscribe el campo `messages`.

## Pruebas

```bash
cd tenants/flexi/whatsapp/webhook-worker
npm test     # 36 comprobaciones: handshake, hashes, clasificación, casos borde
```

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
| `deploy.sh` | Despliegue idempotente. |
| `test/smoke.mjs` | Pruebas locales con D1 simulado. |
