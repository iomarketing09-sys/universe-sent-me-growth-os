# Informe de Voz de Marca - Flexi (Zapatería Piedras Negras)

**Fecha:** 14 Octubre 2026  
**Generado por:** Brand Voice Agent (Growth OS)  
**Fuentes analizadas:** 19 posts orgánicos Facebook + 25 mensajes DM (Messenger)  
**Período:** Agosto - Octubre 2026

---

## 📊 RESUMEN EJECUTIVO

| Métrica | Posts Orgánicos | Mensajes DM (Messenger) | Consolidado |
|---------|----------------|------------------------|-------------|
| **Score Tono Global** | 64/100 | 63/100 | **63.5/100** |
| **Formalidad** | 85% | 60% | 72.5% |
| **Estructura** | 55% | 85% | 70% |
| **Emojis** | 50% | 100% | 75% |
| **Patrones Brand** | 50% | 50% | 50% |
| **Perspectiva** | 100% | 55% | 77.5% |
| **Vocabulario** | 50% | 50% | 50% |

**Diagnóstico:** La voz de marca tiene base sólida pero necesita **estandarización de vocabulario**, **patrones de apertura/cierre/CTA** y **perspectiva consistente** (tú/nosotros vs tercera persona).

---

## 🎯 ANÁLISIS POR FUENTE

### 1. POSTS ORGÁNICOS FACEBOOK (19 posts, Oct 2026)

**Temas principales:**
- Comodidad al caminar (#ComodidadEnMovimiento)
- Estilo por ocasión (formal, casual, temporada)
- Productos específicos: Quirelli, FlexiCountry, plantillas, carteras, cintos
- Ubicación: "Zapatería Flexi #PiedrasNegras", "Soriana Híper local 25"
- Horarios y disponibilidad

**Patrones detectados:**
- **Apertura:** Gancho emocional/beneficio ("Para las ocasiones que merecen algo especial...")
- **Cuerpo:** Beneficio + producto + ubicación
- **Cierre:** CTA suave ("Ven por tu favorita", "Te esperamos")
- **Hashtags:** #Flexi, #PiedrasNegras, #ComodidadEnMovimiento, #Quirelli, #FlexiCountry
- **Emojis:** Moderados (👌🏻 😌 🕕 👜 👞 🍂 🥾 ✨ 🥿 😎 💕 😎 ☺️ 🫵🏻 👟👞🥿👢 🙂 😉 😁)

**Ejemplos representativos:**
> "Para las ocasiones que merecen algo especial tenemos a #Quirelli. Un diseño que marca la diferencia y un estilo que perdura👌🏻 Los tenemos en Zapatería Flexi #PiedrasNegras"

> "Tus pies también necesitan un descanso👣 Elige un calzado que combine estilo, comodidad y la sensación de sentirte bien al caminar."

---

### 2. MENSAJES DIRECTOS - MESSENGER (25 mensajes, Ago-Oct 2026)

**Tipos de consultas atendidas:**
1. **Disponibilidad de tallas** (9 mensajes) - "lo más grande lo tenemos en 29.5"
2. **Disponibilidad de modelos** (6 mensajes) - "por ahora no", "solo eso está disponible"
3. **Ubicación/horarios** (3 mensajes) - "en Soriana Híper...", "hoy cerramos a las 8pm"
4. **Especificaciones técnicas** (3 mensajes) - "Flexi no fabrica ese tipo de suela", "marca Coqueta"
5. **Recomendaciones especializadas** (2 mensajes) - pie diabético, ancho especial
6. **Confirmación de llegada** (2 mensajes) - "ya nos llegó ese modelo"

**Tono conversacional real:**
- **Cortés y directo:** "Buenas tardes", "Buenos días", "Buen día"
- **Informativo concreto:** Tallas, modelos, ubicación, horarios
- **Gestión de expectativas:** "por ahora no", "esperando resurtido", "únicos pares"
- **Poca uso de emojis** (solo 1 🙂 en 25 mensajes)
- **Perspectiva mixta:** "tenemos", "no tenemos", "Flexi no fabrica" (tercera persona marca)

---

## 🔍 HALLAZGOS CLAVE

### Fortalezas
1. **Consistencia de ubicación:** Siempre menciona "Zapatería Flexi #PiedrasNegras" / "Soriana Híper local 25"
2. **Enfoque beneficio:** Comodidad, estilo, durabilidad como pilares
3. **Mención de sub-marcas:** Quirelli, FlexiCountry, Coqueta - diferencia producto
4. **Respuesta rápida y útil** en DMs - información concreta (tallas, stock, ubicación)

### Áreas de Mejora
1. **Vocabulario no estandarizado:** Lista `preferred` y `avoid` vacías en brand_voice.json
2. **Patrones de mensaje ausentes:** Openings, closings, CTAs no definidos sistemáticamente
3. **Inconsistencia perspectiva:** 
   - Posts: "tenemos", "disponibles en", "te esperamos" (nosotros/tú)
   - DMs: "lo tenemos", "no tenemos", "Flexi no fabrica" (mezcla nosotros/tercera persona)
4. **Emojis:** 50% posts vs 4% DMs - necesita regla por canal
5. **CTAs:** Posts tienen CTA suave; DMs casi no usan CTA de cierre

---

## 🎨 PROPUESTA DE VOZ DE MARCA ESTANDARIZADA

### Atributos de Voz (Actualizados)

```json
{
  "tone": "Profesional, cercano, experto en producto, orientado a solución",
  "formality": "tú cercano (usted solo si cliente lo usa primero)",
  "emoji_usage": {
    "organic_social": "moderado (2-3 por post)",
    "whatsapp_messenger": "ligero (0-1 por mensaje, solo si cliente usa)",
    "meta_ads": "mínimo (solo en headline/primary text)"
  },
  "sentence_length": "media-corta (claridad en atención)",
  "perspective": "nosotros/tú (evitar tercera persona 'Flexi hace/no hace')"
}
```

### Vocabulario Propuesto

| Preferidos | Evitar |
|------------|--------|
| "Encuentra tu par ideal" | "El mejor del mercado" ❌ |
| "Comodidad en cada paso" | "Garantizado 100%" ❌ |
| "Para tus pasos" | "Lo más barato" |
| "Estilo que acompaña" | "Único/Exclusivo" (sin prueba) |
| "Te ayudamos a elegir" | "Tenemos todo" |
| "Visítanos en..." | "Pregúntale a..." |

### Términos de Producto
- **Líneas:** Flexi (core), Quirelli (formal caballero), FlexiCountry (outdoor/botas), Coqueta (dama accesible)
- **Accesorios:** Plantillas Memory Foam, Mini plantilla, Talonera, Cintos, Carteras, Productos de limpieza
- **Categorías:** Casual, Formal, Deportivo, Trabajo, Tacones, Flats, Botines

---

## 📝 PATRONES DE MENSAJERÍA ESTANDARIZADOS

### WhatsApp / Messenger (Atención Cliente)

| Etapa | Patrón | Ejemplo |
|-------|--------|---------|
| **Apertura** | "¡Hola! 👋 Bienvenido a Zapatería Flexi. ¿En qué te ayudo hoy?" | Estándar |
| **Consulta talla** | "Tenemos disponible en [talla]. ¿Quieres que te la reservemos?" | Proactivo |
| **Sin stock** | "Por ahora no contamos con [modelo/talla], pero llega resurtido [fecha]. ¿Te aviso cuando llegue?" | Gestión expectativa + CTA |
| **Ubicación** | "Estamos en Soriana Híper local 25 (lado Banco Azteca), abiertos hasta las 8pm 🕕" | Claro + emoji ligero |
| **Especificaciones** | "[Modelo] es [característica]. ¿Buscas algo específico para [uso]?" | Experto + pregunta |
| **Cierre** | "¡Gracias por contactarnos! 😊 ¿Algo más en lo que te pueda ayudar?" | Estándar |

### Posts Orgánicos (Facebook/Instagram)

| Estructura | Ejemplo |
|------------|---------|
| **Hook emocional** + **Beneficio** + **Producto** + **Ubicación** + **CTA suave** | "Tus pies merecen un descanso 👣 Descubre la comodidad de FlexiCountry para explorar sin límites. Disponible en Zapatería Flexi #PiedrasNegras. ¿Cuál te llevas? 🥾" |

### Meta Ads (Click to WhatsApp)

| Componente | Regla |
|------------|-------|
| **Headline** | Beneficio directo + ubicación ("Comodidad en cada paso • Zapatería Flexi Piedras Negras") |
| **Primary Text** | Hook + 2 beneficios + CTA directo ("Escríbenos y encuentra tu talla ideal") |
| **CTA Button** | "Enviar mensaje" / "WhatsApp" |

---

## 🧪 A/B VARIANTS GENERADOS (Ejemplos)

### Caso: Respuesta disponibilidad talla
| Variante | Copy | Hipótesis |
|----------|------|-----------|
| **Control** | "Buenas tardes, lo más grande lo tenemos en 29.5" | Baseline actual |
| **Hook Variation** | "¿Te ayudo a encontrar tu talla ideal? 👇 Tenemos hasta 29.5" | Hook pregunta aumenta engagement |
| **CTA Variation** | "Buenas tardes, lo más grande lo tenemos en 29.5 ¿Te la reservamos?" | CTA directo mejora conversión |

### Caso: Sin stock modelo
| Variante | Copy | Hipótesis |
|----------|------|-----------|
| **Control** | "Buen día, por el momento no." | Baseline |
| **Empatía + Acción** | "Buen día 😊 Ese modelo se agotó, pero llega resurtido la próxima semana. ¿Te aviso cuando tengamos tu talla?" | Empatía + CTA proactivo |
| **Alternativa** | "Buen día, ese no lo tenemos ahora. ¿Buscas algo similar? Tenemos [modelo alternativo] en tu talla 👟" | Redirección a venta |

---

## 🎯 HOOKS GENERADOS PARA FLEXI

### Atención Cliente (Servicio)
1. "¿Tus pies te piden un descanso? 👣 Te ayudamos a encontrar el par perfecto"
2. "¿Buscas comodidad sin renunciar al estilo? Tenemos tu talla ✨"
3. "¿Necesitas calzado para [ocasión]? Te recomiendo según tu uso 👞"
4. "¿Sabes tu talla exacta? Te guiamos para que no falle 📏"
5. "¿Modelo agotado? Te avisamos en cuanto llegue resurtido 🔔"

### Ventas Orgánicas (Posts)
1. "Para las ocasiones que merecen algo especial... #Quirelli 👞"
2. "Tus pasos cuentan una historia. ¿Cuál quieres escribir hoy? ✍️👟"
3. "Comodidad que se siente desde el primer paso ☁️"
4. "De la oficina al evento sin cambiar de zapatos 🔄👔"
5. "El otoño pide botines. FlexiCountry te acompaña 🍂🥾"

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

| Acción | Prioridad | Estado |
|--------|-----------|--------|
| Actualizar `brand_voice.json` con vocabulario preferido/evitar | 🔴 Alta | ⏳ Pendiente |
| Definir `messaging_patterns` (opening, closing, CTA) por canal | 🔴 Alta | ⏳ Pendiente |
| Estandarizar perspectiva: "tenemos/te ayudamos" vs "Flexi tiene" | 🟡 Media | ⏳ Pendiente |
| Reglas emoji por canal (orgánico vs DM vs ads) | 🟡 Media | ⏳ Pendiente |
| Capacitar equipo atención en nuevos patrones | 🟡 Media | ⏳ Pendiente |
| Configurar templates WhatsApp Business con nuevos patrones | 🟢 Baja | ⏳ Pendiente |
| A/B test variantes en próximos 30 días | 🟢 Baja | ⏳ Pendiente |

---

## 📁 ARCHIVOS ACTUALIZADOS

- `tenants/flexi/brand_voice.json` → **Requiere actualización con este informe**
- `tenants/flexi/docs/INFORME_VOZ_MARCA_FLEXI.md` ← **Este archivo**

---

## 🔄 PRÓXIMOS PASOS

1. **Aprobar** vocabulario y patrones propuestos con equipo Flexi
2. **Actualizar** `brand_voice.json` con vocabulario, patrones y channel_rules
3. **Entrenar** Brand Voice Agent con nuevos ejemplos `good`/`bad`
4. **Generar** templates WhatsApp Business aprobados por Meta
5. **Lanzar** campaña Meta Ads "Click to WhatsApp" con copy optimizado
6. **Medir** mejora en tasa de respuesta y conversión DM→venta

---

*Informe generado automáticamente por Growth OS Brand Voice Agent*  
*Modelos: GPT-OSS 20B/120B (Groq) + Morph V3 Fast para análisis de tono*  
*Próxima revisión: 28 Octubre 2026 (post A/B tests)*
