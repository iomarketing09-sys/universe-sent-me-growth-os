---
title: "Diseño de asistencia de métricas y respuestas con OmniRoute"
purpose: "Definir cómo OmniRoute puede analizar resúmenes métricos ya normalizados y producir propuestas de respuesta comunitaria sin convertirse en fuente canónica, sistema de moderación automática ni publicador autónomo."
status: Review
created: 2026-08-23
updated: 2026-08-23
version: "1.0"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-19_Decision_Gateway_IA_OmniRoute.md"
  - "Operations/Production/2026-08-18_Piloto_Local_OmniRoute_Seguro.md"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
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
