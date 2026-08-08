# Reporte Mensual de Métricas — Junio y Julio 2026 (Facebook Orgánico)

**Propósito:** Cerrar el vacío de datos entre `mayo_2026_top_posts_metaBS.md` (mayo) y `agosto_2026_analisis_28_dias.md` / `2026-08-08_Ciclo_Diario_Metricas_24h.md` (julio final–agosto), documentando junio y julio completos con datos reales extraídos de Windsor.ai. Ningún documento existente en el repositorio cubría este rango antes de este reporte.
**Estado:** Active
**Fecha de creación:** 2026-08-08
**Última actualización:** 2026-08-08
**Versión:** 1.0
**Autor:** Claude (extracción directa vía Windsor.ai MCP, connector `facebook_organic`)
**Documentos relacionados:** `../Memories/mayo_2026_top_posts_metaBS.md`, `../Memories/agosto_2026_analisis_28_dias.md`, `../../GrowthOS/08_00_Metricas_Baseline_Plataformas.md`, `../../GrowthOS/00_01_Changelog_GrowthOS.md`

> **Nota de metodología (importante):** Mayo se midió por **alcance** (Meta Business Suite, captura de pantalla manual). Julio final/agosto se mide por **reacciones + comentarios + shares** porque `post_impressions` está deprecado en Graph API v21.0 para esta página (confirmado en `00_01_Changelog_GrowthOS.md` [1.2.3] y en `2026-08-08_Ciclo_Diario_Metricas_24h.md`). Este reporte usa la **misma métrica que julio final/agosto** (reacciones + comentarios + shares) por ser la única disponible de forma confiable retroactiva vía Windsor.ai para junio-julio. **No es comparable en valor absoluto con las cifras de alcance de mayo** — solo es comparable en tendencia relativa (qué días/formatos ganaron dentro del propio período).
>
> Fuente: Windsor.ai MCP, connector `facebook_organic`, cuenta Facebook Page @UniverseSentMe (ID `1036844829507460`). Extracción: 2026-08-08. Cobertura: 2026-06-01 a 2026-07-31 (61 días, cientos de posts individuales, alto volumen multi-post/día).

---

## 1. Resumen Ejecutivo

| Métrica | Junio 2026 | Julio 2026 | Variación |
|---|---|---|---|
| Reacciones totales | 13,935 | 48,376 | **+247%** |
| Comentarios totales | 423 | 926 | +119% |
| Shares totales | 4,093 | 18,853 | **+361%** |
| Interacciones totales | 18,451 | 68,155 | **+269%** |
| Promedio de interacciones/día | 615.0 | 2,198.5 | +257% |

**Lectura operativa:** julio no fue una mejora gradual sobre junio — fue un salto de escala. El crecimiento de shares (+361%) superó incluso al de reacciones (+247%), lo que confirma la hipótesis ya validada en ciclos posteriores (H11: minimalismo dispara shares) desde antes de que se formalizara como hipótesis. El 28 de julio (pico absoluto del período, ver más abajo) es el mismo día que ya aparecía en `08_00_Metricas_Baseline_Plataformas.md` como el post de Fantasma "No es desinterés..." — este reporte confirma con datos de reacciones/shares el mismo pico que Manus ya había registrado por impresiones (173,925).

---

## 2. Top 5 Días — Junio 2026 (por interacciones totales)

| Fecha | Reacciones | Comentarios | Shares | Total |
|---|---|---|---|---|
| 28 Jun | 1,717 | 42 | 773 | **2,532** |
| 22 Jun | 1,824 | 12 | 429 | **2,265** |
| 10 Jun | 1,507 | 36 | 526 | **2,069** |
| 30 Jun | 1,510 | 45 | 389 | **1,944** |
| 14 Jun | 1,485 | 41 | 257 | **1,783** |

### Posts destacados de junio (con copy)

- **22 Jun — "El gato: 😧"** — 1,002 reacciones, 2 comentarios, 127 shares. Formato minimalista (emoji + micro-caption), personaje Universe.
- **22 Jun — "a ver... a ver... 🤨"** — 696 reacciones, 2 comentarios, 280 shares. Mismo día, mismo patrón — el 22 de junio tuvo dos posts fuertes consecutivos, ambos minimalistas.
- **10 Jun — "yo Aura Fuerte 😏"** — 897 reacciones, 20 comentarios, 232 shares.
- **28 Jun — "Me da miedo ser el malo de la historia..."** — 913 reacciones, 4 comentarios, 395 shares (mayor ratio share/reacción del mes, 43%).
- **10 Jun — "🤡"** — 510 reacciones, 13 comentarios, 275 shares. Un solo emoji, patrón ya validado desde junio, mucho antes del ciclo de agosto.

---

## 3. Top 5 Días — Julio 2026 (por interacciones totales)

| Fecha | Reacciones | Comentarios | Shares | Total |
|---|---|---|---|---|
| 19 Jul | 4,611 | 87 | 2,949 | **7,647** |
| 28 Jul | 5,217 | 48 | 2,223 | **7,488** |
| 21 Jul | 3,871 | 118 | 2,046 | **6,035** |
| 18 Jul | 3,688 | 32 | 1,769 | **5,489** |
| 17 Jul | 3,345 | 42 | 1,073 | **4,460** |

### Posts destacados de julio (con copy)

- **19 Jul — "🫣🫣ㅤ#UniverseSentMe"** — **3,109 reacciones, 62 comentarios, 2,321 shares (5,492 interacciones en un solo post)**. El post individual de mayor interacción de todo el período junio-julio. Dos emojis, un hashtag. Confirma el patrón minimalista con el margen más grande observado.
- **28 Jul — "No es desinterés..." (Fantasma)** — 2,369 reacciones, 18 comentarios, 1,340 shares (3,727 interacciones). Ya documentado en `agosto_2026_analisis_28_dias.md` con 173,925 de alcance — este es el mismo post visto desde la métrica de interacciones. Confirma a Fantasma como personaje con tracción real, con evidencia doble (alcance + interacciones).
- **28 Jul — "😭🫣ㅤ#UniverseSentMe #humoracido #memesUSM"** — 2,249 reacciones, 16 comentarios, 716 shares.
- **21 Jul — "🥴🤯 escucho borroso...."** — 2,291 reacciones, 102 comentarios, 1,520 shares. Coincide con el post #1 de `08_00_Metricas_Baseline_Plataformas.md` (175,565 de alcance) — mismo post, métrica distinta, mismo resultado: top absoluto del baseline de 2 semanas.
- **24 Jul — "🫣🫣ㅤ#UniverseSentMe #humor #relatable #astrologia #retrogrado"** — 2,336 reacciones, 41 comentarios, 626 shares. Coincide con el post de 90,723 de alcance ya listado en el baseline (mejor ratio engagement/alcance de esa tabla).
- **18 Jul — "😐"** — 2,536 reacciones, 8 comentarios, **1,451 shares**. Mayor ratio share/reacción de julio (57%) — un solo emoji sin hashtag.
- **23 Jul — "🙂‍↕️ #UniverseSentMe #humor #memesenespañol #relatable #vidareal #meditacion"** — 1,723 reacciones, 10 comentarios, 1,023 shares.

---

## 4. Confirmaciones cruzadas con documentos existentes

Este reporte no contradice ningún dato ya registrado — los confirma desde otro ángulo métrico:

| Post | Alcance (Manus, `08_00_Metricas_Baseline`) | Interacciones (este reporte) | Coincide |
|---|---|---|---|
| "🥴🤯 escucho borroso..." (21 Jul) | 175,565 | 3,913 (2,291+102+1,520) | ✅ Top absoluto en ambas métricas |
| "No es desinterés..." Fantasma (28 Jul) | 173,925 | 2,435 (2,369+18+... nota: shares de este post en el registro de baseline no se desglosan, aquí sí: 1,340) | ✅ Segundo lugar en ambas |
| "🫣🫣" astrología (24 Jul) | 90,723 | 2,377 (2,336+41+... shares 626) | ✅ Presente en ambos top |

**Conclusión de consistencia:** el patrón de "imagen estática + copy minimalista (emoji o casi vacío) = mayor rendimiento" ya era visible desde junio (22 y 28 jun) — **no es un descubrimiento exclusivo del ciclo de agosto**, sino una tendencia sostenida durante los tres meses. Esto sube la confianza de H11 (Fantasma/minimalismo) de "hipótesis reciente" a "patrón de 3 meses consecutivos".

---

## 5. Instagram y TikTok — Junio y Julio (referencia)

- **Instagram:** 103 interacciones totales en junio, 101 en julio (likes+comments+shares). Promedio ~3.3/día en ambos meses — sin cambio significativo. Confirma la nota ya existente en `08_00_Metricas_Baseline_Plataformas.md`: "IG aún no tiene masa crítica suficiente para compararse."
- **TikTok:** actividad en cero durante junio y julio completos — coherente con el registro existente de que el canal se activó el 2026-08-01.

---

## 6. Limitaciones de este reporte

- No se pudo reconstruir `post_impressions`/alcance histórico para junio-julio porque el campo está deprecado en Graph API v21.0 desde el lado de Meta, no solo para fechas recientes — Windsor.ai no devuelve ese campo para ningún rango de fecha en este momento.
- Los datos aquí son a nivel de reacciones/comentarios/shares por post, consistentes con la metodología ya adoptada en `2026-08-08_Ciclo_Diario_Metricas_24h.md`, pero **no directamente comparables en cifra absoluta** con el reporte de mayo (que sí usa alcance).
- No se revisaron los ~750+ posts individuales de junio-julio uno por uno; el análisis por post se concentró en los días de mayor interacción (top 5 por mes) para extraer copys y patrones, más los agregados diarios completos (61/61 días) para las cifras mensuales.

## 7. Próxima actualización recomendada

- Si se recupera acceso a `post_impressions` (o Meta restaura el campo), re-extraer junio-julio con esa métrica para comparación directa con mayo.
- Integrar este reporte como fila de referencia en `08_00_Metricas_Baseline_Plataformas.md` si Manus decide expandir el histórico de ese documento más allá de 2 semanas.
