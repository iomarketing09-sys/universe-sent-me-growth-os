---
title: "Análisis de julio con taxonomía normalizada y pendientes del Growth OS"
purpose: "Aplicar la taxonomía editorial a la muestra histórica disponible de julio y priorizar los pendientes operativos, de aprendizaje y de canon."
status: Active
created: 2026-08-17
updated: 2026-08-20
version: "1.2"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-17_Julio_Analisis_Taxonomia.csv"
  - "Operations/Research/2026-08-17_Analisis_Top_Posts_Junio_Julio.md"
  - "Operations/Research/2026-08-15_Auditoria_General_Growth_OS.md"
  - "Operations/Research/2026-08-15_Deuda_Documental_P2.md"
  - "Operations/Research/2026-08-17_Taxonomia_Editorial_Contenido_USM.md"
organization: "Operations/Research"
---

# Análisis de julio con taxonomía normalizada y pendientes del Growth OS

## Alcance y limitación

La taxonomía se aplicó a los **seis posts top de julio** que ya tienen relación individual con asset y Meta ID. Esta no es todavía una muestra completa de todas las publicaciones de julio. Por tanto, el análisis sirve para revisar la calidad de la clasificación y detectar señales iniciales, pero no para declarar que un personaje o tipo de humor domina todo el mes.

Los seis posts acumulan **22,840 interacciones, 14,272 reacciones, 216 comentarios y 8,352 shares**. La métrica es lifetime historical y no debe mezclarse con ventanas de 24/72 horas.

## Resultado de la taxonomía

| Campo | Resultado en la muestra de 6 posts | Lectura |
|---|---:|---|
| Rol `Protagonista` | 5 | La mayoría está organizada alrededor de una figura central |
| Rol `Dúo o pareja` | 1 | La pieza de `2607987` tiene una lectura interpersonal más clara |
| Humor `Existencial o absurdo` | 4 | Es el patrón dominante de la muestra, pero puede estar influido por la convención `Universe - Existencial` |
| Humor existencial + relatable | 2 | Señal de mezcla entre reflexión y experiencia cotidiana |
| Potencial de etiquetado alto | 1 | El caso `729` debe revisarse porque su potencial social parece superior |
| Potencial medio | 1 | Caso `2607987` |
| Potencial bajo | 4 | No significa que no sean compartibles; la heurística actual no sustituye análisis de shares |

La normalización revela un problema útil: los seis filenames siguen usando `Universe - Existencial`, por lo que el nombre del archivo no basta para conocer el personaje o el tipo real de humor. En julio debe priorizarse la revisión editorial de imagen y caption para sustituir la inferencia de filename por evidencia visual.

## Rendimiento por pieza

| Asset | Interacciones | Shares | Rol | Taxonomía provisional |
|---:|---:|---:|---|---|
| `260604` | 5,482 | 2,312 | Protagonista | Existencial; etiquetado bajo por heurística |
| `2607987` | 3,726 | 1,341 | Dúo o pareja | Existencial + relatable; etiquetado medio |
| `729` | 2,979 | 714 | Protagonista | Existencial + relatable; etiquetado alto |
| `260504` | 3,913 | 1,521 | Protagonista | Existencial; etiquetado bajo por heurística |
| `728` | 3,993 | 1,449 | Protagonista | Existencial; etiquetado bajo por heurística |
| `2607966` | 2,747 | 1,015 | Protagonista | Existencial; etiquetado bajo por heurística |

El mayor rendimiento está concentrado en `260604`, que también tiene el mayor número de shares. Sin embargo, no se puede atribuir ese resultado al personaje porque la muestra no contiene una comparación equilibrada de personajes. La señal más sólida de julio es que las piezas con una situación fácilmente transferible a otra persona —especialmente `260604`, `2607987` y `260504`— tienen alta difusión.

## Aprendizajes provisionales

La primera hipótesis es que el **potencial de compartir** explica mejor el rendimiento de estos seis posts que el nombre del personaje. El promedio de shares de la muestra es 1,392 por publicación, pero la distribución está dominada por tres piezas con más de 1,300 shares.

La segunda hipótesis es que el humor existencial funciona mejor cuando se combina con una situación concreta o relatable. Esta conclusión es compatible con la muestra, pero todavía no está validada para todo julio porque solo hay seis registros taxonómicamente enriquecidos.

La tercera hipótesis es que la taxonomía actual necesita una revisión visual de los seis top posts. En particular, `Universe` no debe conservarse como personaje principal solo porque aparece en el filename; debe confirmarse quién aparece y cuál es su función narrativa.

## Pendientes del Growth OS

| Prioridad | Pendiente | Estado | Próxima acción |
|---|---|---|---|
| Histórico | Métricas comparables de 24/72 horas | No reconstruible para julio | Mantener las métricas lifetime separadas; no usar julio histórico como sustituto de ventanas 24/72 horas de agosto |
| P1 | Completar la cobertura histórica individual de julio | Parcial | Ampliar más allá de los seis top posts solo si existe una pregunta concreta; priorizar shares, comentarios y casos taxonómicamente comparables |
| P1 | Monitorear la ola de Facebook 17–30 agosto | Activo | Registrar `Programada → Publicada`, extraer métricas válidas y no contaminar el experimento con reuse no aprobado |
| P2 | Consolidar la fuente maestra y los estados de julio | Parcial | Los seis top ya tienen CNT, Asset_Ref, Drive ID y Meta ID; ampliar la reconciliación solo con evidencia Meta/Drive y sin crear CNT masivos |
| P2 | Revisión de comentarios recientes | Operativo | Continuar por ventanas incrementales y responder solo con aprobación humana |
| P2 | Revisión de canon con Claude | Pendiente | Usar el Changelog y la taxonomía para clasificar cada supuesto de la Biblia antes de proponer cambios |
| P2 | Instagram | Controlado | Mantener el scheduler histórico fuera de operación; cualquier nueva ola debe tener playbook autocontenido e idempotencia |
| P2 | CNT-004 | Diferido por decisión del usuario | Mantener fuera de producción y no usarlo para conclusiones canónicas |
| P2 | Menciones históricas a Make | Trazabilidad | No tratar documentos antiguos como arquitectura activa; actualizar solo documentos de control cuando corresponda |

## Auditoría de integración al Growth OS

La cobertura individual de julio sigue siendo **parcial**. `Historical_Performance_Individuals.csv` contiene seis publicaciones de julio con Meta ID, métricas lifetime, asset confirmado, Drive ID y CNT editorial (`CNT-074` a `CNT-079`). La comparación mensual sí contiene 207 publicaciones de julio, pero esa tabla es una capa agregada/analítica y no sustituye la reconciliación individual asset → Meta → CNT.

| Capa | Estado actual | Qué falta |
|---|---|---|
| Agregado mensual | Integrado | No falta integración; debe mantenerse separado de lifetime individual y de 24/72h |
| Top posts individuales | Integrado para seis casos | No falta reconciliación de esos seis; falta ampliar la muestra si se quiere estudiar más que los top posts |
| Assets de Drive | Confirmados para los seis top | Falta localizar y cruzar más assets de julio con publicaciones Meta |
| CNT editorial | `CNT-074`–`CNT-079` creados | No crear CNT masivos sin una correspondencia Meta/Drive verificable |
| Taxonomía | Aplicada y revisada visualmente en seis casos | Falta aplicarla a una muestra ampliada de julio |
| Métricas | Lifetime históricas disponibles para los seis y agregado mensual para 207 publicaciones | Falta una capa individual ampliada con métricas y fecha; 24/72h no es reconstruible para publicaciones históricas |
| Aprendizaje | Hipótesis inicial documentada | Falta contrastar potencial de etiquetado, humor y horario con más casos |

Por lo tanto, lo que falta de julio no es “cerrar” los seis top posts: esos ya están integrados. El pendiente real es ampliar la cobertura individual de julio, empezando por publicaciones con más shares y comentarios, y después aplicarles la taxonomía normalizada. Esta ampliación es **P1 histórico**, pero no bloquea la operación actual ni debe retrasar el corte P0 de agosto.

## Recomendación CGO

La **revisión visual y editorial de los seis top posts de julio ya está completada**. El siguiente lote, si se aprueba, debe ampliar la muestra con posts de julio que tengan más shares y comentarios para responder una pregunta concreta de rendimiento. Solo cuando existan suficientes casos comparables por personaje y tipo de humor será razonable comparar grupos.

Para la Biblia, los resultados actuales deben registrarse como hipótesis: `El humor existencial/relatable y la etiquetabilidad parecen explicar parte de la difusión de julio`. No debe elevarse todavía a regla canónica.

Este documento debe comunicarse a Claude mediante el Changelog antes de modificar cualquier regla de la Biblia.

## Revisión visual de los seis top posts

La revisión directa de las imágenes corrigió la taxonomía provisional basada en los filenames. Solo `2607966` y `728` muestran claramente a Universe, mientras que `2607987` muestra a Fantasma. `260504`, `260604` y `729` contienen figuras humanas, corales o esqueletos, pero no aportan evidencia suficiente para asignar personajes canónicos concretos.

| Asset | Personaje principal visual | Rol narrativo | Tipo de humor visual | Potencial de etiquetado |
|---:|---|---|---|---|
| `260504` | No identificado | Reparto coral | Observacional social | Alto |
| `260604` | No identificado | Protagonista | Relatable cotidiano; existencial o absurdo | Alto |
| `2607966` | Universe | Protagonista | Existencial o relatable | Medio |
| `2607987` | Fantasma | Protagonista | Relatable; existencial | Medio |
| `728` | Universe | Protagonista | Sexual o insinuación; observacional social | Medio |
| `729` | No identificado | Dúo o pareja | Humor ácido o negro; relatable | Alto |

La revisión visual confirma que el filename `Universe - Existencial` no puede utilizarse como sustituto del personaje visible. La evidencia cambia el aprendizaje: los posts más fuertes de julio no forman un grupo homogéneo de Universe ni demuestran que un personaje específico sea la causa del rendimiento. La señal más defendible es la combinación de una situación clara, una emoción reconocible y potencial de compartir o etiquetar.

La taxonomía de estos seis registros se considera ahora de confianza alta porque se apoya en observación visual directa. Las clasificaciones no modifican el canon y deben revisarse con Claude únicamente como evidencia de aprendizaje.
