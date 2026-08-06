# CNT-003 Video Prompts for Flow (Clip-by-Clip)

**Propósito:** Prompts de generación de video en Flow para el CNT-003 Trailer 001. Cada clip usa la imagen generada como primer keyframe y añade el movimiento/acción necesario.
**Estado:** Draft
**Fecha de creación:** 2026-08-06
**Última actualización:** 2026-08-06
**Versión:** 1.0
**Autor:** Manus AI (CGO)
**Documentos relacionados:** `CNT003_Trailer001_Clip_Plan.md`, `CNT003_Trailer001_Image_Prompts.md`

---

## Instrucciones generales para Flow

- Cada clip usa la imagen correspondiente como **first keyframe** (imagen de referencia en Flow).
- El prompt de video describe SOLO el movimiento/acción que debe ocurrir DESDE esa imagen.
- No describir estilo ni apariencia — la imagen de referencia ya lo hace.
- Formato: acción del sujeto + movimiento de cámara + elementos en movimiento.

---

## Clip 1 — Mar de Nubes (5s)
**Imagen de referencia:** `1 - Floating_islands_above_clouds`

```
Camera slowly pushes forward toward the central floating island. Clouds drift and roll gently below. Small clouds pass in foreground. The island grows larger as camera advances. Sky lightens slightly.
```

---

## Clip 2 — El Bosque Día (5s)
**Imagen de referencia:** (NOTA: No hay imagen separada de bosque día — usar imagen 4 como base y pedir escena de día, O pedirle a Flow que genere un bosque día separado antes)

```
Camera moves forward along the path between the trees. Leaves rustle gently. Sunlight shifts through the canopy. Small particles float in the air. Distant castle grows slightly larger.
```

**NOTA IMPORTANTE:** La imagen 4 que generaste es de Wilfred en bosque nocturno cósmico. Para el Clip 2 (bosque día), necesitas una imagen de referencia separada de un bosque en día. Puedes generarla con este prompt corto en Remix of Grid:

```
Ancient forest path leading to stone archway. Green trees, golden sunlight, god-rays, fireflies. Day scene.
```

Si no la generas, puedes reemplazar el Clip 2 usando directamente la imagen 4 y cambiar el plan a: empezar con Mar de Nubes → Wilfred en bosque cósmico → personajes → clímax → outro. (Ver alternativa abajo)

---

## Clip 3 — Universe Gato (4s)
**Imagen de referencia:** `3 - Cat_sitting_in_cozy_space`

```
Cat sits still with subtle breathing. The small flame beside it flickers and dances. Warm light pulses softly. Tiny sparks float upward. Gentle shimmer in the air.
```

---

## Clip 4 — Wilfred Caminando (5s)
**Imagen de referencia:** `4 - Wilfred_walking_through_forest`

```
Camera slowly zooms in toward Wilfred. His staff's flame tip glows brighter and dims rhythmically. Mushrooms at the base emit faint blue glow. Fireflies drift upward slowly. Stars in the sky twinkle.
```

---

## Clip 5 — Elara (Fuego) (4s)
**Imagen de referencia:** `5 - Elara_sitting_by_campfire`

```
Fire crackles and flickers. Sparks rise from the flames and drift upward into the dark sky. Firelight shifts subtly across her face and clothing. Embers float around her. Wind gently moves her hair.
```

---

## Clip 6 — Kiri Hada (4s)
**Imagen de referencia:** `6 - Kiri_hovering_with_glowing_wings`

```
Fairy drifts slowly upward in a gentle undulating motion. Her wings pulse with soft glow. Golden particles swirl around her. Flower petals float past her. Light trails follow her movement.
```

---

## Clip 7 — Silvio Payaso (3s)
**Imagen de referencia:** `7 - Man_sitting_at_table`

```
Candle flame flickers gently on the table. Silvio remains still, relaxed pose. Subtle warm bokeh lights in background shift and shimmer. A faint breath of smoke rises from the candle.
```

---

## Clip 8 — Fantasma con Gatos (5s)
**Imagen de referencia:** `8 - Fantasma_levitating_above_woods`

```
Fantasma levitates perfectly still. One black cat slowly turns its head to look at camera. Another cat takes a slow step. Small campfire on ground flickers. Mist drifts between trees. Stars twinkle above.
```

---

## Clip 9 — Portal Cósmico (4s)
**Imagen de referencia:** `9 - White-gold_light_explodes_nebula`

```
The central light explodes outward rapidly. Purple-pink clouds swirl faster and expand. Energy streaks radiate in all directions. Floating rocks drift outward. The light grows to fill the entire frame. Shockwave pushes clouds apart.
```

---

## Clip 10 — Bosque Cósmico (5s)
**Imagen de referencia:** `10 - Magical_forest_at_night`

```
Camera slowly pulls back, revealing more of the cosmic sky above. Wilfred stands still. Campfire crackles, sparks rise toward the stars. Nebula in the sky swirls slowly. Fireflies glow at ground level. Moon light shifts subtly.
```

---

## Clip 11 — Outro (4s)
**Imagen de referencia:** `11 - Text__Universe_Sent_Me__emerges`

```
The warm golden glow pulses gently like a heartbeat. Light breathes — expands slightly then contracts. Fireflies float lazily. The text remains steady, illuminated. The archway and trees remain still. A single particle drifts across the frame at the end.
```

---

## Alternativa: Plan Reducido (10 clips, sin bosque día separado)

Si no generas una imagen separada de bosque día, puedes usar esta estructura de 10 clips:

| # | Imagen Referencia | Prompt Video |
| :--- | :--- | :--- |
| 1 | Mar de Nubes | Camera pushes forward toward island. Clouds roll. |
| 2 | Wilfred (img 4) | Camera zooms in. Staff glows. Fireflies. Stars twinkle. |
| 3 | Universe Gato | Cat sits. Flame flickers. Sparks float. |
| 4 | Elara | Fire crackles. Sparks rise. Wind moves hair. |
| 5 | Kiri | Fairy drifts. Wings pulse. Particles swirl. |
| 6 | Silvio | Candle flickers. Bokeh shifts. Smoke rises. |
| 7 | Fantasma + gatos | Fantasma still. Cat turns head. Fire flickers. Mist drifts. |
| 8 | Portal | Light explodes outward. Clouds swirl. Energy radiates. |
| 9 | Bosque Cósmico | Camera pulls back. Fire crackles. Nebula swirls. |
| 10 | Outro | Glow pulses. Text steady. Fireflies float. |

**Duración total:** ~38-40 segundos.
