#!/usr/bin/env python3
"""
Instagram Scheduler Multi-Tenant para Growth OS

Programa publicaciones en Instagram para múltiples tenants.
Un solo cron procesa todos los tenants independientemente.
"""

import os
import sys
import csv
import logging
from pathlib import Path
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

from growth.ig_publisher import (
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
    
    def __init__(self, tenant_ids: List[str]):
        self.tenant_ids = tenant_ids
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
    
    def process_item(self, item: ScheduleItem) -> Optional[str]:
        logger.info(f"\n{'='*60}")
        logger.info(f"[{item.tenant_id}] Procesando: {item.date_str} {item.time_str} - {item.media_filename}")
        
        publisher = self.publishers.get(item.tenant_id)
        if not publisher:
            logger.error(f"[{item.tenant_id}] No hay publisher configurado")
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
            'by_tenant': {}
        }
        
        for item in pending:
            tenant_id = item.tenant_id
            if tenant_id not in results['by_tenant']:
                results['by_tenant'][tenant_id] = {
                    'processed': 0, 'published': 0, 'failed': 0, 'skipped_future': 0
                }
            
            # Verificar si ya es hora
            if item.datetime_utc > now:
                logger.info(f"⏭️  [{tenant_id}] Saltando (futuro): {item.date_str} {item.time_str}")
                results['skipped_future'] += 1
                results['by_tenant'][tenant_id]['skipped_future'] += 1
                continue
            
            results['processed'] += 1
            results['by_tenant'][tenant_id]['processed'] += 1
            
            post_id = self.process_item(item)
            
            if post_id:
                add_publication_record(self.logs[tenant_id], item, post_id)
                results['published'] += 1
                results['by_tenant'][tenant_id]['published'] += 1
            else:
                results['failed'] += 1
                results['by_tenant'][tenant_id]['failed'] += 1
        
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

def main():
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
    
    args = parser.parse_args()
    
    # Determinar tenants a procesar
    if args.tenant:
        tenant_ids = [args.tenant]
    elif args.all_tenants:
        tenant_ids = discover_tenants()
        if not tenant_ids:
            logger.error("No se detectaron tenants con credenciales válidas")
            sys.exit(1)
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


if __name__ == '__main__':
    main()
