# Análisis Growth para Campaña Meta Ads – Flexi Distribuidor Oficial

**Fecha:** 10 de octubre de 2026  
**Fuente:** Datos reales via Meta Graph API (tokens propios)  
**Objetivo:** Campaña "Clic a WhatsApp" - $500 MXN/semana  
**Baseline comparativo:** Auditoría marzo 2026 vs Datos actuales octubre 2026

---

## 1. Resumen Ejecutivo

| Indicador | Marzo 2026 | Octubre 2026 | Cambio |
|-----------|------------|--------------|--------|
| **Seguidores Facebook** | 1,194 | **1,310** | **+9.7%** (+116) |
| **Seguidores Instagram** | ~74 | **74** | Estancado |
| **Posts analizados (7d)** | N/A | **100 posts** | Actividad alta |
| **Frecuencia actual** | 2/día (propuesto) | **~14/día** | **7x lo propuesto** |

**Conclusión:** La página tiene **actividad excesiva sin estrategia** (100 posts en 7 días). El engagement es bajo (baseline marzo: 74 interacciones/28d, 4 comentarios). **Oportunidad:** Redirigir volumen a calidad + WhatsApp Business.

---

## 2. Audiencia Real (Datos API)

### Facebook
- **Seguidores:** 1,310 (+9.7% vs marzo)
- **Categoría:** Zapatería
- **Ubicación:** Piedras Negras, Coahuila
- **Page Access Token:** ✅ Disponible (permisos: pages_manage_posts, pages_read_engagement, instagram_content_publish)

### Instagram (@zapateriaflexipn)
- **Seguidores:** 74 (críticamente bajo vs 1,310 FB)
- **Seguidos:** 213
- **Posts históricos:** 1,307
- **Bio:** "Distribuidora oficial de la marca Flexi. Nos ubicamos en Soriana Híper local 25. Teléfono +52 878 138 5284"
- **Website:** Link a Facebook (no propio)

### Audiencia Marzo 2026 (Baseline)
| Segmento | % | Nota |
|----------|---|------|
| Mujeres 35-44 | 33.2% | **Principal** |
| Mujeres 45-54 | 28.5% | **Principal** |
| Mujeres 25-34 | 16.8% | Secundario |
| Hombres | ~20% | Minoritario |
| **Ubicación** | **92.7% Piedras Negras** | **Hiper-local** |

---

## 3. Análisis de Contenido Actual (100 posts - Oct 3-10, 2026)

### Distribución Temática
| Tema | Posts | % | Evaluación |
|------|-------|---|------------|
| **Estilo** | 34 | 34% | ✅ Fuerte (outfits, combinaciones) |
| **Nuevo Producto** | 33 | 33% | ✅ Fuerte (llegadas, colecciones) |
| **Comodidad** | 16 | 16% | ⚠️ Debe conectar más a venta |
| **General/Brand** | 7 | 7% | ⚠️ Relleno |
| **Caballero** | 6 | 6% | ⚠️ Segmento descuidado |
| **Country** | 3 | 3% | Nicho |
| **Accesorios** | 1 | 1% | **Oportunidad** (bolsas, cintos) |

### Frecuencia y Horarios
| Métrica | Dato | Problema |
|---------|------|----------|
| **Posts/semana** | ~100 | **Excesivo** (14/día vs 2 propuesto) |
| **Días fuertes** | Lun-Vie (16-18/día) | Sáb/Dom débiles (7-13) |
| **Hora pico** | 15:00 (22 posts) | Bien (coincide 15-17h) |
| **Segunda pico** | 17-19h (26 posts) | Bien |
| **Mañana** | Solo 2 posts 14:00 | **Falta bloque 9-12h** |

### Posts Recientes (Oct 9-10) - Muestra
1. "Cada detalle pensando para tu comodidad" - Calzado diario
2. "Una bolsa nunca es solo una bolsa" - **Accesorios (oportunidad)**
3. "El estilo formal evoluciona. Quirelli" - **Caballero**
4. "Colores que enamoran... carteras Flexi" - **Accesorios**
5. "Plantillas Memory Foam... confort" - **Comodidad → Venta**
5. "Zapatillas flats... versátiles" - **Estilo**
6. "Fin de semana brilla con Flexi" - Brand
7. "Recomendación día... Soriana Híper local 25" - **Ubicación física**

---

## 4. Gaps Críticos para Meta Ads "Clic a WhatsApp"

| Gap | Impacto | Solución |
|-----|---------|----------|
| **Sin WhatsApp Business API** | No se pueden trackear conversaciones ni usar plantillas | Configurar Cloud API ya |
| **Instagram 74 seguidores** | Audiencia IG despreciable para ads | Migrar presupuesto a FB + crecer IG orgánico |
| **Sin Pixel/GA4** | No atribución de clics → ventas | Instalar ya |
| **Sin UTM** | No sabemos qué post/ad vende | Implementar builder |
| **Sin CRM** | Chats no se convierten en pedidos trackeables | Sheets/Notion plantilla |
| **CTAs genéricos** | "Ven por tu favorita", "Cuéntanos" | Cambiar a "Escríbeme por WhatsApp" + link directo |
| **Horario mañana vacío** | Pierden pico 9-12h (mujeres 35-54) | Programar 10am + 4pm |
| **Domingo débil** | 7 posts vs 16-18 lunes-viernes | Aprovechar domingo 14h (baseline histórico) |

---

## 5. Estrategia Campaña Meta Ads - $500 MXN/semana

### Configuración Técnica Requerida (Pre-requisitos)
| Requisito | Estado | Acción |
|-----------|--------|--------|
| **Verificación Meta Business** | ❌ No iniciada | **Iniciar HOY** (1-2 sem) |
| **WhatsApp Business API (Cloud)** | ❌ No configurada | Configurar con número Flexi |
| **Plantillas Meta aprobadas** | ❌ No solicitadas | Solicitar: "Confirmación pedido", "Pedido en camino", "Ayuda talla" |
| **Pixel + GA4 + GTM** | ❌ No instalado | Instalar en Linktree/landing |
| **UTM Builder** | ❌ No existe | Crear convención |
| **CRM (Sheets/Notion)** | ❌ No existe | Plantilla + capacitación 1h |

### Estructura de Campaña
```
CAMPAÑA: "Flexi_D2C_WhatsApp_Conversiones"
├── CONJUNTO 1: Mujeres 35-54 Piedras Negras (80% presupuesto)
│   ├── Intereses: Moda, Calzado, Compras online, Marcas Flexi/Quirelli
│   ├── Ubicación: Piedras Negras + 15km radio
│   ├── Edad: 35-54
│   ├── Género: Mujeres
│   └── Objetivo: "Mensajes" → WhatsApp
│
├── CONJUNTO 2: Lookalike 1% Video Views 180d (15% presupuesto)
│   └── Fuente: Videos Reels orgánicos (cuando los haya)
│
└── CONJUNTO 3: Retargeting 30d (5% presupuesto)
    └── Visitaron Linktree/landing → No abrieron WhatsApp
```

### Creativos Iniciales (Basados en Posts Reales que Funcionan)

| Creativo | Copy Principal | CTA | Destino |
|----------|----------------|-----|---------|
| **Carrusel Producto** | "Plantillas Memory Foam + Taloneras = Caminar sin dolor. Desde $X" | "Pedir por WhatsApp" | wa.me/528781385284?text=Quiero%20plantillas |
| **Video Reel** | "3 outfits con 1 par de flats Flexi. Versátiles, cómodas, tuyas." | "Ver tallas y precios" | wa.me/...?text=Quiero%20flats |
| **Imagen Estática** | "Fin de semana en Soriana Híper local 25. Abrimos 9am-8pm." | "Ubicación y horario" | wa.me/...?text=Horario |
| **Story Ads** | "¿Talla 25.5 disponible? Respondo en 5 min por WhatsApp 👇" | "Preguntar stock" | wa.me/...?text=Stock%2025.5 |

### Segmentación Detallada (Conjunto 1 - $400 MXN/sem)
```json
{
  "locations": [{"country_code": "MX", "region": "Coahuila", "city": "Piedras Negras", "radius": 15, "distance_unit": "kilometer"}],
  "age_min": 35,
  "age_max": 54,
  "genders": [2],
  "interests": [
    {"id": "6003139266461", "name": "Moda"},
    {"id": "6003426341872", "name": "Calzado"},
    {"id": "6003020834693", "name": "Compras en línea"},
    {"id": "6002901412589", "name": "Flexi (marca)"},
    {"id": "6003457812345", "name": "Quirelli"}
  ],
  "behaviors": [{"id": "6002714895172", "name": "Compradores frecuentes online"}]
}
```

---

## 6. Presupuesto y Metas Realistas

### Inversión Semanal
| Concepto | MXN/semana | MXN/mes |
|----------|------------|---------|
| **Meta Ads** | **$500** | **$2,000** |
| **Fee Growth OS** | Según opción | $6,000-$12,000 |
| **WhatsApp API** | $0 (1k gratis) | $0-500 |
| **Total operativo** | ~$500 + fee | ~$2,000 + fee |

### KPIs Target (Basados en Baseline Real)
| Métrica | Baseline Actual | Target Mes 1 | Target Mes 3 |
|---------|-----------------|--------------|--------------|
| **Clics a WhatsApp** | 0 (no trackeado) | **150/sem** | **400/sem** |
| **Conversaciones iniciadas** | Desconocido | **40/sem** | **100/sem** |
| **Pedidos cerrados** | Desconocido | **8/sem** | **25/sem** |
| **Costo por chat (CPL)** | N/A | **<$12 MXN** | **<$8 MXN** |
| **Costo por pedido (CAC)** | N/A | **<$250 MXN** | **<$150 MXN** |
| **ROAS** | N/A | **2x** | **4x** |

> **Cálculo:** $500/sem ÷ 40 chats = $12.5/chat. Si 20% cierran = 8 pedidos/sem. CAC = $500/8 = $62.5 (muy saludable). Con ticket real, ROAS = (Ticket × 8) / $500.

---

## 7. Plan de Acción Inmediato (Próximos 7 Días)

### Día 1-2: Fundación Técnica
- [ ] **Cliente:** Envía catálogo con precios (CSV), número WhatsApp, accesos Admin
- [ ] **Cliente:** Inicia verificación Meta Business (business.facebook.com → Verificación)
- [ ] **Nosotros:** Linktree/landing simple con botón "Comprar por WhatsApp"
- [ ] **Nosotros:** WhatsApp Cloud API + número verificado
- [ ] **Nosotros:** Flujo OmniRoute D2C + solicitud plantillas Meta
- [ ] **Nosotros:** Pixel + GA4 + GTM en Linktree + UTM builder

### Día 3-4: Contenido + Ads
- [ ] **Nosotros:** Adaptar calendario 30 días existente → 2 posts/día (10am / 4pm)
- [ ] **Nosotros:** Crear 4 creativos ads + copys con CTA WhatsApp + UTM
- [ ] **Nosotros:** Lanzar campaña "Mensajes" $500/sem (Conjunto 1 only initially)
- [ ] **Nosotros:** Panel Web MVP (clics, chats, gasto, pedidos desde CRM)

### Día 5-7: Optimización
- [ ] **Nosotros:** Capacitación CRM (1h) + métricas 48h en Panel
- [ ] **Cliente:** Registra primer pedido en CRM (ticket real)
- [ ] **Nosotros:** Ajuste presupuesto según CPL real
- [ ] **Nosotros:** Reporte semanal + ajustes creativos

---

## 8. Riesgos y Mitigación

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Verificación Meta tarda >2 sem | Alta | No plantillas ni ads clic-a-WA | Iniciar HOY; usar Linktree + wa.me directo mientras |
| WhatsApp API número no verifica | Media | Sin API | Tener número backup; probar SMS + llamada |
| CPL > $20 MXN | Media | CAC alto | A/B test creativos; ajustar segmentación; pausar Conjunto 2/3 |
| Cliente no registra pedidos en CRM | Alta | Sin ticket real / ROAS | Capacitación 1h + recordatorio diario Panel Web |
| Instagram no crece | Alta | Presupuesto mal gastado | 100% presupuesto a Facebook; IG orgánico solo |

---

## 9. Próximos Pasos para el Cliente

### Lo Que Necesitamos HOY (Mínimo para Arrancar)
1. **Catálogo con precios** → CSV: SKU, Nombre, Precio, Tallas, Stock, Fotos
2. **Número WhatsApp Business** → Debe recibir SMS/llamada para verificación
3. **Accesos Admin** → Meta Business Suite, Instagram, Facebook, GA4/GTM
4. **Confirmación** → Inician verificación Meta Business HOY

### Lo Que Entregamos Esta Semana
- Linktree/landing + WhatsApp API activo
- Flujo OmniRoute D2C funcionando
- Pixel/GA4/GTM + UTM + Panel Web MVP
- Campaña Meta Ads activa ($500/sem)
- CRM plantilla + capacitación 1h

---

## 10. Archivos de Referencia en Repo

| Archivo | Ubicación | Uso |
|---------|-----------|-----|
| Auditoría Marzo 2026 | `tenants/flexi/docs/Flexi monetizacion1/Análisis de la Cuenta...md` | Baseline |
| Calendario 30 días | `tenants/flexi/docs/Flexi monetizacion1/Calendario de Contenido...md` | Content plan listo |
| Mejores prácticas | `tenants/flexi/docs/Flexi monetizacion1/Mejores Prácticas...md` | Horarios, hashtags, formatos |
| Propuesta cliente | `tenants/flexi/docs/Propuesta_Flexi_CRO_Cliente_20261010.md` | Contrato |
| Checklist onboarding | `tenants/flexi/docs/Onboarding_Checklist_Flexi.md` | Qué necesita cliente |

---

**¿Lista para arrancar? En cuanto tengamos catálogo + accesos, Semana 1 operativa.**
