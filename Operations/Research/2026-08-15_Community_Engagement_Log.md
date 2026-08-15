---
title: "Community Engagement Log — Universe Sent Me"
purpose: "Registrar de forma ligera, append-only y anonimizada las señales cualitativas de comentarios, las respuestas humanas y los aprendizajes editoriales de la comunidad."
status: Active
created: 2026-08-15
updated: 2026-08-15
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md"
  - "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
  - "GrowthOS/12_00_Sistema_Dos_Capas_Contenido_Canon.md"
organization: "Operations/Research"
---

# Community Engagement Log — Universe Sent Me

## 1. Propósito y límites

Este documento define el uso del ledger `2026-08-15_Community_Engagement_Log.csv`. El registro convierte los comentarios en señales de aprendizaje sin transformarlos en un sistema de vigilancia ni en un bot de respuestas. La unidad de registro es un comentario real recuperado desde una publicación propia; cada comentario se identifica por su `Comentario_ID` y solo puede aparecer una vez.

El ledger se creó vacío de forma intencional. Después de una nueva extracción verificable, ya contiene el primer lote de nueve comentarios de la publicación `1036844829507460_122148874371072582`; la auditoría histórica de 67 comentarios de las 20 publicaciones recientes permanece como evidencia agregada y no se reconstruyen sus filas individuales. No se inventan nombres, perfiles, IDs personales, intenciones ni respuestas históricas.

## 2. Fuente y privacidad

La fuente primaria es Meta Graph API para publicaciones propias de Universe Sent Me. La fila debe conservar `Post_ID`, `CNT_ID` cuando exista y `Comentario_ID`, pero no debe guardar nombres, PSID, enlaces de perfil, fotografías, ubicación, edad u otros datos personales. `Insight_Anonimo` debe describir un patrón colectivo, por ejemplo “varias personas describen cansancio laboral”, nunca “la usuaria X dijo…”.

El campo `Privacidad` utiliza inicialmente `Anonimizado`. Si un comentario requiere una revisión excepcional por moderación, la información adicional debe permanecer fuera de este ledger y tratarse con aprobación humana.

## 3. Taxonomía controlada

| Campo | Valores permitidos | Uso |
|---|---|---|
| `Tipo` | `Distribucion_Automatica`, `Vacio`, `Etiqueta_Social`, `Aprobacion_Breve`, `Reaccion_Emoji`, `Contextual_Sustantivo`, `Historia_Personal`, `Pregunta`, `Critica`, `Riesgo_Moderacion`, `Spam` | Clasificar la función observable del comentario sin diagnosticar al autor. |
| `Respuesta_Estado` | `Sin_Revisar`, `No_Requiere_Respuesta`, `Pendiente_Respuesta`, `Respondido`, `Escalado`, `Archivado` | Registrar el estado de atención humana. |
| `Respuesta_Sugerida` | Texto breve o instrucción de no respuesta | Preparar una opción humana sin publicarla. |
| `Aprobacion_Estado` | `No_Aplica`, `Pendiente_Fernando`, `Aprobada`, `Rechazada` | Impedir que una propuesta se interprete como publicación ejecutada. |
| `Moderacion_Estado` | `No_Accion`, `Revisar`, `Ocultar`, `Eliminar`, `Bloquear`, `Escalar` | Registrar una decisión de moderación sin ejecutarla automáticamente. |
| `Prioridad` | `Alta`, `Media`, `Baja` | Priorizar preguntas, historias, críticas útiles y riesgos por encima de emojis o etiquetas automáticas. |
| `Accion_Calendario` | `Ninguna`, `Repetir_Hook`, `Probar_CTA`, `Probar_Personaje`, `Crear_Asset_Respuesta`, `Actualizar_Copy`, `Revisar_Canon` | Devolver la señal al calendario o a la producción. |
| `Privacidad` | `Anonimizado` | Confirmar que no se guardaron datos personales innecesarios. |

## 4. Flujo de revisión

La primera fase mantiene las respuestas públicas bajo aprobación humana. La revisión comunitaria se ejecuta en dos ventanas: una durante el mismo día de publicación y otra entre 24 y 48 horas después. No se consulta cada cinco minutos ni se crea un scheduler adicional para este ledger.

En la primera ventana se priorizan preguntas, historias personales, comentarios contextuales y publicaciones con cinco o más comentarios. En la segunda se recuperan señales tardías, se confirma si una respuesta quedó pendiente y se registra cualquier insight que pueda regresar al calendario. Los comentarios de distribución automática, vacíos, emojis y etiquetas se conservan solo cuando sean necesarios para medir cobertura; no se deben presentar como conversación cualitativa.

Una respuesta humana debe ser breve, cálida y coherente con Universe Sent Me. No debe diagnosticar, prometer ayuda profesional, discutir de forma extensa ni convertir una historia personal en contenido sin consentimiento. Los comentarios sexualizados, críticos, agresivos o ambiguos se revisan individualmente; un comentario aislado no activa automáticamente una sanción.

## 5. Reglas de integridad

El ledger es append-only. Una corrección debe registrarse como nueva observación o mediante una nota de auditoría, no sobrescribiendo silenciosamente una respuesta o clasificación anterior. `Comentario_ID` es la clave de idempotencia y `Ultima_Sincronizacion` debe indicar cuándo se recuperó o revisó la fila.

No se publican respuestas, se ocultan comentarios, se eliminan comentarios ni se bloquean personas desde este documento. `Respuesta_Sugerida` es una bandeja de aprobación, no un hecho de publicación. Cualquier escritura requiere una solicitud explícita y confirmación de Fernando, además de una revisión del texto o acción concreta.

## 6. Métricas derivadas

A partir de este ledger se podrán calcular comentarios cualitativos por publicación, cobertura de respuesta, tiempo aproximado de respuesta, proporción de comentarios con señal editorial y cantidad de comentarios escalados. Estas métricas deben mantenerse separadas de las reacciones, shares y etiquetas automáticas de Meta.

Durante la prueba Aug 17–30, la unidad de análisis será la publicación. Los resultados comunitarios se compararán por personaje, formato, reuse/nuevo, horario y variante de CTA, sin atribuir causalidad a una sola publicación viral.

## 7. Relación con otros documentos

`Auditoria_Comentarios_Facebook.md` contiene el diagnóstico técnico y la taxonomía inicial. Este documento contiene la operación permanente del ledger. `Content_Inventory.csv`, `Publication_Log.csv` y `ExperimentLog.csv` siguen siendo las fuentes para identidad, hechos de publicación y aprendizaje cuantitativo; el Community Engagement Log es una capa cualitativa complementaria y no sustituye ninguno de ellos.

## 7. Primer lote real — publicación `1036844829507460_122148874371072582`

El 15 de agosto se recuperaron nueve comentarios de la publicación de Silvio con solo lectura mediante Meta Graph API v26. Se registraron todos porque el objetivo del primer lote es probar la taxonomía completa, no responder indiscriminadamente.

| Resultado | Casos | Tratamiento |
|---|---:|---|
| Distribución automática o comentario vacío | 3 | Registrar para cobertura, sin respuesta. |
| Aprobación breve | 1 | No requiere respuesta individual. |
| Desinterés explícito | 1 | No responder; no presenta riesgo de moderación por sí solo. |
| Conversación humorística/contextual | 3 | Preparar respuesta juguetona, pendiente de aprobación humana. |
| Comentario con generalización hostil | 1 | Escalar para revisión; no responder ni moderar automáticamente. |

El lote se conserva sin nombres ni perfiles. La publicación no está vinculada automáticamente a un `CNT-####` porque la consulta proporcionó un Meta Post ID, no una identidad de pieza reconciliada. Las tres respuestas sugeridas del ledger son propuestas editoriales y permanecen en `Pendiente_Fernando`; ninguna se ha publicado.

## Referencias

[1]: https://developers.facebook.com/documentation/pages-api/comments-mentions "Meta for Developers — Comments and @mentions"
[2]: https://developers.facebook.com/docs/graph-api/reference/comment/ "Meta for Developers — Graph API Comment reference"
