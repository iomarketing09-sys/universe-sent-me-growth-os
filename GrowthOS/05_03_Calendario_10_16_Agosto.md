---
estado: Aprobado
version: "1.0"
ultima_revision: 2026-08-10
dependencias:
  - GrowthOS/01_00_Arquitectura_Calendario_Escalable.md
  - GrowthOS/08_00_Metricas_Baseline_Plataformas.md
  - Operations/Research/2026-08-08_Reporte_Mensual_Junio_Julio_2026.md
---

# Calendario 10–16 de Agosto 2026 — Nuevo formato: menos reuse, más contenido nuevo

**Propósito:** Documentar el calendario semanal 10-16 agosto y el cambio de estrategia decidido por Fernando: reducir la proporción de memes reutilizados, usar solo los "top" ya validados con datos, y dejar más espacio para contenido nuevo (14 memes nuevos de personajes del elenco extendido: Maeve, Kael, Silvio, Evan, Kiri, Elara, Universe). Reels diarios se mantienen pero quedan como TBD (Fernando define el contenido cada día).
**Estado:** Aprobado
**Fecha de creación:** 2026-08-10
**Última actualización:** 2026-08-10
**Versión:** 1.0
**Autor:** Claude, con dirección de Fernando
**Documentos relacionados:** `08_00_Metricas_Baseline_Plataformas.md` (fuente de los "top reuse"), `Operations/Research/2026-08-08_Reporte_Mensual_Junio_Julio_2026.md` (fuente del análisis horario/día), `01_00_Arquitectura_Calendario_Escalable.md` (reglas de asignación dinámica)

---

## 1. Nota importante sobre alcance de esta sesión

Fernando indicó explícitamente que varias de las 14 piezas nuevas usadas en este calendario **no han pasado por revisión formal de canon** (personajes Maeve/Kael con canon commit aún pendiente en `universe-sent-me-1`; algunos copys de Evan y Universe+Kael que podrían no calzar con sus fichas de diseño actuales). Fernando decidió explícitamente posponer esa revisión a una sesión dedicada, y está considerando invertir el flujo habitual: **dejar que los memes y sus datos de rendimiento alimenten y actualicen la Biblia**, en vez de que la Biblia dicte primero qué se puede publicar. Ese cambio de flujo no se ha decidido ni implementado todavía — queda anotado aquí como contexto de dirección estratégica en discusión, no como cambio de proceso vigente.

## 2. Metodología: cómo se eligieron los horarios

Se analizaron 99 posts individuales de Facebook Orgánico (Windsor.ai, connector `facebook_organic`) de las semanas del 14-20 y 21-27 de julio, con timestamp completo convertido a hora local (México, UTC-6). Se usó **mediana** en vez de promedio como medida principal, porque el promedio queda distorsionado por 3-4 posts virales puntuales que no representan el rendimiento típico de una franja.

**Mejores horas por mediana de interacciones (reacciones+comentarios+shares):**

| Hora | Mediana | n |
|---|---|---|
| 15:00 | 172 | 12 |
| 18:00 | 150 | 9 |
| 20:00 | 91 | 9 |
| 10:00 | 68 | 5 |

**Mejores días por mediana:**

| Día | Mediana | n |
|---|---|---|
| Sábado | 164 | 15 |
| Jueves | 71 | 16 |
| Miércoles | 68 | 11 |

**Nota de discrepancia:** este análisis (volumen/mediana de interacciones absolutas) posiciona el sábado como el día más fuerte, mientras que `05_02_Calendario_04_09_Agosto.md` había marcado el domingo como "Mayor Engagement — 1.77% ER". Ambas cifras pueden ser correctas simultáneamente porque miden cosas distintas: **ER (engagement rate) normaliza por alcance/impresiones**, mientras que este análisis mide **volumen absoluto de interacciones por mediana**. Un día puede tener menos posts o menor alcance total pero mejor proporción de quienes vieron el post y reaccionaron. Ambas métricas quedan documentadas; no se resuelve la discrepancia aquí — queda como nota para una futura sesión de métricas.

## 3. Estructura de slots (4 por día)

10:00 AM · 3:00 PM · 6:00 PM · Reel diario (horario variable, TBD por Fernando)

## 4. Calendario completo

| Día | 10:00 AM | 3:00 PM | 6:00 PM | Reel diario |
|---|---|---|---|---|
| **Lun 10** | 2608025 — Maeve+Kael — "Casi nos dejamos y lo que teníamos era hambre" | 2608020 — Universe — "Qué gano con mentirte" | **Reuse (mayo):** Carrusel "Los cambios de tema que tengo en una sola conversación" (4 may, 242,400 alcance) | TBD |
| **Mar 11** | 2608022 — Evan — "Buscaba algo rico pero no te encontré" | 2608017 — Elara — "Miedo a crecer" | 2608012 — Kiri — "Súper 🍑" | TBD |
| **Mié 12** | 2608024 — Silvio — "Dejaron de buscar a la más bonita" | 2608021 — Kael — "Tus únicas amigas son estas" | **Reuse (mayo):** Escena "Pásame tu pack" (4 may, 159,000 alcance) | TBD |
| **Jue 13** | 2608023 — Evan+Kiri — "Qué quieres desayunar" | 2608019 — Maeve — "Te extraño bruja" | 2608014 — Silvio — "Me hubiera encantado ser pobre" | TBD |
| **Vie 14** | 2608016 — Maeve — "Perdón por dormir tanto" | 2608018 — Maeve+Kael — "Lo hice porque si alguien te hace bien" | **Reuse (mayo):** Meme "No olvides las 3 vrg" (16 may, 138,700 alcance) | TBD |
| **Sáb 15** | 2608015 — Universe+Kael — "La asfixiante realidad" | 2608013 — Evan — "De tanto decir soy ese" | **Reuse (mayo):** Carrusel "Ronroneo para el amigo / Navajazo para el enemigo" (14 may, 110,900 alcance) | TBD |
| **Dom 16** | Espacio libre (contenido nuevo de la semana) | Espacio libre | Espacio libre | TBD |

## 5. Justificación de los 4 posts de reuse elegidos

**Corrección (2026-08-10):** la primera versión de este documento tomó los 4 reuse del baseline de julio (`08_00_Metricas_Baseline_Plataformas.md`) por error. Fernando aclaró que el reuse debe salir específicamente del inventario de mayo ya procesado (`Operations/Memories/mayo_2026_top_posts_metaBS.md`, 12 posts con datos reales de Meta Business Suite, y su índice asociado `01_03_Reuse_Queue.md`). Esta sección queda corregida con la fuente correcta.

Los 4 se tomaron del ranking de alcance real de mayo, siguiendo las prioridades que el propio reporte declara ("PRIORIDAD MÁXIMA: carruseles multi-escena", "PRIORIDAD ALTA: memes de gato con lentes en múltiples escenarios"), y verificando que **no se hayan republicado ya en el ciclo reciente** — el post #6 del ranking ("Amor ya estoy lleno" + "Bruce Bruce Bruce") se excluyó por ya haber aparecido en el calendario de la semana del 4-8 de agosto.

| Reuse (mayo) | Fecha original | Alcance | Likes | Compartidos | Razón de elección |
|---|---|---|---|---|---|
| Carrusel "Los cambios de tema..." | Lun 4 may | **242,400** | 1,700 | 1,300 | #1 histórico del proyecto; prioridad máxima declarada; lunes es día óptimo confirmado en el propio reporte |
| Escena "Pásame tu pack" | Lun 4 may | **159,000** | 1,700 | 253 | #3 histórico; formato de escena con personajes |
| Meme "No olvides las 3 vrg" | Sáb 16 may | **138,700** | 1,500 | 755 | #4 histórico; formato "gato con lentes en escenario", prioridad alta declarada |
| Carrusel "Ronroneo/Navajazo" | Jue 14 may | **110,900** | 786 | 457 | #5 histórico; mismo formato de gato con lentes; reservado al día de mejor rendimiento reciente (sábado) |

Quedan disponibles para una futura ronda, sin usar todavía: #2 "La mente del wey que lee de todo..." (176,800 alcance) y #7 "Adivina kien anda bien caliente" (31,700 alcance).

## 6. Balance de personajes (14 piezas nuevas)

| Personaje | Apariciones |
|---|---|
| Maeve+Kael (dúo) | 2 |
| Silvio | 2 |
| Evan | 2 |
| Maeve | 2 |
| Evan+Kiri | 1 |
| Kael | 1 |
| Universe | 1 |
| Universe+Kael | 1 |
| Elara | 1 |
| Kiri | 1 |

Distribución natural sin sobrecarga de ningún personaje individual — no requirió ajuste manual.

## 7. Cambio de estrategia registrado

Por instrucción explícita de Fernando: a partir de esta semana se **reduce la proporción de contenido reutilizado** a un máximo de 1 pieza de reuse por día (solo piezas "top" ya validadas por datos), dejando el resto del calendario para contenido nuevo. Se mantienen los Reels diarios como formato fijo, con contenido definido día a día por Fernando (no preasignado en este documento).

## 8. Pendiente para sesión futura (no resuelto aquí)

1. Revisión de canon de las 14 piezas nuevas (especialmente 2608013-Evan y 2608015-Universe+Kael, señaladas como las de mayor desviación aparente de sus fichas de diseño actuales).
2. Corrección de typo visible en 2608012 (Kiri): dice "qlho" en vez de "culo" en el texto de la imagen.
3. Discusión de fondo sobre invertir el flujo canon↔contenido: usar datos de rendimiento de memes para informar/actualizar la Biblia, en vez de que la Biblia filtre primero qué se produce.
4. Resolver la discrepancia de metodología entre "mejor día por ER%" (domingo, según `05_02_Calendario_04_09_Agosto.md`) vs. "mejor día por mediana de volumen" (sábado, según este documento).
5. Canon commit formal de Maeve y Kael en `universe-sent-me-1` (ya señalado como pendiente en sesiones anteriores).
