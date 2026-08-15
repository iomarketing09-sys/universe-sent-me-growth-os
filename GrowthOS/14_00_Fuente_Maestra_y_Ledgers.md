---
title: "Fuente maestra y ledgers del Growth OS"
purpose: "Definir una arquitectura mínima y unificada para que inventario, publicaciones, calendarios y aprendizaje compartan IDs sin duplicar datos ni repetir consultas innecesarias."
status: Active
created: 2026-08-15
updated: 2026-08-15
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "GrowthOS/01_00_Arquitectura_Calendario_Escalable.md"
  - "GrowthOS/Integracion_Growth_OS.md"
  - "GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md"
  - "GrowthOS/Content_Inventory.csv"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "Operations/Research/2026-08-15_ExperimentLog.csv"
  - "GrowthOS/00_Índice.md"
organization: "GrowthOS"
---

# Fuente maestra y ledgers del Growth OS

## 1. Decisión de arquitectura

La fuente maestra no debe ser un calendario gigante ni una tabla que repita una pieza cada vez que se publica en otra plataforma. La arquitectura recomendada para Universe Sent Me es **una fuente maestra de contenido más dos ledgers append-only**:

| Capa | Archivo canónico | Qué representa | Quién lo modifica |
|---|---|---|---|
| Identidad y estado de la pieza | `GrowthOS/Content_Inventory.csv` | Una fila por pieza creativa o concepto (`CNT-####`). Contiene personaje, formato, objetivo, hipótesis, canon, producción y elegibilidad de reuse. | Manus prepara; Fernando/Claude aprueban estados protegidos. |
| Historial de publicación | `Operations/Research/2026-08-15_Publication_Log.csv` | Una fila por publicación y plataforma. Conecta pieza, asset, fecha, cuenta, IDs de Meta, permalink, archivado y estado real. | Manus agrega después de cada orden o resultado de Meta. |
| Aprendizaje experimental | `Operations/Research/2026-08-15_ExperimentLog.csv` | Una fila por cohorte, publicación u observación de hipótesis. Contiene métricas, veredicto, conclusión y próxima acción. | Manus agrega datos; CGO/Manus redacta conclusión; Fernando aprueba decisiones de calendario. |

La idea clave es que **no todo debe vivir en una sola fila**. Una pieza puede publicarse muchas veces, en varias plataformas y bajo varios experimentos. Si todo se fuerza dentro de `Content_Inventory.csv`, aparecerán columnas repetidas, estados contradictorios y pérdida de historial. El inventario identifica la pieza; `Publication_Log` identifica el hecho de publicación; `ExperimentLog` identifica lo aprendido.

## 2. Qué queda como vista y qué deja de ser fuente

Los calendarios semanales, la `Reuse Queue`, la `Production Queue` y la `Approval Queue` deben tratarse como **vistas filtradas** del inventario y de los ledgers. Pueden existir como Markdown o CSV para revisión humana, pero no deben introducir un nuevo estado maestro ni duplicar el historial.

| Vista operativa | Regla de generación |
|---|---|
| Calendario semanal | Filtrar piezas `Aprobado`, sin bloqueo de canon, asignarlas a slots y exportar la orden de publicación. |
| Reuse Queue | Filtrar piezas reutilizables cuya última publicación cumpla la regla de 30 días y ordenar por rendimiento histórico. |
| Production Queue | Filtrar piezas en producción o pendientes de asset; no cambia el estado maestro sin una decisión registrada. |
| Approval Queue | Filtrar piezas con revisión de canon o aprobación de Fernando pendiente. |
| Reporte de aprendizaje | Agrupar `ExperimentLog` por `Experiment_ID`, `Hypothesis_ID`, plataforma, tipo y slot. |

El calendario 15–16 de agosto y la propuesta 17–30 permanecen como documentos de planeación/exportación. No deben convertirse en una segunda base de datos permanente.

## 3. IDs mínimos y relaciones

La relación mínima es:

```text
ID_Pieza (CNT-####)
   ├── Asset_Ref / nombre exacto / Drive_ID
   ├── Publicacion_ID → una fila por plataforma y fecha
   │      └── Meta_Post_ID o IG_Media_ID
   └── Observacion_ID → una fila por experimento, cohorte o resultado
          └── Experiment_ID + Hypothesis_ID
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
| `Estado_Produccion` | `Idea`, `En_Produccion`, `Asset_Listo`, `Pendiente_Revision`. |
| `Estado_Publicacion` | `No_Publicada`, `Programada`, `Publicada`, `Archivada`, `Error`. |
| `Ultima_Sincronizacion` | Fecha de la última reconciliación del registro. |

Estos campos deben eliminar la necesidad de interpretar texto libre como “Draft v2”, “pendiente aprobación” o “bloqueado por continuidad” cada vez que se genere un calendario.

## 5. Diseño de bajo consumo de tokens

La operación diaria no debe consultar toda la historia. Manus debe leer el inventario una vez, cargar el calendario del día y consultar únicamente las publicaciones nuevas o modificadas desde el último `Ultima_Sincronizacion`.

El flujo económico es el siguiente:

1. **Antes de publicar:** leer `Content_Inventory.csv` y el calendario aprobado; validar solamente las filas del lote actual.
2. **Durante la publicación:** registrar el resultado en `Publication_Log.csv`; no volver a inspeccionar todo el inventario.
3. **A las 24 y 72 horas:** consultar métricas solo para los `Meta_ID` nuevos del lote, idealmente en una llamada paginada o agrupada; no volver a pedir publicaciones históricas completas.
4. **Al cierre del ciclo:** agregar una observación consolidada a `ExperimentLog.csv`, actualizar el veredicto de la hipótesis y generar las colas como vistas.
5. **Para comentarios:** leer solo comentarios nuevos desde el último cursor o ventana; no revisar cada cinco minutos y no conservar identidades personales.

Esta arquitectura reduce llamadas repetidas, evita que el agente relea documentos largos y permite que cada sesión trabaje con un delta pequeño. El ahorro no proviene de eliminar el aprendizaje; proviene de **no recalcular ni volver a descargar lo que ya está registrado**.

## 6. Primer estado implementado

El primer `ExperimentLog` ya contiene seis observaciones históricas de junio–agosto y nueve publicaciones de Facebook programadas para el 15–16 de agosto. El `Publication_Log` contiene las nueve órdenes de Facebook y la prueba de Instagram que fue eliminada manualmente. Las métricas 24/72 horas de las nueve publicaciones quedan pendientes hasta que exista una ventana temporal válida.

El lote 1 de normalización cubrió inicialmente 28 filas y, tras resolver las excepciones, `Content_Inventory.csv` contiene 30 registros. Se preservaron todas las columnas originales y se añadieron campos normalizados para estado operativo, estado de canon, asset confirmado, asset candidato, relaciones y trazabilidad de reconciliación.

`CNT-002 → 260509` quedó resuelto como `Resolved_Production_Set`: Meta identificó el post `1036844829507460_122143141185072582`, publicado el 30 de julio a las 14:16:47 UTC, con permalink `https://www.facebook.com/reel/911880681976378/`. El reel dura 17.39 segundos y su secuencia coincide con los tres videos de producción de Wilfred/caja/peluche localizados en Drive. El archivo 260509 de Drive corresponde a Universe existencial y se mantiene rechazado. No existe un render final `260####` confirmado, así que no se inventa uno.

`CNT-023` quedó resuelto como `Resolved_Asset_Set`: el episodio 2 de “¿Qué me llegó?” se relaciona con la carpeta de Drive `Elara - Lampara de luna`, que contiene 7 assets verificados: cuatro piezas de video/imagen de entrega y apertura de paquete, más tres renders de secuencia. El registro conserva los siete nombres en `asset_set`, no se fuerza a un único `260####` y se enlaza con `CNT-002`, el episodio 1. La publicación de Facebook quedó confirmada con Page Post ID `1036844829507460_122147352825072582`, Reel ID `1067337609170026`, permalink `https://www.facebook.com/reel/1067337609170026/` y fecha local 2026-08-08 19:19:54.

`CNT-029` y `CNT-030` fueron incorporados desde sus documentos reales de producción. CNT-029 es el reel “Pausa para ver qué piensa de ti”, con banco de 9 cuadros y estado Draft; CNT-030 es su especificación dependiente de audio y montaje, no una publicación independiente. Ambos quedan enlazados entre sí y no reciben referencias 260 inventadas.

El preview actualizado está en `Operations/Research/2026-08-15_Reconciliacion_Lote_01_Preview.md` y el CSV detallado en `Operations/Research/2026-08-15_Reconciliacion_Lote_01_Preview.csv`. CNT-023 conserva además el `drive_reference_id` de la carpeta de producción, el listado exacto de sus siete assets y la publicación confirmada en `Publication_Log.csv`. La normalización es reversible porque `estado` y `bloqueado_canon` originales permanecen intactos. CNT-002 ya no tiene una excepción abierta a nivel de publicación ni de conjunto de producción. Solo queda registrada la ausencia del nombre del render final como archivo `260####`, lo cual no bloquea la integridad de los 30 registros.

## 7. Reglas de gobernanza

`Content_Inventory.csv` es la fuente de identidad de las piezas. `Publication_Log.csv` es el historial de hechos y no debe sobrescribirse para “limpiar” errores; se corrigen mediante una columna de nota o una nueva entrada de corrección. `ExperimentLog.csv` es el registro de aprendizaje y no debe llenarse con hipótesis inventadas ni con métricas estimadas.

Los estados de canon y aprobación no se cambian automáticamente. Fernando o Claude conservan la autoridad sobre canon y aprobación final. Manus puede validar, agregar datos, preparar vistas y documentar resultados, pero no convertir una propuesta en canon ni marcar una pieza bloqueada como aprobada.

## Referencias

[1]: `01_00_Arquitectura_Calendario_Escalable.md` — Arquitectura de metadatos, estados y calendario como vista.
[2]: `13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md` — Formato de exportación y publicación mediante Meta Graph API.
[3]: `Integracion_Growth_OS.md` — HypothesisBank, ExperimentLog y puente con canon.
[4]: `Content_Inventory.csv` — Inventario actual de 28 piezas y sus estados históricos.
[5]: `../Operations/Research/2026-08-15_Publication_Log.csv` — Primer ledger de publicaciones implementado.
[6]: `../Operations/Research/2026-08-15_ExperimentLog.csv` — Primer ledger experimental implementado.
