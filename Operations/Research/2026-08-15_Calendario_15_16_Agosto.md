# Calendario operativo programado — 15 y 16 de agosto de 2026

**Propósito:** Preparar un calendario listo para programar después de la aprobación, usando la misma estrategia de fin de semana: 2 nuevas + 2 reuse el sábado y 3 nuevas + 2 reuse el domingo estelar.
**Estado:** Programada
**Fecha de creación:** 2026-08-15
**Última actualización:** 2026-08-15
**Versión:** 1.1
**Autor:** Manus AI
**Documentos relacionados:** [`2026-08-15_Inventario_Memes_Nuevos_Drive.md`](2026-08-15_Inventario_Memes_Nuevos_Drive.md), [`../../GrowthOS/05_03_Calendario_10_16_Agosto.md`](../../GrowthOS/05_03_Calendario_10_16_Agosto.md), [`../../GrowthOS/01_03_Reuse_Queue.md`](../../GrowthOS/01_03_Reuse_Queue.md), [`../../GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md`](../../GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md)

## Resumen

- 9 publicaciones propuestas: 5 nuevas y 4 reuse aprobados manualmente.
- Sábado: 10:00, 11:00, 13:30 y 19:00.
- Domingo estelar: 10:00, 13:30, 16:00, 19:00 y 22:00.
- Las nueve publicaciones fueron aprobadas y programadas mediante Graph API; sus IDs están registrados en el CSV y en cada fila de esta tabla.
- Los nueve originales utilizados fueron movidos a `Humor existencial/08 Agosto` sin crear copias.

## Calendario

| Fecha | Día | Hora | Tipo | Asset | Caption | Estado | Plataforma | Nota |
|---|---|---:|---|---|---|---|---|---|
| 2026-08-15 | Sábado | 10:00 | Nueva | `2608030 - Universe - Que fibra tomas pa cagarla tanto.jpeg` | ¿Qué fibra tomas para cagarla tanto? 🐈 #UniverseSentMe #UniverseUSM #MemesUSM | `PROGRAMADA` | Facebook; Instagram selectivo | Nuevo; remate inmediato y legible; evitar explicar el texto visual. Meta Post `1036844829507460_122150559441072582`; Photo `122150559393072582`; original movido a `08 Agosto` sin copia. |
| 2026-08-15 | Sábado | 11:00 | Reuse_Approved_User_Context | `260583 - Universe.png` | 😼 #UniverseSentMe #UniverseUSM #MemesUSM | `PROGRAMADA` | Facebook | Reuse manual aprobado; conservar contexto original y verificar que no haya publicación reciente. Meta Post `1036844829507460_122150559591072582`; Photo `122150559555072582`; original movido a `08 Agosto` sin copia. |
| 2026-08-15 | Sábado | 13:30 | Nueva | `2608033 - Fantasma - vendra primero mi boda o jesus.jpeg` | La pregunta importante del día. 👻 #UniverseSentMe #FantasmaUSM #MemesUSM | `PROGRAMADA` | Facebook; Instagram selectivo | Nuevo; humor absurdo y pregunta clara. Revisar ortografía final del asset antes de programar. Meta Post `1036844829507460_122150559693072582`; Photo `122150559639072582`; original movido a `08 Agosto` sin copia. |
| 2026-08-15 | Sábado | 19:00 | Reuse_Approved_User_Context | `260539 - Evan+Kiri.png` | 🫣🫣 #UniverseSentMe #EvanUSM #KiriUSM | `PROGRAMADA` | Facebook; Instagram solo tras revisión | Reuse manual con doble sentido/sexualización válida; mantener contexto y no impulsar con pauta. Meta Post `1036844829507460_122150559765072582`; Photo `122150559729072582`; original movido a `08 Agosto` sin copia. |
| 2026-08-16 | Domingo | 10:00 | Nueva | `2608037- Universe - soñe que era un litrro de agua.jpeg` | Necesito hidratarme hasta en los sueños. 💧 #UniverseSentMe #UniverseUSM #MemesUSM | `PROGRAMADA` | Facebook; Instagram selectivo | Nuevo; pieza visual de Universe y gag reconocible para la mañana. Meta Post `1036844829507460_122150559873072582`; Photo `122150559807072582`; original movido a `08 Agosto` sin copia. |
| 2026-08-16 | Domingo | 13:30 | Reuse_Approved_User_Context | `260673 - Universe.png` | 😐 #UniverseSentMe #UniverseUSM #MemesUSM | `PROGRAMADA` | Facebook | Reuse manual aprobado; copy mínimo para dejar que el visual cargue el remate. Meta Post `1036844829507460_122150559981072582`; Photo `122150559921072582`; original movido a `08 Agosto` sin copia. |
| 2026-08-16 | Domingo | 16:00 | Nueva | `2608036- Elara+Evan - Nadie nos soporta.jpeg` | Cuando hasta ustedes dos saben que son demasiado. 😅 #UniverseSentMe #ElaraUSM #EvanUSM | `PROGRAMADA` | Facebook; Instagram selectivo | Nuevo; formato de pareja y humor relatable para la tarde. Meta Post `1036844829507460_122150560083072582`; Photo `122150560041072582`; original movido a `08 Agosto` sin copia. |
| 2026-08-16 | Domingo | 19:00 | Nueva | `2608060 - Kael+Maeve - gustos salvajones.jpeg` | No tenemos gustos raros, tenemos gustos salvajones. 😏 #UniverseSentMe #MaeveUSM #MemesUSM | `PROGRAMADA` | Facebook; Instagram selectivo | Nuevo; reservar para la transición nocturna y revisar contexto de pareja. Meta Post `1036844829507460_122150560215072582`; Photo `122150560143072582`; original movido a `08 Agosto` sin copia. |
| 2026-08-16 | Domingo | 22:00 | Reuse_Approved_User_Context | `humor4.16.png` | 🫣🫣 #UniverseSentMe #MemesUSM | `PROGRAMADA` | Facebook; Instagram solo tras revisión | Reuse manual con contexto sexualizado; domingo estelar y horario nocturno. No combinar con otra pieza sexualizada cercana. Meta Post `1036844829507460_122150560383072582`; Photo `122150560341072582`; original movido a `08 Agosto` sin copia. |

## Registro de ejecución

La programación se ejecutó mediante Graph API usando el Page Access Token derivado desde `/me/accounts`. Meta devolvió `is_published: false` y `scheduled_publish_time` para los nueve posts, confirmando que quedaron programados y no publicados inmediatamente. Los IDs de publicación y de foto temporal están en el CSV operativo.

## Reglas de ejecución

La aprobación de Fernando quedó recibida antes de la ejecución. Las nueve órdenes de Facebook fueron creadas; Instagram permanece como distribución selectiva no ejecutada en esta operación porque el calendario no incluía una orden de publicación inmediata para esa plataforma. El calendario del 17–30 de agosto no fue alterado.

### Referencias

[1]: 2026-08-15_Inventario_Memes_Nuevos_Drive.md — Registro de los assets nuevos.
[2]: ../../GrowthOS/05_03_Calendario_10_16_Agosto.md — Contexto del calendario vigente.
[3]: ../../GrowthOS/01_03_Reuse_Queue.md — Reglas de reuse y contexto aprobado.
