# Módulo `communications`

Observación y medición de conversaciones. WhatsApp es **solo lectura**; los
comentarios de Facebook tienen una puerta de publicación explícita para
respuestas aprobadas.

## Estructura

```
modules/communications/
├── agent.py               CommunicationsAgent (sugerencia y análisis sombra)
├── llm.py                 cliente OmniRoute compartido (chat/JSON)
├── policy.py              gate de calidad y voz de marca
├── comments/
│   ├── facebook.py        captura, propuestas y publicador aprobado
│   ├── log.py             esquema y migración de comments_log.csv
│   ├── paths.py           rutas explícitas por tenant (sin escrituras)
│   ├── responder.py       UniverseResponder canónico
│   └── review.py          fachada local inbox_snapshot/review_comments
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

## Agente de Comunicaciones

`CommunicationsAgent` trabaja en modo `suggest`: clasifica el comentario,
propone un remate y aplica la política local. Nunca publica, nunca cambia
`aprobaciones.json` y nunca sustituye la aprobación humana. Facebook y WhatsApp
son canales; el agente es la capa compartida de criterio y voz.

El modelo por defecto es `openai/gpt-4.1-mini` vía OmniRoute. Las credenciales
se resuelven en este orden: variables de entorno, `.env` del repo/tenant y
finalmente el contexto de `~/.omniroute/config.json`. Ninguna credencial se
imprime.

Análisis sombra de los comentarios existentes (sin Meta y sin escribir
aprobaciones):

```bash
python3 -m modules.communications.agent --tenant universe --shadow
python3 -m modules.communications.agent --tenant universe --shadow --limit 5
python3 -m modules.communications.agent --tenant universe --shadow \
  --report /tmp/communications_shadow.json --json
```

El reporte incluye la clasificación, el borrador, el resultado de política,
latencia, uso de tokens, errores y la comparación entre `needs_response` y la
aprobación humana de referencia. Por defecto se guarda en
`tenants/<tenant>/comment_responses/facebook_comments/reports/`.

Reglas de seguridad:

- Un borrador con cualquier bandera de calidad queda en `decision: review` y
  `response: null`.
- Precio, stock, tallas, enlaces, claims comerciales y frases corporativas no
  se proponen.
- Solo se envía texto público y contexto creativo al modelo; nunca IDs de
  autor, `comment_id` ni datos personales.
- `approved: true` y la publicación explícita siguen siendo gates humanos
  separados.

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

## Comentarios de Facebook

La implementación canónica vive en `modules/communications/comments/`. Los
comandos históricos de Universe siguen funcionando como envoltorios:

```bash
python3 tenants/universe/harvest_comments.py
python3 tenants/universe/publish_comments.py
```

Los datos históricos **no se movieron** en esta fase:

- `tenants/<tenant>/comment_responses/facebook_comments/aprobaciones.json`
- `tenants/<tenant>/comment_responses/facebook_comments/data/comments_log.csv`

Revisión local, sin red ni POST:

```bash
python3 -m modules.cgo --mode comments_review --tenant universe
```

El agente de comunicaciones se puede ejecutar antes de esa revisión para
contrastar sus propuestas con las aprobaciones existentes. El análisis sombra
es read-only y no requiere token de Meta.

Publicación real de las entradas con `approved: true` y `approved_response`:

```bash
python3 -m modules.cgo --mode comments_review --tenant universe --publish
```

El gate `token` solo se exige con `--publish`. Sin él, la capacidad únicamente
resume aprobaciones y log local. Antes de cada POST se consulta Meta para no
duplicar una respuesta existente.
