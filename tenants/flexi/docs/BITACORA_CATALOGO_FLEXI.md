# Bitácora — Proyecto Catálogo Flexi

**Propósito:** registro vivo para no perder contexto entre sesiones (algunos análisis visuales previos tumbaron la sesión). Actualizar al final de cada sesión de trabajo.
**Tenant:** `flexi` (`physical_cro`, sin canon) · **Última actualización:** 2026-10-16

---

## Estado actual (resumen)

| Artefacto | Ruta | Estado |
|---|---|---|
| Catálogo confirmado (único CSV) | `data/catalogo_flexi_confirmado.csv` | ✅ 54 modelos / 75 variantes |
| Mapa de normalización de colores | `data/color_normalization_map.json` | ✅ |
| Auditoría de contenido OI26 (por nombres) | `docs/AUDITORIA_CONTENIDO_OI26_20261016.md` | ✅ |
| Checklist original del cliente | `docs/CATALOGO_FLEXI_CLIENTE_CHECKLIST_20261014.md` | 🔒 intacto (evidencia) |

---

## Decisiones tomadas (con el cliente)

1. **Fuente de verdad del catálogo** = checklist firmado por la sucursal (`..._CHECKLIST_20261014.md`).
2. **Un solo archivo CSV**, solo lo confirmado.
3. **Se descartan** los 4 modelos `N/H`: `143302, 401301, 68714, 98304`.
4. **Se descartan** los 9 modelos del catálogo previo no confirmados: `104523, 300801, 300808, 303302, 304202, 304401, 304704, 35802, 35902`.
5. **Flexi Country = rama de Flexi** (no es 3ª marca).
6. **Los colores del catálogo son los del checklist** (no se adoptan colores vistos en nombres de imagen).

---

## Trabajo realizado

### 2026-10-16
- Integrado el inventario confirmado → `data/catalogo_flexi_confirmado.csv` (54 modelos / 75 variantes; 45 Flexi + 9 Quirelli).
- Normalizados sinónimos de color: `Black→Negro`, `White→Blanco`, `Oro rosa→Oro rosado`, marca `Flexi`/`Quirelli`.
- Creado `data/color_normalization_map.json`.
- Auditoría de campaña OI26 **solo por nombres** (sin abrir imágenes) de 4 carpetas + 198 fotos producto → `docs/AUDITORIA_CONTENIDO_OI26_20261016.md`.
  - **Resultado:** 7 de 54 modelos con asset OI26; **47 sin foto**.
- Entrada añadida al changelog central: `GrowthOS/00_01_Changelog_GrowthOS.md` [5.98.00].

---

## Pendientes

### P1 — Carpeta con nombres perdidos (BLOQUEADO por riesgo de sesión)
- Ruta: `.../Informes FLEXI/Catálogo disponibles/Productos /`
  - Subcarpeta `Flexii` → 33 imágenes `IMG-YYYYMMDD-WAxxxx.jpg`
  - Subcarpeta `Quirellii` → 17 imágenes `IMG-YYYYMMDD-WAxxxx.jpg`
- **Problema:** nombres genéricos (sin modelo/color) → requiere identificación visual.
- **Riesgo:** intentos previos de análisis visual tumbaron la sesión.
- **Plan seguro:** procesar **por lotes pequeños** (p. ej. 5 imágenes), guardando resultado en CSV tras cada lote, sin base64 masivo ni timeouts largos.

### P2 — Reporte de gaps para el cliente
- Lista accionable de los 47 modelos sin foto (fotografiar / solicitar / reusar).

### P3 — Fase 2 del cruce (archivos reales)
- Para los 7 modelos con match: validar dimensiones, hash de duplicados, manifest `modelo→color→rutas`.
- Requiere revisar antes el PDF de derechos de producción (uso digital).

### P4 — Alineación de config (no iniciado)
- `tenants/flexi/config.json`: alinear funnels con la auditoría CRO (3 funnels) y agregar `unit_economics`.
- `FunnelLine` en `core/growthos-core/core/enums.py` está cableado a las líneas de micas → generalizar para flexi.

---

## Notas de método
- Auditoría por nombres = leer **solo el texto del nombre** (no abre imágenes).
- La llave de cruce de assets es el **código de modelo** (`\d{4,6}`).
- Los colores de los nombres NO son autoritativos; el catálogo manda.

---

## Verificación de duplicidad: Drive (marketing) vs `assets/` (2026-10-16)

**Pregunta:** ¿las carpetas de campaña revisadas en Drive ya son las mismas que están en `assets/`?
**Respuesta:** en su mayoría **SÍ** — `assets/*/campana_oi26` es una copia de las carpetas de Drive.

| Carpeta Drive | Archivos | Ya en `assets/` (mismo nombre) | Mismo nombre+tamaño |
|---|---|---|---|
| Flexi / FOTOS OI26 FINALES (nivel top) | 198 | 198 | **198** (idénticos) |
| Flexi / PORTADILLAS FLEXI OI26 | 36 | 35 | 22 (13 recomprimidos, 1 sólo en Drive) |
| Flexi Country / PORTADILLAS OI26 | 118 (+176 dup) | **0** | 0 |
| Quirelli / Campaña | 158 | 107 | 107 (51 sólo en Drive) |
| Quirelli / Essencial | 54 | 48 | 48 (6 sólo en Drive) |

**Conclusiones:**
1. La campaña OI26 (Flexi/Quirelli) **ya está copiada** en `assets/` → reprocesarla con visión sería redundante.
2. **`Flexi Country` NO está en `assets/`** (0 coincidencias) → es material no integrado.
3. La carpeta de **nombres perdidos** (`Catálogo disponibles/Productos /{Flexii,Quirellii}`) **NO está en `assets/`** y **no se cruza con la campaña** → es material nuevo, el único realmente por catalogar.
4. Ya existe copia de 3 imágenes en `docs/Catálogo disponibles/` (IMG-20261012-WA0005/6/7).

**Cobertura del catálogo en `assets/`: solo 5 de 54 modelos** tienen carpeta
(`142801, 142901, 143001, 143201, 306703`). Los otros 49 no tienen ningún asset.

> Nota: `66517` y `66525` (del catálogo) solo aparecen en la carpeta **Country** de Drive, que no está en `assets/`.

---

## Filtro de assets por inventario (2026-10-16)

**Objetivo:** dejar en `assets/` solo los modelos que están en existencia (catálogo confirmado).
**Ejecutado:** mover (no borrar) las carpetas de modelos fuera de inventario a `assets/_no_inventario/` — **reversible**.

| | Antes | Después |
|---|---|---|
| Carpetas de modelo activas | 89 | **5** |
| Archivos de producto activos | 359 | **23** |
| Archivados | — | 84 carpetas / **336 archivos** |

**Activos (producto):**
| Modelo | Marca | Fotos | Carpeta |
|---|---|---|---|
| 142801 ISAURA | Flexi | 5 | `assets/flexi/campana_oi26/142801` |
| 142901 JOCELYN | Flexi | 2 | `assets/flexi/campana_oi26/142901` |
| 143001 GINNY | Flexi | 3 | `assets/flexi/campana_oi26/143001` |
| 143201 LYDIA | Flexi | 5 | `assets/flexi/campana_oi26/143201` |
| 306703 ARISHA | Quirelli | 8 | `assets/quirelli/campana_oi26/306703` |

**No se tocó** (no son de producto): `brand`, `catalogo`, `tecnologias`, `shared/derechos` (76 archivos).
**Estructura conservada:** `assets/<marca>/campana_oi26/<codigo>/` (opción "solo filtrar").

**Reversión:** mover de vuelta desde `assets/_no_inventario/<marca>/campana_oi26/<codigo>/`.

### Limpieza del cache visual (mismo día)
- `data/visual_assets_cache.json`: se eliminaron las entradas con ruta inválida (movida) → **323 → 75 entradas** (todas válidas).
- Backup: `data/visual_assets_cache.backup_20261016.json`.
- El cache ahora refleja solo assets activos (sin visión; operación barata).
- **Pendiente:** si se recuperan modelos desde `_no_inventario`, regenerar/limpiar de nuevo.
