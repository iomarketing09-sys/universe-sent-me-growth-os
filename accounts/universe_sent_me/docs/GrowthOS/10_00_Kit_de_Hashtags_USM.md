# Kit de Hashtags USM

**Propósito:** Sistema de hashtags de marca con firma `USM` para uso consistente en Facebook e Instagram. Reemplaza la elección ad-hoc de hashtags por un roster fijo y versionado, evitando errores de tipeo (ver caso "LoresUSM") y usos de nombres no aprobados en canon (ver caso "Maeve").
**Estado:** Active
**Fecha de creación:** 2026-08-03
**Última actualización:** 2026-08-15
**Versión:** 1.1
**Autor:** Claude (a solicitud de Fernando, 2026-08-03)
**Documentos relacionados:** `06_00_Reglas_Aprendizaje_Tendencias.md` (Sección 6), `Canon_Contradictions_Report.md`, `Integracion_Growth_OS.md`

---

## 1. Regla del formato

`[Nombre o Concepto]` + `USM`, en PascalCase, sin espacios ni guiones. Ejemplo: `KiriUSM`, `MomentosUSM`, `WilfredUSM`, `MemesUSM`.

**Regla de canon (no negociable):** un hashtag de personaje solo puede usar un nombre confirmado en la Biblia canónica. Antes de crear un hashtag de personaje nuevo, verificar en `Universe Sent Me - Biblia/02 Personajes/` o preguntar a Claude/Fernando. Nunca inventar un nombre para generar el hashtag — así se originó el caso "Maeve".

---

## 2. Roster — Hashtags de Personaje (confirmados en canon)

| Personaje | Hashtag | Estado del nombre |
|---|---|---|
| Universe | `#UniverseUSM` | Nombre propio, canon desde origen |
| Wilfred | `#WilfredUSM` | Nombre propio, canon desde origen |
| Elara | `#ElaraUSM` | Nombre propio, canon desde origen |
| El Ganso | `#GansoUSM` | Identificador estructural (sin nombre propio) |
| El Payaso | `#SilvioUSM` | Nombre propio confirmado 2026-08-03 (commit `8e9fe9a`), diseño corregido y aprobado |
| Maeve (Chica del Suéter) | `#MaeveUSM` | Nombre propio canonizado 2026-08-11 (commit `a994354`); Chica del Suéter es su alias visual/editorial |
| El Hada | `#KiriUSM` | Nombre propio confirmado 2026-08-03 (commit `f7bebca`) |
| El Fantasma | `#FantasmaUSM` | Identificador estructural (sin nombre propio todavía) |
| Evan | `#EvanUSM` | Nombre propio, canon desde origen |
| Kael (Chico de los Pantalones) | `#KaelUSM` | Nombre propio canonizado 2026-08-11 (commit `a994354`); Chico de los Pantalones es su alias visual/editorial |

*Pendiente: revisar únicamente los identificadores estructurales que todavía no tengan nombre propio confirmado; Kael y Maeve ya están correctamente asignados a sus alias visuales.*

---

## 3. Roster — Hashtags de Lugar

| Lugar | Hashtag |
|---|---|
| El Bosque (`@loc_USM_wilfred_camp`) | `#BosqueUSM` |
| La Plaza del Mercado | `#PlazaUSM` |
| Mar de Nubes | `#NubesUSM` |
| Jardines Eternos | `#JardinesUSM` |

---

## 4. Roster — Hashtags de Concepto / Formato

| Concepto | Hashtag | Uso |
|---|---|---|
| Contenido de marca general | `#UniverseSentMe` | Siempre incluido, es el hashtag raíz |
| Momentos/citas cortas | `#MomentosUSM` | Frases, quotes, contenido contemplativo |
| Memes/humor | `#MemesUSM` | Piezas de humor puro |
| Formato "¿Qué me llegó?" | `#QueMeLlegoUSM` | Reseñas de producto en formato Universe |
| Lore/worldbuilding | `#LoreUSM` | Contenido que profundiza el universo sin ser un chiste — **corrección del typo "LoresUSM"** |
| Mini-formato en validación | `#CuandoLeExplicas` | Hipótesis abierta (ver `06_00`, Sección 6) — no lleva `USM` porque nace del texto en pantalla, no del roster de marca |

---

## 5. Regla de combinación

Máximo 5-6 hashtags por pieza en Instagram (2 de personaje/lugar + 2-3 de concepto + `#UniverseSentMe`). En Facebook, el copy pesa más que los hashtags (ver `06_00`, Sección 6) — usar 2-3 como máximo, priorizando los de personaje sobre los de concepto.

---

## 6. Mantenimiento

Este roster se actualiza cuando:
- Fernando confirma un nombre propio nuevo para un personaje (como Kiri).
- Se aprueba un lugar o concepto nuevo en canon.
- Se detecta un typo o uso incorrecto ya publicado (documentar en `Canon_Contradictions_Report.md` y corregir aquí).

Manus no debe crear hashtags de personaje fuera de este roster sin antes verificarlo contra el canon.
