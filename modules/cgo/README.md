# Módulo `cgo`

Orquestador del Growth OS. Es el **único** módulo que importa a los demás y no
duplica reglas de negocio: cada capacidad delega en el módulo dueño y devuelve
un `CgoResult` uniforme.

## Estructura

```
modules/cgo/
├── __init__.py          API pública
├── result.py            CgoContext, CgoResult, GateResult
├── tracks.py            native_digital vs physical_cro
├── gates.py             gates reutilizables
├── orchestrator.py      despacho capacidad → módulo
├── capabilities/        una por capacidad
└── __main__.py          CLI
```

## Capacidades

| Capacidad | Qué hace | Módulo dueño |
| --- | --- | --- |
| `daily_pipeline` | Estado local del día: snapshot, calendario, ads | intelligence |
| `weekly_calendar` | Slots futuros del calendario (solo native) | intelligence |
| `tenant_onboarding` | Auditoría local del tenant | intelligence |
| `cross_tenant_report` | Totales de todos los tenants | intelligence |
| `canon_sync` | Pre-check del repo canon (solo native) | identity |
| `meta_publishing` | Coordina IG/FB | social |
| `verify_setup` | Salud del entorno | todos |

`native_digital`: `universe`, `bam-in-a-can`.
`physical_cro`: `flexi`, `micas-art-deco`, `firma-bordados`.

## Capabilities por track

- `weekly_calendar` y `canon_sync` solo aplican a `native_digital`.
- El resto aplica a ambos.

Si `tenant_type` falta o es inválido, el track es `unknown` y la capacidad
devuelve `UNKNOWN`/`PARTIAL`, no una excepción.

## Estados

`OK`, `PARTIAL`, `BLOCKED`, `NOT_CONFIGURED`, `ERROR`.

Por defecto un gate `UNKNOWN` no bloquea (falta de datos, inventario parcial).
Con `--strict` sí bloquea.

## Publicación

`meta_publishing` separa las dos rutas:

| Plataforma | Ruta | Cron |
| --- | --- | --- |
| Facebook | `native_scheduled`: Meta programa con `published=false` | No |
| Instagram | `queued_for_cron`: `ig_scheduler` publica al vencer el slot | Sí, cada 15 min |

Sin `--publish` todo es dry-run y no se llama a ningún publisher.

## CLI

```bash
python3 -m modules.cgo --mode daily_pipeline --tenant flexi
python3 -m modules.cgo --mode cross_tenant_report
python3 -m modules.cgo --mode verify_setup --json
python3 -m modules.cgo --mode tenant_onboarding --tenant flexi
python3 -m modules.cgo --mode meta_publishing --tenant flexi
python3 -m modules.cgo --mode meta_publishing --tenant flexi --publish
python3 -m modules.cgo --mode weekly_calendar --tenant universe
python3 -m modules.cgo --mode canon_sync --tenant universe
```

Flags: `--tenant`, `--all`, `--json`, `--strict`, `--publish`.

## Timer de Instagram

La API de Instagram no acepta publicación programada: hay que llamarla a la
hora del slot. El timer despierta `ig_scheduler` cada 15 minutos, revisa el
calendario y publica lo vencido. Máximo retraso: 15 minutos.

Los unit files están en `scripts/` y **no** se instalan solos:

```bash
sudo cp scripts/growth-os-ig.service /etc/systemd/system/
sudo cp scripts/growth-os-ig.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now growth-os-ig.timer
```

Comprobar: `systemctl list-timers growth-os-ig.timer`.

El timer de Instagram también ejecuta cada 15 minutos la revisión de cortes de
campañas. Los cortes E24/E48/E72/diarios/FINAL se guardan por anuncio y no
modifican presupuesto ni estado. La regla completa está en
`docs/REGLA_METRICAS_CAMPANAS.md`.

Timer dedicado opcional para separar responsabilidades:

```bash
sudo cp scripts/growth-os-ads.service /etc/systemd/system/
sudo cp scripts/growth-os-ads.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now growth-os-ads.timer
```
