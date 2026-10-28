# Módulo `intelligence`

Métricas, histórico, experimentos, planificación y auditoría. **Solo lectura**
sobre las fuentes externas: no crea, edita ni pausa anuncios.

## Estructura

```
modules/intelligence/
├── __init__.py            API pública (16 nombres)
├── metrics_snapshot.py    Snapshots E0/E24/E72 de publicaciones
├── historical_baseline.py Baseline histórico por tenant
├── experiment_log.py      Observaciones e hipótesis por tenant
├── planner.py             Construcción de calendario desde dryrun/meta_import
├── audit.py               Auditoría de CSV de publicaciones vs activos
├── ads_adapters.py        Meta Marketing API (capture_ads_insights)
└── agents/
    └── meta_ads_agent/    Resultados de campañas y KPIs
```

Los archivos en `growth/` (`metrics_snapshot`, `historical_baseline`,
`experiment_log`, `planner`, `audit`, `integrations/ads_adapters`) quedaron como
envoltorios de compatibilidad y siguen aceptando `python -m growth.<nombre>`.

## Meta Ads Agent

```bash
# Marketing API (red)
python3 -m modules.intelligence.agents.meta_ads_agent.agent flexi \
  --campaign 2026-10_flexi_ads_500mxn

# Sin red: usa tenants/<id>/data/sync/latest.json
python3 -m modules.intelligence.agents.meta_ads_agent.agent flexi --offline
```

Devuelve por campaña: gasto, impresiones, clics, alcance, CTR, CPC, CPM,
conversaciones, **costo por conversación** y clics por conversación.

Nota: Meta reporta `conversations_started_7d` pero **no** la profundidad 2/3 en
esta cuenta. La profundidad real se mide con `modules/communications`.

## Aislamiento por tenant

`historical_baseline` resolvía siempre `tenants/universe/historical`, así que
cualquier tenant recibía evidencia de Universe. Ahora todas las funciones
aceptan `tenant_id` y `base_path`:

```python
historical_base("flexi")            # tenants/flexi/historical
load_reuse_queue("flexi")           # [] si el tenant no tiene histórico
get_historical_reuse_info("123456 - Kael.png", tenant_id="flexi")
```

`DEFAULT_TENANT = "universe"` conserva el comportamiento anterior para scripts
viejos, pero el planner ya propaga el tenant en cada slot.
