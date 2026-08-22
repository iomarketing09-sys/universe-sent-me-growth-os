---
title: "Brief de celda Reels Motion + POV/Meme 001"
purpose: "Diseñar los tres primeros casos controlados para probar si el movimiento físico inmediatamente legible, combinado con un hook POV o un meme reconocible, supera en descubrimiento y compartidos al formato tipo podcast/radio."
status: Review
created: 2026-08-22
updated: 2026-08-22
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "../../GrowthOS/07_00_Registro_Maestro_Reels.md"
  - "../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
  - "../Research/2026-08-19_Auditoria_Reels_y_Monetizacion.md"
  - "../Research/2026-08-22_Reels_Confirmed_Metric_Assessment.json"
  - "../Research/2026-08-22_Reels_Confirmed_Classification.csv"
  - "2026-08-22_Brief_Reel_Dialogue_Radio_003.md"
organization: "Operations/Production"
---

# Brief de celda Reels Motion + POV/Meme 001

## 1. Estado y decisión de producción

Este documento está en **Review** y requiere aprobación humana antes de preparar referencias finales, generar video, crear CNT, asignar slots o publicar. No autoriza ninguna acción en Facebook, Instagram, TikTok o YouTube.

La celda reemplaza temporalmente a `Dialogue_radio` como prioridad de adaptación. La familia de radio no se elimina del historial: queda como observación secundaria y su brief anterior permanece archivado. La hipótesis activa de diseño es `HB-REEL-MOTION-POV-MEME-01`.

## 2. Corrección editorial del caso Piscis

El caso de referencia no utiliza a Evan. La escena correcta es:

> **Elara camina por el bosque usando audífonos. Wilfred aparece detrás, la sigue y le habla, pero Elara lo ignora porque viene concentrada en sus audífonos. El texto visible es `POV: Eres Piscis`.**

El asset `Elara y Evan en el Bosque.mp4` pertenece a otro Reel más reciente de Elara y Evan juntos en el bosque/campamento. La asociación anterior con `CON-2026-08-09-Elara_Evan_Estrellas` fue retirada y queda pendiente de reasignación al ID nativo correcto. No se debe reutilizar como referencia de personajes para el caso Piscis ni relabelarlo como Wilfred. El caso Piscis permanece pendiente de `Meta_Post_ID`, `Primary_Asset_ID` y reconciliación visual propios.

Las anclas obligatorias del nuevo caso son las siguientes:

| Personaje | Anclas que deben conservarse |
|---|---|
| Elara | Sombrero puntiagudo, cabello claro, cardigan café, audífonos visibles. |
| Wilfred | Sombrero rojo puntiagudo, barba blanca larga, túnica verde. Debe aparecer detrás de Elara y hablarle sin conseguir que ella se vuelva. |
| Entorno | Bosque mágico, pero distinto de la cabina de radio y sin copiar la composición del Reel de Evan. |

## 3. Hipótesis y unidad de comparación

> **HB-REEL-MOTION-POV-MEME-01:** los Reels con movimiento físico inmediatamente legible, un hook POV o meme reconocible durante los primeros tres segundos y un payoff visual claro pueden generar más descubrimiento y compartidos que una conversación de estudio que exige escuchar o leer varios turnos.

La unidad de análisis será **una publicación de Reel por plataforma**, no un asset abstracto. Los tres casos deben publicarse primero en la misma plataforma primaria —Facebook—, sin producto afiliado, sin pauta y sin mezclar sus métricas con imágenes, P0, Wave 1 o afiliación. Si después se hace crosspost, cada plataforma conservará su propio ID y snapshot.

La celda debe tener tres casos comparables para una señal preliminar. Cinco casos serán preferibles para una decisión operativa. Los dos Reels históricos de radio y el Reel histórico de Fantasma se conservarán como evidencia contextual, no como controles perfectamente balanceados.

## 4. Controles comunes de la celda

| Variable | Especificación controlada |
|---|---|
| Plataforma primaria | Facebook; Instagram/TikTok/YouTube solo como crosspost posterior y separado. |
| Duración | 7–10 segundos por Reel; ningún caso debe superar 12 segundos. |
| Hook | Texto visible antes de 0.8 s; acción física identificable antes de 1.5 s; sin logo introductorio. |
| Movimiento | Caminar, seguir, cruzar, entrar o salir de una escena; no limitarse a zoom, parpadeo o paneo sobre una imagen fija. |
| Payoff | Debe entenderse por la imagen final sin depender de explicación en caption. |
| Texto en pantalla | Una frase principal; legible en móvil y sin bloques extensos. |
| `Caption_Treatment` | `caption_minimo`: una línea externa, 0–2 emojis como máximo, sin repetir literalmente todo el texto sobreimpreso. |
| `Caption_Function` | `reforzar_remate`: el caption agrega complicidad o contexto breve, pero no explica la escena. |
| Audio | Ambiente o música discreta; el chiste debe entenderse sin audio. No usar diálogo como requisito de comprensión. |
| Watermark | Ausente o registrado explícitamente; no debe variar entre casos. |
| Afiliación | Excluida. No agregar productos ni enlaces nativos. |
| Reuse | Caso nuevo o adaptación con edad mínima de 30 días; no repost idéntico. |
| Ventana | Snapshot de 24 h y 72 h por publicación; registrar hora local, fuente y definición. |
| Métricas primarias | Views, reach, porcentaje de no seguidores, retención inicial, tiempo medio de reproducción, completación y shares. |
| Métricas secundarias | Comentarios, respuestas y seguidores ganados. Likes se conservan, pero no son criterio principal. |

La igualdad de caption se controla por tratamiento y función, no por copiar la misma frase en los tres casos. `Caption_Treatment` y `Caption_Function` deben registrarse como campos separados en el ledger de cada publicación.

## 5. Casos propuestos

### Caso MPM-001 — Elara ignora a Wilfred

| Campo | Especificación |
|---|---|
| `Case_ID` | `MPM-001` |
| `Family_Candidate` | `POV_character_movement` |
| `Concept_ID` | Nuevo concepto; no asignar el concepto de Evan/Elara. |
| `Experiment_ID` | `EXP-202608-REEL-MOTION-POV-MEME-001` |
| `Hypothesis_ID` | `HB-REEL-MOTION-POV-MEME-01` |
| `Hook_Type` | `POV_zodiac_situation` |
| `On_Screen_Text` | `POV: Eres Piscis` |
| `Caption_Treatment` | `caption_minimo` |
| `Caption_Function` | `reforzar_remate` |
| `Caption_Proposed` | `No es que no lo escuche… es que trae su propio universo. 👀` |
| `Characters` | Elara + Wilfred |
| `Motion_Beat` | Elara camina hacia cámara o en plano lateral; Wilfred la sigue detrás, mueve la boca y gesticula; ella nunca se vuelve. |
| `Payoff` | Wilfred se queda un paso atrás y mira a cámara mientras Elara continúa caminando sin enterarse. |
| `Duration_Target` | 8–9 segundos |

La acción debe comunicar la broma incluso en silencio: los audífonos de Elara son la causa visible de la desconexión, no una explicación posterior. No incluir a Evan, camping, tienda de campaña ni elementos del Reel `CON-2026-08-09-Elara_Evan_Estrellas`.

### Caso MPM-002 — Fantasma y los gatos saben algo que él no

| Campo | Especificación |
|---|---|
| `Case_ID` | `MPM-002` |
| `Family_Candidate` | `Motion_meme_adaptation` |
| `Concept_ID` | Nuevo concepto; adaptación, no repost del Reel histórico. |
| `Experiment_ID` | `EXP-202608-REEL-MOTION-POV-MEME-001` |
| `Hypothesis_ID` | `HB-REEL-MOTION-POV-MEME-01` |
| `Hook_Type` | `meme_visual_chain` |
| `On_Screen_Text` | `POV: Dices que no vas a seguir la corriente` |
| `Caption_Treatment` | `caption_minimo` |
| `Caption_Function` | `reforzar_remate` |
| `Caption_Proposed` | `Los gatos ya tomaron la decisión por ti. 👻🐈` |
| `Characters` | Fantasma + tres gatos |
| `Motion_Beat` | Fantasma camina por un sendero; los gatos lo siguen y cada uno cruza el encuadre con el mismo tratamiento de texto, creando una cadena visual clara. |
| `Payoff` | Fantasma se detiene; los gatos continúan y lo obligan visualmente a seguirlos. |
| `Duration_Target` | 7–8 segundos |

Este caso toma la lógica que funcionó —meme reconocible, movimiento de caminata, múltiples figuras y texto repetido—, pero exige un escenario, recorrido y export nuevos. No se reutilizan los archivos `Ghost_walks_cats_through_forest_202607240113.mp4` ni `Ghost_walks_cats_through_forest_202607251436.mp4` como publicación idéntica. El Reel histórico de Fantasma con gatos es una referencia de rendimiento y no un cuarto caso de la celda.

### Caso MPM-003 — Universe dijo “solo cinco minutos”

| Campo | Especificación |
|---|---|
| `Case_ID` | `MPM-003` |
| `Family_Candidate` | `POV_character_movement` |
| `Concept_ID` | Nuevo concepto de Universe; no mezclar con `CON-2026-08-19-DobleCheck-Universe`. |
| `Experiment_ID` | `EXP-202608-REEL-MOTION-POV-MEME-001` |
| `Hypothesis_ID` | `HB-REEL-MOTION-POV-MEME-01` |
| `Hook_Type` | `POV_modern_habit` |
| `On_Screen_Text` | `POV: Dijiste “solo cinco minutos”` |
| `Caption_Treatment` | `caption_minimo` |
| `Caption_Function` | `reforzar_remate` |
| `Caption_Proposed` | `Y el portal ya cambió de horario. 🫠` |
| `Characters` | Universe |
| `Motion_Beat` | Universe, gato blanco con gafas redondas visibles, camina con el teléfono hacia un portal; el fondo cambia de noche a amanecer mientras mantiene el paso. |
| `Payoff` | Sale del portal con la misma expresión y la luz del amanecer; las gafas permanecen visibles y no se transforma su identidad. |
| `Duration_Target` | 8–10 segundos |

El caso prueba si la combinación de hábito digital reconocible y movimiento puede trasladar la señal de Universe a la misma celda sin depender de una conversación. Las gafas redondas deben ser visibles desde el primer plano y en el último; no se permite una transformación que las oculte.

## 6. Orden de producción y aleatorización

No se debe interpretar el orden como ranking creativo. Una vez aprobados los tres casos, se recomienda asignar los tres a slots de fuerza equivalente —10:00–11:00, 16:00–17:00 o 19:00–21:00— y registrar el horario exacto. Si la operación lo permite, el orden de publicación debe sortearse entre los tres casos después de verificar identidad y export. No se deben agregar links de Mercado Libre, CTA de producto, boosts ni cambios de caption después de publicar.

El caso MPM-001 no depende de encontrar primero el ID histórico de Piscis para poder producirlo; el ID histórico sirve para reconciliar la evidencia y evitar atribuir el asset de Evan. La pieza nueva debe recibir su propio `Concept_ID`, `Primary_Asset_ID`, `Experiment_ID` e ID nativo después de publicar.

## 7. Gate de aprobación

Fernando debe aprobar por separado: el texto `POV: Eres Piscis`, la identidad visual de Elara y Wilfred, la ausencia de Evan, la estructura del meme de Fantasma, la preservación de las gafas de Universe, los tres captions externos, la duración y la exclusión de afiliación. La aprobación de este brief no autoriza generación automática, programación ni publicación.

Después de generar, cada export pasa por revisión de identidad, legibilidad, movimiento, ausencia de watermark no registrado y comprensión sin audio. Después de publicar, se registran snapshots de 24 h y 72 h. No se declara `WIN` con un solo caso; el mínimo es n=3 y la decisión operativa requiere llegar a n=5.

## 8. Evaluación de calidad de las propuestas

| Caso | Relatable | Humor/emoción | Giro moderno | Voz de personaje | Share hook | Slot | Resultado |
|---|---:|---:|---:|---:|---:|---:|---|
| MPM-001 | 9 | 9 | 8 | 9 | 9 | 10 | **9.00/10 — PASS** |
| MPM-002 | 9 | 10 | 6 | 9 | 10 | 10 | **9.20/10 — PASS** |
| MPM-003 | 10 | 9 | 10 | 9 | 9 | 10 | **9.50/10 — PASS** |

Los puntajes fueron ejecutados con la rúbrica vigente de propuestas de Growth OS. En esta celda, `format_ok` representa que el Reel tiene movimiento real y no es un Reel de texto estático; el texto funciona como hook visual breve, no como sustituto de una escena.

## 9. Documentos que requieren sincronización

Al aprobarse este brief, deberán actualizarse el ledger de publicaciones de Reels, el staging de producción y la evaluación de la hipótesis. Hasta entonces, no se crea CNT, no se modifica el calendario y no se actualiza `ExperimentLog`.

La corrección del caso Piscis y la separación del asset de Evan/Elara quedan enlazadas con el registro maestro, la fuente maestra y la evaluación estructurada. No se requiere crear otro documento conceptual mientras esta celda permanezca en Review.

## Referencias

[1]: ../../GrowthOS/07_00_Registro_Maestro_Reels.md "Registro Maestro de Reels"
[2]: ../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md "Fuente maestra y ledgers del Growth OS"
[3]: ../Research/2026-08-19_Auditoria_Reels_y_Monetizacion.md "Auditoría de Reels y monetización"
[4]: ../Research/2026-08-22_Reels_Confirmed_Metric_Assessment.json "Evaluación de evidencia de métricas de Reels confirmados"
[5]: ../Research/2026-08-22_Reels_Confirmed_Classification.csv "Clasificación operativa de Reels con asset confirmado"
[6]: 2026-08-22_Brief_Reel_Dialogue_Radio_003.md "Brief archivado Dialogue_radio 003"

> La evidencia histórica debe interpretarse por plataforma y ventana. Los snapshots de Fantasma con gatos son una referencia de alto impacto, no una baseline perfectamente comparable con los nuevos casos. [1] [3] [4]

## Nota de actualización

Este brief reemplaza la prioridad anterior de Dialogue_radio, pero no borra sus registros históricos. Si Fernando aprueba los tres casos, el siguiente documento operativo será el paquete de referencias y generación visual; la producción seguirá bloqueada hasta esa aprobación.
