---
title: "Reporte final de recopilación histórica de junio"
purpose: "Consolidar los assets publicados, sus objetos multimedia de Facebook, publicaciones editoriales, métricas lifetime y aprendizajes documentados para alimentar la Biblia y el Growth OS."
status: "Review"
created: 2026-08-17
updated: 2026-08-17
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-17_Revision_Excel_Assets_Junio.md"
  - "Operations/Research/2026-08-17_Mapeo_Photo_ID_Post_Junio.csv"
  - "Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv"
  - "Operations/Research/Historical_Asset_Performance.csv"
  - "Operations/Research/Historical_Performance_Individuals.csv"
  - "Operations/Research/2026-08-17_Analisis_Top_Posts_Junio_Julio.md"
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

Junio queda ampliamente integrado a nivel histórico individual: `Historical_Performance_Individuals.csv` contiene 177 filas del periodo `Junio_2026`, compuestas por los 172 cruces del lote de junio y los registros destacados ya existentes. El índice visual contiene 196 assets de Drive. La relación entre publicación y asset está confirmada para 172 registros; 17 registros del Excel original no tienen una referencia de asset utilizable y un caso mantiene relación editorial confirmada pero `Asset_Ref` pendiente.

| Pendiente | Estado | Prioridad |
|---|---|---|
| Reconciliar los 17 registros sin Asset_Ref utilizable | Pendiente; contienen referencias internas, vacío o `N/A` | P2 / bajo demanda |
| Revisar los 58 posts de la cola todavía sin asset match | Reserva de investigación; no crear CNT automáticamente | P1 histórico si se busca cobertura completa |
| Convertir todos los assets confirmados en CNT | No recomendado; solo asignar CNT a piezas prioritarias o reutilizables | P2 / bajo demanda |
| Completar taxonomía editorial | Parcial; aplicada en los casos enriquecidos, no como clasificación exhaustiva de todo junio | P1 analítico |
| Analizar comentarios y replies | Pendiente como capa de conversación | P2 |
| Recalcular personajes, horarios y formatos | Hay análisis inicial y tablas, pero todavía requiere ampliación y lectura editorial | P1 analítico |
| Seleccionar reuse histórico | Puede hacerse con los assets confirmados de mayor difusión y distancia de 30 días | P1 operativo cuando se abra una cola reuse |
| Reconstruir ventanas 24/72h históricas | No posible de forma exacta con los datos actuales; conservar lifetime como histórico | No ejecutar |

## Estado

Junio queda **recopilado y relacionado**, pero no completamente cerrado como análisis estratégico. Lo importante que falta no es volver a buscar los 172 cruces ya confirmados, sino decidir qué subconjunto merece enriquecimiento editorial, lectura de comentarios, creación de CNT o incorporación a la cola de reuse. Los 17 registros sin Asset_Ref y los 58 posts restantes de la cola son reservas separadas y no deben mezclarse con la capa individual ya confirmada.

## Referencias

[1]: `Operations/Research/2026-08-17_Mapeo_Photo_ID_Post_Junio.csv` "Mapa de photo IDs a posts editoriales"
[2]: `Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv` "Cola histórica de junio"
[3]: `Operations/Research/Historical_Asset_Performance.csv` "Rendimiento histórico por asset"
[4]: `Operations/Research/Historical_Performance_Individuals.csv` "Ledger individual histórico"
