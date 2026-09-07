# Estado histórico de Universe Sent Me — marzo a agosto de 2026

**Propósito:** Consolidar el último diagnóstico histórico disponible para que el Growth OS y Codex distingan entre evidencia, señales débiles y vacíos de datos al evaluar los experimentos nuevos.

**Estado:** Active  
**Fecha de creación:** 2026-09-06  
**Última actualización:** 2026-09-06  
**Versión:** 1.0  
**Autor:** Manus AI (CGO)  
**Documentos relacionados:** [Índice del Growth OS](00_Índice.md), [Fuente maestra y ledgers](14_00_Fuente_Maestra_y_Ledgers.md), [Reglas de aprendizaje](06_00_Reglas_Aprendizaje_Tendencias.md), [Integración Growth OS–Canon](Integracion_Growth_OS.md), [Studio Governance](../Studio_Governance.md)  
**Organización:** `GrowthOS/`

> Este documento conserva el diagnóstico recibido el 6 de septiembre de 2026. No sustituye los ledgers operativos ni convierte una señal histórica en una hipótesis confirmada.

## 1. Cobertura y calidad de la evidencia

El histórico contiene aproximadamente 275 planificaciones de publicación entre marzo y julio de 2026, pero esas filas no incluyen métricas de rendimiento. También contiene 30 días de métricas agregadas de página entre el 26 de junio y el 24 de julio, 17 franjas horarias agregadas de junio, seis assets de la cola de reutilización con `meta_post_id` y seis publicaciones con métricas individuales del 24 de agosto. En consecuencia, la evidencia post-level sigue siendo pequeña.

| Capa | Cobertura | Uso válido |
|---|---:|---|
| Página/día | 30 días, junio–julio | Tendencias macro de impresiones, interacciones, reacciones, shares y comentarios |
| Página/hora | 17 franjas, junio | Señales agregadas de horario; no prueba rendimiento por personaje |
| Post individual | 6 posts, 24 ago. | Comparaciones descriptivas con `experiment_id`, `hypothesis_id` y `asset_ref` |
| Reuse queue | 6 assets | Reutilización con historial conocido; shares, comments, personaje y `meta_post_id` |
| Planificación | ~275 filas, marzo–julio | Historial de actividad, no evidencia de éxito |

No están disponibles históricamente, de forma suficiente por post, el alcance, las impresiones, las vistas de video, el watch time, la retención, CTR, clics, guardados, DMs, leads ni ventanas E0/E24/E72.

## 2. Experimentos e hipótesis históricas

Los experimentos del 24 de agosto son `EXP-2026-08-CAL-01` y `EXP-2026-08-COMP-GAPS-01`. No tienen veredicto formal histórico. Las hipótesis `HB-003` a `HB-007` fueron inferidas retrospectivamente desde IDs y contexto; ninguna debe tratarse como confirmada o refutada.

| Hipótesis | Observación | Estado CGO |
|---|---|---|
| `HB-003` Universe/humor absurdo genera más shares | Kael 19:00: 26 shares; Universe 17:00: 6 | Incierta; `n=4` y Universe no supera a Kael |
| `HB-004` 19:00/17:00 supera otros horarios | 19:00: 49 interacciones; 17:00: 32 | Señal probable, no conclusión; `n=1` por slot |
| `HB-005` Primer Círculo supera Segundo Círculo | No hubo posts medidos del Segundo Círculo | Pendiente |
| `HB-006` Micro-historia romántica/absurda de 3 paneles | 29 interacciones, 6 shares | Incierta; `n=1` |
| `HB-007` Micro-historia cotidiana de 3 paneles | 25 interacciones, 4 shares | Incierta; `n=1` |

## 3. Hallazgos y señales utilizables

Se confirma actividad diaria sostenida de la página durante junio–julio: 30 días consecutivos con impresiones aproximadas de 25K–72K, interacciones de 700–3K, reacciones de 500–1.8K y shares de 65–311. En los seis posts individuales, Kael a las 19:00 obtuvo 49 interacciones, 22 reacciones y 26 shares; esto es una observación destacada, no una prueba de superioridad permanente.

El agregado horario de junio mostró picos de interacción total a las 11:00, 19:00 y 21:00: 2,459, 2,833 y 2,795 interacciones respectivamente. Las micro-historias de tres paneles obtuvieron 29 y 25 interacciones, pero cada formato tiene una sola observación comparable. Seis assets de junio tienen historial de publicación conocido y fueron aprobados para la cola de reutilización.

| Clasificación | Decisión operativa |
|---|---|
| Confirmado descriptivamente | Usar 17:00/19:00 y explorar 11:00/21:00 en nuevos tests, sin asumir causalidad |
| Señal probable | Priorizar Kael/lore en una prueba nocturna; no declarar que Kael siempre supera a Universe |
| Variante prometedora | Mantener micro-historias de tres paneles como variante experimental |
| Reutilización | Priorizar los seis assets con `meta_post_id` conocido y respetar la regla de 30 días |

## 4. Lo que no puede afirmarse

El histórico no permite comparar Primer Círculo contra Segundo Círculo, Reels contra Photos en retención, el mejor horario por personaje, Universe contra otros personajes en shares, E0/E24/E72 reales ni el rendimiento de los 194 assets sin vínculo publicación–asset. Tampoco permite calcular un engagement rate real por post porque faltan impresiones o alcance por publicación.

No hay hipótesis históricas formalmente invalidadas. La ausencia de evidencia debe registrarse como `Incierta` o `Pendiente`, nunca como `Refutada`.

## 5. Puente hacia el Growth OS de septiembre

El nuevo sistema debe conservar este histórico como baseline de solo lectura y no sobrescribirlo. Los cuatro experimentos nuevos de septiembre (`EXP-2026-09-WEEK1`) —`HB-UNI-001` Primer vs. Segundo Círculo, `HB-UNI-002` Reel vs. Photo, `HB-UNI-003` humor absurdo de Universe y `HB-UNI-004` 20:00 vs. 08:30— llenan vacíos históricos; no reemplazan `HB-003`–`HB-007`.

La prioridad CGO es capturar métricas por post y snapshots E0/E24/E72 desde el inicio, mantener IDs explícitos (`experiment_id`, `hypothesis_id`, `asset_ref`, `meta_post_id`) y emitir veredictos solo con el protocolo vigente del ledger. Las tres piezas de `EXP-2026-09-WEEK1` estaban aprobadas/programadas al momento del diagnóstico, pero tenían cero métricas capturadas; por ello no aportaban evidencia todavía.

## 6. Documentos que deben mantenerse coherentes

Este documento no modifica el canon narrativo. Al actualizar el histórico o emitir nuevos veredictos, deben revisarse el [ExperimentLog], el [Metrics Snapshot Log], la [Fuente maestra y ledgers] y las [Reglas de aprendizaje]. Si una conclusión cambia el calendario, la cola de reutilización o el HypothesisBank, esos documentos deben actualizarse en la misma operación o quedar explícitamente marcados como pendientes.

## 7. Fuente y límites

Fuente de esta consolidación: `pasted_content.txt` recibido en la tarea del 6 de septiembre de 2026, descrito como reconstrucción basada exclusivamente en `tenants/universe/historical/`. El archivo original no se considera fuente operativa; este documento es la versión permanente resumida para el repositorio. No se han inferido causalidad, veredictos nuevos ni datos ausentes.

**Estado CGO:** Universe no parte de cero, pero el histórico sirve principalmente como baseline contextual. La evidencia accionable para decisiones comparativas debe construirse con el sistema de septiembre y sus ledgers.

[ExperimentLog]: ../Operations/Research/2026-08-15_ExperimentLog.csv
[Metrics Snapshot Log]: ../Operations/Research/Metrics_Snapshot_Log.csv
[Fuente maestra y ledgers]: 14_00_Fuente_Maestra_y_Ledgers.md
[Reglas de aprendizaje]: 06_00_Reglas_Aprendizaje_Tendencias.md
[Growth OS]: 00_Índice.md
