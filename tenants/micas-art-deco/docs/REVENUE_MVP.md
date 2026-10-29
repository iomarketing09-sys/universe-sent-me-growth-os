# Revenue MVP — Mica's Art & Deco

**Estado:** Implementado el 2026-10-29. **Alcance:** deals manuales y reporte de unit economics. **No es facturación ni contabilidad.** Flexi queda pendiente por decisión de Fernando.

## Regla de reconocimiento

En Mica's el ingreso se reconoce en dos estados:

- **Anticipo:** el cliente dejó un abono. `amount_collected` es el abono recibido.
- **Cobrado:** el cliente liquidó. `amount_collected` es el total recibido.

`pendiente` es un deal sin dinero recibido; `cancelado` queda fuera del ingreso. Al pasar de anticipo a cobrado se **reemplaza** el monto cobrado, no se suma.

## Uso

Registrar una cotización con anticipo:

```bash
python3 tools/revenue_tracker.py add \
  --tenant micas-art-deco \
  --client "Ana" \
  --product "Tulipán en Flor" \
  --quote 500 \
  --status anticipo \
  --collected 250 \
  --source instagram \
  --payment-method transferencia \
  --publication-id 17918653524245845
```

Cerrar el mismo deal como cobrado:

```bash
python3 tools/revenue_tracker.py update D-0001 \
  --tenant micas-art-deco \
  --status cobrado \
  --collected 500 \
  --payment-method efectivo
```

Consultar la cartera:

```bash
python3 tools/revenue_tracker.py list --tenant micas-art-deco
python3 tools/revenue_tracker.py report --tenant micas-art-deco
python3 tools/revenue_tracker.py report --tenant micas-art-deco --json
```

## Campos clave

| Campo | Uso |
|---|---|
| `deal_id` | `D-0001`, consecutivo por tenant. |
| `contact_name` | Nombre del cliente; evitar datos sensibles innecesarios. |
| `product_ref` | Obra vendida: “Tulipán en Flor”, “Sobres pack 10”, etc. |
| `amount` | Monto cotizado. |
| `amount_collected` | Dinero realmente recibido. |
| `payment_status` | `pendiente`, `anticipo`, `cobrado`, `cancelado`. |
| `payment_method` | Transferencia, efectivo, MercadoPago, etc. |
| `source_publication_id` | ID del post que originó el lead, si se conoce. |
| `source_campaign_id` | Campaña de Meta Ads, si aplica. |
| `source_conversation_id` | Conversación de WhatsApp, si se conoce. |
| `lead_source` | Instagram, Facebook, WhatsApp, referido, directo o tienda. |
| `lost_reason` | Motivo de pérdida, para aprender sin inventar. |

## Reporte

El comando `report` devuelve:

- Deals totales, cotizado total y ingreso reconocido.
- Anticipos, cobrado y saldo por cobrar.
- Tasa de cierre y ticket promedio.
- Desglose por origen, producto y estado de pago.

## Almacenamiento y privacidad

`tenants/micas-art-deco/data/deals_micas-art-deco.csv` está **gitignored** porque contiene nombres y datos de clientes. El código y la documentación sí se versionan; el ledger local no.

## Pendiente

- Conectar WhatsApp → deal automáticamente, con confirmación humana.
- Conectar Meta Ads → CAC/ROAS por campaña.
- Reporte cross-tenant cuando Flexi defina su regla de revenue.
