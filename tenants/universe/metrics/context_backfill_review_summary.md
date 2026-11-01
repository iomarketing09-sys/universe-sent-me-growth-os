# Revisión de contexto/serie — 67 publicaciones

- Total: **67**
- Con asset identificado por huella visual: **36**
- Sin asset exacto, resueltas por revisión visual: **31**
- Marcadas para revisar: **9**

## Resultado aplicado

- `publication_contexts.json`: **339** entradas totales, **67** nuevas.
- `signals.csv`: **180** filas de señal actualizadas.
- Reclasificados: **#10 y #24 → Chipitillo** (gato negro).
- Assets renombrados y actualizados: **#04, #11, #35, #47 y #52**.
- `latest_posts_without_series`: **0**.
- Pruebas focalizadas: `14 passed` (`tests/test_monetization.py`).

## Distribución propuesta

- Universe: 15
- Evan: 10
- Existencial: 8
- Wilfred: 8
- Maeve: 4
- Kiri: 3
- Elara: 2
- Evan+Elara: 2
- Fantasma: 2
- Silvio: 2
- Wilfred+Elara: 2
- Chipitillo: 3
- Elara+Evan: 1
- Elara+Fantasma: 1
- Elara+Universe: 1
- Kiri+Evan: 1
- Maeve+Evan: 1
- Universe+Silvio: 1

## Casos marcados para revisar

- #16 `1036844829507460_122173560681072582` → **Elara** — Elara + vampiro generico; hashtag solo Elara.
- #21 `1036844829507460_122168790159072582` → **Universe** — Mujer generica con gatos blancos tipo Universe; confirmar si cuenta como Universe.
- #22 `1036844829507460_122179351905072582` → **Existencial** — Pareja no identificada; asset nombrado Existencial.
- #28 `1036844829507460_122179127565072582` → **Chipitillo** — Identidad confirmada por cliente; pendiente agregar a la Biblia.
- #29 `1036844829507460_122179338015072582` → **Existencial** — Mujer en cama; asset Existencial, personaje no canon claro.
- #36 `1036844829507460_122173615281072582` → **Existencial** — Dos figuras genericas; asset sin personaje.
- #55 `1036844829507460_122179477797072582` → **Evan** — Evan + acompanante no identificado; se deja primario Evan.
- #58 `1036844829507460_122173087557072582` → **Evan** — 2610054 sigue apareciendo como “sin personaje” en Drive; confirmar renombrado.
- #59 `1036844829507460_122173110633072582` → **Maeve** — Sin `asset_ref` verificable; 260716 ahora corresponde a Kiri+Evan; confirmar asset correcto.

## Notas de criterio

- Se usa el personaje como `serie`, igual que `_derive_series()` en `modules/intelligence/monetization.py`.
- `Existencial` agrupa piezas sin personaje canon: quote cards, objetos, paisajes y memes genericos.
- Los assets viejos (`260xxx`, `2609xxx`) no siempre traen personaje en el nombre; en esos casos manda la revisión visual contra `USM/Elementos`.
- `Chipitillo` queda confirmado por el cliente como el gato negro; todavía no está en la Biblia y queda pendiente incorporarlo.
- No se movieron ni copiaron assets de Drive; solo se usaron nombres/rutas y revisión visual temporal.
