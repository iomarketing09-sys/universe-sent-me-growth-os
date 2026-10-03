# Arquitectura del Growth OS Core

## Propósito
Definir la arquitectura de metadatos y flujos operativos para gestionar piezas de contenido de manera escalable, permitiendo filtrado, priorización y publicación controlada.

## Sistema de Metadatos Estandarizado
Para escalar, cada idea debe existir como una fila independiente en un sistema de inventario estructurado.

### Campos Obligatorios (ID Únicos)
- `ID_Pieza`: Identificador único (formato: `CNT-####`)
- `Fecha_Creacion`: Fecha de registro de la idea
- `Ultima_Modificacion`: Fecha de última actualización
- `Estado`: Etapa del flujo operativo (Enum)

### Campos Narrativos y de Personaje
- `Titulo`: Título o logline de la pieza
- `Tipo_Contenido`: Formato del entregable (Enum)
- `Personaje_Principal`: Protagonista
- `Personajes_Secundarios`: Acompañantes
- `Lugar`: Escenario
- `Categoria`: Temática central (Enum)

### Campos Estratégicos y de Growth OS
- `Plataforma`: Destino principal (Enum)
- `Hipotesis_ID`: Relación con el banco de hipótesis
- `Objetivo`: Propósito estratégico
- `Prioridad`: Nivel de urgencia/importancia (Enum)
- `Dificultad_Produccion`: Esfuerzo estimado (Enum)
- `Es_Reutilizable`: Flag para reciclar contenido (Sí/No)
- `Bloqueado_Canon`: ¿Tiene contradicciones de canon? (Sí/No)
- `Fecha_Ultima_Publicacion`: Fecha de la última publicación
- `Dias_Desde_Publicacion`: Días transcurridos desde la última publicación (calculado)

## Flujos Operativos
El Growth OS define flujos para la creación, revisión, aprobación, programación y publicación de contenido, con mecanismos de control de calidad y trazabilidad.

## Integración
El núcleo está diseñado para ser independiente de la plataforma de publicación, permitiendo la integración con diversas APIs (como Meta Graph API) mediante adaptadores específicos de cuenta.

