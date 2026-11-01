# Comentarios Facebook - Universe Sent Me

La implementación canónica vive en `modules/communications/comments/`. Los
archivos `main.py`, `comment_log.py` y `responders/universe_responder.py` de esta
carpeta son envoltorios de compatibilidad. Las rutas de datos no cambiaron.

## Análisis sombra (read-only)

Antes de publicar se puede contrastar la bandeja actual contra el nuevo Agente
de Comunicaciones. Este comando no llama a Meta, no escribe
`aprobaciones.json` y no publica nada:

```bash
python3 -m modules.communications.agent --tenant universe --shadow
```

El reporte queda en `reports/communications_shadow_<timestamp>.json` dentro de
esta carpeta y no se versiona. Para una prueba corta:

```bash
python3 -m modules.communications.agent --tenant universe --shadow --limit 5
```

## Flujo seguro

1. Recolectar y generar propuestas en modo lectura:

```bash
python3 tenants/universe/harvest_comments.py
```

2. Revisar y editar `aprobaciones.json`. Solo se publican las entradas con `approved: true` y `approved_response` no vacío.

3. Publicar respuestas aprobadas:

```bash
python3 tenants/universe/publish_comments.py
```

También se puede revisar desde CGO sin red ni escrituras:

```bash
python3 -m modules.cgo --mode comments_review --tenant universe
```

La publicación desde CGO exige `--publish` y el gate de token:

```bash
python3 -m modules.cgo --mode comments_review --tenant universe --publish
```

## Protecciones

- `main.py` usa dry-run por defecto; publicar requiere `--live --publish-approved`.
- Antes de responder, el publicador consulta si la página ya tiene una respuesta en Meta.
- Cada respuesta enviada se guarda con `published`, `published_at` y `reply_id`; repetir el comando no la duplica.
- Las aprobaciones existentes se conservan al refrescar propuestas.
- Entre local y Drive se usa el archivo con fecha de modificación más reciente; una versión vieja nunca sobrescribe la revisión actual.
- `data/comments_log.csv` usa un esquema único de 18 columnas y conserva las filas históricas.

## Diagnóstico

```bash
python3 tenants/universe/comment_responses/facebook_comments/main.py \
  --dry-run --hours 168 --max-comments 200
```

El token de usuario de `META_ACCESS_TOKEN` se intercambia en memoria por el token de página mediante `/me/accounts`; no se escribe en disco.
