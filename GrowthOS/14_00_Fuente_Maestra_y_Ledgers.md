---
title: "Fuente maestra y ledgers del Growth OS"
purpose: "Definir una arquitectura mínima y unificada para que inventario, publicaciones, calendarios y aprendizaje compartan IDs sin duplicar datos ni repetir consultas innecesarias."
status: Active
created: 2026-08-15
updated: 2026-08-24
version: "2.51"
author: "Manus AI (CGO)"
related_documents:
  - "GrowthOS/01_00_Arquitectura_Calendario_Escalable.md"
  - "GrowthOS/Integracion_Growth_OS.md"
  - "GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md"
  - "GrowthOS/Content_Inventory.csv"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "Operations/Research/2026-08-15_ExperimentLog.csv"
  - "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
  - "Operations/Research/2026-08-15_Community_Engagement_Log.md"
  - "Operations/Production/extract_metrics_24_72.py"
  - "Operations/Production/extract_metrics_24_72_playbook.md"
  - "Operations/Automation/2026-08-23_Diseno_Captura_Baseline_E0_E24_E72.md"
  - "Operations/Research/2026-08-15_Reconciliacion_Publicaciones_15_16_CNT.md"
  - "GrowthOS/00_Índice.md"
  - "Operations/Research/2026-08-17_Instagram_Publicacion_260633.json"
  - "Operations/Research/2026-08-17_Instagram_IDs_Duplicaciones_Confirmadas.json"
  - "Operations/Research/2026-08-18_Analisis_Rendimiento_28_Dias_Instagram_Facebook.md"
  - "Operations/Research/2026-08-19_Windsor_Instagram_28D_Normalizado.json"
  - "Operations/Research/2026-08-19_Windsor_Facebook_Organic_28D_Normalizado.json"
  - "Operations/Research/2026-08-19_Social_Performance_28D_Normalizado.json"
  - "Operations/Research/2026-08-19_Retorno_Engagement_Esfuerzo_28D.json"
  - "Operations/Production/2026-08-19_Actualizacion_Asistida_Dashboard_Social.md"
  - "Operations/Production/2026-08-19_Piloto_Esfuerzo_y_Experimentacion.md"
  - "Operations/Research/2026-08-19_Inventario_Coste_Reels_28D.json"
  - "Operations/Research/2026-08-19_Historial_Reels_Consolidado.json"
  - "Operations/Research/2026-08-21_Reels_Publication_Inventory.csv"
  - "Operations/Research/2026-08-21_Reels_Audit_Coverage_Summary.json"
  - "Operations/Research/2026-08-21_Meta_Reels_Live_Audit_Summary.json"
  - "Operations/Research/2026-08-21_Corte_Diario_Metricas_2200.md"
  - "Operations/Research/2026-08-21_Corte_Diario_Metricas_2200.json"
  - "Operations/Research/2026-08-21_Corte_Diario_Metricas_2200.csv"
  - "Operations/Research/2026-08-21_Analisis_Corte_Diario_Familias_Personajes.md"
  - "Operations/Research/2026-08-21_Analisis_Corte_Diario_Familias_Personajes.json"
  - "Operations/Research/2026-08-21_Analisis_Corte_Diario_Familias_Personajes.csv"
  - "Operations/Research/2026-08-22_Meta_Daily_Metrics_Raw.json"
  - "Operations/Research/2026-08-22_Corte_Diario_Metricas_2200.md"
  - "Operations/Research/2026-08-22_Reels_Meta_Readonly_Reconciliation.json"
  - "Operations/Research/2026-08-22_Meta_Business_Suite_28D_Reels_Visual_Evidence.md"
  - "Operations/Research/2026-08-22_Reels_Confirmed_Metric_Assessment.json"
  - "Operations/Research/2026-08-22_Corte_Diario_Metricas_2200.csv"
  - "Operations/Research/2026-08-22_Analisis_Semanal_20260816_20260822.md"
  - "Operations/Research/2026-08-22_Analisis_Semanal_20260816_20260822.csv"
  - "Operations/Research/2026-08-22_Weekly_Metrics_20260816_20260822_Raw.json"
  - "Operations/Research/2026-08-22_Weekly_Metrics_20260816_20260822_Joined.csv"
  - "Operations/Research/2026-08-22_Auditoria_Ejecutiva_GrowthOS_Estado_y_Prioridades.md"
  - "Operations/Research/2026-08-22_Propuesta_Ciclo_Semanal_Domingo_Sabado.md"
  - "Operations/Research/2026-08-22_Analisis_Corte_Diario_Familias_Personajes.md"
  - "Operations/Research/2026-08-22_Analisis_Corte_Diario_Familias_Personajes.csv"
  - "Operations/Research/2026-08-21_Reels_Drive_Meta_Crossmatch_Review.csv"
  - "Operations/Research/2026-08-22_Reels_Pending_Asset_Reconciliation_Queue.csv"
  - "Operations/Research/2026-08-22_Reels_Pending_Drive_Triage.csv"
  - "Operations/Research/2026-08-22_Reels_Tier2A_Visual_Review_Batch.csv"
  - "Operations/Research/2026-08-22_Reels_Confirmed_Classification.csv"
  - "Operations/Research/2026-08-22_Reels_Confirmed_Metric_Assessment.json"
  - "Operations/Research/2026-08-22_Reels_Metric_Instrumentation_Protocol.md"
  - "Operations/Production/2026-08-22_Brief_Reel_Dialogue_Radio_003.md"
  - "Operations/Production/2026-08-20_Exploracion_Videoclip_Musical_Desamor.md"
  - "Operations/Research/2026-08-22_Reels_Top5_Visual_Review_Batch.csv"
  - "Operations/Research/2026-08-19_YouTube_Metadata_Nativo.json"
  - "Operations/Research/2026-08-19_Relaciones_Reels_Alta_Evidencia.json"
  - "Operations/Research/2026-08-19_Inventario_Assets_Drive_Reels.json"
  - "Operations/Research/2026-08-19_Publicaciones_Historicas_Adjudicadas.json"
  - "Operations/Research/2026-08-19_Decisiones_Reconciliacion_Reels.json"
  - "Operations/Research/2026-08-19_Corte_Multicanal_28D_1600.md"
  - "Operations/Research/2026-08-19_Comparacion_Snapshots_28D.md"
  - "Operations/Research/2026-08-19_Auditoria_Assets_Drive_Reels.md"
  - "GrowthOS/08_00_Metricas_Baseline_Plataformas.md"
  - "Operations/Research/Historical_Performance_Snapshot.csv"
  - "Operations/Research/Historical_Performance_Individuals.csv"
  - "Operations/Research/2026-08-17_Integracion_CNT_Mayo_Reserve_Revision.md"
  - "Operations/Research/2026-08-17_Revision_Reserve_Mayo.json"
  - "Operations/Research/2026-08-20_Source_Alias_Table.csv"
  - "Operations/Research/2026-08-20_Source_Alias_Table_Report.md"
  - "Operations/Research/2026-08-20_Historical_Performance_Individuals_Consolidated.csv"
  - "Operations/Research/2026-08-20_Junio_Consolidated_View.md"
  - "Operations/Research/2026-08-20_Junio_Duplicate_Groups.md"
  - "Operations/Research/2026-08-20_Alias_Impact_June.md"
  - "Operations/Research/2026-08-20_Alias_Impact_June.json"
  - "Operations/Research/2026-08-22_Comparativa_Junio_Julio_Agosto_y_Brechas_Integracion.md"
  - "Operations/Research/2026-08-22_Comparativa_Junio_Julio_Agosto_Datos.json"
  - "Operations/Research/2026-08-22_Comparativa_Junio_Julio_Agosto_Resumen.csv"
  - "Operations/Research/2026-08-22_Comparativa_Junio_Julio_Agosto_Integracion.csv"
  - "Operations/Research/2026-08-14_Diseno_Prueba_Calendario_2_Semanas.md"
organization: "GrowthOS"
---

# Fuente maestra y ledgers del Growth OS

## 1. Decisión de arquitectura

La fuente maestra no debe ser un calendario gigante ni una tabla que repita una pieza cada vez que se publica en otra plataforma. Los agregados mensuales históricos viven en `Operations/Research/Historical_Performance_Snapshot.csv` como capa de referencia y las publicaciones individuales históricas verificables en `Operations/Research/Historical_Performance_Individuals.csv`; ninguna de las dos capas sustituye los ledgers append-only. La arquitectura activa recomendada para Universe Sent Me es **una fuente maestra de contenido más tres ledgers append-only**, cada uno con una función distinta: hechos de publicación, aprendizaje experimental y señales cualitativas de comunidad. Se propone un cuarto ledger append-only de snapshots temporales para conservar E0/E24/E72 sin sobrecargar los ledgers activos; su diseño está en `Review` y no se considera operativo hasta aprobación.

| Capa | Archivo canónico | Qué representa | Quién lo modifica |
|---|---|---|---|
| Identidad y estado de la pieza | `GrowthOS/Content_Inventory.csv` | Una fila por pieza creativa o concepto (`CNT-####`). Contiene personaje, formato, objetivo, hipótesis, canon, producción y elegibilidad de reuse. | Manus prepara; Fernando/Claude aprueban estados protegidos. |
| Historial de publicación | `Operations/Research/2026-08-15_Publication_Log.csv` | Una fila por publicación y plataforma. Conecta pieza, asset, fecha, cuenta, IDs de Meta, permalink, archivado y estado real. | Manus agrega después de cada orden o resultado de Meta. |
| Aprendizaje experimental | `Operations/Research/2026-08-15_ExperimentLog.csv` | Una fila por cohorte, publicación u observación de hipótesis. Contiene métricas, veredicto, conclusión y próxima acción. | Manus agrega datos; CGO/Manus redacta conclusión; Fernando aprueba decisiones de calendario. |
| Comunidad cualitativa | `Operations/Research/2026-08-15_Community_Engagement_Log.csv` | Una fila por comentario real que aporte señal, respuesta humana o decisión de moderación. No guarda identidades personales y complementa, pero no sustituye, el aprendizaje cuantitativo. | Manus agrega datos anonimizados; las respuestas públicas y acciones de moderación requieren aprobación humana. |
| Snapshots temporales — propuesta en Review | `Operations/Research/Metrics_Snapshot_Log.csv` | Una fila por intento/captura E0, E24, E72 u observado lifetime, con contadores crudos, timestamp, tolerancia, raw y estado. No existe todavía como ledger operativo. | Worker E0/E24/E72 después de aprobación; GitHub conserva el artefacto oficial. |

### 1.1 Jerarquía de fuentes de métricas y sincronización

La comprobación del corte 22 de julio–18 de agosto de 2026 probó tres fuentes. La decisión CGO es **no elegir una única fuente para todo**, sino asignar a cada sistema la función en la que ofrece mejor trazabilidad.

| Fuente | Cobertura comprobada | Limitación comprobada | Rol oficial en el Growth OS |
|---|---|---|---|
| Meta Graph API directa | Identidad de Página, cuenta profesional, IDs, publicación y reconciliación de Meta | El token actual carece de `instagram_manage_insights`; la lectura de Insights de Instagram respondió HTTP 400 | Fuente canónica de identidad, IDs, estados de publicación y operaciones Meta |
| Windsor.ai | Consulta masiva de Instagram y Facebook orgánico; Instagram devolvió 34 piezas con engagement, reach, views, saves, shares y watch time de Reels | `post_engagements` de Facebook no es idéntico a `reacciones + comentarios + shares`; la fecha diaria puede normalizarse distinto | Fuente analítica principal para históricos y cortes comparativos, con definición de métrica registrada por conector |
| Conector de Instagram | Lectura de cuenta, lista de publicaciones e Insights por post; coincidió con Windsor en dos Reels y una imagen | Lectura por publicación, paginación y menor eficiencia para lotes grandes | Fuente secundaria de validación puntual y diagnóstico cuando Windsor presente una anomalía |
| Windsor TikTok orgánico | Siete videos deduplicables con views, reach, likes, shares, favoritos, watch time, finalización y seguidores ganados | La respuesta incluye filas nulas repetidas y agregados diarios de cuenta que no deben sumarse con las filas por video | Fuente analítica principal de TikTok, después de deduplicar por `video_id` |
| Windsor YouTube | Seis videos únicos y actividad diaria por video con views, likes, retención y suscriptores | `date` es actividad diaria; `video_view_count` es snapshot lifetime y no debe sumarse por día | Fuente analítica principal de YouTube con tablas separadas diaria y lifetime |

La regla de no duplicación es estricta: una fila de rendimiento debe registrar `fuente_metrica`, `fecha_extraccion`, `definicion_metrica`, `ventana_comparabilidad` y el ID de la publicación. Para Instagram, Windsor es la fuente primaria de análisis hasta que Graph API obtenga `instagram_manage_insights`; el conector confirma muestras, no reemplaza el lote completo. Para Facebook, `Publication_Log.csv` y los datasets Meta conservan como métrica canónica `reacciones + comentarios + shares`; los agregados de Windsor (`post_engagements`) se guardan como métrica alternativa y no se suman con la métrica canónica.

Las recuperaciones puntuales fuera de un corte normalizado se conservan en `Operations/Research/2026-08-19_Publicaciones_Historicas_Adjudicadas.json`. Esta capa solo registra identidad, formato, copy y hora de publicaciones que Fernando confirmó como parte de una cascada; no introduce métricas retrospectivas ni reemplaza la fuente analítica primaria.

Las decisiones humanas que cierran una revisión sin crear una cascada viven en `Operations/Research/2026-08-19_Decisiones_Reconciliacion_Reels.json`. Una versión alternativa puede quedar vinculada a una familia conceptual sin ser el mismo export; una publicación exclusiva cierra la revisión, pero permanece visible como registro individual en el historial.

El corte renovado de 28 días ejecutado el 19 de agosto a las 16:00 se documenta en `Operations/Research/2026-08-19_Corte_Multicanal_28D_1600.md`. Sus artefactos normalizados reemplazan el snapshot operativo vigente, preservando el rango 22 de julio–18 de agosto y sus definiciones de métrica por plataforma.

La comparación entre el snapshot inicial y el renovado del mismo rango se conserva en `Operations/Research/2026-08-19_Comparacion_Snapshots_28D.md`. Este análisis distingue deltas de snapshot de una tendencia temporal: Facebook permanece no comparable mientras Windsor responda desde caché.

Para TikTok y YouTube, el dashboard debe conservar una capa común sin forzar equivalencia semántica: `views` se muestra como views nativas de cada plataforma, `reach` solo se muestra cuando la fuente lo entrega, y `engagement` se calcula como suma documentada de acciones disponibles si no existe una métrica nativa. YouTube debe mostrar por separado la actividad diaria y el snapshot lifetime; TikTok debe eliminar filas repetidas por `video_id` y priorizar la fila con mayor cobertura de métricas.

La ampliación histórica de mayo/junio integró seis matches visuales exactos Drive↔Meta en `Operations/Research/2026-08-21_Reels_Drive_Meta_Crossmatch_Review.csv`: dos Reels individuales de Fantasma, un asset set de dos clips del hombre con hoodie, dos Reels distintos de radio/diálogo y un Reel individual del pato en traje. El video de Wilfred con la poción permanece sin match exacto después de controles negativos; la proximidad de fechas nunca crea una relación de publicación. El historial estructurado contiene ahora 102 registros por plataforma — Facebook 73, Instagram 16, TikTok 7 y YouTube 6 — y la lista CSV derivada conserva una fila por publicación, no por clip de producción. De los 54 candidatos Meta de mayo/junio, seis tienen match visual exacto con Drive y 48 permanecen con asset pendiente. La cola de reconciliación prioriza esos 48 casos restantes; el lote TOP5 revisó 25 candidatos sin match dentro del conjunto analizado, el bloque NEXT10 añadió un match exacto y nueve no-match primarios, y TIER2A añadió dos matches exactos de radio/diálogo y ocho no-match primarios. La clasificación de los seis matches identifica cuatro familias operativas. La prioridad de `Dialogue_radio` fue corregida el 2026-08-22: sus dos assets distintos quedan como observación secundaria porque Fernando reportó menor atención para el formato tipo podcast. La evidencia de mayor valor para la siguiente celda es `Fantasma caminando con gatos`, con snapshots históricos separados de 6,640 y 6,878 views, y el caso reportado de Elara/Wilfred con `POV: Eres Piscis`, pendiente de ID nativo. La nueva celda candidata es `HB-REEL-MOTION-POV-MEME-01`, basada en movimiento físico legible, hook POV o meme reconocible y payoff visual; requiere n≥3 para señal preliminar y n=5 para decisión operativa. El brief operativo de la celda está en `Operations/Production/2026-08-22_Brief_Celda_Reels_Motion_POV_Meme_001.md` y queda `Active` como marco experimental: incorpora el lineamiento `HOOK-H1-ACTION-FIRST` tras el análisis de retención de MPM-001 y conserva MPM-002 v1 Fantasma/gatos como referencia histórica. La revisión v2 de Silvio y la piedra quedó `Archived_Not_Active` tras la indicación de Fernando. El aprendizaje de hook se aplica ahora al caso `CON-2026-08-24-CraveYou-MaeveFeathers`, cuya revisión `HOOK-FIRST-V1` está documentada en `Operations/Production/2026-08-20_Exploracion_Videoclip_Musical_Desamor.md`. El preflight aprobado generó un keyframe de revisión y, tras autorización explícita, un máster vertical sin audio guardado en Drive bajo el experimento MPM. El 2026-08-23 Fernando publicó manualmente la pieza en Facebook e Instagram. Facebook queda reconciliado con Page Post `1036844829507460_122155182621072582`, Reel `2855499098159488`, `is_published=true` y hora local `17:36:57`; Instagram queda registrado con el shortcode `DcZlBYVRiot` y su permalink proporcionado, pero sin ID nativo, hora exacta, caption completo o audio técnicamente confirmados. La disponibilidad nativa de `Crave You` se marca `Reported_By_Owner / Pending_Native_Audio_Readback`. Las métricas de ambas plataformas permanecen separadas y pendientes de corte; no se genera CNT ni se atribuye veredicto experimental. La hipótesis de fatiga por familiaridad visual permanece exploratoria.

La corrección humana del 2026-08-22 separa el asset `Elara y Evan en el Bosque.mp4` del caso Piscis. Ese archivo pertenece a otro Reel más reciente de Elara y Evan juntos en el bosque/campamento y queda en `Pending_reassignment_after_human_correction` hasta vincularlo con su publicación exacta. El concepto cross-platform `CON-2026-08-09-Elara_Evan_Estrellas` conserva sus IDs y copy, pero deja de tener ese asset como evidencia directa.

El 2026-08-22 Fernando reencuadró MPM-001: ya no debe volver a producirse ni publicarse con el texto `POV: Eres Piscis`. La pieza se convierte en la primera variante de la serie `ELARA-WALK-MUSIC-01`, sin texto sobre la imagen. La idea `cuando te hablan pero tú sigues en tu mundo` funciona como dirección conceptual del hook visual, no como overlay. Elara seguirá caminando con audífonos y Wilfred detrás, pero la canción, artista o grupo no se explicará en pantalla ni en el caption; el audio y cualquier hashtag musical se registrarán como campos operativos después de seleccionar la pista. La referencia histórica de Piscis permanece como evidencia de comportamiento reportado, no como copy vigente de MPM-001.

El playbook operativo actualizado el 2026-08-22 establece una banda de 5–7 publicaciones diarias: seis de lunes a jueves, cinco viernes y sábado, y seis el domingo con un séptimo slot exploratorio opcional. La mezcla objetivo es 65%–70% contenido nuevo y 30%–35% reuse, con máximo ordinario de dos reuse diarios, preflight por fila, reserva aprobada y `Slot_No_Publicado` cuando no exista una pieza válida. El calendario activo 17–30 ya contiene 74 slots para 14 días —5.28 asignados por día—, pero con 35 nuevas y 39 reuse, aproximadamente 47.3%/52.7%; por ello la transición no requiere añadir slots ni reescribir el calendario, sino medir su ejecución y aplicar la mezcla objetivo en el siguiente bloque. La cadencia propuesta no modifica el calendario activo ni autoriza publicaciones; requiere aprobación humana y mantiene Reels, Instagram y afiliados fuera del denominador principal de imágenes.

La propuesta de aplicación aprobada el 2026-08-22 queda en `Operations/Research/2026-08-31_Propuesta_Cadencia_5_6_Review.md` y su CSV asociado. La primera selección de cinco assets del inventario `Humor existencial` fue anulada porque Fernando confirmó que ya habían sido publicados. La fuente corregida de contenido nuevo es el target de Drive `Memes` (`1BpKZpUBIT5jBjkvw7epymlsD3Gp4lwzE`), documentado en `Operations/Research/2026-08-22_Drive_Memes_Seed_Inventory.csv` y `2026-08-22_Drive_Memes_Visual_Review_Notes.md`. El bloque piloto del 31 de agosto al 2 de septiembre contiene 15 filas —cinco por día—, 10 conceptos nuevos derivados de semillas y cinco reuse, equivalente a 66.7%/33.3%. Las filas siguen en `Review` y no autorizan programación; las semillas nuevas requieren adaptación original con assets oficiales USM, y los cinco reuse requieren filename y copy verificables. El calendario activo 17–30 no se reescribe ni recibe slots adicionales.

La comparación documentada el 2026-08-22 entre junio, julio y agosto hasta el día 21 confirma que las filas históricas que coinciden con el inventario de Facebook Reels deben excluirse de las tablas estrictamente image-only: 29 en junio, 8 en julio y 8 en agosto 1–14. La nueva unión de agosto contiene 93 imágenes/posts y 11 Reels, deduplicados por Meta Post ID. La vista image-only deja junio en 201 publicaciones y 17,985 interacciones, julio en 199 y 67,727, y agosto 1–21 en 93 y 14,812; las cifras de agosto son cortes observados acumulados, no ventanas exactas. El detalle reproducible está en `Operations/Research/2026-08-22_Comparativa_Junio_Julio_Agosto_y_Brechas_Integracion.md` y sus artefactos. La conclusión operativa es que julio lidera el rendimiento típico, agosto supera a junio pero depende más de pocos outliers, y las brechas pendientes de junio/julio deben resolverse selectivamente, no mediante reconciliación masiva.

La arquitectura también separa **fuente de identidad** y **fuente de rendimiento**. Que una publicación aparezca en Windsor o en el conector no autoriza a publicarla ni cambia su estado de calendario. Que Graph API confirme un ID no convierte automáticamente el total acumulado en una ventana 24/72 horas. Cada snapshot debe conservar su propia fecha y estado de comparabilidad.

La idea clave es que **no todo debe vivir en una sola fila**. Una pieza puede publicarse muchas veces, en varias plataformas y bajo varios experimentos. Si todo se fuerza dentro de `Content_Inventory.csv`, aparecerán columnas repetidas, estados contradictorios y pérdida de historial. El inventario identifica la pieza; `Publication_Log` identifica el hecho de publicación; `ExperimentLog` identifica lo aprendido cuantitativamente; `Community_Engagement_Log` identifica señales cualitativas de conversación y cobertura de respuesta.

## 2. Qué queda como vista y qué deja de ser fuente

Los calendarios semanales, la `Reuse Queue`, la `Production Queue` y la `Approval Queue` deben tratarse como **vistas filtradas** del inventario y de los ledgers. Pueden existir como Markdown o CSV para revisión humana, pero no deben introducir un nuevo estado maestro ni duplicar el historial.

| Vista operativa | Regla de generación |
|---|---|
| Calendario semanal | Filtrar piezas `Aprobado`, sin bloqueo de canon, asignarlas a slots y exportar la orden de publicación. |
| Reuse Queue | Filtrar piezas reutilizables cuya última publicación cumpla la regla de 30 días y ordenar por rendimiento histórico. |
| Production Queue | Filtrar piezas en producción o pendientes de asset; no cambia el estado maestro sin una decisión registrada. |
| Approval Queue | Filtrar piezas con revisión de canon o aprobación de Fernando pendiente. |
| Reporte de aprendizaje | Agrupar `ExperimentLog` por `Experiment_ID`, `Hypothesis_ID`, plataforma, tipo y slot. |
| Reporte de comunidad | Agrupar `Community_Engagement_Log` por `Post_ID`, `CNT_ID`, `Tipo`, `Respuesta_Estado`, prioridad y ventana de revisión. |

El calendario 15–16 de agosto y la propuesta 17–30 permanecen como documentos de planeación/exportación. No deben convertirse en una segunda base de datos permanente.

## 3. IDs mínimos y relaciones

La relación mínima es:

```text
ID_Pieza (CNT-####)
   ├── Asset_Ref / nombre exacto / Drive_ID
   ├── Publicacion_ID → una fila por plataforma y fecha
   │      └── Meta_Post_ID o IG_Media_ID
   ├── Observacion_ID → una fila por experimento, cohorte o resultado
   │      └── Experiment_ID + Hypothesis_ID
   └── Comentario_ID → una fila cualitativa de comunidad, cuando exista
          └── Respuesta_Estado + Accion_Calendario
```

Los códigos `260####` son referencias de asset y no sustituyen automáticamente al `CNT-####`. Cuando todavía no exista una correspondencia confirmada, el campo `ID_Pieza` debe quedar vacío y anotarse como pendiente de reconciliación; no se debe inventar un vínculo.

## 4. Modelo mínimo recomendado

La fuente maestra debe conservar los campos narrativos y de flujo que ya existen en `Content_Inventory.csv`. La próxima migración debe añadir, sin borrar columnas históricas, los siguientes campos normalizados:

| Campo | Uso |
|---|---|
| `ID_Pieza` | Identidad estable de la pieza creativa. |
| `Asset_Ref` | Código `260####` o referencia de asset. |
| `Asset_Filename` | Nombre exacto del archivo. |
| `Drive_ID` | Identificador de Google Drive cuando exista. |
| `Estado_Canon` | `Libre`, `Revision`, `Aprobado`, `Bloqueado`. |
| `Estado_Produccion` | `Idea`, `En_Produccion`, `Asset_Listo`, `Pendiente_Revision`, `Diferido`. |
| `Estado_Publicacion` | `No_Publicada`, `Programada`, `Publicada`, `Archivada`, `Error`. |
| `Ultima_Sincronizacion` | Fecha de la última reconciliación del registro. |
| `Motivo_Revision_Normalizado` | Clasifica por qué una pieza permanece en `Revision` sin convertir el motivo en una aprobación de canon. |

Estos campos deben eliminar la necesidad de interpretar texto libre como “Draft v2”, “pendiente aprobación” o “bloqueado por continuidad” cada vez que se genere un calendario.

### 4.1 Distinción entre canon y reconciliación administrativa

`Estado_Canon` y `estado_canon_normalizado` expresan la condición canónica de la pieza, pero no deben absorber cualquier problema de inventario. `Motivo_Revision_Normalizado` separa las causas que mantienen un registro en revisión:

| Motivo | Uso |
|---|---|
| `Canon_Contradiccion_Sustantiva` | Existe una contradicción narrativa o de diseño que sí requiere revisión canónica. `CNT-004` conserva este motivo, aunque su desarrollo está diferido. |
| `Canon_Aprobacion_Administrativa` | La pieza espera una aprobación o ficha formal, sin que el inventario evidencie una contradicción sustantiva. |
| `Canon_Restriccion_No_Bloqueante` | Existe una regla de continuidad que debe observarse, pero no constituye por sí sola un bloqueo de canon para la capa libre. |
| `Canon_Resuelto_Reconciliacion_Pendiente` | La identidad canónica fue resuelta, pero falta cerrar la relación de inventario o asset. Actualmente: `CNT-009`, cuyo nombre Silvio está confirmado en `8e9fe9a`. |
| `Inventario_Reconciliacion_Pendiente` | Falta una coincidencia CNT↔260/Drive; no es una aprobación creativa. |
| `Identidad_Reconciliada_Sin_Conflicto_Canon_Evidente` | La pieza fue creada o reconciliada a partir de asset, caption y Meta ID, sin evidencia de contradicción canónica. Actualmente: `CNT-031`–`CNT-039`. |

La reclasificación del 15 de agosto dejó **1** registro en `Canon_Review_Required` (`CNT-004`), **4** en `Canon_Constrained`, **1** en `Canon_Partial` y **33** en `Canon_Clear_or_Unverified`. CNT-004 queda fuera de desarrollo por decisión operativa, pero conserva `Estado_Canon=Revision`; cualquier transición a `Aprobado` sigue reservada a Fernando o Claude. La evidencia completa está en `Operations/Research/2026-08-15_Reclasificacion_Canon_vs_Reconciliacion.json`.

## 5. Diseño de bajo consumo de tokens

La operación diaria no debe consultar toda la historia. Manus debe leer el inventario una vez, cargar el calendario del día y consultar únicamente las publicaciones nuevas o modificadas desde el último `Ultima_Sincronizacion`.

El flujo económico es el siguiente:

1. **Antes de publicar:** leer `Content_Inventory.csv` y el calendario aprobado; validar solamente las filas del lote actual.
2. **Durante la publicación:** registrar el resultado en `Publication_Log.csv`; después de confirmar `is_published=true`, capturar E0 en `Metrics_Snapshot_Log.csv` cuando ese ledger sea aprobado. No volver a inspeccionar todo el inventario.
3. **En cada corte diario:** consultar solo las publicaciones nuevas o modificadas desde el último corte, guardar el snapshot observado y extraer aprendizajes de formato, personaje, horario, shares, comentarios, captions y Reels. Cuando el ledger temporal esté activo, el worker seleccionará E24/E72 por `Target_At_UTC`; las métricas de afiliados permanecen en su ledger independiente.
4. **Al cierre del ciclo:** agregar una observación consolidada a `ExperimentLog.csv`, actualizar el veredicto de la hipótesis y generar las colas como vistas.
5. **Para comentarios:** leer solo comentarios nuevos desde el último cursor o ventana; no revisar cada cinco minutos, deduplicar por `Comentario_ID` y no conservar identidades personales. Registrar las señales en `Community_Engagement_Log.csv`.

Esta arquitectura reduce llamadas repetidas, evita que el agente relea documentos largos y permite que cada sesión trabaje con un delta pequeño. El ahorro no proviene de eliminar el aprendizaje; proviene de **no recalcular ni volver a descargar lo que ya está registrado**.

### 5.1 Cadencia recomendada para reportes diarios

La revisión operativa de métricas se hará **diariamente**, idealmente cerca de las **22:00 de America/Matamoros**, porque el corte incluye las publicaciones reales acumuladas durante el día y permite extraer aprendizaje sin esperar una ventana contractual. El reporte diario `Operations/Research/2026-08-21_Corte_Diario_Metricas_2200.md` es la plantilla de referencia: registra fecha/hora de captura, rango cubierto, publicaciones reales, formato, reacciones, comentarios, shares, interacciones observables, cruces con `Publication_Log`, Reels y limitaciones de la fuente.

Cada reporte diario debe producir una lectura estratégica breve: qué piezas lideraron, qué proporción corresponde a shares, qué personajes o tratamientos aparecen en los líderes, qué formatos tienen señales de descubrimiento, qué comentarios requieren atención y qué hipótesis merecen una nueva prueba. Estas lecturas se incorporan al `ExperimentLog.csv` como observaciones `Corte_Diario` cuando respondan una pregunta concreta, conservando `ventana_comparabilidad=Corte_Observado` en la nota y sin presentarlas como incrementos entre días.

Los cortes diarios **no requieren ventanas exactas de 24/72 horas**. Sus acumulados lifetime observables son válidos para seguimiento operativo, ranking y aprendizaje direccional, siempre que se conserve la fecha de extracción y no se calculen como delta diario. Facebook, Instagram, Reels y afiliados deben permanecer en capas separadas; las métricas no disponibles se registran como ausentes, nunca se estiman.

### 5.2 Ventanas exactas como capa contractual opcional

Las ventanas exactas de 24 y 72 horas se mantienen únicamente cuando un experimento comparable las necesite para un cierre contractual o para comparar publicaciones con una definición temporal idéntica. En ese caso, se consultan solo los `Meta_ID` vencidos, idealmente en lote. Cada fila conserva su hora real y, si Meta no permite reconstruir el snapshot, se registra `24h_snapshot_unavailable` o `72h_snapshot_unavailable` sin inventar el valor [7] [8]. La ausencia de una ventana exacta no bloquea el reporte diario ni elimina sus aprendizajes; solo limita el veredicto formal de esa celda experimental.

La propuesta `Operations/Automation/2026-08-23_Diseno_Captura_Baseline_E0_E24_E72.md` define el cuarto ledger `Metrics_Snapshot_Log.csv`, el hook posterior a `is_published=true`, la cola de posts programados, la opción de Webhook para publicaciones manuales, las tolerancias y las claves idempotentes. Mientras el diseño esté en Review, los campos `Interacciones_24h`/`Interacciones_72h` permanecen bajo el contrato actual y no se crea ningún schedule nuevo.

El flujo económico queda así: un corte diario alimenta el aprendizaje operativo y las decisiones de contenido; una consulta adicional de 24/72 horas se ejecuta solo cuando una celda comparable, P0 u otra revisión formal la requiera. De este modo, el Growth OS aprende de los datos disponibles cada día sin confundir `Corte_Observado`, `lifetime_actual` y `snapshot_24_72h`.

### 5.1 Estado de conectividad y materialización observado el 24 de agosto de 2026

La auditoría de conectividad confirma que la arquitectura de ledgers está vigente, pero no todos sus puntos de entrada están operativos en la configuración actual. `Metrics_Snapshot_Log.csv` todavía no existe, por lo que E0/E24/E72 no se pueden capturar como ledger append-only y las columnas temporales del `Publication_Log`/`ExperimentLog` permanecen vacías bajo el contrato correcto. El conector `Universe Sent Me Meta API` existe con credencial cifrada, pero está deshabilitado; Instagram está habilitado con tres cuentas conocidas y ninguna cuenta activa; Meta Ads Manager aparece habilitado pero la llamada devuelve `not connected`; Google Calendar no tiene scopes suficientes; y no existe un schedule recurrente activo en la sesión auditada.

Google Drive/Sheets sí responde en lectura, pero la hoja `USM Growth OS` fue modificada por última vez el 8 de agosto de 2026 y su Dashboard conserva esa fecha. Por tanto, la hoja debe tratarse como artefacto histórico o auxiliar hasta que exista una sincronización explícita; GitHub continúa siendo la fuente oficial de verdad. La evidencia sanitizada está en `Operations/Research/2026-08-24_Growth_Connectivity_Audit_Evidence.json` y no autoriza cambios de configuración ni publicaciones.

## 6. Primer estado implementado

El `ExperimentLog` contiene observaciones históricas, nueve publicaciones reales de Facebook del 15–16 de agosto y tres publicaciones activas confirmadas de Instagram: `2608030`, `2608036` y `2608060`. Además, registra seis IDs proporcionados por Fernando para duplicaciones Instagram 17–30 (`260633`, `260560`, `260614`, `260625`, `260613` y `260528`) con estado prudente `Programada`, sin permalink ni hora real inventados. La fila histórica de `260633` con media `17943879225288953` permanece como `Eliminada_Manualmente`; el nuevo ID `1564061365193135` se conserva como registro separado. Ninguna de estas filas recibe un CNT inventado; permanecen con `ID_Pieza` vacío hasta una reconciliación con evidencia suficiente. El `Publication_Log` enlaza las nueve publicaciones de Facebook con `CNT-031`–`CNT-039`, conserva intentos históricos de Instagram eliminados manualmente y separa publicaciones activas confirmadas de programaciones con ID proporcionado. Las métricas 24/72 horas de Facebook siguen pendientes cuando Meta no permite reconstruir el snapshot exacto. Para históricos y cortes de publicación, Instagram ya tiene evidencia analítica de Windsor y validación puntual del conector; el estado de cada fila debe distinguir entre `lifetime_actual`, `corte_observado` y `snapshot_24_72h`.

El `Community_Engagement_Log.csv` contiene 18 comentarios reales: nueve del primer lote, seis del delta del 16 de agosto, dos del delta del 17 de agosto y una revisión puntual de publicación. Las cuatro respuestas del primer lote y la respuesta puntual fueron aceptadas por Meta; la respuesta puntual tiene `Respuesta_Meta_ID=122148874563072582_1613678620282915`, aunque su verificación GET devolvió HTTP 403 por permisos. La muestra histórica de 67 comentarios se conserva como análisis agregado y no se transforma retroactivamente en filas. Las futuras revisiones deben recuperar solo el delta nuevo, deduplicar por `Comentario_ID` y mantener respuestas y moderación bajo aprobación humana.

El lote 1 de normalización cubrió inicialmente 28 filas y, tras resolver las excepciones, `Content_Inventory.csv` llegó a 30 registros. La reconciliación del calendario 15–16 añadió nueve piezas de identidad nuevas, por lo que el inventario llegó a 39 registros. La integración histórica de mayo añadió `CNT-040`–`CNT-067`, y la reconciliación visual de junio añadió `CNT-068` para `260724`, por lo que el inventario contiene ahora 68 registros. Se preservaron todas las columnas originales y se añadieron campos normalizados para estado operativo, estado de canon, asset confirmado, asset candidato, relaciones y trazabilidad de reconciliación. Los CNT históricos nuevos no constituyen aprobación canónica ni publicación activa.

`CNT-002 → 260509` quedó resuelto como `Resolved_Production_Set`: Meta identificó el post `1036844829507460_122143141185072582`, publicado el 30 de julio a las 14:16:47 UTC, con permalink `https://www.facebook.com/reel/911880681976378/`. El reel dura 17.39 segundos y su secuencia coincide con los tres videos de producción de Wilfred/caja/peluche localizados en Drive. El archivo 260509 de Drive corresponde a Universe existencial y se mantiene rechazado. No existe un render final `260####` confirmado, así que no se inventa uno.

`CNT-023` quedó resuelto como `Resolved_Asset_Set`: el episodio 2 de “¿Qué me llegó?” se relaciona con la carpeta de Drive `Elara - Lampara de luna`, que contiene 7 assets verificados: cuatro piezas de video/imagen de entrega y apertura de paquete, más tres renders de secuencia. El registro conserva los siete nombres en `asset_set`, no se fuerza a un único `260####` y se enlaza con `CNT-002`, el episodio 1. La publicación de Facebook quedó confirmada con Page Post ID `1036844829507460_122147352825072582`, Reel ID `1067337609170026`, permalink `https://www.facebook.com/reel/1067337609170026/` y fecha local 2026-08-08 19:19:54.

`CNT-029` y `CNT-030` fueron incorporados desde sus documentos reales de producción. CNT-029 es el reel “Pausa para ver qué piensa de ti”, con banco de 9 cuadros, hook de pausa y estado `Draft_Pending_Approval`; la búsqueda acotada de Meta del 14–17 de agosto no encontró una publicación coincidente. CNT-030 es su especificación dependiente de audio y montaje, también `Draft_Pending_Approval`, no una publicación independiente. Ambos quedan enlazados entre sí, conservan sus nombres de assets documentados y no reciben referencias 260 inventadas.

El preview actualizado está en `Operations/Research/2026-08-15_Reconciliacion_Lote_01_Preview.md` y el CSV detallado en `Operations/Research/2026-08-15_Reconciliacion_Lote_01_Preview.csv`. CNT-023 conserva además el `drive_reference_id` de la carpeta de producción, el listado exacto de sus siete assets y la publicación confirmada en `Publication_Log.csv`. CNT-029/CNT-030 conservan sus bancos de assets y no generan filas de publicación hasta que exista aprobación y un permalink real. La normalización es reversible porque `estado` y `bloqueado_canon` originales permanecen intactos. CNT-002 ya no tiene una excepción abierta a nivel de publicación ni de conjunto de producción. Solo queda registrada la ausencia del nombre del render final como archivo `260####`, lo cual no bloquea la integridad de los 39 registros actuales.

## 7. Estado de unificación — lote 1

El 15 de agosto de 2026 se aplicó el primer lote de unificación al inventario maestro. Después de reconciliar el calendario 15–16, `Content_Inventory.csv` conserva sus 39 filas y todos los campos históricos, y contiene siete campos canónicos derivados: `Asset_Ref`, `Asset_Filename`, `Drive_ID`, `Estado_Canon`, `Estado_Produccion`, `Estado_Publicacion` y `Ultima_Sincronizacion`.

| Campo canónico | Regla aplicada en el lote 1 |
|---|---|
| `Asset_Ref` | Copia únicamente de `asset_ref_confirmado`; queda vacío si no existe evidencia confirmada. |
| `Asset_Filename` | Usa el conjunto de assets documentado cuando existe; no convierte nombres de producción en un falso `260####`. |
| `Drive_ID` | Deriva de `drive_reference_id`. |
| `Estado_Canon` | Normaliza el estado existente a `Revision` o `Restringido`; no aprueba canon automáticamente. |
| `Estado_Produccion` | Normaliza ideas, producción pendiente, revisión, reuse, bloqueo y publicación sin borrar el texto original. |
| `Estado_Publicacion` | Marca `Publicada` solo cuando existe `meta_publication_id`; el resto queda `No_Publicada`. |
| `Ultima_Sincronizacion` | Fecha del lote: `2026-08-15`. |

La validación posterior al lote reconcilió 39 IDs únicos, 11 piezas con publicación Meta enlazada (`CNT-002`, `CNT-023` y `CNT-031`–`CNT-039`) y 28 piezas sin publicación confirmada. Se preservaron los estados históricos y no se confirmó ningún asset `260####` sin evidencia.

La unificación todavía no está completa. Los siguientes trabajos quedan explícitamente separados para evitar una migración riesgosa: completar métricas 24/72 horas en `Publication_Log`, cerrar el aprendizaje de `HB-003`, `HB-004` y `HB-005`, convertir calendarios/colas en exportaciones verificables del inventario y poblar progresivamente el `Community_Engagement_Log` con comentarios reales. `CNT-004` queda diferido y no forma parte del lote activo de desarrollo; si se retoma, requerirá revisión canónica y aprobación. El mapeo de las nueve órdenes del calendario 15–16 ya está cerrado mediante `CNT-031`–`CNT-039`. Estos pendientes restantes son de medición, integración, comunidad y aprobación; no deben resolverse inventando IDs.

## Estado operativo del lote MEME-CAD-001–005

El 22 de agosto de 2026 Fernando aprobó cinco semillas del target Drive/Memes para adaptación original: `DRIVE-MEME-001`, `DRIVE-MEME-002`, `DRIVE-MEME-003`, `DRIVE-MEME-005` y `DRIVE-MEME-006`. `MEME-CAD-001` y `MEME-CAD-002` conservan sus renders v1. `MEME-CAD-003` y `MEME-CAD-004` mantienen como candidatas activas las v3: Silvio molesto con piedra-kármica en el escenario tarotista y Wilfred alto/delgado con bastón oficial frente al tablero de discusión. `MEME-CAD-005` pasa a v4 para corregir la frase central de la publicación: Evan queda conectado a seis hombres más que interpretan la misma indirecta y todos piensan que es para ellos.

Los estados y los IDs de producción están registrados en `Operations/Research/2026-08-22_Drive_Memes_Seed_Inventory.csv` y documentados en `Operations/Production/2026-08-22_Briefs_Cadence_Memes_Seed_Adaptations.md`. Los cinco assets están aprobados y viven en Drive, carpeta `Produccion_Memes_Cadencia_2026-08-22` (ID `10vtYpPfcRnV3RnlAt9mshLRKv78dOS53`). `MEME-CAD-003` y `MEME-CAD-004` usan sus v3; `MEME-CAD-005` usa v4 con la pregunta exacta `¿Cómo voy a saber si la indirecta es para mí?`. Las referencias oficiales consultadas proceden de `Elementos/LUGARES`, `Elementos/PROPS` y `Elementos/PERSONAJES`. `MEME-CAD-002`, `MEME-CAD-003` y `MEME-CAD-004` están programados como reemplazos verificados; `MEME-CAD-001` y `MEME-CAD-005` están programados como slots adicionales verificados.

La máquina de estados queda: `CNT_Status=Not_Created`, `Calendar_Status=Cadence_Expanded_22_30`, `Publication_Status=Scheduled_Meta_Verified` para los cinco MEME-CAD, `Affiliate_Attachment=No` e Instagram/Reels separados. Las capturas fuente no son publicables; los renders históricos supersedidos se conservan solo para trazabilidad. Los cuatro slots adicionales fueron verificados con `is_published=false`.

## Ejecución de ampliación de cadencia 22–30 de agosto

La auditoría y ampliación del calendario encontró 50 filas entre el 22 y el 30 de agosto: 26 `Nueva`, 21 `Reuse_Top` y 3 `Reuse_Reserve`, para un promedio de 5.56 slots diarios. La operación añadió cuatro slots y llevó cada día del tramo a 5 o 6 publicaciones. La evidencia permanente está en `Operations/Research/2026-08-22_Cadence_Expansion_22_30_Execution.json`; los cuatro posts fueron verificados en Meta con `is_published=false`.

La ampliación fue autorizada por Fernando como decisión operativa de recuperación de cadencia, sin esperar al cierre mensual. Facebook quedó como única plataforma; Instagram, Reels y afiliados permanecen separados. `CNT_Status=Not_Created`, no se cancelaron posts en esta ampliación, no se movieron originales en Drive y los cuatro nuevos slots quedaron `Programada_Meta_Verificado`. El análisis conserva la cautela metodológica: la caída de agosto frente a julio justifica actuar, pero no se registra como causalidad absoluta aislada de mezcla, frecuencia y concentración de outliers.

## Ejecución autorizada de reemplazos MEME-CAD — 22 de agosto de 2026

Fernando aprobó los cinco assets MEME-CAD y confirmó el reemplazo de tres reuse en Facebook. Se cancelaron y verificaron ausentes de `scheduled_posts` los posts salientes de `2026-08-24 16:00`, `2026-08-26 17:00` y `2026-08-27 17:00`. En sus mismos horarios se programaron `MEME-CAD-004`, `MEME-CAD-002` y `MEME-CAD-003`; los tres nuevos posts tienen `is_published=false` y Meta confirmó sus horarios. La evidencia permanente está en `Operations/Research/2026-08-22_MEME_CAD_Replacements_Execution.json`, con los IDs de Page Post y Photo.

La máquina de estados queda: `CNT_Status=Not_Created`, `Calendar_Status=Cadence_Expanded_22_30`, `Publication_Status=Scheduled_Meta_Verified` para los tres reemplazos y los cuatro slots adicionales, `Affiliate_Attachment=No`, Instagram/Reels separados y `Drive_Moved=No`. `MEME-CAD-001` y `MEME-CAD-005` quedaron programados en los slots adicionales del 28 y 29.

### Dependencias de coherencia

El brief de producción y el inventario de semillas son los registros detallados. La propuesta 23–30 en `Operations/Research/2026-08-23_Propuesta_Cadencia_23_30_MEME-CAD_Review.md` y su CSV asociado conservaron la vista de revisión y ahora registran la ejecución parcial/completa del bloque. El calendario activo y `2026-08-22_Cadence_Expansion_22_30_Execution.json` son la evidencia operativa; el changelog y esta fuente maestra son las vistas de sincronización. Las filas fueron actualizadas después de existir assets finales y autorización explícita por fila.

## 8. Reglas de gobernanza

`Content_Inventory.csv` es la fuente de identidad de las piezas. `Publication_Log.csv` es el historial de hechos y no debe sobrescribirse para “limpiar” errores; se corrigen mediante una columna de nota o una nueva entrada de corrección. `ExperimentLog.csv` es el registro de aprendizaje y no debe llenarse con hipótesis inventadas ni con métricas estimadas. `Community_Engagement_Log.csv` es la capa cualitativa y no debe llenarse con identidades personales, comentarios inventados o respuestas no verificadas.

Los estados de canon y aprobación no se cambian automáticamente. Fernando o Claude conservan la autoridad sobre canon y aprobación final. Manus puede validar, agregar datos, preparar vistas y documentar resultados, pero no convertir una propuesta en canon ni marcar una pieza bloqueada como aprobada.

## Referencias

[1]: `01_00_Arquitectura_Calendario_Escalable.md` — Arquitectura de metadatos, estados y calendario como vista.
[2]: `13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md` — Formato de exportación y publicación mediante Meta Graph API.
[3]: `Integracion_Growth_OS.md` — HypothesisBank, ExperimentLog y puente con canon.
[4]: `Content_Inventory.csv` — Inventario actual de 39 piezas, estados históricos y campos canónicos derivados.
[5]: `../Operations/Research/2026-08-15_Publication_Log.csv` — Primer ledger de publicaciones implementado.
[6]: `../Operations/Research/2026-08-15_ExperimentLog.csv` — Primer ledger experimental implementado.
[7]: https://developers.facebook.com/docs/graph-api/reference/post/insights/ — parámetros `since`, `until`, `period` y métricas de Post Insights.
[8]: https://developers.facebook.com/documentation/pages-api/platforminsights/page — limitaciones y actualización de Page Insights.
[9]: `../Operations/Research/2026-08-15_Reclasificacion_Canon_vs_Reconciliacion.json` — distribución de motivos de revisión canónica y administrativa.


## 9. Tabla de aliases de publicación — 2026-08-20

La tabla `Operations/Research/2026-08-20_Source_Alias_Table.csv` funciona como una capa de reconciliación entre el `Publication_Log` y `Content_Inventory`. Extrae una clave numérica de `Asset_Ref` o del filename operativo y conserva el `Inventory_ID`, `Drive_ID`, `Meta_Post_ID`, permalink, plataforma y estado de publicación. No crea CNT y no convierte una coincidencia de filename en aprobación canónica.

El primer corte contiene 98 filas del Publication Log. Se obtuvieron 52 coincidencias únicas de alta confianza, 46 filas con revisión o sin match y 3 filas sin clave numérica extraíble. Las filas `Review` deben resolverse mediante evidencia adicional de Drive/Meta o conservarse como excepciones explícitas. La tabla es la vista oficial de alias hasta que la fuente maestra incorpore una columna normalizada de alias.

## 10. Vista consolidada del histórico individual de junio — 2026-08-20

`Operations/Research/Historical_Performance_Individuals.csv` permanece como archivo fuente y no se elimina ni se reescribe para borrar duplicados. Para rankings, sumas y comparaciones se debe utilizar `Operations/Research/2026-08-20_Historical_Performance_Individuals_Consolidated.csv`, que reduce 211 filas fuente a 206 publicaciones lógicas.

Se identificaron cinco grupos duplicados de Meta ID. Cada grupo tiene dos filas fuente con métricas de reacciones, comentarios y shares consistentes. La vista consolidada conserva `source_row_ids`, `sources_observed`, asset refs observados y candidatos de inventario para que la pérdida de filas no implique pérdida de evidencia.

La regla queda establecida: **una publicación lógica por Meta ID en agregados; todas las filas fuente conservadas para auditoría**. Esta vista no modifica canon, no crea CNT y no sustituye los ledgers de publicación o experimentación.

## 11. Deuda residual de fuente maestra

La tabla de aliases reduce el problema de falsos huérfanos, pero no lo resuelve completamente. Las 46 filas `Review` requieren resolución posterior por evidencia; las cinco filas P0 deben enlazarse al inventario o mantenerse como excepción documentada. La consolidación histórica permite corregir doble conteo en junio, pero no autoriza recalcular ventanas 24/72 horas ni mezclar lifetime con cortes experimentales.


## 12. Asociación de los cinco assets P0 — 2026-08-20

El registro `Operations/Research/2026-08-20_P0_Asset_Association_Register.csv` cruza los cinco rows del baseline P0 con la tabla de aliases y el inventario. `260633` quedó asociado a `CNT-062` y `260642` a `CNT-064`, ambos con alta confianza. `2608028`, `2608034- Elara` y `2608027.jpeg` no tienen fila en `Content_Inventory`, aunque sus Meta Post IDs y archivos visuales locales están preservados como excepciones. No se crearon CNT ni se cambió canon.

## 13. Resolución parcial de aliases 17–30 — 2026-08-20

La programación 17–30 contiene 81 filas en la tabla de aliases; 43 permanecen en `Review`. La revisión de evidencia local encontró 33 assets con identidad verificable en `calendar_visual_review_20260816`, pero sin fila de inventario, y 10 sin evidencia local en esa carpeta. La identidad de asset verificada no equivale a asociación CNT: las 33 filas quedan listas para una decisión administrativa de inventario y las 10 requieren evidencia adicional de Drive/Meta o del usuario.

La vista enriquecida está en `Operations/Research/2026-08-20_17_30_Alias_Evidence_Enriched.csv`. Hasta que se apruebe la normalización, cada publicación conserva su Meta ID, permalink, fecha y estado en el alias; `Content_Inventory.csv` no se modifica automáticamente.


## 14. Capa staging de aliases de inventario — 2026-08-20

Se creó `Operations/Research/2026-08-20_Inventory_Alias_Staging_17_30.csv` con 33 assets cuya identidad visual está verificada, pero cuya fila de inventario todavía no existe. La capa staging conserva Alias ID, publicación, Meta Post ID, permalink, fecha/hora, ruta de evidencia y SHA-256. Tiene `CNT_Creation_Allowed=No`, no modifica `Content_Inventory.csv` y no produce impacto de canon.

La función de esta capa es separar tres conceptos que no deben mezclarse: identidad del archivo, asociación administrativa al inventario y creación editorial de un CNT. Solo los dos primeros pueden resolverse automáticamente; el tercero requiere aprobación y reconciliación.

## 15. Casos que no aparecieron en la evidencia local inicial

La búsqueda ampliada localizó archivos para los diez casos que inicialmente no aparecían en `calendar_visual_review_20260816`. `260508` tiene dos variantes y dos candidatos de inventario (`CNT-042` y `CNT-043`); los otros ocho tienen un archivo local, pero no una fila de inventario correspondiente. La tabla de opciones está en `Operations/Research/2026-08-20_10_Cases_Resolution_Options.csv`.

La ruta recomendada es validar primero los dos filenames de `260508` contra sus candidatos existentes y, después, mantener los otros ocho como aliases staging de evidencia. No se debe crear CNT ni escoger inventario por personaje, similitud visual o nombre parcial.


## 16. Matches 260508 y aprobación de aliases no-CNT — 2026-08-20

Se validaron dos aliases de `260508` por filename exacto y evidencia local independiente. `ALIAS-0036` se mapea a `CNT-042` (`260508 - Universe.jpg`) y `ALIAS-0047` se mapea a `CNT-043` (`Universe - Existencial 260508.png`). Ambos pasan a `Confidence=High` y quedan cerrados para este corte; no se creó CNT.

Las ocho filas restantes con archivo local pero sin fila de inventario se prepararon en `Operations/Research/2026-08-20_NonCNT_Inventory_Alias_Approval.csv`. Todas están en `Pending_Admin_Approval`, con `Proposed_Record_Type=Inventory_Alias_NonCNT`, `CNT_Creation_Allowed=No` y `Canon_Impact=None`. La aprobación solicitada solo autoriza normalizar la relación administrativa del alias; no autoriza crear CNT ni modificar canon.


## 17. Aprobación administrativa de aliases no-CNT — 2026-08-20

Fernando aprobó las ocho filas de `Operations/Research/2026-08-20_NonCNT_Inventory_Alias_Approval.csv`. Su estado pasa a `Approved_Admin`; la aprobación solo autoriza conservar la relación administrativa del alias con su publicación y evidencia local. Se mantienen `CNT_Creation_Allowed=No` y `Canon_Impact=None`. `Content_Inventory.csv` no se modifica en este paso.

## 18. Impacto de aliases en las métricas de junio — 2026-08-20

El análisis de `Operations/Research/2026-08-20_Alias_Impact_June.md` confirma que la actualización de aliases no cambia los Meta IDs ni añade interacciones históricas. Los dos aliases resueltos de `260508` corresponden a publicaciones de mayo, no de junio; por tanto, su impacto directo sobre los agregados de junio es cero. Las ocho aprobaciones `Approved_Admin`, la capa staging de 33 assets y las excepciones P0 pertenecen a la operación de agosto y tampoco deben incorporarse a las métricas históricas de junio.

El control de calidad mantiene separadas dos preguntas: **cuánto rindió junio** y **a qué CNT/asset puede atribuirse cada resultado**. Para la primera, los agregados deben calcularse sobre la vista consolidada: 172 publicaciones lógicas y 17,334 interacciones en el corte actual, no sobre las 177 filas fuente que contienen cinco duplicados. Para la segunda, la resolución de `260508` mejora la precisión de atribución de sus 17 interacciones totales, repartidas como 9 en `CNT-042` y 8 en `CNT-043`, sin cambiar la suma mensual.

La regla operativa queda establecida: una reconciliación administrativa puede cambiar la clasificación por asset/CNT y la elegibilidad para análisis de reuse, pero no reescribe métricas de publicación ni se mezcla con P0, afiliados o ventanas 24/72 horas.

## 19. Convención activa de ciclo semanal — domingo a sábado

Fernando confirmó la adopción de la convención de reporte y aprendizaje domingo–sábado. El domingo abre el ciclo editorial y el sábado lo cierra después del último slot; la regla no reescribe cortes mensuales ni cambia por sí sola la programación, los denominadores de plataforma o las aprobaciones requeridas. El reporte semanal se construye a partir de los reportes diarios del bloque completo y prioriza la mediana por publicación, shares, comentarios, formato, volumen, mezcla nuevo/reuse y alcance cuando exista.

El primer cierre bajo esta convención corresponde al bloque **domingo 16 a sábado 22 de agosto de 2026**. Su extracción raw, cruce con el calendario, resumen CSV y análisis general quedan en `Operations/Research/2026-08-22_Weekly_Metrics_20260816_20260822_Raw.json`, `Operations/Research/2026-08-22_Weekly_Metrics_20260816_20260822_Joined.csv`, `Operations/Research/2026-08-22_Analisis_Semanal_20260816_20260822.csv` y `Operations/Research/2026-08-22_Analisis_Semanal_20260816_20260822.md`. La observación `OBS-WEEKLY-20260816-20260822` se añadió al `ExperimentLog.csv` como `Cierre_Semanal`, sin ventanas 24/72h. Las actualizaciones de `00_Índice.md`, `01_00_Arquitectura_Calendario_Escalable.md`, `04_00_Formato_Calendario_Semanal_CGO.md`, `06_00_Reglas_Aprendizaje_Tendencias.md` y la propuesta activada conservan la misma regla.

## 20. Corte diario de métricas — 2026-08-22 22:02

El corte diario de Meta recuperó seis publicaciones reales del 22 de agosto: cinco imágenes/posts y un Reel. Las imágenes sumaron 127 interacciones conocidas y el Reel 18; las cifras son acumulados observables al momento de la captura, no incrementos exactos de 24 horas. El slot adicional de `CNT-083` a las 22:00 acababa de publicarse, no expuso shares y queda fuera de cualquier lectura de rendimiento hasta contar con suficiente exposición.

El post de las 10:00 (`2608050`) lideró las imágenes con 51 interacciones conocidas y 8 shares. `260589` lideró comentarios con 12. Las dos piezas nuevas `2608050` y `2608063` todavía no tienen reconciliación taxonómica permanente; `260589` permanece como personaje no identificado, `260510` como Universe con confianza alta y `CNT-083/2607828` como Ganso con confianza alta. No se atribuye el resultado a un personaje o familia aislada.

El Reel `MPM-001` —Elara caminando con audífonos y Wilfred detrás— quedó en nivel L1 observable con 18 interacciones básicas. Meta no expuso views, reach ni retención en esta extracción; por eso no se compara con imágenes ni se evalúa formalmente la celda `HB-REEL-MOTION-POV-MEME-01`. Afiliados conserva su ledger independiente y no se sumó al engagement editorial.

Los documentos operativos permanentes son `Operations/Research/2026-08-22_Corte_Diario_Metricas_2200.md`, su CSV y raw, y `Operations/Research/2026-08-22_Analisis_Corte_Diario_Familias_Personajes.md` con su CSV. La observación `OBS-DAILY-20260822-2200` se añadió al `ExperimentLog.csv` como `Corte_Observado`, sin campos 24/72h. Las filas de publicación observadas se añadieron de forma append-only al `Publication_Log.csv`; no se reescribieron hechos históricos ni se modificaron calendario, canon, Reels o afiliados.
