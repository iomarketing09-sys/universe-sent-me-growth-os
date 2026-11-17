# Shadow test — reglas de comentarios Universe Sent Me

**Fecha de reevaluación:** 17 de noviembre de 2026 (UTC).
**Modo:** local, solo lectura de la muestra previamente capturada. No se consultó Meta, no se llamó a modelos generativos, no se modificaron colas/aprobaciones/logs operativos y no se publicó contenido.

## Muestra
- Comentarios únicos evaluados: 32 (misma muestra del shadow test anterior).
- Se conservó el contexto editorial exacto que ya estaba vinculado por ID de publicación.
- Esta reevaluación aísla el efecto de las correcciones de detección; no incorpora comentarios nuevos.

## Resultado con las reglas corregidas
- `skip_already_replied`: 11.
- `discard_low_signal`: 6.
- `record_brand_signal`: 5.
- `ignore_user_tag`: 4.
- `hold_risky_brand_mention`: 1.
- `hold_for_missing_context`: 5.
- `retain_human_approval`: 0.

## Señales detectadas
- `brand_mention`: 6.
- `low_signal`: 6.
- `meaningful_text`: 14.
- `risky_brand_mention`: 2.
- `tagged_mention`: 4.

## Verificación de los falsos positivos anteriores
- **«Que Diablos haha»**: ahora queda sin señal de pregunta. Al no tener contexto editorial exacto, permanece en `hold_for_missing_context`; no se descarta ni se responde automáticamente.
- **Mención sexualizada con «Universe Sent Me»**: ahora se clasifica como `risky_brand_mention` y pasa a `hold_for_risky_brand_mention`; deja de incrementar la métrica de señales limpias de marca.
- Las menciones limpias de la página siguen en `record_brand_signal`; las etiquetas de usuarios siguen en `ignore_user_tag`.

## Interpretación y límites
- Los comentarios ya respondidos se excluyen del reprocesamiento.
- El contenido riesgoso que contiene el nombre de la página queda para revisión humana, no genera respuesta y no cuenta como señal positiva de marca.
- Las afirmaciones y preguntas sin contexto exacto siguen retenidas; no se generan borradores sin contexto editorial.
- Los comentarios con contexto exacto pueden llegar a `retain_human_approval`, nunca a publicación automática.
- Esta prueba valida reglas deterministas sobre una muestra histórica; no mide la calidad de respuestas generadas ni sustituye revisión humana.

**Archivo de detalle:** `comments_policy_shadow_2026-11-17.csv`.
