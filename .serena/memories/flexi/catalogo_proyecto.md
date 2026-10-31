# Proyecto Catálogo Flexi (tenant `flexi`, physical_cro, sin canon)

Bitácora viva: `tenants/flexi/docs/BITACORA_CATALOGO_FLEXI.md`
Changelog: `GrowthOS/00_01_Changelog_GrowthOS.md` [5.98.00] (2026-10-16)

## Estado (2026-10-16)
- `tenants/flexi/data/catalogo_flexi_confirmado.csv` → 54 modelos / 75 variantes (45 Flexi + 9 Quirelli). Único CSV; solo lo confirmado.
- `tenants/flexi/data/color_normalization_map.json` → normalización de colores de nombres de imagen (no altera catálogo).
- `tenants/flexi/docs/AUDITORIA_CONTENIDO_OI26_20261016.md` → auditoría por nombres; 7 de 54 modelos con asset OI26, 47 sin foto.

## Decisiones del cliente
- Fuente de verdad = checklist de sucursal (`tenants/flexi/docs/CATALOGO_FLEXI_CLIENTE_CHECKLIST_20261014.md`).
- Descartados: 4 modelos N/H (143302, 401301, 68714, 98304) y 9 del catálogo previo no confirmados (104523, 300801, 300808, 303302, 304202, 304401, 304704, 35802, 35902).
- Flexi Country = rama de Flexi.
- Colores del catálogo = los del checklist.

## Modelos con asset OI26 (7)
142801, 142901, 143001, 143201, 66517, 66525 (Flexi) y 306703 (Quirelli).

## Pendientes
- P1 (bloqueado): `.../Informes FLEXI/Catálogo disponibles/Productos /{Flexii (33), Quirellii (17)}` con nombres perdidos (`IMG-…-WA…jpg`) → identificación visual por lotes pequeños (análisis visual previo tumbó la sesión).
- P2: reporte de gaps (47 modelos sin foto) para el cliente.
- P3: cruce con archivos reales (dimensiones, hash duplicados, manifest) para los 7 modelos.
- P4: alinear `tenants/flexi/config.json` (3 funnels + `unit_economics`) y generalizar `FunnelLine` (hoy cableado a micas).

## Riesgos / notas
- Análisis visual de imágenes (vision vía OmniRoute / `test_vision.py`) ha caído la sesión → hacer por lotes y persistir resultados tras cada lote.
- Carpeta de trabajo en Drive (solo lectura); no copiar ni modificar originales.
- `physical_cro` no usa canon; gate = auditoría CRO.
