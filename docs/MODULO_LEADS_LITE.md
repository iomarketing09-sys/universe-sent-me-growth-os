# Módulo Leads Lite

Registra conversaciones y nivel de intención antes de que exista una venta. No es un CRM completo ni un pipeline de revenue: es la capa que evita perder leads cuando todavía no hay montos ni cierres.

## Por qué existe

Un deal responde “¿cuánto vendimos?”. Un lead responde “¿cuánta gente nos escribió, de dónde vino y qué tan cerca está de comprar?”. Sin esa capa, las conversaciones de Ads y WhatsApp se pierden y no se puede calcular el costo por lead ni la tasa de avance.

## Modelo

`Lead` en `core/growthos-core/growthos/core/models.py`.

| Campo | Uso |
|---|---|
| `lead_id` | `L-0001`, consecutivo por tenant. |
| `tenant_id` | Aislamiento por tenant. |
| `contact_name`, `contact_phone`, `contact_email` | Identificación mínima. |
| `lead_source` | WhatsApp, Facebook, Instagram, Meta_Ads, referido, directo o tienda. |
| `intent` | `frio`, `tibio`, `caliente`. |
| `status` | `nuevo`, `contactado`, `calificado`, `cotizado`, `cita_agendada`, `ganado`, `perdido`. |
| `product_interest` | Producto o tema de interés. |
| `budget_range` | Rango declarado por el cliente, si lo dio. |
| `source_publication_id` | Post que originó el lead. |
| `source_campaign_id` | Campaña de Ads. |
| `source_conversation_id` | Hilo de WhatsApp o DM. |
| `next_action_at` | Fecha de seguimiento. |
| `lost_reason` | Motivo de pérdida. |

Un lead necesita al menos nombre, teléfono, email o ID de conversación.

## CLI

```bash
python3 tools/lead_tracker.py add --tenant flexi \
  --name "Cliente" --phone "8781234567" --source whatsapp \
  --intent caliente --interest "Botines Quirelli" \
  --campaign-id 2026-10_flexi_ads_500mxn \
  --next-action-at 2026-10-31

python3 tools/lead_tracker.py update L-0001 --tenant flexi \
  --status cotizado --intent caliente

python3 tools/lead_tracker.py list --tenant flexi --intent caliente
python3 tools/lead_tracker.py report --tenant flexi --json
```

## Reporte

Devuelve leads totales, calientes/tibios/fríos, abiertos, ganados, perdidos, nuevos en los últimos 7 días, seguimientos vencidos y tasas de contacto, cotización, cita y cierre. También desglose por intención, origen y estado.

## Privacidad

`tenants/<tenant>/data/leads_<tenant>.csv` está **gitignored** porque contiene datos de clientes.

## Fuera de alcance

- No infiere intención automáticamente: la asigna una persona.
- No calcula revenue ni CAC. Para eso está `MODULO_REVENUE_LITE.md`.
- No sincroniza con WhatsApp todavía; el registro es manual o por script.
