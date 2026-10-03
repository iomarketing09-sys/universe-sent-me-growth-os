# Roadmap de Implementación para el Plan de Crecimiento de Firma Bordados

## Objetivo
Proveer un plan de acción priorizado y secuencial para pasar de la documentación a la ejecución práctica del plan de crecimiento, enfocado en aspectos que puedan implementarse sin modificar el sitio web de Firma Bordados.

## Principios de Priorización
1. **Impacto Alto, Esfuerzo Bajo**: Acciones que generen mejoras significativas con poca inversión
2. **Dependencias Claras**: Acciones que habiliten otras mejoras futuras
3. **Uso de Recursos Existentes**: Aprovechar herramientas, scripts y procesos ya disponibles
4. **Medibilidad**: Acciones que permitan tracking claro de resultados

## Fase 1: Fundación (Semanas 1-2) - Impacto Inmediato

### Acción 1.1: Establecer el Proceso de Validación de Assets (Punto 2)
- **Qué hacer**: Implementar el flujo básico de exportación y normalización de assets desde Google Drive hacia el CSV de GrowthOS
- **Por qué primero**: Es la base para todas las demás acciones; sin assets correctamente catalogados, no podemos publicar ni experimentar
- **Cómo hacerlo**:
  1. Crear un script simple `export_drive_inventory.py` en `growthos/scripts/` que:
     - Liste archivos en `Firma Bordados/` y subcarpetas de Drive
     - Extraiga nombre, ID, tipo MIME, ruta relativa
     - Genere CSV temporal con campos básicos (nombre, ID, tipo)
  2. Probar con una carpeta de prueba antes de aplicar a producción
  3. Definir reglas iniciales de mapeo (extensión→Tipo_Contenido, palabras clave básicas)
- **Recursos necesarios**: 1-2 horas de trabajo de alguien familiarizado con Python y Google Drive API
- **Resultado esperado**: Capacidad para generar un CSV básico de assets desde Drive
- **Métrica de éxito**: CSV generado con al menos 10 assets correctamente mapeados

### Acción 1.2: Implementar Plantillas de Copy V2 y Horarios de Impacto (Parte del Punto 1)
- **Qué hacer**: Comenzar a usar sistemáticamente las plantillas de copy y horarios de impacto en las publicaciones existentes
- **Por qué primero**: No requiere cambios tecnológicos, solo disciplina y seguimiento
- **Cómo hacerlo**:
  1. Imprimir y distribuir las Plantillas de Copy V2 al equipo de contenido
  2. Crear un calendario de publicación compartido (Google Sheets) con las franjas horarias:
     - Mañana: 08:30-09:30 (Venta directa/Educativo)
     - Tarde: 14:00-15:30 (Trabajo del día)
     - Noche: 19:30-21:00 (Interacción/Confianza)
     - Domingo: 20:00-21:00 (Reel resumen)
  3. Asignar responsable diario para verificar que se sigan los horarios y plantillas
- **Recursos necesarios**: 30 minutos de setup + disciplina diaria
- **Resultado esperado**: Todas las publicaciones siguen horarios establecidos y usan estructura de copy consistente
- **Métrica de éxito**: ≥ 90% de cumplimiento de horarios y uso de plantillas en 2 semanas

### Acción 1.3: Iniciar el Marco de Hipótesis (Documento de Hipótesis)
- **Qué hacer**: Lanzar el primer experimento estructurado usando el marco de validación de hipótesis
- **Por qué primero**: Comienza el ciclo de aprendizaje que mejorará todo lo demás con el tiempo
- **Cómo hacerlo**:
  1. Seleccionar una hipótesis simple y de alto impacto basada en observaciones (ej. HB-002: Las publicaciones con preguntas generan más comentarios)
  2. Documentar completamente el experimento usando el formato del marco de hipótesis
  3. Ejecutar durante una semana con 3-5 publicaciones por variante
  4. Extraer métricas y validar/rechazar la hipótesis
- **Recursos necesarios**: 1 hora para setup + tiempo normal de creación de contenido
- **Resultado esperado**: Primer aprendizaje documentado y accionable
- **Métrica de éxito**: Hipótesis probada, resultado documentado, decisión tomada basada en datos

## Fase 2: Consolidación (Semanas 3-4) - Construyendo Capacidades

### Acción 2.1: Automatizar la Exportación y Importación de Assets
- **Qué hacer**: Convertir el proceso manual de Acción 1.1 en un flujo semi-automatizado
- **Cómo hacerlo**:
  1. Mejorar `export_drive_inventory.py` para incluir:
     - Mapeo de extensión a Tipo_Contenido (PDF, Imagen, Video)
     - Detección básica de palabras clave para Categoria y Tipo_Contenido específico
     - Generación de IDs secuenciales (CNT-####) evitando duplicados
     - Salida a `pieces_firmabordados_ready.csv` listo para importar
  2. Crear script de validación que ejecute `audit_inventory.py` y reporte C_REAL
  3. Documentar procedimiento: "Ejecutar exportador → validar → importar si C_REAL=0"
- **Recursos necesarios**: 3-4 horas de trabajo de desarrollo
- **Resultado esperado**: Proceso repetible y confiable para mantener el inventario actualizado
- **Métrica de éxito**: Se puede ejecutar el proceso completo en <15 minutos con resultados consistentes

### Acción 2.2: Establecer el Ciclo de Publicación y Métricas (Punto 3)
- **Qué hacer**: Implementar el flujo completo desde la idea hasta la captura de métricas
- **Cómo hacerlo**:
  1. Definir roles claros: Ideación → Copy/Asset Prep → Programación → Publicación → Difusión Táctica → Métricas
  2. Crear checklist diario/semanal para cada fase del flujo
  3. Programar extracción automática de métricas a las 22:00 usando los scripts existentes (`extract_metrics_24_72.py`)
  4. Reunión semanal de 30 minutos para revisar métricas de la semana pasada
- **Recursos necesarios**: 2 horas de setup + adaptación de roles existentes
- **Resultado esperado**: Proceso completo de publicación medible y repetible
- **Métrica de éxito**: Ciclo completado exitosamente para al menos 3 piezas consecutivas

### Acción 2.3: Primera Reunión de Validación de Hipótesis
- **Qué hacer**: Reunir al equipo para revisar los resultados de la hipótesis piloto y planificar la siguiente
- **Cómo hacerlo**:
  1. Presentar resultados del experimento usando el formato de registro de experimento
  2. Decidir: Validar/Rechazar/Reformular
  3. Si se valida: determinar cómo actualizar plantillas de copy o tácticas
  4. Si se rechaza: documentar aprendizaje y descartar
  5. Planificar siguiente hipótesis basada en aprendizajes y datos observados
- **Recursos necesarios**: 1 hora de reunión + preparación
- **Resultado esperado**: Proceso de aprendizaje institucionalizado
- **Métrica de éxito**: Reunión realizada, decisiones documentadas, próxima hipótesis planificada

## Fase 3: Optimización (Semanas 5-6) - Escalando lo que Funciona

### Acción 3.1: Implementar el Reporte Semanal de Experimentos
- **Qué hacer**: Crear el reporte markdown sugerido en el marco de hipótesis
- **Cómo hacerlo**:
  1. Usar la plantilla del marco de hipótesis para generar reporte semanal
  2. Incluir: hipótesis probadas, resultados, validaciones, aprendizajes, próximos pasos
  3. Distribuir a todo el equipo de growth y contenido
  4. Archivar en carpeta de conocimiento para referencia futura
- **Recursos necesarios**: 30 minutos por semana una vez estable el proceso
- **Resultado esperado**: Conocimiento acumulado y accesible para todo el equipo
- **Métrica de éxito**: Reportes semanales consistentes con mejora visible en hipótesis probadas

### Acción 3.2: Optimizar basado en Aprendizajes
- **Qué hacer**: Aplicar los aprendizajes validados para mejorar el contenido
- **Cómo hacerlo**:
  1. Actualizar Plantillas de Copy V2 con lo que haya funcionado
  2. Ajustar guías de horarios si se descubre que ciertos bloques funcionan mejor
  3. Modificar criterios de selección de assets basado en lo que genere mejor engagement
  4. Comunicar cambios claramente al equipo
- **Recursos necesarios**: Tiempo de actualización de documentos + comunicación
- **Resultado esperado**: Mejora continua en la efectividad del contenido
- **Métrica de éxito**: Tendencia positiva en métricas clave (interacciones, CTR, alcance) durante 4-6 semanas

### Acción 3.3: Establecer el Repositorio de Hipótesis
- **Qué hacer**: Crear una biblioteca de conocimiento de todas las hipótesis probadas
- **Cómo hacerlo**:
  1. Crear carpeta `/home/universe-sent-me/new-growth-os/docs/hipotesis/` (o en Google Drive)
  2. Archivar cada registro de experimento completado usando formato estándar
  3. Mantener índice maestro con: ID, hipótesis, resultado, fecha, aprendizaje clave
  4. Usar este repositorio para evitar duplicados y construir sobre aprendizajes previos
- **Recursos necesarios**: 1 hora de setup + 10 minutos por experimento
- **Resultado esperado**: Base de conocimiento acumulativa que evita repetir errores
- **Métrica de éxito**: Repositorio con ≥5 hipótesis documentadas y accesible para el equipo

## Fase 4: Escalabilidad y Refinado (Semana 7+) - Operación Estable

### Acción 4.1: Ritmo de Mejora Continua
- **Qué hacer**: Institutionalizar los ciclos de aprendizaje y mejora
- **Cómo hacerlo**:
  - **Diario**: Verificación de cumplimiento de horarios y plantillas
  - **Semanal**: 
    - Lunes: Revisión de métricas de semana pasada + planificación de publicaciones
    - Miércoles: Checkpoint intermedio (opcional)
    - Viernes: Preparación para extracción de métricas + validación de hipótesis en curso
    - Domingo (o lunes): Reunión de revisión de gates y hipótesis (30-45 min)
  - **Mensual**: Reporte de aprendizajes y actualización de mejores prácticas
- **Resultado esperado**: Operación estable con mejora continua medible

### Acción 4.2: Medición de Impacto y ROI
- **Qué hacer**: Establecer línea de base y medir mejora con el tiempo
- **Cómo hacerlo**:
  1. Tomar métricas de línea de base de las 4 semanas pre-implementación (usar datos históricos disponibles)
  2. Medir cambio porcentual en:
     - Interacciones promedio por publicación
     - CTR a WhatsApp
     - Alcance orgánico promedio
     - Porcentaje de hipótesis validadas
     - Cumplimiento de horarios y plantillas
  3. Reportar mejora trimestral
- **Resultado esperado**: Caso de negocio claro para la inversión en este proceso
- **Métrica de éxito**: Mejora medible en KPIs clave después de 8 semanas

## Métricas de Éxito General para el Roadmap

| Métrica | Línea de Base (Estimada) | Meta a 8 semanas | Método de Medición |
|---------|--------------------------|------------------|-------------------|
| Interacciones por publicación | 20-30 | ≥ 35 (+20-75%) | Promedio semanal de piezas_firmabordados.csv |
| CTR a WhatsApp | 1.5-2% | ≥ 2.5% (+25-66%) | De métricas de extracción 24/72h |
| % de publicaciones en horario correcto | < 50% | ≥ 90% | Auditoría semanal de timestamps |
| % de hipótesis validadas | N/A | ≥ 50% | De registro de hipótesis |
| Tiempo para publicar una pieza | > 2 horas | < 1 hora (con proceso establecido) | Tiempo de idea a publicación |

## Próximos Pasos Inmediatos (Día 1)

Si el equipo quiere comenzar hoy, recomiendo:

1. **Hoy (30 min)**: 
   - Reunir al equipo de contenido y explicar brevemente los horarios de impacto y plantillas de copy V2
   - Acordar intentar seguir estrictamente los horarios mañana y usar las plantillas en todo el copy

2. **Mañana (2 horas)**:
   - Designar a una persona para crear el script básico de exportación de assets (versión 0.1)
   - Otro miembro comenzar a documentar la primera hipótesis basada en una observación reciente

3. **Pasado mañana (1 hora)**:
   - Probar el script de exportación en un subconjunto de assets
   - Revisar la hipótesis documentada y asegurar que siga el formato

4. **Al final de la semana 1**:
   - Tener al menos una pieza siguiendo el nuevo flujo completo (idea → copy/asset → programación → publicación)
   - Tener la primera hipótesis lista para probar la semana siguiente

Este roadmap proporciona un camino claro desde la documentación actual hacia una operación estable, medible y en mejora continua, todo enfocado en maximizar la efectividad de las publicaciones en Facebook e Instagram dentro de las restricciones establecidas (sin modificar el sitio web).

¿Le gustaría que desarrolle alguno de estos puntos en mayor detalle, o prefiere que comencemos con la primera acción recomendada?
