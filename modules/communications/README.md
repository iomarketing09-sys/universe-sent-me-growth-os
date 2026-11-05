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

### Contexto del meme (solo tenants que lo declaran)

Un tenant cuyo comentario depende del chiste de la imagen declara en su
`config.json`:

```json
"comments": { "requires_meme_context": true }
```

Con esa bandera, si la publicación no tiene `meme_text` en
`publication_contexts.json`, el respondedor **no genera propuesta**: devuelve
`decision: sin_contexto` y el comentario queda en el log con
`publish_status: sin_contexto`. `inbox_snapshot` lo expone como
`sin_contexto` con la lista de `comment_ids`, que es la bandera de huecos a
llenar.

Sin la bandera (Flexi, Micas, Firma) el comportamiento no cambia: el copy y la
conversación son suficientes.

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

Para revisar propuestas en un formato legible, genera Markdown y CSV a partir
del JSON de aprobaciones o del reporte sombra:

```bash
python3 -m modules.communications.review_report \
  --input tenants/universe/comment_responses/facebook_comments/reports/agent_pilot_20261101T0200Z.json
```

Los archivos se guardan junto al JSON, dentro de `reports/`. El Markdown incluye
comentario, propuesta, estado y alertas; el CSV se puede abrir directamente en
hoja de cálculo.

Reglas de seguridad:

- Un borrador con cualquier bandera de calidad queda en `decision: review` y
  `response: null`.
- El meme y el copy mandan sobre el nombre del archivo. Los desajustes de
  contexto, los chistes literales del asset y las escenas inventadas también
  fuerzan revisión.
- El humor es ácido: se dirige a la situación, la pose o el remate del meme,
  nunca a la dignidad de una persona. Se sigue el juego, no se humilla.
- Si el primer borrador falla política o contexto, el agente hace una segunda
  pasada con el motivo del rechazo. Si vuelve a fallar, queda en revisión.
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

Para generar las propuestas de la captura con el agente (opt-in), usa
`--agent`. Las propuestas se guardan con `approved: false`; el publicador sigue
siendo el único que puede enviar algo a Meta, y solo con aprobación explícita:

```bash
python3 tenants/universe/comment_responses/facebook_comments/main.py \
  --dry-run --agent --max-comments 10

python3 tenants/universe/harvest_comments.py --agent
```

Si el agente no responde, el flujo cae automáticamente al responder anterior y
deja `agent.fallback: true` en la propuesta para que se pueda auditar.

Publicación real de las entradas con `approved: true` y `approved_response`:

```bash
python3 -m modules.cgo --mode comments_review --tenant universe --publish \
  --comments-batch-size 5 --comments-batch-pause-seconds 900
```

Si las propuestas se separaron en otra cola, indica el archivo explícitamente;
así se revisa y publica esa cola sin mezclarla con `aprobaciones.json`:

```bash
python3 -m modules.cgo --mode comments_review --tenant universe \
  --comments-approvals-file tenants/universe/comment_responses/facebook_comments/aprobaciones_nuevas_8.json
```

El gate `token` solo se exige con `--publish`. Sin él, la capacidad únicamente
resume aprobaciones y log local. Antes de cada POST se consulta Meta para no
duplicar una respuesta existente.

La captura y generación de propuestas puede automatizarse sin publicar con
`scripts/run_comments_harvest.py`. El timer `growth-os-comments.timer` corre
cada hora entre 08:00 y 22:00 y reconstruye `aprobaciones_nuevas.json` y
`reports/nuevas_pendientes.md`; la publicación sigue siendo manual.
