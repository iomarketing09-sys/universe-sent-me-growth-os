# Control de Canon

## Campos de Canon

- `Bloqueado_Canon`: Indica si la pieza tiene una contradicción de canon que la bloquea. Valores: `Sí` / `No`.
- `Estado_Canon`: Estado de revisión de canon. Valores posibles:
  - `Canon_Clear_or_Unverified`: No hay contradicción conocida o no se ha verificado.
  - `Canon_Constrained`: Tiene alguna restricción pero no bloquea.
  - `Canon_Review_Required`: Se requiere revisión por parte del equipo de canon.
  - `Canon_Partial`: Parte del contenido está aprobada, parte necesita revisión.

## Regla de Bloqueo
Una pieza **no puede** transitar a los estados `Programado` o `Publicado` si:
- `Bloqueado_Canon` es `Sí`, **o**
- `Estado_Canon` no es `Canon_Clear_or_Unverified` (es decir, requiere revisión, está restringido o es parcial).

Solo roles autorizados (por ejemplo, el equipo de canon) pueden cambiar `Bloqueado_Canon` a `No` o establecer `Estado_Canon` en `Canon_Clear_or_Unverified` tras revisión.

## Motivos de Revisión
Cuando se rechaza o se requiere revisión por canon, se registra un motivo en `Motivo_Revision_Normalizado`, con valores como:
- `Canon_Contradiccion_Sustantiva`
- `Canon_Absolucion_Administrativa`
- `Canon_Restriccion_No_Bloqueante`
- `Canon_Resuelto_Reconciliacion_Pendiente`
- `Inventario_Reconciliacion_Pendiente`
- `Identidad_Reconciliada_Sin_Conflicto_Canon_Evidente`

