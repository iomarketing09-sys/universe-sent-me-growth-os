# Registro Maestro de Reels Publicados

**Propósito:** Mantener un inventario actualizado de todos los Reels publicados para evitar repeticiones, monitorear el cumplimiento de la Regla de Cascada y facilitar el análisis de rendimiento.
**Estado:** Active
**Fecha de creación:** 2026-08-01
**Última actualización:** 2026-08-21
**Versión:** 2.6
**Autor:** Manus AI (CGO)
**Documentos relacionados:** `05_00_Calendario_01_02_Ago.md`, `Operations/Memories/deep_dive_reels_comparativo.md`, `../Operations/Research/2026-08-19_Historial_Reels_Consolidado.json`, `../Operations/Research/2026-08-19_Relaciones_Reels_Alta_Evidencia.json`, `../Operations/Research/2026-08-19_Inventario_Assets_Drive_Reels.json`, `../Operations/Research/2026-08-19_Publicaciones_Historicas_Adjudicadas.json`, `../Operations/Research/2026-08-19_Decisiones_Reconciliacion_Reels.json`, `../Operations/Research/2026-08-19_Piezas_Sin_Cascada_Revision.json`, `../Operations/Research/2026-08-19_Auditoria_Assets_Drive_Reels.md`, `../Operations/Research/2026-08-19_Meta_Reels_Audit.json`, `../Operations/Research/2026-08-19_YouTube_Metadata_Nativo.json`, `../Operations/Research/2026-08-19_Inventario_Coste_Reels_28D.json`, `../Operations/Research/Affiliate_Link_Ledger.csv`, `../Operations/Production/2026-08-19_Brief_Pieza01_DobleCheck_Universe_Flow.md`, `../Operations/Production/2026-08-20_Exploracion_Videoclip_Musical_Desamor.md`, `14_00_Fuente_Maestra_y_Ledgers.md`

---

## Historial consolidado y cascadas verificadas — corte 22 julio–18 agosto de 2026

El consolidado actual contiene **45 registros de video corto** con evidencia de fuente: 16 Reels de Facebook, 16 Reels de Instagram, 7 videos de TikTok y 6 videos/Shorts de YouTube. Treinta y nueve provienen del corte analítico original; seis publicaciones históricas adjudicadas se incorporaron para cerrar relaciones confirmadas por Fernando, conservando IDs y formato pero sin inventar una ventana métrica comparable. Los formatos de Facebook se clasifican por `video` y `video_inline` en Meta; el resto de publicaciones orgánicas de Facebook permanece fuera de esta tabla hasta que tenga evidencia de formato.

| Concepto canónico confirmado | Facebook | Instagram | TikTok | YouTube | Estado de reconciliación |
|---|:---:|:---:|:---:|:---:|---|
| Instante suspendido / “Vitamina B (besos)” | Sí | Sí | Sí | Sí | Cascada confirmada; fechas nativas disponibles en las cuatro publicaciones. |
| Mi gato sabe hacer de todo | Sí | Sí | No confirmada | No confirmada | Cross-post confirmado entre Facebook e Instagram. |
| Rock gótico vs. Juan Gabriel / gatos en la madrugada | Sí | Sí | Sí | No confirmada | Cascada confirmada por Fernando; TikTok usa una adaptación de copy distinta y conserva su asset fuente identificado. |
| Muros vemos / Inbox no sabemos | Sí | Sí | Sí | Sí | Coincidencia textual confirmada; fecha de YouTube pendiente. |
| Conversaciones atrancadas | Sí | Sí | No confirmada | No confirmada | Coincidencia textual confirmada entre Meta. |
| Fantasma Backrooms | Sí | Sí | No confirmada | No confirmada | Coincidencia textual confirmada entre Meta. |
| Caja de Luna | Sí | Sí | No confirmada | No confirmada | Coincidencia textual confirmada entre Meta. |
| Ojos correctos | No confirmada | No confirmada | Sí | Sí | Cross-post confirmado entre TikTok y YouTube. |
| Habilidades / manual de usuario | No confirmada | No confirmada | Sí | Sí | Cross-post confirmado entre TikTok y YouTube. |
| Wilfred / Momentos USM | Sí | Sí | No confirmada | No confirmada | Alta evidencia: hashtags coincidentes y 16 segundos de diferencia de publicación. |
| Elara y Evan / estrellas | Sí | Sí | No confirmada | No confirmada | Alta evidencia: personajes y tags coincidentes; 36 segundos de diferencia. |
| Cartones / papeles | Sí | Sí | No confirmada | No confirmada | Alta evidencia: copy semánticamente equivalente y 44 segundos de diferencia. |
| Universe sin caption (11 ago) | Sí | Sí | No confirmada | No confirmada | Cascada confirmada por Fernando: ambos registros proceden de `VID_20260811_004743_587_bsl.mp4`; la carpeta `TRAILER UNIVERSE` no define el formato editorial. |
| Fantasma caminando con gatos | Sí | Sí | No confirmada | Sí | Cascada confirmada por Fernando; Meta verificó el copy idéntico en FB/IG y el Short `Qoa-XUOVALk` fue reasignado a esta producción. |
| Mi ascenso a la locura | Sí | Sí | No confirmada | No confirmada | Cascada confirmada por Fernando; copy y hashtags idénticos, publicados con 13 segundos de diferencia. |
| Escribiendo / verdadero terror psicológico | Sí | Sí | No confirmada | Sí | Cascada confirmada por Fernando; FB/IG publicaron el copy `El verdadero terror psicológico...` con 13 segundos de diferencia y YouTube usa el título `Escribiendo...`. |
| Gato con 17 juguetes / gastar sin mañana | Sí | Sí | Sí | No confirmada | Cascada confirmada por Fernando; Meta se publicó localmente el 4 de julio y TikTok el 31 de julio como republicación diferida. |

> **Estado de revisión:** no quedan piezas pendientes de decisión cross-platform. Tres registros permanecen fuera de una cascada por resolución explícita: P01 es una versión alternativa de *Fantasma caminando con gatos* y no el mismo export; P04 es un carrusel de memes exclusivo de TikTok; P05 es un Reel exclusivo de Facebook. Ninguno recibe campañas o relaciones inventadas.

La evidencia por publicación, las relaciones confirmadas y las limitaciones se conservan en `Operations/Research/2026-08-19_Historial_Reels_Consolidado.json`. Las fechas nativas de los seis videos de YouTube están en `Operations/Research/2026-08-19_YouTube_Metadata_Nativo.json`, las relaciones de alta evidencia y confirmadas por Fernando en `Operations/Research/2026-08-19_Relaciones_Reels_Alta_Evidencia.json`, las recuperaciones de identidad fuera del corte en `Operations/Research/2026-08-19_Publicaciones_Historicas_Adjudicadas.json`, las decisiones de versión/exclusividad en `Operations/Research/2026-08-19_Decisiones_Reconciliacion_Reels.json` y los assets fuente disponibles en Drive en `Operations/Research/2026-08-19_Inventario_Assets_Drive_Reels.json`. Veintinueve publicaciones ya tienen asset fuente asociado; los assets que aún permanezcan solo en el celular siguen como evidencia pendiente. Ningún registro recibe `Experiment_ID` retrospectivo sin evidencia explícita; por ahora todos mantienen `Sin_etiqueta_historica`. Estos archivos son el insumo de la vista de cascadas del dashboard.

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
| `CON-2026-08-20-RemoteControl-EvanElara` | Videoclip musical “Remote Control” | Evan + Elara | **Cascada completa confirmada y trazable.** Instagram: `18209594575357100`, [permalink](https://www.instagram.com/reel/DcR29-aRRXN/), 20 Ago 17:41:41 CDT. Facebook: Reel `2815726225473165`, Post `122153750763072582`, [permalink](https://www.facebook.com/reel/2815726225473165/), producto nativo con link `https://meli.la/1eUqUye` y etiqueta `usmfb20260820rc01`, 20 Ago 18:02:04 CDT. TikTok: [`7676249640928414997`](https://www.tiktok.com/@universe.sent.me/video/7676249640928414997). YouTube Short: [`nb6om1LhOMc`](https://youtube.com/shorts/nb6om1LhOMc). |
| `CON-2026-08-19-DobleCheck-Universe` | Doble check → Universe / “yo después de mandar ‘no pasa nada’” | Universe | **Cascada completa.** Instagram: `17902439976554149`, [permalink](https://www.instagram.com/reel/DcPY7QNF1hb/). Facebook vigente: [`2210896633022235`](https://www.facebook.com/reel/2210896633022235), producto nativo con link `https://meli.la/1AQ2upG` y etiqueta `usmfb20260819p01`. TikTok: [`7675906878127246613`](https://www.tiktok.com/@universe.sent.me/video/7675906878127246613). YouTube Short: [`YVsi53pXA4s`](https://youtube.com/shorts/YVsi53pXA4s?si=uGY617fIq5IknnQ6). El Reel de Graph `1549931766108154` fue eliminado antes de métricas y no entra al análisis. |
| CNT-002 | Wilfred reseña su propio peluche | Wilfred | Pendiente de producción (Flow). |
| CNT-003 | Trailer 001 — Universe Sent Me | Universe | Pendiente de producción (Flow). |
| Nuevo | Propuesta 2: Idealización | Wilfred/Elara | Generando en Flow (Sábado 1 Ago). |
| CNT-015 | El instante suspendido (Fantasma contemplativo) | Fantasma | **Publicado** en cascada (5 Ago, 7:00-7:30 PM). Audio: por definir. Hook: "vitamina B (besos)" en copy. |


---

## Auditoría operativa de Reels — 2026-08-21

La reconciliación del historial estructurado `Operations/Research/2026-08-19_Historial_Reels_Consolidado.json` queda actualizada a v1.6 y contiene **51 registros de publicaciones de video corto**, distribuidos en Facebook 22, Instagram 16, TikTok 7 y YouTube 6. Estos registros representan publicaciones por plataforma, no piezas únicas: hay 24 conceptos identificables y 17 grupos de crosspost o relación multicanal. Las métricas no se suman entre plataformas.

| Control | Resultado actual |
|---|---|
| Registros por plataforma | Facebook 22; Instagram 16; TikTok 7; YouTube 6 |
| Conceptos identificables | 24 |
| Grupos con relación cross-platform | 17 |
| Assets con evidencia Drive | 32/51 en el historial estructurado |
| Publicaciones con `Experiment_ID` explícito | 1/51 — el Reel Doble Check |
| Publicaciones con `Hypothesis_ID` explícito | 1/51 — `HB-REEL-01` |
| Reels con views disponibles | 27/51; las fuentes no son uniformes |
| Reels con reach disponible | 14/51 |
| Facebook Reels con views/reach recuperables en este corte | 0/22 |

El Reel más reciente detectado en Meta es **`Universe viéndote Farmear Aura`**, Page Post ID `1036844829507460_122154017667072582`, Reel ID `2005557463434064`, publicado el 2026-08-21 21:30:59 UTC y verificado como `is_published=true`. La consulta de solo lectura devolvió el permalink `https://www.facebook.com/reel/2005557463434064/` y un comentario de la propia Página; la consulta de Insights devolvió HTTP 400 porque la solicitud no contenía una métrica válida para este objeto. No se registran views, reach, retención, completaciones ni seguidores ganados.

La consulta de `/{page_id}/scheduled_posts` del mismo corte devolvió 47 posts programados, todos con attachment `photo` y ninguno con attachment `video`. Por tanto, el Reel de hoy ya está publicado en Meta; no aparece como un Reel pendiente dentro del scheduler de Facebook. Su hora local equivalente es aproximadamente 16:30 en `America/Matamoros`.

También se incorporaron al historial los Reels recientes `Remote Control` (`2815726225473165`) y `Doble Check → Universe` (`2210896633022235`). `Remote Control` tiene cascada completa confirmada en Instagram, Facebook, TikTok y YouTube; `Doble Check` conserva `EXP-202608-REALUNIVERSE-01` y `HB-REEL-01`. Ambos necesitan snapshots propios antes de recibir un veredicto de aprendizaje.

La ampliación histórica de mayo/junio añadió tres matches exactos entre Drive y Meta: `Fantasma_tranquilo_con_viento_202605241629.mp4` → Reel `1877535942934184`; el asset set de los dos clips `Man_*_20260613` → Reel `2417378928740605`; y `Pato_villano_mirando_cámara_POV_EresAries.mp4` → Reel `1049041731412120`. El archivo `Wilfred realista haciendo una posion.mp4` permanece sin match confirmado después de dos controles visuales negativos; la matriz completa está en `Operations/Research/2026-08-21_Reels_Drive_Meta_Crossmatch_Review.csv`.

### Estado de Maeve

El documento `Operations/Production/2026-08-20_Exploracion_Videoclip_Musical_Desamor.md` conserva el proyecto de Maeve como **dirección de producción en revisión**, no como Reel publicado. El tratamiento `Crave You — Maeve entre todas las miradas` y su variante `La habitación de las plumas` permanecen en `REVIEW`; no existe todavía un `Platform_Content_ID` ni un export de video incorporado al historial de Reels. Debe tratarse como `En_Produccion/Pendiente_Revision`, no como publicación, métrica o experimento cerrado. Si Fernando se refiere a otro Reel de Maeve distinto, habrá que vincularlo mediante nombre exacto del archivo, fecha o ID nativo antes de añadirlo.

### Brecha principal

Sí existe información histórica de Reels, pero estaba repartida entre el historial multicanal, auditorías de Meta/Windsor, documentos de producción y el registro maestro. El problema no era ausencia total de publicaciones; era que no había una vista operativa actualizada que distinguiera **publicado**, **programado**, **en producción**, **en revisión** y **medido**. La auditoría actual establece esa separación y deja las métricas faltantes como pendientes explícitos. De los 51 registros actuales, 32 tienen evidencia de asset en Drive, 36 tienen engagement, 27 tienen views y 14 tienen reach; el caso de Wilfred permanece en revisión y no se inventa un vínculo.

## Actualización operativa — 2026-08-20

El Reel `CON-2026-08-19-DobleCheck-Universe` / Meta `2210896633022235` permanece **publicado en cascada** en Instagram, Facebook, TikTok y YouTube Shorts. Fernando confirmó además la incorporación de un producto nativo de Mercado Libre en Facebook. El tracking asociado es exclusivo: etiqueta `usmfb20260819p01`, link `https://meli.la/1AQ2upG` y producto `MLMU3833350067`. La publicación no se mezcla con el experimento P0 de imágenes; sus métricas de video y afiliación se medirán en carriles separados.

El siguiente paso técnico es recuperar métricas específicas de video desde la publicación de Facebook y capturar snapshots afiliados por etiqueta. No se debe inferir rendimiento comercial a partir de interacciones del Reel.

Documentos sincronizados: `Operations/Production/2026-08-19_Playbook_Tracking_Afiliados_MercadoLibre.md`, `Operations/Research/2026-08-19_Auditoria_Reels_y_Monetizacion.md` y `Operations/Research/Affiliate_Link_Ledger.csv`.

---

## Corte de métricas Meta — 2026-08-20 05:07 UTC

El Reel `2210896633022235` aparece en el feed de la página mediante el post `1036844829507460_122153090559072582`. El corte actual devolvió **1 reacción**, **0 comentarios** y `shares` no expuesto por el objeto consultado. No se recuperaron vistas, watch time o retención mediante Insights; el endpoint de Insights usado previamente devolvió errores de métrica no válida. Este corte es lifetime/actual, no una ventana 24/72 horas, y permanece separado de P0.

La evidencia JSON se conserva en `Operations/Research/2026-08-20_Meta_Reel_2210896633022235_Metrics.json`.

---
