---
title: "Hallazgos visuales — 57 posts de junio sin match"
purpose: "Determinar qué reservas de junio aportan evidencia útil para personajes o celdas comparables sin convertir la cola completa en CNT ni en canon."
status: Active
created: 2026-08-21
updated: 2026-08-21
version: "0.3"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv"
  - "Operations/Research/2026-08-21_Junio_57_Unmatched_Meta_Raw.json"
  - "Operations/Research/2026-08-21_Junio_57_Unmatched_Character_Utility.csv"
  - "Operations/Research/2026-08-21_Junio_57_Approved_Character_Analysis.md"
  - "Operations/Research/2026-08-21_Junio_Priority_Queue_Visual_Findings.md"
  - "Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv"
  - "Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md"
organization: "Operations/Research"
---

# Hallazgos visuales — 57 posts de junio sin match

## Método

La cola contiene 57 publicaciones `Needs_Asset_Match`. Meta devolvió imágenes para 56; una publicación, `1036844829507460_122129194233072582`, permanece sin `full_picture`. La revisión se realizó por `Meta_ID`, fecha, caption y composición visual. Los filenames o semejanzas generales de estilo no se consideran prueba de personaje ni de `Asset_Ref`.

La clasificación completa se conserva en `2026-08-21_Junio_57_Unmatched_Character_Utility.csv`. Las etiquetas de personaje son hipótesis visuales para análisis, no asignaciones canónicas.

## Resultado de cobertura

| Clase | Casos | Decisión |
|---|---:|---|
| `Format_Control` | 36 | Mantener como controles de formato, texto, fotografía o relación; no son necesarios para ranking de personajes |
| `Character_Review` | 19 | 17 pasan a análisis visual selectivo sin CNT; 2 quedan como reserva por bajo valor |
| `Cell_Candidate` | 1 | `122127951885072582` queda como candidato de revisión para microhistoria estricta |
| `No_Visual_Evidence` | 1 | Mantener en reserva; no inferir personaje desde caption |
| **Total** | **57** | La cola no se integra masivamente |

## Casos necesarios para análisis de personajes

| Personaje o grupo visual | Meta_ID | Rango | Interacciones | Shares | Utilidad |
|---|---|---:|---:|---:|---|
| Universe visual candidato: gato musculoso con gato con gafas | `1036844829507460_122130196011072582` | 25 | 164 | 42 | Prioridad máxima; control de transformación e identidad |
| Universe visual candidato: gato con gafas en nube | `1036844829507460_122125520661072582` | 87 | 15 | 1 | Control de identidad visual |
| Universe visual candidato: gato con gafas, caption relacional/sexual | `1036844829507460_122128989885072582` | 108 | 11 | 0 | Separar identidad visual de categoría de humor |
| Universe visual candidato: gato con gafas en muro | `1036844829507460_122130324285072582` | 149 | 7 | 0 | Control de identidad visual de bajo rendimiento |
| Universe visual candidato: gato con gafas en nube | `1036844829507460_122133558903072582` | 179 | 4 | 1 | Reserva de identidad visual |
| Wilfred visual candidato: gnome en bosque | `1036844829507460_122125544019072582` | 74 | 18 | 2 | Continuidad de personaje, no señal de rendimiento |
| Wilfred visual candidato: gnome frente a teclado | `1036844829507460_122134065975072582` | 120 | 10 | 1 | Mejor caso adicional de Wilfred por legibilidad visual |
| Wilfred visual candidato: gnome en bosque | `1036844829507460_122130309663072582` | 161 | 6 | 2 | Segundo control de continuidad |
| Wilfred visual candidato: gnome en diálogo | `1036844829507460_122130032151072582` | 177 | 4 | 0 | Borderline de diálogo, mantener separado |
| Wilfred visual candidato: gnome haciendo playlist | `1036844829507460_122126670549072582` | 184 | 3 | 0 | Reserva de continuidad |
| Ganso visual candidato: pato/ave con vestuario formal | `1036844829507460_122134608507072582` | 98 | 14 | 2 | Subcelda de vestuario de personaje secundario |
| Fantasma visual candidato: figura blanca en bosque | `1036844829507460_122130329817072582` | 99 | 13 | 1 | Control de identidad visual; no canonizar |
| Fantasma visual candidato: figura blanca en bosque | `1036844829507460_122125895013072582` | 195 | 2 | 0 | Segundo control de identidad de bajo rendimiento |
| Silvio visual candidato: figura clown de pelo morado | `1036844829507460_122133424479072582` | 170 | 5 | 1 | Evidencia de presencia visual, no regla de rendimiento |
| Roster mixto: grupo de personajes alrededor de fogata | `1036844829507460_122131071243072582` | 126 | 9 | 0 | Útil para continuidad de elenco; no atribuir a un personaje individual |
| Mujer mágica no identificada | `1036844829507460_122134055109072582` | 128 | 9 | 0 | No asignar automáticamente a Elara |
| Mujer y gato en escena fantástica | `1036844829507460_122126239515072582` | 155 | 6 | 0 | Relación visual candidata; no asignar Kiri/Universe |

Los dos casos de personaje que no pasan a análisis inmediato son `1036844829507460_122126283465072582` —mujer fantástica de 4 interacciones— y `1036844829507460_122126267355072582` —gnome de 1 interacción—. Se conservan como reserva porque aportan poca información marginal frente a los controles de mayor legibilidad.

## Caso de celda comparable

El post `1036844829507460_122127951885072582` (`r229`, 0 interacciones lifetime en la cola) muestra una composición de cuatro paneles con conversación telefónica, turnos claros y remate visual de baile. Es un candidato de **microhistoria secuencial estricta**, pero queda en `Candidate_Review` hasta comprobar la definición vigente de la celda y, si se quiere integrarlo al ledger visual, localizar su asset en Drive. No se promueve por ser un caso de rendimiento alto; se promueve solo si cumple la estructura comparable.

## Casos que no son necesarios para personajes

Los 36 `Format_Control` son principalmente fotografías de naturaleza o carretera con texto, cielos con captions, composiciones motivacionales, parejas o personas genéricas, infográficos sexuales y referencias de plataforma. Pueden servir como controles de formato o de confusión, pero no deben entrar en rankings de Universe, Wilfred, Elara, Kiri, Silvio, Fantasma o Ganso.

El único caso sin imagen, `1036844829507460_122129194233072582`, tampoco debe clasificarse por caption. La ausencia de `full_picture` es una limitación de evidencia y no una señal de que carezca de personaje.

## Aprobación de Fernando

El **21 de agosto de 2026**, Fernando aprobó incorporar los 17 casos de personaje a la capa de análisis selectivo. La autorización cubre descripción visual, hipótesis de personaje, rol narrativo, potencial de etiquetado y relación con celdas. No cubre la creación de CNT, la modificación del canon, el reuse, el calendario ni la publicación de contenido. El ledger registra la autorización con `approval_status=Approved_Character_Analysis`, `approval_by=Fernando` y `approval_scope=Selective_character_analysis_only`.

El candidato `1036844829507460_122127951885072582` fue validado estructuralmente como una secuencia de cuatro paneles. Su estado pasa a `Excluded_3P_Retain_4P_Candidate`: queda fuera de `MICRO-STRICT-3P` por no cumplir el conteo exacto de tres paneles, y se conserva únicamente como candidato potencial de una futura `MICRO-SEQ-4P`. Esa subcelda no se abre todavía.

## Decisión operativa

La cola de junio sí contiene material necesario para el análisis de personajes, pero solo en una capa selectiva de **17 casos aprobados** y **2 reservas visuales**. El corte cuantitativo conserva 300 interacciones y 53 shares en los 17 casos, pero el caso Universe de 164 interacciones y 42 shares concentra 54.7% de las interacciones y 79.2% de los shares; sin él, la mediana baja a 8 interacciones y 0.5 shares. No se crea un ranking de personajes ni se infiere causalidad. No se crean CNT, no se agregan los casos al canon y no se modifican calendario ni reuse.

Las transformaciones de Universe deben registrar `preserva_gafas_universe` y `preserva_marcadores_identidad`. Un gato con gafas se registra como marcador visual candidato; no demuestra por sí solo identidad canónica.
