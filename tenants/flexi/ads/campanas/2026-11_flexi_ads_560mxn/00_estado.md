# 00 — Estado de la campaña

| Campo | Valor |
|---|---|
| Campaña | Flexi OI26 — continuación |
| Slug | `2026-11_flexi_ads_560mxn` |
| Estado | **ACTIVA en Meta desde 2026-10-30 17:36 CDT** |
| Presupuesto | **560 MXN** lifetime, a nivel campaña (CBO) |
| Duración | 6 días |
| Inicio real | 2026-10-30 17:36 CDT |
| Fin real | 2026-11-05 16:19 CST |
| Objetivo | Mensajes a WhatsApp (Click-to-WhatsApp) |
| Cuenta publicitaria | `act_965886593249554` |
| Página / Instagram | Zapateria Flexi Piedras Negras / `@zapateriaflexipn` |
| KPI principal | Costo por conversación |

## Cierre de la campaña anterior

`2026-10_flexi_ads_500mxn` quedó **pausada** el 2026-10-30.

| Métrica | Valor |
|---|---|
| Gasto | 439.28 MXN |
| Presupuesto | 500.00 MXN |
| Remanente | 60.72 MXN |
| Impresiones | 12,772 |
| Alcance | 6,653 |
| Clics | 999 |
| CTR | 7.82% |
| CPC | 0.44 MXN |
| Conversaciones | 80 |
| Costo por conversación | 5.49 MXN |

### Rendimiento por anuncio

| Anuncio | Gasto | Clics | CTR | Conversaciones | Costo / conversación |
|---|---|---|---|---|---|
| ARISHA (306703) | 137.16 | 440 | 9.95% | 33 | **4.16** |
| LYDIA (143201) | 77.03 | 155 | 10.22% | 18 | **4.28** |
| ISAURA (142801) | 221.65 | 400 | 5.89% | 41 | 5.41 |
| ARISHA (duplicado) | 3.44 | 4 | 9.30% | 1 | 3.44 |

**Lectura:** ARISHA y LYDIA son las más eficientes por conversación. ISAURA dio volumen pero a mayor costo. La nueva campaña prioriza las eficientes y prueba las llegadas nuevas con presupuesto menor.

## Creativos y assets

| Creativo | Modelo | Marca | Color | Asset | Formato |
|---|---|---|---|---|---|
| ARISHA | 306703 | Quirelli | Nude | `assets/ad_arisha_306703.jpg` | 1080×1350, 238 KB |
| LYDIA | 143201 | Flexi | Negro | `assets/ad_lydia_143201.jpg` | 1080×1350, 258 KB |
| IZADORA | 142601 | Flexi | Tan | `assets/ad_izadora_142601.jpg` | 1080×1350, 153 KB |
| AMALIA | 307001 | Quirelli | Taupe | `assets/ad_amalia_307001.jpg` | 1080×1350, 244 KB |

## Distribución

Un solo ad set con los cuatro anuncios y 560 MXN lifetime. Meta reparte el presupuesto y aprende más rápido que con cuatro ad sets fragmentados.

## Audiencia

- Piedras Negras, Coahuila. Personas que viven en la ciudad, sin radio ampliado.
- Mujeres, 25 a 55 años.
- Idioma español.
- Segmentación detallada: ninguna.
- Ubicaciones automáticas de Meta.
- Destino: solo WhatsApp (+52 878 138 5284).

### Diferencia con la campaña anterior

El ad set anterior tenía radio de 80 km, edad 18–65 y mensajería multi-destino, aunque el config aprobado decía sin radio y 28–55. Esta campaña respeta el criterio aprobado y concentra el alcance para poder medir.

## Reglas

- Sin precios, descuentos, stock, “disponible”, “apartado”, “garantizado” ni superlativos.
- CTA a WhatsApp.
- Si un creativo supera 8 MXN por conversación a los 3 días, se pausa y se redistribuye su presupuesto.

## IDs publicados

| Objeto | ID |
|---|---|
| Campaña | `120247658527630665` |
| Ad set (recreado) | `120247659400770665` |
| ARISHA | `120247659400780665` |
| LYDIA | `120247659400800665` |
| IZADORA | `120247659400810665` |
| AMALIA | `120247659400790665` |

Detalle completo en `meta_ids.json`.

## Correcciones aplicadas (2026-10-30)

El ad set se recreó para cambiar el destino. Nuevo ID: `120247659400770665`.

El `2026-10-30 23:18 -05` se reconcilió `campaign.json.published.adset_id` del
ID anterior `120247658527640665` al ID activo `120247659400770665`. La lectura
de Meta confirmó que el ad set pertenece a la campaña `120247658527630665`.

| Campo | Spec | Estado |
|---|---|---|
| Destino | Solo WhatsApp | ✅ `WHATSAPP` |
| Radio | Solo Piedras Negras | ✅ Sin radio |
| Idioma | Español | ✅ Locale 23 |
| Edad | 25–55 | ⚠️ Editada en UI; la API aún reporta 18–65 |
| Tipo de ubicación | Solo residentes | Aceptado tal cual: incluye “pasan frecuentemente” y “estuvieron recientemente” |

Los textos y los cuatro creativos coinciden con el spec. Los anuncios están en revisión (`PENDING_REVIEW` / `IN_PROCESS`).

## Pendiente

1. Confirmar en la UI que la edad quedó en 25–55 (la API aún muestra 18–65).
2. Confirmar que el locale 23 sea español de México.
3. Revisar el reporte automático de 48 h programado para `2026-11-01 16:36 CST` (48 horas reales desde el inicio).

Configuración cerrada por decisión de Fernando el 2026-10-30.
