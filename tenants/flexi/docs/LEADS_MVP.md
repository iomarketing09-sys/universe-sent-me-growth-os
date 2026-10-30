# Leads y nivel de intención — Flexi

**Estado:** MVP implementado el 2026-10-30. **Alcance:** registrar conversaciones y su intención. **Ventas:** pendientes; todavía no hay datos de cierre.

## Regla de intención

La intención la asigna una persona al leer la conversación. No se infiere automáticamente.

| Nivel | Señales |
|---|---|
| **Frío** | Pregunta general, no da talla ni producto, no responde las preguntas de calificación. |
| **Tibio** | Pregunta por precio, talla o disponibilidad; responde al menos una pregunta clave. |
| **Caliente** | Pide apartar o comprar, da talla y forma de pago, pregunta por sucursal o envío. |

## Estados

`nuevo` → `contactado` → `calificado` → `cotizado` → `cita_agendada` → `ganado` / `perdido`.

`ganado` en un lead significa que la conversación avanzó a compra, no que el dinero esté registrado. El cobro se lleva en Revenue cuando exista.

## Origen

Usa el origen real de la conversación:

- `whatsapp` para la campaña Click-to-WhatsApp.
- `facebook` o `instagram` para DM.
- `meta_ads` si el lead llega por formulario o campaña sin mensaje.
- `tienda` para visitas presenciales.

Si conoces la campaña o el post, guárdalos en `--campaign-id` y `--publication-id`. Eso permite cruzar leads con las 80 conversaciones de Ads.

## Uso diario

```bash
python3 tools/lead_tracker.py add --tenant flexi \
  --name "Cliente" --phone "8781234567" --source whatsapp \
  --intent caliente --interest "Botines Quirelli" \
  --campaign-id 2026-10_flexi_ads_500mxn \
  --conversation-id "<id del hilo>" \
  --next-action-at 2026-10-31

python3 tools/lead_tracker.py list --tenant flexi --intent caliente
python3 tools/lead_tracker.py report --tenant flexi
```

## Qué mide

- Volumen de leads por origen e intención.
- Cuántos avanzan a cotización y cita.
- Seguimientos vencidos.
- Tasa de contacto, cotización y cita.

No mide revenue ni CAC todavía. Eso llega cuando existan ventas y se conecte Ads.

## Pendiente

- Cargar los leads históricos de la campaña de octubre.
- Definir quién captura los leads y con qué frecuencia.
- Conectar WhatsApp y DM para crear leads con confirmación humana.
