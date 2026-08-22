---
title: "Brief de celda Reels Motion + POV/Meme 001"
purpose: "Diseñar los tres primeros casos controlados para probar si el movimiento físico inmediatamente legible, combinado con un hook situacional o un meme reconocible, supera en descubrimiento y compartidos al formato tipo podcast/radio; MPM-001 abre además una serie musical recurrente de Elara caminando con audífonos."
status: Active
created: 2026-08-22
updated: 2026-08-22
version: "1.8"
author: "Manus AI (CGO)"
related_documents:
  - "../../GrowthOS/07_00_Registro_Maestro_Reels.md"
  - "../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
  - "../Research/2026-08-19_Auditoria_Reels_y_Monetizacion.md"
  - "../Research/2026-08-22_Reels_Confirmed_Metric_Assessment.json"
  - "../Research/2026-08-22_Reels_Confirmed_Classification.csv"
  - "../Research/2026-08-22_Reels_Metric_Instrumentation_Protocol.md"
  - "2026-08-22_Brief_Reel_Dialogue_Radio_003.md"
organization: "Operations/Production"
---

# Brief de celda Reels Motion + POV/Meme 001

## 1. Estado y decisión de producción

Este documento está **Active** porque MPM-001 ya fue publicado y entra a medición. La producción, programación o publicación de MPM-002 y MPM-003 sigue requiriendo aprobación humana separada; este estado no autoriza acciones adicionales en Facebook, Instagram, TikTok o YouTube.

La celda reemplaza temporalmente a `Dialogue_radio` como prioridad de adaptación. La familia de radio no se elimina del historial: queda como observación secundaria y su brief anterior permanece archivado. La hipótesis activa de diseño es `HB-REEL-MOTION-POV-MEME-01`.

## 2. Nueva premisa editorial de MPM-001

El caso de referencia no utiliza a Evan. La escena correcta es:

> **Elara camina por el bosque usando audífonos. Wilfred aparece detrás, la sigue y le habla, pero Elara lo ignora porque está completamente dentro de su experiencia auditiva. No habrá texto sobre la imagen: el hook será la situación visual y la música funcionará como capa emocional no explicada.**

El asset `Elara y Evan en el Bosque.mp4` pertenece a otro Reel más reciente de Elara y Evan juntos en el bosque/campamento. La asociación anterior con `CON-2026-08-09-Elara_Evan_Estrellas` fue retirada y queda pendiente de reasignación al ID nativo correcto. No se debe reutilizar como referencia de personajes para MPM-001 ni relabelarlo como Wilfred. MPM-001 permanece pendiente de `Meta_Post_ID`, `Primary_Asset_ID` y reconciliación visual propios.

Las anclas obligatorias del nuevo caso son las siguientes:

| Personaje | Anclas que deben conservarse |
|---|---|
| Elara | Sombrero puntiagudo, cabello claro, cardigan café, audífonos visibles. |
| Wilfred | Sombrero rojo puntiagudo, barba blanca larga, túnica verde. Debe aparecer detrás de Elara y hablarle sin conseguir que ella se vuelva. |
| Entorno | Bosque mágico, pero distinto de la cabina de radio y sin copiar la composición del Reel de Evan. |

## 3. Hipótesis y unidad de comparación

> **HB-REEL-MOTION-POV-MEME-01:** los Reels con movimiento físico inmediatamente legible, un hook situacional o meme reconocible durante los primeros tres segundos y un payoff visual claro pueden generar más descubrimiento y compartidos que una conversación de estudio que exige escuchar o leer varios turnos.
>
> **Subhipótesis propuesta `HB-REEL-MUSIC-WALK-01`:** una serie de caminatas de Elara con audífonos, donde el audio funciona como identidad emocional pero no se explica en el video, puede crear variantes repetibles de humor visual y abrir una superficie editorial para proponer música sin sacrificar comprensión silenciosa.

La unidad de análisis será **una publicación de Reel por plataforma**, no un asset abstracto. Los tres casos deben publicarse primero en la misma plataforma primaria —Facebook—, sin producto afiliado, sin pauta y sin mezclar sus métricas con imágenes, P0, Wave 1 o afiliación. Si después se hace crosspost, cada plataforma conservará su propio ID y snapshot.

La celda debe tener tres casos comparables para una señal preliminar. Cinco casos serán preferibles para una decisión operativa. Los dos Reels históricos de radio y el Reel histórico de Fantasma se conservarán como evidencia contextual, no como controles perfectamente balanceados.

## 4. Controles comunes de la celda

| Variable | Especificación controlada |
|---|---|
| Plataforma primaria | Facebook; Instagram/TikTok/YouTube solo como crosspost posterior y separado. |
| Duración | 7–10 segundos por Reel; ningún caso debe superar 12 segundos. |
| Hook | El hook puede ser textual o puramente visual; en MPM-001 no habrá texto y la acción física debe ser identificable antes de 1.5 s, sin logo introductorio. |
| Movimiento | Caminar, seguir, cruzar, entrar o salir de una escena; no limitarse a zoom, parpadeo o paneo sobre una imagen fija. |
| Payoff | Debe entenderse por la imagen final sin depender de explicación en caption. |
| Texto en pantalla | Por caso: MPM-001 usa `None`; no añadir texto sobre la imagen. Los otros casos pueden usar una sola frase breve si su ficha lo conserva. |
| `Caption_Treatment` | `caption_minimo`: una línea externa, 0–2 emojis como máximo, sin repetir literalmente todo el texto sobreimpreso. |
| `Caption_Function` | `reforzar_remate`: el caption agrega complicidad o contexto breve, pero no explica la escena. |
| Audio | Música o ambiente discreto seleccionado en post; el chiste debe entenderse sin audio. No usar diálogo como requisito de comprensión ni revelar la canción en texto. |
| Watermark | Ausente o registrado explícitamente; no debe variar entre casos. |
| Afiliación | Excluida. No agregar productos ni enlaces nativos. |
| Reuse | Caso nuevo o adaptación con edad mínima de 30 días; no repost idéntico. |
| Ventana | Reporte diario como fuente operativa; niveles L1/L2/L3 por publicación. Snapshot 24/72 solo como capa contractual opcional. |
| Métricas primarias | Views, reach, porcentaje de no seguidores, retención inicial, tiempo medio de reproducción, completación y shares. |
| Métricas secundarias | Comentarios, respuestas y seguidores ganados. Likes se conservan, pero no son criterio principal. |

La igualdad de caption se controla por tratamiento y función, no por copiar la misma frase en los tres casos. `Caption_Treatment` y `Caption_Function` deben registrarse como campos separados en el ledger de cada publicación.

### 4.1 Capa musical de la serie Elara Walk

MPM-001 inaugura una serie opcional de variantes de Elara caminando con audífonos en situaciones distintas. La música no se menciona ni se explica en el hook, en los subtítulos ni en el caption. Puede existir como audio de fondo o como referencia editorial para elegir un sonido, pero la escena debe conservar su comprensión en silencio.

| Campo | Regla para la serie |
|---|---|
| `Series_ID` | `ELARA-WALK-MUSIC-01` |
| `Music_Variant_ID` | Identificador interno de la pista o dirección sonora usada en cada variante |
| `Music_Reference` | Género, mood o referencia de grupo/artista/canción para curaduría; no se imprime automáticamente en el Reel |
| `Audio_Source` | Sonido original, pista licenciada o audio disponible en la biblioteca de la plataforma; debe registrarse explícitamente |
| `Music_Hashtag` | Opcional; máximo uno o dos hashtags relevantes, solo después de validar que describen el audio realmente usado |
| `Visible_Music_Explanation` | `No` |
| `Silent_Comprehension` | `Required` |
| `Character_Anchor` | Sombrero puntiagudo, cabello claro, cardigan café y audífonos visibles |

Las primeras direcciones sonoras que se pueden explorar son: **indie dream-pop suave** para una caminata de desconexión; **alt-pop con pulso firme** para una caminata de indiferencia segura; y **folk etéreo o dark-folk ligero** para una caminata nocturna en el bosque. Estas son direcciones creativas, no canciones aprobadas. El grupo, artista, canción o hashtag concreto se registra solo cuando se haya elegido la pista y se haya comprobado que la publicación puede usarla.

Las variantes futuras pueden cambiar la situación —Wilfred hablando, una reunión incómoda, una caminata nocturna, una entrada triunfal o una reacción a otros personajes— sin cambiar la ancla visual de Elara ni convertir el audio en explicación narrativa. Cada variante debe registrar `Music_Variant_ID`, `Hook_Text`, `Situation_Type`, `Audio_Source` y `Hashtag_Set` por separado.

## 5. Casos propuestos

### Caso MPM-001 — Elara ignora a Wilfred

| Campo | Especificación |
|---|---|
| `Case_ID` | `MPM-001` |
| `Series_ID` | `ELARA-WALK-MUSIC-01` |
| `Music_Variant_ID` | `ELARA-WALK-MUSIC-01-V01` |
| `Audio_Source` | Biblioteca nativa de Facebook e Instagram; seleccionado al publicar. |
| `Music_Reference` | `Let It Happen — Tame Impala`, disponible en ambos catálogos nativos al momento de la publicación. No se imita ninguna melodía, letra, interpretación ni grabación. |
| `Music_Hashtag` | `#letithappen #tameimpala`, usados en el caption publicado. |
| `Visible_Music_Explanation` | `No` |
| `Family_Candidate` | `Music_walk_situational` |
| `Concept_ID` | Nuevo concepto; no asignar el concepto de Evan/Elara. |
| `Experiment_ID` | `EXP-202608-REEL-MOTION-POV-MEME-001` |
| `Hypothesis_ID` | `HB-REEL-MOTION-POV-MEME-01` |
| `Hook_Type` | `visual_situation_no_text` — Elara sigue en su mundo mientras Wilfred intenta hablarle. |
| `On_Screen_Text` | `None` — no colocar texto sobre la imagen ni identificar canción, artista o grupo. |
| `Caption_Treatment` | `caption_minimo` |
| `Caption_Function` | `reforzar_remate` |
| `Caption_Proposed` | `Ella no está disponible en este plano. 👀` — publicado por Fernando en Facebook e Instagram, junto con `#UniverseSentMe #ElaraUSM #letithappen #tameimpala`. |
| `Characters` | Elara + Wilfred |
| `Motion_Beat` | Elara camina hacia cámara o en plano lateral con los audífonos visibles; Wilfred la sigue detrás, mueve la boca y gesticula; ella nunca se vuelve ni revela qué audio está escuchando. |
| `Payoff` | Wilfred se queda un paso atrás y mira a cámara mientras Elara continúa caminando sin enterarse. |
| `Duration_Target` | 8–9 segundos |

La acción debe comunicar la broma incluso en silencio: los audífonos de Elara son la causa visible de la desconexión, no una explicación posterior. No incluir a Evan, camping, tienda de campaña ni elementos del Reel `CON-2026-08-09-Elara_Evan_Estrellas`. La música debe existir solo como pista de audio o referencia editorial externa; no debe convertirse en texto explicativo dentro del video.

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

El caso MPM-001 no depende de encontrar primero el ID histórico de la publicación de referencia para poder producirlo; cualquier ID histórico sirve únicamente para reconciliar evidencia y evitar atribuirle el asset de Evan. La pieza nueva debe recibir su propio `Concept_ID`, `Primary_Asset_ID`, `Experiment_ID` e ID nativo después de publicar.

## 7. Gate de aprobación

Fernando debe aprobar por separado: el hook `¿De cuánto te hablan…?`, la identidad visual de Elara y Wilfred, la ausencia de Evan, la capa musical sin explicación visible, la estructura del meme de Fantasma, la preservación de las gafas de Universe, los tres captions externos, la duración y la exclusión de afiliación. La aprobación de este brief no autoriza generación automática, programación ni publicación.

Después de generar, cada export pasa por revisión de identidad, legibilidad, movimiento, ausencia de watermark no registrado y comprensión sin audio. Después de publicar, el reporte diario registra primero identidad y engagement básico como `L1_Engagement_Observable`; cuando una fuente autorizada exponga views, reach o retención, se añade `L2_Discovery` o `L3_Video_Retention`. Las ventanas exactas de 24/72 horas son opcionales y solo se usan para un cierre contractual comparable. El protocolo completo está en `Operations/Research/2026-08-22_Reels_Metric_Instrumentation_Protocol.md`. No se declara `WIN` con un solo caso; el mínimo es n=3 y la decisión operativa requiere llegar a n=5.

## 8. Evaluación de calidad de las propuestas

| Caso | Relatable | Humor/emoción | Giro moderno | Voz de personaje | Share hook | Slot | Resultado |
|---|---:|---:|---:|---:|---:|---:|---|
| MPM-001 | 9 | 9 | 8 | 9 | 9 | 10 | **9.00/10 — PASS** |
| MPM-002 | 9 | 10 | 6 | 9 | 10 | 10 | **9.20/10 — PASS** |
| MPM-003 | 10 | 9 | 10 | 9 | 9 | 10 | **9.50/10 — PASS** |

Los puntajes fueron ejecutados con la rúbrica vigente de propuestas de Growth OS. En esta celda, `format_ok` representa que el Reel tiene movimiento real y no es un Reel de texto estático; el texto funciona como hook visual breve, no como sustituto de una escena.

## 9. Documentos que requieren sincronización

Al aprobarse este brief, deberán actualizarse el ledger de publicaciones de Reels, el staging de producción y la evaluación de la hipótesis. Hasta entonces, no se crea CNT, no se modifica el calendario y no se actualiza `ExperimentLog`.

La corrección de MPM-001 y la separación del asset de Evan/Elara quedan enlazadas con el registro maestro, la fuente maestra y la evaluación estructurada. La serie musical se documenta dentro de este brief y no requiere otro documento conceptual mientras esta celda permanezca en Review.

## 10. Paquete técnico de generación visual

El primer set de referencias fue descartado porque no coincidía con el estilo ni los diseños de personaje oficiales de `My Drive/Universe sent me/USM/Elementos`. Se consultaron directamente las carpetas oficiales de `PERSONAJES` y `LUGARES`, y se regeneró un set nuevo con ese material como fuente de verdad. MPM-003 también fue refinada a v2 para asegurar la visibilidad de las gafas. La ejecución debe seguir el orden: referencia primaria oficial → variaciones de encuadre → clip de video → revisión visual → edición exacta del texto → aprobación de export. Los binarios generados se guardan en paralelo en `My Drive/Universe sent me/USM/Reels/08 Agosto/EXP-202608-REEL-MOTION-POV-MEME-001`; GitHub conserva la fuente documental. MPM-001 ya fue cargado allí. Todavía no se ha creado CNT, modificado calendario ni publicado contenido.

### 10.1 Definiciones globales

| Dimensión | Especificación bloqueada |
|---|---|
| Subgénero | Fantasía cotidiana cinematográfica de Universe Sent Me; humor seco y reconocible, no fantasía épica solemne. |
| Rendering | Ilustración 2D digital pictórica, linework suave, textura de pincel, animación contenida pero con trayectoria física clara. |
| Color | Bosques y escenas exteriores en azul petróleo, verde profundo y violeta suave; acentos cálidos solo para separar sujetos. |
| Cámara | Vertical 9:16, composición móvil con primer plano legible y espacio seguro superior para texto añadido en post. |
| Duración | MPM-001: 8–9 s; MPM-002: 7–8 s; MPM-003: 8–10 s. |
| Audio | Sin diálogo ni narración necesarios. El chiste debe funcionar sin audio; si se añade ambiente, debe ser neutro y equivalente entre casos. |
| Texto | El texto exacto se añadirá en edición, no dentro de la imagen de referencia ni mediante texto generado por IA. Esto evita errores de letras y mantiene `Caption_Treatment` controlado. |
| Logo y watermark | Ninguno durante la generación. Si aparece un watermark no previsto, el export falla revisión. |
| Afiliación | Excluida. No incluir productos, enlaces, catálogos ni CTA comercial. |

### 10.2 Mapa de referencias de identidad

| Caso | Referencias permitidas | Uso | Exclusiones críticas |
|---|---|---|---|
| MPM-001 | `Official_Element_Refs/Elara.jpeg`, `Official_Element_Refs/Wilfred.png` y `Official_Element_Refs/Bosque_Ancestral_1.jpeg`, descargados de `Elementos/PERSONAJES` y `Elementos/LUGARES`. | Fijar diseño 2D, proporciones, sombrero, audífonos, cardigan, barba, túnica, bastón y bosque oficial. | No usar `Elara y Evan en el Bosque.mp4`; no incluir a Evan, camping, tienda, mochilas, fogata compartida ni escena de pareja. |
| MPM-002 | `Official_Element_Refs/Fantasma_Reference_Sheet.jpeg`, descargado de `Elementos/PERSONAJES/FANTASMA`; el estilo se alinea con `MPM-001_primary_reference_official_style_v2.png`. | Fijar sábana blanca con pliegues, lentes oscuros redondos con marco dorado, manos, botas y linework oficial. | No convertirlo en un fantasma de ojos negros; no reutilizar `Ghost_walks_cats_through_forest_202607240113.mp4` ni `...202607251436.mp4`; no repetir su recorrido ni encuadre. |
| MPM-003 | `Official_Element_Refs/Universe_Reference_Sheet.jpeg`, descargado de `Elementos/PERSONAJES/UNIVERSE`; el estilo se alinea con `MPM-001_primary_reference_official_style_v2.png`. | Fijar gato blanco peludo, orejas, gafas grandes redondas doradas ornamentadas, lentes oscuros y correas laterales. | Las gafas deben permanecer visibles; no sustituir a Universe por otro gato ni copiar la transformación de `FUT-TRANS-003`. Referencia generada válida: `MPM-003_primary_reference_official_style_v2.png`. |

Las referencias de My Drive se utilizarán como fuente de verdad de identidad y estilo. La composición, acción, fondo y recorrido se generarán de nuevo para que ningún caso sea un repost o una duplicación de asset. El registro de revisión visual está en `Generated_Reels/Motion_POV_Meme_001/reference_review_notes.md`. Las primeras referencias generadas quedan descartadas; las únicas válidas son `MPM-001_primary_reference_official_style_v2.png`, `MPM-002_primary_reference_official_style_v2.png` y `MPM-003_primary_reference_official_style_v2.png`.

### 10.3 Prompt de referencia primaria — MPM-001

```text
Create a vertical 9:16 primary visual reference for a short comedic fantasy Reel in the Universe Sent Me world. Use a 2D digital painterly illustration style with soft linework, subtle brush texture, cinematic depth, deep green and blue forest light, and readable character silhouettes. Elara is in the foreground, a petite young woman with light wavy hair, a pointed brown witch hat, a brown knitted cardigan, light top and visible white over-ear headphones. She walks calmly through a magical forest and looks straight ahead, completely absorbed in her headphones. Wilfred is behind her in the same frame, an elderly forest guardian gnome with a pointed red hat, long white beard and green tunic; he is visibly trying to speak to her while following her. Elara must not turn around. Keep the upper third and lower center visually clean for later editorial text. No Evan, no camping, no tent, no backpacks, no shared campfire, no props, no readable text, no logos, no watermarks, no labels, no annotations.
```

### 10.4 Prompt de referencia primaria — MPM-002

```text
Create a vertical 9:16 primary visual reference for a new Universe Sent Me comedic fantasy Reel. Use a 2D digital painterly illustration style, soft linework, deep violet moonlight and muted teal shadows. Show Fantasma as a mysterious ghostly character walking across a moonlit abandoned greenhouse walkway, with three expressive black cats following in a staggered line. This is a new location and new composition, not a recreation of a forest path. Fantasma is already moving at the front of the group; the cats are visibly closing the distance and subtly pulling the group in different directions. Make the physical walking direction immediately readable and leave clean space for text added later. No exact copied frame from any existing Reel, no readable text, no logos, no watermarks, no labels, no annotations.
```

### 10.5 Prompt de referencia primaria — MPM-003

```text
Create a vertical 9:16 primary visual reference for a short comedic fantasy Reel in the Universe Sent Me world. Use a 2D digital painterly style with soft linework, subtle brush texture, cinematic magical realism, cool blue corridor light and a warm violet portal glow. Universe is a white cat with clearly visible round glasses, holding a phone while walking toward a small glowing portal in a cosmic hallway. The cat must remain recognizable and the round glasses must be unobstructed. Show a clean, simple action path from the lower foreground toward the portal, with empty safe space at the top for later editorial text. No other characters, no readable text, no logos, no watermarks, no labels, no annotations.
```

## 11. Blueprints de video

Los tres clips deben generarse como piezas independientes de una sola toma continua, no como una conversación ni como una sucesión de imágenes estáticas. El texto será compuesto posteriormente con el mismo template editorial; el modelo de video debe priorizar movimiento corporal, dirección y reacción final.

### MPM-001 — Elara ignora a Wilfred

| Tiempo | Acción y encuadre | Texto añadido en edición |
|---|---|---|
| 0.0–1.2 s | Plano medio vertical. Elara ya camina en primer término; Wilfred entra detrás y abre la boca para hablar; los audífonos están visibles desde el primer cuadro. | Sin texto. |
| 1.2–5.8 s | Tracking lateral suave. Wilfred gesticula y acelera un poco; Elara mantiene el paso, la mirada al frente y los audífonos visibles, completamente absorbida por una canción no identificada. | Sin texto. |
| 5.8–8.5 s | Wilfred se detiene, mira a cámara con derrota; Elara sale parcialmente del encuadre sin haberse girado. | Sin texto; el remate vive en la acción, la música y el caption. |

**Video prompt in English:**

```text
Vertical 9:16 comedic fantasy scene in the established Universe Sent Me 2D painterly style. Elara is a petite young woman with light wavy hair, a pointed brown witch hat, brown knitted cardigan and clearly visible white over-ear headphones. Wilfred is an elderly forest guardian gnome with a pointed red hat, long white beard and green tunic. Elara starts walking calmly through a deep green magical forest in the foreground while Wilfred follows several steps behind her and visibly tries to talk with mouth movement and hand gestures. The camera performs a gentle lateral tracking movement that keeps both characters readable. Elara never turns her head, never makes eye contact and never reacts; the headphones remain visible throughout, and her behavior suggests she is fully absorbed in an unseen song. By the final beat Wilfred stops, looks directly at the camera with dry defeat, and Elara continues out of the frame. The forest, both characters, their clothing and the headphones exist continuously from the first frame to the last; no character pops in or disappears. Keep the upper third and both characters' faces clean; no text will be added to the image or in post. Do not generate readable text, lyrics, artist names or song titles. No dialogue, no narration, no logo, no watermark. Use only subtle neutral environmental ambience if audio is generated; the specific music track will be selected and mixed in post.
```

### MPM-002 — Fantasma y los gatos

| Tiempo | Acción y encuadre | Texto añadido en edición |
|---|---|---|
| 0.0–1.0 s | Plano frontal corto. Fantasma avanza por la pasarela del invernadero abandonado y los tres gatos aparecen detrás en cadena. | `No lo sigas` sobre Fantasma. |
| 1.0–5.5 s | Dolly backward. Cada gato cruza una marca del suelo y conserva el mismo tratamiento de texto, creando una cadena visual. | Repetir `No lo sigas` sobre cada gato al entrar. |
| 5.5–7.8 s | Fantasma intenta detenerse; los gatos siguen avanzando y él termina caminando detrás de ellos. | No añadir explicación. |

**Video prompt in English:**

```text
Vertical 9:16 comedic fantasy Reel in the established Universe Sent Me 2D painterly style. Fantasma walks forward on a moonlit abandoned greenhouse walkway, with three expressive black cats following in a visible staggered line. Use a gentle dolly backward so the group remains readable from the waist up and the walking direction is unmistakable. Fantasma begins confidently, then slows and tries to stop; the cats continue forward with independent small steps and pull the group toward the far end of the walkway. By the final beat Fantasma gives up and follows the cats, creating a clear visual reversal. Fantasma, all three cats, the greenhouse structure and the moonlit background exist continuously throughout the clip; no extra cats appear and none disappear. Leave the upper and mid-frame areas clean for identical text labels to be added in post above Fantasma and each cat. No readable generated text, no dialogue, no narration, no background music, no logo, no watermark.
```

### MPM-003 — Universe dijo “solo cinco minutos”

| Tiempo | Acción y encuadre | Texto añadido en edición |
|---|---|---|
| 0.0–1.2 s | Plano medio. Universe, gato blanco con gafas redondas visibles, camina con el teléfono hacia el portal. | `POV: Dijiste “solo cinco minutos”` |
| 1.2–7.0 s | Tracking backward. Universe cruza el umbral; la iluminación pasa suavemente de azul nocturno a amanecer mientras continúa caminando. | Mantener el hook. |
| 7.0–9.5 s | Sale del portal con la misma expresión; el fondo revela que pasó mucho más tiempo. Las gafas siguen visibles. | Sin explicación adicional. |

**Video prompt in English:**

```text
Vertical 9:16 comedic magical-realism Reel in the established Universe Sent Me 2D painterly style. Universe is a white cat with clearly visible round glasses and a phone in one paw. Universe walks steadily through a cool blue cosmic hallway toward a small violet glowing portal. The camera tracks backward smoothly while the cat crosses the threshold without stopping; the lighting gradually changes from deep night blue to pale sunrise gold as the background shifts from stars to dawn. Universe keeps the same mildly tired expression and continues walking as if only five minutes passed. In the final beat Universe exits the portal into a dawn-lit corridor, still wearing the same unobstructed round glasses, revealing that much more time has passed. Universe, the phone, the glasses, the portal and the corridor exist continuously; do not hide or replace the glasses and do not add other characters. Keep the upper third clean for text added in post. No readable generated text, no dialogue, no narration, no background music, no logo, no watermark.
```

## 12. Template de edición y medición

Para no introducir una variable oculta, los tres exports deben usar el mismo margen superior, familia tipográfica, tamaño aproximado, contraste, animación de entrada y duración del hook. En MPM-002 se repetirá literalmente la frase `No lo sigas` sobre Fantasma y cada gato, con el mismo estilo y solo desplazando la posición según el sujeto. El caption externo seguirá siendo `caption_minimo` con función `reforzar_remate`; no se copiará todo el texto sobreimpreso en el caption.

Antes de publicar, cada export debe pasar por cuatro controles: identidad de personajes, trayectoria de movimiento, legibilidad del hook sin audio y ausencia de watermark o producto. Después de publicar, se guardarán snapshots de 24 y 72 horas con la misma definición de views, reach, no seguidores, retención inicial, tiempo medio, completación, shares, comentarios, respuestas y seguidores ganados.

## 13. Plan de publicación manual de MPM-001

MPM-001 se recomienda como publicación primaria en **Facebook**, con una subida separada a **Instagram** si el mismo audio está disponible o puede incorporarse legalmente desde la biblioteca de la plataforma. La primera prueba no debe dispersarse simultáneamente en TikTok y YouTube: esos crossposts pueden ejecutarse después como publicaciones independientes, con sus propios IDs y métricas, pero no son necesarios para responder la pregunta inicial.

La ventana recomendada es **17:00–18:00 en `America/Matamoros`**, con 17:00 como punto central. La evidencia histórica considera 15:00 y 18:00 franjas prometedoras, pero no demuestra un horario ganador; por eso esta hora se trata como una elección operativa razonable y no como una conclusión causal. Si la subida ocurre fuera de esa ventana, debe conservarse la hora real y no modificarse después para aparentar equivalencia.

| Orden | Acción manual | Regla de control |
|---:|---|---|
| 1 | Subir a Facebook | Video vertical sin texto sobre la imagen; usar el export aprobado después de añadir el audio elegido. |
| 2 | Caption | `Ella no está disponible en este plano. 👀` exactamente; no agregar explicación de la canción. |
| 3 | Audio | Registrar pista/audio nativo, ID o nombre disponible, fuente y duración; no usar una imitación generada de una canción existente. |
| 4 | Hashtags | Para la primera prueba: ninguno, salvo que Fernando decida usar uno o dos hashtags que correspondan exactamente al audio elegido. |
| 5 | Instagram | Subir como publicación independiente, idealmente 10–20 minutos después, usando el mismo export y audio equivalente; registrar `IG_Media_ID` y permalink separados. |
| 6 | TikTok/YouTube | Posponer para no abrir variables adicionales en la primera lectura; si se ejecutan, tratarlos como crossposts independientes. |

### Afiliación

**No agregaría un producto de afiliado a MPM-001.** El objetivo de esta pieza es medir si la combinación de movimiento, situación visual y atmósfera musical funciona. Un producto nativo añadiría una variable comercial y podría cambiar el comportamiento de la audiencia, el caption, el audio o la intención de la publicación. Si se quiere monetizar otra pieza, debe seleccionarse fuera de esta celda y registrarse en el ledger de afiliados con su propio enlace, etiqueta, producto y snapshot; no debe entrar en el rendimiento de MPM-001.

### Medición posterior

Después de la subida manual, Fernando debe proporcionar o confirmar los IDs nativos. El corte diario registrará primero `L1_Engagement_Observable` y luego intentará `L2/L3` mediante Windsor o Instagram integrado. La fila debe conservar `Series_ID=ELARA-WALK-MUSIC-01`, `Music_Variant_ID=ELARA-WALK-MUSIC-01-V01`, `Audio_Source`, `Music_Reference`, `Music_Hashtag=None` si no se usa hashtag, `Published_At_Local`, `Export_SHA256`, `Platform_Content_ID` y permalink. Esta publicación no recibe un veredicto de éxito con un solo corte.

### 13.1 Estado de publicación confirmado — MPM-001

MPM-001 se publicó manualmente en Facebook e Instagram el 22 de agosto de 2026 con el caption `Ella no está disponible en este plano. 👀`, los hashtags `#UniverseSentMe #ElaraUSM #letithappen #tameimpala` y `Let It Happen — Tame Impala` elegido desde la biblioteca nativa en ambas plataformas. Los permalinks son [Facebook](https://www.facebook.com/share/r/1FF3rq76yg/) e [Instagram](https://www.instagram.com/reel/DcW-pUnxqGG/?igsi=eXU5YzF0cHkwNjFj). La publicación es `Crosspost_At_Launch`: se registrará como una unidad de celda con métricas estrictamente separadas por plataforma.

Las horas exactas, el Page Post/Reel ID de Facebook, el Instagram Media ID y los snapshots L1/L2/L3 siguen pendientes. No se añaden afiliación, pauta ni una inferencia de rendimiento por haber completado la publicación.

## 14. Gate siguiente

Las primeras referencias fueron rechazadas por no respetar el estilo de `Elementos`. Las tres referencias regeneradas con los archivos oficiales ya están disponibles: MPM-001, MPM-002 y MPM-003, esta última únicamente en su versión `official_style_v2`. MPM-001 completó su preflight y publicación; sus próximos datos son hora local, IDs y snapshots separados. MPM-002 permanece `Reference_Ready_Quota_Wait` y MPM-003 aún no se genera. Las referencias y el video generado de MPM-001 están cargados en [la carpeta operativa de Drive](https://drive.google.com/drive/folders/1NAyNNUnkNF5QGO7oYDgpw4b5poEPTuhX). La generación de referencias no equivale a aprobar los videos finales de los casos restantes. El siguiente gate de producción es esperar cuota y aprobación explícita para MPM-002; no se crean CNT, no se asignan slots, no se programa y no se publica MPM-002/003 hasta completar su revisión operativa.

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

## Historial de versiones

| Fecha | Versión | Cambio | Autor |
|---|---|---|---|
| 2026-08-22 | 1.7 | Se consolida MPM-001 como serie musical sin texto sobre la imagen y con caption mínimo. | Manus AI (CGO) |
| 2026-08-22 | 1.8 | MPM-001 pasa a publicado en Facebook e Instagram; se registran caption, hashtags, audio nativo y permalinks, con métricas por plataforma aún pendientes. | Manus AI (CGO) |
