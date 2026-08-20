# Propuesta P02 — Movimiento inusual / Universe

**Propósito:** Proponer la segunda pieza controlada de `REAL → UNIVERSE / REACCIÓN`, cambiando la situación humana de P01 por compra impulsiva y preservando a Universe como anchor character, el payoff silencioso y la transformación real → mundo USM.

**Estado:** Archived — no aprobada por Fernando; la similitud percibida con P01 impide llevarla a storyboard o generación.

**Fecha de creación:** 2026-08-20

**Última actualización:** 2026-08-20

**Versión:** 1.1

**Autor:** Manus AI (CGO)

**Documentos relacionados:** `2026-08-19_Diseno_Experimento_Reels_v2.md`, `2026-08-19_Brief_Pieza01_DobleCheck_Universe_Flow.md`, `../Research/2026-08-19_Auditoria_Reels_Fernando_GPT.md`, `../../GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md`, `../../GrowthOS/07_00_Registro_Maestro_Reels.md`

---

## Identificadores propuestos

| Campo | Valor |
|---|---|
| Concept_ID | `CON-2026-08-20-MovimientoInusual-Universe` |
| Campaign_Label | `REAL → UNIVERSE / REACCIÓN` |
| Experiment_ID | `EXP-202608-REALUNIVERSE-01` |
| Hypothesis_ID | `HB-REEL-01` |
| Personaje ancla | Universe: gato blanco pequeño, gafas redondas doradas finas; nunca humano. |
| Estado | `DRAFT_NOT_AUTHORIZED` |

## Decisión editorial — 2026-08-20

Fernando rechazó esta propuesta antes de producción por sentirse demasiado cercana a P01: conserva teléfono, culpa posterior, transición violeta y la misma estructura de reacción seca. No se generaron keyframes, clips ni assets; por tanto, no hubo gasto de créditos ni publicación.

La siguiente exploración se mueve a una familia independiente de **videoclip musical / microhistoria emocional**, inspirada en el atractivo observado de Fantasma caminando con gatos y de Elara + Evan en el bosque. Esta familia no se compara directamente contra `EXP-202608-REALUNIVERSE-01` hasta que se defina su hipótesis propia, canción autorizada y relación canónica de sus personajes.

## Variable que cambia y controles que se preservan

P02 no busca declarar una ganadora frente a P01. Es el segundo caso de la misma familia. La situación cambia de ansiedad posterior a un mensaje a **culpa cómica posterior a una compra impulsiva**. El resto debe conservar la misma gramática visual.

| Elemento | P01 | P02 propuesto | Decisión de control |
|---|---|---|---|
| Situación humana | “No pasa nada” después de enviar un mensaje. | Revisar una alerta de gasto después de decir “solo iba a ver”. | **Variable cambiada.** |
| Personaje | Universe. | Universe. | Constante. |
| Arco | Real → portal → reacción seca de Universe. | Real → portal → reacción seca de Universe. | Constante. |
| Texto | Una línea contextual al inicio. | Una línea contextual al inicio. | Constante de formato; cambia la situación. |
| Comprensión sin audio | Obligatoria. | Obligatoria. | Constante. |
| Duración de comparación | P01 final se publicó en ~12 s. | Objetivo: **11–12 s**, no los 6–7 s inicialmente planeados. | Igualar el render publicado de P01 evita introducir duración como una segunda diferencia. |

## Idea narrativa

> **Texto en pantalla:** `yo después de decir “solo iba a ver”`

Una mano sostiene un teléfono sobre un escritorio real. Aparece una alerta genérica y no identificable de gasto: **“movimiento inusual”**. La mano se queda inmóvil. La tarjeta/alerta se pliega hacia una luz violeta que llena el cuadro. En Nubealis, Universe está sentado a la derecha de un pequeño montón de paquetes sin marca; intenta empujar discretamente una caja fuera del plano. Un paquete diminuto cae desde arriba. Universe mira de reojo a cámara, cubre el teléfono con una pata y hace el gesto seco de que esto nunca ocurrió.

La gracia no es “Universe compra cosas”; es reconocer el reflejo humano de minimizar una compra que claramente ya dejó evidencia. La última caja que cae da un segundo golpe visual sin necesitar diálogo.

## Estructura de edición propuesta

| Tiempo objetivo | Imagen | Función |
|---|---|---|
| 0.0–1.8 s | Escritorio real, teléfono y alerta genérica de “movimiento inusual”. Texto contextual visible. | Hook humano legible. |
| 1.8–3.4 s | La alerta se pliega/abre como luz violeta; el escritorio sigue físicamente presente durante la transición. | Transformación. |
| 3.4–8.8 s | Universe frente a paquetes neutros, intenta ocultar uno y cubre el teléfono. | Payoff principal. |
| 8.8–11.5 s | Cae un paquete pequeño; side-eye de Universe y corte. | Remate y compartibilidad. |

**Audio:** SFX de alerta breve, whoosh de portal y golpe suave de caja. La pieza debe aprobarse primero en mute. `Prayer Instrumental` solo se prueba después, a volumen bajo, y no se incorpora durante la generación.

## Producción propuesta en Flow

| Bloque | Modelo | Referencia | Objetivo | Estimación de coste |
|---|---|---|---|---:|
| Clip 1 — alerta → portal | Omniflash | Keyframe inicial de escritorio/teléfono. | Hook y transformación sin bloquear un estado final rígido. | 7 puntos |
| Clip 2 — portal → Universe con paquetes | Veo Lite | Frame final de Clip 1 + KF-B de Universe/pedidos. | Bloquear el aterrizaje con personaje, composición, cajas y luz consistentes. | 10 puntos |
| Clip 3 — intento de ocultar / caja cae | Veo Lite | KF-B + KF-C de payoff. | Bloquear inicio, gesto de pata y frame final del side-eye. | 10 puntos |
| **Total estimado** |  |  | Sin contar iteraciones justificadas. | **27 puntos** |

No se genera nada hasta revisar los tres keyframes por separado. Omniflash se usa solo donde el final no necesita ser un frame predeterminado; Veo Lite se reserva para continuidad obligatoria de inicio/final.

## Copy de publicación propuesto

```text
el movimiento inusual era yo 🟣

#UniverseSentMe #UniverseUSM #MemesUSM #CuandoLeExplicas
```

La versión de Facebook puede añadir producto afiliado **solo si** el artículo se integra orgánicamente con los paquetes y se crea un link/tag nuevo por publicación. La pieza no debe convertir el producto en explicación del chiste ni duplicar el enlace de P01.

## Evaluación de propuesta

La rúbrica se ejecutó el 2026-08-20 con `score_proposal.py`; el resultado fue `PASS`.

| Criterio | Puntuación | Peso | Razón |
|---|---:|---:|---|
| Relatable | 9.4/10 | 30% | “Solo iba a ver” y una alerta de gasto son un reconocimiento inmediato. |
| Humor / emoción | 9.0/10 | 25% | La negación y la evidencia física de los paquetes construyen un remate seco. |
| Share hook | 9.0/10 | 15% | Invita a etiquetar a quien compra “solo para ver”. |
| Giro moderno | 9.0/10 | 10% | App/notificación cotidiana dentro de portal y Nubealis. |
| Voz de personaje | 9.2/10 | 10% | Universe reacciona y se delata; no es omnisciente ni sermonea. |
| Slot | 10.0/10 | 5% | Recomendado: 19:00–21:00 CDT; conservar mismo horario de comparación si P01 ofrece ese dato. |
| Formato válido | Sí | 3% | Reel visual, no Reel de frase filosófica. |
| Canon seguro | Sí | 2% | Sin moralización ni transformación humana. |
| **Resultado total** | **9.24/10** |  | **PASS; supera el mínimo 8.5.** |

## Criterios de aprobación

P02 pasa a storyboard solamente si Fernando aprueba: la situación, el texto en pantalla, el segundo remate de la caja y el uso de 27 puntos estimados. Si se aprueba, el siguiente entregable es una lista de referencias visuales para generar KF-A, KF-B y KF-C; no un video directo.
