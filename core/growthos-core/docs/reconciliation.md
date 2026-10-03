# Reconciliación de Datos

## Propósito
El proceso de reconciliación asegura que los datos de diferentes fuentes (por ejemplo, inventario interno vs. datos de plataforma) estén consistentes y que las piezas de contenido estén correctamente clasificadas y listas para producción.

## Campos de Reconciliación
- `Reconciliacion_Estado`: Estado del proceso de reconciliación. Valores:
  - `No_Confirmed_Match`: No se ha confirmado una coincidencia con la fuente externa.
  - `Resolved_Production_Set`: Se ha resuelto y la pieza está lista para producción.
- `Reconciliacion_Confianza`: Nivel de confianza en la reconciliación. Valores:
  - `High`: Alta confianza.
  - `Medium`: Confianza media.
  - `Low`: Baja confianza.
  - `None`: No hay confianza o no se ha evaluado.
- `Reconciliacion_Fuente`: Indica la fuente o método utilizado para la reconciliación.
- `Reconciliacion_Nota`: Notas adicionales sobre el proceso de reconciliación.

## Flujo de Trabajo
1. Una pieza entra en el sistema con `Reconciliacion_Estado` = `No_Confirmed_Match`.
2. Se realiza una comparación con la fuente externa (por ejemplo, inventario de Meta, datos de cadáver).
3. Si se encuentra una coincidencia y se resuelve cualquier discrepancia, el estado pasa a `Resolved_Production_Set` y se establece un nivel de confianza.
4. Si no se puede reconciliar, la pieza permanece en `No_Confirmed_Match` y se registra la razón en `Reconciliacion_Nota`.

## Uso
Los campos de reconciliación son utilizados por los procesos de automatización de cuentas para determinar qué piezas están listas para pasar a producción y cuáles requieren atención manual.

