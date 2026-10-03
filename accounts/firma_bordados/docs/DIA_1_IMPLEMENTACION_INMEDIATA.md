# Día 1 – Implementación Inmediata del Plan de Crecimiento
## Acciones para comenzar hoy (Basado en la Fase 1 del Roadmap)

## ⏰ Tiempo estimado: 2-3 horas distribuidas en el día

---

### 🎯 **Objetivo del Día 1**
Establecer las bases fundamentales para el plan de crecimiento:
1. Implementar inmediatamente los horarios de impacto y plantillas de copy V2
2. Poner en marcha el proceso de validación de assets desde Google Drive
3. Documentar la primera hipótesis de marketing para probar

---

## 📋 **Acciones del Día 1**

### ✅ **Acción 1: Implementar Horarios de Impacto y Plantillas de Copy V2** (30 min)
**Responsable:** Líder de contenido + Equipo de creación de copy

**Pasos:**
1. **Reunión breve (15 min)** con todo el equipo de contenido:
   - Compartir el documento `HORARIOS_Y_PLANTILLAS_DE_COPY.md`
   - Explicar claramente los horarios de impacto:
     - **Mañana:** 08:30 - 09:30 (Venta directa / Educativo)
     - **Tarde:** 14:00 - 15:30 (Trabajo del día)
     - **Noche:** 19:30 - 21:00 (Interacción / Confianza)
     - **Domingo:** 20:00 - 21:00 (Reel resumen semanal)
   - Enfatizar: **"Nunca publicar fuera de estas franjas excepto por excepciones justificadas y documentadas"**

2. **Distribuir y acordar el uso de Plantillas de Copy V2:**
   - Revisar cada plantilla (Venta, Información/Trabajo del día, Interacción/Confianza, Valor Educativo)
   - Acordar que **TODAS** las publicaciones a partir de hoy deben seguir una de estas plantillas
   - Asignar un "guardian de copy" diario que revise brevemente las publicaciones antes de programarlas

3. **Crear un recordatorio visual:**
   - Imprimir la tabla de horarios y colocarla en el área de trabajo
   - Crear un evento recurrente en el calendario del equipo: "Revisión de horarios y copy - 10:00 daily"

**Resultado esperado al final del día:** 
- El equipo tiene clara la nueva guía de horarios y copy
- Se ha comenzado a aplicar las plantillas en el copy de hoy

---

### 📂 **Acción 2: Iniciar el Proceso de Validación de Assets** (60-90 min)
**Responsable:** Diseñador/Administrador de assets + Persona con acceso a Google Drive

**Pasos:**
1. **Revisar el inventario actual de assets:**
   - Acceder a la carpeta de Google Drive: `Firma Bordados/` y subcarpetas
   - Identificar los tipos de assets disponibles (fotos, videos, PDFs, etc.)
   - Anotar ejemplos de nombres de archivo (ej: `01_lunes_detalle_uniforme.png`, `VID-20260821-WA0002.mp4`)

2. **Preparar el entorno para el script de exportación:**
   - Verificar que tienen acceso a Google Drive API (o usar alternativa como `rclone`)
   - Si usan Google Drive API:
     - Asegurarse de tener credenciales de servicio o OAuth configuradas
     - Habilitar la API de Google Drive en Google Cloud Console
   - Si usan rclone:
     - Verificar que esté instalado y configurado para acceder a su Drive de Firma Bordados

3. **Probar el script básico de exportación:**
   - Revisar el script: `/home/universe-sent-me/new-growth-os/scripts/export_drive_inventory.py`
   - **Nota importante:** Este es un script de muestra. Para usarlo con su Drive real, necesitan:
     - Opción A (Google Drive API): 
       * Configurar autenticación (service account key o OAuth)
       * Reemplazar la sección "sample data" con consultas reales a la API de Drive
       * Consultar archivos en las carpetas `Firma Bordados/` y subcarpetas
     - Opción B (rclone - más simple para comenzar):
       * Usar `rclone lsjson "nombre_del_remote:Firma Bordados"` para obtener lista de archivos
       * Convertir ese output al formato CSV necesario
   - Ejecutar una prueba con un subconjunto pequeño de assets (ej. solo la carpeta `Catalogos/`)

3. **Definir reglas iniciales de mapeo (para la versión 0.1 del exportador):**
   - **Tipo_Contenido** basado en extensión:
     - `.pdf` → `"PDF"`
     - `.png`, `.jpg`, `.jpeg` → `"Imagen"`
     - `.mp4`, `.mov` → `"Video"`
   - **Categoria** basada en palabras clave en el nombre de archivo:
     - Si contiene `"catalog"` o `"Catálogo"` → `"Marca / Narrativa / Resonancia"`
     - Si contiene `"guía"` o `"guia"` → `"Valor educativo"`
     - Si contiene `"trabajo"` o `"trabajo del día"` → `"Trabajo del día"`
     - Si contiene `"testimonio"` o `"historia"` → `"Interacción/confianza"`
   - **Titulo**: Limpiar el nombre de archivo (quitar extensiones, guiones bajos, números de día)
     - Ej: `01_lunes_detalle_uniforme.png` → `"Detalle de uniforme deportivo - Lunes"`
   - **Objetivo**: Generar una descripción básica basada en el tipo y título
   - **ID_Pieza**: Usar formato `CNT-####` secuencial (empezar en 0001)
   - **Estado inicial**: `"Idea"` para todos los assets nuevos
   - **Prioridad**: `"Media"` por defecto (ajustar a `"Alta"` si hay palabras como `"oferta"`, `"urgente"`, `"promoción"`)
   - **Dificultad_Produccion**: `"Media"` por defecto
   - **Es_Reutilizable**: `"Sí"` por defecto (excepto para contenido muy específico de fecha)
   - **Fuente**: `"Google Drive - Folder: [ruta relativa]"`
   - **Formato**: Extensión en mayúsculas (PDF, PNG, JPG, MP4)
   - **Drive_ID**: El ID de archivo de Google Drive (obtenido de la API o rclone)
   - **Asset_Ref_Confirmado**: El nombre exacto del archivo (con extensión)

4. **Generar el primer CSV de assets:**
   - Ejecutar su versión adaptada del exportador
   - Guardar el output en: `/home/universe-sent-me/new-growth-os/assets/assets_inventario_dia1.csv`
   - Verificar que tenga al menos 5-10 assets con los campos básicos completados

**Resultado esperado al final del día:**
- Tener un proceso claro (documentado aunque sea brevemente) para exportar assets desde Drive
- Tener un CSV preliminar con assets inventariados y campos básicos completados
- Saber exactamente qué necesitan hacer para mejorar el exportador en los próximos días

---

### 📝 **Acción 3: Documentar la Primera Hipótesis de Marketing** (30-45 min)
**Responsable:** Líder de growth/estrategia + Analista de métricas

**Pasos:**
1. **Revisar la plantilla de hipótesis:**
   - Abrir `/home/universe-sent-me/new-growth-os/docs/HIPOTESIS_PLANTILLA.md`
   - Entender la estructura requerida para documentar una hipótesis HB-XXX

2. **Seleccionar una hipótesis inicial sencilla y de alto potencial:**
   - Basarse en observaciones recientes o datos históricos disponibles
   - Ejemplos de buenas hipótesis iniciales:
     * "HB-001: Las publicaciones que incluyen preguntas en el copy generan un 15% más de comentarios que las declarativas"
     * "HB-002: Los Reels con música en tendencia generan un 25% más de interacciones que los videos informativos estándar"
     * "HB-003: Los horarios de publicación entre 19:00-20:00 generan un 20% más de alcance que las 20:00-21:00 los viernes"
   - **Importante:** Elegir una que sea fácil de probar con los assets disponibles esta semana

3. **Documentar completamente la hipótesis usando la plantilla:**
   - Llenar todas las secciones de `HIPOTESIS_PLANTILLA.md`
   - Ser específico sobre:
     - **Variable Independiente:** Qué exactamente se está cambiando
     - **Variable Dependiente:** Qué se está midiendo y cómo
     - **Población Objetivo:** Qué audiencia se está considerando (puede ser general al inicio)
     - **Métrica de Éxito:** Umbral claro y justificado (ej. "≥ 15% aumento en comentarios basado en datos históricos de ~10 comentarios promedio")
     - **Duración del Experimento:** Sugerir 1 semana (mínimo 3-5 publicaciones por variante)
     - **Relacionado con:** Indicar a qué pilar y tipo de contenido se aplica

4. **Planificar la ejecución (para la semana siguiente):**
   - Identificar qué assets necesitan crear o adaptar
   - Definir los grupos de control y variante (si es A/B)
   - Asignar responsables para crear el copy y programar las publicaciones
   - Acordar que extraerán métricas a 24h y 72h usando los procesos existentes

**Resultado esperado al final del día:**
- Tener la primera hipótesis completamente documentada en formato estándar
- Tener un plan claro para probarla la semana siguiente
- El equipo entiende el proceso de validación de hipótesis que se usará continuamente

---

## ✅ **Checklist de Éxito para el Día 1**

Al final del día 1, deben poder marcar:

- [ ] El equipo ha sido informado de los nuevos horarios de impacto y está de acuerdo en seguirlos
- [ ] Se ha distribuido y acordado el uso de las Plantillas de Copy V2 para todo el copy
- [ ] Se ha probado el proceso de exportación de assets desde Google Drive (aunque sea con datos de muestra)
- [ ] Se ha generado un CSV preliminar de assets inventariados
- [ ] Se ha documentado completamente la primera hipótesis de marketing usando la plantilla estándar
- [ ] Se tiene un plan claro para ejecutar y validar esa hipótesis la próxima semana

## 📌 **Recordatorios Importantes**

1. **No busquen la perfección en el Día 1:** El objetivo es comenzar, no tener todo listo y perfecto. Mejorarán el proceso en los días siguientes.
2. **Enfoque en acción, no en documentación:** Pasen más tiempo haciendo que leyendo o planeando en exceso.
3. **Comunicación constante:** Usen su canal habitual (Slack, WhatsApp, etc.) para avisar cuando completen cada acción.
4. **Celebrar pequeños avances:** Cada acción completada es un paso hacia un proceso más medible y efectivo.

## 🔜 **Qué Viene Después (Día 2 en adelante)**

Una vez completadas estas acciones iniciales, en los días siguientes deberían:

- **Día 2:** Mejorar el exportador de assets basado en lo aprendido de la prueba inicial
- **Día 3-4:** Ejecutar la primera publicación siguiendo los nuevos horarios y plantillas
- **Fin de Semana 1:** Tener listo el primer experimento de hipótesis para comenzar a probarlo la semana siguiente

Recuerden: El objetivo no es tener todo perfecto hoy, sino comenzar a construir los hábitos y procesos que generarán mejora continua con el tiempo.

--- 
*Este documento es una guía operativa para el Día 1 de implementación. Para ver el plan completo y la fundamentación estratégica, consulte:*
- `PLAN_CRECIMIENTO.md` (Punto 1: Alineación estratégica de contenidos)
- `POINT_2_VALIDATE_ASSETS.md` (Punto 2: Validación de assets)
- `HIPOTESIS_PLANTILLA.md` (Plantilla para hipótesis)
- `HYPOTHESIS_VALIDATION_FRAMEWORK.md` (Marco completo de experimentación)
