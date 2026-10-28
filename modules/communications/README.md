# Módulo `communications`

Observación y medición de conversaciones. **Solo lectura**: no envía mensajes.

## Estructura

```
modules/communications/
└── whatsapp/
    ├── agent.py             WhatsAppAgent (reporte completo por tenant)
    ├── adapters.py          Adaptadores del sync multitenant
    ├── graph.py             Graph API v26 (token de página, WABA, conversaciones)
    ├── d1.py                Cliente D1 de solo lectura (API REST de Cloudflare)
    ├── conversations.py     Resumen, profundidad y atribución a anuncios
    ├── echo_diagnostics.py  Diagnóstico de ecos (respuestas desde el celular)
    ├── backfill.py          Recupera ecos que el worker descartó
    ├── d1_write.py          Escrituras puntuales (solo reparaciones)
    └── env.py               Lectura de credenciales sin exponerlas
```

`growth/integrations/whatsapp_adapters.py` y `whatsapp_graph.py` siguen
funcionando como envoltorios de compatibilidad.

## Comandos

```bash
# Reporte completo (sin Graph)
python3 -m modules.communications.whatsapp.agent flexi

# Solo métricas concretas
python3 -m modules.communications.whatsapp.agent flexi --only depth
python3 -m modules.communications.whatsapp.agent flexi --only campaigns
python3 -m modules.communications.whatsapp.agent flexi --only echoes --graph

# Diagnóstico de ecos suelto
python3 -m modules.communications.whatsapp.echo_diagnostics flexi --output /tmp/ecos.json

# Recuperar ecos que el worker no guardó (dry-run por defecto)
python3 -m modules.communications.whatsapp.backfill flexi
python3 -m modules.communications.whatsapp.backfill flexi --apply
```

## Backfill de ecos

El worker guarda **todos** los payloads en `raw_events`, aunque no sepa leerlos. Cuando se
descubrió que Meta manda los ecos en `message_echoes` y el worker solo leía
`smb_message_echoes`, quedaron 21 respuestas humanas sin registrar (25–27 oct 2026). El
backfill relee esos payloads y las inserta con `INSERT OR IGNORE`, así que es idempotente:
correrlo dos veces no duplica nada. El campo `received_at` es el del momento real de llegada
a Meta; un eco trae un `timestamp` inválido (2017) y se conserva tal cual para no falsear el
dato original.

## Fuentes de datos

- **D1 del worker** (`flexi_whatsapp_obs`): tabla `events` (mensajes, estados,
  atribución) y `raw_events` (payload crudo para depurar).
- **Graph API**: apps suscritas al WABA y datos de cuenta.

Credenciales: `CF_API_TOKEN` y `META_ACCESS_TOKEN` se leen del entorno o de
`.env`. El módulo nunca las imprime. `account_id` y `d1_database_id` viven en
`tenants/<id>/whatsapp/config.json`.

## Seguridad

- `d1.py` rechaza cualquier consulta que no sea `SELECT`/`WITH`/`PRAGMA`.
- Los teléfonos nunca se guardan completos: el worker guarda hash + últimos 4.
- El verify token del webhook ya no vive en `config.json`; solo su referencia a
  `.env`.

## Comentarios (siguiente fase)

El módulo queda listo para añadir `comments/` (Facebook e Instagram) reusando
`modules/social/meta_graph.py`. No implementado todavía para no mezclarlo con la
ingesta de WhatsApp.
