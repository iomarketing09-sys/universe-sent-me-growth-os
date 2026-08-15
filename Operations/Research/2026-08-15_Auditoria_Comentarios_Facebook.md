---
title: "Auditoría de comentarios de Facebook y propuesta de Community Growth"
purpose: "Verificar los permisos reales de Meta para comentarios de Facebook y definir un sistema de escucha, respuesta y aprendizaje para Universe Sent Me."
status: Active
created: 2026-08-15
updated: 2026-08-15
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
  - "GrowthOS/08_00_Metricas_Baseline_Plataformas.md"
  - "GrowthOS/12_00_Sistema_Dos_Capas_Contenido_Canon.md"
  - "GrowthOS/00_01_Changelog_GrowthOS.md"
organization: "Operations/Research"
---

# Auditoría de comentarios de Facebook y propuesta de Community Growth

## 1. Propósito y alcance

Este documento establece el estado técnico y estratégico del sistema de comentarios de la página de Facebook **Universe Sent Me**. La auditoría se realizó con llamadas de solo lectura a Meta Graph API el 15 de agosto de 2026. No se publicaron respuestas, no se eliminaron comentarios, no se ocultó contenido y no se modificó ninguna publicación.

La propuesta no trata los comentarios únicamente como una bandeja que debe limpiarse. Para Growth OS, cada comentario puede cumplir tres funciones simultáneas: señal de distribución, evidencia cualitativa de identificación emocional y oportunidad de construir relación con la comunidad. Por eso la prioridad es crear un ciclo de **escucha → respuesta prudente → aprendizaje → ajuste editorial**, antes de automatizar respuestas masivas.

## 2. Veredicto ejecutivo

> **La API de Meta sí tiene acceso operativo para leer los comentarios de Facebook de Universe Sent Me.** La lectura real respondió HTTP 200 en las pruebas y la página devolvió las tareas `MODERATE` y `CREATE_CONTENT`.

El token vigente mostró `pages_manage_engagement` y `pages_read_engagement`, además de `pages_read_user_content`; no mostró `pages_read_user_engagement`. La guía específica de Meta para comentarios enumera también `pages_read_user_engagement` como permiso requerido, pero la ausencia de ese permiso no bloqueó la lectura observada. Esta diferencia debe conservarse como una advertencia de compatibilidad, no como un bloqueo activo.

La oportunidad es suficientemente grande para justificar un sistema ligero: en una muestra de las 20 publicaciones más recientes se encontraron **67 comentarios**, con comentarios en **16 de 20 publicaciones (80%)**. La mediana fue de **2 comentarios por publicación**, el promedio de **3.35** y el máximo de **14**. Esto sugiere que la comunidad ya está conversando; todavía no sabemos cuánto valor se está perdiendo por falta de respuesta estructurada.

## 3. Estado técnico verificado

### 3.1 Identidades y tareas

| Elemento | Resultado verificado |
|---|---|
| Página | Universe Sent Me |
| Page ID | `1036844829507460` |
| Identidad del token de usuario | Fernando Gdlr, ID `2920605591459033` |
| `/me/permissions` | HTTP 200; sin permisos rechazados devueltos |
| Página en `/me/accounts` | HTTP 200; token de página derivable |
| Tareas de página | `MODERATE`, `CREATE_CONTENT`, `MANAGE`, `ANALYZE`, `MESSAGING`, entre otras |
| `/PAGE_ID/feed` | HTTP 200 |
| `/POST_ID/comments` | HTTP 200 en publicaciones propias recientes |
| `can_comment` | `true` en la muestra consultada |
| Escrituras de moderación | No probadas en esta auditoría; requieren confirmación explícita antes de ejecutarse |

### 3.2 Permisos efectivos del token

El token vigente devolvió los siguientes permisos concedidos: `pages_manage_engagement`, `pages_read_engagement`, `pages_read_user_content`, `pages_manage_posts`, `pages_show_list`, `business_management`, `public_profile`, `instagram_basic`, `instagram_content_publish`, `instagram_manage_comments` y `read_audience_network_insights`.

La documentación de Meta describe `pages_manage_engagement` como el permiso usado para moderar comentarios, `pages_read_engagement` para leer contenido publicado y `pages_read_user_content` para contenido generado por usuarios en la página [1]. La guía específica de comentarios y menciones enumera `pages_manage_engagement`, `pages_read_engagement` y `pages_read_user_engagement`, junto con las tareas `MODERATE` y `CREATE_CONTENT` [2].

La situación actual debe expresarse con precisión: **la lectura de comentarios está validada; la capacidad de responder o eliminar está respaldada por los permisos y tareas observados, pero todavía no se ha ejecutado una escritura controlada**. No debemos convertir una capacidad documentada en una acción automática sin probar primero el caso de uso y el tono de marca.

## 4. Evidencia de actividad reciente

El escaneo consultó las 20 publicaciones más recientes disponibles en el feed de la página y solicitó el resumen de comentarios de cada publicación.

| Métrica | Resultado |
|---|---:|
| Publicaciones revisadas | 20 |
| Comentarios acumulados | 67 |
| Publicaciones con al menos un comentario | 16 |
| Proporción con comentarios | 80% |
| Promedio por publicación | 3.35 |
| Mediana por publicación | 2 |
| Promedio cuando hubo comentarios | 4.19 |
| Máximo observado | 14 |

La distribución fue desigual: cuatro publicaciones no tuvieron comentarios, mientras que varias concentraron entre 8 y 14. Esto es importante para la operación: no conviene revisar todos los posts con la misma intensidad. El sistema debe priorizar las piezas que ya están recibiendo señales y aquellas que tienen potencial de conversación, no únicamente las que tienen más reacciones.

## 5. Propuesta CGO: sistema de comentarios en tres capas

### Capa 1 — Escucha y registro

La primera capa debe ser de solo lectura y baja frecuencia. Su función es recuperar comentarios nuevos de publicaciones propias, evitar duplicados mediante `Comentario_ID`, y crear una fila de aprendizaje por cada comentario que aporte señal. La revisión no debe ejecutarse cada cinco minutos: ese patrón es caro, innecesario y contradice la estrategia de simplificación aplicada al scheduler de Instagram.

Para empezar, recomiendo dos revisiones diarias en días de alta frecuencia y una revisión diaria en días de menor actividad. Como alternativa aún más ligera, se puede ejecutar un resumen al final del día y una revisión manual adicional solo cuando una publicación supere un umbral de comentarios. El sistema debe registrar únicamente lo necesario y evitar guardar nombres, PSID o datos personales salvo que exista una razón operativa clara.

### Capa 2 — Respuesta humana guiada

Durante la primera prueba, las respuestas deben ser humanas, pero apoyadas por un playbook. El objetivo no es responder todo con la misma frase, sino conservar la personalidad de Universe Sent Me: cálida, observadora, ligeramente cósmica y con humor cuando el contexto lo permita.

| Tipo de comentario | Acción recomendada | Automatización inicial |
|---|---|---|
| Identificación: “me pasa”, “soy yo” | Validar y devolver una pregunta breve o una complicidad | No automatizar |
| Historia personal | Agradecer, reconocer el patrón y evitar diagnosticar | No automatizar |
| Pregunta sobre personaje o contexto | Responder con información canónica o admitir que es un meme suelto | Plantilla revisada por humano |
| Etiqueta o mención de otra persona | Responder solo si la etiqueta es natural y no invasiva | No automatizar al inicio |
| Elogio o agradecimiento | Agradecer con voz de marca y, si procede, devolver una pregunta | Plantilla de bajo riesgo |
| Crítica razonable | Responder sin discutir; identificar si contiene una objeción útil | No automatizar |
| Spam, enlaces sospechosos o abuso | Ocultar/eliminar según política y registrar el motivo | Acción humana confirmada |
| Comentario sexualizado o de doble sentido | Distinguir contexto humorístico de acoso; no borrar solo por incomodidad | Acción humana confirmada |

La regla es **no premiar el conflicto con una discusión extensa**. Las respuestas deben abrir conversación o cerrar con elegancia. Para comentarios con historias personales, no se debe diagnosticar, prometer ayuda profesional ni convertir la respuesta en una intervención emocional impropia de la página.

### Capa 3 — Aprendizaje editorial

Cada revisión debe producir una señal que pueda regresar al calendario y al sistema de generación de memes. El registro no necesita ser pesado: basta con relacionar la publicación, el tipo de comentario y la decisión editorial.

Las columnas mínimas recomendadas son `Post_ID`, `Fecha`, `Archivo`, `Comentario_ID`, `Tipo`, `Señal`, `Respuesta_Estado`, `Insight`, `Accion_Calendario` y `Privacidad`. `Tipo` debe utilizar una taxonomía estable; `Insight` debe resumirse de forma anónima, por ejemplo: “varias personas describen el mismo cansancio laboral”, no “la usuaria X dijo…”.

## 6. Experimento recomendado para los próximos 14 días

No recomiendo llenar cada copy con “comenta”, porque eso puede producir comentarios de baja intención y dificultar la lectura del aprendizaje. Recomiendo distribuir cuatro variantes de CTA natural dentro del calendario experimental Aug 17–30:

| Variante | Uso | Hipótesis |
|---|---|---|
| Sin CTA | Línea base en memes de identificación inmediata | El contenido puede generar conversación sin pedirla |
| Pregunta contextual | “¿En qué momento te pasa esto?” | Las preguntas específicas producen historias más útiles |
| Elección de personaje | “¿Quién de USM diría esto?” | El elenco convierte la conversación en participación del universo |
| Etiqueta natural | Solo cuando el meme describe una situación compartible | Las etiquetas amplían distribución sin forzar interacción |

La prueba debe equilibrar las variantes entre horarios, personajes y reuse/nuevo. No se debe comparar una variante solo en domingos o solo con el personaje que históricamente rinde mejor. La unidad de análisis será la publicación individual, pero la decisión se tomará con medianas por variante para no dejar que un post viral domine la conclusión.

Los indicadores principales serán comentarios por publicación, proporción de publicaciones con comentarios, mediana de comentarios, cobertura de respuesta y número de comentarios cualitativos. Como el alcance no siempre está disponible de forma estable en Graph API, se puede usar temporalmente `comentarios/reacciones` como proxy interno, etiquetándolo como proxy y no como tasa oficial de conversación.

## 7. Qué automatizar y qué no automatizar todavía

### Automatizar primero

Debe automatizarse la recuperación de comentarios, la deduplicación por `Comentario_ID`, el resumen por publicación, la detección de nuevas publicaciones que cruzan un umbral y la preparación de una bandeja de revisión. Estas tareas son repetitivas y tienen bajo valor creativo.

### Mantener bajo aprobación humana

Las respuestas públicas, menciones, eliminación, ocultamiento y cualquier respuesta a una historia personal deben permanecer bajo aprobación humana durante la primera fase. También debe mantenerse bajo aprobación humana cualquier comentario que pueda interpretarse como crisis, acoso, discriminación o conflicto con las reglas de la página.

La recomendación técnica es **no crear todavía un bot de respuesta en tiempo real**. Primero validaremos la taxonomía y el tono con datos reales durante 14 días. Si el volumen aumenta y las respuestas repetitivas superan claramente el tiempo disponible, se puede separar después el colector determinista del agente que propone respuestas.

## 8. Próximo paso operativo

El siguiente paso recomendado es una prueba controlada de una sola respuesta a un comentario real, elegido por Fernando, con texto preparado y confirmación antes de publicar. Esa prueba validará el endpoint de escritura, el formato del Page Access Token y el comportamiento visible en Facebook sin abrir todavía la puerta a automatización masiva.

Después de esa prueba, el Growth OS debe incorporar un registro ligero de comentarios cualitativos y añadir una revisión de comunidad al cierre diario. La decisión de automatizar respuestas deberá basarse en tres evidencias: volumen sostenido, baja tasa de errores de clasificación y existencia de plantillas de respuesta aprobadas.

## 9. Documentos que requieren coherencia

La actualización de este documento requiere mantener sincronizados los siguientes archivos:

| Documento | Actualización necesaria |
|---|---|
| `GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md` | Actualizar permisos efectivos, estado real de comentarios y diferencia con `pages_read_user_engagement` |
| `GrowthOS/00_01_Changelog_GrowthOS.md` | Registrar la auditoría, el escaneo de 20 publicaciones y la propuesta de flujo |
| `GrowthOS/12_00_Sistema_Dos_Capas_Contenido_Canon.md` | En una futura revisión, enlazar el registro cualitativo real de comunidad con esta auditoría |
| `GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md` | Incorporar la señal de comentarios como variable de aprendizaje cuando termine la prueba de 14 días |

## Referencias

[1]: https://developers.facebook.com/documentation/pages-api "Meta for Developers — Facebook Pages API"
[2]: https://developers.facebook.com/documentation/pages-api/comments-mentions "Meta for Developers — Comments and @mentions"
[3]: https://developers.facebook.com/docs/graph-api/reference/comment/ "Meta for Developers — Graph API Comment reference"
