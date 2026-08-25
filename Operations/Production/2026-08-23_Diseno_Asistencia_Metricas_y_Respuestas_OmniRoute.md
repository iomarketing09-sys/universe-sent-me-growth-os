---
title: "Diseño de asistencia de métricas y respuestas con OmniRoute"
purpose: "Definir cómo OmniRoute puede analizar resúmenes métricos ya normalizados y producir propuestas de respuesta comunitaria sin convertirse en fuente canónica, sistema de moderación automática ni publicador autónomo."
status: Review
created: 2026-08-23
updated: 2026-08-25
version: "1.6"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-19_Decision_Gateway_IA_OmniRoute.md"
  - "Operations/Production/2026-08-18_Piloto_Local_OmniRoute_Seguro.md"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
  - "GrowthOS/08_00_Metricas_Baseline_Plataformas.md"
  - "GrowthOS/todo.md"
  - "GrowthOS/Integracion_Growth_OS.md"
  - "Operations/Research/2026-08-15_Community_Engagement_Log.md"
  - "Operations/Automation/2026-08-23_Diseno_Captura_Baseline_E0_E24_E72.md"
organization: "Operations/Production"
---

# Diseño de asistencia de métricas y respuestas con OmniRoute

## 1. Decisión

OmniRoute puede apoyar dos carriles: **lectura cualitativa de cortes métricos ya normalizados** y **propuestas de respuestas comunitarias**. No sustituye la extracción de Meta/Windsor, la normalización, la deduplicación, los cálculos, la moderación, los ledgers ni el acto de publicar.

> Toda salida de OmniRoute es un `Draft`. Una salida generada no es una métrica, una conclusión aprobada, una autorización editorial ni una orden de publicación.

La configuración aprobada para el piloto permanece local y manual: Combo `usm-groq-gemini-priority`, con `groq/openai/gpt-oss-20b` como ruta preferida y `gemini/gemini-3.5-flash` como fallback. El fallback mejora disponibilidad, pero puede variar la redacción o la interpretación; cada resultado debe conservar el proveedor y modelo que realmente atendieron.

## 2. Fronteras de arquitectura

| Capa | Responsable | Puede hacer | No puede hacer |
| :--- | :--- | :--- | :--- |
| Fuente y cálculo | Meta Graph API, Windsor y scripts versionados | Recuperar, normalizar, deduplicar y calcular los valores reproducibles | Pedir interpretación creativa al modelo como sustituto de un cálculo |
| Fuente maestra | `Content_Inventory`, `Publication_Log`, `ExperimentLog` y `Community_Engagement_Log` | Conservar hechos, ventanas, IDs, decisiones y evidencia | Ser sobrescrita por una salida IA |
| Preparación mínima | Script o persona responsable | Reducir el corte a agregados, definiciones, fecha y limitaciones | Enviar secretos, datos crudos o PII al modelo |
| OmniRoute | Gateway local + provider aprobado | Generar una lectura exploratoria o un borrador de respuesta | Publicar, moderar, clasificar definitivamente o cambiar una fila canónica |
| Revisión humana | Fernando y responsables editoriales | Aprobar, rechazar o reescribir; decidir la acción de calendario | Delegar el criterio de seguridad, canon o causalidad al modelo |
| Escritura/publish | Scripts existentes y Meta Graph API, solo tras orden explícita | Publicar un lote aprobado y verificarlo | Tomar borradores sin aprobación como instrucciones de escritura |

No se permite una conexión `navegador → OmniRoute`, ni que OmniRoute reciba tokens de Meta, contraseñas, API keys, datos crudos de Windsor, comentarios íntegros o documentos privados. Para un uso compartido futuro, el único diseño admisible es `backend privado → payload mínimo validado → OmniRoute privado`; este documento no aprueba construirlo todavía.

## 3. Carril A — análisis asistido de métricas

### 3.1 Qué se prepara antes del modelo

El análisis humano o determinista conserva las fuentes, cálculos y artefactos oficiales. OmniRoute recibe únicamente un **brief agregado y pseudonimizado**. No recibe filas crudas, handles, IDs nativos, capturas, URLs privadas ni identificadores de personas.

| Campo del brief | Ejemplo de forma permitida | Regla |
| :--- | :--- | :--- |
| `corte_id` | `Corte_2026-08-23_2200` | Referencia interna del reporte, no ID Meta |
| `plataforma` y `ventana` | `Facebook`, `Corte_Observado` | No mezclar ventanas ni plataformas |
| `fuente` y `definición` | `Meta`, `reacciones + comentarios + shares` | Mantener la definición exacta |
| `n_elegible` y exclusiones | `12 piezas; 3 sin comparación por maduración` | Las ausencias se explicitan, no se rellenan |
| agregados comparables | mediana, rango, shares y comentarios por cohorte | Solo datos ya calculados y revisados |
| etiquetas creativas | personaje, formato, hook, tratamiento de caption | Sin nombres de cuentas ni URLs |
| límites de comparabilidad | `muestra pequeña`, `lifetime`, `outlier`, `sin E0` | Obligatorio en cada prompt |

La IA no calcula la fuente de verdad ni reconcilia diferencias entre plataformas. Si el modelo realiza una operación aritmética para explicarla, esa operación debe verificarse contra el reporte determinista antes de entrar a un documento o ledger.

### 3.2 Prompt base de métricas

```text
Actúa como analista exploratorio de Universe Sent Me.

Usa exclusivamente este corte agregado y ya normalizado:
[PEGAR BRIEF SIN IDs, PII, SECRETOS NI FILAS CRUDAS]

Reglas obligatorias:
- No inventes métricas, causas, muestras, publicaciones ni resultados.
- No declares causalidad; usa lenguaje como "señal", "observación" o "hipótesis".
- No combines ventanas, plataformas ni definiciones distintas.
- Repite las limitaciones de comparabilidad antes de sugerir una acción.
- No escribas en ningún ledger, no cambies hipótesis existentes y no publiques contenido.

Devuelve en este orden:
1. Draft — tres observaciones descriptivas respaldadas solo por el brief.
2. Draft — hasta dos hipótesis de trabajo, con el dato que faltaría para evaluarlas.
3. Draft — una prueba pequeña y codificable, sin cambiar el calendario.
4. Limitaciones y verificaciones humanas obligatorias.
```

### 3.3 Salida y validación humana

La salida puede generar una nota de revisión, nunca un veredicto automático. Para ser incorporada al `ExperimentLog`, una persona debe confirmar que: las cifras citadas existen en el corte; la ventana y fuente permanecen visibles; las hipótesis no son presentadas como hechos; y la acción propuesta conserva una celda comparable, una `Hypothesis_ID` existente o el estado `Sin_hipotesis_asignada`.

## 4. Carril B — propuestas de respuestas comunitarias

### 4.1 Flujo obligatorio

```text
Meta Graph API de solo lectura
→ filtro determinista por cursor + Comentario_ID
→ deduplicación y taxonomía inicial
→ clasificación de riesgo
→ contexto mínimo anonimizado
→ OmniRoute: hasta tres propuestas Draft
→ revisión de Fernando y texto exacto aprobado
→ lote explícitamente autorizado
→ preflight anti-duplicado + publicación por script existente
→ verificación de autoría, parent, texto e is_hidden
→ append-only en Community Engagement Log y evidencia
```

El `Comentario_ID` se usa localmente para idempotencia y verificación; **no se envía a OmniRoute**. El modelo recibe una síntesis de intención y el contexto creativo estrictamente necesario, no el nombre, perfil, enlace, foto, ID ni historia completa de la persona.

| Riesgo | Casos orientativos | Tratamiento de OmniRoute | Publicación |
| :--- | :--- | :--- | :--- |
| Verde | elogio simple, reacción de emoji clara, acuerdo contextual no sensible | Puede proponer hasta tres respuestas breves | Solo tras aprobación humana del texto exacto |
| Ámbar | crítica, pregunta ambigua, historia personal, recomendación musical, enlace o hilo anidado | Puede ayudar a redactar, pero debe incluir riesgos y una opción `No responder` | Revisión individual obligatoria |
| Rojo | salud, duelo, crisis, autolesión, menores, acoso, discurso de odio, amenaza, sexualización, tema legal, datos personales o moderación | No se envía al modelo; se etiqueta para revisión humana | Nunca automática |
| Gris | intención insuficiente, solo nombre, etiqueta, texto vacío o conversación entre terceros | No requiere propuesta | No responder salvo decisión humana posterior |

### 4.2 Prompt base para propuesta comunitaria

```text
Actúa como asistente de community management de Universe Sent Me.

Contexto público y anonimizado:
- Tipo de señal: [ELOGIO / PREGUNTA / MÚSICA / CRÍTICA NO SENSIBLE].
- Resumen fiel: [RESUMEN SIN NOMBRE, ID, ENLACE, PERFIL NI DETALLES PERSONALES].
- Contexto del post: [TEMA GENERAL DEL POST].
- Voz: humor cálido, específico y breve; Universe se ríe con la audiencia, no de ella.

Reglas:
- Esto es solo un Draft. No afirmes que se publicó ni recomiendes publicación automática.
- No inventes que escuchaste, viste, hiciste o compartiste algo que no esté en el contexto.
- No diagnostiques, no des consejo profesional, no discutas, no pidas datos personales y no amplifiques contenido sexual o sensible.
- Si falta contexto o hay riesgo, responde "REVISIÓN HUMANA" y explica por qué.

Entrega: hasta tres variantes de máximo 180 caracteres, una razón editorial breve y una opción "No responder" cuando aplique.
```

### 4.3 Criterio de aprobación y verificación

Ningún resultado pasa directamente de `Draft` a `Respondido`. Antes de publicar, Fernando revisa el comentario en su contexto real, elige o reescribe una variante y aprueba un lote delimitado. El publicador existente conserva su preflight anti-duplicado y, después del POST, comprueba autoría de la Página, relación padre-hijo adecuada, texto exacto e `is_hidden`. Ante cualquier fallo, se detiene el lote y se registra la evidencia parcial; no se reintenta a ciegas.

## 5. Niveles de automatización

| Nivel | Qué se automatiza | Riesgo | Estado recomendado |
| :--- | :--- | :--- | :--- |
| 0 — Manual asistido | Fernando ejecuta un prompt local y revisa el resultado | Bajo; no hay acceso a datos reales | Disponible ahora |
| 1 — Preparación de borradores | Un proceso local prepara briefs agregados de métricas o propuestas anonimizada; no escribe ni publica | Bajo–medio; requiere sanitización y logs mínimos | Piloto siguiente recomendado |
| 2 — Lectura programada | Un job de solo lectura recupera el delta, deduplica y deja una cola `Pendiente_Fernando` con análisis/propuestas Draft | Medio; requiere secreto de servidor, idempotencia y control de errores | Diseño posterior, no activado |
| 3 — Publicación por lote aprobado | Un script publica exclusivamente IDs y textos incluidos en un artefacto aprobado; verifica cada resultado | Medio; ya existe como carril controlado | Solo por solicitud y aprobación explícitas |
| 4 — Bot autónomo | El sistema interpreta y publica por sí mismo | Alto: tono, seguridad, duplicados y responsabilidad | Prohibido |

La siguiente mejora debe ser Nivel 1: generar un paquete de revisión que contenga un resumen de métricas anonimizado y, por separado, una lista de propuestas comunitarias `Pendiente_Fernando`. La automatización útil es reducir la preparación repetitiva; el criterio editorial y la publicación permanecen humanos.

## 6. Trazabilidad, retención y errores

Cada ejecución debe registrar, fuera de los ledgers canónicos, `fecha_utc`, `carril`, `corte_o_lote`, `clase_de_datos`, `provider_real`, `modelo_real`, `combo_solicitado`, `versión_omniroute`, `latencia_ms`, `estado`, `decisión_humana` y enlaces a los artefactos aprobados. Para el carril comunitario, el mapeo entre el resumen enviado y el `Comentario_ID` queda solo en el artefacto local/privado de revisión; no se replica dentro del prompt.

Los prompts y respuestas no aprobados se tratan como temporales: no se guardan en el repositorio si contienen texto de comentarios reales. Solo se conserva un resumen anonimizado, la decisión humana y el texto exacto finalmente publicado cuando corresponda. Si se detecta un secreto, PII o un dato no permitido en un prompt, se aborta la ejecución, se elimina el temporal, se revisan los logs del gateway y se rota cualquier secreto que haya sido expuesto.

Un error de proveedor, una salida truncada, JSON inválido, una discrepancia de modelo o un fallback inesperado equivale a **sin borrador**. No se inventa una salida, no se rellena una métrica y no se publica. El modelo atendido se registra tal como lo devuelva OmniRoute; las diferencias entre `usage` y headers de Gemini se preservan como observaciones separadas.

## 7. Criterio para avanzar

Para pasar del Nivel 0 al Nivel 1 se requiere un piloto de cinco briefs métricos sintéticos o agregados y cinco casos comunitarios verdes ya anonimizados. La validación debe confirmar que no se envió PII, secreto, comentario crudo ni ID; que las propuestas se etiquetaron `Draft`; que ninguna métrica se alteró; y que Fernando pudo aprobar, reescribir o rechazar cada salida. El piloto no incluye consulta programada ni publicación.

Antes de considerar el Nivel 2 se necesita aprobación separada del diseño técnico, una ubicación segura para secretos, pruebas de idempotencia, límites de tasa, auditoría de logs, un mecanismo de pausa y una definición de frecuencia. No se usa un scheduler de alta frecuencia para comentarios; se respeta el ritmo operativo vigente de cortes y deltas.

## 8. Extensión propuesta: loop multicanal de Growth para Universe Sent Me

### 8.1 Alcance confirmado

La propuesta cubre exclusivamente las cuentas y piezas de **Universe Sent Me** en Instagram, Facebook, TikTok y YouTube. Contempla un corte diario, un cierre semanal, una hoja de consulta derivada y reportes revisables dentro de Manus. No comparte infraestructura, credenciales, datos, proveedores ni presupuesto con Firma Bordados.

El propósito no es producir un resumen automático de vanidad. El loop debe convertir cada publicación identificable en una oportunidad de aprendizaje: conservar el hecho y la métrica en los ledgers, separar lo comparable de lo inmaduro y generar hipótesis de bajo riesgo para el siguiente ciclo. OmniRoute participa únicamente después de esta preparación y nunca reemplaza una fuente, fórmula, veredicto ni decisión editorial.

### 8.2 Arquitectura objetivo y fronteras

```text
Fuentes aprobadas de cada plataforma
→ validación, deduplicación y normalización determinista
→ GitHub: fuente canónica y ledgers append-only
→ hoja derivada de consulta / dashboard
→ brief agregado, sin IDs ni PII
→ OmniRoute local: análisis Draft
→ revisión humana
→ hipótesis o experimento aprobado, si corresponde
```

| Capa | Función | Regla obligatoria |
| :--- | :--- | :--- |
| Recolección | Recuperar exclusivamente métricas nativas y metadatos operativos mínimos de las cuatro plataformas. | Conservar `source`, `retrieved_at`, `window_type`, definición de cada métrica y estado de disponibilidad. |
| Normalización | Resolver duplicados, separar snapshots de actividad diaria y relacionar cada fila con `Concept_ID`/`Platform_Content_ID` cuando exista evidencia. | No sumar Reach, views o engagement entre plataformas, ni convertir ausencia en cero. |
| Ledgers canónicos | Registrar hechos de publicación, snapshots y aprendizaje en el repositorio. | GitHub sigue siendo la única fuente de verdad; la hoja no modifica ni corrige ledgers. |
| Hoja derivada | Facilitar filtros por período, plataforma, formato, personaje, hook, hipótesis y estado de madurez. | Se regenera desde artefactos canónicos; no se vuelve una segunda base de datos. |
| OmniRoute local | Leer solamente un brief agregado por plataforma o cohorte y proponer observaciones e hipótesis. | Salida `Draft`; sin secretos, identificadores nativos, filas crudas, comentarios íntegros ni escritura automática. |
| Revisión humana | Validar cifras, limitaciones, interpretación y posible experimento. | Ningún draft actualiza un ledger, altera el calendario o publica contenido. |

Instagram Insights permite consultas de métricas de cuenta y de media para cuentas profesionales, mientras YouTube distingue reportes masivos de consultas específicas y TikTok expone campos de rendimiento por video para una cuenta autorizada. Estas capacidades deben comprobarse con la cuenta y permisos concretos antes de activar cualquier lectura automática. [1] [2] [3]

### 8.3 Qué debe medir el loop actual

El corte diario debe responder “qué cambió y qué requiere atención”, sin convertir acumulados lifetime en resultados de 24/72 horas. El cierre semanal debe responder “qué probar o ajustar en la siguiente cohorte”, manteniendo cada plataforma y ventana separadas.

| Corte | Datos deterministas mínimos | Salida de OmniRoute permitida | Decisión humana posterior |
| :--- | :--- | :--- | :--- |
| Diario, idealmente cerca de 22:00 `America/Matamoros` | Piezas nuevas o modificadas; plataforma; formato; estado de madurez; views o Reach cuando exista; acciones nativas; retención disponible; crecimiento; fuente y hora de lectura. | Hasta tres observaciones descriptivas, alertas de calidad de datos y una pregunta de aprendizaje. | Confirmar que la lectura no mezcla ventanas ni confunde una pieza inmadura con un resultado. |
| Semanal, al cierre del sábado después del último slot | Cohortes maduras; mediana por pieza; distribución; shares, guardados/favoritos, comentarios y retención según plataforma; cobertura de cascada; mezcla nuevo/reuse y evidencia de hipótesis. | Hipótesis de trabajo, máximo dos experimentos codificables y limitaciones explícitas. | Aprobar, reescribir o rechazar la hipótesis; decidir si entra a un siguiente calendario. |

Para el Growth actual, el análisis debe priorizar cinco preguntas: qué formato y plataforma aportan señal real por pieza; si los hooks `action-first` y las situaciones reconocibles sostienen retención; qué personaje, estructura narrativa y tratamiento de caption merecen más casos comparables; si la cascada Instagram–TikTok–YouTube se completó y cómo difiere su desempeño; y qué piezas aún son demasiado nuevas, incompletas o no comparables para concluir algo. Estas preguntas se derivan de las reglas activas y no autorizan declarar un ganador con muestras pequeñas. [4]

### 8.4 Dos modalidades viables para el siguiente paso

| Modalidad | Cómo funciona | Ventajas | Límites y requisitos |
| :--- | :--- | :--- |
| **A. Piloto controlado de siete días** | Se generan cortes diarios de solo lectura con las rutas ya comprobadas; TikTok y YouTube se incorporan después de validar su fuente. El sábado se crea la hoja derivada y OmniRoute recibe briefs agregados para un reporte semanal `Draft`. | Menor riesgo, comprueba definiciones y detecta huecos antes de depender de un proceso recurrente. No requiere conceder más permisos ni mover secretos ahora. | Requiere revisión operativa de los cortes y no ofrece todavía cobertura automática completa de las cuatro plataformas. |
| **B. Loop multicanal programado** | Un proceso de solo lectura recupera deltas a diario, normaliza, actualiza artefactos canónicos y refresca la hoja derivada; después genera un brief mínimo para el análisis `Draft` diario y semanal. | Reduce el trabajo repetitivo y conserva historial uniforme por plataforma y cohorte. | Requiere aprobar por separado las rutas de acceso de TikTok/YouTube, ubicación de secretos, idempotencia, límites de tasa, mecanismo de pausa, pruebas de lectura y el destino de la hoja derivada. No puede usar los conectores de Manus directamente desde un servicio externo sin un diseño de credenciales u orquestación aprobado. |

La primera versión de este diseño no seleccionó una modalidad ni creó un schedule. La decisión posterior y su alcance quedan registrados en la sección 8.6; cualquier activación técnica conserva sus propios gates.

### 8.5 Condiciones de aprobación y coherencia documental

Antes de activar cualquier automatización se deben aprobar: la modalidad elegida; las rutas de lectura por plataforma; los campos y ventanas exactos; el formato de la hoja derivada; la cadencia; el mecanismo de pausa; y un piloto de solo lectura que no escriba métricas ni veredictos basados en la salida del modelo.

Si la propuesta se aprueba, requerirán actualización coordinada `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`, `GrowthOS/08_00_Metricas_Baseline_Plataformas.md`, `GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md`, `GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md`, `Operations/Automation/2026-08-23_Diseno_Captura_Baseline_E0_E24_E72.md` y `GrowthOS/00_01_Changelog_GrowthOS.md`. Ninguno de esos cambios se autoriza por este diseño.

### 8.6 Decisión registrada: modalidad B

El 2026-08-25 Fernando autorizó preparar la **modalidad B: loop multicanal programado**. Esta autorización permite detallar y verificar la arquitectura, pero **no activa todavía** integraciones, credenciales, lectura automática, schedule, escritura canónica, publicación ni respuestas automáticas. Cada uno de esos cambios requiere su propio gate de aprobación.

### 8.7 Contrato mínimo de datos y ejecución

El loop programado tiene dos pasos no intercambiables. Primero, un proceso determinista recoge y normaliza solo los deltas disponibles; después, OmniRoute recibe un brief sanitizado y produce análisis `Draft`. El modelo no consulta plataformas, no calcula el registro canónico y no llama a herramientas de publicación.

| Etapa | Entrada permitida | Salida | Control de integridad |
| :--- | :--- | :--- | :--- |
| 1. Lectura | Fuente autorizada de una plataforma, credencial guardada fuera del repositorio y cursor/fecha del último corte. | Respuesta de solo lectura y evidencia operacional restringida. | `read_only`, límite de tasa, timeout, registro de HTTP y error explícito. |
| 2. Normalización | Datos por publicación y cuenta, sin comentarios ni perfiles. | Filas con nombres de métrica y ventana originales; valores ausentes permanecen `null`. | Dedupe por `Platform + Platform_Content_ID + Snapshot_At_UTC`; no se rellenan ceros. |
| 3. Validación | Filas normalizadas y relación explícita con el ledger. | Lote `valid`, `partial`, `rejected` o `deferred`. | Requiere fuente, hora, plataforma y definición; nunca infiere `Concept_ID`, CNT o hipótesis. |
| 4. Escritura canónica | Solo un lote `valid`/`partial` y la evidencia asociada. | Append-only de artefactos y actualización documentada. | Idempotency key de ejecución; GitHub conserva el estado oficial antes de refrescar vistas derivadas. |
| 5. Hoja derivada | Artefactos canónicos ya confirmados. | Tablas filtrables de consulta y calidad de datos. | Si la hoja falla, el lote canónico no se revierte ni se duplica. |
| 6. Brief OmniRoute | Agregados por cohorte: plataforma, formato, etiquetas creativas, ventana, mediana/rango y limitaciones. | Nota `Draft` con observaciones, hipótesis y pruebas pequeñas. | No recibe secretos, IDs nativos, URLs privadas, handles, filas crudas ni comentarios. |
| 7. Revisión humana | Reporte determinista y Draft de OmniRoute. | Aprobación, rechazo o reescritura de hipótesis/experimento. | No hay transición automática a calendario, publicación o ledger de veredictos. |

Cada fila normalizada debe conservar al menos los siguientes campos. No todas las plataformas entregarán cada métrica; los campos no expuestos permanecen `null` y se conserva `availability_reason`.

| Grupo | Campos obligatorios | Campos condicionales |
| :--- | :--- | :--- |
| Identidad y trazabilidad | `platform`, `platform_content_id`, `published_at_utc`, `retrieved_at_utc`, `source`, `window_type`, `metric_definition`, `batch_id`, `row_status` | `publication_id`, `concept_id`, `experiment_id`, `hypothesis_id`, solo si existe vínculo explícito. |
| Clasificación editorial | `content_type`, `crosspost_status`, `maturity_status` | `character`, `hook_type`, `caption_treatment`, `narrative_structure`, solo si se registraron antes de la publicación. |
| Distribución y acción | `views`, `reach`, `impressions`, `likes_or_reactions`, `comments`, `shares`, `saves_or_favorites` | `native_engagement`, únicamente cuando la fuente documente su definición. |
| Video y crecimiento | `avg_watch_time_seconds`, `completion_rate`, `retention_3s_rate`, `followers_gained`, `subscribers_gained`, `subscribers_lost` | Cada métrica exige su unidad, fuente y denominador originales. |
| Calidad | `availability_reason`, `comparability`, `error_code`, `is_partial_period` | `raw_evidence_path` solo en almacenamiento privado/restringido; nunca en el prompt de OmniRoute. |

### 8.8 Rutas de fuente que deben comprobarse antes de activar

| Plataforma | Ruta base existente o candidata | Estado de diseño | Gate previo a automatización |
| :--- | :--- | :--- | :--- |
| Facebook | Meta Graph API y los runners E0/E24/E72 ya versionados. | Base de lectura y normalización existente; el corte diario actual es descriptivo y no cierra hipótesis. | Confirmar secreto de servidor, hook E0 real, lock y frecuencia del worker. |
| Instagram | Conector de Instagram para lectura puntual; Insights oficial o Windsor para lote analítico. | La cuenta de Universe está seleccionada para lectura; el historial distingue la validación puntual de la fuente analítica. | Verificar disponibilidad de Insights, campos, permisos y ruta sostenible fuera de una sesión manual. |
| TikTok | Windsor como fuente histórica principal; API oficial de videos como ruta alternativa autorizable. | Se debe comprobar cobertura de views, acciones, retención y crecimiento antes de elegir fuente. | Confirmar el proveedor, credenciales, límites y la deduplicación por `video_id`. |
| YouTube | Windsor como fuente histórica principal; YouTube Analytics API como ruta alternativa autorizable. | Se deben separar actividad diaria y snapshot lifetime de video. | Confirmar proveedor, autorización de canal, métricas y agregación segura por video/día. |

El horario propuesto es un corte diario cerca de las 22:00 `America/Matamoros` y un cierre semanal después del último slot del sábado. La frecuencia se configura solo tras probar que cada fuente responde con datos íntegros y que el job es idempotente; un error debe registrar `deferred` y no provocar reintentos ciegos, escrituras parciales ni conclusiones.

### 8.9 Hoja derivada y OmniRoute local

La hoja derivada deberá contener, como mínimo, tres pestañas: `Metrics_Daily_View` para cortes por contenido y plataforma, `Weekly_Growth_Draft` para cohortes maduras y `Data_Quality` para cobertura, nulos, fuente, ventana y errores. Será una vista de consulta reconstruible desde los artefactos canónicos; no podrá cambiar métricas, relaciones ni estados de los ledgers.

OmniRoute permanecerá privado en el equipo local de Fernando. Un trabajo local puede leer únicamente el brief agregado ya aprobado, llamar al combo configurado y guardar una nota `Draft` con `provider_real`, `modelo_real`, `latencia_ms`, `estado` y `decisión_humana`. Si el equipo está apagado, el resultado es `analysis_deferred`; la captura determinista y los ledgers no se alteran ni quedan bloqueados por la ausencia del modelo.

### 8.10 Validaciones realizadas y bloqueos restantes

| Elemento | Resultado de verificación | Decisión operativa |
| :--- | :--- | :--- |
| Instagram `@universe_sent_me_0326` | La cuenta quedó seleccionada para esta sesión y respondió en modo solo lectura. La lista de publicaciones devuelve ID, tipo, fecha, permalink, likes y comentarios; la consulta de insights por post devolvió `shares`, `comments`, `likes`, `saved`, `total_interactions`, `reach` y `views`. | La ruta sirve para validar contenido y obtener métricas por post. Antes de automatizarla fuera de la sesión se debe resolver una credencial o una orquestación sostenible, sin exponer tokens. |
| Facebook | El runner `run_daily_metrics_cut.py` ya implementa lectura GET-only, cruce por `Meta_Post_ID`, separación de Reels y registros descriptivos. El pipeline E0/E24/E72 dispone de módulos probados, pero su hook productivo y worker recurrente permanecen separados. | Reutilizar los runners existentes; no mezclar el schedule temporal de comentarios con el futuro job de métricas. |
| TikTok | La fuente histórica Windsor.ai está deshabilitada en la configuración actual. La integración visible TikTok for Business también está deshabilitada y se orienta a campañas publicitarias, no valida todavía la cobertura orgánica necesaria. | No activar hasta elegir y probar una ruta de datos orgánica con campos, permisos, límites y deduplicación confirmados. |
| YouTube | Windsor.ai y vidIQ están deshabilitados. La documentación oficial ofrece YouTube Analytics para consultas y Reporting API para reportes masivos, pero no hay una ruta conectada ni autorizada en esta sesión. [2] | No activar hasta elegir y probar una ruta de datos de canal que separe actividad diaria y snapshots lifetime. |
| Hoja `USM Growth OS` | Existe una hoja con pestañas históricas `Cola de Publicación`, `ExperimentLog`, `Hypothesis Bank` y `Dashboard`; su modificación más reciente fue el 8 de agosto y el dashboard no representa el contrato multicanal actual. | No se modifica. Para la vista derivada se requiere aprobar nuevas pestañas `Metrics_Daily_View`, `Weekly_Growth_Draft` y `Data_Quality`, o crear una hoja separada de consulta. |

Estas verificaciones no añaden una fuente canónica nueva ni autorizan un schedule. El siguiente gate es elegir la ruta sostenible de TikTok y YouTube, decidir el destino de la hoja derivada y aprobar dónde residirá la autenticación de los procesos de solo lectura.

### 8.11 Comparación de costo: equipo local vs. servicio independiente

Fernando eligió como runtime primario su equipo Xubuntu junto a OmniRoute. Esta opción no incorpora una nueva suscripción de hosting: depende de que el equipo, su conexión y la sesión local permanezcan disponibles. El costo de fuentes de datos es independiente del lugar donde se ejecute el job.

| Componente | Equipo Xubuntu local | VPS independiente orientativo |
| :--- | :--- | :--- |
| Ejecución del job y OmniRoute | Sin cuota adicional de servidor; depende de electricidad, internet y que el equipo permanezca encendido. | Un VPS pequeño requiere al menos 2 GB de RAM para mantener sistema, job y OmniRoute con margen operativo. Un ejemplo público de 1 vCPU / 2 GB en DigitalOcean figura en USD 12/mes, sin respaldos opcionales. [5] |
| Recuperación ante apagones | El análisis se marca `analysis_deferred`; el siguiente ciclo no debe duplicar ni completar artificialmente el anterior. | Mayor continuidad, pero requiere hardening, actualizaciones, backups, firewall, monitoreo y una política de respuesta a incidentes. |
| Datos y credenciales | Permanecen bajo control local; nunca se guardan en GitHub ni se envían a OmniRoute. | Deben residir en un almacén de secretos del proveedor y nunca en archivos versionados. Requiere una aprobación adicional de infraestructura. |
| Windsor.ai para TikTok y YouTube | Igual costo que en un VPS; la opción local no elimina esta suscripción si se utilizan ambas fuentes. | Igual costo que en local. |

Para dos fuentes —TikTok y YouTube— la referencia pública de Windsor.ai indica que el plan gratuito permanente permite solo una fuente y una cuenta; el plan Basic admite tres fuentes con actualización diaria por USD 23/mes o USD 19/mes facturado anualmente. [6] En consecuencia, un escenario independiente mínimo con Windsor Basic y un VPS de 2 GB equivale aproximadamente a **USD 35/mes antes de impuestos, respaldos y posibles cargos del proveedor**. El mismo escenario sobre Xubuntu elimina el VPS y conserva solo el costo de Windsor, si se decide continuar después de la prueba.

No se contratará ningún servicio por este documento. La opción local es la decisión vigente; un VPS solo se reconsidera si el equipo no puede mantenerse encendido con suficiente regularidad o si se requiere independencia operativa total.

### 8.12 Hoja derivada preparada

El 2026-08-25 se crearon en la hoja existente `USM Growth OS` las pestañas vacías `Metrics_Daily_View`, `Weekly_Growth_Draft` y `Data_Quality`. La acción fue autorizada por Fernando y se limitó a añadir estas tres vistas; `Cola de Publicación`, `ExperimentLog`, `Hypothesis Bank` y `Dashboard` permanecieron sin cambios.

Las pestañas aún no contienen datos, fórmulas ni headers. Su estructura final se cargará únicamente después de confirmar una fuente con cobertura válida para TikTok y YouTube y de aprobar el piloto programado de solo lectura. Esto evita presentar una hoja parcialmente configurada como una fuente de verdad o inducir conclusiones antes de que existan cortes reproducibles.

### 8.13 Prueba de Windsor.ai y alternativas de bajo costo

La prueba autorizada de Windsor.ai se habilitó sin crear pagos, tareas de destino ni acciones de escritura. El perfil responde como `Trial` y ya conserva conexiones de lectura para `tiktok_organic`, `youtube`, Facebook orgánico e Instagram. La consulta de TikTok para la cuenta Universe Sent Me devolvió registros por video con `video_views_count`, `video_likes`, `video_comments`, `video_shares`, `video_favorites`, `video_reach`, `video_average_time_watched` y `video_full_watched_rate`; por tanto, cubre el contrato mínimo de TikTok para la prueba.

La conexión de YouTube tiene dos cuentas etiquetadas `baminacan@gmail.com` e `io.marketing.09@gmail.com`, ninguna identificada explícitamente como Universe Sent Me. Para mantener la separación de marcas, no se consultó contenido de ninguna de ellas. Fernando debe identificar cuál corresponde al canal de Universe Sent Me antes de cualquier lectura o automatización de YouTube.

| Alternativa | Costo recurrente de software/intermediario | Cobertura útil | Condición y límite |
| :--- | :--- | :--- | :--- |
| **APIs oficiales directas + Python/cron local** | Sin cuota de un intermediario; usa el equipo Xubuntu ya elegido. | TikTok Display API puede devolver por video views, likes, comments y shares; YouTube Analytics consulta views, watch time y subscribers por canal/video. [7] [8] | Requiere registrar clientes OAuth, guardar tokens solo en el equipo local y mantener dos integraciones. TikTok no sustituye la analítica avanzada de retención disponible en Windsor. |
| **Windsor.ai** | Trial activo; su precio publicado para Basic es USD 23/mes o USD 19/mes anual si se requieren dos fuentes. [6] | En esta prueba ya confirmó cobertura amplia de TikTok y expone campos de YouTube, además de conectores y destinos comunes. | El plan gratuito permanente limita la cuenta a una fuente y una cuenta; el servicio no debe crear exports ni acciones de escritura sin un gate separado. [6] |
| **n8n Community autoalojado** | Sin cuota de software; se ejecuta junto a OmniRoute en Xubuntu. [9] | Orquesta llamadas a las APIs oficiales, validación, GitHub y hoja derivada. | No añade datos ni credenciales: sigue requiriendo las APIs oficiales. También añade mantenimiento operativo y no se instala por este documento. |
| **Apps Script para YouTube** | Sin servidor adicional; corre asociado a Google Workspace. | Puede llevar métricas de YouTube Analytics a una hoja mediante un servicio avanzado. [10] | Solo resuelve YouTube, desplaza parte de la automatización fuera de GitHub y no resuelve TikTok; no se usa como fuente canónica sin rediseño. |

La ruta de menor costo recurrente es utilizar APIs oficiales directas con un script local programado; la ruta de menor esfuerzo técnico es conservar Windsor.ai, sujeta a su precio tras la prueba. Una combinación transitoria también es posible: usar Windsor solo para validar TikTok mientras se construye la integración oficial de YouTube, pero no se debe contratar ni programar una exportación hasta que Fernando elija la fuente final.

## Referencias

[1]: https://developers.facebook.com/docs/instagram-api/guides/insights "Meta for Developers — Instagram Insights"
[2]: https://developers.google.com/youtube/analytics "Google for Developers — YouTube Analytics and Reporting APIs"
[3]: https://developers.tiktok.com/doc/tiktok-api-v2-video-query/ "TikTok for Developers — Query Videos"
[4]: ../../GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md "Growth OS — Reglas estratégicas de aprendizaje y tendencias"
[5]: https://www.digitalocean.com/pricing/droplets "DigitalOcean — Droplet pricing"
[6]: https://windsor.ai/pricing/ "Windsor.ai — Pricing"
[7]: https://developers.tiktok.com/doc/tiktok-api-v2-video-query/ "TikTok for Developers — Query Videos"
[8]: https://developers.google.com/youtube/analytics/reference/reports/query "Google for Developers — YouTube Analytics Reports: Query"
[9]: https://docs.n8n.io/choose-how-to-use-n8n/ "n8n Docs — Self-hosted Community edition"
[10]: https://developers.google.com/apps-script/advanced/youtube-analytics "Google for Developers — Apps Script YouTube Analytics service"
