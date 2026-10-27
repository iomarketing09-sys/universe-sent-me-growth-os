# 01 — Brief (propuesta para Gate 1)

**Campaña:** `2026-10_flexi_ads_500mxn` · **Estado:** borrador para aprobación
**Autor:** CGO · **Fecha:** 2026-10-16

---

## Contexto

Flexi es distribuidor oficial de la marca en Piedras Negras. Para la campaña OI26 solo hay
**5 modelos con asset aprobado** (`142801`, `142901`, `143001`, `143201`, `306703`). La sucursal
atiende WhatsApp desde la app del teléfono (coexistencia, sin bot) y hoy está en observación
silenciosa de su propia voz.

## Objetivo de negocio

Conseguir **conversaciones de WhatsApp con intención real** (preguntar por un modelo, talla o
visita a tienda) y aprender **qué ángulo creativo** las produce al menor costo.

No es una campaña de rentabilidad ni de escala: con 500 MXN no se sale de la fase de aprendizaje.
Es una **prueba de mensaje y audiencia** con una ventana de 7 días.

## KPI y umbral

| Métrica | Meta | Cómo se mide |
|---|---|---|
| Conversaciones iniciadas | ≥14 en 7 días | Ads Manager (CTWA) |
| Costo por conversación | ≤35 MXN | Gasto / conversaciones |
| CTR | ≥0.8 % | Ads Manager |
| Tiempo a primera respuesta | <15 min en horario | Worker: `in` → siguiente `out_app` |
| Calidad del lead | ≥50 % menciona modelo, talla o visita | Muestreo manual de conversaciones |

**Regla de corte a 72 h:** si el CPA supera 60 MXN o el CTR cae por debajo de 0.5 %, se pausa y
se revisa antes de seguir gastando. No se toca nada antes de 72 h salvo rechazo de anuncios.

## Oferta y mensaje

**No hay promoción válida.** El cliente respondió **No** a los cuatro claims propuestos:
2×1, meses sin intereses, envío gratis >$1,200 y 15 % de cumpleaños. Por lo tanto:

- El mensaje se apoya en **distribuidor oficial**, **comodidad** y **asesoría de talla**.
- **Prohibido** mencionar precio, descuento, promoción, envío gratis, meses o disponibilidad.
- La acción es "mándanos mensaje y te asesoramos", no "compra ahora".

## Público

Mujeres de 28 a 55 años **solo en Piedras Negras, Coahuila** (ciudad, sin radio de ampliación).
Detalle y rationale en `02_audiencia.md`.

## Restricciones

1. Inventario **parcial**: nunca afirmar stock, talla o color disponible.
2. Claims rechazados por el cliente: no volver a usarlos sin una validación nueva y por escrito.
3. Solo los 5 modelos aprobados + material de marca.
4. Sin bot: la sucursal contesta desde la app. Si no puede sostener <15 min, la campaña se pausa.
5. Sin publicar hasta que exista cuenta publicitaria de Flexi y autorización de gasto (G3).

## Presupuesto y ventana

| Dato | Valor |
|---|---|
| Presupuesto total | **500 MXN** |
| Tipo | Lifetime (nunca se excede el total) |
| Duración | **7 días** |
| Gasto diario equivalente | **71.43 MXN/día** |
| Inicio | Por definir (primer lunes hábil tras G3) |
| Fin | Inicio + 7 días |

## Hipótesis a probar

1. El ángulo de **comodidad** (beneficio directo) supera a **prueba social** en CTR y costo por conversación.
2. Una audiencia **amplia** (geo + edad + género, sin intereses) entrega mejor que una segmentación
   estrecha con este presupuesto.
3. El cuello de botella será el **tiempo de respuesta humana**, no la entrega del anuncio.

## Fuera de alcance

- Retargeting y lookalike: no hay volumen suficiente para alimentarlos.
- Ventas directas, catálogo o tienda Meta: el objetivo es conversación, no checkout.
- Escalar presupuesto o prometer ROAS.
- Promociones, precio y disponibilidad.
