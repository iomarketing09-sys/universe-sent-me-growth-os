# Operación compartida de Growth OS

**Estado:** Activo · **Fecha:** 2026-11-02
**Alcance:** salud, alertas, SLA y ownership de los servicios que cruzan los
edificios de Growth OS.

La operación compartida es la capa transversal de la ciudad: no es un edificio
de negocio, sino la infraestructura que vigila los timers y servicios que usan
Comunicaciones, Growth, Datos y Monetización.

## Ownership

| Rol | Responsable | Alcance |
| :--- | :--- | :--- |
| Accountable y autoridad de canon | Fernando | Decisión final, canon y escalamiento |
| Operador técnico (CGO) | Codex | Repo, timers, runbooks y mantenimiento |
| Comunicaciones | Comunicaciones | Comentarios y WhatsApp Flexi |
| Growth/Ads | Growth | Instagram y latido de Ads |
| Datos | Datos/Operación | Sync diario multitenant |
| Monetización | Monetización | Sync de monetización |

Manus ya no forma parte de Growth OS y no figura como owner de ningún servicio.
Claude tampoco conserva un rol activo: Fernando absorbió la autoridad de canon.
El CGO puede preparar y auditar contenido, pero no aprobar canon ni publicar en
nombre de un owner funcional.

El registro operativo vive en `ops/services.yaml`. Cualquier cambio de cadencia,
owner o runbook debe actualizar ese archivo y este documento.

## Canal de alertas

Por ahora el único canal es un **Telegram privado de Fernando**. El bot y el
chat se configuran en el `.env` raíz:

```bash
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

El token nunca se versiona. Si se expone, se revoca en BotFather y se reemplaza
en `.env` y en el entorno del servicio.

El grupo compartido `Growth OS Ops` queda como siguiente paso. Hasta entonces,
el monitor y el watchdog notifican al chat privado; la visibilidad todavía no
está separada por rol.

Las alertas incluyen severidad, servicio, edificio, owner funcional, último
latido y runbook. La misma alerta no se reenvía durante 60 minutos; cuando el
sistema se recupera se envía un aviso de recuperación y se limpia el estado.

## Servicios vigilados

| Servicio | Cadencia | Alerta si | Owner funcional |
| :--- | :--- | :--- | :--- |
| `comments-harvest` | Cada hora, 08:00–22:00 | El timer no corre o la siguiente ejecución vence | Comunicaciones |
| `comments-publish` | Cada 15 minutos | No hay latido en 45 minutos o el servicio falla | Comunicaciones |
| `instagram` | Cada 15 minutos | No hay latido en 45 minutos, el servicio falla o `logs/intelligence/last.json` supera 45 minutos | Growth |
| `sync` | Diario | La siguiente ejecución vence o `logs/sync/last.json` supera 26 h | Datos |
| `monetization` | Diario, 02:15 | La siguiente ejecución vence o la salida supera 26 h | Monetización |

`growth-os-ads.timer` existe como timer dedicado, pero no está instalado. Hoy el
timer de Instagram ejecuta el latido de Ads; por eso el servicio vigilado es
`instagram`.

El ciclo de métricas de intelligence corre dentro del mismo timer de Instagram
(`scripts/run_ig_scheduler.py`) y deja su latido en `logs/intelligence/last.json`.
Las unidades `scripts/growth-os-intelligence.*` existen para separarlo, pero no
están instaladas: requieren `sudo` desde la terminal.

## Monitor externo

El monitor externo es un **sensor del NOC**, no un edificio nuevo. Cubre lo que
el watchdog interno no puede ver: que el host y el webhook sigan alcanzables
desde fuera aunque el propio host haya dejado de ejecutar el watchdog.

La configuración versionada vive en `ops/external_monitors.yaml`.

La implementación actual es un Worker independiente de Cloudflare
(`growth-os-external-monitor`) con una base D1 propia
(`growth_os_external_monitor`). El cron del Worker evalúa ambos checks cada 5
minutos. El worker usa el flag `global_fetch_strictly_public` para que la
consulta al webhook pase por la ruta pública de Cloudflare, no por una llamada
interna entre Workers.

| Check | Tipo | Qué mide | Owner funcional |
| :--- | :--- | :--- | :--- |
| `host-heartbeat` | Heartbeat | El host envía un latido cada 5 minutos | Operations |
| `whatsapp-webhook` | HTTP | `/health` del worker y acceso a D1 | Communications |

### Ownership

| Rol | Responsable | Alcance |
| :--- | :--- | :--- |
| Accountable | Fernando | Recibe alertas, aprueba severidad y tiene break-glass |
| Operador técnico | CGO | Crea checks, rota credenciales y mantiene runbooks |
| Owner funcional | Operations | Interpreta la alerta y ejecuta el runbook |

La cuenta del proveedor debe ser de operaciones, no personal. Las credenciales
se guardan fuera de Git; Fernando conserva acceso de recuperación. Administrar
el monitor no otorga autoridad para silenciar alertas, cambiar campañas ni
aprobar payouts.

### Activación y operación

El Worker y su D1 se despliegan con:

```bash
bash ops/external-monitor-worker/deploy.sh
```

El despliegue crea o reutiliza la D1, aplica el esquema, publica el cron y carga
los secretos. Si `EXTERNAL_MONITOR_TOKEN` no existe, lo genera y lo guarda en el
`.env` raíz; también deja `EXTERNAL_MONITOR_HEARTBEAT_URL` configurada.

El latido recurrente corre actualmente en el crontab del usuario del host:

```bash
bash scripts/install_external_heartbeat_cron.sh
```

El timer de systemd sigue ejecutando el watchdog interno. La migración del
latido al ciclo systemd requiere `sudo bash scripts/install_ops_health.sh`; no es
obligatoria para que el monitor externo funcione.

Para comprobar el estado sin exponer el token:

```bash
curl -sS -A 'GrowthOS-Monitor/1.0' \
  "https://growth-os-external-monitor.io-marketing-09.workers.dev/status?token=<token>"
```

El acceso manual a `/check` ejecuta una evaluación inmediata. Las alertas solo
se envían en transiciones para evitar repetir el mismo aviso cada 5 minutos.

El heartbeat solo se envía después de ejecutar el watchdog. Si el host está
caído, no hay latido y el proveedor alerta. Si el watchdog reporta un problema
de negocio, el latido sí se envía: el monitor externo mide liveness, no salud
de workflows.

### Reglas

- El monitor solo hace lecturas HTTP; no tiene permisos sobre Meta, campañas ni
  payouts. Su token de Cloudflare se usa únicamente para desplegar y rotar el
  Worker.
- No se comparten URLs de heartbeat, `/stats` ni tokens. El status page para un
  tenant debe mostrar solo su edificio y ningún dato interno.
- Un check por superficie: host, worker y, si crece la operación, un check por
  tenant. Un solo check agregado oculta qué edificio falló.
- El monitor externo complementa al watchdog; no lo reemplaza.

### Chequeo de trabajo pendiente

El watchdog también evalúa `comments-review-backlog`. No es un timer: lee la
cola maestra de comentarios y alerta cuando el trabajo se queda detenido aunque
los servicios sigan en verde.

| Condición | Alerta |
| :--- | :--- |
| Más de 5 propuestas sin revisar | `review_backlog` |
| La propuesta más vieja supera 4 horas | `review_stale` |
| Alguna respuesta aprobada sigue sin publicar | `approved_not_published` |
| Una aprobación no tiene texto de respuesta | `approved_without_response` |

La edad se toma de `first_seen_at`; si el registro es viejo, se reconstruye con
el primer avistamiento en `data/comments_log.csv`.

## Cómo ejecutar el watchdog

Sin enviar nada:

```bash
python3 scripts/run_ops_health.py --json
```

Con salida legible:

```bash
python3 scripts/run_ops_health.py
```

Enviando alertas reales por Telegram:

```bash
python3 scripts/run_ops_health.py --notify
```

Prueba del canal, sin ejecutar el watchdog:

```bash
python3 scripts/run_ops_health.py --test-telegram
```

El código de salida es `0` si todo está bien, `1` si hay advertencias y `2` si
hay un problema crítico. Esto permite que systemd marque la ejecución como
fallida y conserve el diagnóstico en `journalctl`.

## Instalación

```bash
bash scripts/install_ops_health.sh
systemctl list-timers growth-os-health.timer --no-pager
journalctl -u growth-os-health.service -n 50 --no-pager
```

Para desactivarlo:

```bash
sudo systemctl disable --now growth-os-health.timer
```

## Runbooks

### Regla común

1. Revisar `systemctl status <unit>` y `journalctl -u <unit> -n 100 --no-pager`.
2. Confirmar que el `.env` y las credenciales del servicio estén presentes.
3. Revisar si hay una ejecución manual en curso antes de relanzar.
4. Relanzar solo el servicio afectado, no todos los timers.
5. Si el fallo es de credenciales o de un proveedor externo, escalar a Fernando.
6. Registrar qué se hizo y si se cambió una cadencia o un owner.

### intelligence

- **Síntoma:** el watchdog reporta `instagram` con el latido de intelligence vencido,
  o el reporte semanal no trae datos nuevos.
- **Revisar:** `systemctl status growth-os-ig.timer`,
  `journalctl -u growth-os-ig.service -n 100 --no-pager` y
  `logs/intelligence/last.json`.
- **Acción:** ejecutar `python3 scripts/run_intelligence_cycle.py --all-tenants` en manual.
- **No hacer:** borrar filas del ledger ni inventar ventanas E0/E24/E72 para recuperar historial.
- **Escalar:** si Meta rechaza el token o un tenant queda en `failed`.

### comments-harvest

- **Síntoma:** no se generan propuestas nuevas o el timer no despierta.
- **Revisar:** `systemctl status growth-os-comments.timer`, `journalctl -u growth-os-comments.service`.
- **Acción:** ejecutar `python3 scripts/run_comments_harvest.py` en modo manual.
- **No hacer:** publicar o aprobar comentarios desde este runbook.
- **Escalar:** si Meta rechaza el token o el harvest falla repetidamente.

### comments-publish

- **Síntoma:** hay respuestas aprobadas sin publicar o el worker no late.
- **Revisar:** `systemctl status growth-os-comments-publish.timer`, `journalctl -u growth-os-comments-publish.service`.
- **Acción:** lanzar una tanda manual solo si no hay otra ejecución:
  `sudo systemctl start --no-block growth-os-comments-publish.service`.
- **No hacer:** cambiar `approved`, `approved_response` ni estados para forzar una publicación.
- **Escalar:** si Meta devuelve error de permisos o el reply no se confirma.

### comments-backlog

- **Síntoma:** el watchdog reporta `review_backlog`, `review_stale` o
  `approved_not_published`.
- **Revisar:** `python3 scripts/run_ops_health.py --json` y la cola
  `tenants/universe/comment_responses/facebook_comments/aprobaciones.json`.
- **Acción:** revisar las propuestas pendientes y aprobar o descartar con
  motivo explícito. Si hay aprobadas sin publicar, revisar el journal de
  `growth-os-comments-publish.service`.
- **No hacer:** aprobar en masa ni editar `published`/`reply_id` a mano para
  silenciar la alerta.
- **Escalar:** si la cola crece durante varios ciclos o el publicador no puede
  confirmar los replies.

### instagram

- **Síntoma:** no hay publicaciones programadas o no se capturan métricas de Ads.
- **Revisar:** `systemctl status growth-os-ig.timer`, `journalctl -u growth-os-ig.service`.
- **Acción:** ejecutar `python3 scripts/run_ig_scheduler.py --all-tenants` en modo de diagnóstico.
- **Escalar:** si el fallo es de Meta Graph o de un asset.

### sync

- **Síntoma:** `logs/sync/last.json` está viejo o el sync diario falla.
- **Revisar:** `systemctl status growth-os-sync.timer`, `journalctl -u growth-os-sync.service`, `logs/sync/last.err`.
- **Acción:** ejecutar `bash scripts/cron_sync.sh` manualmente.
- **Escalar:** si el fallo es de Google Drive, Meta o credenciales de un tenant.

### monetization

- **Síntoma:** no aparece un corte diario o la salida de Content Earnings está vieja.
- **Revisar:** `systemctl status growth-os-monetization.timer`, `journalctl -u growth-os-monetization.service`.
- **Acción:** ejecutar `python3 scripts/run_monetization_sync.py --all --json` en modo diagnóstico.
- **No hacer:** aprobar periodos o registrar payouts desde este runbook.
- **Escalar:** si Meta no devuelve earnings o hay una discrepancia financiera.

## Límites de esta primera versión

- El watchdog interno corre en el mismo host que los servicios. El monitor
  externo ya cubre la caída total del host mediante el heartbeat recurrente.
- Telegram es el único canal. Si Telegram falla, el error queda en el journal,
  pero no hay ruta secundaria. El grupo compartido todavía no existe.
- La revisión de `whatsapp-webhook` ya tiene `/health` real y configuración en
  `ops/external_monitors.yaml`; falta crear el monitor en el proveedor y cargar
  el heartbeat. La seguridad HMAC sigue validada.
