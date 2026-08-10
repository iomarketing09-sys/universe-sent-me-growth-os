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
| **Lun 10** | 2608025 — Maeve+Kael — "Casi nos dejamos y lo que teníamos era hambre" | 2608020 — Universe — "Qué gano con mentirte" | **Reuse:** "🥴🤯 escucho borroso..." (21 jul) | TBD |
| **Mar 11** | 2608022 — Evan — "Buscaba algo rico pero no te encontré" | 2608017 — Elara — "Miedo a crecer" | 2608012 — Kiri — "Súper 🍑" | TBD |
| **Mié 12** | 2608024 — Silvio — "Dejaron de buscar a la más bonita" | 2608021 — Kael — "Tus únicas amigas son estas" | **Reuse:** "No es desinterés..." — Fantasma (28 jul) | TBD |
| **Jue 13** | 2608023 — Evan+Kiri — "Qué quieres desayunar" | 2608019 — Maeve — "Te extraño bruja" | 2608014 — Silvio — "Me hubiera encantado ser pobre" | TBD |
| **Vie 14** | 2608016 — Maeve — "Perdón por dormir tanto" | 2608018 — Maeve+Kael — "Lo hice porque si alguien te hace bien" | **Reuse:** "😭🫣 #humoracido #memesUSM" (28 jul) | TBD |
| **Sáb 15** | 2608015 — Universe+Kael — "La asfixiante realidad" | 2608013 — Evan — "De tanto decir soy ese" | **Reuse:** "🫣🫣 #astrologia #retrogrado" (24 jul) — mejor ratio del período (3.31%) | TBD |
| **Dom 16** | Espacio libre (contenido nuevo de la semana) | Espacio libre | Espacio libre | TBD |

## 5. Justificación de los 4 posts de reuse elegidos

Los 4 se tomaron de `08_00_Metricas_Baseline_Plataformas.md` (top 6 de FB por engagement, periodo julio), filtrando por **no haber sido republicados** en el calendario de la semana del 4-8 de agosto (verificado contra el rendimiento real de esa semana ya registrado). Los 2 descartados de ese top 6 ("Si estás leyendo esto...", "Abrazos que curan el alma") quedan disponibles para una futura ronda de reuse.

| Reuse | Fecha original | Impresiones | Engagement | Ratio | Razón de elección |
|---|---|---|---|---|---|
| "🥴🤯 escucho borroso..." | 21 Jul | 175,565 | 3,912 | 2.23% | Top absoluto del período; arranque de semana |
| "No es desinterés..." (Fantasma) | 28 Jul | 173,925 | 3,719 | 2.14% | Segundo mejor; varía personaje (Fantasma) |
| "😭🫣 #humoracido" | 28 Jul | 138,492 | 2,983 | 2.15% | Tercero; formato minimalista puro |
| "🫣🫣 #astrologia #retrogrado" | 24 Jul | 90,723 | 3,002 | **3.31%** | Mejor ratio engagement/impresión de todo el baseline; reservado al día de mejor rendimiento histórico (sábado) |

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
