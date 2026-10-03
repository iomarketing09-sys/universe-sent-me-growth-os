# Ciclo de Vida de una Pieza

## Estados de una pieza (EstadoPieza)

- **IDEA**: Concepto inicial, aún no producido.
- **PENDIENTE_DE_PRODUCCION**: Aprobado para producción, esperando recursos.
- **APROBADO**: Listo para ser programado o publicado.
- **PUBLICADO**: Ya publicado en la plataforma destino.
- **ARCHIVADO**: Guardado para referencia, ya no activo.
- **DIFERIDO**: Pospuesto temporalmente.
- **BLOQUEADO**: No puede avanzar por problemas de canon u otros.
- **PROGRAMADO**: Programado para publicación futura.

## Transiciones típicas

IDEA → PENDIENTE_DE_PRODUCCIÓN → APROBADO → PUBLICADO → ARCHIVADO

Desde cualquier estado se puede pasar a DIFERIDO o BLOQUEADO según reglas de negocio.
Desde BLOQUEADO, tras revisión, puede volver a APROBADO si se resuelve el bloqueo.
Desde PUBLICADO puede pasar a ARCHIVADO.

## Campos de estado normalizado

- `Estado_Operacion_Normalizado`: Versión canónica del estado operativo.
- `Estado_Canon_Normalizado`: Versión canónica del estado de canon.
Estos campos aseguran consistencia frente a posibles variaciones de entrada.

