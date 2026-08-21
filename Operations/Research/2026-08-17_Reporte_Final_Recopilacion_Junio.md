---
title: "Reporte final de recopilación histórica de junio"
purpose: "Consolidar los assets publicados, sus objetos multimedia de Facebook, publicaciones editoriales, métricas lifetime y aprendizajes documentados para alimentar la Biblia y el Growth OS."
status: "Review"
created: 2026-08-17
updated: 2026-08-21
version: "1.3"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-17_Revision_Excel_Assets_Junio.md"
  - "Operations/Research/2026-08-17_Mapeo_Photo_ID_Post_Junio.csv"
  - "Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv"
  - "Operations/Research/Historical_Asset_Performance.csv"
  - "Operations/Research/Historical_Performance_Individuals.csv"
  - "Operations/Research/2026-08-17_Analisis_Top_Posts_Junio_Julio.md"
  - "Operations/Research/2026-08-21_Junio_Priority_Queue_Visual_Findings.md"
  - "Operations/Research/2026-08-21_Junio_Priority_Queue_Visual_Matches.csv"
organization: "Operations/Research"
---

# Reporte final de recopilación histórica de junio

## Resumen ejecutivo

La recopilación de junio pasó de una búsqueda parcial por top posts a una relación estructurada entre **assets, Facebook photo objects, publicaciones editoriales y métricas históricas**. El archivo aportado por el usuario contenía 189 registros de Facebook; 172 tenían una referencia de asset suficientemente utilizable para consultar el objeto multimedia. Meta permitió recuperar los 172 objetos, y la comparación visual contra las publicaciones de junio permitió localizar el post editorial correspondiente en todos los casos revisados.

La validación manual del usuario confirmó los 11 casos que habían quedado en revisión automática y también resolvió el outlier `Universe sent me - 015`: el candidato editorial mostrado a la derecha fue aprobado como la publicación correspondiente. Por ello, el lote de 172 objetos multimedia queda editorialmente relacionado; 171 conservan un Asset_Ref identificable y uno queda con relación editorial confirmada pero Asset_Ref pendiente.

## Cobertura final

| Elemento | Resultado |
|---|---:|
| Registros del Excel de junio | 189 |
| Facebook photo IDs únicos | 189 |
| Registros con referencia de asset utilizable en el Excel | 172 |
| Objetos multimedia recuperados desde Meta | 172 |
| Relaciones photo object → post editorial confirmadas | 172 |
| Relaciones con Asset_Ref identificable | 171 |
| Relaciones editoriales con Asset_Ref pendiente | 1 |
| Registros sin Asset_Ref utilizable fuera del lote | 17 |
| Publicaciones de junio con asset y relación integrada | 172 |
| Publicaciones de la cola todavía sin asset match | 58 |

Los 17 registros sin Asset_Ref utilizable continúan como una cola separada. Incluyen referencias internas `humor3.8`, `humor4.06`, `humor3.14`, `humor4.07`, un valor de nombre interno de imagen, un vacío y `N/A`. No se transformaron en CNT ni en Asset_Ref canónicos.

## Identificadores y trazabilidad

Cada relación conserva tres identificadores separados:

| Identificador | Función |
|---|---|
| `facebook_photo_id` | Identifica el objeto multimedia consultado en Meta |
| `meta_publication_id` | Identifica la publicación editorial de la Página |
| `Asset_Ref` | Identifica el asset creativo en Drive/inventario |

Esta separación evita el error de usar el photo ID como si fuera el Meta post ID. Los seis CNT que ya existían se conservaron sin duplicación. No se crearon CNT masivos nuevos en esta fase; la ampliación del inventario se hará después de revisar reutilización, duplicados y prioridad editorial.

## Rendimiento histórico integrado

Las métricas siguientes son **lifetime historical** y no representan ventanas uniformes de 24 o 72 horas. Se calcularon sobre las 172 publicaciones que ahora tienen una relación editorial integrada:

| Métrica | Total | Promedio por publicación |
|---|---:|---:|
| Interacciones | 17,334 | 100.78 |
| Reacciones | 13,198 | 76.73 |
| Comentarios | 384 | 2.23 |
| Shares | 3,752 | 21.81 |

Estas cifras amplían considerablemente la base de aprendizaje de junio. No deben compararse directamente con métricas recientes de 24/72 horas sin normalizar la ventana temporal.

## Cambios realizados

Se actualizaron la cola `2026-08-17_Cola_Reconciliacion_Assets_Junio.csv`, `Historical_Asset_Performance.csv`, `Historical_Performance_Individuals.csv` y `2026-08-17_Mapeo_Photo_ID_Post_Junio.csv`. Los 160 matches visuales automáticos quedaron integrados primero; después se incorporaron las 11 confirmaciones visuales manuales y la decisión editorial sobre `Universe sent me - 015`.

Los registros añadidos a los ledgers mantienen la fuente de evidencia, el tipo de validación y la advertencia de comparabilidad lifetime. Las relaciones confirmadas no se mezclaron con la extracción P0 de 24/72 horas.

## Valor para la Biblia y el Growth OS

Junio deja de ser únicamente un conjunto de top posts y se convierte en una base histórica amplia. Ahora permite estudiar, con mayor cobertura, la relación entre frecuencia de publicación, personajes, composición visual, tono, captions, reacciones, comentarios y shares.

Los aprendizajes deben separarse en tres niveles. El primero es **rendimiento bruto**, útil para encontrar picos. El segundo es **difusión**, medido especialmente por shares. El tercero es **conversación**, donde los comentarios y replies muestran si el meme produjo identificación, debate, etiquetas o reformulaciones de la audiencia.

La siguiente fase recomendada es asignar CNT únicamente a los assets prioritarios o reutilizables, comenzando por los que tengan mayor rendimiento y una relación visual/editorial confirmada. No es necesario convertir automáticamente los 171 Asset_Ref en CNT si todavía no serán usados en producción.

## Auditoría de pendientes actualizada

Junio queda ampliamente integrado a nivel histórico individual. En el corte actual, `Historical_Performance_Individuals.csv` contiene 178 filas del periodo `Junio_2026` y 173 `Meta_ID` únicos con `Asset_Ref`; las filas incluyen los 172 cruces del lote original, registros destacados ya existentes y un match suplementario confirmado el 21 de agosto. El índice visual contiene 196 assets de Drive. La cola de posts todavía sin match baja de 58 a 57 después de confirmar `122129404893072582` con `Asset_Ref=260746`.

| Pendiente | Estado | Prioridad |
|---|---|---|
| Reconciliar los 17 registros sin Asset_Ref utilizable | Pendiente; contienen referencias internas, vacío o `N/A` | P2 / bajo demanda |
| Revisar los 57 posts de la cola todavía sin asset match | Reserva de investigación; no crear CNT automáticamente | P1 histórico si se busca cobertura completa |
| Convertir todos los assets confirmados en CNT | No recomendado; solo asignar CNT a piezas prioritarias o reutilizables | P2 / bajo demanda |
| Completar taxonomía editorial | Parcial; aplicada en los casos enriquecidos, no como clasificación exhaustiva de todo junio | P1 analítico |
| Analizar comentarios y replies | Pendiente como capa de conversación | P2 |
| Recalcular personajes, horarios y formatos | Hay análisis inicial y tablas, pero todavía requiere ampliación y lectura editorial | P1 analítico |
| Seleccionar reuse histórico | Puede hacerse con los assets confirmados de mayor difusión y distancia de 30 días | P1 operativo cuando se abra una cola reuse |
| Reconstruir ventanas 24/72h históricas | No posible de forma exacta con los datos actuales; conservar lifetime como histórico | No ejecutar |

## Auditoría de estado posterior a la aprobación de CNT

Los seis candidatos aprobados ya fueron integrados como `CNT-080`–`CNT-085` y quedaron en `Reuse_Candidate`. Esto es una integración de inventario histórico, no una decisión de calendario. La prueba activa de agosto continúa sin cambios hasta el 30 de agosto.

| Capa | Estado al 18 de agosto | Pendiente real |
|---|---|---|
| Publicaciones individuales | 178 filas de junio; 173 Meta IDs únicos | No falta integración básica de publicaciones confirmadas |
| Assets de Drive | 196 assets indexados; 173 relaciones publicación→asset confirmadas en el ledger actual | Resolver 17 registros sin `Asset_Ref` utilizable y 57 casos de cola sin match si se busca cobertura completa |
| CNT prioritarios | `CNT-080`–`CNT-085` creados | No crear más CNT hasta seleccionar otro lote útil |
| Taxonomía visual | 17 assets revisados; seis enriquecidos como CNT | Ampliar solo a lotes con valor analítico o de reuse |
| Comentarios | 72 comentarios extraídos de cinco posts prioritarios | Hacer análisis cualitativo profundo solo si aporta decisiones de comunidad |
| Reuse | Cola de seis CNT preparada | No programar durante la prueba activa; reevaluar después del 30 de agosto |
| Lifetime histórico | Integrado y separado | No reconstruir ventanas históricas 24/72h |
| Canon | Sin cambios | No convertir rendimiento en reglas canónicas automáticamente |

## Estado

Junio queda **integrado a nivel suficiente para el Growth OS**. Lo pendiente se divide en dos reservas: una reserva de reconciliación —17 registros sin `Asset_Ref` utilizable y 57 casos sin match— y una reserva analítica —taxonomía, comentarios y selección adicional de reuse—. Ninguna bloquea la prueba activa de agosto.

La recomendación CGO es congelar la programación de estos seis CNT hasta el cierre del experimento del 30 de agosto. Después se podrá comparar su evidencia histórica con el veredicto P0 y decidir si alguno merece una nueva prueba controlada.

## Corte suplementario del 21 de agosto

La revisión selectiva de los tres casos de mayor prioridad en `Needs_Asset_Match` produjo una sola confirmación adicional. El post `122129404893072582` coincide visualmente con `Universe - Existencial 260746.png` (`Drive_ID=1CYrpRf4KUOClP_Qvcc65yDx0Sq-JIguk`) y se integró al ledger individual con 155 interacciones, 19 shares y la estructura de microhistoria de tres paneles. Los candidatos `122134147251072582` y `122130196011072582` no coincidieron con los archivos sugeridos por similitud y permanecen sin match.

Este corte no cambia el total histórico del lote original —172 relaciones—; añade una evidencia suplementaria al ledger operativo, eleva los Meta IDs únicos integrados a 173 y reduce la cola abierta a 57. No se creó CNT, no se modificó calendario y no se consideró el filename como prueba independiente de la coincidencia.

La decisión es congelar las 57 reservas restantes. Solo deben reabrirse si una pregunta concreta requiere cerrar una celda comparativa, elegir un reuse o validar una hipótesis de personaje/formato.

## Referencias

[1]: `Operations/Research/2026-08-17_Mapeo_Photo_ID_Post_Junio.csv` "Mapa de photo IDs a posts editoriales"
[2]: `Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv` "Cola histórica de junio"
[3]: `Operations/Research/Historical_Asset_Performance.csv` "Rendimiento histórico por asset"
[4]: `Operations/Research/Historical_Performance_Individuals.csv` "Ledger individual histórico"
