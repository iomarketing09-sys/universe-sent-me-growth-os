# Módulo `intelligence`

Métricas, histórico, experimentos, planificación y auditoría. **Solo lectura**
sobre las fuentes externas: no crea, edita ni pausa anuncios.

## Estructura

```
modules/intelligence/
├── __init__.py            API pública (27 nombres)
├── metrics_snapshot.py    Snapshots E0/E24/E72 de publicaciones
├── historical_baseline.py Baseline histórico por tenant
├── experiment_log.py      Observaciones e hipótesis por tenant
├── planner.py             Construcción de calendario desde dryrun/meta_import
├── audit.py               Auditoría de CSV de publicaciones vs activos
├── ads_adapters.py        Meta Marketing API (capture_ads_insights)
├── ads_ledger.py          Corte diario por anuncio (CSV idempotente)
├── ads_reporting.py       Reporte JSON/texto/Markdown por anuncio
├── campaign_capture.py    Checkpoints E24/E48/E72/diarios/FINAL
├── campaign_optimizer.py  Plan de cambios por anuncio (solo recomendación)
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

## Rendimiento por anuncio

El sync con `--live-ads` guarda un corte diario por anuncio en
`tenants/<id>/ads/insights/ad_insights_daily.csv`. El archivo es operativo y no
se versiona; repetir el sync el mismo día reemplaza la fila, no la duplica.

```bash
# Consulta el último corte local de una campaña
python3 tools/ads_report.py --tenant flexi --campaign 120247658527630665

# Refresca el corte desde Meta y genera el reporte
python3 tools/ads_report.py --tenant flexi --campaign 120247658527630665 --live

# Salida para automatizaciones
python3 tools/ads_report.py --tenant flexi --campaign 120247658527630665 --json
```

El reporte ordena primero los anuncios con conversaciones por costo ascendente;
los anuncios sin conversaciones quedan al final para no confundirlos con el
mejor CPA. Los que superan `--max-cpa` (8 MXN por defecto) aparecen en
`alerts`.

## Captura automática de campañas

`campaign_capture.py` lee `tenants/<id>/ads/campanas/*/meta_ids.json` y usa la
fecha exacta de inicio de Meta. Genera cortes obligatorios a las 24, 48 y 72
horas, cada 24 horas hasta el cierre y un `FINAL` dos horas después. La regla
completa vive en `docs/REGLA_METRICAS_CAMPANAS.md`.

```bash
python3 scripts/run_ads_capture.py --all-tenants --dry-run
python3 scripts/run_ads_capture.py --all-tenants
```

Los reportes se guardan en
`tenants/<id>/ads/insights/captures/<slug>/E48.{json,md}` y el estado
idempotente en `tenants/<id>/ads/insights/capture_state.json`. El timer
dedicado está en `scripts/growth-os-ads.timer`; mientras no se instale, el
timer de Instagram de 15 minutos ejecuta el mismo chequeo.

Cada corte también genera un plan en
`tenants/<id>/ads/plans/<slug>/E48.{json,md}`. El plan es
`recommendation_only`, nunca escribe en Meta y usa la antigüedad programada del
corte para decidir. Antes de 72 horas una señal mala queda en `watch`; desde
72 horas puede proponer `pause_ad` sobre un anuncio individual. Nunca propone
pausar toda la campaña ni cambiar presupuesto.

Antes de generar el plan, la captura reconcilia los IDs publicados de
`campaign.json` contra los ad sets observados en Meta y `meta_ids.json`. La
corrección es local y queda auditada en `metadata_reconciliation`; si hay varios
ad sets, el plan queda con `execution_blocked=true` en vez de adivinar.

```bash
# Regenerar el plan desde una captura local, sin red
python3 tools/ads_plan.py --tenant flexi \
  --campaign 120247658527630665 --checkpoint E48
```

La política por defecto está en `campaign_optimizer.DEFAULT_POLICY` y puede
sobrescribirse por tenant en `tenants/<id>/ads/campaign_policy.json`.

## Snapshots E0/E24/E72

`metrics_snapshot.py` captura y persiste un snapshot por ventana en
`tenants/<id>/metrics_snapshot_log.csv`. Ya no depende de que alguien lo
invoque a mano: el timer de Instagram llama a `run_capture_cycle()` en cada
pasada y este programa E0/E24/E72 para las publicaciones recientes del
`publication_log_week2.csv` (idempotente por `publication_id` + ventana).

```bash
python3 -m growth.metrics_snapshot flexi schedule   # crea ventanas pendientes
python3 -m growth.metrics_snapshot flexi capture    # captura las que ya vencieron
python3 -m growth.metrics_snapshot flexi validate
```

Facebook aporta `post_impressions` (impresiones), `post_impressions_unique`
(alcance), `post_engaged_users`, clics y video. Instagram aporta `reach`,
`views`, `total_interactions`, `saved`, likes, comentarios y shares. Las
métricas se piden una por una para que una métrica no disponible no invalide
toda la captura.

**Permiso pendiente:** `instagram_manage_insights` (App Review) es necesario
para reach/views de Instagram. Sin él, el snapshot guarda los conteos públicos
y deja el error en la columna `error`; no falla la captura.

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
