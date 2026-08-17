---
title: "Calendario propuesto de Instagram — 17–30 de agosto de 2026"
purpose: "Definir una primera ola selectiva de publicaciones de Instagram a partir del calendario Facebook 17–30, usando únicamente assets existentes y el flujo manual aprobado por fila."
status: "Review"
created: 2026-08-17
updated: 2026-08-17
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-14_Recomendacion_Instagram_CGO.md"
  - "Operations/Research/2026-08-16_Asignacion_Visual_Calendario_17_30_Agosto.csv"
  - "Operations/Production/instagram_15_16_scheduler_playbook.md"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "Operations/Research/2026-08-17_Investigacion_Ventanas_Temporales_Meta.md"
organization: "Operations/Research"
---

# Calendario propuesto de Instagram — 17–30 de agosto de 2026

## Alcance

Este documento es una **propuesta de cola selectiva**, no una programación nativa de Instagram. Meta no ofrece actualmente una ruta operativa confiable para `scheduled_publish_time` en esta cuenta; por ello, cada fila debe aprobarse explícitamente y publicarse de forma inmediata mediante `media → FINISHED → media_publish`.

El calendario Facebook permanece independiente. No se crearán imágenes nuevas, no se moverán assets desde Drive durante la publicación y no se recuperarán slots perdidos automáticamente. Si una hora pasa, la fila se convierte en una nueva decisión editorial y no se presenta como publicación cumplida en horario.

## Primera ola recomendada

La primera ola contiene seis assets ya existentes, separados para observar distintos horarios, personajes y contextos sin duplicar todo el calendario de Facebook.

| Orden | Fecha objetivo | Hora objetivo | Asset | Tipo | Caption exacto | Motivo CGO | Estado operativo |
|---:|---|---|---|---|---|---|---|
| 1 | 2026-08-17 | 10:00 | `260633 - Universe.png` | `Reuse_Top` | `😮‍💨 #UniverseSentMe` | Primer test de imagen estática, Universe y horario de mañana. | `Pendiente_Aprobación_Fernando` |
| 2 | 2026-08-19 | 13:30 | `260560 - Fantasma.png` | `Reuse_Top` | `Esperando octubre… 👻 #UniverseSentMe` | Candidato prioritario; Fantasma tiene señal previa y el mensaje es legible sin contexto. | `Pendiente_Aprobación_Fernando` |
| 3 | 2026-08-21 | 19:00 | `260614 - Universe.png` | `Reuse_Top` | `Analizando mi propio caos. 🧐 #UniverseSentMe` | Candidato secundario para probar una franja nocturna con copy breve. | `Pendiente_Aprobación_Fernando` |
| 4 | 2026-08-23 | 22:00 | `260625.png` | `Reuse_Top` | `El cambio da miedo… quedarse igual también. 😮‍💨 #UniverseSentMe` | Candidato prioritario; composición vertical y humor relatable. | `Pendiente_Aprobación_Fernando` |
| 5 | 2026-08-25 | 17:00 | `260613 - Wilfred.png` | `Reuse_Top` | `Wilfred sabe. 🌲 #UniverseSentMe` | Prueba de personaje; visual simple y copy de reconocimiento inmediato. | `Pendiente_Aprobación_Fernando` |
| 6 | 2026-08-30 | 22:00 | `260528 - Universe.png` | `Reuse_Top` | `Ya duérmete… 🌙 #UniverseSentMe` | Contexto nocturno explícito; reserva el horario de domingo por la noche. | `Pendiente_Aprobación_Fernando` |

Las fechas y horas son **ventanas de decisión**, no órdenes automáticas. Antes de cada publicación se debe confirmar que la fila no tenga `IG_Media_ID`, no esté `PUBLICADA` ni `ELIMINADA_MANUALMENTE`, y que exista una URL pública exacta del asset.

## Reservas y exclusiones

| Grupo | Assets | Decisión |
|---|---|---|
| Candidatos secundarios | `260633`, `260613`, `260620`, `260644`, `260635` | Mantener en cola; seleccionar solo si una pieza de la primera ola no está disponible o si se decide ampliar la prueba. |
| Doble sentido / riesgo de distribución | `260539`, `humor4.16` | No usar en la primera ola. Requieren aprobación individual y deben probarse de forma aislada, sin otra pieza sexualizada cercana ni promoción pagada. |
| Ya activas | `2608030`, `2608036`, `2608060` | No republicar. Mantener sus IDs y permalinks como historial activo. |
| Prohibida | `260583` | No tocar ni republicar. Su estado histórico es `ELIMINADA_MANUALMENTE`. |
| Nuevos del calendario Facebook | Las piezas `2608027`–`2608065` con caption pendiente | Mantener Facebook-first hasta validar visualmente el asset y aprobar una fila específica para Instagram. |

## Flujo de bajo consumo

La operación recomendada usa una revisión local de la fila y una sola ejecución de publicación por asset aprobado. La validación debe recuperar solo la fila objetivo y revisar la URL, caption e idempotencia. El publicador debe derivar el Page Access Token, crear un único contenedor, esperar dentro del mismo proceso a `FINISHED`, ejecutar `media_publish` y guardar el resultado completo. No se deben abrir tareas recurrentes, hacer polling cada cinco minutos, consultar el historial completo de Instagram ni descargar nuevamente archivos de Drive.

Cada publicación debe registrar `IG_Container_ID`, `IG_Media_ID`, permalink, hora real, estado, caption exacto y cualquier error. La aprobación es por fila y no se extiende automáticamente a la siguiente.

## Medición

Instagram se medirá separado de Facebook. Para cada publicación se conservará un corte observado con hora real, edad del post, alcance, vistas, interacciones, shares, visitas al perfil, follows y comentarios disponibles. Estos cortes no se deben mezclar con `Interacciones_24h` o `Interacciones_72h` de Facebook.

## Decisión solicitada

Se solicita aprobar o modificar la **primera ola de seis assets**. La aprobación del calendario no constituye por sí sola autorización de publicación; cada ejecución futura deberá nombrar el asset, el caption exacto y la autorización de Instagram únicamente.

## Documentos que requerirán actualización después de la aprobación

Una vez aprobada la ola, deberán actualizarse este documento, la recomendación CGO de Instagram, el ledger de publicación, el ledger de experimentos y el índice. Si se publica una pieza, solo se añadirán datos devueltos por Meta; no se crearán filas ficticias.
