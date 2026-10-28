# Changelog — Growth OS

Registro de cambios importantes del proyecto. Se actualiza al completar un
módulo, un agente o un hito relevante.

Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).

---

## [Sin publicar]

### Añadido

- **Módulo `cgo`** (`modules/cgo/`): orquestador con las 7 capacidades
  (`daily_pipeline`, `weekly_calendar`, `tenant_onboarding`,
  `cross_tenant_report`, `canon_sync`, `meta_publishing`, `verify_setup`), CLI
  `python3 -m modules.cgo` y contrato único `CgoResult` (status, gates,
  actions, artifacts, next_actions). Solo CGO importa a los demás módulos.
- **`tenant_auditor`** (`modules/intelligence/agents/tenant_auditor/`): 9
  checks locales (config, track, marca, assets, inventario, canales,
  calendario, sync, histórico) sin red ni scraping. Exportado como
  `intelligence.audit_tenant`.
- **Tracks normalizados**: `universe` y `bam-in-a-can` →
  `native_digital`; `flexi`, `micas-art-deco` y `firma-bordados` →
  `physical_cro`. `flexi` y `bam-in-a-can` recibieron `client_name`,
  `timezone` y `contact_channel`.
- **Timer de Instagram** (`scripts/growth-os-ig.timer`): cada 15 minutos,
  porque la API de IG no programa publicaciones. Incluye
  `growth-os-ig.service`. No se instala solo; el README de `cgo` trae el
  comando. También se restauraron los unit files del sync que se habían
  perdido del repo.
- **Guard de reuse en `social`** (`modules/social/ig_scheduler.py`): dos
  políticas explícitas. Los tenants de contenido usan una ventana de 30 días
  sobre su propio histórico; los de producto físico (`physical_cro`, `retail`,
  `ecommerce_product`) reciben `NOT_APPLICABLE` y se apoyan en el inventario.
  `run_once()` reporta `blocked` por tenant y `process_item()` no publica si el
  activo está bloqueado. Documentado en `modules/social/README.md`.
- **Módulo `social`** (`modules/social/`): publicación en Instagram y Facebook,
  programación por calendario, registro de publicaciones y lectura de métricas
  orgánicas de Meta. Incluye 21 nombres en su API pública.
- **Módulo `identity`** (`modules/identity/`): sincronización multitenant
  (`sync.py`), registro de tenants (`tenant_registry.py`) y el
  `brand_voice_agent` completo con sus 5 skills (tono, variantes A/B,
  cumplimiento Meta, investigación de competencia y análisis de voz de posts).
- **Módulo `creative`** (`modules/creative/`): copy de campaña
  (`agents/copywriter_agent/`), kit de marca por tenant (`brand_kit.py`) y
  selector de imágenes reales del inventario (`image_selector.py`). Incluye
  `README` con los comandos y las reglas de negocio.
- **Kit de marca de Flexi** (`tenants/flexi/brand_kit.json`): temporada OI26
  ("Luz y sombra"), rojo de marca `#D82232` muestreado del logo oficial
  (Pantone 1797) y paleta de temporada marcada como aproximada hasta confirmar.
- **Módulo `communications`** (`modules/communications/`): WhatsApp de solo
  lectura con `WhatsAppAgent`, cliente D1 real vía API de Cloudflare,
  resumen de conversaciones, profundidad, atribución a anuncios y diagnóstico
  de ecos. Incluye `README` con comandos.
- **Módulo `intelligence`** (`modules/intelligence/`): `metrics_snapshot`,
  `historical_baseline`, `experiment_log`, `planner`, `audit` y
  `ads_adapters` (Marketing API). API pública de 16 nombres y 6 envoltorios de
  compatibilidad en `growth/`.
- **`meta_ads_agent`** (`modules/intelligence/agents/meta_ads_agent/`): reporte
  de campañas con gasto, CTR, CPC, conversaciones, costo por conversación y
  modo `--offline` sobre el snapshot del sync. Es el último agente que faltaba:
  `verify_setup` ya reporta **SETUP COMPLETO**.
- **`CHANGELOG.md`**: este archivo, para conservar contexto entre sesiones.

### Cambiado

- El código de publicación se movió de `growth/` a `modules/social/`:
  `ig_publisher`, `ig_scheduler`, `meta_publisher`, `publisher`,
  `publication_tracker` y `integrations/meta_graph`.
- Los archivos originales en `growth/` se conservan como **envoltorios de
  compatibilidad** que reexportan desde el módulo nuevo. Ningún script ni test
  existente se rompió.
- `growth/sync.py` y `growth/tenant_registry.py` pasaron a `modules/identity/`
  con el mismo patrón de envoltorio. `agents/brand_voice_agent/` vive ahora en
  `modules/identity/agents/`.
- `agents/copywriter_agent/` pasó a `modules/creative/agents/copywriter_agent/`
  con envoltorios en la ruta anterior. El agente resuelve la raíz del repo y no
  depende de `Path.cwd()`, así que funciona desde cualquier directorio.
- `TenantRegistry` resuelve la raíz del proyecto buscando `modules/` y
  `tenants/` hacia arriba, así que ya no depende de la profundidad del archivo
  que lo contiene.

### Corregido

- **Host de imágenes configurable** en `social`: `IgPublisher` acepta
  `IMAGE_HOST=imgbb|catbox`. ImgBB respondía `103 forbidden` desde esta red
  con una key válida, así que `flexi` usa `catbox.moe` (gratis, sin cuenta).
  `load_tenant_credentials` solo exige `IMGBB_API_KEY` cuando el host es
  `imgbb`.
- `get_historical_reuse_info` aceptaba `tenant_id` pero leía siempre la cola
  de `universe`; ahora usa la cola del tenant recibido.
- `ScheduleItem.from_meta_import_row` no pasaba `tenant_id` al baseline, así
  que el calendario de cualquier tenant recibía evidencia de `universe`.
- `modules/social` no exportaba `publish_schedule_from_dryrun`, que CGO usa
  para la ruta de Facebook.
- Los 4 tests de `meta_publisher` fallaban por depender de `dryrun_output.json`
  en la raíz, un artefacto que está en `.gitignore` y se perdió. Ahora usan el
  fixture versionado `tests/fixtures/dryrun_firma_bordados.json` (20 slots:
  17 media, 3 text). Suite: 172 passed, 15 failed (los heredados de modelo).
- El guard de reuse devolvía `UNKNOWN` cuando el baseline no tenía fila; ahora
  distingue "activo en inventario sin fecha" de "sin historial" en el `reason`,
  sin bloquear publicaciones por falta de datos.
- `scripts/sync_all.py --list` volvía a mostrar la tabla vacía tras el refactor
  (el registro buscaba `tenants/` dentro de `modules/`). Vuelve a listar los 5
  tenants.
- `tests/test_sync.py` parcheaba el shim `growth.integrations.meta_graph` en
  lugar del módulo real `modules.social.meta_graph`.
- `config.json` de Flexi apuntaba `asset_dir` de ARISHA (306703) a
  `assets/flexi/...` cuando las fotos viven en `assets/quirelli/...`.
- El selector de imágenes ya no cuenta como distintas las copias
  `nombre (1).jpg` ni las variantes de mayúsculas en la extensión.
- `pytest.ini` usa `--basetemp=.pytest_tmp` para no llenar la cuota de `/tmp`.
- `growth/integrations/whatsapp_adapters.py` y `whatsapp_graph.py` pasaron a
  `modules/communications/whatsapp/` con envoltorios de compatibilidad.
- El verify token del webhook dejó de estar hardcodeado en el adaptador y de
  guardarse en `tenants/flexi/whatsapp/config.json`; se lee de `.env`.
- El worker de WhatsApp ahora guarda los ecos que Meta manda en
  `value.message_echoes` (antes solo leía `smb_message_echoes`, así que se
  perdían). Requiere redesplegar el worker para tomar efecto.
- **`scripts/cron_sync.sh`**: script que faltaba y hacía fallar
  `growth-os-sync.service` todos los días con `status=203/EXEC`. Sincroniza los 5
  tenants con datos en vivo, deja `logs/sync/last.json` + `history.log` y sale
  con código distinto de 0 si algo falla. Probado en manual: exit 0.
- `scripts/sync_all.py` ya no escribe snapshots ni crea `tenants/<id>/data/`
  para tenants sin credenciales (`skipped_write`).
- `schema.sql` del worker incluye las columnas de `referral` y se agregó
  `migrations/001_referral_columns.sql`.
- Worker `flexi-whatsapp-webhook` **redesplegado** (versión `6b367fc4`) con el
  soporte de `message_echoes`; verificado end-to-end con un eco sintético y
  `/stats` sigue protegido por el secreto existente.
- `deploy.sh` resuelve credenciales desde `tenants/flexi/.env` o `growth-os/.env`
  (`CF_API_TOKEN`), toma el `account_id` de `whatsapp/config.json` y no falla si
  falta el verify token (conserva el secreto ya cargado).
- `wrangler.toml` fija `preview_urls = false` para evitar URLs de preview
  accidentales.
- **Aislamiento del baseline histórico**: `historical_baseline` apuntaba fijo a
  `tenants/universe/historical`, así que cualquier tenant veía evidencia de
  Universe. Ahora todas las funciones aceptan `tenant_id`/`base_path` y el
  planner lo propaga. `tests/test_planner_historical.py` verifica que Flexi no
  hereda evidencia de Universe.
- **Política de snapshots**: solo `tenants/*/data/sync/latest.json` se versiona;
  los timestamped quedan en disco (fuera de git) y el cron borra los de más de
  90 días.
- **Backfill de ecos** (`modules/communications/whatsapp/backfill.py`): recuperó
  21 respuestas humanas (15 de texto) que el bug había descartado entre el 24 y
  el 27 de octubre. Idempotente vía `INSERT OR IGNORE`.

### Pendiente

- `IgScheduler._check_historical_reuse` no existe: 7 tests en rojo.
- `load_dryrun_schedule` y conteos de calendario: 4 tests en rojo.
- Publicación de Facebook separada de `meta_publisher`.
- Soporte de YouTube y TikTok (pospuesto).
- `meta_ads_agent` y `whatsapp_agent` siguen vacíos.

---

## [2026-10-27]

### Añadido

- Paquete `growthos` reestructurado en `core/growthos-core/growthos/` con
  imports absolutos, `pyproject.toml`, configuración y migraciones SQLite.
  Suite del core: 26 tests en verde.
- Agentes `brand_voice_agent` y `copywriter_agent` restaurados con sus skills
  vendorizadas y procedencia documentada.
- Documentación del proyecto y skill `growth-cgo`.
- Workspace completo de la campaña Meta Ads de Flexi, incluyendo reporte A4.

### Cambiado

- `pytest.ini` registra `core/growthos-core` en `pythonpath` para resolver
  `growthos` de forma consistente.

### Seguridad

- El sync multitenant redacta tokens, secretos y credenciales en URLs antes de
  persistir snapshots o imprimirlos.
- Se eliminaron tokens de Meta de archivos de evidencia ya versionados.

---

## [2026-10-26]

### Añadido

- Sync multitenant (`growth/sync.py`) con snapshots por tenant.
- Integraciones de solo lectura: Meta Graph, Meta Ads, Google Webmaster y
  WhatsApp.
- CLI `scripts/sync_all.py`.

### Corregido

- La consulta de página de Facebook pedía un campo inexistente
  (`remembered_email_access_token`); ahora usa `id,name,followers_count,website`.
- `scripts/sync_all.py` no ejecutaba `main()` al invocarse como script.

---

## Notas de contexto

- El proyecto sufrió una pérdida de archivos entre el 20 y el 24 de octubre de
  2026. El código actual es una reconstrucción local posterior a ese incidente.
- Algunos documentos en `docs/` fueron escritos antes de la pérdida y pueden
  describir un estado que ya no corresponde. El estado vigente es este changelog.
- La lógica del sistema vive hoy en `growth/`; la migración a `modules/` es
  progresiva y se hace módulo por módulo con envoltorios de compatibilidad.
