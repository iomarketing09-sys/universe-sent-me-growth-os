# Marco de Validación de Hipótesis para Firma Bordados

## Objetivo
Establecer un proceso sistemático para crear, probar, validar y aprender de hipótesis de marketing relacionadas con el contenido de Facebook e Instagram, mejorando continuamente la efectividad de las publicaciones mediante experimentación controlada.

## 1. Estructura de una Hipótesis (HB-XXX)

Cada hipótesis debe seguir este formato:

```
HB-###: [Declaración de la hipótesis]
- **Variable Independiente**: Qué se está cambiando/probando
- **Variable Dependiente**: Qué se está midiendo (métrica clave)
- **Población Objetivo**: Qué audiencia o segmento se está probando
- **Métrica de Éxito**: Umbral específico que define si la hipótesis se valida
- **Duración del Experimento**: Tiempo mínimo para recopilar datos suficientes
- **Relacionado con**: [Pilar de contenido y tipo de contenido aplicable]
```

### Ejemplo:
```
HB-001: Los Reels con música en tendencia generan un 25% más de interacciones que los videos informativos estándar
- **Variable Independiente**: Tipo de contenido (Reel con música vs video informativo)
- **Variable Dependiente**: Tasa de interacción total (reactions+comments+shares)/impresiones
- **Población Objetivo**: Mujeres de 25-40 años en Piedras Negras/Eagle Pass interesadas en moda
- **Métrica de Éxito**: ≥ 25% aumento en interacciones por impresión vs grupo de control
- **Duración del Experimento**: 1 semana (mínimo 3 pares de publicaciones)
- **Relacionado con**: Pilar Valor educativo, Tipo Contenido: Reel / Meme adaptado
```

## 2. Flujo de Validación de Hipótesis

### Paso 1: Formulación
- Nacer de observaciones, preguntas o análisis de datos históricos
- Revisar hipótesis existentes para evitar duplicados
- Asignar número secuencial HB-XXX
- Documentar completamente usando el formato anterior
- Vincular a un pilar de contenido y tipo de contenido específico

### Paso 2: Diseño del Experimento
- Definir grupos de control y variante (si aplica A/B)
- Determinar tamaño de muestra necesario (mínimo 3-5 publicaciones por variante)
- Seleccionar métricas primarias y secundarias a medir
- Establecer criterios de exclusión (ej. días festivos, eventos especiales)
- Asignar fechas tentativas de ejecución

### Paso 3: Ejecución
- Crear piezas en el CSV con el `Hipotesis_ID` correspondiente
- Seguir el flujo de publicación estándar (Gates 3→4→5→6)
- Asegurar que las variables independientes sean las únicas diferencias entre variantes
- Mantener constantes todos los demás factores (horario, audiencia objetivo, CTA similar, etc.)

### Paso 4: Recopilación de Métricas
- Ejecutar extracción de métricas a 24h y 72h para cada publicación
- Registrar resultados en el CSV de métricas o en tabla de experimentos dedicada
- Calcular métricas agregadas por variante (promedio, mediana, desviación estándar)

### Paso 5: Análisis y Validación
- Aplicar pruebas estadísticas apropiadas (t-test, chi-cuadrado, etc.) si se tiene suficiente muestra
- Comparar resultados contra el umbral de éxito definido
- Determinar si la hipótesis se valida, se rechaza o es inconclusa
- Documentar tamaño de efecto y nivel de confianza

### Paso 6: Aprendizaje y Documentación
- Registrar aprendizaje clave independientemente del resultado
- Actualizar mejores prácticas o plantillas de copy si se valida
- Programar experimentos de seguimiento si es prometedora pero inconclusa
- Compartir resultados en reuniones de revisión de gates

## 3. Plantilla de Registro de Experimento

Crear un registro en formato Markdown o CSV para cada hipótesis probada:

```markdown
# Experimento HB-001: Reels con música vs videos informativos

## Hipótesis
Los Reels con música en tendencia generan un 25% más de interacciones que los videos informativos estándar

## Diseño
- **Grupo A (Control)**: Videos informativos estándar (n=5 publicaciones)
- **Grupo B (Variante)**: Reels con música en tendencia (n=5 publicaciones)
- **Variables constantes**: 
  - Hora de publicación: 19:30-21:00
  - Pilar: Valor educativo
  - CTA: "Más tips en nuestro catálogo de cuidados"
  - Audiencia objetivo: Mujeres 25-40 interesados en moda
  - Duración: 1 semana (lunes 5 - viernes 9 de agosto)

## Resultados
| Métrica | Grupo A (Media) | Grupo B (Media) | Diferencia | % Cambio | p-valor |
|---------|-----------------|-----------------|------------|----------|---------|
| Interacciones por publicación | 28.4 | 37.2 | +8.8 | +31.0% | 0.032 |
| CTR a WhatsApp | 1.8% | 2.1% | +0.3% | +16.7% | 0.12 |
| Nuevos seguidores | 4.2 | 5.6 | +1.4 | +33.3% | 0.08 |

## Conclusión
✅ **HIPÓTESIS VALIDADA** - Los Reels con música en tendencia generan un 31% más de interacciones (p=0.032), superando el umbral del 25%.

## Aprendizaje
- El efecto es consistente across diferentes temas educativos
- La música en tendencia específica del género (norteño, banda) funciona mejor que pop genérico
- Los primeros 3 segundos son críticos para retención

## Próximos Pasos
1. Actualizar plantilla de copy para Reels educativos: enfatizar los primeros 3 segundos
2. Diseñar experimento HB-002: Comparar diferentes géneros musicales (norteño vs banda vs pop)
3. Compartir resultado en próxima reunión de growth (agosto 15)
```

## 4. Métricas Clave para Validación

Según los datos históricos disponibles, estos son los umbrales sugeridos para validación:

| Tipo de Hipótesis | Métrica Primaria | Umbral de Éxito Mínimo | Comentario |
|-------------------|------------------|------------------------|------------|
| **Engagement/Interacción** | Interacciones por publicación | ≥ 20% aumento vs control | Basado en promedio histórico de ~25 interacciones |
| **CTR/Conversión** | CTR a WhatsApp o llamada | ≥ 15% aumento vs control | Basado en CTR histórico de ~1.5-2% |
| **Alcance/Viralidad** | Compartidos por impresión | ≥ 25% aumento vs control | Los compartidos indican mayor potencial orgánico |
| **Crecimiento de Audiencia** | Nuevos seguidores por publicación | ≥ 20% aumento vs control | Metricamente más ruidoso, requiere mayor muestra |
| **Retención** | % de video visto (para Reels/videos) | ≥ 10% aumento vs control | Solo aplicable a contenido de video |

## 5. Reglas para Experimentación Ética y Efectiva

1. **Una variable a la vez**: Solo cambiar un elemento entre control y variante
2. **Tamaño de muestra mínimo**: 3-5 publicaciones por variante para detectar diferencias significativas
3. **Duración adecuada**: Al menos una semana completa para capturar variabilidad semanal
4. **Documentación completa**: Registrar todos los factores que podrían afectar resultados
5. **Replicabilidad**: Otro miembro del equipo debería poder repetir el experimento
6. **Evitar sesgos de confirmación**: Buscar activamente evidencia que contradiga la hipótesis
7. **Escalabilidad**: Considerar si el resultado se puede aplicar a gran escala antes de implementar ampliamente

## 6. Integración con el Sistema GrowthOS

### Campos CSV Relevantes
- `Hipotesis_ID`: Vincula cada pieza a su hipótesis de experimentación
- `Nota_Taxonomia`: Para registrar aprendizajes clave después de la validación
- `Reconciliacion_Estado` y `Reconciliacion_Confianza`: Para marcar si la hipótesis se validó (Validado/High) o no (No Validado/Low)
- `Fecha_Ultima_Publicacion`: Para calcular el período exacto del experimento

### Reportes Sugeridos
1. **Reporte Semanal de Experimentos**: 
   - Lista de hipótesis probadas esa semana
   - Resultados y estado de validación
   - Próximos pasos recomendados

2. **Tablero de Hipótesis Activas**:
   - Hipótesis en proceso de prueba
   - Hipótesis validadas esperando implementación
   - Hipótesis rechazadas con aprendizajes

3. **Reporte Mensual de Aprendizajes**:
   - Síntesis de todos los experimentos del mes
   - Cambios recomendados en plantillas de copy, horarios o tácticas
   - Hipótesis prioritarias para el próximo mes

## 7. Próximos Pasos para Implementar este Marco

1. **Crear plantilla de hipótesis** en formato Markdown para uso del equipo
2. **Establecer repositorio de hipótesis** (carpeta en GrowthOS o Google Drive)
3. **Definir ciclo de revisión**: Reunión semanal para revisar hipótesis en proceso y planificar nuevas
4. **Capacitar al equipo** en el formato de hipótesis y proceso de validación
5. **Iniciar con una hipótesis piloto** basada en datos históricos observados
6. **Refinar el proceso** basado en la experiencia del primer ciclo

## 8. Ejemplo de Hipótesis Prioritarias para Probar

Basados en la análisis preliminar de los datos disponibles, estas son algunas hipótesis de alto potencial para probar inicialmente:

```
HB-001: Los Reels con música en tendencia generan un 25% más de interacciones que los videos informativos estándar
HB-002: Los publicaciones que incluyen preguntas en el copy generan un 15% más de comentarios que las declarativas
HB-003: Los horarios de publicación entre 19:00-20:00 generan un 20% más de alcance que las 20:00-21:00 los viernes
HB-004: Los carruseles con máximo 3 slides tienen un 30% menor tasa de abandono que los de 5+ slides
HB-005: Los videos que muestran el proceso de bordado (mano trabajando) generan un 40% más de tiempo de visualización que los de producto terminado
```

--- 
*Este marco complementa el Puntos 1-3 del plan de crecimiento, enfocándose en el aspecto de experimentación y aprendizaje continuo para maximizar la efectividad de las publicaciones en Facebook e Instagram.*  
