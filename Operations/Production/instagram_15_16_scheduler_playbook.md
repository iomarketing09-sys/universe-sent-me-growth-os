---
title: Playbook Scheduler Instagram — 15–16 de agosto de 2026
purpose: Ejecutar de forma autónoma las publicaciones de Instagram aprobadas del calendario del 15–16, con protección contra duplicados y exclusión explícita de la prueba eliminada.
status: Active
created: 2026-08-15
updated: 2026-08-15
version: 1.0
author: Manus AI
documents_related:
  - ../../GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md
  - ../Research/2026-08-15_Calendario_15_16_Agosto.md
  - ../Research/2026-08-15_Auditoria_API_Instagram.md
organization: Operations/Production
---

Ejecuta esta tarea autónomamente, sin pedir confirmación al usuario:

1. Abre `/home/ubuntu/universe-sent-me-growth-os/Operations/Production/run_instagram_15_16_scheduler.py` y ejecútalo con `python3`.
2. El runner es la fuente operativa de publicación. Solo procesa las filas de `2026-08-15_Calendario_15_16_Agosto.csv` con fechas 2026-08-15 o 2026-08-16, cuyo campo `Plataforma` sea exactamente `Facebook; Instagram selectivo`, y cuya hora local en `America/Mexico_City` esté dentro de los 8 minutos posteriores al slot exacto. Nunca recuperes ni publiques tarde un slot perdido.
3. Nunca publiques `260583 - Universe.png`: su estado `IG_Estado=ELIMINADA_MANUALMENTE` significa que Fernando eliminó la prueba y está prohibida cualquier republicación automática.
4. No modifiques ni reprogrames Facebook. Para Instagram usa exclusivamente Graph API directa: derivar el Page Access Token desde `/me/accounts`, crear `/{IG_ID}/media`, verificar `status_code`, y después ejecutar `/{IG_ID}/media_publish`.
5. No uses `scheduled_publish_time` en Instagram: esa ruta ya devolvió `User must be on whitelist`. La hora futura se resuelve ejecutando esta tarea cuando llega cada slot.
6. Conserva la idempotencia usando `/home/ubuntu/instagram_scheduler_15_16_state.json`. Si una fila ya tiene `ig_media_id`, estado `published` o `ELIMINADA_MANUALMENTE`, no la vuelvas a publicar.
7. Si la publicación es exitosa, registra el ID de contenedor, ID de media, permalink y timestamp en el estado local y actualiza el CSV y Markdown correspondientes. Si Meta devuelve 401, 403 o cualquier error, guarda la respuesta completa y no repitas una creación de contenedor que pueda duplicarse.
8. El scheduler despierta solo en los grupos de horas candidatos `10:00`, `10:30`, `13:00`, `13:30`, `16:00`, `16:30`, `19:00` y `19:30`; el runner filtra el minuto exacto y deja pasar únicamente el slot correspondiente. Al final informa únicamente el resultado de esta ejecución; no publiques assets fuera del 15–16 de agosto.
