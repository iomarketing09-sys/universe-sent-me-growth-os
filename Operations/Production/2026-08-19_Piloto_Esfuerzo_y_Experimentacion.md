# Piloto de esfuerzo y experimentación por pieza

**Propósito:** Establecer el primer piloto para medir horas, coste y etiquetas de campaña/experimento por publicación, de modo que el Growth OS pueda pasar de `engagement por pieza` a retorno de esfuerzo observado.

**Estado:** Active

**Fecha de creación:** 2026-08-19

**Última actualización:** 2026-08-19

**Versión:** 1.1

**Autor:** Manus AI

**Documentos relacionados:** `../../GrowthOS/08_00_Metricas_Baseline_Plataformas.md`, `../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`, `../Research/2026-08-15_ExperimentLog.csv`, `../Research/2026-08-19_Inventario_Coste_Reels_28D.json`, `2026-08-19_Actualizacion_Asistida_Dashboard_Social.md`, `Piloto_Esfuerzo_y_Experimentacion.csv`.

---

## Objetivo del piloto

El piloto no estima datos de producción. Solo registra esfuerzo observado o supuestos aprobados por Fernando para una cohorte limitada de piezas. La unidad mínima es una publicación por plataforma; si una misma pieza se adapta a varias plataformas, cada adaptación recibe su propia fila cuando el esfuerzo adicional sea significativo.

## Cohorte inicial propuesta

La cohorte operativa recomendada es el experimento existente `EXP-2026-08-CAL-01`, porque ya contiene IDs de publicación, plataforma, formato, tipo de contenido e hipótesis relacionadas. Las piezas que no pertenezcan a un experimento deben registrarse como `Sin_etiqueta_historica`, no recibir una campaña inventada.

## Supuesto aprobado de coste por Reel

Fernando aprobó un coste aproximado de **MX$15 por Reel**. Se registra como `Supuesto_aprobado` y aplica solo a formatos de video identificables dentro del dataset normalizado: `Reel` en Instagram, `Video` en TikTok y `Video / Short` en YouTube. No se aplica a Facebook porque el corte actual no clasifica el formato de sus publicaciones y no debe inferirse.

| Plataforma | Piezas de video elegibles | Engagement observado | Coste asignado | Engagement por MX$ | Ventana de datos |
|---|---:|---:|---:|---:|---|
| Instagram | 14 | 47 | MX$210 | 0.224 | Snapshot actual/lifetime |
| TikTok | 7 | 23 | MX$105 | 0.219 | Snapshot actual/lifetime |
| YouTube | 6 | 31 | MX$90 | 0.344 | Snapshot lifetime por video |

> **Límite de comparabilidad:** este inventario no reconcilia todavía cross-posts del mismo asset entre plataformas. El coste se presenta por publicación de cada canal, no como coste incremental de adaptación ni como ROI total de una sola producción reutilizada. Sin horas observadas, no se calcula engagement por hora.

La evidencia por pieza se conserva en `Operations/Research/2026-08-19_Inventario_Coste_Reels_28D.json`.

## Campos obligatorios

| Campo | Definición | Regla |
|---|---|---|
| `Production_Record_ID` | Identificador único de la fila | Formato `PRD-YYYYMMDD-###`. |
| `Meta_or_Platform_ID` | ID nativo de la publicación | Debe coincidir con un registro de rendimiento. |
| `Platform` | Canal de distribución | Facebook, Instagram, TikTok o YouTube. |
| `Experiment_ID` | Experimento al que pertenece la pieza | Reutilizar ID existente; si no existe, `Sin_etiqueta_historica`. |
| `Campaign_Label` | Nombre operativo aprobado de la campaña | No inferir desde el copy. |
| `Production_Hours` | Horas invertidas en la adaptación publicada | Medida observada o supuesto marcado. |
| `Hourly_Cost` | Coste por hora aplicable | Moneda explícita en `Currency`. |
| `Effort_Status` | Calidad del dato de esfuerzo | `Observado`, `Supuesto_aprobado` o `Pendiente`. |
| `Owner` | Responsable que reporta el esfuerzo | Nombre o rol. |
| `Recorded_At` | Fecha del registro | ISO 8601. |

## Reglas de cálculo

| Métrica | Fórmula | Restricción |
|---|---|---|
| Coste total por pieza | `Production_Hours × Hourly_Cost` | Solo si ambos datos están presentes. |
| Engagement por hora | `Engagement / Production_Hours` | No calcular con horas cero o pendientes. |
| Engagement por coste | `Engagement / Coste total` | No comparar monedas diferentes. |
| Retorno por experimento | Suma de engagement y coste por `Experiment_ID` | Requiere al menos dos piezas con esfuerzo observado. |

> Los resultados de este piloto no deben extrapolarse a todo el catálogo hasta que la cohorte tenga suficientes piezas con datos observados y ventanas de rendimiento comparables.

## Información pendiente de Fernando

Para iniciar la cohorte se requiere confirmar: el coste/hora que se utilizará, el número aproximado de horas por tipo de pieza, la moneda y el nombre de campaña aprobado para las piezas que no tengan `Experiment_ID` existente.
