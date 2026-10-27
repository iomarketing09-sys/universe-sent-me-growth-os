# Changelog — Growth OS

Registro de cambios importantes del proyecto. Se actualiza al completar un
módulo, un agente o un hito relevante.

Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).

---

## [Sin publicar]

### Añadido

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
