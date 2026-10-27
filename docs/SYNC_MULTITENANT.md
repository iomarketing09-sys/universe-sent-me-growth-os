# Sync Multi-tenant

## Propósito

`scripts/sync_all.py` genera un snapshot local por tenant. La versión inicial no usa tokens a menos que se active el flag `--live-meta`, que permite capturar datos orgánicos desde Meta Graph API sin publicar contenido.

## Modos de operación

| Modo | flag | solicitud externa | escríbe | datos origen |
|------|------|-------------------|--------|--------------|
| Local (default) | `--no-live-meta` | No | No | Evidencia ya guardada (`data/`) |
| Live Meta | `--live-meta` | Sí (Meta Graph API v26.0) | No | Live + Evidencia local |
| Live Google | `--live-google` | Sí (GSC + Bing Webmaster) | No | Live + Evidencia local |
| Live Ads | `--live-ads` | Sí (Meta Marketing API) | No | Live + Evidencia local |
| Live WhatsApp | `--live-whatsapp` | Sí (Worker D1) | No | Live + Evidencia local |

## Piloto: Flexi

Flexi es el tenant inicial porque ya cuenta con configuración de Meta y Google, métricas locales, una campaña documentada y un Worker de WhatsApp en modo solo-lectura.

### Modalidades

| Fuente | Local | Live | Notas |
|--------|-------|------|-------|
| Meta orgánico (`page_id`, `ig_user_id`) | Configuración, CSV de métricas | Instagram 25 recientes posts, Page info | Solo GET - no publishing |
| Google (GSC + Bing) | GSC/Bing JSON locales | Search Analytics, Sitemaps, Crawl Errors | Requiere gsc_token.json + BING_WEBMASTER_API_KEY |
| Ads | Estado de campañas (Markdown) | Marketing API insights | CRUD de campañas via Marketing API |
| WhatsApp | Worker + CRM contadores | Solo-lectura (estados) | Webhooks activos |
| Directorios | Configuración | No implementado | Fuentes explícitas en `config.json` |

## Uso

```bash
cd /home/universe-sent-me/growth-os

# Enumerar tenants
python3 scripts/sync_all.py --list

# Revisar Flexi solo-lectura (no pide tokens)
python3 scripts/sync_all.py --tenant flexi --no-write

# Live Meta para Flexi (pide META_ACCESS_TOKEN de .env)
python3 scripts/sync_all.py --tenant flexi --live-meta

# Live Google para Flexi (requiere gsc_token.json + BING_WEBMASTER_API_KEY)
python3 scripts/sync_all.py --tenant flexi --live-google

# Live Ads para Flexi (requiere ad_account_id en config.json)
python3 scripts/sync_all.py --tenant flexi --live-ads

# Live WhatsApp para Flexi (requiere worker deployado)
python3 scripts/sync_all.py --tenant flexi --live-whatsapp

# Guardar snapshot local
python3 scripts/sync_all.py --tenant flexi
```

**Ambientes compatibles:**
- `.env` (prod) → Token real de Meta
- `.env` → Local cuando `META_ACCESS_TOKEN` no está configurado
- `.env.dev` → Development (si existe)

## Estados

### Local (default)

- `local_evidence`: datos locales resumidos (CSVs, JSONs, Markdowns)
- `configured_no_local_evidence`: configuración valida, pero sin datos históricos
- `not_configured`: faltan datos mínimos de configuración

### Live Meta

- `live_success`: datos capturados en vivo (cuenta con `live_data`)
- `live_error`: error en la API (blocked con error message interno)
- `live_denied`: acceso denegado por Meta (`blocked` con motivo)

### Live Google

- `live_success`: datos capturados en vivo (cuenta con `search_console`, `bing_webmaster`, `summary`)
- `live_error`: error en la API
- `not_configured`: falta gsc_token.json o BING_WEBMASTER_API_KEY

### Live Ads

- `live_success`: account configurado + insights capturados
- `live_error`: excepción al leer API
- `live_denied`: access_token denegado por Meta
- `not_configured`: falta ad_account_id en config['ads']

### Live WhatsApp

- `live_success`: worker deployado + mensajes legibles
- `live_error`: excepción al leer del D1
- `live_denied`: worker no deployado o permisos denegados
- `live_denied_by_config`: wrangler.toml incompleto o faltan DB

### Combinados

- `status`: el estado principal tras cualquier operación
- `mode`: `"live_meta"`, `"live_google"`, `"live_ads"`, `"live_whatsapp"` si se usó flag, `"local_evidence"` por default
- `meta.live_data`: payload de respuesta de Meta (cuando aplica)

## Estructura del snapshot

```json
{
  "schema_version": "1.0",
  "tenant_id": "flexi",
  "generated_at": "2026-10-25T19:50:44Z",
  "mode": "live_meta",
  "external_requests": 2,
  "external_writes": 0,
  "sources": {
    "meta": {
      "status": "live_success",
      "mode": "live_meta",
      "page_configured": true,
      "instagram_configured": true,
      "live_data": {
        "status": "success",
        "Instagram": { ... },
        "Facebook_Page": { ... },
        "Messages_Viewer": { ... }
      }
    },
    "google": { 
      "status": "live_success", 
      "mode": "live_google",
      "services": {
        "search_console": { ... },
        "bing_webmaster": { ... },
        "google_business": { ... }
      },
      "summary": { ... }
    },
    "ads": { "status": "local_evidence", ... },
    "whatsapp": { "status": "local_evidence", ... },
    "directories": { "status": "configured_no_local_evidence", ... }
  },
  "summary": {
    "local_evidence": 3,
    "live_success": 1,
    "configured_no_local_evidence": 2
  }
}
```

## Seguridad

- **`--live-meta`**: Solo READ, nunca publiquemos, nunca actualicemos.
- **`--live-google`**: Solo READ desde GSC + Bing, no modifica.
- **`--live-ads`**: Solo READ desde Marketing API: no crea/modifica campañas, no gasta presupuesto.
- **`--live-whatsapp`**: Solo READ desde worker D1: no envía mensajes, no responde por sí mismo.
- **Tokens**: Cargados desde `.env`, nunca expuestos en logs.
- **Sanidad**: Resumen estructurado (`has_evidence`), no brute-force JSONs intermedios.

## Próximo

1. `collect_directories(live=True)`: Repeticiones de consultas de contactos
2. Completar documentación de despliegue (7 pasos)

Todos los adaptadores deberán conservar el mismo contrato de salida (`status`, `mode`, `*_configured`, `*_data`).

## Google Webmaster Tools (GSC + Bing)

El modo `live_google` captura métricas de Google Search Console y Bing Webmaster Tools.

| Fuente | Local | Live | Notas |
|--------|-------|------|-------|
| Search Console | GSC JSON locales | Search Analytics, Sitemaps | Requiere gsc_token.json (OAuth) |
| Bing Webmaster | Bing JSON locales | GetUrlList, GetCrawlErrors | Requiere BING_WEBMASTER_API_KEY |
| Google Business | GBP JSON locales | No implementado | Requiere Google Business Profile API |

### Estados

- `live_success`: GSC/Bing capturados + summary con métricas agregadas
- `live_error`: excepción al leer API
- `not_configured`: falta gsc_token.json o BING_WEBMASTER_API_KEY

### Estructura del snapshot

```json
{
  "google": {
    "status": "live_success",
    "mode": "live_google",
    "services": {
      "search_console": {
        "status": "success",
        "period": {"start": "2026-09-26", "end": "2026-10-25"},
        "metrics": {
          "clicks": 123,
          "impressions": 4567,
          "ctr": 0.0269,
          "position": 12.5
        },
        "top_queries": [
          {"query": "zapatería flexi piedras negras", "clicks": 45, "impressions": 1200, "ctr": 0.0375, "position": 3.2}
        ],
        "top_pages": [...],
        "sitemaps": [...]
      },
      "bing_webmaster": {
        "status": "success",
        "period": {"start": "2026-09-26", "end": "2026-10-25"},
        "indexed_pages": 15,
        "crawl_errors": 0
      },
      "google_business": {
        "status": "not_implemented",
        "note": "Requiere Google Business Profile API",
        "place_id": "ChIJ...",
        "configured": true
      }
    },
    "summary": {
      "total_clicks": 123,
      "total_impressions": 4567,
      "avg_ctr": 0.0269,
      "avg_position": 12.5,
      "indexed_pages": 15,
      "crawl_errors": 0
    }
  }
}
```

### Uso

```bash
# Snapshot local (por default)
python3 scripts/sync_all.py --tenant flexi

# Snapshot con Google live (requiere gsc_token.json + BING_WEBMASTER_API_KEY en .env)
python3 scripts/sync_all.py --tenant flexi --live-google
```

### Seguridad

- Solo READ desde GSC + Bing: no modifica sitemaps, no cambia configuración.
- Tokens: gsc_token.json (OAuth refresh) + BING_WEBMASTER_API_KEY en .env.
- Sanidad: `summary` agrega métricas para decisión G4.

## WhatsApp Live

El modo live_whatsapp captura mensajes y estados remotos del worker de WhatsApp (`wrangler.toml` + D1).

| Fuente | Local | Live | Notas |
|--------|-------|------|-------|
| Worker config | `wrangler.toml` | Si está deployado | Lee binding D1 y database_id |
| Message Echoes | N/A | Consulta (simulada) | WABA: 1087457280345914; Webhook aún no reporta por permisos JWT |
| Remote contacts | CRM local | SELECT direction, status FROM messages | Solo lectura desde D1 del worker |

### Estructura del snapshot

```json
{
  "whatsapp": {
    "status": "live_success",
    "mode": "live_whatsapp",
    "live_worker_configured": true,
    "live_message_echoes": {
      "outcome": "success",
      "note": "Consulta preparada; Webhook aún no reporta por permisos JWT.",
      "flags": {"message_echoes_available": false, ...}
    },
    "live_remote_contacts": {
      "outcome": "success",
      "stats": {"directions": {"in": N, "out": N}, "status_counts": {...}, "total_messages": N},
      "last_sync_at": "2026-10-25T20:00:00Z",
      "waba_id": "1087457280345914",
      "waba_db": "flexi_whatsapp_obs"
    },
    "contacts": {"total": M, "test_records": P}
  }
}
```

### Uso

```bash
# Snapshot local (por default)
python3 scripts/sync_all.py --tenant flexi

# Snapshot con WhatsApp live
python3 scripts/sync_all.py --tenant flexi --live-whatsapp
```

### Seguridad

- Solo READ desde worker D1: no envía mensajes, no responde por sí mismo.
- Tokens: si el worker necesita Bearer token, se puede leer desde secretos locales (placeholder).
- Sanidad: `live_message_echoes` y `live_remote_contacts` incluyen `outcome` para indicar permisos/fallo.

## Ads Live

El modo live_ads captura métricas de campañas publicitarias usando Meta Marketing API (v26.0).

| Fuente | Local | Live | Notas |
|--------|-------|------|-------|
| Campañas | Estado en Markdown (00_estado.md) | Marketing API /insights | Solo lectura: spend, impressions, clicks, reach, frequency, CTR, CPM, CPC |
| Ad sets | Documentados en Markdown | Marketing API | Mismo contrato de campos |
| Ads | Documentados en Markdown | Marketing API | Mismo contrato |

### Estados

- `live_success`: account configurado + insights capturados
- `live_error`: excepción al leer API
- `live_denied`: access_token denegado por Meta
- `not_configured`: falta ad_account_id en config['ads']

### Estructura del snapshot

```json
{
  "ads": {
    "status": "live_success",
    "mode": "live_ads",
    "ad_account_configured": true,
    "campaigns": [
      {
        "id": "238461234567890",
        "name": "Flexi OI26 - Prueba 500MXN",
        "objective": "MESSAGES",
        "status": "ACTIVE",
        "spend": 487.23,
        "impressions": 12450,
        "clicks": 312,
        "reach": 8921,
        "frequency": 1.39,
        "ctr": 2.51,
        "cpm": 39.12,
        "cpc": 1.56,
        "conversations": 47,
        "cost_per_conversation": 10.37
      }
    ],
    "summary": {
      "total_spend": 487.23,
      "total_impressions": 12450,
      "total_clicks": 312,
      "total_conversations": 47
    },
    "local_campaigns": [...]
  }
}
```

### Uso

```bash
# Snapshot local (por default)
python3 scripts/sync_all.py --tenant flexi

# Snapshot con Ads live (requiere ad_account_id en config.json)
python3 scripts/sync_all.py --tenant flexi --live-ads
```

### Seguridad

- Solo READ desde Marketing API: no crea/modifica campañas, no gasta presupuesto.
- Tokens: mismo META_ACCESS_TOKEN que Graph API.
- Sanidad: cada campaña incluye `cost_per_conversation` calculado (spend/conversations) para decisión G4.

## Avance Graph API Pull (2026-10-26)

Durante la implementación del adaptador `growth/integrations/whatsapp_graph.py` se validó con Meta Graph API v26.0 lo siguiente:

### Resultado

- El endpoint `/phone_number_id/conversations` no es válido para WhatsApp Cloud API y devuelve `(#100) Tried accessing nonexisting field (conversations)`.
- El endpoint `/page_id/conversations` sí responde correctamente, pero corresponde a las conversaciones de la **Página de Facebook / Messenger**, no a un pull directo del historial de WhatsApp Cloud.
- La primera prueba devolvió 10 conversaciones recientes con participantes, fecha de actualización, conteo de mensajes y no leídos.
- La consulta de `/conversation_id/messages` devolvió mensajes, pero el campo `direction` viene vacío; por lo tanto, el conteo actual de `inbound`/`outbound` no es confiable.

### Corrección aplicada

- `get_conversations()` ahora usa `/page_id/conversations` en lugar de `/phone_number_id/conversations`.
- `pull_conversations_with_depth()` usa el `page_id` de la configuración del tenant.
- Se mantiene el modo solo lectura: no se envían mensajes ni se modifica nada en Meta.

### Limitación principal

- WhatsApp Cloud API normalmente entrega mensajes históricos mediante webhooks, no mediante un endpoint de consulta tipo Messenger.
- Sin el permiso/evento `message_echoes`, no es posible capturar los mensajes salientes escritos por la sucursal desde la app de WhatsApp Business.
- Por ahora, `/page_id/conversations` puede ayudar a medir conversaciones de Messenger/Page, pero **no debe interpretarse como el historial completo de WhatsApp**.

### Estado del diagnóstico de ecos

- El worker D1 registra eventos entrantes y estados.
- El payload contiene claves `message_echoes`, pero hasta el diagnóstico no se encontraban ecos guardados.
- El resultado previo fue `blocked_no_waba_app_subscription`: no se detectó la app conectada al WABA en la metadata consultada.
- El permiso denominado `channel_messages` no aparece como un permiso real de Meta; se trató de una hipótesis local, no de un permiso confirmado.

### Próximos pasos recomendados

1. No usar `/page_id/conversations` como fuente oficial de WhatsApp.
2. Resolver la suscripción del webhook de WhatsApp Cloud a `message_echoes` y `messages`.
3. Verificar que la app `Universe Publicaciones` (ID `26134666266196379`) esté efectivamente suscrita al WABA de Flexi.
4. Ejecutar una prueba controlada: recibir un mensaje y responder desde la app de la sucursal.
5. Correr de nuevo el diagnóstico del worker D1; se espera al menos un evento saliente (`out`) y la clave `smb_message_echoes`.
6. Hasta entonces, medir profundidad real de WhatsApp únicamente con los eventos guardados por el worker.
