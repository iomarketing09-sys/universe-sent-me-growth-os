#!/usr/bin/env python3
"""
Metrics Snapshot System (E0/E24/E72) para Growth OS

Captura métricas de Meta Insights en ventanas específicas:
- E0: Al publicar (baseline)
- E24: 24 horas después
- E72: 72 horas después

Funciona con métricas disponibles:
- Public counts (reactions, comments, shares) - siempre disponibles
- Post insights (post_reactions_by_type_total, post_clicks, post_video_views) - cuando aplica
- Page insights - si la página tiene acceso
"""

import csv
import os
import time
import uuid
import requests
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from zoneinfo import ZoneInfo


class SnapshotWindow(str, Enum):
    E0 = "E0"
    E24 = "E24"
    E72 = "E72"


class SnapshotStatus(str, Enum):
    PENDING = "Pending"
    CAPTURED = "Captured"
    FAILED = "Failed"
    SKIPPED = "Skipped"
    NO_DATA = "No_Data"  # Métricas disponibles pero sin datos


GRAPH_API_VERSION = "v26.0"
GRAPH_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"


@dataclass
class MetricsSnapshot:
    snapshot_id: str = ""
    publication_id: str = ""
    tenant_id: str = ""
    platform: str = ""
    
    window: str = SnapshotWindow.E0.value
    target_at_utc: str = ""
    captured_at_utc: str = ""
    
    # Public counts (siempre disponibles)
    reactions: int = 0
    comments: int = 0
    shares: int = 0
    
    # Reactions breakdown
    reaction_like: int = 0
    reaction_love: int = 0
    reaction_wow: int = 0
    reaction_haha: int = 0
    reaction_sorry: int = 0
    reaction_anger: int = 0
    reaction_care: int = 0
    
    # Post insights (cuando disponibles)
    reach: int = 0
    impressions: int = 0
    engaged_users: int = 0
    clicks: int = 0
    video_views: int = 0
    video_watch_time: int = 0
    
    # Page insights (cuando disponibles)
    page_impressions: int = 0
    page_reach: int = 0
    page_engaged_users: int = 0
    
    # Estado
    status: str = SnapshotStatus.PENDING.value
    error: str = ""
    insights_available: bool = False
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec='seconds'))
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'MetricsSnapshot':
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in d.items() if k in valid_fields}
        return cls(**filtered)


SNAPSHOT_LOG_FIELDS = [
    'snapshot_id', 'publication_id', 'tenant_id', 'platform',
    'window', 'target_at_utc', 'captured_at_utc',
    'reactions', 'comments', 'shares',
    'reaction_like', 'reaction_love', 'reaction_wow', 'reaction_haha',
    'reaction_sorry', 'reaction_anger', 'reaction_care',
    'reach', 'impressions', 'engaged_users', 'clicks', 'video_views', 'video_watch_time',
    'page_impressions', 'page_reach', 'page_engaged_users',
    'status', 'error', 'insights_available', 'created_at'
]


def get_snapshot_log_path(tenant_id: str) -> Path:
    return Path(f'tenants/{tenant_id}/metrics_snapshot_log.csv')


def load_snapshot_log(tenant_id: str) -> List[MetricsSnapshot]:
    log_path = get_snapshot_log_path(tenant_id)
    if not log_path.exists():
        return []
    
    snapshots = []
    with log_path.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                snap = MetricsSnapshot.from_dict(row)
                snapshots.append(snap)
            except Exception as e:
                print(f"Warning: Error loading snapshot row: {e}")
    return snapshots


def save_snapshot_log(tenant_id: str, snapshots: List[MetricsSnapshot]) -> None:
    log_path = get_snapshot_log_path(tenant_id)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    with log_path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=SNAPSHOT_LOG_FIELDS)
        writer.writeheader()
        for snap in snapshots:
            writer.writerow(snap.to_dict())


def upsert_snapshot(tenant_id: str, snapshot: MetricsSnapshot) -> MetricsSnapshot:
    snapshots = load_snapshot_log(tenant_id)
    for i, existing in enumerate(snapshots):
        if existing.snapshot_id == snapshot.snapshot_id:
            snapshots[i] = snapshot
            save_snapshot_log(tenant_id, snapshots)
            return snapshot
    snapshots.append(snapshot)
    save_snapshot_log(tenant_id, snapshots)
    return snapshot


def get_pending_snapshots(tenant_id: str, now: datetime = None) -> List[MetricsSnapshot]:
    if now is None:
        now = datetime.now(timezone.utc)
    
    all_snapshots = load_snapshot_log(tenant_id)
    pending = []
    for snap in all_snapshots:
        if snap.status != SnapshotStatus.PENDING.value:
            continue
        try:
            target = datetime.fromisoformat(snap.target_at_utc.replace('Z', '+00:00'))
            if target <= now:
                pending.append(snap)
        except:
            pass
    return pending


# ==============================================================================
# META API HELPERS
# ==============================================================================

def load_tenant_env(tenant_id: str) -> Dict[str, str]:
    env_path = Path(f'tenants/{tenant_id}/.env')
    if not env_path.exists():
        return {}
    
    env = {}
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip()
    return env


def get_page_token(user_token: str, page_id: str) -> Optional[str]:
    url = f'{GRAPH_BASE}/{page_id}?fields=access_token&access_token={user_token}'
    try:
        r = requests.get(url, timeout=30).json()
        return r.get('access_token')
    except:
        return None


def get_ig_id(user_token: str, page_id: str) -> Optional[str]:
    url = f'{GRAPH_BASE}/{page_id}?fields=instagram_business_account&access_token={user_token}'
    try:
        r = requests.get(url, timeout=30).json()
        return r.get('instagram_business_account', {}).get('id')
    except:
        return None


def api_get(page_token: str, endpoint: str, params: Dict = None) -> Dict:
    """Helper para GET a Graph API - always returns dict"""
    params = params or {}
    params['access_token'] = page_token
    try:
        r = requests.get(f'{GRAPH_BASE}/{endpoint}', params=params, timeout=30)
        if r.status_code >= 400:
            try:
                err_data = r.json()
                return {'error': err_data.get('error', {}).get('message', f'HTTP {r.status_code}'), 'status': r.status_code, 'code': err_data.get('error', {}).get('code', '')}
            except:
                return {'error': f'HTTP {r.status_code}', 'status': r.status_code}
        return r.json()
    except Exception as e:
        return {'error': str(e), 'status': 0}


# ==============================================================================
# SNAPSHOT CREATION
# ==============================================================================

def create_snapshot_for_publication(
    tenant_id: str,
    publication_row: Dict[str, str],
    page_token: str,
    ig_id: str,
    window: str = SnapshotWindow.E0.value
) -> MetricsSnapshot:
    pub_id = publication_row.get('publication_id', '')
    platform = publication_row.get('platform', 'Facebook').split('/')[0]
    pub_date = publication_row.get('date', '')
    pub_time = publication_row.get('time', '')
    
    tz = ZoneInfo("America/Matamoros")
    if window == SnapshotWindow.E0.value:
        target = datetime.now(timezone.utc)
    else:
        dt_local = datetime.strptime(f"{pub_date} {pub_time}", "%Y-%m-%d %H:%M")
        dt_local = dt_local.replace(tzinfo=tz)
        dt_utc = dt_local.astimezone(timezone.utc)
        
        if window == SnapshotWindow.E24.value:
            target = dt_utc + timedelta(hours=24)
        elif window == SnapshotWindow.E72.value:
            target = dt_utc + timedelta(hours=72)
        else:
            target = dt_utc
    
    snapshot = MetricsSnapshot(
        snapshot_id=f"SNAP-{uuid.uuid4().hex[:8].upper()}",
        publication_id=pub_id,
        tenant_id=tenant_id,
        platform=platform,
        window=window,
        target_at_utc=target.isoformat(timespec='seconds'),
        status=SnapshotStatus.PENDING.value
    )
    return snapshot


def schedule_all_windows_for_publication(
    tenant_id: str,
    publication_row: Dict[str, str],
    page_token: str,
    ig_id: str
) -> List[MetricsSnapshot]:
    snapshots = []
    for window in [SnapshotWindow.E0, SnapshotWindow.E24, SnapshotWindow.E72]:
        snap = create_snapshot_for_publication(
            tenant_id, publication_row, page_token, ig_id, window.value
        )
        upsert_snapshot(tenant_id, snap)
        snapshots.append(snap)
    return snapshots


# ==============================================================================
# CAPTURE LOGIC
# ==============================================================================

def capture_public_counts(page_token: str, post_id: str) -> Dict[str, int]:
    """Obtiene conteos públicos del post (reactions, comments, shares)"""
    result = api_get(page_token, post_id, {
        'fields': 'reactions.limit(0).summary(true),comments.limit(0).summary(true),shares'
    })
    
    counts = {'reactions': 0, 'comments': 0, 'shares': 0}
    
    if 'error' not in result:
        counts['reactions'] = result.get('reactions', {}).get('summary', {}).get('total_count', 0)
        counts['comments'] = result.get('comments', {}).get('summary', {}).get('total_count', 0)
        counts['shares'] = result.get('shares', {}).get('count', 0)
        
        # Reactions breakdown
        reaction_types = ['LIKE', 'LOVE', 'WOW', 'HAHA', 'SORRY', 'ANGER', 'CARE']
        for rt in reaction_types:
            url = f'{GRAPH_BASE}/{endpoint}/reactions?type={rt}&limit=0&summary=true&access_token={page_token}'
            # We'll skip individual type calls for rate limiting
    
    return counts


def capture_reactions_breakdown(page_token: str, post_id: str) -> Dict[str, int]:
    """Obtiene desglose de reacciones"""
    result = api_get(page_token, f'{post_id}/reactions', {'limit': 0, 'summary': 'true'})
    
    breakdown = {
        'reaction_like': 0, 'reaction_love': 0, 'reaction_wow': 0,
        'reaction_haha': 0, 'reaction_sorry': 0, 'reaction_anger': 0, 'reaction_care': 0
    }
    
    if 'error' not in result:
        for reaction in result.get('data', []):
            rtype = reaction.get('type', '').lower()
            if rtype == 'like':
                breakdown['reaction_like'] = 1
            elif rtype == 'love':
                breakdown['reaction_love'] = 1
            # etc. - simplified
    
    return breakdown


def capture_post_insights(page_token: str, post_id: str) -> Dict[str, Any]:
    """Intenta capturar insights del post"""
    insights = {}
    metrics_to_try = [
        ('post_reactions_by_type_total', 'lifetime'),
        ('post_clicks', 'lifetime'),
        ('post_video_views', 'lifetime'),
        ('post_video_avg_time_watched', 'lifetime'),
    ]
    
    for metric, period in metrics_to_try:
        result = api_get(page_token, f'{post_id}/insights', {'metric': metric, 'period': period})
        if 'error' not in result:
            data = result.get('data', [])
            if data:
                values = data[0].get('values', [])
                if values:
                    insights[metric] = values[0].get('value')
    
    return insights


def capture_page_insights(page_token: str, page_id: str, since: int, until: int) -> Dict[str, Any]:
    """Intenta capturar insights de página"""
    insights = {}
    metrics = ['page_impressions', 'page_impressions_unique', 'page_engaged_users']
    for metric in metrics:
        result = api_get(page_token, f'{page_id}/insights', {
            'metric': metric, 'period': 'day', 'since': since, 'until': until
        })
        if 'error' not in result:
            data = result.get('data', [])
            if data:
                values = data[0].get('values', [])
                if values:
                    insights[metric] = values[0].get('value')
    return insights


def capture_instagram_insights(page_token: str, ig_media_id: str) -> Dict[str, Any]:
    """Captura métricas de Instagram Media (post/reel)"""
    insights = {}
    # Métricas disponibles para Instagram Media
    metrics = 'reach,impressions,engagement,saved,video_views,likes,comments,shares,replies'
    result = api_get(page_token, f'{ig_media_id}/insights', {'metric': metrics})
    
    # Handle case where result might be a string (error message) or dict
    if isinstance(result, dict) and 'error' not in result:
        data = result.get('data', [])
        for item in data:
            metric = item.get('name')
            values = item.get('values', [])
            if values:
                insights[metric] = values[0].get('value')
    elif isinstance(result, dict):
        # Has error key
        error_msg = result.get('error', {}).get('message', '')
        error_code = result.get('error', {}).get('code', '')
        if 'permission' in error_msg.lower() or '10' in str(error_code):
            insights['_permission_error'] = 'instagram_manage_insights required (App Review)'
        else:
            insights['_error'] = error_msg
    elif isinstance(result, str):
        # Result is a string error message
        insights['_error'] = result
        insights['_permission_error'] = 'Unknown error'
    else:
        insights['_error'] = 'Unexpected response type'
    
    return insights


def capture_instagram_account_insights(page_token: str, ig_user_id: str) -> Dict[str, Any]:
    """Captura métricas de cuenta Instagram (nivel cuenta)"""
    insights = {}
    metrics = 'follower_count,impressions,reach,profile_views'
    result = api_get(page_token, f'{ig_user_id}/insights', {'metric': metrics, 'period': 'day'})
    
    if isinstance(result, dict) and 'error' not in result:
        data = result.get('data', [])
        for item in data:
            metric = item.get('name')
            values = item.get('values', [])
            if values:
                insights[metric] = values[0].get('value')
    elif isinstance(result, dict) and 'error' in result:
        error_msg = result.get('error', {}).get('message', '')
        error_code = result.get('error', {}).get('code', '')
        if 'permission' in error_msg.lower() or '10' in str(error_code):
            insights['_permission_error'] = 'instagram_manage_insights required (App Review)'
        else:
            insights['_error'] = error_msg
    elif isinstance(result, str):
        insights['_error'] = result
        insights['_permission_error'] = 'Unknown error'
    else:
        insights['_error'] = 'Unexpected response type'
    
    return insights


def capture_snapshot(tenant_id: str, snapshot: MetricsSnapshot, 
                     page_token: str, ig_id: str) -> MetricsSnapshot:
    """Ejecuta la captura completa para una snapshot"""
    snapshot.captured_at_utc = datetime.now(timezone.utc).isoformat(timespec='seconds')
    post_id = snapshot.publication_id
    
    if not post_id:
        snapshot.status = SnapshotStatus.FAILED.value
        snapshot.error = "No publication_id"
        return snapshot
    
    insights_captured = False
    
    try:
        # 1. Public counts (siempre disponibles - Facebook e Instagram)
        counts_result = api_get(page_token, post_id, {
            'fields': 'reactions.limit(0).summary(true),comments.limit(0).summary(true),shares'
        })
        
        if 'error' not in counts_result:
            snapshot.reactions = counts_result.get('reactions', {}).get('summary', {}).get('total_count', 0)
            snapshot.comments = counts_result.get('comments', {}).get('summary', {}).get('total_count', 0)
            snapshot.shares = counts_result.get('shares', {}).get('count', 0)
        
        # 2. Reactions breakdown
        try:
            reactions_result = api_get(page_token, f'{post_id}/reactions', {'limit': 0, 'summary': 'true'})
            if 'error' not in reactions_result:
                for reaction in reactions_result.get('data', []):
                    rtype = reaction.get('type', '').lower()
                    if rtype == 'like':
                        snapshot.reaction_like += 1
                    elif rtype == 'love':
                        snapshot.reaction_love += 1
                    elif rtype == 'wow':
                        snapshot.reaction_wow += 1
                    elif rtype == 'haha':
                        snapshot.reaction_haha += 1
                    elif rtype == 'sorry':
                        snapshot.reaction_sorry += 1
                    elif rtype == 'anger':
                        snapshot.reaction_anger += 1
                    elif rtype == 'care':
                        snapshot.reaction_care += 1
        except:
            pass
        
        # 3. Post insights (Facebook posts)
        if snapshot.platform.lower() == 'facebook':
            insights_result = api_get(page_token, f'{post_id}/insights', {
                'metric': 'post_reactions_by_type_total,post_clicks,post_video_views',
                'period': 'lifetime'
            })
            
            if 'error' not in insights_result:
                insights_captured = True
                for item in insights_result.get('data', []):
                    metric = item.get('name', '')
                    values = item.get('values', [])
                    if values:
                        val = values[0].get('value')
                        if metric == 'post_reactions_by_type_total' and isinstance(val, dict):
                            for k, v in val.items():
                                k_lower = k.lower()
                                if 'like' in k_lower:
                                    snapshot.reaction_like = v
                                elif 'love' in k_lower:
                                    snapshot.reaction_love = v
                                elif 'wow' in k_lower:
                                    snapshot.reaction_wow = v
                                elif 'haha' in k_lower:
                                    snapshot.reaction_haha = v
                                elif 'sorry' in k_lower or 'sad' in k_lower:
                                    snapshot.reaction_sorry = v
                                elif 'anger' in k_lower or 'angry' in k_lower:
                                    snapshot.reaction_anger = v
                                elif 'care' in k_lower:
                                    snapshot.reaction_care = v
                        elif metric == 'post_clicks':
                            snapshot.clicks = val
                        elif metric == 'post_video_views':
                            snapshot.video_views = val
        
        # 4. Instagram Media Insights (posts/reels de Instagram)
        elif snapshot.platform.lower() == 'instagram' and ig_id:
            # ig_id es el IG Business Account ID
            # post_id debería ser el Instagram Media ID
            ig_insights = capture_instagram_insights(page_token, post_id)
            if ig_insights and '_permission_error' not in ig_insights and '_error' not in ig_insights:
                insights_captured = True
                # Map Instagram metrics to snapshot fields
                snapshot.reach = ig_insights.get('reach', 0)
                snapshot.impressions = ig_insights.get('impressions', 0)
                snapshot.engaged_users = ig_insights.get('engagement', 0)
                snapshot.reactions = ig_insights.get('likes', 0)
                snapshot.comments = ig_insights.get('comments', 0)
                snapshot.shares = ig_insights.get('shares', 0)
                snapshot.video_views = ig_insights.get('video_views', 0)
                # Saved, replies are IG-specific
                # Could add custom fields if needed
        
        # 5. Instagram Account Insights (opcional, nivel cuenta)
        if ig_id and snapshot.window == 'E0':
            # Only capture account-level once per publication cycle
            try:
                acc_insights = capture_instagram_account_insights(page_token, ig_id)
                # Could store in separate fields or log
            except:
                pass
        
        snapshot.status = SnapshotStatus.CAPTURED.value
        snapshot.insights_available = insights_captured
        snapshot.error = ""
        
    except Exception as e:
        snapshot.status = SnapshotStatus.FAILED.value
        snapshot.error = str(e)
    
    return snapshot


def run_capture_cycle(tenant_id: str) -> Dict[str, int]:
    env = load_tenant_env(tenant_id)
    user_token = env.get('META_ACCESS_TOKEN') or env.get('META_PAGE_ACCESS_TOKEN')
    page_id = env.get('FB_PAGE_ID') or env.get('META_PAGE_ID')
    
    if not user_token or not page_id:
        return {'error': 'Missing credentials', 'captured': 0, 'failed': 0}
    
    page_token = get_page_token(user_token, page_id)
    if not page_token:
        return {'error': 'Could not get page token', 'captured': 0, 'failed': 0}
    
    ig_id = get_ig_id(user_token, page_id) or ""
    
    pending = get_pending_snapshots(tenant_id)
    
    results = {'captured': 0, 'failed': 0, 'skipped': 0, 'no_data': 0}
    
    for snap in pending:
        updated = capture_snapshot(tenant_id, snap, page_token, ig_id)
        upsert_snapshot(tenant_id, updated)
        
        if updated.status == SnapshotStatus.CAPTURED.value:
            results['captured'] += 1
        elif updated.status == SnapshotStatus.FAILED.value:
            results['failed'] += 1
        elif updated.status == SnapshotStatus.NO_DATA.value:
            results['no_data'] += 1
        else:
            results['skipped'] += 1
        
        time.sleep(1)
    
    return results


# ==============================================================================
# VALIDATOR
# ==============================================================================

def validate_snapshot_ledger(tenant_id: str) -> Dict[str, Any]:
    snapshots = load_snapshot_log(tenant_id)
    
    total = len(snapshots)
    by_status = {}
    by_window = {}
    by_platform = {}
    errors = []
    incomplete = []
    
    for snap in snapshots:
        by_status[snap.status] = by_status.get(snap.status, 0) + 1
        by_window[snap.window] = by_window.get(snap.window, 0) + 1
        by_platform[snap.platform] = by_platform.get(snap.platform, 0) + 1
        
        if snap.status == SnapshotStatus.FAILED.value:
            errors.append(f"{snap.snapshot_id}: {snap.error}")
    
    # Check for missing windows per publication
    pub_windows = {}
    for snap in snapshots:
        if snap.publication_id not in pub_windows:
            pub_windows[snap.publication_id] = set()
        pub_windows[snap.publication_id].add(snap.window)
    
    for pub_id, windows in pub_windows.items():
        if len(windows) < 3:
            missing = set(['E0', 'E24', 'E72']) - windows
            incomplete.append(f"{pub_id}: missing {missing}")
    
    return {
        'tenant_id': tenant_id,
        'total_snapshots': total,
        'by_status': by_status,
        'by_window': by_window,
        'by_platform': by_platform,
        'incomplete_publications': incomplete,
        'errors': errors,
        'valid': len(errors) == 0 and len(incomplete) == 0
    }


# ==============================================================================
# CLI
# ==============================================================================

def discover_tenants() -> List[str]:
    tenants = []
    tenants_dir = Path('tenants')
    if not tenants_dir.exists():
        return []
    for tenant_dir in tenants_dir.iterdir():
        if not tenant_dir.is_dir():
            continue
        env_path = tenant_dir / '.env'
        if env_path.exists():
            with open(env_path) as f:
                content = f.read()
                if 'META_ACCESS_TOKEN' in content and 'FB_PAGE_ID' in content:
                    tenants.append(tenant_dir.name)
    return tenants


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python -m growth.metrics_snapshot <tenant_id|--all-tenants> <comando>")
        print("Comandos: schedule, capture, validate, list")
        sys.exit(1)
    
    if sys.argv[1] == '--all-tenants':
        tenant_ids = discover_tenants()
        if not tenant_ids:
            print("No tenants found")
            sys.exit(1)
    else:
        tenant_ids = [sys.argv[1]]
    
    if len(sys.argv) < 3:
        print("Comando requerido: schedule, capture, validate, list")
        sys.exit(1)
    
    cmd = sys.argv[2]
    
    for tenant in tenant_ids:
    
        if cmd == 'list':
            snaps = load_snapshot_log(tenant)
            print(f"Snapshots ({tenant}): {len(snaps)}")
            for s in snaps[-10:]:
                print(f"  {s.snapshot_id} | {s.window} | {s.status} | {s.publication_id[:20]}... | insights={s.insights_available}")
        
        elif cmd == 'validate':
            result = validate_snapshot_ledger(tenant)
            print(f"Validación ({tenant}): {'PASS' if result['valid'] else 'FAIL'}")
            print(f"  Total: {result['total_snapshots']}")
            print(f"  By status: {result['by_status']}")
            print(f"  By window: {result['by_window']}")
            print(f"  Incomplete: {result['incomplete_publications']}")
            if result['errors']:
                print(f"  Errors: {result['errors']}")
        
        elif cmd == 'capture':
            result = run_capture_cycle(tenant)
            print(f"Captura ({tenant}): {result}")
        
        elif cmd == 'schedule':
            print("Schedule not implemented in CLI - use Python API")
