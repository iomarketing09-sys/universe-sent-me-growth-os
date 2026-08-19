# Métricas Baseline — Facebook, Instagram, TikTok & YouTube (Universe Sent Me)

**Propósito:** Registro de métricas reales extraídas de Windsor.ai y Meta. Fuente de verdad para comparaciones de rendimiento, calibración de hipótesis y decisiones de canal en Facebook, Instagram, TikTok y YouTube. No es un resumen de sesión — es un documento vivo que debe actualizarse con cada ciclo de análisis.
**Estado:** Active
**Fecha de creación:** 2026-08-03
**Última actualización:** 2026-08-19
**Versión:** 2.0
**Autor:** Claude (Guardián de Canon, extracción directa vía Windsor.ai MCP)
**Documentos relacionados:** `07_00_Registro_Maestro_Reels.md`, `06_00_Reglas_Aprendizaje_Tendencias.md`, `01_00_Arquitectura_Calendario_Escalable.md`, `14_00_Fuente_Maestra_y_Ledgers.md`, `../Operations/Research/Historical_Performance_Snapshot.csv`, `../Operations/Research/Historical_Performance_Individuals.csv`, `../Operations/Research/2026-08-15_Publication_Log.csv`, `../Operations/Research/2026-08-15_ExperimentLog.csv`, `../Operations/Research/2026-08-16_P2_Comunidad_Delta_01.json`, `../Operations/Research/2026-08-16_P2_Baseline_Preparacion_01.json`, `../Operations/Research/2026-08-17_Metricas_24_72_Extraccion_02.json`, `../Operations/Research/2026-08-17_Investigacion_Ventanas_Temporales_Meta.md`, `../Operations/Research/2026-08-19_Social_Performance_28D_Normalizado.json`

> **Metodología:** Este documento conserva snapshots históricos y cortes reproducibles. El corte multicanal más reciente fue extraído desde Windsor.ai el 2026-08-19 para el período 22 de julio–18 de agosto de 2026. Cuentas: Facebook Page `1036844829507460`, Instagram `17841462696378190`, TikTok `Universe Sent Me` (`_000bYPIECRpRjubuhKmzaeo3iFDirTBYXPP`) y YouTube `Universe Sent Me` (`UCBNbmSB3QG73ef7EqN2Ew1A`, conectado en Windsor como account `27679`). Los snapshots históricos anteriores no se sobrescriben; cada fila conserva fuente, fecha de extracción y ventana.

---

## 1. Diagnóstico General de Plataformas

| Métrica | Facebook | Instagram |
|---|---|---|
| Rango de alcance típico (post) | 1,000 – 175,000 | 0 – 242 |
| Rango de engagement típico | 10 – 4,000 | 0 – 19 |
| Formato dominante | Imagen estática | Reel |
| Mejor ratio engagement/alcance | Imágenes con emoji mínimo y copy relatable | Reels con alto % de no-seguidores |
| Estado del canal | **Principal activo del estudio** | En desarrollo — alcance muy bajo todavía |

**Conclusión operativa:** Facebook es el motor principal de distribución orgánica. Instagram aún no tiene masa crítica suficiente para compararse. Toda decisión de prioridad de producción debe partir de esta diferencia.

---

## 2. Top 10 — Facebook (últimas 2 semanas, por impresiones)

| Fecha | Copy / Concepto | Tipo | Impresiones | Engagement | Reacciones | Ratio Eng/Imp |
|---|---|---|---|---|---|---|
| 21 Jul | "🥴🤯 escucho borroso..." | Imagen | 175,565 | 3,912 | 2,290 | **2.23%** |
| 28 Jul | "No es desinterés..." (Fantasma) | Imagen | 173,925 | 3,719 | 2,366 | **2.14%** |
| 28 Jul | "😭🫣 #humoracido #memesUSM" | Imagen | 138,492 | 2,983 | 2,252 | **2.15%** |
| 24 Jul | "🫣🫣 #astrologia #retrogrado" | Imagen | 90,723 | 3,002 | 2,335 | **3.31%** ← mejor ratio |
| 01 Ago | "Si estás leyendo esto..." | Imagen | 83,918 | 1,074 | 667 | **1.28%** |
| 28 Jul | "Abrazos que curan el alma" | Imagen | 84,317 | 663 | 511 | **0.79%** |
| 27 Jul | "☺️😊 #memesUSM #humor" | Imagen | 48,050 | 1,019 | 901 | **2.12%** |
| 21 Jul | "Me encanta bruce lee..." | Imagen | 46,004 | 1,694 | 1,279 | **3.68%** ← mejor ratio |
| 31 Jul | "No todos los hadas dan flores" (Kiri) | Imagen | 24,480 | 501 | 401 | **2.05%** |
| 23 Jul | "🙂‍↔️ #memesenespañol" | Imagen | 69,925 | 2,754 | 1,723 | **3.94%** ← mejor ratio |

**Patrón visible:** El top 10 es 100% imagen estática. Los posts con emoji como protagonista único del copy (`🥴🤯`, `🫣🫣`, `😭🫣`, `☺️😊`) generan alcance masivo. El Fantasma ya tiene presencia en el top 10 orgánico.

---

## 3. Reels en Facebook — Rendimiento real (últimas 2 semanas)

| Fecha | Concepto | Impresiones | Engagement | Ratio |
|---|---|---|---|---|
| 25 Jul | "Dicen que si lo ves caminando..." (Fantasma) | 6,907 | 42 | 0.61% |
| 24 Jul | "Cultiva la paz interior..." (Bosque) | 4,517 | 16 | 0.35% |
| 30 Jul | "Mi gato sabe hacer de todo..." | 1,073 | 4 | 0.37% |
| 02 Ago | "Muros vemos, inbox no sabemos" (Wilfred) | 612 | 4 | 0.65% |
| 29 Jul | "Rock gótico vs Juan Gabriel" | 777 | 3 | 0.39% |
| 27 Jul | "Mi ascenso a la locura" | 657 | 7 | 1.07% |
| 29 Jul | "Wilfred en el bosque" | 523 | 1 | 0.19% |
| 21 Jul | "El verdadero terror psicológico" | 979 | 3 | 0.31% |
| 03 Ago | "El Bucle del Fantasma" *(estreno hoy)* | 118 | 1 | — *(demasiado temprano)* |

**Brecha imagen vs Reel en Facebook:** Los Reels obtienen entre 10× y 100× menos impresiones que las imágenes estáticas comparables en la misma página. El mejor Reel del período (Fantasma caminando, 6,907 impresiones) queda por debajo del percentil 50 de las imágenes estáticas.

> **Hipótesis a validar:** El algoritmo de Facebook favorece imagen sobre Reel para esta cuenta específica en esta etapa de crecimiento. Puede cambiar si los Reels acumulan más tiempo de visualización. Registrar esta hipótesis en `HypothesisBank` cuando exista.

---

## 4. Instagram — Rendimiento real (últimas 2 semanas)

| Fecha | Concepto | Tipo | Alcance | Vistas | Engagement |
|---|---|---|---|---|---|
| 24 Jul | "Cultiva la paz interior" | Reel | 242 | 343 | 19 |
| 21 Jul | "El verdadero terror psicológico" | Reel | 108 | 156 | 3 |
| 30 Jul | "Mi gato sabe hacer de todo" | Reel | 115 | 139 | 5 |
| 27 Jul | "Mi ascenso a la locura" | Reel | 106 | 124 | 2 |
| 25 Jul | "Dicen que si lo ves caminando" (Fantasma) | Reel | 124 | 141 | 7 |
| 01 Ago | "Si estás leyendo esto..." | Imagen | 3 | 8 | 2 |
| 29 Jul | "Rock gótico vs Juan Gabriel" | Reel | 56 | 77 | 1 |
| 03 Ago | "El Bucle del Fantasma" *(estreno hoy)* | Reel | 7 | 6 | 0 |

**Estado del canal IG:** Alcance promedio de 50–242 personas por pieza. El canal todavía no tiene masa crítica. Los Reels funcionan mejor que las imágenes en IG (a diferencia de FB), pero los números absolutos son muy bajos. No usar IG como referencia de rendimiento hasta que el alcance promedio supere las 500 personas por pieza de forma consistente.

---

## 5. Insights Clave para Producción (extraídos de los datos)

1. **Emoji solo como copy = alcance masivo en FB.** Los posts con solo uno o dos emojis y hashtags cortos generan el mayor alcance orgánico. La audiencia de Facebook responde mejor a lo visual-inmediato que a copy elaborado.

2. **Fantasma tiene tracción orgánica en FB.** "No es desinterés" (173K) y la referencia previa del Reel de Fantasma caminando (6.9K Reels, que para un Reel es el techo del período) confirman que este personaje resuena. "El Bucle del Fantasma" debe monitorearse las próximas 48–72h para confirmar o descartar.

3. **El copy largo no penaliza pero tampoco amplifica.** "No todos los hadas dan flores..." (Kiri, 260 palabras de copy) logró 24K impresiones — mejor que cualquier Reel, pero muy por debajo de los posts de imagen con emoji. El CTA ("Cuéntamelo en los comentarios") sí generó interacción en comentarios.

4. **Los Reels no son el formato ganador en FB todavía.** Ningún Reel del período supera las 7K impresiones en FB. Las imágenes más modestas del período superan eso con facilidad. Esto no significa que los Reels sean inútiles — construyen identidad visual del universo — pero no son el motor de alcance en esta etapa.

5. **IG requiere estrategia diferenciada.** No se puede usar la misma pieza en FB e IG y esperar resultados similares. Los Reels tienen mejor desempeño proporcional en IG que las imágenes. Pendiente definir cuándo IG justifica producción dedicada.

---

## 6. Métricas de Monetización (Mercado Libre)

| Métrica | Meta (Q3 2026) | Estado Actual | Fuente |
|---|---|---|---|
| Clics en Afiliado (Mensual) | 5,000 | 0 | ML Dashboard / Bitly |
| Tasa de Conversión (CR) | 1.5% | 0% | ML Dashboard |
| Ingresos Afiliados | $500 USD | $0 | ML Dashboard |
| Vistas en ML Clips | 10,000 | 0 | ML App |

**Nota operativa:** Estas métricas se integrarán en el reporte semanal a partir de la primera publicación del formato "¿Qué me llegó?".

---

## 7. Diseño de actualización de baseline común

La baseline común debe permitir comparar Facebook e Instagram sin mezclar magnitudes, formatos ni ventanas temporales incompatibles. Las cifras históricas de las secciones anteriores se conservan como snapshot Windsor.ai del 3–5 de agosto; no se sobrescriben con datos parciales del lote 15–16.

| Campo de actualización | Regla |
|---|---|
| `Periodo` | Cohorte explícita: junio, julio, agosto o ventana aprobada. |
| `Plataforma` | `Facebook` e `Instagram` siempre separados; nunca sumar alcance entre canales. |
| `Formato` | `Imagen`, `Reel`, `Carrusel` u otro formato real. |
| `N_publicaciones` | Solo publicaciones con Meta ID o fuente histórica verificable. |
| `Interacciones` | Definición constante por cohorte; documentar si es reacciones + comentarios + shares. |
| `Alcance_o_Impresiones` | Mantener el campo original de la fuente; no convertir impresiones en alcance. |
| `Mediana_por_publicacion` | Mediana de la métrica principal dentro de la cohorte, no promedio de promedios. |
| `Comentarios_totales` | Total de comentarios reales; separar etiquetas automáticas y comentarios cualitativos usando el Community Engagement Log. |
| `Ventana` | `Lifetime`, `24h_snapshot`, `72h_snapshot` o `Historico`; no comparar ventanas distintas sin marcarlo. |
| `Fuente` | Windsor.ai, Meta Graph API, Publication Log o ExperimentLog, con fecha de extracción. |
| `Estado` | `Historico`, `Parcial`, `Validado_24h`, `Validado_72h` o `Snapshot_No_Disponible`. |

La próxima actualización numérica deberá unir `Content_Inventory.csv`, `Publication_Log.csv` y `ExperimentLog.csv` por `CNT-####` y Meta ID. Para el lote 15–16 se incorporarán las nueve publicaciones solo cuando existan ventanas válidas. La extracción del 15 de agosto encontró cero ventanas elegibles; la revisión P0 del 17 de agosto encontró cuatro ventanas 24h elegibles, pero Meta devolvió únicamente totales lifetime, por lo que no se añadieron métricas prematuras.

El reporte comparará por separado: (a) frecuencia y mediana de interacciones por publicación; (b) Facebook imagen frente a Facebook Reel; (c) Instagram Reel frente a Instagram imagen; (d) contenido nuevo frente a reuse; y (e) comentarios totales frente a comentarios cualitativos. Facebook seguirá siendo el canal principal de distribución en la lectura actual, mientras Instagram se evaluará como canal en desarrollo y no se presentará como fracaso por sus volúmenes absolutos todavía pequeños.

No se emitirá un veredicto de canal hasta completar el lote de métricas y armonizar las definiciones de interacción. La baseline común es un marco de comparación, no una autorización para mezclar los numeradores de Facebook e Instagram.

## 8. Control P2 de preparación — 16 de agosto de 2026

La auditoría de preparación se ejecutó sobre los identificadores de observación `OBS-FB-15_16-*` y `OBS-IG-15_16-*`, evitando contar filas históricas que comparten `Experiment_ID`. El lote contiene **12 observaciones**: nueve de Facebook y tres de Instagram. Las nueve publicaciones activas de Facebook tienen Meta ID, pero **0/9** tienen `Interacciones_24h` y **0/9** tienen `Interacciones_72h`; las tres filas de Instagram están documentadas como operación o excluidas del aprendizaje activo. Por ello, la baseline común no se actualiza numéricamente en esta revisión.

| Control | Resultado | Decisión |
|---|---:|---|
| Observaciones del lote 15–16 | 12 | Separar por plataforma. |
| Facebook activo | 9 | Mantener pendiente de métricas 24/72h. |
| Instagram activo para aprendizaje | 0 | No mezclar filas eliminadas; conservar trazabilidad. |
| Snapshots 24h válidos | 0 | No escribir métricas. |
| Snapshots 72h válidos | 0 | No escribir métricas. |
| Actualización numérica de baseline | No ejecutada | Esperar el cierre P0 del extractor. |

La siguiente actualización numérica debe ejecutarse después de que el extractor de 48 horas produzca snapshots válidos para Facebook. La comunidad se mide por separado mediante `Community_Engagement_Log.csv`; sus comentarios vacíos, menciones automáticas y la respuesta puntual no se mezclan con las métricas 24/72h.

## 9. Resultado P0 de extracción — 17 de agosto de 2026

La extracción oficial se ejecutó en un solo lote a las `2026-08-17T03:37:53Z`, usando la tarea `EXP-2026-08-CAL-01`. Evaluó nueve publicaciones de Facebook del 15–16; cuatro ya habían cumplido 24 horas (`CNT-031` a `CNT-034`) y cinco todavía no. Meta respondió HTTP 200 para las cuatro consultas, pero solo entregó totales acumulados lifetime. Conforme a la regla P0, esos totales se conservaron como evidencia y no se escribieron en `Interacciones_24h` ni `Interacciones_72h`.

| Asset | Ventana elegible | Lifetime reacciones | Lifetime comentarios | Lifetime shares | Lifetime interacciones | Métrica 24h escrita |
|---|---|---:|---:|---:|---:|---|
| `CNT-031` / `2608030` | 24h | 96 | 2 | 23 | 121 | No |
| `CNT-032` / `2608033` | 24h | 52 | 1 | 20 | 73 | No |
| `CNT-033` / `2608034` | 24h | 35 | 7 | 10 | 52 | No |
| `CNT-034` / `2608035` | 24h | 53 | 3 | 14 | 70 | No |

**Resultado P0:** `4/9` publicaciones tenían una ventana 24h elegible; `0/4` devolvieron un snapshot exacto; `0` campos 24h/72h fueron escritos. Instagram no fue tocado, no se publicó contenido y la baseline común no se actualiza numéricamente todavía. La evidencia completa está en `Operations/Research/2026-08-17_Metricas_24_72_Extraccion_02.json`. El diagnóstico y la solución propuesta para futuras capturas están en `Operations/Research/2026-08-17_Investigacion_Ventanas_Temporales_Meta.md`.

## 10. Corte observado del lote 15–16 — 17 de agosto de 2026

Se ejecutó una revisión agrupada de lectura a las `2026-08-17T04:25:10.797397Z` sobre las nueve publicaciones activas de Facebook. El corte recuperó 370 reacciones, 23 comentarios y 109 shares, para 502 interacciones observadas. La evidencia detallada, la edad de cada post y los 23 comentarios recuperados están en `Operations/Research/2026-08-17_Corte_Observado_15_16.json` y `Operations/Research/2026-08-17_Reporte_Corte_Observado_15_16.md`.

Este corte es operativo y descriptivo: no reemplaza snapshots exactos de 24/72 horas, no actualiza `Interacciones_24h` ni `Interacciones_72h` y no cierra hipótesis. Los comentarios se conservan como señal cualitativa separada de la baseline numérica.

## 11. Snapshot histórico mensual integrado — 17 de agosto de 2026

Se integró `Operations/Research/Historical_Performance_Snapshot.csv` como capa histórica separada. Contiene agregados de junio y julio por plataforma, además de un snapshot de los 12 top posts de Facebook disponibles para mayo. Mayo no se presenta como total mensual porque la fuente es una captura de top posts de Meta Business Suite, no un extracto mensual completo.

| Periodo | Plataforma | Cobertura | Métrica principal | Valor | Estado |
|---|---|---|---|---:|---|
| Mayo 2026 | Facebook | Top 12 posts | Alcance acumulado del snapshot | 933,016 | Histórico; tendencia relativa |
| Junio 2026 | Facebook | Mes completo | Interacciones | 18,451 | Histórico |
| Julio 2026 | Facebook | Mes completo | Interacciones | 68,155 | Histórico |
| Junio 2026 | Instagram | Mes completo | Interacciones | 103 | Histórico; tendencia interna IG |
| Julio 2026 | Instagram | Mes completo | Interacciones | 101 | Histórico; tendencia interna IG |

Estos valores no se escriben en `Interacciones_24h`, `Interacciones_72h` ni en los ledgers operativos. Tampoco se suman alcance de mayo con interacciones de junio-julio. La tabla sirve para contexto de tendencia, selección de reuse y formulación de hipótesis.

El lote individual 02 añade 28 filas verificables del ranking de reuse de mayo y 11 top posts de junio-julio en `Historical_Performance_Individuals.csv`. Cada fila conserva Meta ID, fecha, fuente y definición métrica; no recibe CNT automáticamente y no se incorpora al Publication Log operativo.

## 12. Corte multicanal de 28 días — 22 de julio a 18 de agosto de 2026

Este corte incorpora por primera vez TikTok y YouTube al mismo marco analítico. Los números se muestran juntos para facilitar la lectura operativa, pero **no deben sumarse como una audiencia total ni ordenarse como si las plataformas compartieran la misma definición de view, reach o engagement**.

| Plataforma | Contenido deduplicado | Views observadas | Reach | Engagement normalizado | Mediana de engagement | Crecimiento |
|---|---:|---:|---:|---:|---:|---|
| Instagram | 34 piezas | 1,646 | 1,216 | 59 | 1 | No disponible en el corte |
| TikTok | 7 videos | 2,268 | 2,188 | 23 | 3 | 2 seguidores ganados |
| YouTube | 6 videos únicos / 24 filas diarias | 5,022 views diarias | No aplica | 36 likes | 0 | 10 suscriptores ganados / 1 perdido |

### 12.1 Reglas de integración

El dashboard debe tener una vista ejecutiva por plataforma y una vista de contenido. La vista ejecutiva presenta volumen publicado, views observadas, reach cuando exista, engagement normalizado, crecimiento de audiencia y tendencia. La vista de contenido conserva una fila por `content_id` para Instagram y TikTok; YouTube conserva además una tabla diaria separada porque Windsor entrega actividad por video y día.

| Campo común | Instagram | TikTok | YouTube |
|---|---|---|---|
| `content_id` | `media_id` | `video_id` | `video` |
| `published_at` | `timestamp` | `video_create_datetime` | Debe recuperarse del catálogo/video; no usar `date` diaria como fecha de publicación |
| `views` | `media_views` | `video_views_count` | `views` diario; `video_view_count` como snapshot lifetime |
| `reach` | `media_reach` | `video_reach` | No usar si no existe; no sustituirlo por views |
| `engagement` | `media_engagement` | likes + comments + shares + favorites cuando no exista nativo | likes + comments + shares en la fila diaria |
| Retención | `media_reel_avg_watch_time` para Reels | `video_average_time_watched`, `video_full_watched_rate` | `average_view_duration`, `average_view_percentage` |
| Audiencia ganada | No disponible en este corte | `video_new_followers` | `subscribers_gained` y `subscribers_lost` |
| Ventana | `lifetime_current_snapshot` | `lifetime_current_snapshot` | `daily_observed_activity` y `lifetime_current_snapshot` separados |

TikTok entregó filas repetidas con métricas nulas para un mismo video; el normalizador conserva la fila con mayor cobertura de campos y deduplica por `video_id`. YouTube devuelve varias filas diarias para el mismo video; el dashboard no debe sumar `video_view_count` repetido. Facebook conserva su métrica canónica histórica `reacciones + comentarios + shares`, mientras Windsor `post_engagements` queda como métrica alternativa por su definición diferente.

El dataset reproducible del corte está en `Operations/Research/2026-08-19_Social_Performance_28D_Normalizado.json`. La fuente de arquitectura, roles y reglas de no duplicación está en `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`.

## 13. Próxima Actualización

Este documento debe actualizarse:
- Cada domingo (ciclo semanal de análisis)
- Después de publicar cualquier pieza con distribución en más de una plataforma
- Cuando se cierren hipótesis en el HypothesisBank

Herramienta de extracción histórica: MCP → connectors `facebook_organic`, `instagram`, `tiktok_organic` y `youtube`; Meta Graph API v26 + `Publication_Log.csv` para identidad, publicación y reconciliación. Campos normalizados del dashboard: `platform`, `content_id`, `published_at`/`date`, `content_type`, `views`, `reach`, `engagement`, `likes`, `comments`, `shares`, `saves_or_favorites`, `avg_watch_time_seconds`, `completion_rate`/`average_view_percentage`, `followers_gained`/`subscribers_gained`, `source`, `retrieved_at`, `window_type` y `comparability`. Las filas sin dato deben permanecer como `null`, no convertirse en cero.

## Referencias

[1]: https://developers.facebook.com/docs/graph-api/reference/post/insights/ "Meta for Developers — Post Insights"
[2]: ../Operations/Research/2026-08-15_Publication_Log.csv "Publication Log de Universe Sent Me"
[3]: ../Operations/Research/2026-08-15_ExperimentLog.csv "ExperimentLog de Universe Sent Me"
