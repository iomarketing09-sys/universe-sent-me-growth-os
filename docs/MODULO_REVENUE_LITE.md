# Módulo Revenue Lite (Unit Economics)

Cierra el hueco entre **conversación** y **resultado económico**. El alcance es
deals y unit economics; **no** es facturación, CFDI, cobros ni contabilidad.

## Estado real (2026-10-29)

- **Mica's Art & Deco:** MVP implementado con CSV + CLI. Reconoce ingreso en
  `anticipo` y `cobrado`.
- **Flexi:** pendiente por decisión de Fernando.
- El modelo `Deal`, la tabla `deals`, el `DealRepository` y el CLI existen.
- El almacenamiento operativo del MVP es un CSV por tenant:
  `tenants/<tenant>/data/deals_<tenant>.csv`.
- El CSV está gitignored porque contiene datos de clientes.

## Flujo

```text
Post / anuncio / referido
        |
        v
Conversación (WhatsApp, Instagram, Facebook)
        |
        v
Deal: cotizado
        |
        +--> anticipo  -> amount_collected = abono recibido
        |
        +--> cobrado   -> amount_collected = total recibido
        |
        +--> cancelado -> fuera del ingreso
        |
        v
Reporte: anticipos + cobrado, saldo, cierre, ticket, CAC y ROAS
```

## Regla de reconocimiento

`amount` es el monto cotizado. `amount_collected` es el dinero realmente
recibido.

| `payment_status` | Ingreso reconocido | `amount_collected` |
| --- | --- | --- |
| `pendiente` | No | 0 |
| `anticipo` | Sí, por el abono | Abono recibido |
| `cobrado` | Sí, por el total | Total recibido |
| `cancelado` | No | Lo que se haya registrado, fuera del reporte |

Al pasar de `anticipo` a `cobrado` se **reemplaza** `amount_collected` con el
total. No se suman el anticipo y el cobrado, para evitar doble conteo.

## Componentes

| Aspecto | Implementación |
| --- | --- |
| Modelo | `Deal` en `core/growthos-core/growthos/core/models.py` |
| Enums | `LeadSource`, `DealStage`, `FunnelLine`, `PaymentStatus` |
| Repositorio SQLite | `DealRepository` en `growthos/storage/repositories.py` |
| Migración | `002_deals_revenue_fields.sql` |
| Store del MVP | `RevenueStore` en `modules/intelligence/revenue.py` |
| CLI | `tools/revenue_tracker.py` → `add`, `update`, `list`, `report` |
| Storage | `tenants/<tenant>/data/deals_<tenant>.csv` |
| Tests | `tests/test_revenue.py` |

## Campos del Deal

| Campo | Uso |
| --- | --- |
| `deal_id` | `D-0001`, consecutivo por tenant. |
| `tenant_id` | Aislamiento por tenant. |
| `lead_source` | Instagram, Facebook, WhatsApp, Meta_Ads, referido, directo o tienda. |
| `deal_stage` | New, Qualified, Proposal, Negotiation, Appointment_Scheduled, Closed_Won, Closed_Lost. |
| `funnel_line` | TOFU, MOFU o BOFU. |
| `product_ref` | Obra, modelo o pack vendido. |
| `amount` | Monto cotizado. |
| `amount_collected` | Dinero realmente recibido. |
| `payment_status` | Pendiente, anticipo, cobrado o cancelado. |
| `payment_method` | Transferencia, efectivo, MercadoPago, etc. |
| `payment_date` | Fecha del abono o cobro. |
| `appointment_at` | Fecha de cita o montaje; base del show rate. |
| `source_publication_id` | Post que originó el lead, si se conoce. |
| `source_campaign_id` | Campaña de Meta Ads, si aplica. |
| `source_conversation_id` | Conversación o DM (Facebook, Instagram, WhatsApp), si se conoce. |
| `contact_name`, `contact_phone`, `contact_email` | Datos mínimos de contacto. |
| `notes`, `lost_reason` | Contexto y motivo de pérdida. |

## CLI

```bash
# Registrar cotización con anticipo
python3 tools/revenue_tracker.py add \
  --tenant micas-art-deco \
  --client "Ana" \
  --product "Tulipán en Flor" \
  --quote 500 \
  --status anticipo \
  --collected 250 \
  --source instagram \
  --payment-method transferencia

# Agendar montaje/cita
python3 tools/revenue_tracker.py add \
  --tenant micas-art-deco \
  --client "Ana" \
  --product "Restyling Estándar" \
  --quote 2100 \
  --status anticipo \
  --collected 1050 \
  --stage cita \
  --appointment-at 2026-11-17 \
  --campaign-id pinos-2026

# Pasar a cobrado; se reemplaza el monto, no se suma
python3 tools/revenue_tracker.py update D-0001 \
  --tenant micas-art-deco \
  --status cobrado \
  --collected 500

# Consultar
python3 tools/revenue_tracker.py list --tenant micas-art-deco
python3 tools/revenue_tracker.py report --tenant micas-art-deco
python3 tools/revenue_tracker.py report --tenant micas-art-deco --json
```

## Reporte

El comando `report` devuelve:

- Deals totales, cotizado total e ingreso reconocido.
- Anticipos, cobrado y saldo por cobrar.
- Tasa de cierre y ticket promedio.
- Desglose por origen, producto y estado de pago.

## Roadmap

1. ✅ MVP CSV + CLI con anticipo/cobrado.
2. 🔄 Auto-registro desde DM/WhatsApp con confirmación humana.
3. 🔄 Atribución de CAC desde Meta Ads.
4. 🔄 Reporte cross-tenant cuando Flexi defina su regla.
5. 🔄 Ingesta de pagos (transferencia, efectivo, MercadoPago).

## Fuera de alcance

Facturación, CFDI, conciliación bancaria, P&L y cobros automáticos.
