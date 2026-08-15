# Diseño de Prueba de Calendario — Dos Semanas

**Propósito:** Diseñar una prueba controlada para medir el efecto conjunto de la frecuencia, el tipo de contenido —nuevo frente a reuse— y las franjas horarias preferidas por la audiencia de Universe Sent Me, sin modificar todavía el calendario operativo vigente.

**Estado:** Review  
**Fecha de creación:** 2026-08-14  
**Última actualización:** 2026-08-14  
**Versión:** 1.2
**Autor:** Manus AI  
**Documentos relacionados:** [`GrowthOS/05_03_Calendario_10_16_Agosto.md`](../../GrowthOS/05_03_Calendario_10_16_Agosto.md), [`Operations/Research/2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto.md`](2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto.md), [`Operations/Research/2026-08-14_Ciclo_Aprendizaje_Horarios.md`](2026-08-14_Ciclo_Aprendizaje_Horarios.md), [`GrowthOS/Integracion_Growth_OS.md`](../../GrowthOS/Integracion_Growth_OS.md), [`GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md`](../../GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md)

---

## 1. Decisión de diseño

La prueba se ejecutará durante **14 días**, con una frecuencia diferenciada por día: **seis publicaciones de lunes a jueves, cuatro el viernes, cuatro el sábado y cinco el domingo**. Esta matriz aumenta la presencia en los días laborales principales, conserva el patrón reducido de viernes y sábado, y reserva el domingo como día estelar sin mezclarlo con la lógica de lunes a sábado.

El formato primario será **imagen estática o meme**, porque la prueba busca comparar horario, frecuencia y reuse sin introducir la variable adicional de Reel, carrusel o video. Los Reels y carruseles podrán publicarse si existe una obligación editorial, pero quedarán fuera del cálculo principal y deberán registrarse como `Exploratorio`.

> **Experimento:** `EXP-2026-08-CAL-01`  
> **Hipótesis relacionadas:** `HB-003` horarios, `HB-004` saturación por reuse y `HB-005` superficie de descubrimiento/frecuencia.

## 2. Matriz horaria propuesta

La matriz mantiene los horarios preferidos de media mañana y tarde, pero formaliza el domingo nocturno como una condición específica. No se trata de afirmar que todos los horarios nocturnos funcionan; se trata de medirlos sin mezclarlos con el comportamiento de lunes a sábado.

| Tipo de día | Slot 1 | Slot 2 | Slot 3 | Slot 4 | Slot 5 | Slot 6 | Frecuencia fija |
|---|---:|---:|---:|---:|---:|---:|---:|
| Lunes–jueves | 10:00 | 11:00 | 13:30 | 16:00 | 17:00 | 19:00 | 6 posts |
| Viernes | 10:00 | 11:00 | 13:30 | — | 19:00 | — | 4 posts |
| Sábado | 10:00 | 11:00 | 13:30 | — | 19:00 | — | 4 posts |
| Domingo estelar | 10:00 | 13:30 | 16:00 | 19:00 | 22:00 | — | 5 posts |

La franja de 13:30 representa el intervalo flexible de 13:00–14:00. De lunes a jueves se añade una publicación a las 19:00. El viernes adopta el patrón del sábado: se elimina la publicación de las 16:00 y la de las 17:00 se mueve a las 19:00. El domingo conserva su matriz estelar: 10:00, 13:30, 16:00, 19:00 y 22:00; la condición nocturna se mantiene como señal exploratoria. Los horarios deben registrarse en hora local de Ciudad de México y ejecutarse con una tolerancia máxima de ±10 minutos. Si una publicación se retrasa más de 30 minutos, se conserva su hora real y se marca `Desviación_Horaria = Sí`; no se debe corregir artificialmente el dato.

El domingo nocturno se mantiene porque existe una observación cualitativa consistente de mayor tráfico y desvelo, pero durante estas dos semanas solo producirá una señal exploratoria. Con dos domingos no se puede cerrar una hipótesis sobre el comportamiento dominical; el resultado servirá para decidir si se extiende el test.

## 3. Mezcla de contenido controlada

Los días de seis publicaciones tendrán cuatro piezas nuevas y dos reuse; viernes y sábado, con cuatro slots, tendrán dos piezas nuevas y dos reuse; el domingo mantendrá tres piezas nuevas y dos reuse. En el total de 14 días esto produce **46 piezas nuevas y 28 reuse** en 74 slots, aproximadamente 62% contenido nuevo y 38% reuse. La expansión aumenta frecuencia mediante contenido nuevo y no mediante saturación adicional de reuse. La pieza reutilizada debe ser `Reuse_Top`: una pieza de mayo validada por datos, con más de 30 días de antigüedad y sin republicación reciente.

| Tipo | Cantidad diaria | Cantidad en 14 días | Regla |
|---|---:|---:|---|
| Contenido nuevo | 4 en días de 6 slots; 2 en viernes/sábado; 3 el domingo | 46 | Debe estar aprobado para producción y etiquetado por personaje, formato y copy |
| Reuse top | 2 por día | 28 | Debe proceder de la Reuse Queue y cumplir antigüedad mínima |
| Exploratorio fuera del test | Variable | No contado | Reel/carrusel u otra pieza no comparable; registrar por separado |

Para no confundir horario con tipo de contenido, las piezas reuse no ocuparán siempre los mismos slots. Se rotarán entre 10:00, 11:00, 13:30, 16:00, 17:00 y 19:00 de lunes a jueves; el viernes entre 10:00, 11:00, 13:30 y 19:00; el sábado entre 10:00, 13:30 y 19:00; y el domingo entre 10:00, 13:30, 16:00, 19:00 y 22:00. La rotación no pretende ser una aleatorización estadística perfecta, pero evita que reuse quede permanentemente asociado al horario de menor o mayor rendimiento.

La rotación recomendada es:

| Día de prueba | Slots de reuse |
|---|---|
| Día 1 | 10:00 y 16:00 |
| Día 2 | 11:00 y 17:00 |
| Día 3 | 13:30 y 10:00 |
| Día 4 | 16:00 y 13:30 |
| Día 5 | 17:00 y 11:00 |
| Día 6, sábado | 10:00 y 19:00 |
| Día 7, domingo | 16:00 y 22:00 |
| Días 8–14 | Repetir la secuencia invirtiendo el orden cuando sea posible |

El objetivo no es demostrar que todo contenido nuevo supera a todo reuse. El objetivo es saber si **una proporción limitada de reuse top mantiene la presencia y permite que la mayoría de los slots explore contenido nuevo**.

## 4. Reglas para que la prueba sea interpretable

Durante las dos semanas no se debe cambiar la matriz diferenciada, añadir publicaciones espontáneas dentro de los slots definidos, mover sistemáticamente los horarios o cambiar la proporción aproximada 62/38. Si una pieza no está lista, el slot debe quedar vacío y registrarse como `Slot_No_Publicado`; no se debe rellenar con reuse improvisado.

El contenido nuevo debe distribuir razonablemente los personajes y evitar que una semana sea dominada por un solo personaje. Tampoco se deben comparar directamente Reels, carruseles y memes estáticos en la misma tabla. Las publicaciones exploratorias podrán existir, pero deben tener una etiqueta de exclusión.

La prueba se ejecutará primero en Facebook, que es el canal con histórico suficiente. Instagram puede recibir la misma pieza cuando el asset cumpla los requisitos de Graph API, pero sus métricas se analizarán aparte y no se mezclarán con Facebook.

## 5. Registro obligatorio por publicación

Cada fila del `ExperimentLog` debe incluir los siguientes campos antes de publicar y completar los resultados después de la extracción de métricas:

| Campo | Ejemplo |
|---|---|
| `Experiment_ID` | `EXP-2026-08-CAL-01` |
| `Hypothesis_ID` | `HB-003`, `HB-004` o `HB-005` |
| `Fecha_Local` | `2026-08-18` |
| `Slot_Planeado` | `13:30` |
| `Hora_Real` | `13:34` |
| `Tipo_Contenido` | `Nueva` o `Reuse_Top` |
| `Formato` | `Imagen estática` |
| `Personaje` | `Universe` |
| `Día_Semana` | `Martes` |
| `ID_Meta` | ID devuelto por Graph API |
| `Estado_Publicación` | `Programada`, `Publicada`, `Fallida` |
| `Interacciones_24h` | Reacciones + comentarios + shares |
| `Interacciones_72h` | Reacciones + comentarios + shares |
| `Shares_24h` | Conteo de shares |
| `Desviación_Horaria` | `Sí` / `No` |
| `Incluida_En_Test` | `Sí` / `No` |
| `Notas` | Incidencias o contexto relevante |

## 6. Métricas y criterios de decisión

La métrica primaria de resultado de página será **interacciones totales por día**, porque mide la superficie agregada de distribución. La métrica primaria de calidad típica será la **mediana de interacciones por publicación**, porque evita que un solo viral domine la conclusión. Las métricas secundarias serán shares por publicación y `shares / interacciones`.

La prueba no se considerará cerrada si solo mejora una publicación viral. Para considerar que una franja o mezcla merece continuar, debe cumplir tres condiciones: tener al menos seis observaciones comparables cuando sea posible; mejorar la mediana frente a la referencia; y no depender de un solo outlier.

| Pregunta | Métrica principal | Decisión posible |
|---|---|---|
| ¿La frecuencia de seis posts de lunes a jueves y cuatro viernes/sábado mantiene presencia suficiente? | Interacciones totales/día | Mantener, subir o bajar frecuencia |
| ¿El 38% aproximado de reuse top es sostenible? | Mediana por `Nueva` vs `Reuse_Top` | Mantener reuse, reducirlo o ampliar su uso selectivo |
| ¿Funcionan las franjas de media mañana? | Mediana por slot 10:00/11:00 | Mantener o redistribuir slots |
| ¿Funciona la tarde? | Mediana por 13:30/16:00/17:00 | Comparar con media mañana |
| ¿El domingo nocturno tiene señal especial? | Mediana domingo 19:00/22:00 | Extender test; no concluir todavía con dos domingos |
| ¿Hay canibalización? | Interacciones/día frente a mediana/post | Separar crecimiento agregado de calidad individual |

## 7. Qué se podrá concluir y qué no

Al finalizar dos semanas se podrá determinar si la frecuencia diferenciada —seis publicaciones de lunes a jueves, cuatro viernes/sábado y cinco domingo— mantiene un rendimiento diario superior al régimen reducido de agosto, si la mezcla aproximada 62/38 es operativamente sostenible y si aparecen señales iniciales a favor de media mañana, tarde, 19:00 o domingo nocturno.

No se podrá concluir todavía cuál es el mejor horario universal de la audiencia, si la mayoría de los usuarios son no seguidores, ni si al crecer la Página será posible publicar menos. Esas preguntas requieren más tiempo, datos históricos de seguidores y, cuando estén disponibles, alcance e impresiones desglosados por publicación.

## 8. Próximo paso antes de tocar el calendario

Antes de modificar `05_03_Calendario_10_16_Agosto.md`, Fernando debe confirmar que acepta la matriz de seis publicaciones de lunes a jueves, cuatro viernes/sábado y cinco el domingo, y que dispone de aproximadamente 46 piezas nuevas y 28 piezas reuse top para completar los 74 slots de la prueba. Si no existe esa capacidad de producción, habrá que reducir la frecuencia antes de crear el calendario experimental, sin rellenar huecos con reuse improvisado.

Una vez confirmado el diseño, se creará el calendario experimental como documento nuevo o como copia de trabajo vinculada a este protocolo. El calendario histórico no se sobreescribirá.

### Referencias

[1]: ../../GrowthOS/05_03_Calendario_10_16_Agosto.md — Preferencias y cambios de horario registrados para el 10–16 de agosto.
[2]: 2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto.md — Comparación histórica de frecuencia y rendimiento.
[3]: 2026-08-14_Ciclo_Aprendizaje_Horarios.md — Hipótesis HB-003 y criterios iniciales de cierre.
[4]: ../../GrowthOS/Integracion_Growth_OS.md — HypothesisBank y ExperimentLog.
[5]: ../../GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md — Campos operativos del pipeline de publicación.
