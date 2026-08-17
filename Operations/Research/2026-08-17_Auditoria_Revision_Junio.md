---
title: "Auditoría de revisión histórica de junio"
purpose: "Comparar los top posts de junio ya documentados en el Growth OS con la revisión manual mencionada por Fernando y definir el siguiente lote sin duplicar evidencia."
status: "Review"
created: 2026-08-17
updated: 2026-08-17
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-08_Reporte_Mensual_Junio_Julio_2026.md"
  - "Operations/Research/2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv"
  - "Operations/Research/Historical_Performance_Individuals.csv"
  - "GrowthOS/08_00_Metricas_Baseline_Plataformas.md"
  - "GrowthOS/Content_Inventory.csv"
organization: "Operations/Research"
---

# Auditoría de revisión histórica de junio

## Dictamen inicial

Junio es el siguiente periodo correcto para trabajar. Mayo ya tiene suficiente cobertura estructurada y el repositorio ya contiene una primera selección de **cinco top posts individuales de junio**. Estos cinco registros coinciden con la sección “Posts destacados de junio” del reporte mensual elaborado con Windsor.ai; no es necesario volver a integrarlos ni crearles CNT automáticamente.

Las capturas que Fernando compartió con Claude pertenecen a la biblia y no deben tratarse como fuente estadística. La fuente operativa de junio es la carpeta Drive `06 Junio` (`1Yihb7b3K3cRYOziDp_DbBJsNeyiB3S0y`), que contiene 197 elementos: 196 archivos de imagen y una subcarpeta `Top`. La carpeta organiza los assets por mes, pero no conserva por sí sola el día de publicación. Por tanto, el Growth OS puede confirmar lo que ya está versionado, pero debe reconstruir cualquier fecha individual cruzando cada asset con publicaciones Meta mediante filename/ref, caption, imagen o evidencia de calendario. No se debe asumir que los cinco top posts representan todo el mes.

## Top posts de junio ya integrados

| Fecha | Concepto | Meta ID | Interacciones | Estado |
|---|---|---|---:|---|
| 22 jun | `El gato: 😧` | `1036844829507460_122132599809072582` | 1,128 | Integrado como histórico individual; sin CNT |
| 22 jun | `a ver... a ver... 🤨` | `1036844829507460_122132690157072582` | 975 | Integrado como histórico individual; sin CNT |
| 9 jun | `yo Aura Fuerte 😏` | `1036844829507460_122128723341072582` | 1,127 | Integrado como histórico individual; sin CNT |
| 28 jun | `Me da miedo ser el malo de la historia...` | `1036844829507460_122134136793072582` | 1,308 | Integrado como histórico individual; sin CNT |
| 10 jun | `🤡` | `1036844829507460_122129013585072582` | 785 | Integrado como histórico individual; sin CNT |

La suma de estos cinco posts no debe confundirse con el agregado mensual de junio: el mes completo registra 18,451 interacciones, mientras estos son únicamente los destacados individuales seleccionados por el reporte.

## Qué confirma junio

El reporte mensual identifica una señal consistente: imagen estática y copy minimalista, especialmente uno o dos emojis o una frase muy corta, aparece entre los mejores posts del mes. El 22 de junio tuvo dos piezas fuertes consecutivas, lo que refuerza la hipótesis de que el formato y el copy pesan más que una distribución uniforme de captions largos.

Esta evidencia sirve para aprendizaje editorial y selección de futuros reuse, pero no basta por sí sola para crear CNT. Para enlazar los cinco top posts a inventario se necesita filename/asset de Drive o una relación editorial explícita; el Meta ID y el caption prueban la publicación, no necesariamente el archivo creativo de origen.

## Siguiente lote recomendado

El siguiente lote de junio debe comenzar con los posts individuales adicionales del dataset de 508 filas y los assets de la carpeta `06 Junio`. La reconstrucción debe priorizar los top posts y usar coincidencia visual o evidencia de Meta cuando el filename no sea suficiente. Las filas se clasificarán como `Fecha_y_asset_confirmados`, `Meta_confirmado_asset_pendiente` o `Asset_Drive_sin_post_confirmado`. Solo la primera categoría podrá enlazarse después a un CNT. Este proceso no requiere las capturas de la biblia ni debe mezclar su contenido con estadísticas de publicación.

No se modificaron `Content_Inventory.csv`, `Publication_Log.csv` ni `ExperimentLog.csv` durante esta auditoría.
