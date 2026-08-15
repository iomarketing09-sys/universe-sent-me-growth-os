---
title: "Reconciliación de publicaciones Facebook 15–16 de agosto con Content Inventory"
purpose: "Registrar la reconciliación verificable entre los nueve assets publicados en Facebook el 15–16 de agosto de 2026, sus identificadores CNT y los hechos de publicación en Meta, incluyendo el estado separado de Instagram 2608030."
status: Active
created: 2026-08-15
updated: 2026-08-15
version: "1.3"
author: "Manus AI (CGO)"
related_documents:
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
  - "GrowthOS/Content_Inventory.csv"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "Operations/Research/2026-08-15_ExperimentLog.csv"
  - "Operations/Research/2026-08-15_Calendario_15_16_Agosto.csv"
  - "Operations/Research/2026-08-15_Calendario_15_16_Agosto.md"
  - "Operations/Research/2026-08-15_Auditoria_General_Growth_OS.md"
organization: "Operations/Research"
---

# Reconciliación de publicaciones Facebook 15–16 de agosto con Content Inventory

## Propósito y decisión

Este documento cierra la reconciliación del lote publicado en Facebook el 15 y 16 de agosto de 2026. El calendario y el `Publication_Log` ya contenían los nueve Meta Post IDs reales, pero sus campos `ID_Pieza` estaban vacíos y los nueve assets todavía no existían como filas `CNT-####` en `Content_Inventory.csv`.

La decisión aplicada es crear los nueve registros de identidad `CNT-031` a `CNT-039` a partir de evidencia directa: nombre exacto del archivo en Drive, personajes y caption del calendario aprobado, Meta Post ID, permalink y respuesta de Graph API. No se reutilizó ningún CNT genérico por semejanza temática. Esto evita convertir una idea editorial amplia —por ejemplo, “contenido de Universe” o “contenido de Fantasma”— en una relación falsa con un asset concreto.

> Los códigos `260####` siguen siendo referencias de asset. La relación con `CNT-####` queda confirmada aquí porque el archivo exacto, el post real y la fila del calendario apuntan a la misma pieza.

## Resultado del lote

| Publicación | CNT | Asset exacto | Personajes | Meta Post ID | Publicación local | Reconciliación |
|---|---|---|---|---|---|---|
| PUB-FB-15_16-01 | CNT-031 | `2608030 - Universe - Que fibra tomas pa cagarla tanto.jpeg` | Universe | `1036844829507460_122150559441072582` | 2026-08-15 10:00:22 | High — asset exacto en Drive + caption + Meta |
| PUB-FB-15_16-02 | CNT-032 | `260583 - Universe.png` | Universe | `1036844829507460_122150559591072582` | 2026-08-15 11:00:05 | High — asset exacto en Drive + caption + Meta |
| PUB-FB-15_16-03 | CNT-033 | `2608033 - Fantasma - vendra primero mi boda o jesus.jpeg` | Fantasma | `1036844829507460_122150559693072582` | 2026-08-15 13:30:00 | High — asset exacto en Drive + caption + Meta |
| PUB-FB-15_16-04 | CNT-034 | `260539 - Evan+Kiri.png` | Evan + Kiri | `1036844829507460_122150559765072582` | 2026-08-15 19:00:00 | High — asset exacto en Drive + caption + Meta |
| PUB-FB-15_16-05 | CNT-035 | `2608037- Universe - soñe que era un litrro de agua.jpeg` | Universe | `1036844829507460_122150559873072582` | 2026-08-16 10:00:00 | High — asset exacto en Drive + caption + Meta |
| PUB-FB-15_16-06 | CNT-036 | `260673 - Universe.png` | Universe | `1036844829507460_122150559981072582` | 2026-08-16 13:30:00 | High — asset exacto en Drive + caption + Meta |
| PUB-FB-15_16-07 | CNT-037 | `2608036- Elara+Evan - Nadie nos soporta.jpeg` | Elara + Evan | `1036844829507460_122150560083072582` | 2026-08-16 16:00:00 | High — asset exacto en Drive + caption + Meta |
| PUB-FB-15_16-08 | CNT-038 | `2608060 - Kael+Maeve - gustos salvajones.jpeg` | Kael + Maeve | `1036844829507460_122150560215072582` | 2026-08-16 19:00:00 | High — asset exacto en Drive + caption + Meta |
| PUB-FB-15_16-09 | CNT-039 | `humor4.16.png` | Según asset | `1036844829507460_122150560383072582` | 2026-08-16 22:00:00 | High — asset exacto en Drive + caption + Meta |

Los nueve posts fueron confirmados como existentes mediante Meta Graph API v26. La respuesta de Meta devolvió la caption esperada, la fecha UTC correspondiente a la hora local del calendario y un permalink verificable para cada post [10] [11]. Los permalinks completos están en `Publication_Log.csv` y `meta_permalink` dentro del inventario, por lo que este informe no duplica todas las URLs largas.

## Instagram 2608030

`CNT-031` también queda enlazado a la publicación manual de Instagram registrada como `PUB-IG-15_16-01`. El media real es `18145111759484218`, con permalink `https://www.instagram.com/p/DcEX6BSE8ka/`, publicado el 15 de agosto a las 10:59:41 hora local después de aprobación explícita. El slot original de las 10:00 quedó perdido.

Esta publicación **no fue una programación futura nativa de Instagram ni una ejecución automática del scheduler**. El commit `1694b00` documenta la publicación manual. El archivo local de idempotencia del scheduler no estaba disponible en esta sesión; por esa razón no se usa como evidencia positiva ni se infiere una ejecución automática. La evidencia operativa disponible es el calendario versionado, el `IG_Media_ID`, el permalink y el commit manual. La prueba de `260583`, enlazada a `CNT-032` como `PUB-IG-TEST-02`, permanece en estado `Eliminada_Manualmente` y no debe republicarse. La documentación operativa mantiene el scheduler selectivo desactivado y la distribución de Instagram bajo aprobación manual.

## Reglas de canon y estado

Los nueve registros nuevos conservan los campos históricos requeridos y reciben `Estado_Canon=Revision`, `Estado_Produccion=Asset_Listo` y `Estado_Publicacion=Publicada` en la fuente maestra. `Revision` no significa aprobación de canon: Fernando o Claude deben decidir cualquier estado protegido. La reconciliación confirma identidad y publicación, no canon narrativo.

`260583` queda registrado porque el post de Facebook del 15 de agosto tiene un Meta Post ID real; la prohibición de republicación se aplica a la prueba de Instagram eliminada y queda reflejada en `CNT-032`, `PUB-IG-TEST-02`, el calendario y las notas del ledger. No se crea una nueva publicación ni se programa una republicación.

## Estado de métricas al corte

La fecha del entorno al comprobar el ledger fue `2026-08-15T13:22:11-05:00` en `America/Matamoros`. El primer post de Facebook tenía aproximadamente tres horas de antigüedad y los demás no habían alcanzado 24 horas; las publicaciones del 16 de agosto tampoco tenían una ventana válida. En consecuencia, no se consultaron ni se estimaron `Interacciones_24h` o `Interacciones_72h`. El `Publication_Log` y el `ExperimentLog` conservan esos campos vacíos con estado `Pendiente_24h`, que es el resultado correcto hasta que una ejecución posterior tenga una ventana temporal válida. La primera extracción agrupada se ejecutó a las `2026-08-15T21:59:37Z`: evaluó las nueve publicaciones del experimento, encontró `eligible_count=0`, escribió cero métricas y dejó evidencia en `2026-08-15_Metricas_24_72_Extraccion_01.json`.

## Impacto en documentos relacionados

La reconciliación actualiza `Content_Inventory.csv`, `Publication_Log.csv` y `ExperimentLog.csv`. También requiere que la arquitectura deje de describir el lote como “nueve órdenes pendientes de mapear”: ahora están enlazadas a `CNT-031`–`CNT-039`, aunque sus métricas de 24 y 72 horas siguen pendientes.

El siguiente trabajo es consultar únicamente los nueve Meta Post IDs nuevos cuando cada ventana temporal sea válida, completar `Interacciones_24h` y `Interacciones_72h` y cerrar el veredicto de `HB-003`, `HB-004` y `HB-005` sin tratar esta reconciliación de identidad como evidencia de rendimiento.

## Fuentes

[1]: `../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md` — arquitectura de identidad, publicación y aprendizaje.
[2]: `../../GrowthOS/Content_Inventory.csv` — registros `CNT-031`–`CNT-039` y campos canónicos.
[3]: `2026-08-15_Publication_Log.csv` — hechos de publicación, IDs, permalinks y estados.
[4]: `2026-08-15_ExperimentLog.csv` — observaciones del experimento y enlace con hipótesis.
[5]: `2026-08-15_Calendario_15_16_Agosto.csv` — calendario aprobado, captions, asset filenames y assignments de plataforma.
[6]: `https://graph.facebook.com` — Graph API utilizada para confirmar los nueve posts de Facebook.
[7]: `https://www.facebook.com/122146890051072582/posts/122150559441072582` — permalink de la primera publicación como ejemplo verificable.
[8]: `https://www.instagram.com/p/DcEX6BSE8ka/` — publicación manual real de Instagram para `CNT-031`.
[9]: `../../GrowthOS/00_01_Changelog_GrowthOS.md` — registro de cambios del Growth OS.

## Referencias externas

[10]: https://developers.facebook.com/docs/graph-api/ — documentación general de Meta Graph API.
[11]: https://developers.facebook.com/docs/pages-api/ — documentación de Pages API.
