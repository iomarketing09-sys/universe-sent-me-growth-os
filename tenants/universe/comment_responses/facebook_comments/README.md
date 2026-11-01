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

Para usar el nuevo Agente de Comunicaciones como generador de propuestas:

```bash
python3 tenants/universe/harvest_comments.py --agent
```

El agente se activa solo con `--agent`; las propuestas siguen entrando como
`approved: false`, incluyen metadatos del agente y nunca se publican solas. Si
el agente falla, se usa el responder anterior como fallback.

Para revisar las propuestas en Markdown y CSV:

```bash
python3 -m modules.communications.review_report \
  --input tenants/universe/comment_responses/facebook_comments/reports/agent_pilot_20261101T0200Z.json
```

2. Revisar y editar `aprobaciones.json`. Solo se publican las entradas con `approved: true` y `approved_response` no vacío.

3. Publicar respuestas aprobadas:

```bash
python3 tenants/universe/publish_comments.py
```

El publicador usa tandas de máximo 5 respuestas y una pausa de 15 minutos entre
tandas. Para ajustarlo:

```bash
python3 tenants/universe/publish_comments.py \
  --batch-size 5 --batch-pause-seconds 900
```

También se puede revisar desde CGO sin red ni escrituras:

```bash
python3 -m modules.cgo --mode comments_review --tenant universe
```

La publicación desde CGO exige `--publish` y el gate de token:

```bash
python3 -m modules.cgo --mode comments_review --tenant universe --publish
```

## Automatización

`growth-os-comments.timer` ejecuta cada hora entre 08:00 y 22:00 una captura
de comentarios y genera propuestas, pero **nunca publica**. La ejecución deja:

- `aprobaciones.json` como fuente de verdad.
- `aprobaciones_nuevas.json` como vista de solo lectura con lo aún no aprobado.
- `reports/nuevas_pendientes.md` y `.csv` para revisar en chat.

La publicación sigue siendo una decisión humana: solo se envían las respuestas
marcadas con `approved: true`. Un worker de systemd puede procesar esas
aprobaciones en segundo plano, sin depender de que el chat o la terminal sigan
abiertos.

Para instalar o reactivar el timer:

```bash
bash scripts/install_comments_timer.sh
```

### Publicador en segundo plano

`growth-os-comments-publish.timer` despierta cada 15 minutos al worker, que
publica únicamente respuestas ya aprobadas. No captura comentarios, no aprueba
nada y no procesa `aprobaciones_nuevas.json` porque esa vista es de solo
lectura. El worker usa un candado exclusivo y tandas de 5 respuestas con 15
minutos de pausa.

```bash
bash scripts/install_comments_publisher.sh
systemctl list-timers growth-os-comments-publish.timer --no-pager
journalctl -u growth-os-comments-publish.service -f
```

Para lanzar una tanda inmediata sin esperar al timer:

```bash
sudo systemctl start --no-block growth-os-comments-publish.service
```

Para desactivarlo:

```bash
sudo systemctl disable --now growth-os-comments-publish.timer
```

No se recomienda cron para este flujo: systemd evita ejecuciones simultáneas
del mismo servicio, conserva el estado en `journalctl` y permite limitar el
tiempo de ejecución.

Para revisar una cola separada de propuestas nuevas sin tocar la principal:

```bash
python3 -m modules.cgo --mode comments_review --tenant universe \
  --comments-approvals-file tenants/universe/comment_responses/facebook_comments/aprobaciones_nuevas_8.json
```

## Protecciones

- `main.py` usa dry-run por defecto; publicar requiere `--live --publish-approved`.
- Antes de responder, el publicador consulta si la página ya tiene una respuesta en Meta.
- Cada respuesta enviada se guarda con `published`, `published_at` y `reply_id`; repetir el comando no la duplica.
- Las aprobaciones existentes se conservan al refrescar propuestas.
- Entre local y Drive se usa el archivo con fecha de modificación más reciente; una versión vieja nunca sobrescribe la revisión actual.
- El worker de publicación toma de Drive cualquier cola más reciente antes de publicar y sincroniza el resultado al terminar.
- `data/comments_log.csv` usa un esquema único de 18 columnas y conserva las filas históricas.

## Diagnóstico

```bash
python3 tenants/universe/comment_responses/facebook_comments/main.py \
  --dry-run --hours 168 --max-comments 200
```

El token de usuario de `META_ACCESS_TOKEN` se intercambia en memoria por el token de página mediante `/me/accounts`; no se escribe en disco.
