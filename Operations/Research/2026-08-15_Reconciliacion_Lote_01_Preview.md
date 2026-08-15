# Preview de reconciliación — lote 1

**Estado:** Active
**Fecha:** 2026-08-15
**Regla:** las resoluciones se basan en evidencia documental, Meta y Drive; ningún `260####` fue marcado como asset confirmado.

## Distribución propuesta de estados

| Campo | Distribución |
|---|---:|
| Estado operativo `Reuse_Candidate` | 2 |
| Estado operativo `Production_Pending` | 3 |
| Estado operativo `Blocked_Operational` | 1 |
| Estado operativo `Pending_Approval` | 2 |
| Estado operativo `Idea` | 17 |
| Estado operativo `Draft_Pending_Approval` | 3 |
| Estado canon `Canon_Review_Required` | 13 |
| Estado canon `Canon_Clear_or_Unverified` | 13 |
| Estado canon `Canon_Constrained` | 1 |
| Estado canon `Canon_Partial` | 1 |

## Coincidencias CNT↔260 encontradas en la misma línea

| Archivo | Línea | CNT | Referencia 260 | Contexto |
|---|---:|---|---|---|
| GrowthOS/05_02_Calendario_04_09_Agosto.md | 34 | CNT-002 | 260509 | | **9:00 PM** | FB | Foto (Meme) | Universe | `260509.png` — "Pensamientos con groserías..." *(Corrección 2026-08-04: CNT-002 ya se publicó el 30-Jul, no se produce de nuevo — este slot vuelve a meme reutilizado)* | Reuse Queue | |
| Operations/Research/2026-08-12_Revision_Cambios_GrowthOS_Claude_Fernando.md | 47 | CNT-023 | 260801 | El Episodio 2 de CNT-023 ("¿Qué me llegó?") se reconcilió con la producción final de Lámpara Luna (storyboard de 9 escenas). El Backlog, Production Queue, Approval Queue e inventario CSV quedaron actualizados con las piezas de la semana 10– |

## Resultado aplicado al inventario

Se añadieron columnas normalizadas sin borrar ni sobrescribir `estado` o `bloqueado_canon`. El inventario contiene ahora **30 registros** y **0 assets 260 confirmados**, porque ninguna de las cuatro excepciones requería inventar una relación de archivo.

| Excepción | Resolución | Evidencia |
|---|---|---|
| `CNT-002` | `Resolved_Production_Set` | Meta identificó el post `1036844829507460_122143141185072582`, publicado el 30-Jul 14:16:47 UTC, con permalink [Facebook Reel](https://www.facebook.com/reel/911880681976378/). El video dura 17.39 s y contiene la secuencia de caja Mercado Libre, Wilfred y peluche. Drive aporta tres videos de producción relacionados; no existe un 260 único confirmado. |
| `CNT-023` | `Resolved_Asset_Set` | La carpeta Drive `Elara - Lampara de luna` contiene 7 assets: `Cat_delivers_package_to_witch_202608081911.mp4`, `Cat_delivers_package_to_woman_202608081951.jpeg`, `Cat_walking_with_package_1080p_202608081939.mp4`, `Char_Elara_opening_package_202608081909.mp4` y tres renders `Generar_video_de_secuencia_imagenes_202608081917.mp4`, `...1922.mp4`, `...1928.mp4`. Se registra como conjunto, no como un único `260`. |
| `CNT-029` | `Resolved_Project_Record` | Se recupera su ficha de producción, banco de 9 cuadros y estado Draft; no existe referencia `260` y no se inventa. |
| `CNT-030` | `Resolved_Dependent_Record` | Se recupera su ficha de audio/montaje y se enlaza con `CNT-029`; no es una publicación independiente. |

`CNT-023` queda completamente trazable como conjunto de 7 assets de Drive, con relación a `CNT-002` como episodio 1 y sin publicación propia confirmada. `CNT-029` y `CNT-030` ya fueron incorporados al inventario como registros completos. `CNT-002` queda cerrado a nivel de publicación y conjunto de producción: su `Meta_Post_ID`, permalink, fecha y assets relacionados ya están en el inventario y en `Publication_Log`.

## Estado final

Las cuatro excepciones originales quedaron resueltas a nivel de registro y trazabilidad. CNT-002 ya no tiene una excepción abierta: el post real y el conjunto de producción fueron identificados. Queda únicamente una nota histórica: no se conserva el nombre del render final como archivo `260####`, por lo que el inventario no crea una falsa precisión.
