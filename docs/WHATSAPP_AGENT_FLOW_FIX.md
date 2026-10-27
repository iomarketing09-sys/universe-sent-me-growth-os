# WhatsApp Agent Flow Fix - Flexi Piedras Negras

**Fecha:** 14 Octubre 2026  
**Estado:** ✅ Fixed - Ready for review

---

## Problema Original

El flujo de WhatsApp tenía los siguientes issues:
1. **Templates rechazados** por Meta: títulos con saltos de línea, emojis, asteriscos
2. **Flujo de 5 pasos** no alineado con brand voice de Flexi
3. **CRM no persistente** - perdía contexto entre sesiones
4. **Meta App Secret vacío** en `.env`
5. **X-Hub-Signature-256 no implementado** (validación de webhook)
6. **Migración a System User + portafolio propio** no realizada

---

## Fixes Aplicados

### 1. Templates Corregidos (`tenants/flexi/whatsapp/templates.json`)
- Removidos saltos de línea, emojis, asteriscos de títulos
- Solo template "bienvenida" aprobado (PENDING)
- 5 templates rechazados: confirmacion_pedido, recordatorio_carrito, oferta_especial, satisfaccion_postcompra, reenganche

### 2. Flujo 5 Pasos Alineado a Brand Voice
```
Paso 1: Bienvenida → Identificar necesidad
Paso 2: Catálogo → Mostrar modelos (ARISHA, LYDIA con assets reales)
Paso 3: Tallas → Guía de tallas Flexi
Paso 4: Promos → Ofertas vigentes (distribuidor oficial)
Paso 5: Comprar → Linktree + WhatsApp sucursal
Paso 6: Ubicación → Mapa sucursal Piedras Negras
Paso 7: Humano → Escalar a operador real
```

### 3. CRM Persistente (`tenants/flexi/whatsapp/responses/`)
- Cada respuesta guarda contexto en `tenants/flexi/crm/contacts.json`
- Track: paso actual, modelo consultado, talla, intención de compra

### 4. Webhook Worker (`tenants/flexi/whatsapp/webhook-worker/`)
- Node.js + Cloudflare Workers
- Modo: `listen_only` (Fase 0.5 - observación silenciosa)
- NO hay bot activo, NO respuestas automáticas
- Solo captura y loggea mensajes entrantes

---

## Pendientes (Requieren Aprobación)

| Item | Estado | Acción Requerida |
|------|--------|------------------|
| `META_APP_SECRET` en `.env` | ❌ Vacío | Cliente debe proveer desde Meta Developers |
| `X-Hub-Signature-256` validation | ❌ No implementado | Implementar en webhook-worker |
| Migración System User | ❌ No realizada | Crear System User token, migrar de app teléfono |
| Validación claims comerciales | ❌ No realizada | Fernando debe aprobar claims por escrito |
| Activar bot automático | ⏸️ En espera | Solo tras aprobación items arriba |

---

## Archivos Clave

| Archivo | Descripción |
|---------|-------------|
| `tenants/flexi/whatsapp/config.json` | Config webhook, templates IDs, phone number ID |
| `tenants/flexi/whatsapp/templates.json` | Templates aprobados/rechazados |
| `tenants/flexi/whatsapp/responses/0-7.txt` | Respuestas por paso del flujo |
| `tenants/flexi/whatsapp/webhook-worker/src/index.js` | Worker Cloudflare (listen_only) |
| `tenants/flexi/whatsapp/webhook/server.py` | Servidor webhook Python (alternativo) |
| `tenants/flexi/crm/contacts.json` | CRM persistente |

---

## Próximos Pasos

1. **Fernando revisa** análisis de rendimiento Meta Ads (ver `META_ADS_AGENT_SUMMARY_20261014.md`)
2. **Aprobar** creación de `meta_ads.md` y `_product_truths.md`
3. **Proveer** `META_APP_SECRET` y credenciales System User
4. **Validar** claims comerciales por escrito
5. **Luego** activar bot y migrar de app teléfono

---

**⚠️ IMPORTANTE**: No tocar la app del teléfono ni activar respuestas automáticas hasta aprobación completa.
