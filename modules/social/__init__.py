"""Módulo de redes sociales.

Cubre el ciclo de publicación en Instagram y Facebook:

- publicación directa y programación por calendario
- registro y seguimiento de publicaciones
- lectura de métricas orgánicas desde Meta Graph API

La publicación está desactivada por defecto; cada operación requiere
autorización explícita del tenant.
"""

from modules.social.ig_publisher import (
    IgPublisher,
    create_ig_publisher_for_tenant,
    get_meta_tokens,
    load_tenant_credentials,
)
from modules.social.ig_scheduler import (
    IgScheduler,
    ScheduleItem,
    discover_tenants,
    parse_tenant_schedule,
)
from modules.social.meta_graph import capture_organic, query_instagram_media
from modules.social.meta_publisher import (
    MetaPublisher,
    MetaResponse,
    load_dryrun_schedule,
    load_integration_env,
    load_meta_import_csv,
    publish_meta_import_slots,
    publish_schedule_from_dryrun,
)
from modules.social.preflight import PreflightResult, preflight_items, preflight_tenant
from modules.social.publish_state import (
    PublishJob,
    PublishJobStore,
    job_key as publish_job_key,
)
from modules.social.publication_tracker import (
    REQUIRED_COLUMNS,
    load_publications,
    pending_publications,
    summary,
)
from modules.social.publisher import get_pending_count, publish_pending

__all__ = [
    "IgPublisher",
    "IgScheduler",
    "MetaPublisher",
    "MetaResponse",
    "PreflightResult",
    "PublishJob",
    "PublishJobStore",
    "REQUIRED_COLUMNS",
    "ScheduleItem",
    "capture_organic",
    "create_ig_publisher_for_tenant",
    "discover_tenants",
    "get_meta_tokens",
    "get_pending_count",
    "load_dryrun_schedule",
    "load_integration_env",
    "load_meta_import_csv",
    "load_publications",
    "load_tenant_credentials",
    "parse_tenant_schedule",
    "pending_publications",
    "preflight_items",
    "preflight_tenant",
    "publish_job_key",
    "publish_meta_import_slots",
    "publish_pending",
    "publish_schedule_from_dryrun",
    "query_instagram_media",
    "summary",
]
