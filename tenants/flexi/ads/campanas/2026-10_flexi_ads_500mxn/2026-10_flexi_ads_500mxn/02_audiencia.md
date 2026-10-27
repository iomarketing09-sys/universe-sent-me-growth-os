# 02 — Audiencia (propuesta para Gate 1)

**Campaña:** `2026-10_flexi_ads_500mxn` · **Estado:** borrador para aprobación

---

## Segmentación base

| Dimensión | Valor | Rationale |
|---|---|---|
| Ubicación | **Piedras Negras, Coahuila, México (ciudad)** | Indicación del cliente (2026-10-16): no ampliar a municipios vecinos |
| Radio | **Sin radio** | Solo la ciudad; excluye Eagle Pass y cualquier zona de EE. UU. |
| Edad | 28–55 años | Núcleo de clientas actuales (61.7 % mujeres 35–54 en la auditoría) |
| Género | Mujeres | Los 5 modelos aprobados son línea femenina |
| Intereses | **Ninguno (amplia)** | Con 71 MXN/día, los intereses fragmentan la entrega; el creativo es la variable del test |
| Exclusiones | Ninguna | No hay audiencias propias con volumen todavía |
| Tamaño estimado | Por confirmar en Ads Manager (esperado 20k–45k) | Se valida al crear el ad set |

## Estrategias evaluadas

| Estrategia | Tamaño | Presupuesto | ¿Se usa? | Motivo |
|---|---|---|---|---|
| **Amplia (ciudad + edad + género)** | 20k–45k | **100 %** | **Sí** | Máxima entrega dentro de Piedras Negras con una sola variable: el creativo |
| Core con intereses | Menor | 0 % | No | Fragmenta la entrega y compite con el algoritmo |
| Lookalike 1 % | Insuficiente | 0 % | No | No hay base de compradores ni volumen para sembrarla |
| Retargeting 30 d | Muy pequeña | 0 % | No | Requiere píxel/CTWA con historial; hoy no existe |

## Configuración de entrega

| Dato | Valor |
|---|---|
| Objetivo | Mensajes a WhatsApp (Click-to-WhatsApp) |
| Optimización | Conversaciones iniciadas |
| Puja | `LOWEST_COST_WITHOUT_CAP` |
| Ubicaciones | Advantage+ automático, **excluyendo Audience Network** |
| Ventana de atribución | 7 días por clic / 1 día por vista |
| Horario | Solo horario de tienda: Lun–Vie 9–20, Sáb 10–19, Dom 11–17 |

## Notas

- **Dayparting:** el anuncio solo corre cuando hay quien conteste. Si la sucursal no puede cubrir
  un día, se excluye ese día en el ad set.
- **Sin intereses:** si a las 72 h la entrega es pobre (CPM alto, alcance bajo), se prueba una
  segunda versión con 3 intereses (calzado, moda, compras online) como ajuste, no como nuevo test.
- **Un solo ad set:** repartir 500 MXN en varios conjuntos impide que cualquiera salga de learning.
- La estimación de tamaño es preliminar; Meta la calcula al crear el conjunto.
