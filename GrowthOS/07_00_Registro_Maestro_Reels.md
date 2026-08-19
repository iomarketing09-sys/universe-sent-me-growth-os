# Registro Maestro de Reels Publicados

**Propósito:** Mantener un inventario actualizado de todos los Reels publicados para evitar repeticiones, monitorear el cumplimiento de la Regla de Cascada y facilitar el análisis de rendimiento.
**Estado:** Active
**Fecha de creación:** 2026-08-01
**Última actualización:** 2026-08-19
**Versión:** 1.4
**Autor:** Manus AI (CGO)
**Documentos relacionados:** `05_00_Calendario_01_02_Ago.md`, `Operations/Memories/deep_dive_reels_comparativo.md`, `../Operations/Research/2026-08-19_Historial_Reels_Consolidado.json`, `../Operations/Research/2026-08-19_Relaciones_Reels_Alta_Evidencia.json`, `../Operations/Research/2026-08-19_Meta_Reels_Audit.json`, `../Operations/Research/2026-08-19_YouTube_Metadata_Nativo.json`, `../Operations/Research/2026-08-19_Inventario_Coste_Reels_28D.json`, `14_00_Fuente_Maestra_y_Ledgers.md`

---

## Historial consolidado y cascadas verificadas — corte 22 julio–18 agosto de 2026

El consolidado actual contiene **39 registros de video corto** con evidencia de fuente: 12 Reels de Facebook, 14 Reels de Instagram, 7 videos de TikTok y 6 videos/Shorts de YouTube. Los formatos de Facebook se clasifican por `video` y `video_inline` en Meta; el resto de publicaciones orgánicas de Facebook permanece fuera de esta tabla hasta que tenga evidencia de formato.

| Concepto canónico confirmado | Facebook | Instagram | TikTok | YouTube | Estado de reconciliación |
|---|:---:|:---:|:---:|:---:|---|
| Instante suspendido / “Vitamina B (besos)” | Sí | Sí | Sí | Sí | Cascada confirmada; fechas nativas disponibles en las cuatro publicaciones. |
| Mi gato sabe hacer de todo | Sí | Sí | No confirmada | No confirmada | Cross-post confirmado entre Facebook e Instagram. |
| Rock gótico vs. Juan Gabriel | Sí | Sí | No confirmada | No confirmada | Cross-post confirmado entre Facebook e Instagram. |
| Muros vemos / Inbox no sabemos | Sí | Sí | Sí | Sí | Coincidencia textual confirmada; fecha de YouTube pendiente. |
| Conversaciones atrancadas | Sí | Sí | No confirmada | No confirmada | Coincidencia textual confirmada entre Meta. |
| Fantasma Backrooms | Sí | Sí | No confirmada | No confirmada | Coincidencia textual confirmada entre Meta. |
| Caja de Luna | Sí | Sí | No confirmada | No confirmada | Coincidencia textual confirmada entre Meta. |
| Ojos correctos | No confirmada | No confirmada | Sí | Sí | Cross-post confirmado entre TikTok y YouTube. |
| Habilidades / manual de usuario | No confirmada | No confirmada | Sí | Sí | Cross-post confirmado entre TikTok y YouTube. |
| Wilfred / Momentos USM | Sí | Sí | No confirmada | No confirmada | Alta evidencia: hashtags coincidentes y 16 segundos de diferencia de publicación. |
| Elara y Evan / estrellas | Sí | Sí | No confirmada | No confirmada | Alta evidencia: personajes y tags coincidentes; 36 segundos de diferencia. |
| Cartones / papeles | Sí | Sí | No confirmada | No confirmada | Alta evidencia: copy semánticamente equivalente y 44 segundos de diferencia. |

> **Regla vigente:** las 11 piezas que aún no tienen relación explícita o evidencia de alta confianza se conservan como publicaciones independientes. No se atribuyen a una cascada, no se suman como una sola producción y no reciben una etiqueta de campaña inventada.

La evidencia por publicación, las relaciones confirmadas y las limitaciones se conservan en `Operations/Research/2026-08-19_Historial_Reels_Consolidado.json`. Las fechas nativas de los seis videos de YouTube están en `Operations/Research/2026-08-19_YouTube_Metadata_Nativo.json` y las tres relaciones de alta evidencia en `Operations/Research/2026-08-19_Relaciones_Reels_Alta_Evidencia.json`. Ningún registro recibe `Experiment_ID` retrospectivo sin evidencia explícita; por ahora todos mantienen `Sin_etiqueta_historica`. Estos archivos son el insumo de la vista de cascadas del dashboard.

---

## Historial Reciente (Julio - Agosto 2026) y Métricas Detalladas

| Fecha Publicación | Título / Concepto | Personaje Principal | Plataforma | Visualizaciones | % No Seguidores | Interacciones (L/C/G/S) | Seguidores Obtenidos | Score de Eficacia (0-10) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2026-08-05** | El instante suspendido (Fantasma contemplativo) | Fantasma | FB, IG, TT, YT | *(Pendiente)* | *(Pendiente)* | *(Pendiente)* | *(Pendiente)* | *(Pendiente)* |
| **2026-08-01** | Wilfred: Muros vemos, Inbox no sabemos | Wilfred | FB, IG, TT, YT | *(Pendiente)* | *(Pendiente)* | *(Pendiente)* | *(Pendiente)* | *(Pendiente)* |
| **2026-07-30** | Mi gato sabe hacer de todo... | Universe | IG | 114 | 95.6% | 5 (3/0/0/2) | 1 | **8.5** (Alto % No Seguidores, 1 seguidor) |
| **2026-07-30** | Mi gato sabe hacer de todo... | Universe | FB | 1025 | N/A | 21 (19/2/N/A/N/A) | N/A | **7.0** (Buenas vistas en FB) |
| **2026-07-29** | Rock gótico vs Juan Gabriel | Universe | IG | 55 | 80.6% | 1 (1/0/0/0) | 0 | **4.0** (Bajo engagement) |
| **2026-07-29** | Rock gótico vs Juan Gabriel | Universe | FB | 742 | N/A | 27 (23/4/N/A/N/A) | N/A | **6.5** (Mejor en FB) |
| **2026-07-29** | Wilfred en el bosque (Humor) | Wilfred | IG | 21 | 64.5% | 0 (0/0/0/0) | 0 | **2.0** (Muy bajo rendimiento) |
| **2026-07-29** | Wilfred en el bosque (Humor) | Wilfred | FB | 493 | N/A | 7 (6/1/N/A/N/A) | N/A | **5.0** (Rendimiento moderado en FB) |
| **2026-07-27** | Mi ascenso a la locura | Universe / Hada | IG | 106 | 91.9% | 2 (2/0/0/0) | 0 | **7.5** (Alto % No Seguidores, pero bajo engagement) |
| **2026-07-27** | Mi ascenso a la locura | Universe / Hada | FB | 603 | N/A | 23 (20/3/N/A/N/A) | N/A | **6.0** (Rendimiento moderado en FB) |
| **Mayo 2026** | Fantasma paseando gatos | Fantasma | IG | 124 | 92.2% | 7 (7/0/0/0) | 0 | **8.0** (Alto % No Seguidores, buen potencial) |
| **Mayo 2026** | Fantasma paseando gatos | Fantasma | FB | 6878 | N/A | 128 (122/6/N/A/N/A) | N/A | **9.5** (Excelente rendimiento en FB) |
| **2026-06-14** | No corras por correr | Wilfred | IG | *(No hay datos)* | *(No hay datos)* | *(No hay datos)* | *(No hay datos)* | *(No hay datos)* |

---

## Auditoría de Cascada Pendiente

Se ha detectado que varios Reels recientes solo se publicaron en Instagram. Según la estrategia CGO v3.0, deben replicarse en las demás plataformas:

1. **"Mi gato sabe hacer de todo..." (30 Jul)** -> Subir a TikTok y YouTube Shorts.
2. **"Rock gótico vs Juan Gabriel" (29 Jul)** -> Subir a TikTok y YouTube Shorts.
3. **"Wilfred en el bosque" (29 Jul)** -> Subir a TikTok y YouTube Shorts.
4. **"Mi ascenso a la locura" (27 Jul)** -> Subir a TikTok y YouTube Shorts.

---

## Próximos Estrenos (Pipeline)

| ID_Pieza | Concepto | Personaje | Estado Actual |
| :--- | :--- | :--- | :--- |
| CNT-002 | Wilfred reseña su propio peluche | Wilfred | Pendiente de producción (Flow). |
| CNT-003 | Trailer 001 — Universe Sent Me | Universe | Pendiente de producción (Flow). |
| Nuevo | Propuesta 2: Idealización | Wilfred/Elara | Generando en Flow (Sábado 1 Ago). |
| CNT-015 | El instante suspendido (Fantasma contemplativo) | Fantasma | **Publicado** en cascada (5 Ago, 7:00-7:30 PM). Audio: por definir. Hook: "vitamina B (besos)" en copy. |
