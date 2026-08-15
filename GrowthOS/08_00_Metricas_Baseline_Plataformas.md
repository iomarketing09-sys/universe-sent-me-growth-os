# Métricas Baseline — Facebook & Instagram (Universe Sent Me)

**Propósito:** Registro de métricas reales extraídas de Windsor.ai. Fuente de verdad para comparaciones de rendimiento, calibración de hipótesis y decisiones de canal. No es un resumen de sesión — es un documento vivo que debe actualizarse con cada ciclo de análisis.
**Estado:** Active
**Fecha de creación:** 2026-08-03
**Última actualización:** 2026-08-15
**Versión:** 1.2
**Autor:** Claude (Guardián de Canon, extracción directa vía Windsor.ai MCP)
**Documentos relacionados:** `07_00_Registro_Maestro_Reels.md`, `06_00_Reglas_Aprendizaje_Tendencias.md`, `01_00_Arquitectura_Calendario_Escalable.md`, `14_00_Fuente_Maestra_y_Ledgers.md`, `../Operations/Research/2026-08-15_Publication_Log.csv`, `../Operations/Research/2026-08-15_ExperimentLog.csv`

> **Metodología:** Datos extraídos directamente desde Windsor.ai el 2026-08-03. Período cubierto: últimos 14 días con datos del día actual incluidos. Cuentas: Facebook Page @UniverseSentMe (ID `1036844829507460`) e Instagram @universe_sent_me_0326 (ID `17841462696378190`). Los datos de IG publicados hoy mismo pueden mostrar cero por latencia de la API.

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

La próxima actualización numérica deberá unir `Content_Inventory.csv`, `Publication_Log.csv` y `ExperimentLog.csv` por `CNT-####` y Meta ID. Para el lote 15–16 se incorporarán las nueve publicaciones solo cuando existan ventanas válidas; la primera extracción del 15 de agosto evaluó las nueve y encontró cero ventanas elegibles, por lo que no se añadieron métricas prematuras.

El reporte comparará por separado: (a) frecuencia y mediana de interacciones por publicación; (b) Facebook imagen frente a Facebook Reel; (c) Instagram Reel frente a Instagram imagen; (d) contenido nuevo frente a reuse; y (e) comentarios totales frente a comentarios cualitativos. Facebook seguirá siendo el canal principal de distribución en la lectura actual, mientras Instagram se evaluará como canal en desarrollo y no se presentará como fracaso por sus volúmenes absolutos todavía pequeños.

No se emitirá un veredicto de canal hasta completar el lote de métricas y armonizar las definiciones de interacción. La baseline común es un marco de comparación, no una autorización para mezclar los numeradores de Facebook e Instagram.

## 8. Próxima Actualización

Este documento debe actualizarse:
- Cada domingo (ciclo semanal de análisis)
- Después de publicar cualquier pieza con distribución en más de una plataforma
- Cuando se cierren hipótesis en el HypothesisBank

Herramienta de extracción histórica: Windsor.ai MCP → connector `facebook_organic` + `instagram`. Fuente operativa vigente para publicaciones reconciliadas: Meta Graph API v26 + `Publication_Log.csv`. Campos clave históricos: `post_impressions`, `post_engagements`, `post_reactions_total`, `media_reach`, `media_views`, `media_engagement`. Campos operativos: reacciones, comentarios, shares, Meta ID, timestamp real y estado de ventana.

## Referencias

[1]: https://developers.facebook.com/docs/graph-api/reference/post/insights/ "Meta for Developers — Post Insights"
[2]: ../Operations/Research/2026-08-15_Publication_Log.csv "Publication Log de Universe Sent Me"
[3]: ../Operations/Research/2026-08-15_ExperimentLog.csv "ExperimentLog de Universe Sent Me"
