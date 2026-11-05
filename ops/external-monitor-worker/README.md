# Monitor externo Growth OS

Worker independiente de Cloudflare que vigila dos superficies:

- `host-heartbeat`: el host envía un latido autenticado cada 5 minutos.
- `whatsapp-webhook`: consulta `/health` del worker de WhatsApp y su acceso a D1.

El Worker guarda estado en una D1 propia y ejecuta un cron cada 5 minutos. Solo
envía alertas cuando un check cambia de estado; al recuperarse envía un aviso de
recuperación. No escribe en Meta, campañas ni payouts.

## Rutas

| Ruta | Acceso | Uso |
| :--- | :--- | :--- |
| `GET /health` | Público | Salud del monitor y D1; no expone estados internos. |
| `GET /heartbeat?token=...` | Secreto | Registra el latido del host. |
| `GET /status?token=...` | Secreto | Estado operativo de ambos checks. |
| `GET /check?token=...` | Secreto | Ejecuta una evaluación manual sin esperar al cron. |

## Activación

1. Ejecutar `bash ops/external-monitor-worker/deploy.sh`.
2. Instalar el latido recurrente con `bash scripts/install_external_heartbeat_cron.sh`.
3. Confirmar `/status` y ejecutar una evaluación con `/check`.
4. Opcional: migrar el latido al ciclo systemd con
   `sudo bash scripts/install_ops_health.sh`.

El deploy genera `EXTERNAL_MONITOR_TOKEN` si falta, crea la URL de heartbeat y
la guarda en el `.env` raíz. No imprime ninguno de los dos valores.

Las alertas usan `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID` del `.env`. Mientras
Fernando sea el único destinatario, el chat configurado será su Telegram privado;
el grupo `Growth OS Ops` se incorporará cuando exista.
