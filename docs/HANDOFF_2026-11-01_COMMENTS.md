# Handoff — Comentarios y publicación automática

Actualizado: 2026-11-01 00:49 CDT
Repo: `/home/universe-sent-me/growth-os`
Rama: `main`

## Para continuar en un chat nuevo

Lee este archivo y revisa el estado actual antes de actuar:

```text
Lee docs/HANDOFF_2026-11-01_COMMENTS.md y continúa desde ahí.
No publiques ni cambies aprobaciones sin confirmación explícita.
```

## Estado actual

- `comments_review` está integrado en CGO y delega en `modules/communications/comments`.
- El publicador systemd corre fuera del chat:
  - `growth-os-comments-publish.service`
  - `growth-os-comments-publish.timer`
- El timer está activo y ejecuta el worker cada 15 minutos.
- El worker usa candado exclusivo, procesa solo `approved: true` y respeta tandas de 5 con pausa de 900 segundos.
- Ignora `aprobaciones_nuevas.json` porque tiene `kind: review_queue`; esa vista es de solo lectura.
- La captura horaria de propuestas sigue separada y nunca publica:
  - `growth-os-comments.service`
  - `growth-os-comments.timer`

Snapshot de colas al actualizar este documento:

- `aprobaciones.json`: 18/18 publicadas, 0 errores.
- `aprobaciones_nuevas_8.json`: 5/8 publicadas, 3 pendientes, 0 errores.
- El servicio quedó en pausa de 15 minutos antes de la última tanda.

## Commits locales

- `c120187` — `feat(comments): integrar revision y publicacion aprobada en CGO`
- `d8ca1ae` — `feat(comments): automatizar captura y publicacion con systemd`

No se ha hecho `push`. La data operativa sigue sin commitear a propósito porque
el worker la está escribiendo.

## Pendientes

1. Esperar a que `growth-os-comments-publish.service` termine las 3 respuestas restantes del lote.
2. Confirmar que no haya `last_error` en las colas.
3. Sincronizar las colas actualizadas con Google Drive.
4. Commitear por separado la data operativa:
   - `aprobaciones.json`
   - `aprobaciones_nuevas_8.json`
   - `comments_log.csv`
   - `publication_contexts.json`
   - `publication_log_week2.csv`
   - snapshots de métricas y sync
5. Hacer `push` cuando el usuario lo autorice.

## Comandos de operación

```bash
systemctl status growth-os-comments-publish.service --no-pager
systemctl list-timers growth-os-comments-publish.timer --no-pager
journalctl -u growth-os-comments-publish.service -f
```

Forzar una corrida:

```bash
sudo systemctl start --no-block growth-os-comments-publish.service
```

Detener la automatización:

```bash
sudo systemctl disable --now growth-os-comments-publish.timer
sudo systemctl stop growth-os-comments-publish.service
```

## Reglas de seguridad

- No publicar sin aprobación humana explícita.
- No aprobar ni descartar respuestas automáticamente.
- No publicar desde `aprobaciones_nuevas.json`; es una vista de revisión.
- Antes de cada POST, el publicador consulta Meta para evitar duplicados.
- Si dos procesos intentan publicar, el candado `.publish.lock` evita el solapamiento.

## Contexto del chat

Las memorias locales están activadas, pero no hay memoria consolidada de este
chat en `MEMORY.md` ni en `memory_summary.md`. Para continuar con fidelidad:

```bash
cd /home/universe-sent-me/growth-os
codex fork --last
```

Para un chat limpio, usar este handoff. Para revisar el contexto restante en la
TUI, ejecutar `/status`; para verlo siempre en el footer, configurar
`/statusline` con `context stats` y `token counters`.

Regla de checkpoint sugerida: cuando `/status` indique 25% o menos de contexto
restante, ejecutar `/export docs/chat_exports/<sesion>.md`, generar un handoff
actualizado y abrir el chat nuevo. No esperar a que el chat se cierre solo.
