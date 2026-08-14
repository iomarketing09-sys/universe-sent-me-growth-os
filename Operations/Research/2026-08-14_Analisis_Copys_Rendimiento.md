# Análisis de copys y rendimiento — 14 de agosto de 2026

**Propósito:** Registrar la evidencia histórica sobre longitud de copy, emojis y rendimiento para orientar los copys del experimento `EXP-2026-08-CAL-01`.  
**Estado:** Review  
**Fecha de creación:** 2026-08-14  
**Última actualización:** 2026-08-14  
**Versión:** 1.0  
**Autor:** Manus AI  
**Documentos relacionados:** [`Operations/Research/2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto.md`](2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto.md), [`Operations/Research/2026-08-14_Propuesta_Calendario_17_30_Agosto.md`](2026-08-14_Propuesta_Calendario_17_30_Agosto.md), [`GrowthOS/01_03_Reuse_Queue.md`](../../GrowthOS/01_03_Reuse_Queue.md)

## Hallazgo principal

La evidencia disponible respalda la intuición de que **un copy mínimo —incluso un emoji— puede funcionar muy bien**, pero no demuestra que los emojis sean la causa del rendimiento. En el conjunto histórico de 508 publicaciones, varios de los mejores posts usaron uno o dos emojis y hashtags mínimos:

| Rendimiento | Copy observado | Interacciones |
|---|---|---:|
| 1 | `🫣🫣 #UniverseSentMe` | 5,482 |
| 2 | `😒` | 4,103 |
| 3 | `😐` | 3,993 |
| 5 | `😮‍💨` | 3,740 |
| 7 | `🫣🫣 #UniverseSentMe #humor #relatable #astrologia #retrogrado` | 3,002 |
| 8 | `😭🫣 #UniverseSentMe #humoracido #memesUSM` | 2,979 |

También existen buenos resultados con texto corto y una idea clara, como `No es desinterés...`, que alcanzó 3,726 interacciones, y `Ya va ser la hora del tecito 😇`, con 2,280. Los copys largos no deben descartarse automáticamente: el post de “Lunes de enfoque” obtuvo 1,702 interacciones, pero su mayor longitud y su llamado a comentar lo convierten en una variante distinta, no directamente comparable con un emoji.

## Regla provisional para la prueba

Para memes estáticos cuyo punchline ya está dentro de la imagen, el copy base será **mínimo**: uno o dos emojis que reaccionen al remate, opcionalmente acompañados por un hashtag de marca. No se añadirá una explicación que repita el meme. Para piezas cuyo texto visual no cierre por sí mismo, se probará un copy corto de una frase. Los llamados a comentar se reservarán para piezas diseñadas para conversación y se etiquetarán como variante de copy.

La prueba no debe asignar automáticamente copy mínimo a todas las piezas. Se registrará `Tipo_Copy` como `Emoji_Minimo`, `Frase_Corta` o `Conversacional`, para comparar el efecto sin confundir formato visual, horario y tipo de contenido.

## Límites

Estos datos son observacionales. Los posts con emojis también pueden haber tenido mejor imagen, mejor horario, mayor novedad, más shares o mayor distribución inicial. Por tanto, el resultado se usará como regla de producción y como hipótesis de copy, no como causalidad demostrada.

### Referencias

[1]: ../../Operations/Research/2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto.md — Comparación histórica de rendimiento.  
[2]: ../../GrowthOS/Integracion_Growth_OS.md — HypothesisBank y ExperimentLog.  
