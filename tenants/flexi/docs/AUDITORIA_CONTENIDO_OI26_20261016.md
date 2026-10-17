# Auditoría de Contenido Campaña OI26 — Flexi + Quirelli

**Tenant:** flexi · **Marca:** Flexi (+ rama Flexi Country) y sub-marca Quirelli
**Fecha:** 2026-10-16
**Método:** revisión **solo de nombres de archivo** (sin abrir ni copiar imágenes)
**Fuente:** `/home/universe-sent-me/GoogleDrive/Informes FLEXI/marketing/`
**Cruce contra:** `tenants/flexi/data/catalogo_flexi_confirmado.csv` (54 modelos / 75 variantes)

---

## 1. Cobertura auditada

| Carpeta | Archivos | Modelos distintos | Modelos del catálogo |
|---|---|---|---|
| Flexi / `Campaña OI26/FOTOS OI26 FINALES/PORTADILLAS FLEXI OI26` | 36 | 32 | 4 |
| Flexi / `Campaña Country OI26/- PORTADILLAS OI26` | 118 ( +176 `Copia de` ) | 20 | 2 |
| Quirelli / `Campaña OI26/Campaña` | 158 | 20 | 1 |
| Quirelli / `Campaña OI26/Essencial` | 54 | 24 | 0 |
| Flexi / `Campaña OI26/FOTOS OI26 FINALES` (fotos producto, nivel top) | 198 | 55 | 4 |

**Total archivos auditados por nombre:** 564 (366 en las 4 carpetas + 198 fotos producto).
**Códigos de modelo distintos en toda la campaña:** ~96.

> No se auditó el contenido del `PORTADILLAS_QUIRELLI_OI26.zip` (356 MB).

---

## 2. Resultado del cruce: 7 de 54 modelos del catálogo tienen asset OI26

| Modelo | Marca | Colores catálogo (checklist) | Color en nombre | Coincide |
|---|---|---|---|---|
| 142801 | Flexi | Beige, Negro | BEIGE, TAN | ✅ Beige |
| 142901 | Flexi | Negro, Oro | TAN | ❌ |
| 143001 | Flexi | Negro, Oro, Plata | PLATA | ✅ |
| 143201 | Flexi | Negro | NEGRO | ✅ |
| 66517 | Flexi | Marrón, Negro | NEGRO | ✅ |
| 66525 | Flexi | Chocolate | CHOCOLATE, NEGRO | ✅ Chocolate |
| 306703 | Quirelli | Negro, Nude | NEGRO, NUDE | ✅ ambos |

**Cobertura por marca:** Flexi 6/45 · Quirelli 1/9.

---

## 3. Modelos del catálogo SIN asset OI26 (47)

`101905, 101908, 101912, 117207, 127202, 134806, 136804, 137002, 139601, 140601, 142303, 304402, 305101, 401001, 402112, 403019, 404801, 406401, 406412, 407801, 414404, 417606, 418502, 419501, 419502, 421501, 421503, 422906, 423101, 423201, 423803, 424202, 424601, 48301, 48303, 50816, 5807, 59305, 63201, 63202, 66514, 700803, 700804, 707205, 707902, 88701, 88702`

Acción: fotografiar / solicitar a la marca / reusar de otras fuentes.

---

## 4. Hallazgos

1. La campaña OI26 cubre ~96 modelos, pero **solo 7 pertenecen al catálogo confirmado de la sucursal**.
2. **47/54 confirmados quedan sin foto** de esta campaña → gap principal.
3. Diferencias de color entre nombres y catálogo (p. ej. `142901` TAN vs catálogo Oro/Negro) — los nombres no son autoritativos; el catálogo conserva los colores del checklist.
4. `Flexi Country` es una **rama de Flexi** (mismos criterios de marca; códigos propios).
5. Duplicados físicos: 176 archivos `Copia de …` en Country.

---

## 5. Caveats

- Cruce **por nombre**; la llave fue el código de modelo (`\d{4,6}`).
- Colores de nombre normalizados solo para el cruce (`tenants/flexi/data/color_normalization_map.json`), no para el catálogo.
- No se leyó contenido ni metadatos de las imágenes.

---

*Generado por Growth CGO Agent · método solo-nombres · ver `color_normalization_map.json`*
