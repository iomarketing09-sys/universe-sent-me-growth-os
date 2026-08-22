---
title: "Playbook operativo de cadencia diaria — 5–7 piezas"
purpose: "Definir cómo recuperar una cadencia diaria de 5–7 publicaciones sin perder consistencia editorial, trazabilidad, separación de formatos y capacidad de aprendizaje del Growth OS."
status: Review
created: 2026-08-14
updated: 2026-08-22
version: "1.5"
author: "Manus AI (CGO)"
related_documents:
  - "GrowthOS/05_03_Calendario_10_16_Agosto.md"
  - "Operations/Research/2026-08-16_Calendario_Operativo_17_30_Agosto.md"
  - "Operations/Research/2026-08-22_Comparativa_Junio_Julio_Agosto_y_Brechas_Integracion.md"
  - "Operations/Research/2026-08-14_Ciclo_Aprendizaje_Horarios.md"
  - "Operations/Research/2026-08-21_Analisis_Corte_Diario_Familias_Personajes.md"
  - "Operations/Research/2026-08-22_Reels_Metric_Instrumentation_Protocol.md"
  - "GrowthOS/Integracion_Growth_OS.md"
  - "GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md"
organization: "Operations/Research"
---

# Playbook operativo de cadencia diaria — 5–7 piezas

## 1. Decisión CGO

La cadencia reducida de agosto no debe corregirse publicando piezas de relleno. La decisión operativa es recuperar una **banda de 5 a 7 publicaciones diarias**, con una base de seis en los días de mayor capacidad, manteniendo un mínimo de cinco en viernes y sábado. El séptimo slot es una capacidad excepcional y controlada, no una obligación diaria.

La meta de esta estructura no es regresar mecánicamente al volumen de julio. Es aumentar la superficie de descubrimiento sin volver a depender de reuse improvisado ni contaminar las hipótesis con cambios simultáneos. La comparación reciente mostró que agosto está por encima de junio en mediana e interacciones por día, pero por debajo de julio y mucho más concentrado en pocos outliers. [1]

> **Principio rector:** cada slot debe tener una función editorial identificable. Si no existe una pieza aprobada que cumpla esa función, el slot se deja vacío y se registra `Slot_No_Publicado`; no se rellena con un asset improvisado.

Este playbook no modifica por sí mismo el calendario activo 17–30 de agosto. Sin embargo, el 22 de agosto Fernando autorizó explícitamente aplicar la ampliación al tramo 22–30; esa excepción operativa quedó registrada en `Operations/Research/2026-08-22_Cadence_Expansion_22_30_Execution.json`. Para cualquier cambio futuro de fecha, hora, asset, caption o plataforma se mantiene la exigencia de orden y aprobación humana separada.

### 1.1 Lectura de transición del calendario activo

El calendario activo 17–30 partió de 74 slots para 14 días, equivalentes a **5.28 publicaciones asignadas por día**. Tras la autorización del 22 de agosto se añadieron cuatro slots en el tramo 22–30, por lo que el calendario vigente contiene 78 slots. Cada día del 22 al 30 queda en la banda de **5–6 publicaciones**; el tramo suma 50 filas y 5.56 publicaciones promedio por día. La mezcla vigente del calendario es de 40 piezas nuevas, 35 `Reuse_Top` y 3 `Reuse_Reserve`; se registra como transición operativa y no se presenta como cumplimiento automático del objetivo futuro de 65%–70% nuevas.

Durante el calendario activo, la operación correcta es medir cuántas publicaciones reales se ejecutan, documentar slots vacíos y preservar los estados de Facebook, Instagram, Reels y afiliados. La aplicación autorizada del 22–30 es la primera ejecución documentada de esta recuperación: añadió solo assets exactos, mantuvo Facebook como plataforma y dejó un ledger reproducible. En adelante no se deben añadir piezas solo para alcanzar siete por día ni convertir el reuse existente en contenido nuevo por etiqueta administrativa.

## 2. Objetivos y límites de operación

| Objetivo | Regla operativa | Indicador de control |
|---|---|---|
| Recuperar presencia | Publicar entre 5 y 7 piezas aprobadas por día según la matriz semanal | Publicaciones reales por día |
| Elevar el piso | Priorizar mediana de interacciones por pieza, no solo el mejor post | Mediana diaria y mediana móvil de siete días |
| Conservar consistencia | Mantener funciones editoriales, identidad visual, captions y hashtags verificables | Preflight aprobado por fila |
| Evitar contaminación | Separar imágenes, Reels, Instagram, afiliados y experimentos | `Formato`, `Plataforma`, `Incluida_En_Test` y `Affiliate_Status` |
| Aprender diariamente | Usar el reporte diario como fuente principal; no fabricar deltas de 24/72 horas | Corte diario con hora y fuente |
| Proteger la marca | No forzar personajes ni canon en memes donde no aporten | Revisión de identidad y canon |

La cadencia es una condición de distribución, no una hipótesis aislada. Durante la primera semana se observará si aumenta la superficie sin que caigan la mediana y los shares por pieza. No se declarará ganadora una franja, familia o personaje con un único outlier; se requieren al menos tres casos comparables para señal preliminar y cinco para una decisión operativa.

## 3. Matriz semanal de publicaciones

La matriz base produce 40 publicaciones por semana, un promedio de **5.7 piezas por día**. Puede subir a 41 cuando el domingo supera el control de calidad y se habilita el séptimo slot exploratorio. Así se recupera parte de la cadencia histórica sin convertir el máximo en obligación.

| Tipo de día | Slots base | Frecuencia base | Séptimo slot | Frecuencia máxima | Función |
|---|---|---:|---|---:|---|
| Lunes–jueves | 10:00, 11:00, 13:30, 16:00, 17:00, 19:00 | 6 | No aplica | 6 | Días de mayor superficie y aprendizaje |
| Viernes | 10:00, 11:00, 13:30, 17:00, 19:00 | 5 | No aplica | 5 | Mantener presencia sin saturar el cierre semanal |
| Sábado | 10:00, 11:00, 13:30, 17:00, 19:00 | 5 | No aplica | 5 | Presencia estable y piezas de baja fricción |
| Domingo | 10:00, 11:00, 13:30, 16:00, 19:00, 22:00 | 6 | 17:00, solo con reserva aprobada | 7 | Día de mayor exploración; 22:00 sigue siendo condición experimental |

Todos los horarios son locales de `America/Matamoros` y deben conservar la hora real de publicación. Una tolerancia de hasta ±10 minutos se registra como operación normal. Un retraso superior a 30 minutos se registra como `Desviación_Horaria = Sí`; no se corrige retrospectivamente para que parezca una publicación en el slot original.

La matriz no debe interpretarse como prueba de que 22:00 sea universalmente mejor. El domingo nocturno es una condición exploratoria y no se convierte en regla sin repetición suficiente. Si la reserva del séptimo slot no pasa el preflight, el domingo conserva seis publicaciones.

## 4. Arquitectura de cartera diaria

Cada día se construye como una cartera de funciones, no como una lista de personajes. Los personajes son condimento; la situación reconocible, el remate y la compartibilidad son las variables editoriales que se deben proteger.

### 4.1 Día de seis publicaciones

| Slot | Tipo de pieza | Función editorial | Tratamiento de caption |
|---|---|---|---|
| 10:00 | Nueva — relatable/social | Abrir el día con una situación reconocible y autosuficiente | `caption_minimo` o emoji de remate |
| 11:00 | `Reuse_Top` | Ancla de distribución con evidencia histórica | Caption validado, sin copiar el texto visual innecesariamente |
| 13:30 | Nueva — difusión mínima | Favorecer shares y etiquetado de baja fricción | `caption_minimo` |
| 16:00 | Nueva o reuse controlado — aprendizaje | Probar una familia, horario o estructura previamente definida | Treatment asignado antes de publicar |
| 17:00 | Nueva — personaje o microhistoria | Aportar variedad narrativa sin forzar canon | `caption_refuerzo` o `caption_conversacional` según el brief |
| 19:00 | Nueva — remate fuerte | Cerrar la jornada con una pieza de mayor potencial de conversación | Treatment definido; no cambiarlo después de ver resultados |

La composición objetivo de un día de seis slots es **cuatro piezas nuevas y dos reuse**, salvo que una celda comparable requiera otra proporción previamente aprobada. Las dos piezas reuse no deben ocupar siempre el mismo horario; se rotan para no confundir reuse con franja.

### 4.2 Día de cinco publicaciones

| Slot | Tipo de pieza | Función editorial |
|---|---|---|
| 10:00 | Nueva — situación relatable | Aumentar identificación temprana |
| 11:00 | `Reuse_Top` o nueva validada | Conservar un ancla con evidencia |
| 13:30 | Nueva — difusión mínima | Buscar shares y etiquetas |
| 17:00 | Nueva — personaje, diálogo o microhistoria | Variar el lenguaje narrativo |
| 19:00 | Nueva — remate de cierre | Proteger la oportunidad de un acierto fuerte |

El día de cinco no es un día de menor calidad. Solo elimina las condiciones de 16:00 y 22:00 para controlar la carga y conservar una lectura más limpia de viernes y sábado.

### 4.3 Séptimo slot del domingo

El séptimo slot de las 17:00 solo se habilita si existe una pieza **nueva, aprobada, visualmente consistente, sin conflicto de personaje/canon y con caption ya cerrado**. No puede ser un reuse elegido a última hora. Se registra como `Exploratorio_Domingo_17`, queda fuera de cualquier conclusión de horario hasta reunir suficientes casos y no desplaza la pieza de las 19:00.

## 5. Mezcla de contenido y reglas de reuse

La cartera objetivo de los próximos bloques sigue siendo aproximadamente **65%–70% contenido nuevo y 30%–35% reuse**, con un máximo ordinario de dos reuse por día. La aplicación 22–30 priorizó recuperar el piso de volumen con assets reales: el tramo quedó en 26 filas `Nueva`, 21 `Reuse_Top` y 3 `Reuse_Reserve`, sin rellenar huecos con reuse no validado. La transición se considera correcta en su primera dimensión cuando cada día alcanza al menos cinco publicaciones reales; la mezcla objetivo se optimizará en los siguientes bloques con más producción nueva.

| Banda diaria | Nuevas | Reuse permitido | Exploratorio | Regla |
|---|---:|---:|---:|---|
| 5 slots | 3–4 | 1–2 | 0–1 | Nunca rellenar un slot con reuse no validado |
| 6 slots | 4 | 2 | 0–1 | Al menos una pieza nueva debe responder una hipótesis concreta |
| 7 slots | 5 | 2 | 1 | El séptimo es opcional y siempre queda marcado como exploratorio |

Un `Reuse_Top` debe proceder de la `Reuse Queue`, tener antigüedad suficiente, contar con asset exacto y no haber sido republicado recientemente. El reuse se rota por horarios y familias; no se coloca siempre en la franja de mayor expectativa. Una pieza reuse no se convierte automáticamente en una nueva evidencia de la familia original si cambia el caption, el formato o la plataforma.

La cartera diaria debe evitar repetir el mismo personaje principal en slots consecutivos, salvo que el concepto sea explícitamente secuencial. No se asigna un personaje solo para llenar una columna. Si la escena no contiene una identidad canónica clara, se registra como `Personaje_No_Identificado` o como personaje secundario, sin inferirlo por el filename.

## 6. Distribución de familias y tratamientos

Para que la frecuencia no destruya la consistencia, cada día de seis piezas debe cubrir al menos tres funciones editoriales: una situación relatable, una pieza de difusión mínima y una pieza narrativa o de conflicto. El cuarto slot funcional se asigna a la hipótesis que esté activa esa semana.

| Función | Familias candidatas | Pregunta que responde |
|---|---|---|
| Identificación | `Relatable_Social`, autodesprecio/antihéroe | ¿La situación es reconocible sin contexto adicional? |
| Difusión | `Difusión_Minimal`, transformación visual simple | ¿La pieza se puede compartir o etiquetar con baja fricción? |
| Conversación | `Ácido_Interpersonal`, diálogo ácido | ¿El conflicto abre comentarios sin depender de explicación? |
| Narrativa | Microhistoria secuencial, reacción visual | ¿La secuencia se entiende y produce un payoff? |
| Reels | `HB-REEL-MOTION-POV-MEME-01` | ¿El movimiento y el hook POV/meme mejoran el descubrimiento? |

Los treatments `caption_minimo`, `caption_refuerzo` y `caption_conversacional` se asignan antes de la publicación y se registran por separado. No se puede llamar “caption conversacional” a una pregunta añadida después de observar el resultado. En una semana normal, ningún treatment debe dominar todos los slots de una misma familia.

Las piezas de Reels se mantienen fuera de la tabla principal de imágenes. Se registran en la capa L1 diaria y se enriquecen con Windsor o Instagram cuando haya views, reach o retención disponibles. La falta de un campo se guarda como `null` o `Unavailable`, nunca como cero. [3]

## 7. Flujo operativo diario

### D–2: selección de cartera

Se revisa el reporte diario más reciente y se anotan únicamente las señales que puedan cambiar una decisión. Se seleccionan los slots del día D desde el inventario, la `Production Queue` y la `Reuse Queue`. Para cada fila se fija `Experiment_ID`, familia, formato, personaje principal, personajes secundarios, rol narrativo, treatment, tipo de contenido, slot y función editorial.

La selección debe producir una cartera principal de cinco o seis piezas y, cuando corresponda, una reserva de una pieza. La reserva no se publica automáticamente: existe para cubrir un fallo de preflight, pero cualquier sustitución requiere aprobación humana y debe conservarse la diferencia entre slot planeado y slot real.

### D–1: producción y revisión

Se verifican el original de Drive, el nombre exacto, la dimensión, la identidad visual, el estado de canon, el caption, los hashtags del kit USM y la compatibilidad con la plataforma. La revisión se hace por fila, no por lote abstracto. Las piezas que dependen de una referencia oficial deben conservar el enlace o Drive ID de origen.

Antes del cierre D–1 se congela la cartera: no se cambian simultáneamente familia, personaje, caption y horario. Si una pieza no pasa el control, se marca `Bloqueada_Preflight`; no se compensa con una publicación improvisada.

### Día D: ejecución y registro

La publicación se ejecuta solo con aprobación humana y con la orden de plataforma claramente definida. Facebook e Instagram se mantienen separados. Para Facebook se registran Page Post ID, Photo ID o Reel ID, permalink, hora local real y estado de publicación. Para Instagram se registra el flujo real —contenedor, publicación o error— sin afirmar programación si solo se creó un contenedor.

Cada publicación debe actualizar el `Publication_Log` y dejar el asset operativo en la carpeta mensual correspondiente de Drive conforme al flujo aprobado. No se crean copias y no se archiva un original si Meta devolvió un error o si el ID no pudo verificarse. [4]

### D+1: corte diario y aprendizaje

El corte diario registra todas las publicaciones que existan hasta la hora de extracción, separando imágenes, Reels, Instagram y afiliados. Se calculan interacciones observables, shares, comentarios, mediana, top 1/top 5 y desviaciones horarias. El reporte diario es la fuente principal de aprendizaje; no se presenta un acumulado lifetime como delta de 24 horas.

Las familias y personajes solo se comparan cuando el denominador esté explícito. Una observación diaria puede reforzar o debilitar direccionalmente una hipótesis, pero no la canoniza. La conclusión debe decir si una señal queda `compatible`, `exploratoria`, `no evaluable` o `requiere más casos`.

## 8. Preflight obligatorio por pieza

| Control | Criterio de aprobación | Acción si falla |
|---|---|---|
| Asset | Archivo exacto y Drive ID verificable | Bloquear; no sustituir sin aprobación |
| Formato | Imagen, Reel u otro correctamente declarado | Separar del denominador principal |
| Identidad | Personajes y anclas visuales verificadas | Corregir antes de producir/publicar |
| Composición | Remate legible sin explicación adicional | Volver a revisión editorial |
| Caption | Treatment y función registrados por separado | No publicar hasta cerrar copy |
| Hashtags | Solo etiquetas permitidas por el kit USM | Corregir y volver a validar |
| Hipótesis | Una pregunta concreta o `Exploratorio` | No incluir en una celda por inercia |
| Reuse | Antigüedad, historial y asset exactos | Excluir o mover a reserva |
| Afiliados | Link/producto registrado aparte | No mezclar con engagement editorial |
| Plataforma | Facebook/Instagram claramente indicada | Detener la orden |

El preflight debe terminar con una de cuatro decisiones: `Aprobada`, `Aprobada_Con_Nota`, `Bloqueada_Preflight` o `Reserva`. No se utiliza `Pendiente` como sustituto de una decisión cuando el slot ya debe ejecutarse.

## 9. Medición y reglas de ajuste

La métrica de presencia será el número de publicaciones reales por día. La métrica de calidad típica será la mediana de interacciones por pieza. Shares por pieza y `shares/interacciones` funcionarán como señales de difusión; comentarios y respuestas se leerán como señales de conversación. Los Reels se miden en una tabla separada con el protocolo L0–L4.

| Señal observada en dos o más cortes | Ajuste operativo |
|---|---|
| Menos de cinco publicaciones reales sin causa documentada | Revisar capacidad de producción y reducir slots antes de rellenar |
| Más de un slot vacío por falta de preflight | Aumentar la reserva aprobada, no el reuse improvisado |
| Mediana descendente mientras sube la frecuencia | Revisar calidad y mezcla; no aumentar a siete |
| Top 1/top 5 concentran excesivamente el MTD | Mantener la búsqueda de outliers, pero elevar la cartera media |
| Shares estables o crecientes con menor volumen | Conservar las funciones de difusión y revisar la cadencia |
| Una familia o personaje domina por un solo post | Marcar como outlier y exigir casos comparables |
| Reels sin views/reach/retención | Mantener L1 y buscar enriquecimiento L2/L3; no escribir ceros |

Como regla de continuidad, una familia puede recibir más slots solo si tiene al menos tres casos comparables con señal direccional y cinco para un veredicto operativo. Una franja no se reordena por una sola publicación viral. La decisión semanal debe considerar mediana, shares, concentración de outliers, calidad de preflight y porcentaje de slots realmente ejecutados.

## 10. Checklist de cierre diario

| Paso | Evidencia mínima |
|---|---|
| Conteo de ejecución | Número real de publicaciones, slots vacíos y desviaciones |
| Identidad | Meta ID, permalink, asset y Drive ID por fila |
| Mezcla | Nueva, `Reuse_Top`, experimento y exploratorio separados |
| Formato | Imágenes y Reels en denominadores distintos |
| Comunidad | Comentarios raíz, replies y moderación incremental sin identidades personales |
| Afiliados | Links, productos, clicks y ventas en ledger separado |
| Aprendizaje | Hipótesis compatible, exploratoria, no evaluable o requiere casos |
| Próximo día | Ajuste concreto sin modificar más de una variable crítica a la vez |

## 11. Qué no se debe hacer

No se debe publicar siete piezas solo para alcanzar una cifra, colocar reuse al final del mes por comodidad, asignar personajes por filename, cambiar captions después de ver resultados, mezclar imágenes con Reels, sumar afiliados al engagement editorial, rellenar huecos con assets no aprobados, ni convertir el rendimiento de un outlier en canon.

Tampoco se debe modificar el calendario activo, cancelar programaciones, mover assets en Drive o publicar en Facebook/Instagram solo porque este playbook recomiende una banda de frecuencia. Esas son acciones operativas separadas y requieren aprobación humana explícita. En la aplicación del 22 de agosto sí existió esa autorización: se añadieron cuatro slots sin cancelar filas, mientras que los tres reemplazos MEME-CAD se ejecutaron bajo una autorización específica separada.

## 12. Gate antes de aplicar

Antes de aplicar esta matriz a un calendario nuevo, Fernando debe confirmar tres cosas: que existe capacidad para producir al menos cinco piezas aprobadas por día; que la reserva de assets exactos está disponible sin depender de reuse improvisado; y que acepta mantener Reels, Instagram y afiliados fuera del denominador principal de imágenes. Para la aplicación 22–30, Fernando confirmó expresamente la ampliación, y el preflight verificó los cuatro assets adicionales y sus horarios.

Después de la aprobación, se prepara un CSV de revisión humana con una fila por slot. Solo tras la aprobación del CSV o una autorización equivalente, explícita y acotada por alcance, se puede programar o publicar. La aplicación 22–30 quedó en un documento y un ledger nuevos, enlazados desde el calendario activo; no se sobrescribieron las filas existentes y los cuatro slots se añadieron como registros verificables.

## Referencias

[1]: 2026-08-22_Comparativa_Junio_Julio_Agosto_y_Brechas_Integracion.md "Comparativa de crecimiento y brechas de integración — junio, julio y agosto 2026"
[2]: 2026-08-16_Calendario_Operativo_17_30_Agosto.md "Calendario operativo 17–30 de agosto"
[3]: 2026-08-22_Reels_Metric_Instrumentation_Protocol.md "Protocolo de instrumentación L0–L4 de Reels"
[4]: ../../GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md "Pipeline de publicación local y estándar CSV"
