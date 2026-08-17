# Recomendación CGO — distribución de memes en Instagram

**Propósito:** Definir si Universe Sent Me debe publicar memes estáticos en Instagram, qué piezas deben probarse primero y cómo separar evidencia de Facebook de evidencia propia de Instagram.  
**Estado:** Active
**Fecha de creación:** 2026-08-14
**Última actualización:** 2026-08-17
**Versión:** 1.5
**Autor:** Manus AI  
**Documentos relacionados:** [`GrowthOS/08_00_Metricas_Baseline_Plataformas.md`](../../GrowthOS/08_00_Metricas_Baseline_Plataformas.md), [`Operations/Research/2026-08-14_Propuesta_Calendario_17_30_Agosto_con_Copys.md`](2026-08-14_Propuesta_Calendario_17_30_Agosto_con_Copys.md), [`Operations/Research/2026-08-14_Analisis_Copys_Rendimiento.md`](2026-08-14_Analisis_Copys_Rendimiento.md), [`GrowthOS/12_00_Sistema_Dos_Capas_Contenido_Canon.md`](../../GrowthOS/12_00_Sistema_Dos_Capas_Contenido_Canon.md), [`Calendario Instagram 17–30 propuesto`](2026-08-17_Calendario_Instagram_17_30_Propuesto.md)

## Dictamen ejecutivo

**Sí recomiendo publicar una selección de memes estáticos en Instagram, pero no recomiendo duplicar automáticamente todo el calendario de Facebook.** La razón es que los datos disponibles muestran dos comportamientos distintos: Facebook funciona actualmente como motor de distribución de imágenes estáticas, mientras que Instagram tiene poco alcance absoluto y responde relativamente mejor a Reels que a imágenes. En la línea base registrada el 3 de agosto, Instagram mostraba entre 50 y 242 personas de alcance por pieza; el mejor Reel obtuvo 242 de alcance y 343 vistas, mientras que una imagen obtuvo solo 3 de alcance y 8 vistas. Esto no prueba que los memes estáticos no funcionen en Instagram: la muestra de imágenes es demasiado pequeña y el conector actual aparece desconectado, por lo que falta una prueba controlada reciente.

La recomendación, por tanto, es **mantener Facebook como superficie primaria y usar Instagram como laboratorio de descubrimiento**, con una cuota limitada de imágenes de alto potencial visual. No conviene desviar la producción de Facebook ni medir el éxito de Instagram con los mismos umbrales absolutos durante esta fase.

## Qué memes probaría primero

| Prioridad | Asset | Motivo CGO | Caption sugerido | Riesgo / condición |
|---|---|---|---|---|
| 1 | `260560 - Fantasma.png` | Fantasma ya tiene tracción en Facebook; el visual vertical es simple, legible y relatable. | `Esperando octubre… 👻 #UniverseSentMe` | Prueba orgánica; no asumir transferencia automática. |
| 2 | `260625.png` | Tiene composición vertical y un remate de humor ácido que se entiende sin contexto adicional. | `El cambio da miedo… quedarse igual también. 😮‍💨 #UniverseSentMe` | Revisar que el texto sea legible en preview. |
| 3 | `260528 - Universe.png` | Es una pieza vertical, nocturna y muy clara; puede probarse en domingo o noche. | `Ya duérmete… 🌙 #UniverseSentMe` | Solo horario nocturno; no usar como “buenos días”. |
| 4 | `260539 - Evan+Kiri.png` | Tiene fuerte capacidad de detener el scroll por el doble sentido y la reacción de Kiri. | `🫣 #UniverseSentMe` | Prueba orgánica, sin promoción pagada; revisar elegibilidad y distribución. |
| 5 | `humor4.16.png` | Es la pieza con mayor potencial de scroll-stop por el contexto sexualizado explícito. | `🫣🫣 #UniverseSentMe` | **Reserva de prueba**, no primera publicación. Puede recibir distribución limitada o quedar fuera de recomendaciones; nunca usar como base única de la estrategia. |
| 6 | `260614 - Universe.png` | Tiene formato vertical y una idea relatable, pero requiere leer más texto. | `Analizando mi propio caos. 🧐 #UniverseSentMe` | Secundario; probar después de las piezas 1–3. |

Las piezas `260539` y `humor4.16` no deben descartarse por su contexto sexualizado, porque el Growth OS ya define el doble sentido y la sexualización como atributos editoriales válidos de la capa libre de memes. Sin embargo, **validez editorial no equivale a distribución garantizada**: Instagram puede limitar la recomendación de contenido sexualmente sugerente aunque no exista desnudez explícita. Por eso deben tratarse como una hipótesis de distribución, no como la nueva línea editorial dominante.

## Qué no recomiendo hacer

No recomiendo publicar los 68 slots de Facebook también en Instagram. Eso duplicaría volumen sin evidencia de que el canal tenga capacidad de distribuirlo y dificultaría saber si el crecimiento proviene del formato, el personaje, el copy o la frecuencia. Tampoco recomiendo convertir todos los memes en Reels solo para “adaptarlos” a Instagram: la línea base muestra que los Reels tienen mejor desempeño relativo en Instagram, pero el alcance absoluto sigue siendo pequeño, y producir una versión de video de cada meme aumentaría el costo sin resolver el problema de distribución.

Tampoco recomiendo usar una pieza sexualizada como contenido de buenos días, publicarla junto a otra pieza sexualizada o impulsarla con pauta. El test debe ser orgánico, aislado y medido por alcance, vistas, interacciones, shares, visitas al perfil y follows.

## Diseño de prueba recomendado

Durante los primeros 14 días, Instagram debería recibir **una imagen estática seleccionada por cada dos o tres días**, además de los Reels que ya estén producidos. El calendario de Facebook permanece intacto. Las imágenes seleccionadas no se contabilizan dentro de la proporción 3:2 del experimento principal de Facebook; funcionan como una capa de distribución secundaria.

| Variable | Regla inicial |
|---|---|
| Volumen | 5–6 imágenes en 14 días, más Reels ya disponibles |
| Copy | Emoji mínimo o frase corta; no repetir el texto visual |
| Formato | Imagen vertical legible; evitar piezas con texto diminuto |
| Horarios | Mantener una ventana comparable, preferentemente 13:30–19:00; `260528` solo por la noche |
| Sexualizado | Máximo 1–2 pruebas en el periodo, separadas por varios días |
| Promoción pagada | No usar durante la prueba |
| Métricas | Alcance, vistas, interacciones, shares, visitas al perfil y follows |
| Criterio de avance | Repetir formato/personaje solo si supera claramente la mediana de IG del periodo y no presenta limitación de distribución |

## Decisión operativa

La decisión CGO es **cross-post selectivo, no cross-post masivo**. La primera tanda debería usar `260560`, `260625` y `260528`. Después, si la cuenta no presenta restricciones, se puede probar `260539`; `humor4.16` queda como reserva para una prueba controlada, porque su potencial de interacción es alto pero también lo es el riesgo de distribución limitada. El resto de los reuse debe permanecer Facebook-first hasta disponer de métricas propias de Instagram.

La ejecución automática queda bloqueada por decisión operativa. Cualquier publicación futura requiere aprobación manual explícita y registro propio de Instagram; la prueba histórica de `260583` permanece eliminada y no debe republicarse.

## Decisión operativa revisada — 2026-08-15

La automatización programada de Instagram queda descartada. Instagram se gestionará como un laboratorio de **aprobación manual fila por fila**: Fernando decide el asset, confirma el caption y autoriza la publicación inmediata; el sistema no debe recuperar slots perdidos ni publicar por inferencia. Facebook conserva su calendario y su programación independiente.

La pérdida de una ventana no debe convertirse en una prohibición de publicar. Si un meme sigue siendo oportuno y el asset está validado, se puede publicar fuera del slot original como una nueva decisión editorial, registrando la hora real y sin fingir que se cumplió el horario del calendario. Para proteger el aprendizaje CGO, se recomienda no publicar varios memes seguidos: elegir una pieza con alto potencial visual, esperar métricas iniciales y decidir la siguiente a partir de evidencia.

La primera prueba manual del lote fue `2608030 - Universe - Que fibra tomas pa cagarla tanto.jpeg`, publicada con aprobación explícita a las 10:59:41 de America/Mexico_City. El slot original de las 10:00 se conserva como perdido; la publicación se registra como decisión editorial fuera de horario. Antes de publicar otra pieza se deben recoger métricas iniciales de esta prueba. Como siguiente opción de menor riesgo editorial queda `2608033 - Fantasma - vendra primero mi boda o jesus.jpeg`, pero requiere corregir o confirmar la ortografía visible indicada en el calendario. No recomiendo comenzar con `260539`, `2608060` ni `humor4.16` sin revisión adicional por su contexto sexualizado o de pareja.

El flujo aprobado para cada decisión será: **selección manual → revisión de asset y caption → aprobación explícita → creación de media → verificación de estado → `media_publish` → registro de IDs, permalink, hora real y métricas iniciales**. En la prueba 2608030, Meta devolvió `status_code=FINISHED` y el permalink `https://www.instagram.com/p/DcEX6BSE8ka/`. No se utilizará `scheduled_publish_time`.

## Propuesta de cola selectiva 17–30 — 2026-08-17

La propuesta vigente para el siguiente periodo contiene seis assets existentes: `260633`, `260560`, `260614`, `260625`, `260613` y `260528`. No es una programación automática ni una autorización global de publicación. Cada fila requiere aprobación explícita, URL pública exacta, caption confirmado y validación de idempotencia antes de `media → FINISHED → media_publish`. El detalle de fechas objetivo, captions, reservas y exclusiones está en [`Calendario Instagram 17–30 propuesto`](2026-08-17_Calendario_Instagram_17_30_Propuesto.md).

La primera ola mantiene Facebook como superficie primaria, excluye `260583`, no republica `2608030`, `2608036` ni `2608060`, y deja `260539` y `humor4.16` como pruebas de mayor riesgo para una decisión posterior.

## Resultado de la primera ejecución de la ola 17–30 — 2026-08-17

La fila `260633 - Universe.png` fue publicada manualmente en Instagram con aprobación explícita de Fernando. Meta confirmó el contenedor `17976689082089880` en estado `FINISHED`, publicó el media `17943879225288953` y devolvió el permalink [https://www.instagram.com/p/DcIQHJJHEp0/](https://www.instagram.com/p/DcIQHJJHEp0/). La publicación ocurrió a las 23:08:35 de America/Matamoros, fuera de la ventana planeada de las 10:00; por tanto, se registra como decisión editorial fuera de horario y no como cumplimiento del slot.

La publicación no usó `scheduled_publish_time`, no modificó Facebook ni Drive y no creó un CNT porque la relación `260633 ↔ CNT-####` todavía no está confirmada. El asset fue localizado en la carpeta `05 Mayo`; la discrepancia con la expectativa operativa de `08 Agosto` se conserva como pendiente administrativa. Las otras cinco filas siguen requiriendo aprobación y ejecución individual.

## Recomendación sobre un nuevo scheduler — 2026-08-17

La tarea histórica de Instagram fue eliminada y **no recomiendo recrearla con intervalos, polling o el playbook 15–16**. El diagnóstico muestra cuatro riesgos: zona horaria inconsistente, despertares que no coinciden con los slots, tareas nuevas sin dependencias autocontenidas y posibilidad de confundir una ventana perdida con autorización para publicar tarde.

Si Fernando quiere automatizar las cinco filas restantes, la opción CGO aceptable es un scheduler de **una ejecución exacta por publicación**, con seis despertares totales para seis filas. Cada tarea debe contener el asset, caption, URL pública, fecha, hora, zona `America/Matamoros`, ventana máxima de ±2 minutos, bloqueo idempotente y regla `no-op_late`. Si la hora ya pasó, no publica ni recupera el slot; informa el incumplimiento para decisión humana. No se debe usar `scheduled_publish_time`, tocar Facebook, mover Drive ni ejecutar un worker recurrente.

Mi recomendación operativa inmediata es conservar el **modo manual fila por fila** hasta aprobar una campaña nueva autocontenida. Es más seguro y, con el volumen actual de Instagram, la diferencia de consumo frente a seis despertares programados no justifica todavía asumir el riesgo de una automatización defectuosa. El scheduler exacto solo debe implementarse después de confirmar las cinco filas, sus horarios y la zona horaria canónica.

## Referencias internas

[1]: ../../GrowthOS/08_00_Metricas_Baseline_Plataformas.md — Línea base de métricas de Facebook e Instagram, extraída de Windsor.ai el 3 de agosto de 2026.  
[2]: 2026-08-14_Analisis_Copys_Rendimiento.md — Análisis histórico de copys mínimos y emojis.  
[3]: 2026-08-14_Propuesta_Calendario_17_30_Agosto_con_Copys.md — Programación operativa con captions y decisiones de distribución.  
