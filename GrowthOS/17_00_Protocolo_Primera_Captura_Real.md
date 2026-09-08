# Protocolo de primera captura real de métricas

**Propósito:** Validar una captura real, manual y de solo lectura en Codex sin publicar, programar ni activar automatizaciones.

**Estado:** Draft  
**Fecha de creación:** 2026-09-08  
**Última actualización:** 2026-09-08  
**Versión:** 1.0  
**Autor:** Manus AI (CGO)  
**Documentos relacionados:** [Contrato Codex–Growth OS](16_00_Contrato_Codex_Metricas.md), [Estado histórico de Universe 2026](15_00_Estado_Historico_Universe_2026.md), [Fuente maestra y ledgers](14_00_Fuente_Maestra_y_Ledgers.md), [Studio Governance](../Studio_Governance.md)  
**Organización:** `GrowthOS/`

## 1. Alcance cerrado

La primera captura utilizará **una sola publicación ya existente**, una sola plataforma y una sola cuenta. Será una lectura puntual de métricas actuales (`window_type=lifetime`). No se publicará contenido, no se modificará la publicación, no se consultarán otras publicaciones y no se crearán recomendaciones.

| Elemento | Límite |
|---|---|
| Publicaciones | 1 |
| Plataforma | 1 |
| Cuenta | 1 |
| Capturas | 1 snapshot `lifetime` |
| Operaciones externas | Lectura única |
| Resultado | Un registro validado en Codex |
| Datos | Solo métricas agregadas del post; sin comentarios, DMs, nombres ni datos personales |

## 2. Selección del post

El post debe cumplir todos estos requisitos: tener `meta_post_id` explícito; estar publicado y no eliminado; pertenecer a la cuenta USM autorizada; tener `publication_id`, `asset_ref`, `experiment_id` e `hypothesis_id` cuando existan; y no requerir login manual compartido durante la ejecución. Si falta cualquier identificador esencial, la captura se detiene.

Para esta primera prueba no se debe elegir un post financiero, promocional, sensible o con información personal. Preferir un post orgánico ya publicado y de bajo riesgo operativo.

## 3. Datos permitidos

Codex debe registrar únicamente: identificadores del post, timestamps UTC, plataforma, formato, personaje y círculo si ya están documentados, más `impressions`, `reach`, `views`, `interactions`, `reactions`, `comments`, `shares`, `saves` y `clicks` cuando la fuente los entregue. Los valores no entregados deben ser `null` y marcarse con `quality_status=missing`; no deben convertirse en cero.

No se almacenarán tokens, respuestas completas con datos personales, comentarios, DMs, nombres de usuarios ni contenido no necesario para validar el contrato.

## 4. Secuencia operativa

Primero, Fernando aprueba por mensaje el `platform`, `account_id`, `meta_post_id` y la ventana de ejecución. Después, Codex valida que la publicación local exista y que el `meta_post_id` coincida. Luego se realiza una sola lectura. El payload se normaliza al esquema `metric_snapshot`, se asigna `snapshot_id`, se valida como `lifetime`, se exporta a JSON/CSV y se registra el resultado agregado.

Si la fuente no devuelve una métrica, el proceso continúa con `null` y `missing`. Si falla la autenticación, el ID, la respuesta o la validación, el proceso se detiene sin reintentos automáticos.

## 5. Criterios de éxito

La captura es exitosa si existe exactamente un snapshot válido, el `publication_id` coincide, el `meta_post_id` coincide, el timestamp es posterior a la publicación, `window_type=lifetime`, los faltantes están representados correctamente, no hay secretos en los outputs y los archivos son reproducibles.

La captura **no** demuestra qué personaje, formato o horario funciona mejor. Solo demuestra que Codex puede recibir, normalizar, validar y exportar una observación real.

## 6. Criterios de detención

Detener inmediatamente si se solicita publicar o modificar contenido, si aparecen datos personales, si la cuenta no coincide, si el post no tiene ID verificable, si la respuesta contiene campos inesperados sensibles, si se requieren más de una lectura o si Codex no puede validar el snapshot. No se reintenta sin aprobación nueva.

## 7. Después de la captura

Se revisa el JSON/CSV y el log de ejecución. Si todo pasa, el CGO cambia este documento a `Active` y autoriza diseñar la siguiente captura: un post nuevo con E0, seguido posteriormente por E24 y E72. Esa segunda fase requiere una aprobación separada y no debe mezclarse con esta prueba.

**Estado actual:** Diseñada, no autorizada para ejecución.

[Contrato Codex–Growth OS]: 16_00_Contrato_Codex_Metricas.md
[Estado histórico de Universe 2026]: 15_00_Estado_Historico_Universe_2026.md
[Fuente maestra y ledgers]: 14_00_Fuente_Maestra_y_Ledgers.md
[Studio Governance]: ../Studio_Governance.md
