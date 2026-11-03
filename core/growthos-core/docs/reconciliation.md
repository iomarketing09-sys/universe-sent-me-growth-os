# Reconciliación de Datos

## Contrato canónico

`GrowthOS/Content_Inventory_CANONICAL.csv` usa un contrato estable de **47
columnas snake_case**, definido por `CSVAdapter.COLUMN_ORDER[Piece]`.

- Las 46 columnas del inventario fuente se conservan.
- Los encabezados legacy `Asset_Ref`, `Asset_Filename`, `Drive_ID`,
  `Estado_Canon`, `Estado_Produccion`, `Estado_Publicacion`,
  `Ultima_Sincronizacion` y `Motivo_Revision_Normalizado` se aceptan al importar
  como alias, pero se exportan en minúsculas.
- `es_historico` es la columna canónica adicional.
- `Content_Inventory_RECONCILIATION.csv` contiene una fila por pieza y columna.
- `Content_Inventory_OVERRIDES.csv` contiene una fila por cada `C_REAL` que
  requiere decisión humana.

Los valores de enum se clasifican así:

- `A`: coincidencia exacta con el vocabulario canónico.
- `B`: transformación determinista y documentada.
- `C_REAL`: valor ambiguo; el canónico queda vacío hasta que exista un override.
- `NONE_EMPTY`: campo opcional vacío.
- `FREE_TEXT`: texto copiado sin transformación.

Un override solo se aplica cuando `resuelto` es un valor válido para el enum del
campo. Una propuesta sin `resuelto` permanece pendiente y no contamina el
canónico.

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
