---
title: Playbook Scheduler Instagram — 15–16 de agosto de 2026
purpose: Registrar y ejecutar únicamente publicaciones de Instagram aprobadas manualmente por Fernando, con protección contra duplicados y exclusión explícita de la prueba eliminada; la automatización programada queda desactivada.
status: Active
created: 2026-08-15
updated: 2026-08-17
version: 1.8
author: Manus AI
documents_related:
  - ../../GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md
  - ../Research/2026-08-15_Calendario_15_16_Agosto.md
  - ../Research/2026-08-15_Auditoria_API_Instagram.md
  - ../Research/2026-08-16_Instagram_2608060_Prueba_Resultado.json
  - ../Research/2026-08-17_Instagram_Republicacion_2608036_2608060.json
organization: Operations/Production
---

## Modo operativo vigente: aprobación manual

La tarea programada está pausada desde el 2026-08-16. Este playbook no autoriza ejecuciones autónomas. Cada publicación de Instagram requiere una decisión explícita de Fernando para una fila concreta; sin esa aprobación, el runner no debe crear contenedores ni publicar media. Facebook mantiene su registro independiente y no debe modificarse desde este flujo.

## Procedimiento manual aprobado

Cuando Fernando apruebe una fila específica, se deberá comprobar el asset exacto, caption, estado `IG_Estado`, ausencia de `ig_media_id` y contexto editorial. Solo después se ejecutará `media`, se verificará `status_code` y se ejecutará `media_publish`. La decisión manual deberá indicar como mínimo la fila o asset, la hora de publicación inmediata y si se autoriza Instagram únicamente. Nunca usar `scheduled_publish_time` ni republicar `260583 - Universe.png`. Si la fila ya tiene cualquier `IG_Media_ID` o está marcada `Eliminada_Manualmente`, la ejecución se detiene antes de llamar a Meta; no se crea un contenedor de prueba ni se reintenta.

## Historial del procedimiento anterior

Las instrucciones siguientes documentan el runner heredado y no constituyen autorización para nuevas ejecuciones automáticas:

Ejecuta esta tarea autónomamente, sin pedir confirmación al usuario:

1. Abre `/home/ubuntu/universe-sent-me-growth-os/Operations/Production/run_instagram_15_16_scheduler.py` y ejecútalo con `python3`.
2. El runner es la fuente operativa de publicación. Solo procesa las filas de `2026-08-15_Calendario_15_16_Agosto.csv` con fechas 2026-08-15 o 2026-08-16, cuyo campo `Plataforma` sea exactamente `Facebook; Instagram selectivo`, y cuya hora local en `America/Mexico_City` esté dentro de los 8 minutos posteriores al slot exacto. Nunca recuperes ni publiques tarde un slot perdido. Las cinco imágenes ya fueron alojadas una sola vez en URLs temporales; cada despertar reutiliza únicamente la URL correspondiente y no descarga ni sube archivos otra vez.
3. Nunca publiques `260583 - Universe.png`: su estado `IG_Estado=ELIMINADA_MANUALMENTE` significa que Fernando eliminó la prueba y está prohibida cualquier republicación automática.
4. No modifiques ni reprogrames Facebook. Para Instagram usa exclusivamente Graph API directa: derivar el Page Access Token desde `/me/accounts`, crear `/{IG_ID}/media`, verificar `status_code`, y después ejecutar `/{IG_ID}/media_publish`.
5. No uses `scheduled_publish_time` en Instagram: esa ruta ya devolvió `User must be on whitelist`. La hora futura se resuelve ejecutando esta tarea cuando llega cada slot.
6. Conserva la idempotencia usando `/home/ubuntu/instagram_scheduler_15_16_state.json`. Si una fila ya tiene `ig_media_id`, estado `published` o `ELIMINADA_MANUALMENTE`, no la vuelvas a publicar.
7. Si la publicación es exitosa, registra el ID de contenedor, ID de media, permalink y timestamp en el estado local y actualiza el CSV y Markdown correspondientes. Si Meta devuelve 401, 403 o cualquier error, guarda la respuesta completa y no repitas una creación de contenedor que pueda duplicarse. No uses `gws`, `copy`, `cp` ni operaciones de Drive durante la ejecución; el movimiento mensual ya ocurrió antes del scheduler.
8. El scheduler despierta solo en los grupos de horas candidatos `10:00`, `10:30`, `13:00`, `13:30`, `16:00`, `16:30`, `19:00` y `19:30`; el runner filtra el minuto exacto y deja pasar únicamente el slot correspondiente. Al final informa únicamente el resultado de esta ejecución; no publiques assets fuera del 15–16 de agosto.

## Registro de ejecución

### 2026-08-15 00:11:13 America/Mexico_City

- Resultado: `nothing_due`.
- Filas procesadas: 0.
- IDs de contenedor: ninguno.
- IDs de media: ninguno.
- Errores de Meta: ninguno; no se realizaron llamadas de publicación porque ningún slot estaba dentro de la ventana válida de ocho minutos.
- Facebook: sin cambios.
- Exclusión confirmada: `260583 - Universe.png` no fue recuperada ni publicada.
- `scheduled_publish_time`: no utilizado.

### 2026-08-15 00:16:21 America/Mexico_City

- Resultado: `nothing_due`.
- Filas procesadas: 0.
- IDs de contenedor: ninguno.
- IDs de media: ninguno.
- Errores de Meta: ninguno; no se realizaron llamadas `media`, verificación ni `media_publish` porque ningún slot estaba dentro de la ventana válida de ocho minutos.
- Facebook: sin cambios.
- Exclusión confirmada: `260583 - Universe.png` no fue recuperada ni publicada.
- `scheduled_publish_time`: no utilizado.

### 2026-08-15 10:10:20 America/Mexico_City

- Resultado: `nothing_due`.
- Filas objetivo validadas: 4 filas con `Plataforma=Facebook; Instagram selectivo` para 2026-08-15 y 2026-08-16.
- Filas procesadas: 0; el slot de 10:00 ya estaba fuera de la ventana válida de ocho minutos al despertar del runner.
- IDs de contenedor: ninguno.
- IDs de media: ninguno.
- Errores de Meta: ninguno; no se realizaron llamadas `media`, verificación ni `media_publish`.
- Facebook: sin cambios.
- Exclusión confirmada: `260583 - Universe.png` no forma parte de las filas objetivo y no fue recuperada ni publicada; permanece prohibida por `IG_Estado=ELIMINADA_MANUALMENTE`.
- `scheduled_publish_time`: no utilizado.

### 2026-08-15 10:39:40 America/Mexico_City

- Resultado: `nothing_due`.
- Filas objetivo validadas: 4 filas con `Plataforma=Facebook; Instagram selectivo` para 2026-08-15 y 2026-08-16.
- Filas procesadas: 0; el slot de 10:00 estaba fuera de la ventana válida de ocho minutos cuando despertó el runner.
- IDs de contenedor: ninguno.
- IDs de media: ninguno.
- Errores de Meta: ninguno; no se ejecutaron llamadas `media`, verificación ni `media_publish`.
- Facebook: sin cambios.
- Exclusión confirmada: `260583 - Universe.png` no fue recuperada ni publicada y permanece bloqueada por `IG_Estado=ELIMINADA_MANUALMENTE`.
- `scheduled_publish_time`: no utilizado.
- Estado local: `/home/ubuntu/instagram_scheduler_15_16_state.json` permaneció sin registros nuevos.

---

### 2026-08-15 10:47:13 America/Mexico_City — Cambio a aprobación manual

- La tarea programada `USM Instagram 15-16 Agosto` quedó desactivada.
- Motivo: la ejecución automática no garantizaba que el despertar coincidiera con la ventana de ocho minutos posterior al slot; además, la zona configurada era `America/Matamoros` mientras el procedimiento exigía `America/Mexico_City`.
- Instagram: seis filas quedaron registradas como `PENDIENTE_APROBACION_MANUAL` o `PENDIENTE_REVISION_MANUAL` en el CSV; ninguna fue publicada por este cambio.
- Facebook: sin cambios.
- `260583 - Universe.png`: continúa excluida por `ELIMINADA_MANUALMENTE`.

### 2026-08-15 10:59:44 America/Mexico_City — Publicación manual aprobada de 2608030

- Resultado: `published` mediante Graph API directa.
- Cuenta/IG ID: `17841462696378190` (`@universe_sent_me_0326`).
- Asset: `2608030 - Universe - Que fibra tomas pa cagarla tanto.jpeg`.
- Caption: `¿Qué fibra tomas para cagarla tanto? 🐈 #UniverseSentMe #UniverseUSM #MemesUSM`.
- ID de contenedor: `17976428061089880`.
- Verificación: `status_code=FINISHED`; Meta confirmó que el media estaba listo para publicarse.
- ID de media: `18145111759484218`.
- Permalink: https://www.instagram.com/p/DcEX6BSE8ka/
- Hora real publicada: `2026-08-15T10:59:41-06:00`.
- `scheduled_publish_time`: no utilizado.
- Facebook: sin cambios.
- `260583 - Universe.png`: no tocada y continúa excluida por `ELIMINADA_MANUALMENTE`.

**Nota de coherencia documental:** El CSV operativo fue actualizado con los IDs, permalink, estado `PUBLICADA` y hora real de Instagram. La recomendación CGO y el calendario Markdown deben reflejar que Instagram funciona como laboratorio selectivo con decisiones fila por fila; Facebook conserva su programación independiente.


### 2026-08-16 — Diagnóstico de despertares repetidos y pausa de seguridad

- La tarea `USM Instagram 15-16 Agosto` tenía estado activo, `runAsNewTask=true`, cron `0 0,30 11,14,17,20 15,16 8 *`, zona `America/Matamoros` y expiración `2026-08-17T04:30:00Z`.
- La configuración del proyecto contiene el conector editable `Universe Sent Me Meta API` con UID `76925630-05da-4aa7-878d-64a6a520ca6d` y estado habilitado. No se modificó el conector.
- El playbook y el runner sí existen y están versionados en `Operations/Production/`. El mensaje de la tarea sobre archivo inexistente no coincide con el repositorio; la causa operativa más probable es que una tarea nueva no recibe automáticamente las rutas locales del sandbox de la sesión principal.
- La tarea fue pausada mediante `manus-config schedule update --enabled=false`. Su estado operativo actual es `pause`; no se ejecutaron publicaciones, no se modificó Facebook, no se movió Drive y `260583` permanece excluida.
- No se debe reactivar esta tarea histórica. La distribución de Instagram queda en aprobación manual fila por fila hasta que Fernando solicite una campaña nueva con un playbook autocontenido y un horario válido.

---

### 2026-08-16 — Preflight de prueba única para 2608060

- Resultado: `BLOCKED_IDEMPOTENCY`.
- Asset validado: `2608060 - Kael+Maeve - gustos salvajones.jpeg`.
- Cuenta objetivo: `@universe_sent_me_0326` (`17841462696378190`).
- La fila ya tenía `IG_Media_ID=17922210816414183` y `Estado_Publicacion=Eliminada_Manualmente` en los ledgers.
- Acción: detenerse antes de `media`; no se creó contenedor, no se verificó estado y no se ejecutó `media_publish`.
- `scheduled_publish_time`: no utilizado.
- Facebook: sin cambios. Drive: sin cambios. Scheduler: sin cambios. Reintentos: ninguno.
- Evidencia: `Operations/Research/2026-08-16_Instagram_2608060_Prueba_Resultado.json`.

La aprobación recibida del 2026-08-16 sí autorizó excepcionalmente la republicación de `2608036` y `2608060`, pese a sus publicaciones anteriores eliminadas manualmente. Esta excepción es puntual, queda documentada en la evidencia de republicación y no autoriza republicar `260583` ni duplicar `2608030`.

### 2026-08-16 18:43 America/Matamoros — Republicación autorizada de 2608036

La republicación excepcional de `2608036- Elara+Evan - Nadie nos soporta.jpeg` fue autorizada explícitamente por Fernando. Se utilizó el asset existente y una URL CDN pública temporal; no se generó una imagen nueva. Meta confirmó `status_code=FINISHED` y después `media_publish` devolvió el media `17891183814416135`, con permalink https://www.instagram.com/p/DcHxuuWllRk/. La hora real fue `2026-08-16T18:43:02-06:00`. No se utilizó `scheduled_publish_time`, no se tocó Facebook, Drive ni el scheduler y no hubo reintento.

### 2026-08-16 18:43 America/Matamoros — Republicación autorizada de 2608060

La republicación excepcional de `2608060 - Kael+Maeve - gustos salvajones.jpeg` fue autorizada explícitamente por Fernando. Se utilizó el asset existente y una URL CDN pública temporal; no se generó una imagen nueva. Meta confirmó `status_code=FINISHED` y después `media_publish` devolvió el media `17909839698449207`, con permalink https://www.instagram.com/p/DcHxv5SlorV/. La hora real fue `2026-08-16T18:43:17-06:00`. No se utilizó `scheduled_publish_time`, no se tocó Facebook, Drive ni el scheduler y no hubo reintento.

Estas dos filas nuevas son publicaciones activas distintas de los intentos históricos eliminados. `2608030` permanece sin duplicar y `260583` sigue prohibida.
