# Campaña Pinos de Autor 2026 — Mica's Art & Deco

**Canal:** orgánico (Facebook, Instagram, TikTok) + reactivación 1:1.
**Plaza:** Piedras Negras, Coahuila.
**Ventana de montajes:** lunes 9 de noviembre al viernes 18 de diciembre de 2026.
**Objetivo:** 14 montajes agendados con anticipo del 50%.
**Campaña en el tracker:** `pinos-2026`.

## Oferta

| Línea | Alcance | Precio final |
|---|---|---|
| Restyling Mediano | Hasta 1.90 m, adornos del cliente | $1,800 |
| Restyling Estándar | 2.10–2.20 m, adornos del cliente | $2,100 |
| Restyling Grande / Monumental | 2.40–2.70 m o más, adornos del cliente | $2,500 |
| Transformación Total VIP | Diseño y montaje integral | Desde $3,200 |
| Pinos Comerciales | Clínicas, spas, notarías, boutiques | $3,500–$5,000 |

**El pino lo pone el cliente.** Si lo pide, se cotiza aparte el pino con adornos y luces.

Incluye: diagnóstico, diseño, montaje y ajuste final.
No incluye salvo cotización aparte: pino, luces nuevas, adornos fuera de inventario, traslado fuera de Piedras Negras y desmontaje.

## Reglas de comunicación

- **Los precios no se publican en el copy.** Se dan en DM o WhatsApp.
- **La política de anticipo y no reembolso no se publica.** Se explica en la conversación, antes de cobrar.
- No se promete disponibilidad que no exista. La escasez se comunica solo con fechas reales.
- Tono cálido y artístico; sin claims tipo “mejor del mercado” ni “garantizado”.
- CTA único: DM o WhatsApp **878 101 2084**.

## Capacidad real

- 1 montaje por día.
- Horarios: 10:00 o 16:00, solo uno por día.
- Solo lunes a viernes.
- 30 días hábiles en la ventana.
- 3 días no vendibles: 1 dic (apartado), 16 dic (no disponible), 18 dic (apartado).
- **27 fechas vendibles.**

Detalle en `CAPACIDAD_MONTAJES.csv`.

## Embudo y metas

Supuestos a validar con datos reales de las primeras dos semanas:

| Etapa | Tasa supuesta | Para 14 ventas |
|---|---|---|
| Conversaciones iniciadas | — | ~134 |
| DM calificado (responde las 4 preguntas) | 50% | ~67 |
| Cotización enviada | 60% | ~40 |
| Cita con anticipo | 35% | 14 |

Con 2.2K seguidores en Facebook el volumen no sale solo de contenido. El plan reparte la meta:

| Fuente | Acción | Montajes esperados |
|---|---|---|
| Reactivación 1:1 | 40–60 clientas históricas por WhatsApp | 5–8 |
| Orgánico | 13 feeds, 4 reels, historias diarias | 4–6 |
| Referidos y aliados | 6–8 floristerías, mueblerías, inmobiliarias | 2–3 |

## Escenarios financieros

| Escenario | Montajes | Bruto | Anticipos 50% |
|---|---|---|---|
| Conservador | 8 | ~$18,700 | ~$9,350 |
| Base | 12 | ~$31,600 | ~$15,800 |
| Objetivo | 14 | ~$40,600 | ~$20,300 |

Las cifras son ingreso bruto. El neto depende de materiales, traslado y horas de montaje, que aún no están costeados.

## KPIs semanales

Se capturan en `KPIS_SEMANALES.csv`:

- Alcance y guardados por publicación.
- DMs y conversaciones iniciadas.
- Cotizaciones enviadas.
- Citas agendadas y anticipos cobrados.
- Montajes realizados y show rate.
- Ticket promedio y revenue reconocido.

CAC orgánico = costo de contenido y horas ÷ montajes. No se reporta como cero.

## Operación en el tracker

Al agendar:

```bash
python3 tools/revenue_tracker.py add --tenant micas-art-deco \
  --client "Cliente" --product "Restyling Estándar" --quote 2100 \
  --status anticipo --collected 1050 --source facebook \
  --stage cita --appointment-at 2026-11-17 \
  --campaign-id pinos-2026 --conversation-id "<id del DM>"
```

Al instalar:

```bash
python3 tools/revenue_tracker.py update D-0001 --tenant micas-art-deco \
  --status cobrado --collected 2100
```

El reporte calcula citas totales, próximas, pasadas y show rate.

## Decisiones pendientes

1. ¿El desmontaje de enero está incluido o se cobra aparte?
2. ¿Las luces están incluidas en Restyling o solo se colocan las del cliente?
3. Radio de traslado incluido en Piedras Negras.
4. ¿Se ofrece descuento por dos o más pinos en el mismo domicilio? Recomendación: no descontar; cobrar el segundo a precio completo con montaje el mismo día.
5. ¿Existe inventario de adornos suficiente para 5–8 Transformaciones VIP?
