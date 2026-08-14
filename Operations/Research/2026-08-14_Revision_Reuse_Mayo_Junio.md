# Revisión de Reuse — Mayo frente a Junio

**Propósito:** Revisar rápidamente la disponibilidad física de memes en `My Drive/Universe sent me/USM/Humor existencial/05 Mayo`, cruzarla con la Reuse Queue y comprobar si conviene pasar a piezas de junio para la prueba de dos semanas.

**Estado:** Review  
**Fecha de creación:** 2026-08-14  
**Última actualización:** 2026-08-14  
**Versión:** 1.5
**Autor:** Manus AI  
**Documentos relacionados:** [`GrowthOS/01_03_Reuse_Queue.md`](../../GrowthOS/01_03_Reuse_Queue.md), [`Operations/Research/2026-08-14_Diseno_Prueba_Calendario_2_Semanas.md`](2026-08-14_Diseno_Prueba_Calendario_2_Semanas.md), [`GrowthOS/05_02_Calendario_04_09_Agosto.md`](../../GrowthOS/05_02_Calendario_04_09_Agosto.md), [`GrowthOS/05_03_Calendario_10_16_Agosto.md`](../../GrowthOS/05_03_Calendario_10_16_Agosto.md)

---

## 1. Resultado rápido

La carpeta de mayo ahora está organizada operativamente por Fernando. La raíz contiene los candidatos que no se han publicado en los últimos 30 días; las carpetas separadas contienen lo reutilizado en julio y agosto. Esto corrige el problema anterior de confundir inventario físico con reserva disponible. La raíz de mayo vuelve a ser una fuente válida de candidatos, aunque cada pieza todavía debe pasar por el filtro de rendimiento, saturación, claridad y canon.

| Fuente | Inventario encontrado | Estado para la prueba |
|---|---:|---|
| Raíz de `05 Mayo` | 133 assets: 131 imágenes y 2 videos | Candidatos disponibles según clasificación del usuario; pendientes de filtro de rendimiento/canon |
| `05 Mayo/Reutilizado Agosto` | 21 imágenes | Historial de reuse; no usar automáticamente en la prueba |
| `05 Mayo/Reutilizado Juilo (menos de 30 dias)` | 7 imágenes | Historial de reuse reciente; bloqueado por la regla de 30 días |
| Fecha individual de publicación en mayo | No disponible para los 133 candidatos raíz | Registrar como `Unknown_May_2026`; no inventar fecha |
| Carpeta `06 Junio` | 197 imágenes y una subcarpeta `Top` | Reserva más reciente |
| Subcarpeta `06 Junio/Top` | 9 archivos: 8 piezas y 1 captura de pantalla | 8 candidatos curados de alto interés |

La raíz de mayo puede tratarse como disponible bajo la clasificación de Fernando: no se ha publicado en los últimos 30 días. La fecha exacta de publicación original en mayo queda como desconocida y no debe reconstruirse artificialmente a partir de `createdTime` o `modifiedTime` de Drive. El control operativo será `Fecha_Ultima_Publicacion = Unknown_May_2026`, `Regla_30_Dias = Confirmada_por_usuario` y una nueva fecha real de reuse registrada cuando se publique.

## 2. Revisión visual rápida de mayo

Se revisó una muestra estratificada de piezas físicas de Drive; después, el usuario confirmó que varias de las piezas mostradas ya habían sido publicadas. Por ello, la revisión visual se conserva como evaluación de estilo, no como validación de disponibilidad. La carpeta contiene principalmente memes verticales con texto incrustado, buena legibilidad general y variedad suficiente: escenas de Wilfred, Universe, Fantasma, gatos minimalistas, fondos atmosféricos, humor relatable, frases existenciales y algunos comics de varias viñetas.

No se observó una razón visual para eliminar la carpeta de mayo completa. Sí conviene poner algunas piezas en revisión antes de publicar cuando el copy es largo, demasiado contextual, dependiente de una situación específica o visualmente menos claro. Las piezas de estilo minimalista, las de una sola idea y las que tienen un personaje fácilmente identificable son mejores candidatas para la prueba de reuse.

La muestra sugiere que mayo todavía puede aportar variedad, pero no debe rellenar slots solo porque hay muchos archivos. La cola debe priorizar rendimiento histórico y evitar repetir el mismo personaje, fondo o formato en días consecutivos.

## 3. Estado de mayo frente a la prueba de dos semanas

La prueba requiere aproximadamente 28 piezas `Reuse_Top` durante 14 días. La raíz de mayo contiene 133 candidatos clasificados por el usuario como no publicados en los últimos 30 días, por lo que sí existe una reserva física suficiente para cubrir la prueba. No obstante, la selección final debe limitarse a 28 piezas con buen rendimiento histórico, diversidad de personajes y ausencia de bloqueos de canon.

El conjunto `06 Junio/Top` sigue siendo útil como reserva de contenido más reciente, pero ya no es necesario depender de él para completar los 28 slots. La raíz de mayo ofrece suficiente volumen; junio puede usarse selectivamente para introducir frescura y evitar que toda la prueba dependa de memes de mayo.

## 4. Recomendación operativa

Se recomienda **no descartar ni borrar piezas de mayo**. La raíz debe funcionar como fuente principal de la prueba y las carpetas históricas deben conservarse como archivo de trazabilidad. Para el calendario experimental, la selección debe seguir este orden:

1. Seleccionar los 28 `Reuse_Top` desde la raíz de mayo, aplicando rendimiento histórico, diversidad de personajes, claridad y canon.
2. Sustituir selectivamente entre 4 y 8 slots por piezas de `06 Junio/Top` si aportan frescura o personajes distintos.
3. Mantener fuera de la prueba las carpetas `Reutilizado Agosto` y `Reutilizado Juilo (menos de 30 dias)`, salvo nueva validación explícita de antigüedad.
4. Dejar fuera temporalmente los archivos con errores, copy demasiado contextual, duplicados de formato o bloqueos de canon.

La recomendación actualizada es **usar la raíz de mayo como fuente principal de la prueba**, porque ya está separada por estado operativo y contiene 133 candidatos. Se recomienda reservar entre 4 y 8 slots para piezas de junio si sus métricas y personajes aportan variedad. Las carpetas `Reutilizado Agosto` y `Reutilizado Juilo (menos de 30 dias)` deben permanecer fuera de la selección actual, salvo que una pieza supere explícitamente la ventana de 30 días y vuelva a validarse.

## 5. Piezas y grupos que requieren atención

Las piezas ya reutilizadas en julio y agosto quedaron físicamente separadas por Fernando y no forman parte de la raíz candidata. En particular, la carpeta `Reutilizado Agosto` contiene 21 imágenes y `Reutilizado Juilo (menos de 30 dias)` contiene 7 imágenes. La muestra visual anterior queda reemplazada por esta clasificación estructural de Drive.

## 6. Cruce con publicaciones de Meta

Se extrajo el historial de Facebook del 1 al 31 de mayo de 2026 y se obtuvieron **205 publicaciones**. El cruce se realizó comparando los adjuntos de imagen de Meta con los 131 archivos de imagen de la raíz de mayo mediante hashes perceptuales, conservando además el ID de publicación, fecha, permalink, reacciones, comentarios y shares.

| Resultado del cruce | Cantidad |
|---|---:|
| Publicaciones de Meta de mayo | 205 |
| Publicaciones con adjunto de imagen descargable | 202 |
| Coincidencias de imagen confirmadas automáticamente | 135 publicaciones |
| Coincidencias confirmadas únicas | 123 assets |
| Publicaciones con coincidencia que requieren revisión | 67 publicaciones |
| Assets raíz de mayo sin coincidencia confirmada | 8 imágenes |
| Assets con más de una publicación histórica | 11 |

Las coincidencias confirmadas no significan que el meme deba reutilizarse automáticamente. Significan que ahora conocemos su rendimiento histórico individual. En los casos publicados más de una vez se conserva el máximo y la mediana de interacciones para evitar que un único resultado distorsione la selección.

El ranking inicial identifica 28 candidatos para la prueba, priorizados por máximo de interacciones, mediana, shares, diversidad y revisión de canon. Los primeros candidatos por interacciones fueron `260633 - Universe.png` con 14, `260642 - Universe+Wilfred.png` con 12, `260528 - Universe.png` con máximo 11 y mediana 8.5, `260644 - Universe.png` con 10, `260515 - Universe.png` con 10 y `260560 - Fantasma.png` con máximo 10 y mediana 5.5.

Los ocho assets sin coincidencia confirmada son `260514 - Que feo fingir que estas bien.png`, `260539 - Evan+Kiri.png`, `260563.png`, `260583 - Universe.png`, `260663 - Kiri.png`, `260673 - Universe.png`, `humor4.16.png` y `Universe - Existencial 260507.png`. No deben clasificarse como malos; simplemente quedan como `Sin_Historial_Visual_Confirmado` hasta una revisión manual o una coincidencia adicional.

El cruce es una mejora importante frente a la ausencia anterior de fechas y métricas, pero el hash perceptual puede producir coincidencias `Review_Image` en piezas visualmente parecidas. Para la prueba se deben usar primero las coincidencias `Confirmed_Image_Likely` y revisar manualmente cualquier candidato marcado como revisión antes de programarlo.

## 7. Revisión manual de los ocho assets sin match

La revisión visual manual fue completada y Fernando aprobó las ocho piezas para integrarlas a la reutilización. El doble sentido y la sexualización se consideran atributos editoriales válidos para esta línea de contenido, no motivos automáticos de descarte.

Las ocho piezas quedan como `Approved_User_Context`. Esto incluye `260539 - Evan+Kiri.png` y `humor4.16.png`, cuyos contextos sexualizados deben conservarse. Los cambios de personaje solo se propondrán si son necesarios para resolver una contradicción de canon o una incompatibilidad con el personaje asignado; no se cambiará el contexto sexualizado por defecto.

El detalle de clasificación está en [`2026-08-14_Reuse_Mayo_Unmatched_Review.csv`](2026-08-14_Reuse_Mayo_Unmatched_Review.csv). Las revisiones restantes son técnicas: confirmar copy ambiguo, personaje y canon cuando corresponda, sin bloquear automáticamente la elegibilidad para la prueba.

## 8. Límites de esta revisión

La revisión actual confirma la estructura de Drive, los nombres con referencias y personajes, los tipos de archivo y la clasificación operativa realizada por Fernando. El cruce con Meta recupera fechas y rendimiento para 123 assets, pero no elimina la ausencia de un registro editorial original de mayo: la fecha histórica se obtiene de la publicación encontrada en Meta, no de una ficha de producción. Para los ocho assets sin match se mantiene `Unknown_May_2026`. Antes de programar cada pieza se debe registrar su nuevo `ID_Meta`, fecha de publicación y resultado de métricas.

No se eliminó, movió ni modificó ningún archivo de Drive. La recomendación de descartar significa **excluir temporalmente de la prueba**, no borrar del archivo.

### Referencias

[5]: 2026-08-14_Reuse_Mayo_Meta_Cruce_Datos.csv — Cruce de 205 publicaciones de mayo con adjuntos y candidatos de Drive.
[6]: 2026-08-14_Reuse_Mayo_Ranking.csv — Ranking reproducible de 123 assets con rendimiento histórico.

[1]: ../../GrowthOS/01_03_Reuse_Queue.md — Reglas de antigüedad, canon y prioridades de reuse.
[2]: 2026-08-14_Diseno_Prueba_Calendario_2_Semanas.md — Protocolo de la prueba y necesidad de 28 piezas reuse.
[3]: ../../GrowthOS/05_02_Calendario_04_09_Agosto.md — Piezas de mayo ya usadas o referenciadas en agosto.
[4]: ../../GrowthOS/05_03_Calendario_10_16_Agosto.md — Piezas reuse y cambios de mezcla editorial del 10–16 de agosto.
