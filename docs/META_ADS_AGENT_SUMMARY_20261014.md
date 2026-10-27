# Meta Ads Agent Summary - Flexi Piedras Negras

**Fecha:** 14 Octubre 2026  
**Campaña:** 2026-10_flexi_ads_500mxn  
**Estado:** 📊 Análisis completado - Pendiente aprobación

---

## Análisis de Rendimiento (251 posts, 2026-08-04 a 2026-10-17)

### Métricas Globales
- **Total clicks**: 183
- **Total engagement**: 61 (reacciones + comentarios + shares)
- **Mediana clicks**: 0
- **Media clicks**: 0.729
- **Top 10 posts**: 33.3% de clicks totales
- **Top 20 posts**: 48.1% de clicks totales

### Top Posts por Clicks

| Fecha | Clicks | Engagement | Contenido |
|-------|--------|------------|-----------|
| 2026-09-25 | 17 | 3 | Encuesta: "¿cuál sería tu favorito?" / "VOTA POR TU PREFERIDO" |
| 2026-09-26 | 6 | 0 | "Sábado de shopping… un nuevo par puede transformar todo un look" |
| 2026-09-24 | 6 | 0 | Quirelli / "ocasiones que mereces lucir espectacular" |
| 2026-10-13 | 5 | 0 | "Hay zapatos que complementan tu atuendo y otros que elevan toda tu presencia" |
| 2026-10-09 | 5 | 0 | Flats / "toque moderno a tus outfits" |

**El post de encuesta concentra 17 de 183 clicks = 9.3% del total.**

---

## Señales por Característica

| Característica | Muestra | Clicks promedio vs. sin ella | Factor |
|----------------|---------|------------------------------|--------|
| Pregunta | 16 | 1.38 vs 0.69 | **2.01×** |
| Encuesta/voto | 2 | 8.50 vs 0.67 | **12.75×** (muestra pequeña) |
| Comodidad/confort | 94 | 0.97 vs 0.59 | **1.65×** |
| Estilo | 94 | 0.77 vs 0.71 | 1.08× |
| Quirelli | 43 | 0.81 vs 0.71 | 1.14× |
| CTA explícito | 87 | 0.80 vs 0.69 | 1.17× |
| Oficina | 2 | 2.00 vs 0.72 | 2.78× |
| Escolar | 25 | 0.40 vs 0.77 | 0.52× |
| Botines | 8 | 0.00 vs 0.75 | ❌ Negativa |
| Menciona ubicación | 48 | 0.52 vs 0.78 | ❌ Negativa |
| Menciona precio | 11 | 0.09 vs 0.76 | ❌ Negativa |

---

## ⚠️ Caveat Crítico

**No hay impresiones ni reach disponibles** con los permisos actuales. `post_clicks` es métrica relativa de consumo/interacción, **NO clicks web ni CTR**.

La encuesta es outlier fuerte; no debe definir sola la voz.

---

## Señales Defendibles para Voice Meta Ads

### ✅ Hooks que funcionan:
- Preguntas directas y encuestas
- Comodidad/confort
- Beneficio ligado a estilo, oficina u ocasión
- Quirelli con narrativa de estilo/ocasión

### ❌ Evitar como hook:
- Precio
- Ubicación como gancho principal
- Escolar en este periodo
- Botines en este periodo

---

## Hechos Verificados por Modelo (Product Truths)

| Modelo | Marca | Tipo | Línea | Atributos Verificados | Colores |
|--------|-------|------|-------|----------------------|---------|
| 142801 ISAURA | Flexi | Balerina punta cuadrada | Semivestir/casual | Piel natural | Beige, Negro |
| 142901 JOCELYN | Flexi | Mocasín/slip on | Confort/casual | Walking Soft, piel | Oro, Negro |
| 143001 GINNY | Flexi | Balerina sport | Confort/casual | Comodidad/suavidad/ligereza | Plata, Negro, Oro |
| 143201 LYDIA | Flexi | Modelo confirmado | - | Marca Flexi, color Negro | Negro |
| 306703 ARISHA | Quirelli | Modelo confirmado | - | Marca Quirelli | Nude, Negro |

**Referencia**: `tenants/flexi/docs/CATALOGO_FLEXI_CONTEXTO_20261014.md` líneas 37, 49, 84, 176, 182.

---

## Propuesta Pendiente de Aprobación

Crear dos capas nuevas, **sin cambiar la voz de WhatsApp**:

1. `tenants/flexi/brand/voice/meta_ads.md`
   - Hooks permitidos
   - Ritmo y longitud
   - Cómo usar "distribuidor oficial" sin sonar a respuesta de chat
   - Ejemplos buenos/malos específicos de anuncio

2. `tenants/flexi/ads/campanas/2026-10_flexi_ads_500mxn/_product_truths.md`
   - Hechos verificados por modelo
   - Campos no verificados como `[POR CONFIRMAR]`
   - Copywriter deberá usar al menos un hecho verificado por variante

---

## Siguiente Paso

Responder a Fernando con este análisis y pedir aprobación para:
1. Guardar análisis dentro de la campaña
2. Crear `meta_ads.md`
3. Crear `_product_truths.md`
4. Ajustar copywriter para exigir un hecho verificado por variante
5. Regenerar G2 como `propuesta_v5.md`
6. Mantener v4 y anteriores como historial; no publicar nada

**No crear capas ni modificar agente hasta confirmación de Fernando.**
