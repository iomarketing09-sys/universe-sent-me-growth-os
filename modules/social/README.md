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

## Estabilización de publicación

`IgScheduler` mantiene un estado por tenant en
`tenants/<id>/data/social/publish_state.json`. Cada slot tiene una clave
idempotente (`instagram|tenant|fecha|hora|asset`) y registra intentos, último
error, próximo reintento y estado terminal.

Los errores transitorios usan backoff exponencial: 15, 30, 60, 120 y 240
minutos. Después de 5 intentos el job pasa a `dead` y se agrega a
`tenants/<id>/data/social/dead_letter.jsonl`. Un error permanente de preflight
queda en `blocked` y no se reintenta hasta liberarlo manualmente.

```bash
# Preflight local de todos los slots del tenant
python3 scripts/social_preflight.py --tenant flexi

# Validar también permisos de publicación contra Meta
python3 scripts/social_preflight.py --tenant flexi --remote

# Ver estado, reintentos y cuarentena
python3 scripts/social_publish_state.py --tenant flexi

# Liberar jobs después de corregir asset, formato o credenciales
python3 scripts/social_publish_state.py --tenant flexi --release-dead
python3 scripts/social_publish_state.py --tenant flexi --release-blocked
```

El preflight valida credenciales, `IMAGE_HOST`, formato soportado, existencia
del asset, peso, formato de imagen y relación de aspecto de feed. `catbox` queda
bloqueado para producción; los tenants actuales usan `imgbb`.

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

## Facebook: álbum multi-imagen (carrusel)

Facebook no tiene endpoint de carrusel para páginas: el equivalente es un álbum.
`MetaPublisher.publish_album()` es la ruta oficial; no armar el flujo a mano.

```python
from modules.social import MetaPublisher

publisher = MetaPublisher(page_id=PAGE_ID, access_token=PAGE_TOKEN, dry_run=False)
result = publisher.publish_album(
    image_paths=["01.jpg", "02.jpg", "03.jpg"],          # 2 a 10, en orden
    caption="Texto del post",
    scheduled_publish_time="2026-11-04T16:00:00+00:00",  # siempre UTC
)
```

- Paso 1: sube cada foto a `/{PAGE_ID}/photos` con `published=false` y
  `temporary=false`, para que no expire a las 24 h.
- Paso 2: crea el post en `/{PAGE_ID}/feed` con `attached_media[i]`,
  `published=false` y `unpublished_content_type=SCHEDULED`.
- `result.raw_response["photo_ids"]` devuelve los IDs subidos.
- Verificación: `GET /{post_id}?fields=is_published,scheduled_publish_time`.
- En `dry_run` valida el conteo (2–10) y devuelve `mock_album_*` sin red.

### Programar un slot del calendario (solo Facebook)

`publish_meta_import_slots()` lee `meta_import.csv`, filtra por fecha y
despacha `PHOTO`, `CAROUSEL`, `REEL`/`VIDEO` y `TEXT`. Omite los slots ya
registrados como `scheduled`/`published` en `publication_log*.csv`, así que
repetir el comando no duplica.

Con `--since`/`--until` el modo toca **solo Facebook**, porque Instagram no
programa por API: sus slots los publica el cron de `ig_scheduler` al vencer la
hora.

```bash
# Solo los slots del 4 de noviembre
python3 -m modules.cgo --mode meta_publishing --tenant micas-art-deco \
  --publish --since 2026-11-04 --until 2026-11-04
```

## Contexto de publicación

Toda publicación real escribe su contexto en
`tenants/<id>/publication_contexts.json` mediante
`modules.intelligence.publication_context.record_publication()`. Ese JSON es la
fuente única para análisis y respuestas a comentarios; no se mantiene un ledger
paralelo.

- `IgScheduler.process_item()` lo escribe después del publish real de
  Instagram.
- `record_scheduled_publication()` lo escribe para Facebook, tanto en el lote
  como en `publish_single_slot()`.
- Es idempotente por `publication_id`. Si el post ya tiene alias corto y largo,
  actualiza ambos y conserva `visual_context` y demás campos ricos existentes.
- Si la fila ya está en `publication_log_week2.csv` pero falta el contexto,
  vuelve a intentar la escritura para repararlo sin duplicar el log.
- `character` y `meme_text` se derivan del nombre del asset; si falta el chiste,
  se usa `assets_meme_text.csv`. El escritor nunca abre imágenes.
- Un fallo al guardar contexto se registra como warning y no revierte ni bloquea
  la publicación.

## Uso

### Host de imágenes para Instagram

La API de Instagram exige una URL pública, no un archivo local. El publisher
sube la imagen al host indicado por `IMAGE_HOST` en `tenants/<id>/.env`:

| `IMAGE_HOST` | Requiere | Notas |
| --- | --- | --- |
| `imgbb` (default) | `IMGBB_API_KEY` | ImgBB puede bloquear redes con error 103 |
| `catbox` | nada | `catbox.moe`, gratuito, sin cuenta |

```bash
# tenants/flexi/.env
FB_PAGE_ID=...
META_ACCESS_TOKEN=...
IMAGE_HOST=catbox
```

Si `IMAGE_HOST` no se declara, se mantiene `imgbb` y se exige su key.

## Uso

```bash
# Una pasada para todos los tenants con calendario
python3 -m modules.social.ig_scheduler

# Solo un tenant
python3 -m modules.social.ig_scheduler --tenant flexi
```

El resultado de `run_once()` separa `published`, `failed`, `skipped_future` y
`blocked`, ambos en total y por tenant.
