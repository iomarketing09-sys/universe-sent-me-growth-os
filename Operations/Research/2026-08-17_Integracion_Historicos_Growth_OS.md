---
title: "Integración de históricos estadísticos al Growth OS"
purpose: "Determinar qué datos de mayo, junio y julio ya están documentados, qué falta estructurar y cómo incorporar la evidencia histórica sin mezclar métricas, ventanas ni canales incompatibles."
status: "Review"
created: 2026-08-17
updated: 2026-08-17
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "GrowthOS/08_00_Metricas_Baseline_Plataformas.md"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
  - "Operations/Research/2026-08-08_Reporte_Mensual_Junio_Julio_2026.md"
  - "Operations/Research/2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto.md"
  - "Operations/Research/2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv"
  - "Operations/Memories/mayo_2026_top_posts_metaBS.md"
  - "Operations/Memories/agosto_2026_analisis_28_dias.md"
organization: "Operations/Research"
---

# Integración de históricos estadísticos al Growth OS

## Respuesta ejecutiva

**Sí conviene integrar los históricos**, pero no copiándolos directamente al `Publication_Log.csv` ni mezclando todas las cifras en una sola baseline. Los datos anteriores son valiosos para responder qué formatos, copys, personajes, horarios y niveles de frecuencia funcionaron antes de agosto; sin embargo, fueron extraídos con métricas y ventanas diferentes.

La integración correcta debe crear una **capa histórica de referencia**. Esa capa alimenta hipótesis, rankings de reuse y decisiones de calendario, mientras que los ledgers operativos actuales siguen reservados para hechos de publicación y métricas con metodología vigente.

## Qué existe actualmente

| Periodo | Evidencia disponible | Qué aporta | Estado de integración |
|---|---|---|---|
| Mayo 2026 | `Operations/Memories/mayo_2026_top_posts_metaBS.md`, `Reuse_Mayo_Meta_Cruce_Datos.csv`, `Reuse_Mayo_Ranking.csv` | Top posts, alcance histórico, publicaciones de reuse, IDs de Meta, candidatos y rendimiento individual de piezas. | Parcial: se usa para ranking/reuse, pero no existe una tabla histórica común por periodo y plataforma. |
| Junio 2026 | `2026-08-08_Reporte_Mensual_Junio_Julio_2026.md`, `Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv` | 13,935 reacciones, 423 comentarios, 4,093 shares y 18,451 interacciones agregadas; patrones de minimalismo y horarios. | Documentado y parcialmente estructurado; falta una vista histórica normalizada. |
| Julio 2026 | Mismos reportes, baseline de plataformas y dataset comparativo | 48,376 reacciones, 926 comentarios, 18,853 shares y 68,155 interacciones agregadas; top posts y señales de Fantasma, emojis e imágenes estáticas. | Mejor integrado que junio, pero permanece distribuido entre reporte, baseline y CSV. |
| Agosto 2026 | `agosto_2026_analisis_28_dias.md`, baseline, ledgers y corte observado 15–16 | Periodo operativo actual, hipótesis, publicación, métricas P0/P2 y cortes observados. | Es la capa operativa vigente; no debe mezclarse sin marcar con históricos. |

## Qué ya está integrado al Growth OS

El Growth OS ya utiliza parte de esos históricos. La baseline de plataformas conserva el top de Facebook de finales de julio y principios de agosto, identifica que las imágenes estáticas superan a los Reels en Facebook durante la muestra, registra la tracción de Fantasma y mantiene Instagram como canal en desarrollo. El reporte mensual de junio–julio documenta los agregados completos de 61 días y confirma que el patrón de copy minimalista aparece antes de agosto.

El ranking de reuse de mayo ya se usa operativamente para seleccionar `Reuse_Top` y `Reuse_Reserve`. También se cruzaron assets de mayo con IDs de Meta y se utilizaron referencias históricas para construir la cola de agosto. Por tanto, **los históricos no están desconectados**; el problema es que su evidencia está repartida en varias capas y no existe todavía una tabla de referencia única.

## Qué no debe hacerse

No se deben sumar alcance de mayo con interacciones de junio–julio, ni comparar lifetime de agosto con snapshots estrictos de 24/72 horas como si fueran la misma ventana. Tampoco se deben crear CNT nuevos solo porque un post histórico tenga un `260####`; el código de asset y el `CNT-####` siguen siendo identificadores distintos hasta que exista evidencia de reconciliación.

El `Publication_Log.csv` tampoco debe recibir una importación masiva histórica sin revisar duplicados, plataforma, fecha local, Meta ID y procedencia. La evidencia histórica puede conservarse como `Historico` sin convertirse automáticamente en una observación operativa actual.

## Capa histórica recomendada

Se recomienda crear una tabla derivada, no destructiva, con una fila por cohorte o publicación histórica verificable. El esquema mínimo sería:

| Campo | Propósito |
|---|---|
| `Historico_ID` | Identificador estable de la fila histórica. |
| `Periodo` | `Mayo_2026`, `Junio_2026`, `Julio_2026` o `Agosto_2026`. |
| `Plataforma` | Facebook, Instagram o TikTok, siempre separadas. |
| `Meta_ID` | ID real cuando exista. |
| `Asset_Ref` | `260####` o nombre histórico, sin inventar CNT. |
| `Fecha_Local` | Fecha de publicación según la fuente. |
| `Formato` | Imagen, Reel, carrusel u otro formato documentado. |
| `Metric_Definition` | Alcance, impresiones, reacciones+comentarios+shares, likes+comments+shares u otra definición explícita. |
| `Metric_Value` | Valor de la métrica principal. |
| `Reacciones`, `Comentarios`, `Shares` | Desglose cuando la fuente lo proporcione. |
| `Ventana` | `Historico`, `Lifetime`, `14d_snapshot` o la ventana real disponible. |
| `Fuente` | Archivo, conector y fecha de extracción. |
| `Comparability` | `Comparable_dentro_periodo`, `Tendencia_relativa` o `No_comparable_absoluto`. |
| `Notas` | Limitaciones, duplicados y contexto editorial. |

Esta capa debería alimentar tres vistas: una **baseline histórica mensual**, un **ranking de reuse por asset** y un **banco de patrones** para hipótesis. No debe sustituir los ledgers actuales ni escribir métricas 24/72h.

## Prioridad de integración

El primer lote recomendado es un resumen estructurado de mayo, junio y julio, no una importación de todos los posts históricos. Debe contener agregados mensuales, top posts, metodología, límites de comparabilidad y enlaces a los datasets existentes. El segundo lote puede incorporar publicaciones individuales con Meta ID y asset confirmado, empezando por el ranking de reuse de mayo y los top posts de junio–julio.

La integración de históricos mejorará el Growth OS en cuatro puntos: permitirá medir la caída de agosto contra una base de tres meses; distinguirá patrones persistentes de efectos particulares de agosto; hará más confiable la selección de reuse; y evitará que el aprendizaje se reinicie cada mes.

## Decisión CGO propuesta

La recomendación es **aprobar la integración histórica en dos capas**:

1. Mantener los documentos originales como evidencia y no sobrescribirlos.
2. Crear una tabla histórica normalizada y una vista mensual que cite explícitamente la métrica, ventana y fuente de cada valor.
3. Usar esos históricos para hipótesis y selección editorial, no para cerrar métricas P0 actuales.
4. Mantener Facebook e Instagram separados y conservar `Historico` como estado de ventana.

El siguiente trabajo concreto sería construir `Historical_Performance_Snapshot.csv` a partir de los datasets ya presentes, comenzando con los agregados mensuales y los top posts verificables. Ese archivo deberá enlazarse desde la baseline y la fuente maestra, y cada fila deberá conservar su método de medición.
