# Módulo `social`

Ciclo de publicación en Instagram y Facebook: programación por calendario,
publicación, registro de publicaciones y lectura de métricas orgánicas.

## Estructura

```
modules/social/
├── __init__.py              API pública
├── ig_scheduler.py          Programador multi-tenant + guard de reuse
├── ig_publisher.py          Publicación en Instagram
├── meta_publisher.py        Publicación en Facebook (dry-run por defecto)
├── meta_graph.py            Lectura de métricas orgánicas
├── publication_tracker.py   Estado de publicaciones desde CSV
└── publisher.py             Publicación pendiente simple
```

La publicación está desactivada por defecto. `MetaPublisher` arranca en
`dry_run=True` y `IgScheduler` solo publica lo que ya está en la fecha/hora del
calendario del tenant.

## Guard de reuse: dos políticas

`IgScheduler.historical_reuse_report(asset, tenant_id=...)` decide si un activo
puede volver a publicarse. El dictamen incluye `status`, `reason` y
`asset_ref`, para que el log explique el porqué y no solo un booleano.

| Tipo de tenant | `tenant_type` | Regla |
| --- | --- | --- |
| Contenido | otros valores | Ventana de 30 días sobre el histórico del tenant |
| Producto físico | `physical_cro`, `retail`, `ecommerce_product` | `REUSE_NOT_APPLICABLE`: manda el inventario |

Estados posibles: `BLOCKED`, `ALLOWED`, `UNKNOWN`, `NOT_APPLICABLE`.

```python
from modules.social import IgScheduler

scheduler = IgScheduler(["universe", "flexi"])
scheduler.historical_reuse_report("123456 - Kael.png", tenant_id="universe")
scheduler.historical_reuse_report("142801 - Isaura.png", tenant_id="flexi")
```

### Contenido (ventana de 30 días)

La referencia del activo se extrae del nombre del archivo (`"123456 - Kael.png"`
→ `"123456"`). Se busca en la cola de reutilización del **tenant correcto**
(`tenants/<id>/historical/metrics/cola_reutilizacion_*.csv`). Si no hay fila, o
la fecha no es válida, el estado es `UNKNOWN` y la publicación **no se bloquea**:
el guard informa, no inventa historial.

### Producto físico (inventario)

Para tenants de producto no aplica la ventana: un mismo modelo puede volver a
publicarse. En su lugar se consulta `config.ads.approved_models`:

- `IN_INVENTORY` — modelo cargado en la config.
- `NOT_IN_INVENTORY` — no está cargado.
- `INVENTORY_UNKNOWN` — el tenant no tiene inventario declarado.

**Importante:** `approved_models` es una lista **parcial** (modelos que la
sucursal ya cargó), no un inventario completo. Un `NOT_IN_INVENTORY` significa
"no lo tengo declarado", no "no existe en sucursal". Para Flexi el inventario
real sigue pendiente como insumo de negocio.

## Uso

```bash
# Una pasada para todos los tenants con calendario
python3 -m modules.social.ig_scheduler

# Solo un tenant
python3 -m modules.social.ig_scheduler --tenant flexi
```

El resultado de `run_once()` separa `published`, `failed`, `skipped_future` y
`blocked`, ambos en total y por tenant.
