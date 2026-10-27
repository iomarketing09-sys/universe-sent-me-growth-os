# Módulo Revenue Lite (Unit Economics)

Cierra el hueco entre **conversación** (`dm_cotizacion`) y **resultado económico** (venta real).
Scope mínimo y evolutivo: **deals + reporte de unit economics**. NO es facturación ni contabilidad.

---

## Flujo Revenue Lite (physical_cro)

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    REVENUE LITE - FLUJO (physical_cro)                     │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  Lead entra (WhatsApp / Meta / GBP)                                      │
│       │                                                                    │
│       ▼                                                                    │
│  tools/revenue_tracker.py add                                            │
│       • Deal_ID (D-0001) · Cliente · Lead_Source · Linea                 │
│       • Monto_Cotizado · Costo_Produccion · Costo_Adquisicion (CAC)      │
│       │                                                                    │
│       ▼                                                                    │
│  tools/revenue_tracker.py update <id> --cerrado <monto>                  │
│       • Etapa → Cerrado Ganado / Cerrado Perdido                         │
│       │                                                                    │
│       ▼                                                                    │
│  tools/revenue_tracker.py report                                         │
│       • Ticket promedio · Tasa de cierre · Margen % · CAC · ROAS         │
│       • Desglose por Línea y por Origen de lead                          │
│                                                                            │
│  STORAGE: tenants/{tenant}/data/deals_{tenant}.csv  (multi-tenant)       │
│  MODELO:  core/growthos-core/core/models.py :: Deal                      │
│  DOC:     docs/MODULO_REVENUE_LITE.md                                    │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Especificación Técnica

| Aspecto | Detalle |
|---------|---------|
| **Modelo** | `Deal` (core/growthos-core) |
| **Enums** | `LeadSource`, `DealStage`, `FunnelLine` |
| **Repo** | `DealRepository` (upsert por `Deal_ID`, aislamiento por tenant) |
| **CLI** | `tools/revenue_tracker.py` → `add` · `update` · `list` · `report` |
| **Objetivos** | `unit_economics` en `tenants/{tenant}/config.json` (metas internas a validar) |
| **Estado** | 🟢 Operativo — 6 tests en `core/growthos-core/tests/` |
| **Fuera de scope** | Facturación, CFDI, cobros, P&L |

---

## Roadmap

1. ✅ **MVP**: Deals + unit economics básicos (operativo)
2. 🔄 **Auto-registro** desde WhatsApp Agent
3. 🔄 **Atribución CAC** desde Meta Ads
4. 🔄 **Ingesta de pagos** (Stripe, transferencias, efectivo)
5. 🔄 **Reporte cross-tenant** consolidado

---

## Estructura de Datos

### Deal (modelo)
```python
class Deal(BaseModel):
    Deal_ID: str                    # D-0001
    tenant_id: str                  # flexi, la-cupula, etc.
    Cliente: str
    Lead_Source: LeadSource         # WHATSAPP, META_ADS, GBP, ORGANIC, REFERRAL
    Linea: FunnelLine               # VENTA_DIRECTA, B2B, CAPACITACION, etc.
    Monto_Cotizado: float
    Costo_Produccion: float
    Costo_Adquisicion: float        # CAC
    Etapa: DealStage                # NUEVO, EN_CONTACTO, COTIZADO, CERRADO_GANADO, CERRADO_PERDIDO
    Fecha_Creacion: datetime
    Fecha_Cierre: Optional[datetime]
    Monto_Final: Optional[float]
    Notas: str
```

### Enums
```python
class LeadSource(str, Enum):
    WHATSAPP = "whatsapp"
    META_ADS = "meta_ads"
    GBP = "gbp"
    ORGANIC = "organic"
    REFERRAL = "referral"

class DealStage(str, Enum):
    NUEVO = "nuevo"
    EN_CONTACTO = "en_contacto"
    COTIZADO = "cotizado"
    CERRADO_GANADO = "cerrado_ganado"
    CERRADO_PERDIDO = "cerrado_perdido"

class FunnelLine(str, Enum):
    VENTA_DIRECTA = "venta_directa"
    B2B = "b2b"
    CAPACITACION = "capacitacion"
    OTRO = "otro"
```

---

## CLI Usage

```bash
# Agregar deal
python3 tools/revenue_tracker.py add \
  --tenant flexi \
  --cliente "Juan Perez" \
  --lead-source whatsapp \
  --linea venta_directa \
  --monto-cotizado 5000 \
  --costo-produccion 3000 \
  --costo-adquisicion 500

# Actualizar deal
python3 tools/revenue_tracker.py update D-0001 --cerrado 4800

# Reporte
python3 tools/revenue_tracker.py report --tenant flexi
```

---

## Reportes Generados

El comando `report` genera:
- **Ticket promedio** por línea
- **Tasa de cierre** (%)
- **Margen %** (Monto_Final - Costo_Produccion - CAC) / Monto_Final
- **CAC** promedio por lead source
- **ROAS** por canal
- **Desglose** por Línea y Origen de lead

---

*Actualizado: 15 Octubre 2026*
