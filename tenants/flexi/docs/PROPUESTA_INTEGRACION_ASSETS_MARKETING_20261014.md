# Propuesta de Integración de Assets de Marketing - Flexi & Quirelli
**Fecha:** 2026-10-14  
**Cliente:** Flexi (tenant: flexi)  
**Fuente:** `/home/universe-sent-me/GoogleDrive/Informes FLEXI/marketing/`

---

## 📦 Resumen del Inventario de Assets

### Flexi (Marca Principal)
| Carpeta | Contenido | Tamaño | Prioridad |
|---------|-----------|--------|-----------|
| `Catalogo/` | 3 ZIPs: Catálogo OI26 principal (28MB), Accesorios (8MB), Pro/Servicio (14MB) | ~50MB | **ALTA** - PDFs fuente para catálogo B2B |
| `Campaña OI26/FOTOS OI26 FINALES/` | 200+ fotos finales (nombradas: MODELO_CODIGO_COLOR_OI26.jpg) | ~6GB | **ALTA** - Assets listos para contenido social |
| `Campaña OI26/PORTADILLAS FLEXI OI26/` | Portadillas de campaña | - | MEDIA |
| `Campaña Country OI26/` | PDF derechos + Portadillas Quirelli (357MB ZIP) | ~360MB | MEDIA |
| `Tenologias y atributos/` | 15 ZIPs logos tecnología + manuales capacitación | ~25MB | **ALTA** - Para comunicar atributos |
| `logotipo oficial/` | Logo Flexi, Tipografía, Uso de marca (Brandbook) | ~7MB | **ALTA** - Brand guidelines |
| `Logo Flexi Country/` | Brandbook completo FC, logos, tipografía | ~85MB | MEDIA |

### Quirelli (Sub-marca)
| Carpeta | Contenido | Tamaño | Prioridad |
|---------|-----------|--------|-----------|
| `CATÁLOGO-QUIRELLI_OI26.zip` | Catálogo Quirelli OI26 (2.2MB) | 2MB | **ALTA** |
| `Campaña OI26/Campaña/` | 100+ fotos finales (nombradas: MODELO_CODIGO_COLOR_QUIRELLI_OI26.jpg) | ~2GB | **ALTA** |
| `Campaña OI26/Essencial/` | Versiones "Essencial" recortadas/optimizadas | ~700MB | MEDIA |
| `Logo oficial/` | Logotipo con ®, Guía de marca, Tipografía | ~9MB | **ALTA** |

### Documentos de Derechos
- `Flexi_-_Derechos_Producción_Otoño_Invierno_2026.pdf` (8.6MB)
- `QUIRELLI_-_Derechos_Producción_Otoño_Invierno_2026.pdf` (3MB)
- `Flexi_Country_-_Derechos_Producción_Otoño_Invierno_2026.pdf` (3.9MB)

---

## 🎯 Estrategia de Integración Propuesta

### Fase 1: Extracción y Catalogación (Esta semana)
```bash
# Estructura destino en growth-os
tenants/flexi/assets/
├── flexi/
│   ├── catalogo/           # PDFs descomprimidos
│   ├── campana_oi26/       # Fotos finales organizadas por modelo
│   ├── tecnologias/        # Logos de tecnología (Walking Soft, etc.)
│   ├── brand/              # Logos, tipografía, brandbook
│   └── portadillas/
├── quirelli/
│   ├── catalogo/
│   ├── campana_oi26/
│   ├── esencial/
│   └── brand/
└── shared/
    └── derechos/           # PDFs de derechos de producción
```

### Fase 2: Mapeo Modelo ↔ Assets (Crítico)
**Patrón de nomenclatura detectado:**
- Flexi: `NOMBRE_MODELO_CODIGO_COLOR_OI26.jpg` → ej: `GINNY_143001_PLATA_OI26.jpg`
- Quirelli: `NOMBRE_MODELO_CODIGO_COLOR_QUIRELLI_OI26.jpg` → ej: `ADRIENNA_307201_NEGRO_QUIRELLI_OI26.jpg`

**Acción:** Script para extraer código de modelo del filename y mapear a `catalogo_modelos_oficiales.csv`

### Fase 3: Selección de Assets para Producción (Top 5 prioridad)
| Prioridad | Modelo | Marca | Código | Assets Disponibles | Formato Objetivo |
|-----------|--------|-------|--------|-------------------|------------------|
| 1 | Ginny | Flexi | 143001 | Múltiples colores | Carrusel 3 colores |
| 2 | 117207 | Flexi | 117207 | Taupe, Blanco, Negro | Carrusel 3 colores |
| 3 | 305101 | Quirelli | 305101 | Negro, Tan (Hexafoam) | Carrusel tecnología |
| 4 | 404801 | Flexi | 404801 | Oporto, Negro | Carrusel Caballero |
| 5 | 88702 | Quirelli | 88702 | Negro, Brandy | Carrusel Hidalgo |

### Fase 4: Generación de Contenido
- **Carruseles Meta/Instagram**: 1080x1080px, 3-5 slides
- **Reels**: 1080x1920px, 15-30s
- **WhatsApp Business**: Catálogo nativo + plantillas
- **PDF B2B**: Catálogo profesional unificado

---

## 🛠️ Scripts y Herramientas Necesarias

### 1. Script de Extracción y Organización
```python
# tenants/flexi/scripts/organize_assets.py
# - Descomprime ZIPs
# - Parsea nombres de archivo → modelo, color, marca
# - Copia a estructura tenants/flexi/assets/
# - Genera manifest JSON: asset_map.json
```

### 2. Script de Mapeo Catálogo-Assets
```python
# tenants/flexi/scripts/map_catalog_assets.py
# - Lee catalogo_modelos_oficiales.csv
# - Cruza con asset_map.json
# - Reporta: modelos con assets, sin assets, assets huérfanos
# - Genera catalogo_con_assets.csv
```

### 3. Generador de Carruseles (Plantillas)
```python
# tenants/flexi/scripts/generate_carousel.py
# - Plantillas Canva/Figma programáticas (Pillow/PIL)
# - Input: modelo, assets, copy, brand guidelines
# - Output: PNGs listos para Meta Ads Manager
```

---

## 📋 Checklist de Decisiones Pendientes (Para Reunión Mañana)

### Catálogo e Inventario
- [ ] Confirmar 65 modelos / 83 variantes (lista entregada)
- [ ] Validar colores por modelo
- [ ] Confirmar stock disponible por modelo/color/talla
- [ ] Definir precios PVP y precio distribuidor (B2B)
- [ ] Confirmar tallas disponibles por modelo

### WhatsApp Business
- [ ] Número de teléfono a registrar
- [ ] Nombre de negocio verificado
- [ ] Categoría: "Retail" / "Shopping"
- [ ] Configurar catálogo nativo en WhatsApp
- [ ] Plantillas de mensaje (HSM) aprobadas

### Meta Business Manager
- [ ] Acceso a Business Manager del cliente
- [ ] Cuenta publicitaria configurada
- [ ] Pixel instalado en web/ecommerce
- [ ] Eventos de conversión definidos

### Brand & Legal
- [ ] Confirmar uso de assets OI26 para digital (derechos PDF)
- [ ] Aprobar brand voice v2.0 (Flexi vs Quirelli separados)
- [ ] Definir tone of voice por canal (WhatsApp vs Meta Ads vs Organic)

---

## 📁 Estructura de Archivos a Crear en growth-os

```
tenants/flexi/
├── assets/                          # NUEVO - Assets organizados
│   ├── flexi/
│   ├── quirelli/
│   └── shared/
├── data/
│   ├── catalogo_modelos_oficiales.csv       # EXISTE
│   ├── catalogo_modelos_oficiales.json      # EXISTE
│   ├── catalogo_modelos_contexto.json       # EXISTE
│   ├── asset_manifest.json                  # NUEVO - Mapeo assets
│   └── catalogo_con_assets.csv              # NUEVO - Catálogo enriquecido
├── docs/
│   ├── CATALOGO_FLEXI_CLIENTE_20261014.md   # EXISTE - Para cliente
│   ├── CATALOGO_FLEXI_CLIENTE_CHECKLIST_20261014.md  # EXISTE
│   ├── CATALOGO_FLEXI_RESUMEN_20261014.md   # EXISTE
│   ├── CATALOGO_FLEXI_CONTEXTO_20261014.md  # EXISTE
│   ├── PROPUESTA_INTEGRACION_ASSETS_20261014.md  # ESTE DOC
│   └── BRAND_GUIDELINES_FLEXI_QUIRELLI.md   # NUEVO - De brandbooks
├── brand_voice.json                     # EXISTE v2.0
├── scripts/
│   ├── organize_assets.py               # NUEVO
│   ├── map_catalog_assets.py            # NUEVO
│   └── generate_carousel.py             # NUEVO
└── content/                             # NUEVO - Contenido generado
    ├── carruseles/
    ├── reels/
    ├── whatsapp/
    └── b2b_catalog/
```

---

## ⚡ Acciones Inmediatas (Post-Reunión)

1. **Ejecutar extracción:** `python3 tenants/flexi/scripts/organize_assets.py`
2. **Mapear catálogo:** `python3 tenants/flexi/scripts/map_catalog_assets.py`
3. **Revisar reporte:** `cat tenants/flexi/data/catalogo_con_assets.csv`
4. **Generar primeros 5 carruseles:** `python3 tenants/flexi/scripts/generate_carousel.py --top5`
5. **Subir a Meta Ads Manager** y programar en `GrowthOS/01_01_Calendario_Semanal.md`

---

## 🔗 Referencias Rápidas

| Documento | Ubicación |
|-----------|-----------|
| Catálogo cliente (para revisión) | `tenants/flexi/docs/CATALOGO_FLEXI_CLIENTE_20261014.md` |
| Checklist cliente | `tenants/flexi/docs/CATALOGO_FLEXI_CLIENTE_CHECKLIST_20261014.md` |
| Contexto técnico + URLs | `tenants/flexi/data/catalogo_modelos_contexto.json` |
| Brand Voice v2.0 | `tenants/flexi/brand_voice.json` |
| Manual operaciones | `GROWTH_OS_MANUAL.md` |
| AGENTS.md | `AGENTS.md` |

---

**Próximo paso:** Revisar esta propuesta con el cliente mañana, confirmar checklist, y proceder con extracción de assets.
