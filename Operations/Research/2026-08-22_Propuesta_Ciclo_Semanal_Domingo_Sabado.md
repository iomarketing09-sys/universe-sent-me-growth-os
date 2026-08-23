# Propuesta de ciclo semanal: domingo–sábado

**Propósito:** Evaluar y proponer una convención de reporte semanal que cierre el sábado y abra el siguiente ciclo operativo el domingo, sin confundir el calendario de análisis con una prueba causal ni modificar la programación activa de Facebook.

**Estado:** Draft
**Fecha de creación:** 2026-08-22
**Última actualización:** 2026-08-22
**Versión:** 0.1
**Autor:** Manus AI (CGO)
**Organización:** `Operations/Research/`
**Documentos relacionados:** `GrowthOS/04_00_Formato_Calendario_Semanal_CGO.md`, `GrowthOS/00_Índice.md`, `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`, `Operations/Research/2026-08-19_Windsor_Facebook_Organic_28D_Normalizado.json`, `Operations/Research/2026-08-22_Corte_Diario_Metricas_2200.md`

---

## 1. Propuesta ejecutiva

Se propone que el **ciclo de reporte y aprendizaje** de Universe Sent Me se defina de **domingo a sábado**. El sábado se realiza el corte general de la semana después del último slot con exposición mínima razonable; el domingo se considera el primer día del nuevo ciclo operativo y editorial.

Esta convención es recomendable por organización y continuidad de aprendizaje, pero no debe presentarse como prueba de que el domingo sea siempre el día de mayor rendimiento. La evidencia histórica de mayo sí identificó al domingo como el día de mayor engagement relativo, mientras que el dataset de Facebook más reciente de 28 días muestra una señal más matizada y no confirma que domingo supere a todos los demás días por publicación.

## 2. Evidencia disponible

La plantilla semanal basada en mayo reportó **domingo como el día de mayor engagement relativo, con 1.77% de ER**, y **50.3K vistas promedio**; lunes registró 80.8K vistas promedio. Esto respalda tratar domingo como un día estratégico, pero proviene de un baseline histórico agregado y no debe extrapolarse automáticamente al comportamiento actual. [1]

Para comprobar la hipótesis con una vista más reciente, se agregaron los 143 registros diarios de Facebook del periodo **22 de julio–18 de agosto de 2026**. La interacción observable por publicación se calculó como reacciones + comentarios + shares en los campos disponibles del dataset. Los valores son acumulados del registro consultado y están afectados por volumen desigual, outliers y mezcla editorial; no equivalen a una tasa de alcance ni a una comparación causal limpia. [2]

| Día | Posts | Interacciones observables | Promedio por post | Mediana por post |
|---|---:|---:|---:|---:|
| Lunes | 26 | 5,169 | 198.81 | 40.5 |
| Martes | 20 | 9,425 | 471.25 | 61.0 |
| Miércoles | 16 | 6,328 | 395.50 | 27.0 |
| Jueves | 19 | 3,707 | 195.11 | 33.0 |
| Viernes | 25 | 5,114 | 204.56 | 32.0 |
| Sábado | 18 | 2,665 | 148.06 | 49.5 |
| Domingo | 19 | 1,074 | 56.53 | 42.0 |

La lectura correcta es que **domingo no está demostrado como el día más fuerte en la ventana reciente de Facebook**: su mediana por publicación fue inferior a sábado y su promedio quedó muy afectado por un volumen total menor. Al mismo tiempo, el baseline de mayo y el diseño editorial vigente sí justifican mantener domingo como día de alta atención potencial. Ambas señales deben convivir sin borrar ninguna de las dos.

## 3. Cómo funcionaría el ciclo propuesto

| Momento | Función | Regla de medición |
|---|---|---|
| Domingo | Inicio del nuevo ciclo y primera jornada editorial | No se mezclan sus resultados con la semana cerrada el sábado anterior. |
| Lunes–viernes | Ejecución, producción y revisión de la programación | Los reportes diarios siguen siendo la fuente primaria de aprendizaje. |
| Sábado | Última jornada del ciclo y cierre general | Se captura el resumen después del último slot; el contenido recién publicado se marca como exposición inmadura. |
| Domingo siguiente | Inicio del ciclo posterior | Se compara domingo contra otros domingos, no contra todo el promedio semanal sin controles. |

El cierre no debe realizarse antes de que el último contenido relevante del sábado haya sido publicado. Para el esquema actual, el corte operativo recomendado es **después del slot final y no antes de las 22:15–22:30 en `America/Matamoros`**. Si el último post acaba de salir, se incluyen sus datos de identidad y estado, pero no se usa para juzgar rendimiento.

## 4. Reglas que deben permanecer separadas

La convención domingo–sábado afecta el **reporte, el aprendizaje y la organización del Growth OS**. No cambia por sí sola los horarios de Meta, la cadencia autorizada, los denominadores de imágenes, la medición de Reels, Instagram o afiliados, ni los límites de aprobación humana.

Las comparaciones históricas mensuales de junio, julio y agosto deben conservar sus límites calendarios originales. La nueva semana analítica será una vista adicional y no debe reescribir los agregados mensuales ni convertir acumulados lifetime en deltas diarios.

## 5. Recomendación del CGO

Recomiendo **adoptar la convención como Draft operativo**, sujeto a confirmación de Fernando, por tres motivos. Primero, coloca el domingo —que tiene respaldo histórico como día de interés— al inicio de la semana y permite preparar el ciclo con sus resultados frescos. Segundo, permite cerrar el aprendizaje el sábado sin esperar al lunes. Tercero, hace más fácil comparar bloques completos domingo–sábado y relacionarlos con la cadencia real.

No recomiendo declarar todavía que domingo es el día más fuerte. La evidencia actual respalda la frase más precisa: **domingo es un día estratégico que merece tratamiento separado y medición propia; su superioridad frente a todos los días aún requiere una muestra controlada de varios domingos**.

Para validarlo, se recomienda observar al menos **cuatro a seis ciclos domingo–sábado**, manteniendo separados formato, volumen, mezcla de nuevo/reuse, horario y outliers. La métrica de decisión debe priorizar la mediana por publicación y las señales de shares/comentarios, acompañadas por alcance cuando esté disponible.

## 6. Documentos que requerirían actualización si se aprueba

Si Fernando confirma la adopción, deberán actualizarse `GrowthOS/00_Índice.md` en su flujo de trabajo semanal, `GrowthOS/04_00_Formato_Calendario_Semanal_CGO.md`, el documento de arquitectura del calendario y el protocolo de reportes diarios. El estado de esta propuesta permanece **Draft** hasta esa aprobación; no se modifica la programación actual.

## Referencias

[1]: ../../GrowthOS/04_00_Formato_Calendario_Semanal_CGO.md "Formato de Calendario Semanal CGO — baseline de mayo 2026"
[2]: 2026-08-19_Windsor_Facebook_Organic_28D_Normalizado.json "Facebook orgánico normalizado — 28 días, 22 de julio a 18 de agosto de 2026"
