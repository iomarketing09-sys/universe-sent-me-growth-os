# Módulo `creative`

Copy, kit de marca y selección de imágenes para armar piezas de campaña.

## Estructura

```
modules/creative/
├── __init__.py           API pública (11 nombres)
├── brand_kit.py          Colores, logo, tipografía y reglas visuales por tenant
├── image_selector.py     Selección de imágenes reales del inventario
└── agents/
    └── copywriter_agent/ Copy por tenant, con voz de marca y skills de anuncios
```

`agents/copywriter_agent/` en la raíz quedó como envoltorio de compatibilidad.

## Uso

Copy (dry-run, no escribe nada):

```bash
python3 -m modules.creative.agents.copywriter_agent.agent flexi \
  --campaign 2026-10_flexi_ads_500mxn --offline
```

Guardar la propuesta dentro de la campaña: agregar `--write`.

Selección de imágenes (solo modelos del inventario, sin duplicados):

```bash
python3 -m modules.creative.image_selector flexi \
  --campaign 2026-10_flexi_ads_500mxn \
  --max-per-model 5 --max-total 8
```

Kit de marca del tenant:

```bash
python3 -m modules.creative.brand_kit flexi
```

## Reglas de negocio

- El producto siempre es real y sale de `config.ads.approved_models` (inventario).
- El resto del material (guía de temporada, brand book, fotos de marca) es libre
  mientras respete el kit.
- Máximo 5 imágenes por modelo y 8 por campaña, ajustables por CLI.
- No se pinta precio, stock ni promociones en el arte.
- Si el kit no define paleta exacta, los hex se marcan como `hex_aproximado` y
  hay que confirmarlos antes de arte final.

## Kit de Flexi

`tenants/flexi/brand_kit.json` sale de material oficial:

- Temporada OI26, macrotendencia **"Luz y sombra"** (`GUIA_DE_TEMPORADA_FLEXI_OI26.pdf`).
- Paleta: rojo Flexi `#D82232` (muestreado de `LOGO_FLEXI_ROJO.png`, Pantone 1797)
  más arena, canela, café profundo, vino, azul petróleo y naranja quemado
  (aproximados, pendientes de confirmar contra la guía impresa).
- Tipografía pendiente: confirmar con `Final_BrandBook_FC (1).pdf`.
