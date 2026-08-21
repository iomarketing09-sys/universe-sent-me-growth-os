---
title: "Prompts de producción — assets comparables aprobados"
purpose: "Definir la composición, el texto visual, el caption propuesto y las restricciones de los cuatro assets autorizados para generación exclusiva."
status: Active
created: 2026-08-21
updated: 2026-08-21
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-21_Autorizacion_Generacion_Briefs_Comparables.csv"
  - "Operations/Research/2026-08-21_Paquete_Revision_Humana_Briefs_Comparables.md"
  - "Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md"
  - "Operations/Production/2026-08-21_Generated_Comparable_Assets.csv"
  - "Operations/Production/2026-08-21_Comparable_Identity_V2_Proposals.csv"
  - "Operations/Production/2026-08-21_Control_Visual_Assets_Comparables.md"
  - "GrowthOS/Integracion_Growth_OS.md"
organization: "Operations/Production"
---

# Prompts de producción — assets comparables aprobados

## Alcance común

La autorización de Fernando cubre únicamente la generación de un asset nuevo por brief. Los cuatro resultados son experimentales y no deben entrar en calendario, CNT, reuse, afiliados o publicación sin una decisión humana posterior. Los textos visuales deben estar en español y ser legibles; no añadir marcas de agua, logotipos, productos ni personajes canónicos salvo `Universe` en `FUT-TRANS-003`.

## `FUT-MICRO-005` — `HB-006`

**Archivo propuesto:** `FUT-MICRO-005_HB-006_Microhistoria_Romantico_Absurd_3P.png`
**Caption propuesto:** `El amor también tiene presupuesto. 🤭`
**Tratamiento:** `caption_minimo`; función `reaccion`.

**Prompt:**

> Create a polished Spanish-language social meme image for Universe Sent Me, with exactly three equal-width comic panels in one horizontal composition. Use two entirely generic non-canonical characters, a warm cream and muted lavender palette, clean expressive 2D editorial cartoon style, simple readable backgrounds, and crisp black Spanish speech bubbles. Panel 1: Character A asks “¿Me quieres?” and Character B answers “Claro.” Panel 2: Character A asks “¿Mucho?” and Character B answers “Lo suficiente para no compartir mi postre.” Panel 3: Character A says “Eso no es amor.” and Character B replies “Es amor con límites presupuestarios.” The third panel must clearly reframe the romantic expectation into an absurd practical joke. Render the Spanish text exactly, with no extra text. Exactly three panels, no fourth panel, no canonical Universe Sent Me character, no coercion, no humiliation, no explicit sexuality, no protected-trait attack, no watermark, no logo.

**Criterio de aceptación:** exactamente tres paneles; turnos claros; tercer panel cambia la lectura; personajes genéricos; texto visual legible; sin contenido excluido.

## `FUT-MICRO-006` — `HB-007`

**Archivo propuesto:** `FUT-MICRO-006_HB-007_Microhistoria_Cotidiana_3P.png`
**Caption propuesto:** `La logística también tiene enemigos. 😭`
**Tratamiento:** `caption_refuerzo`; función `refuerzo_semantico`.

**Prompt:**

> Create a polished Spanish-language social meme image for Universe Sent Me, with exactly three equal-width comic panels in one horizontal composition. Use two entirely generic non-canonical characters, a soft blue and mustard palette, clean expressive 2D editorial cartoon style, and simple everyday locations. Panel 1: Character A asks “¿Por qué llegaste tarde?” and Character B answers “Porque salí temprano.” Panel 2: Character A says “Eso no tiene sentido.” and Character B answers “Yo también lo pensé.” Panel 3: Character A asks “Entonces, ¿qué pasó?” and Character B replies “El trayecto se quedó con la responsabilidad.” The third panel must reveal a social reframe rather than a romantic conflict or a moral lesson. Render the Spanish text exactly, with no extra text. Exactly three panels, no single-scene composition, no canonical character, no romantic repetition, no coercion, no anxiety escalation, no protected-trait attack, no watermark, no logo.

**Criterio de aceptación:** exactamente tres paneles; conflicto cotidiano no romántico; tercer panel autosuficiente; caption de refuerzo no explica literalmente los globos.

## `FUT-TRANS-003` — `HB-008`

**Archivo propuesto:** `FUT-TRANS-003_HB-008_Transformacion_Universe.png`
**Caption propuesto:** `¿En qué momento cambió todo? 👀`
**Tratamiento:** `caption_conversacional`; función `pregunta_abierta`.

**Prompt:**

> Create a polished Spanish-language before-and-after social meme image for Universe Sent Me. Show the exact same cat character, Universe, in two clearly separated vertical states labeled “ANTES” and “DESPUÉS”. Universe is a recognizable dark-and-white cat wearing the same round glasses in both states; the glasses must be fully visible and identical in shape, color, and position. Use one dominant transformation only: the same tired, slouched Universe becomes energized and upright with a bright cosmic aura, while preserving the same feline face, glasses, silhouette, and core identity. Keep the background simple and related between both states so the transformation, not the background, explains the contrast. Clean expressive 2D editorial cartoon style, deep navy, warm cream, and restrained gold accents. Render only the exact labels “ANTES” and “DESPUÉS”; no speech bubbles, no extra text, no product, no affiliate reference, no character substitution, no clothing-only change, no multiple simultaneous transformations, no watermark, no logo.

**Criterio de aceptación:** mismo Universe en ambos estados; gafas visibles en ambos; marcadores felinos preservados; una sola transformación dominante; labels legibles; sin producto.

## `FUT-ACID-003` — `HB-009`

**Archivo propuesto:** `FUT-ACID-003_HB-009_Dialogo_Acido_Situacional.png`
**Caption propuesto:** `La contradicción se presentó sola. 😌`
**Tratamiento:** `caption_minimo`; función `reaccion`.

**Prompt:**

> Create a polished Spanish-language social meme image for Universe Sent Me using one clean comic panel with two generic non-canonical characters and two clearly distinguishable voices. Use a dry, expressive 2D editorial cartoon style, muted green and warm orange palette, and a simple everyday setting. Character A says “Dijiste que ibas a cambiar.” Character B replies “Cambié de opinión.” Character A delivers the final remate: “Eso explica demasiado.” Make the interpersonal target a harmless contradiction or habit, not a protected trait. The exchange must be readable in one glance, with distinct speech-bubble placement and expressions. Render the Spanish text exactly, with no extra text. No coercion, no threats, no humiliation, no sexual dominance, no protected-trait attack, no generic no-remate exchange, no watermark, no logo.

**Criterio de aceptación:** dos voces visualmente distinguibles; objetivo situacional; remate claro; `Safety_Flag=No_coercion`; caption mínimo sin explicar el chiste.

## Assets generados

Los cuatro prompts autorizados produjeron cuatro PNG en `Operations/Production/Generated_Comparable_Assets/`. Sus paths, controles y bloqueos operativos están registrados en `Operations/Production/2026-08-21_Generated_Comparable_Assets.csv`.

## Segunda propuesta de identidad visual

A petición de Fernando, se generaron variantes v2 de `FUT-MICRO-005`, `FUT-MICRO-006` y `FUT-ACID-003` usando personajes con anclas visuales estables. Elara conserva el sombrero puntiagudo y cabello claro; Evan conserva el suéter café; Universe conserva sus lentes redondos. Las variantes v2 preservan la composición y el texto de sus briefs originales, pero la nueva referencia de Evan muestra que su fidelidad facial y actitudinal es todavía parcial. Quedan registradas como `Proposal_Review_Identity_Partial` y no reemplazan automáticamente los primeros assets. Si se requiere fidelidad alta, debe hacerse una tercera iteración usando la referencia ampliada de Evan.

| Brief | Personajes v2 | Archivo | Estado |
|---|---|---|---|
| `FUT-MICRO-005` | Elara + Evan | `FUT-MICRO-005_HB-006_Microhistoria_Romantico_Absurd_3P_v2.png` | `Identity_Partial` |
| `FUT-MICRO-006` | Elara + Evan | `FUT-MICRO-006_HB-007_Microhistoria_Cotidiana_3P_v2.png` | `Identity_Partial` |
| `FUT-ACID-003` | Universe + Evan | `FUT-ACID-003_HB-009_Dialogo_Acido_Situacional_v2.png` | `Identity_Partial` |

## Post-generación

Cada archivo debe conservar su `Brief_ID`, `Experiment_ID`, `Hypothesis_ID` y `Cell_ID` en el ledger de producción. El control visual debe marcar `Pass`, `Revise` o `Reject` antes de cualquier uso operativo. Una imagen aprobada visualmente todavía requiere una decisión humana independiente para calendario, CNT, reuse, afiliados o publicación.
