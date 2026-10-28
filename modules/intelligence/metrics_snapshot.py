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


_INT_FIELDS = {
    'reactions', 'comments', 'shares',
    'reaction_like', 'reaction_love', 'reaction_wow', 'reaction_haha',
    'reaction_sorry', 'reaction_anger', 'reaction_care',
    'reach', 'impressions', 'views', 'saved', 'total_interactions',
    'engaged_users', 'clicks', 'video_views', 'video_watch_time',
    'page_impressions', 'page_reach', 'page_engaged_users',
    'attempts',
}


def _to_int(value: Any) -> int:
    """Coacciona enteros de Meta (int, str, dict de valores) sin romper el snapshot."""
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return 0
        try:
            return int(float(text))
        except ValueError:
            return 0
    if isinstance(value, dict):
        for key in ('value', 'total_count', 'count'):
            if key in value:
                return _to_int(value[key])
    return 0


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
    views: int = 0
    saved: int = 0
    total_interactions: int = 0
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
    attempts: int = 0
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec='seconds'))
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'MetricsSnapshot':
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in d.items() if k in valid_fields}
        for name in _INT_FIELDS:
            if name in filtered:
                filtered[name] = _to_int(filtered[name])
        if 'insights_available' in filtered:
            filtered['insights_available'] = str(filtered['insights_available']).strip().lower() in {'true', '1', 'yes'}
        return cls(**filtered)


SNAPSHOT_LOG_FIELDS = [
    'snapshot_id', 'publication_id', 'tenant_id', 'platform',
    'window', 'target_at_utc', 'captured_at_utc',
    'reactions', 'comments', 'shares',
    'reaction_like', 'reaction_love', 'reaction_wow', 'reaction_haha',
    'reaction_sorry', 'reaction_anger', 'reaction_care',
    'reach', 'impressions', 'views', 'saved', 'total_interactions',
    'engaged_users', 'clicks', 'video_views', 'video_watch_time',
    'page_impressions', 'page_reach', 'page_engaged_users',
    'status', 'error', 'insights_available', 'created_at', 'attempts'
]


def get_snapshot_log_path(tenant_id: str) -> Path:
    return Path(f'tenants/{tenant_id}/metrics_snapshot_log.csv')


VALID_WINDOWS = {SnapshotWindow.E0.value, SnapshotWindow.E24.value, SnapshotWindow.E72.value}
VALID_STATUSES = {status.value for status in SnapshotStatus}


def _read_ledger_rows(path: Path) -> List[Dict[str, str]]:
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def _ledger_has_foreign_rows(rows: List[Dict[str, str]]) -> bool:
    for row in rows:
        if row.get('window') not in VALID_WINDOWS:
            return True
        if row.get('status') not in VALID_STATUSES:
            return True
    return False


def load_snapshot_log(tenant_id: str) -> List[MetricsSnapshot]:
    log_path = get_snapshot_log_path(tenant_id)
    if not log_path.exists():
        return []

    raw_rows = _read_ledger_rows(log_path)
    if _ledger_has_foreign_rows(raw_rows):
        print(
            f"Warning: {log_path} tiene filas con esquema ajeno; "
            "se ignoran y se conservarán en un respaldo al escribir."
        )
        return []

    snapshots = []
    for row in raw_rows:
        try:
            snap = MetricsSnapshot.from_dict(row)
            snapshots.append(snap)
        except Exception as e:
            print(f"Warning: Error loading snapshot row: {e}")
    return snapshots


def save_snapshot_log(tenant_id: str, snapshots: List[MetricsSnapshot]) -> None:
    log_path = get_snapshot_log_path(tenant_id)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    if log_path.exists() and _ledger_has_foreign_rows(_read_ledger_rows(log_path)):
        backup = log_path.with_name(
            f"{log_path.stem}.legacy-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.csv"
        )
        log_path.rename(backup)
        print(f"Warning: ledger incompatible movido a {backup}")

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
        retryable_failure = snap.status == SnapshotStatus.FAILED.value and snap.attempts < 3
        if snap.status != SnapshotStatus.PENDING.value and not retryable_failure:
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
    pub_id = (publication_row.get('publication_id') or '').strip()
    platform = publication_row.get('platform', 'Facebook').split('/')[0]
    published = publication_target_utc(publication_row)
    if published is None:
        raise ValueError("La publicación no tiene fecha/hora válida para programar snapshots")

    offsets = {SnapshotWindow.E0.value: 0, SnapshotWindow.E24.value: 24, SnapshotWindow.E72.value: 72}
    if window not in offsets:
        raise ValueError(f"Ventana no soportada: {window}")
    target = published + timedelta(hours=offsets[window])
    
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


def _parse_local_datetime(value: Any) -> Optional[datetime]:
    text = str(value or '').strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace('Z', '+00:00'))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=ZoneInfo("America/Matamoros"))
    return parsed.astimezone(timezone.utc)


def publication_target_utc(publication_row: Dict[str, str]) -> Optional[datetime]:
    """Momento real de publicación de una fila del log.

    Instagram registra ``published_at`` cuando el post ya salió. Facebook se
    programa de forma nativa, así que su hora real es la del slot (date/time).
    """
    platform = (publication_row.get('platform') or '').lower()
    published_at = _parse_local_datetime(publication_row.get('published_at'))

    if 'instagram' in platform and published_at is not None:
        return published_at

    raw_date = str(publication_row.get('date') or '').strip()
    raw_time = str(publication_row.get('time') or '').strip().split('-')[0].strip()
    if raw_date and raw_time:
        slot = _parse_local_datetime(f"{raw_date}T{raw_time}:00")
        if slot is not None:
            return slot
    return published_at


def get_publication_log_path(tenant_id: str) -> Path:
    return Path(f'tenants/{tenant_id}/publication_log_week2.csv')


def load_publication_log(tenant_id: str) -> List[Dict[str, str]]:
    log_path = get_publication_log_path(tenant_id)
    if not log_path.exists():
        return []
    with log_path.open('r', encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def _is_real_meta_id(value: str) -> bool:
    value = (value or '').strip()
    if not value or value.startswith(('mock_', 'pub_')):
        return False
    return any(char.isdigit() for char in value)


def ensure_snapshots_for_publications(
    tenant_id: str,
    since_days: int = 4,
    now: Optional[datetime] = None,
) -> List[MetricsSnapshot]:
    """Crea E0/E24/E72 pendientes para publicaciones ya registradas.

    Es idempotente: no duplica ventanas que ya existan para el mismo
    ``publication_id``. Se puede llamar en cada ciclo de captura. Solo mira
    publicaciones recientes para no llenar la cola con históricos.
    """
    if now is None:
        now = datetime.now(timezone.utc)
    existing = {(snap.publication_id, snap.window) for snap in load_snapshot_log(tenant_id)}
    created: List[MetricsSnapshot] = []

    for row in load_publication_log(tenant_id):
        if (row.get('status') or '').strip().lower() not in {'published', 'scheduled'}:
            continue
        pub_id = (row.get('publication_id') or '').strip()
        if not _is_real_meta_id(pub_id):
            continue
        try:
            published = publication_target_utc(row)
        except ValueError:
            continue
        if published is None:
            continue
        if published < now - timedelta(days=since_days):
            continue
        for window in (SnapshotWindow.E0.value, SnapshotWindow.E24.value, SnapshotWindow.E72.value):
            if (pub_id, window) in existing:
                continue
            snapshot = create_snapshot_for_publication(tenant_id, row, '', '', window)
            upsert_snapshot(tenant_id, snapshot)
            existing.add((pub_id, window))
            created.append(snapshot)
    return created


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
        counts['reactions'] = _to_int(result.get('reactions', {}).get('summary', {}).get('total_count', 0))
        counts['comments'] = _to_int(result.get('comments', {}).get('summary', {}).get('total_count', 0))
        counts['shares'] = _to_int(result.get('shares', {}).get('count', 0))
    
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
    """Captura insights del post de Facebook de una métrica a la vez.

    Meta rechaza la llamada completa si una sola métrica no está disponible, por
    eso se consultan por separado y las no disponibles se reportan en
    ``_unavailable_metrics`` en lugar de perder el resto.
    """
    insights: Dict[str, Any] = {}
    unavailable = []
    metrics_to_try = [
        ('post_reactions_by_type_total', 'lifetime'),
        ('post_clicks', 'lifetime'),
        ('post_engaged_users', 'lifetime'),
        ('post_impressions', 'lifetime'),
        ('post_impressions_unique', 'lifetime'),
        ('post_video_views', 'lifetime'),
        ('post_video_avg_time_watched', 'lifetime'),
    ]
    
    for metric, period in metrics_to_try:
        result = api_get(page_token, f'{post_id}/insights', {'metric': metric, 'period': period})
        data = result.get('data', []) if 'error' not in result else []
        values = data[0].get('values', []) if data else []
        if values:
            insights[metric] = values[0].get('value')
        else:
            unavailable.append(metric)
    
    if unavailable:
        insights['_unavailable_metrics'] = ','.join(unavailable)
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
    """Captura métricas de Instagram Media (post/reel) métrica por métrica.

    ``impressions`` y ``engagement`` ya no son válidas para media insights en
    Graph v26; se usa ``views`` y ``total_interactions``. Cada métrica se pide
    por separado para que una métrica retirada no invalide toda la captura.
    """
    insights: Dict[str, Any] = {}
    unavailable = []
    metrics = ['reach', 'views', 'total_interactions', 'saved', 'likes', 'comments', 'shares']
    
    for metric in metrics:
        result = api_get(page_token, f'{ig_media_id}/insights', {'metric': metric})
        if not isinstance(result, dict):
            unavailable.append(metric)
            continue
        if 'error' in result:
            error_msg = str(result.get('error', ''))
            error_code = str(result.get('code', ''))
            if 'permission' in error_msg.lower() or error_code == '10':
                insights['_permission_error'] = 'instagram_manage_insights required (App Review)'
                return insights
            unavailable.append(metric)
            continue
        data = result.get('data', [])
        values = data[0].get('values', []) if data else []
        if values:
            insights[metric] = values[0].get('value')
        else:
            unavailable.append(metric)
    
    if unavailable:
        insights['_unavailable_metrics'] = ','.join(unavailable)
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
    snapshot.attempts += 1
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
            insights = capture_post_insights(page_token, post_id)
            for metric, val in insights.items():
                if metric.startswith('_'):
                    continue
                if metric == 'post_reactions_by_type_total' and isinstance(val, dict):
                    for k, v in val.items():
                        k_lower = k.lower()
                        if 'like' in k_lower:
                            snapshot.reaction_like = _to_int(v)
                        elif 'love' in k_lower:
                            snapshot.reaction_love = _to_int(v)
                        elif 'wow' in k_lower:
                            snapshot.reaction_wow = _to_int(v)
                        elif 'haha' in k_lower:
                            snapshot.reaction_haha = _to_int(v)
                        elif 'sorry' in k_lower or 'sad' in k_lower:
                            snapshot.reaction_sorry = _to_int(v)
                        elif 'anger' in k_lower or 'angry' in k_lower:
                            snapshot.reaction_anger = _to_int(v)
                        elif 'care' in k_lower:
                            snapshot.reaction_care = _to_int(v)
                elif metric == 'post_clicks':
                    snapshot.clicks = _to_int(val)
                elif metric == 'post_engaged_users':
                    snapshot.engaged_users = _to_int(val)
                elif metric == 'post_impressions':
                    snapshot.impressions = _to_int(val)
                elif metric == 'post_impressions_unique':
                    snapshot.reach = _to_int(val)
                elif metric == 'post_video_views':
                    snapshot.video_views = _to_int(val)
                elif metric == 'post_video_avg_time_watched':
                    snapshot.video_watch_time = _to_int(val)
            insights_captured = any(not key.startswith('_') for key in insights)
        
        # 4. Instagram Media Insights (posts/reels de Instagram)
        elif snapshot.platform.lower() == 'instagram' and ig_id:
            # Conteos públicos de IG vienen como like_count/comments_count.
            media = api_get(page_token, post_id, {'fields': 'like_count,comments_count,media_type'})
            if isinstance(media, dict) and 'error' not in media:
                snapshot.reactions = _to_int(media.get('like_count', 0))
                snapshot.comments = _to_int(media.get('comments_count', 0))

            ig_insights = capture_instagram_insights(page_token, post_id)
            if ig_insights and '_permission_error' not in ig_insights:
                insights_captured = any(not key.startswith('_') for key in ig_insights)
                snapshot.reach = _to_int(ig_insights.get('reach', snapshot.reach))
                snapshot.views = _to_int(ig_insights.get('views', snapshot.views))
                snapshot.saved = _to_int(ig_insights.get('saved', snapshot.saved))
                snapshot.total_interactions = _to_int(
                    ig_insights.get('total_interactions', snapshot.total_interactions)
                )
                if 'likes' in ig_insights:
                    snapshot.reactions = _to_int(ig_insights['likes'])
                if 'comments' in ig_insights:
                    snapshot.comments = _to_int(ig_insights['comments'])
                if 'shares' in ig_insights:
                    snapshot.shares = _to_int(ig_insights['shares'])
                if '_unavailable_metrics' in ig_insights:
                    snapshot.error = f"Insights no disponibles: {ig_insights['_unavailable_metrics']}"
            elif ig_insights.get('_permission_error'):
                snapshot.error = ig_insights['_permission_error']
        
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
        if not insights_captured and not snapshot.error:
            snapshot.status = SnapshotStatus.NO_DATA.value
            snapshot.error = "Sin insights de Meta; solo conteos públicos"
        
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

    scheduled = ensure_snapshots_for_publications(tenant_id)
    
    page_token = get_page_token(user_token, page_id)
    if not page_token:
        return {'error': 'Could not get page token', 'captured': 0, 'failed': 0}
    
    ig_id = get_ig_id(user_token, page_id) or ""
    
    pending = get_pending_snapshots(tenant_id)
    
    results = {'scheduled': len(scheduled), 'captured': 0, 'failed': 0, 'skipped': 0, 'no_data': 0}
    
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
            created = ensure_snapshots_for_publications(tenant)
            print(f"Snapshots programados ({tenant}): {len(created)}")
            for snap in created:
                print(f"  {snap.snapshot_id} | {snap.window} | {snap.target_at_utc} | {snap.publication_id}")
