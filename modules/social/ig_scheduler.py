#!/usr/bin/env python3
"""
Instagram Scheduler Multi-Tenant para Growth OS

Programa publicaciones en Instagram para múltiples tenants.
Un solo cron procesa todos los tenants independientemente.
"""

import os
import re
import sys
import csv
import json
import logging
from pathlib import Path
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from modules.social.ig_publisher import (
    IgPublisher,
    create_ig_publisher_for_tenant,
    load_tenant_credentials
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ==============================================================================
# REUSE: CONTENIDO vs PRODUCTO FÍSICO
# ==============================================================================

# Ventana en la que no se repite un activo de contenido.
REUSE_WINDOW_DAYS = 30

# Tenants de producto físico: la restricción real es el inventario, no la
# ventana de 30 días (un mismo modelo puede volver a publicarse).
PRODUCT_TENANT_TYPES = {"physical_cro", "retail", "ecommerce_product"}

REUSE_BLOCKED = "BLOCKED"
REUSE_ALLOWED = "ALLOWED"
REUSE_UNKNOWN = "UNKNOWN"
REUSE_NOT_APPLICABLE = "NOT_APPLICABLE"


def project_root() -> Path:
    """Raíz del repo, sin importar desde dónde se ejecute."""
    current = Path(__file__).resolve().parent
    for candidate in (current, *current.parents):
        if (candidate / "tenants").is_dir() and (candidate / "modules").is_dir():
            return candidate
    return current.parents[2]


def asset_ref_from_filename(asset_filename: Optional[str]) -> Optional[str]:
    """``"123456 - Kael - Test.png"`` -> ``"123456"``."""
    if not asset_filename:
        return None
    match = re.search(r"\d{3,}", str(asset_filename))
    return match.group(0) if match else None


def _parse_date(value: Any) -> Optional[date]:
    if not value:
        return None
    text = str(value).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(text[: len(fmt) + 2], fmt).date()
        except ValueError:
            continue
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


# ==============================================================================
# ESTRUCTURAS DE DATOS
# ==============================================================================

@dataclass
class ScheduleItem:
    """Un item de programación"""
    tenant_id: str
    date_str: str
    time_str: str
    media_filename: str
    caption: str
    post_type: str
    datetime_local: datetime
    datetime_utc: datetime
    
    @property
    def unique_key(self) -> str:
        return f"{self.tenant_id}_{self.date_str}_{self.time_str}_{self.media_filename}"


# ==============================================================================
# PUBLICATION LOG HANDLING (por tenant)
# ==============================================================================

LOG_FIELDS = [
    'date', 'time', 'platform', 'piece', 'asset_filename',
    'status', 'publication_id', 'published_at', 'reach',
    'interactions', 'DMs', 'leads'
]

def get_log_path(tenant_id: str) -> Path:
    """Ruta del log para un tenant"""
    return Path(f'tenants/{tenant_id}/publication_log_week2.csv')

def get_schedule_path(tenant_id: str) -> Path:
    """Ruta del schedule para un tenant (busca el más reciente)"""
    tenant_dir = Path(f'tenants/{tenant_id}')
    # Buscar meta_import*.csv o future_schedule.csv
    for pattern in ['meta_import*.csv', 'future_schedule.csv']:
        matches = list(tenant_dir.glob(pattern))
        if matches:
            return max(matches, key=lambda p: p.stat().st_mtime)
    return None


def load_publication_log(tenant_id: str) -> List[Dict[str, str]]:
    log_path = get_log_path(tenant_id)
    if not log_path.exists():
        return []
    with log_path.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_publication_log(tenant_id: str, rows: List[Dict[str, str]]) -> None:
    log_path = get_log_path(tenant_id)
    with log_path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def is_already_published(log_rows: List[Dict], item: ScheduleItem) -> bool:
    for row in log_rows:
        if (row.get('date') == item.date_str and
            row.get('time') == item.time_str and
            row.get('asset_filename') == item.media_filename and
            row.get('platform') == 'Instagram' and
            row.get('publication_id', '').strip()):
            return True
    return False


def add_publication_record(log_rows: List[Dict], item: ScheduleItem, post_id: str) -> None:
    now = datetime.now().isoformat(timespec='seconds')
    new_row = {
        'date': item.date_str,
        'time': item.time_str,
        'platform': 'Instagram',
        'piece': item.caption[:80],
        'asset_filename': item.media_filename,
        'status': 'published',
        'publication_id': post_id,
        'published_at': now,
        'reach': '',
        'interactions': '',
        'DMs': '',
        'leads': ''
    }
    log_rows.append(new_row)


# ==============================================================================
# SCHEDULE PARSING
# ==============================================================================

def parse_tenant_schedule(tenant_id: str) -> List[ScheduleItem]:
    schedule_path = get_schedule_path(tenant_id)
    if not schedule_path:
        logger.warning(f"No schedule encontrado para {tenant_id}")
        return []
    
    tz = ZoneInfo("America/Matamoros")
    items = []
    
    with schedule_path.open('r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date_str = row.get('Date (YYYY-MM-DD)', '').strip()
            time_str = row.get('Time (HH:MM, 24h)', '').strip()
            media = row.get('Media URL', '').strip()
            caption = row.get('Caption', '').strip()
            hashtags = row.get('Hashtags', '').strip()
            post_type = row.get('Post Type', '').strip()
            
            if not all([date_str, time_str, media]):
                continue
            
            full_caption = caption
            if hashtags:
                full_caption = f"{caption}\n\n{hashtags}"
            
            try:
                dt_local = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                dt_local = dt_local.replace(tzinfo=tz)
                dt_utc = dt_local.astimezone(timezone.utc)
            except ValueError as e:
                logger.warning(f"[{tenant_id}] Fecha/hora inválida: {date_str} {time_str} - {e}")
                continue
            
            items.append(ScheduleItem(
                tenant_id=tenant_id,
                date_str=date_str,
                time_str=time_str,
                media_filename=media,
                caption=full_caption,
                post_type=post_type,
                datetime_local=dt_local,
                datetime_utc=dt_utc
            ))
    
    items.sort(key=lambda x: x.datetime_utc)
    return items


def discover_tenants() -> List[str]:
    """Descubre tenants que tienen configuración para Instagram"""
    tenants = []
    tenants_dir = Path('tenants')
    if not tenants_dir.exists():
        return []
    
    for tenant_dir in tenants_dir.iterdir():
        if not tenant_dir.is_dir():
            continue
        # Verificar que tenga .env con credenciales IG
        env_path = tenant_dir / '.env'
        if env_path.exists():
            with open(env_path) as f:
                content = f.read()
                if 'META_ACCESS_TOKEN' in content and 'FB_PAGE_ID' in content:
                    tenants.append(tenant_dir.name)
    
    return tenants


# ==============================================================================
# MAIN SCHEDULER CLASS
# ==============================================================================

class IgScheduler:
    """Scheduler multi-tenant para Instagram"""
    
    def __init__(self, tenant_ids: List[str], historical_baseline=None):
        self.tenant_ids = tenant_ids
        self._historical_baseline = historical_baseline
        self.publishers: Dict[str, IgPublisher] = {}
        self.all_items: List[ScheduleItem] = []
        self.logs: Dict[str, List[Dict]] = {}
        
        # Inicializar publishers y cargar schedules
        for tenant_id in tenant_ids:
            try:
                self.publishers[tenant_id] = create_ig_publisher_for_tenant(tenant_id)
                logger.info(f"[{tenant_id}] Publisher OK - IG ID: {self.publishers[tenant_id].ig_id}")
            except Exception as e:
                logger.error(f"[{tenant_id}] Error inicializando publisher: {e}")
                continue
            
            # Cargar schedule
            items = parse_tenant_schedule(tenant_id)
            self.all_items.extend(items)
            logger.info(f"[{tenant_id}] Items en schedule: {len(items)}")
            
            # Cargar log
            self.logs[tenant_id] = load_publication_log(tenant_id)
            logger.info(f"[{tenant_id}] Items en log: {len(self.logs[tenant_id])}")
        
        logger.info(f"Total items multi-tenant: {len(self.all_items)}")
    
    def get_pending_items(self) -> List[ScheduleItem]:
        pending = []
        for item in self.all_items:
            log_rows = self.logs.get(item.tenant_id, [])
            if not is_already_published(log_rows, item):
                pending.append(item)
        return pending
    
    # ------------------------------------------------------------------ reuse
    @property
    def historical_baseline(self):
        """Baseline histórico (inyectable para tests; import perezoso)."""
        if self._historical_baseline is None:
            from modules.intelligence import historical_baseline

            self._historical_baseline = historical_baseline
        return self._historical_baseline

    def _tenant_config(self, tenant_id: str) -> Dict[str, Any]:
        path = project_root() / "tenants" / tenant_id / "config.json"
        if not path.is_file():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}

    def is_product_tenant(self, tenant_id: str) -> bool:
        """True si el tenant vende producto físico (calzado, retail)."""
        return str(self._tenant_config(tenant_id).get("tenant_type", "")) in PRODUCT_TENANT_TYPES

    def inventory_status(self, model_code: str, tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """¿El modelo está en el inventario declarado del tenant?

        La lista sale de ``config.ads.approved_models``, que por ahora es
        parcial: no es un inventario completo de sucursal.
        """
        tenant_id = tenant_id or (self.tenant_ids[0] if self.tenant_ids else "universe")
        code = str(model_code or "").strip()
        models = (self._tenant_config(tenant_id).get("ads") or {}).get("approved_models") or []
        codes = {str(model.get("code")): model for model in models}

        if not codes:
            return {
                "tenant_id": tenant_id,
                "code": code,
                "status": "INVENTORY_UNKNOWN",
                "source": "config.ads.approved_models",
                "note": "El tenant no tiene inventario declarado.",
            }
        if code in codes:
            return {
                "tenant_id": tenant_id,
                "code": code,
                "status": "IN_INVENTORY",
                "model": codes[code].get("name", ""),
                "brand": codes[code].get("brand", ""),
                "source": "config.ads.approved_models",
                "note": "Inventario parcial (solo modelos cargados en la config).",
            }
        return {
            "tenant_id": tenant_id,
            "code": code,
            "status": "NOT_IN_INVENTORY",
            "source": "config.ads.approved_models",
            "note": "Inventario parcial: el modelo puede existir en sucursal sin estar cargado.",
        }

    def historical_reuse_report(
        self,
        asset_filename: Optional[str],
        tenant_id: Optional[str] = None,
        today: Optional[date] = None,
    ) -> Dict[str, Any]:
        """Dictamen de reutilización con el motivo, para logs y reportes."""
        tenant_id = tenant_id or (self.tenant_ids[0] if self.tenant_ids else "universe")
        base = {"tenant_id": tenant_id, "asset_filename": asset_filename or ""}

        cache = getattr(self, "_reuse_cache", None)
        cache_key = (tenant_id, asset_filename or "")
        if today is None and cache is not None and cache_key in cache:
            return dict(cache[cache_key])

        report = self._reuse_report(asset_filename, tenant_id, today, base)
        if today is None:
            if cache is None:
                cache = self._reuse_cache = {}
            cache[cache_key] = dict(report)
        return report

    def _reuse_report(
        self,
        asset_filename: Optional[str],
        tenant_id: str,
        today: Optional[date],
        base: Dict[str, Any],
    ) -> Dict[str, Any]:
        if not asset_filename:
            return {**base, "status": REUSE_UNKNOWN, "reason": "Sin nombre de activo."}

        if self.is_product_tenant(tenant_id):
            code = asset_ref_from_filename(asset_filename)
            inventory = self.inventory_status(code, tenant_id) if code else None
            return {
                **base,
                "status": REUSE_NOT_APPLICABLE,
                "reason": "Tenant de producto físico: manda el inventario, no la ventana de 30 días.",
                "asset_ref": code,
                "inventory": inventory,
            }

        asset_ref = asset_ref_from_filename(asset_filename)
        if not asset_ref:
            return {**base, "status": REUSE_UNKNOWN, "reason": "El activo no tiene referencia numérica."}

        try:
            queue = self.historical_baseline.load_reuse_queue(tenant_id)
        except Exception as exc:  # el baseline nunca debe tumbar el scheduler
            return {**base, "status": REUSE_UNKNOWN, "reason": f"Baseline no disponible: {type(exc).__name__}"}

        row = next((item for item in queue if str(item.get("asset_ref")) == asset_ref), None)
        if not row:
            try:
                inventory = self.historical_baseline.load_asset_inventory(tenant_id)
            except Exception:
                inventory = []
            in_inventory = any(str(item.get("asset_id")) == asset_ref for item in inventory)
            reason = (
                "Activo en inventario sin fecha de publicación: no se puede calcular la ventana."
                if in_inventory
                else "Sin historial de publicación para este activo."
            )
            return {**base, "status": REUSE_UNKNOWN, "asset_ref": asset_ref, "reason": reason}

        last = _parse_date(row.get("fecha_ultima_publicacion"))
        if not last:
            return {
                **base,
                "status": REUSE_UNKNOWN,
                "asset_ref": asset_ref,
                "reason": "El historial no tiene una fecha válida.",
            }

        reference = today or datetime.now(timezone.utc).date()
        days_since = (reference - last).days
        status = REUSE_BLOCKED if days_since <= REUSE_WINDOW_DAYS else REUSE_ALLOWED
        return {
            **base,
            "status": status,
            "asset_ref": asset_ref,
            "last_published": last.isoformat(),
            "days_since": days_since,
            "window_days": REUSE_WINDOW_DAYS,
            "reason": (
                f"Publicado hace {days_since} días (ventana de {REUSE_WINDOW_DAYS})."
            ),
        }

    def _check_historical_reuse(
        self, asset_filename: Optional[str], tenant_id: Optional[str] = None
    ) -> str:
        """Compatibilidad: solo el dictamen, sin el detalle."""
        return self.historical_reuse_report(asset_filename, tenant_id=tenant_id)["status"]

    def process_item(self, item: ScheduleItem) -> Optional[str]:
        logger.info(f"\n{'='*60}")
        logger.info(f"[{item.tenant_id}] Procesando: {item.date_str} {item.time_str} - {item.media_filename}")
        
        publisher = self.publishers.get(item.tenant_id)
        if not publisher:
            logger.error(f"[{item.tenant_id}] No hay publisher configurado")
            return None
        
        reuse = self.historical_reuse_report(item.media_filename, tenant_id=item.tenant_id)
        if reuse["status"] == REUSE_BLOCKED:
            logger.warning(
                f"[{item.tenant_id}] No se publica {item.media_filename}: {reuse['reason']}"
            )
            return None

        try:
            post_id = publisher.publish(item.media_filename, item.caption)
            return post_id
        except Exception as e:
            logger.error(f"[{item.tenant_id}] Error publicando: {e}")
            return None
    
    def run_once(self) -> Dict[str, any]:
        """Ejecuta una pasada completa para todos los tenants"""
        now = datetime.now(timezone.utc)
        pending = self.get_pending_items()
        
        results = {
            'total_pending': len(pending),
            'processed': 0,
            'published': 0,
            'failed': 0,
            'skipped_future': 0,
            'blocked': 0,
            'by_tenant': {}
        }
        
        for item in pending:
            tenant_id = item.tenant_id
            if tenant_id not in results['by_tenant']:
                results['by_tenant'][tenant_id] = {
                    'processed': 0, 'published': 0, 'failed': 0,
                    'skipped_future': 0, 'blocked': 0
                }
            
            # Verificar si ya es hora
            if item.datetime_utc > now:
                logger.info(f"⏭️  [{tenant_id}] Saltando (futuro): {item.date_str} {item.time_str}")
                results['skipped_future'] += 1
                results['by_tenant'][tenant_id]['skipped_future'] += 1
                continue
            
            results['processed'] += 1
            results['by_tenant'][tenant_id]['processed'] += 1

            reuse = self.historical_reuse_report(item.media_filename, tenant_id=tenant_id)
            if reuse["status"] == REUSE_BLOCKED:
                logger.warning(f"⛔ [{tenant_id}] Bloqueado por reuse: {reuse['reason']}")
                results['blocked'] += 1
                results['by_tenant'][tenant_id]['blocked'] += 1
                continue

            post_id = self.process_item(item)
            
            if post_id:
                add_publication_record(self.logs[tenant_id], item, post_id)
                results['published'] += 1
                results['by_tenant'][tenant_id]['published'] += 1
            else:
                results['failed'] += 1
                results['by_tenant'][tenant_id]['failed'] += 1
        
        self._reuse_cache = {}

        # Guardar logs actualizados por tenant
        for tenant_id, log_rows in self.logs.items():
            tenant_results = results['by_tenant'].get(tenant_id, {})
            if tenant_results.get('published', 0) > 0:
                save_publication_log(tenant_id, log_rows)
                logger.info(f"📝 [{tenant_id}] Log actualizado")
        
        return results
    
    def run_daemon(self, check_interval: int = 30) -> None:
        """Ejecuta como daemon continuo"""
        logger.info(f"🚀 Iniciando daemon multi-tenant (check cada {check_interval}s)...")
        logger.info(f"Tenants: {', '.join(self.tenant_ids)}")
        logger.info("Presiona Ctrl+C para detener")
        
        try:
            while True:
                results = self.run_once()
                
                if results['processed'] > 0:
                    logger.info(f"\n{'='*60}")
                    logger.info(f"RESULTADOS:")
                    logger.info(f"  Procesados: {results['processed']}")
                    logger.info(f"  Publicados: {results['published']}")
                    logger.info(f"  Fallidos: {results['failed']}")
                    logger.info(f"  Futuros: {results['skipped_future']}")
                    for tid, tr in results['by_tenant'].items():
                        if tr['processed'] > 0:
                            logger.info(f"  [{tid}]: pub={tr['published']} fail={tr['failed']}")
                
                # Mostrar próximos por tenant
                pending = self.get_pending_items()
                for tenant_id in self.tenant_ids:
                    future = [p for p in pending if p.tenant_id == tenant_id and p.datetime_utc > datetime.now(timezone.utc)]
                    if future:
                        next_item = future[0]
                        logger.info(f"⏰ [{tenant_id}] Próximo: {next_item.date_str} {next_item.time_str}")
                
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            logger.info("\n🛑 Daemon detenido")


# ==============================================================================
# CLI ENTRY POINT
# ==============================================================================

def main(argv=None):
    import argparse
    import time
    
    parser = argparse.ArgumentParser(description='Instagram Scheduler Multi-Tenant para Growth OS')
    parser.add_argument('--tenant', type=str, help='Tenant específico (ej: firma-bordados)')
    parser.add_argument('--all-tenants', action='store_true', help='Procesar todos los tenants detectados')
    parser.add_argument('--schedule', type=str, help='Ruta manual al CSV de schedule (solo con --tenant)')
    parser.add_argument('--once', action='store_true', help='Ejecutar una sola pasada (para cron)')
    parser.add_argument('--daemon', action='store_true', help='Ejecutar como daemon continuo')
    parser.add_argument('--interval', type=int, default=30, help='Intervalo en daemon (segundos)')
    parser.add_argument('--dry-run', action='store_true', help='Solo mostrar qué se haría')
    parser.add_argument('--skip-metrics', action='store_true', help='No capturar snapshots E0/E24/E72 en esta pasada')
    
    args = parser.parse_args(argv)
    
    # Determinar tenants a procesar
    if args.tenant:
        tenant_ids = [args.tenant]
    elif args.all_tenants:
        tenant_ids = discover_tenants()
        if not tenant_ids:
            # Nada que publicar no es un error: el timer corre cada 15 min.
            logger.warning(
                "No hay tenants con credenciales IG; nada que publicar por ahora."
            )
            return 0
    else:
        parser.error("Debe especificar --tenant <id> o --all-tenants")
    
    logger.info(f"Tenants a procesar: {tenant_ids}")
    
    scheduler = IgScheduler(tenant_ids)
    
    if args.dry_run:
        pending = scheduler.get_pending_items()
        now = datetime.now(timezone.utc)
        
        logger.info(f"\n=== DRY-RUN ===")
        logger.info(f"Ahora (UTC): {now}")
        logger.info(f"Items pendientes: {len(pending)}")
        
        for item in pending:
            status = "LISTO" if item.datetime_utc <= now else f"FUTURO ({item.datetime_utc})"
            logger.info(f"  [{item.tenant_id}] {item.date_str} {item.time_str} | {item.media_filename} | {status}")
        return
    
    if args.daemon:
        scheduler.run_daemon(args.interval)
    else:
        # Default: run once (para cron)
        results = scheduler.run_once()
        
        logger.info(f"\n=== RESULTADOS ===")
        logger.info(f"Procesados: {results['processed']}")
        logger.info(f"Publicados: {results['published']}")
        logger.info(f"Fallidos: {results['failed']}")
        logger.info(f"Saltados (futuro): {results['skipped_future']}")
        
        for tid, tr in results['by_tenant'].items():
            if tr['processed'] > 0:
                logger.info(f"  [{tid}]: procesados={tr['processed']} publicados={tr['published']} fallidos={tr['failed']}")

        if not args.skip_metrics:
            from modules.intelligence.metrics_snapshot import run_capture_cycle

            for tid in tenant_ids:
                try:
                    metrics = run_capture_cycle(tid)
                    logger.info(f"📊 [{tid}] métricas: {metrics}")
                except Exception as exc:  # la publicación nunca debe fallar por métricas
                    logger.warning(f"📊 [{tid}] métricas no capturadas: {exc}")


if __name__ == '__main__':
    main()
