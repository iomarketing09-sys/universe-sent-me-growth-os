# Módulo `intelligence`

Métricas, histórico, experimentos, planificación y auditoría. **Solo lectura por
defecto**: la única escritura en Meta es `change_plan_executor.py`, explícita,
limitada a `pause_ad` y auditada.

## Estructura

```
modules/intelligence/
├── __init__.py            API pública (33 nombres)
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
├── change_plan_executor.py Aplica planes aprobados con verificación
├── campaign_report.py     Reporte unificado: Meta + WhatsApp, cliente e interno
├── monetization.py        Señales, periodos, payouts y umbral por tenant
├── revenue.py             Deals y cobranza de tenants de producto
└── agents/
    ├── meta_ads_agent/    Resultados de campañas y KPIs
    ├── monetization_agent/ Monetización, umbral y conciliación read-only
    └── tenant_auditor/    Auditoría local de onboarding
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

## Monetization Agent

Lee el ledger de Monetization Lite, resume el umbral de payout y cruza la
evidencia de app, API de página y suma por publicación. Es **solo lectura**:
no aprueba periodos, no registra payouts ni escribe en Meta.

```bash
python3 -m modules.intelligence.agents.monetization_agent.agent universe
python3 -m modules.intelligence.agents.monetization_agent.agent universe \
  --since 2026-10-01 --until 2026-10-31 --full
python3 -m modules.cgo --mode monetization_report --tenant universe --json
```

La captura y actualización local se ejecutan con
`scripts/run_monetization_sync.py`. El timer dedicado está en
`scripts/growth-os-monetization.timer`; mientras no se instale, el reporte se
puede consultar manualmente o desde `daily_pipeline`.

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
`tenants/<id>/metrics_snapshot_log.csv`. El timer de Instagram llama a
`run_capture_cycle()` cada 15 minutos para **todos** los tenants con
`publication_log_week2.csv` y `.env`; programa E0/E24/E72 para las
publicaciones recientes (idempotente por `publication_id` + ventana). El mismo
ciclo guarda las métricas diarias de página en
`tenants/<id>/page_metrics_daily.csv`.

Las publicaciones de Facebook se registran en el `publication_log_week2.csv`
desde `meta_publisher.publish_schedule_from_dryrun()` con su `post_id`; sin esa
fila el snapshot de Facebook no existe.

```bash
python3 -m modules.intelligence.metrics_snapshot flexi schedule   # crea ventanas pendientes
python3 -m modules.intelligence.metrics_snapshot flexi capture    # captura las que ya vencieron
python3 -m modules.intelligence.metrics_snapshot flexi validate
python3 -m modules.intelligence.metrics_snapshot flexi normalize  # migra filas legacy
python3 -m modules.intelligence.metrics_snapshot flexi dedupe --dry-run
python3 -m modules.intelligence.metrics_snapshot flexi dedupe    # una fila por plataforma+post+ventana
```

Facebook aporta reacciones, comentarios, shares, clics y video por publicación;
`post_impressions` y `post_impressions_unique` ya no existen en la API. A nivel
página se capturan `page_post_engagements`, `page_views_total`,
`page_video_views`, `page_actions_post_reactions_total` y `page_daily_follows`.
Instagram aporta `reach`, `views`, `total_interactions`, `saved`, likes,
comentarios y shares cuando el token tiene `instagram_manage_insights`. Las
métricas se piden una por una para que una métrica no disponible no invalide
toda la captura.

El ledger de Universe convivió con filas del esquema viejo
(`captured_at,post_id,created_time,...`). `normalize` las convierte al esquema
canónico, conserva una copia `.pre-normalize-*.csv.bak`, respeta symlinks y es
idempotente. Las ventanas legacy tipo `E48h` se conservan; no se reinterpretan
como E0/E24/E72. Las capturas posteriores de un post histórico se guardan como
`LIFETIME_BACKFILL` para no etiquetar un acumulado actual como si fuera el dato
de la ventana original.

`dedupe` limpia las recapturas históricas de la misma ventana. Conserva la
primera captura válida (`Captured` antes que `No_Data`/`Failed`/`Pending`) y
deja un respaldo `.pre-dedupe-*.csv.bak`. Las filas sin `publication_id` no se
tocan.

Solo se programan ventanas que vencen dentro de las próximas 2 horas; una
captura tardía se omite en vez de guardar un dato actual con etiqueta falsa.

Para reconstruir el historial y mantener el publication log al día:

```bash
python3 tenants/universe/metrics/sync_publication_log.py --dry-run
python3 tenants/universe/metrics/backfill_lifetime.py --dry-run
```

**Permiso pendiente:** `instagram_manage_insights` (App Review) es necesario
para reach/views de Instagram. Sin él, el snapshot guarda los conteos públicos
y deja el error en la columna `error`; no falla la captura.

### Cobertura de medición

`measurement_coverage.py` responde qué métricas tienen muestras reales y qué
hipótesis todavía no pueden evaluarse. No emite veredictos ni rellena huecos:

```bash
python3 -m modules.intelligence.measurement_coverage universe
python3 -m modules.intelligence.measurement_coverage universe --json
```

- Un contador en `0` en el ledger significa ausencia de captura, no un cero
  observado. Las proporciones derivadas devuelven `None` cuando no tienen
  denominador y sí aceptan `0.0` como dato real.
- Varios snapshots de la misma publicación cuentan una sola vez. El resumen usa
  su último valor con dato para no sobrerrepresentar publicaciones recapturadas.
- `count` = conteo absoluto; `ratio` = proporción entre 0 y 1 (no porcentaje).

En Facebook, Graph v26 retiró reach/impresiones por publicación. Para video sí
expone `post_video_views`, `post_video_views_organic`,
`post_video_avg_time_watched` (ms por reproducción), `post_video_view_time`
(ms totales), `post_video_complete_views_organic` y `post_video_length` (ms).
De ahí salen `video_completion_rate` (completaciones / reproducciones
orgánicas) y `video_average_watch_share` (tiempo medio visto / duración).
Instagram sigue bloqueado para reach/views hasta aprobar
`instagram_manage_insights`.

Estado verificado en Universe el 2026-11-05: 284 snapshots y 102
publicaciones; HB-002 con 2 publicaciones de video y mediana de completación
`0.1795`, todavía insuficiente para un veredicto; HB-004 en `no_samples` por
falta de reach. El vínculo de esas piezas con HB-002 requiere decisión de CGO:
no se asignó una hipótesis a posteriori.

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

## Aplicar un plan de cambios

`campaign_optimizer` recomienda; `change_plan_executor` aplica solo lo aprobado.
Dry-run por defecto, `pause_ad` como única acción automatizada, verificación de
`status` y rastro en `tenants/<id>/ads/insights/actions.jsonl`.

```bash
# Ver qué haría con el último corte
python3 -m modules.intelligence.change_plan_executor \
  --tenant flexi \
  --capture tenants/flexi/ads/insights/captures/2026-11_flexi_ads_560mxn/E72.json

# Aplicar (una sola acción o todas las pausables)
python3 -m modules.intelligence.change_plan_executor --tenant flexi \
  --capture .../E72.json --apply --only 120247659400790665
```

`keep` y `watch` se ignoran; `scale_candidate` y `rotate_creative` se reportan
como no automatizadas.

## Reporte unificado de campaña

Une las dos fuentes por `ad_id`: la última captura de Meta y las conversaciones
atribuidas de WhatsApp. Genera dos salidas del mismo dato, sin edición manual:

```bash
python3 -m modules.intelligence.campaign_report \
  --tenant flexi --campaign 2026-11_flexi_ads_560mxn [--checkpoint FINAL]
```

- `reporte_cliente.md`: una página, sin jerga ni IDs.
- `reporte_interno.md`: ad_ids, estados, checkpoints y discrepancias.
- `reporte_cliente.html`: plantilla A4 imprimible (guardar como PDF desde el navegador).

Los anuncios con menos del 10% de las conversaciones no se declaran eficientes:
su costo todavía no es concluyente.

## Reporte semanal

`weekly_report.py` cierra la ventana domingo–sábado y la compara con la semana
anterior. Una página: resultados por canal, qué se hizo, qué se aprendió, hasta
tres recomendaciones y qué se necesita del cliente.

```bash
python3 -m modules.intelligence.weekly_report --tenant flexi [--reference 2026-11-03]
python3 -m modules.intelligence.weekly_report --tenant flexi --refresh-meta
```

Salidas en `tenants/<id>/reports/semanal/` (`.md` y `.html` A4). Solo cuentan
como publicadas las piezas con estado `published` o `scheduled`; las omitidas se
excluyen. La tabla separa Facebook orgánico, Facebook pauta, Instagram orgánico,
Instagram pauta y otros espacios de Meta. La pauta se desglosa con
`publisher_platform`. El orgánico sale del ledger local (`metrics_snapshot_log`
+ `page_metrics_daily`); solo si no hay capturas por publicación cae a la
consulta directa de Meta. La pauta sigue consultando Meta y cachea el resultado.

`--refresh-meta` consulta Meta y guarda un caché local en
`tenants/<id>/ads/insights/captures/weekly_meta_<inicio>_<fin>.json`. Sin ese
flag, el reporte se regenera desde el caché y no hace llamadas de red. Meta ya
no expone alcance e impresiones orgánicas de Facebook; Instagram requiere
`instagram_manage_insights` para alcance e interacciones completas.
