"""Reporte semanal para el cliente: domingo a sábado, con comparativo."""

from __future__ import annotations

import argparse
import csv
import html
import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from modules.intelligence.report_template import (
    DEEP,
    GOLD,
    INK,
    MUTED,
    ORANGE,
    PAPER,
    RULE,
)

ConversationProvider = Callable[..., Dict[str, Any]]

GRAPH_API_VERSION = "v26.0"
GRAPH_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

CHANNEL_LABELS = {
    "facebook_organic": "Facebook orgánico",
    "facebook_paid": "Facebook pauta",
    "instagram_organic": "Instagram orgánico",
    "instagram_paid": "Instagram pauta",
    "other_paid": "Otros espacios",
}

CHANNEL_ORDER = tuple(CHANNEL_LABELS)

FACEBOOK_PAGE_METRICS = (
    "page_post_engagements",
    "page_views_total",
    "page_video_views",
    "page_actions_post_reactions_total",
    "page_daily_follows",
)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def week_bounds(reference: date) -> tuple[date, date]:
    """Semana domingo–sábado ya cerrada respecto a ``reference``."""
    offset = (reference.weekday() + 1) % 7
    current_start = reference - timedelta(days=offset)
    end = current_start - timedelta(days=1)
    return end - timedelta(days=6), end


def _clip(text: str, limit: int = 70) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0].rstrip(" ,;:")
    return (cut or text[: limit - 1].rstrip()) + "…"


def _load_publications(tenant_dir: Path, start: date, end: date) -> List[Dict[str, str]]:
    items: List[Dict[str, str]] = []
    for path in sorted(tenant_dir.glob("publication_log*.csv")):
        try:
            with path.open(encoding="utf-8-sig", newline="") as handle:
                for row in csv.DictReader(handle):
                    raw = (row.get("date") or "").strip()
                    status = (row.get("status") or "").strip().lower()
                    if status not in {"published", "scheduled"}:
                        continue
                    try:
                        day = date.fromisoformat(raw)
                    except ValueError:
                        continue
                    if start <= day <= end:
                        items.append(
                            {
                                "date": raw,
                                "platform": (row.get("platform") or "").strip(),
                                "piece": (row.get("piece") or "").strip(),
                                "status": status,
                            }
                        )
        except (OSError, csv.Error, UnicodeDecodeError):
            continue
    return sorted(items, key=lambda item: item["date"])


def _load_actions(tenant_dir: Path, start: date, end: date) -> List[Dict[str, Any]]:
    path = tenant_dir / "ads" / "insights" / "actions.jsonl"
    if not path.is_file():
        return []
    items = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            entry = json.loads(line)
            moment = datetime.fromisoformat(str(entry.get("timestamp"))).date()
        except (ValueError, TypeError):
            continue
        if start <= moment <= end:
            items.append(entry)
    return items


def _meta_week_cache_path(root: Path, tenant_id: str, start: date, end: date) -> Path:
    return (
        root
        / "tenants"
        / tenant_id
        / "ads"
        / "insights"
        / "captures"
        / f"weekly_meta_{start}_{end}.json"
    )


def _empty_channels(note: str = "Sin captura local de métricas de Meta.") -> Dict[str, Dict[str, Any]]:
    channels = {}
    for key, label in CHANNEL_LABELS.items():
        channels[key] = {
            "key": key,
            "label": label,
            "reach": None,
            "impressions": None,
            "interactions": None,
            "clicks": None,
            "spend": None,
            "conversations": None,
            "cost_per_conversation": None,
            "pieces": None,
            "status": "unavailable",
            "note": note,
        }
    return channels


def _normalize_meta_week(payload: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    channels = _empty_channels()
    if isinstance(payload, dict):
        for key, value in (payload.get("channels") or {}).items():
            if key in channels and isinstance(value, dict):
                channels[key].update(value)
                channels[key]["key"] = key
                channels[key]["label"] = CHANNEL_LABELS[key]
    normalized = dict(payload or {})
    normalized["channels"] = channels
    return normalized


def _load_meta_week(root: Path, tenant_id: str, start: date, end: date) -> Dict[str, Any]:
    path = _meta_week_cache_path(root, tenant_id, start, end)
    try:
        return _normalize_meta_week(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, ValueError):
        return _normalize_meta_week({})


def _ledger_organic_week(
    root: Path,
    tenant_id: str,
    start: date,
    end: date,
    timezone: ZoneInfo,
) -> Dict[str, Optional[Dict[str, Any]]]:
    """Orgánico desde el ledger del tenant, sin llamar a Meta."""
    tenant_dir = root / "tenants" / tenant_id
    latest: Dict[tuple, Dict[str, str]] = {}
    snapshot_path = tenant_dir / "metrics_snapshot_log.csv"
    if snapshot_path.exists():
        with snapshot_path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                platform = str(row.get("platform") or "").lower()
                if platform not in {"facebook", "instagram"}:
                    continue
                try:
                    moment = datetime.fromisoformat(
                        str(row.get("target_at_utc") or "").replace("Z", "+00:00")
                    ).astimezone(timezone)
                except ValueError:
                    continue
                if not start <= moment.date() <= end:
                    continue
                key = (platform, str(row.get("publication_id") or ""))
                current = latest.get(key)
                if current is None or str(row.get("target_at_utc")) > str(current.get("target_at_utc")):
                    latest[key] = row

    page_rows = []
    page_path = tenant_dir / "page_metrics_daily.csv"
    if page_path.exists():
        with page_path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                try:
                    day = date.fromisoformat(str(row.get("date") or ""))
                except ValueError:
                    continue
                if start <= day <= end:
                    page_rows.append(row)

    def _total(rows, field):
        return sum(int(float(row.get(field) or 0)) for row in rows)

    facebook_rows = [row for (platform, _), row in latest.items() if platform == "facebook"]
    instagram_rows = [row for (platform, _), row in latest.items() if platform == "instagram"]

    facebook = None
    if facebook_rows or page_rows:
        interactions = _total(page_rows, "page_post_engagements") if page_rows else (
            _total(facebook_rows, "reactions")
            + _total(facebook_rows, "comments")
            + _total(facebook_rows, "shares")
        )
        facebook = {
            "reach": None,
            "impressions": None,
            "interactions": interactions,
            "clicks": _total(facebook_rows, "clicks") if facebook_rows else None,
            "pieces": len(facebook_rows) or None,
            "status": "partial",
            "note": (
                "Ledger local. Meta ya no expone alcance e impresiones orgánicas; "
                "interacciones = actividad de página. "
                + (
                    "Clics = clics en publicaciones."
                    if facebook_rows
                    else "Los clics por publicación aparecen cuando existan capturas E0/E24/E72."
                )
            ),
            "extra": {
                "page_views": _total(page_rows, "page_views_total"),
                "video_views": _total(page_rows, "page_video_views"),
                "reactions": _total(page_rows, "page_actions_post_reactions_total"),
                "new_follows": _total(page_rows, "page_daily_follows"),
            },
        }

    instagram = None
    if instagram_rows:
        likes = _total(instagram_rows, "reactions")
        comments = _total(instagram_rows, "comments")
        instagram = {
            "reach": _total(instagram_rows, "reach") or None,
            "impressions": _total(instagram_rows, "impressions") or None,
            "interactions": likes + comments,
            "clicks": None,
            "pieces": len(instagram_rows),
            "status": "partial",
            "note": (
                "Ledger local. Likes y comentarios públicos; alcance e impresiones "
                "solo si las capturas incluyen insights."
            ),
            "extra": {"likes": likes, "comments": comments},
        }
    return {"facebook_organic": facebook, "instagram_organic": instagram}


def _load_env(root: Path, tenant_id: str) -> Dict[str, str]:
    values: Dict[str, str] = {}
    for path in (root / ".env", root / "tenants" / tenant_id / ".env"):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.replace("export ", "").strip()] = value.strip().strip("'\"")
    return values


def _tenant_config(root: Path, tenant_id: str) -> Dict[str, Any]:
    try:
        payload = json.loads(
            (root / "tenants" / tenant_id / "config.json").read_text(encoding="utf-8")
        )
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _local_timezone(config: Dict[str, Any]) -> ZoneInfo:
    try:
        return ZoneInfo(str(config.get("timezone") or "America/Matamoros"))
    except ZoneInfoNotFoundError:
        return ZoneInfo("UTC")


def _graph_get(token: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    import requests

    request_params = dict(params or {})
    request_params["access_token"] = token
    response = requests.get(
        f"{GRAPH_BASE_URL}/{endpoint.lstrip('/')}", params=request_params, timeout=45
    )
    try:
        payload = response.json()
    except ValueError:
        payload = {"error": {"message": f"HTTP {response.status_code}"}}
    if response.status_code >= 400 or "error" in payload:
        error = payload.get("error") if isinstance(payload, dict) else None
        message = error.get("message") if isinstance(error, dict) else str(error)
        raise RuntimeError(message or f"HTTP {response.status_code}")
    return payload


def _page_token(user_token: str, page_id: str) -> str:
    try:
        payload = _graph_get(user_token, page_id, {"fields": "access_token"})
        return str(payload.get("access_token") or user_token)
    except RuntimeError:
        return user_token


def _post_local_date(post: Dict[str, Any], timezone: ZoneInfo) -> Optional[date]:
    raw = str(post.get("created_time") or post.get("timestamp") or "").strip()
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone(timezone).date()
    except ValueError:
        return None


def _facebook_week_posts(
    page_token: str,
    page_id: str,
    start: date,
    end: date,
    timezone: ZoneInfo,
) -> List[Dict[str, Any]]:
    payload = _graph_get(
        page_token,
        f"{page_id}/posts",
        {
            "fields": "id,created_time,message,permalink_url,reactions.summary(true),comments.summary(true),shares",
            "limit": 100,
        },
    )
    posts = []
    for post in payload.get("data") or []:
        day = _post_local_date(post, timezone)
        if day is not None and start <= day <= end:
            posts.append(post)
    return posts


def _facebook_post_clicks(page_token: str, posts: Sequence[Dict[str, Any]]) -> int:
    total = 0
    for post in posts:
        post_id = str(post.get("id") or "")
        if not post_id:
            continue
        try:
            payload = _graph_get(
                page_token, f"{post_id}/insights", {"metric": "post_clicks", "period": "lifetime"}
            )
        except RuntimeError:
            continue
        for item in payload.get("data") or []:
            for value in item.get("values") or []:
                total += int(value.get("value") or 0)
    return total


def _sum_page_insights(payload: Dict[str, Any]) -> int:
    total = 0
    for item in payload.get("data") or []:
        for value in item.get("values") or []:
            metric_value = value.get("value")
            if isinstance(metric_value, dict):
                metric_value = sum(int(part or 0) for part in metric_value.values())
            total += int(metric_value or 0)
    return total


def _fetch_facebook_organic(
    page_token: str,
    page_id: str,
    start: date,
    end: date,
    timezone: ZoneInfo,
) -> Dict[str, Any]:
    insights = {}
    for metric in FACEBOOK_PAGE_METRICS:
        payload = _graph_get(
            page_token,
            f"{page_id}/insights",
            {
                "metric": metric,
                "period": "day",
                "since": start.isoformat(),
                "until": (end + timedelta(days=1)).isoformat(),
            },
        )
        insights[metric] = _sum_page_insights(payload)
    posts = _facebook_week_posts(page_token, page_id, start, end, timezone)
    clicks = _facebook_post_clicks(page_token, posts)
    return {
        "reach": None,
        "impressions": None,
        "interactions": insights.get("page_post_engagements", 0),
        "clicks": clicks,
        "pieces": len(posts),
        "status": "partial",
        "note": (
            "Meta ya no expone alcance e impresiones orgánicas de Facebook. "
            "Interacciones = actividad de la página; clics = clics en publicaciones."
        ),
        "extra": {
            "page_views": insights.get("page_views_total", 0),
            "video_views": insights.get("page_video_views", 0),
            "reactions": insights.get("page_actions_post_reactions_total", 0),
            "new_follows": insights.get("page_daily_follows", 0),
        },
    }


def _fetch_instagram_organic(
    page_token: str,
    instagram_id: str,
    start: date,
    end: date,
    timezone: ZoneInfo,
) -> Dict[str, Any]:
    payload = _graph_get(
        page_token,
        f"{instagram_id}/media",
        {
            "fields": "id,caption,media_type,like_count,comments_count,timestamp,permalink",
            "limit": 100,
        },
    )
    media = []
    for item in payload.get("data") or []:
        day = _post_local_date(item, timezone)
        if day is not None and start <= day <= end:
            media.append(item)
    likes = sum(int(item.get("like_count") or 0) for item in media)
    comments = sum(int(item.get("comments_count") or 0) for item in media)
    return {
        "reach": None,
        "impressions": None,
        "interactions": likes + comments,
        "clicks": None,
        "pieces": len(media),
        "status": "partial",
        "note": (
            "Alcance e impresiones de Instagram requieren instagram_manage_insights. "
            "Likes y comentarios se leen con los permisos actuales."
        ),
        "extra": {"likes": likes, "comments": comments},
    }


def _messaging_conversations(actions: Sequence[Dict[str, Any]]) -> int:
    totals = {}
    for action in actions or []:
        action_type = str(action.get("action_type") or "")
        try:
            value = int(float(action.get("value") or 0))
        except (TypeError, ValueError):
            value = 0
        for key in (
            "onsite_conversion.messaging_conversation_started_7d",
            "messaging_conversation_started_7d",
            "messaging_conversation_started",
        ):
            if action_type == key or key in action_type:
                totals[key] = totals.get(key, 0) + value
    return (
        totals.get("onsite_conversion.messaging_conversation_started_7d", 0)
        or totals.get("messaging_conversation_started_7d", 0)
        or totals.get("messaging_conversation_started", 0)
    )


def _campaign_ids(tenant_dir: Path) -> set[str]:
    ids = set()
    for path in (tenant_dir / "ads" / "campanas").glob("*/meta_ids.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        campaign_id = str(((payload.get("campaign") or {}).get("id")) or "")
        if campaign_id:
            ids.add(campaign_id)
    return ids


def _fetch_paid_channels(
    user_token: str,
    ad_account_id: str,
    tenant_dir: Path,
    start: date,
    end: date,
) -> Dict[str, Dict[str, Any]]:
    payload = _graph_get(
        user_token,
        f"{ad_account_id}/insights",
        {
            "level": "campaign",
            "fields": "campaign_id,campaign_name,spend,impressions,clicks,reach,actions",
            "time_range": json.dumps({"since": start.isoformat(), "until": end.isoformat()}),
            "breakdowns": "publisher_platform",
            "limit": 500,
        },
    )
    selected_campaigns = _campaign_ids(tenant_dir)
    totals: Dict[str, Dict[str, Any]] = {}
    for row in payload.get("data") or []:
        campaign_id = str(row.get("campaign_id") or "")
        if selected_campaigns and campaign_id not in selected_campaigns:
            continue
        platform = str(row.get("publisher_platform") or "other").lower()
        bucket = totals.setdefault(
            platform,
            {"spend": 0.0, "impressions": 0, "clicks": 0, "reach": 0, "conversations": 0},
        )
        bucket["spend"] += float(row.get("spend") or 0)
        bucket["impressions"] += int(float(row.get("impressions") or 0))
        bucket["clicks"] += int(float(row.get("clicks") or 0))
        bucket["reach"] += int(float(row.get("reach") or 0))
        bucket["conversations"] += _messaging_conversations(row.get("actions") or [])

    result = {}
    for key, platform in (("facebook_paid", "facebook"), ("instagram_paid", "instagram")):
        bucket = totals.get(platform)
        if not bucket:
            result[key] = {
                "status": "unavailable",
                "note": "Sin inversión registrada en la ventana.",
            }
            continue
        spend = round(bucket["spend"], 2)
        conversations = bucket["conversations"]
        result[key] = {
            "reach": bucket["reach"],
            "impressions": bucket["impressions"],
            "clicks": bucket["clicks"],
            "spend": spend,
            "conversations": conversations,
            "cost_per_conversation": round(spend / conversations, 2) if conversations else None,
            "status": "ok",
            "note": "Pauta desglosada por ubicación en Meta.",
        }

    other = {"spend": 0.0, "impressions": 0, "clicks": 0, "reach": 0, "conversations": 0}
    for platform, bucket in totals.items():
        if platform in {"facebook", "instagram"}:
            continue
        for field in other:
            other[field] += bucket[field]
    if other["spend"]:
        other_spend = round(other["spend"], 2)
        result["other_paid"] = {
            "reach": other["reach"],
            "impressions": other["impressions"],
            "clicks": other["clicks"],
            "spend": other_spend,
            "conversations": other["conversations"],
            "cost_per_conversation": (
                round(other_spend / other["conversations"], 2)
                if other["conversations"]
                else None
            ),
            "status": "ok",
            "note": "Espacios de pauta fuera de Facebook e Instagram.",
        }
    return result


def _fetch_meta_week(root: Path, tenant_id: str, start: date, end: date) -> Dict[str, Any]:
    config = _tenant_config(root, tenant_id)
    env = _load_env(root, tenant_id)
    user_token = env.get("META_ACCESS_TOKEN") or env.get("META_PAGE_ACCESS_TOKEN") or ""
    page_id = str((config.get("meta") or {}).get("page_id") or env.get("FB_PAGE_ID") or "")
    instagram_id = str((config.get("meta") or {}).get("ig_user_id") or "")
    ad_account_id = str((config.get("ads") or {}).get("ad_account_id") or "")
    timezone = _local_timezone(config)
    channels = _empty_channels("No se pudo consultar Meta.")
    errors = []
    if not user_token:
        channels = _empty_channels("Falta META_ACCESS_TOKEN.")
    else:
        page_token = _page_token(user_token, page_id) if page_id else user_token
        ledger = _ledger_organic_week(root, tenant_id, start, end, timezone)
        if page_id:
            # El ledger manda cuando ya tiene capturas por publicación. Si solo
            # hay métricas de página, se completa con la consulta a Meta.
            if ledger.get("facebook_organic") and ledger["facebook_organic"].get("pieces") is not None:
                channels["facebook_organic"].update(ledger["facebook_organic"])
            else:
                try:
                    channels["facebook_organic"].update(
                        _fetch_facebook_organic(page_token, page_id, start, end, timezone)
                    )
                except RuntimeError as exc:
                    channels["facebook_organic"]["note"] = f"No disponible: {exc}"
                    errors.append(f"Facebook orgánico: {exc}")
        if instagram_id:
            if ledger.get("instagram_organic"):
                channels["instagram_organic"].update(ledger["instagram_organic"])
            else:
                try:
                    channels["instagram_organic"].update(
                        _fetch_instagram_organic(page_token, instagram_id, start, end, timezone)
                    )
                except RuntimeError as exc:
                    channels["instagram_organic"]["note"] = f"No disponible: {exc}"
                    errors.append(f"Instagram orgánico: {exc}")
        if ad_account_id:
            try:
                channels.update(
                    _fetch_paid_channels(user_token, ad_account_id, root / "tenants" / tenant_id, start, end)
                )
            except RuntimeError as exc:
                for key in ("facebook_paid", "instagram_paid"):
                    channels[key]["note"] = f"No disponible: {exc}"
                errors.append(f"Pauta: {exc}")
    payload = {
        "schema_version": "1.0",
        "tenant_id": tenant_id,
        "period": {"start": start.isoformat(), "end": end.isoformat()},
        "fetched_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "channels": channels,
        "errors": errors,
    }
    path = _meta_week_cache_path(root, tenant_id, start, end)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return _normalize_meta_week(payload)


def _conversations(
    tenant_id: str,
    start: date,
    end: date,
    provider: Optional[ConversationProvider] = None,
) -> Dict[str, Any]:
    if provider is None:
        from modules.communications.whatsapp.conversations import conversation_summary

        provider = conversation_summary
    try:
        payload = provider(tenant_id, limit=1000)
    except Exception as exc:  # noqa: BLE001
        return {"available": False, "error": str(exc), "total": 0, "depth": {}, "per_ad": {}}

    seen = set()
    per_ad: Dict[str, int] = {}
    depth = {"1": 0, "2": 0, "3+": 0}
    for conversation in payload.get("conversations") or []:
        stamp = conversation.get("first_at")
        if not stamp:
            continue
        moment = datetime.fromisoformat(str(stamp).replace("Z", "+00:00")).date()
        if not start <= moment <= end:
            continue
        key = conversation.get("contact") or id(conversation)
        if key in seen:
            continue
        seen.add(key)
        ad_id = str(conversation.get("ad_id") or "") if conversation.get("from_ad") else ""
        if ad_id:
            per_ad[ad_id] = per_ad.get(ad_id, 0) + 1
        value = int(conversation.get("depth") or 0)
        depth["1" if value <= 1 else "2" if value == 2 else "3+"] += 1
    return {"available": True, "total": len(seen), "depth": depth, "per_ad": per_ad}


def build_weekly(
    tenant_id: str,
    reference: Optional[date] = None,
    *,
    base_path: Optional[Path] = None,
    provider: Optional[ConversationProvider] = None,
    meta_metrics: Optional[Dict[str, Any]] = None,
    refresh_meta: bool = False,
) -> Dict[str, Any]:
    root = Path(base_path) if base_path else _project_root()
    tenant_dir = root / "tenants" / tenant_id
    start, end = week_bounds(reference or date.today())
    previous_start = start - timedelta(days=7)
    previous_end = start - timedelta(days=1)

    current = _conversations(tenant_id, start, end, provider)
    previous = _conversations(tenant_id, previous_start, previous_end, provider)
    publications = _load_publications(tenant_dir, start, end)
    actions = _load_actions(tenant_dir, start, end)
    if meta_metrics is not None:
        meta_week = _normalize_meta_week(meta_metrics)
    elif refresh_meta:
        meta_week = _fetch_meta_week(root, tenant_id, start, end)
    else:
        meta_week = _load_meta_week(root, tenant_id, start, end)

    delta = current["total"] - previous["total"]
    return {
        "tenant_id": tenant_id,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "previous_start": previous_start.isoformat(),
        "previous_end": previous_end.isoformat(),
        "conversations": current,
        "previous": previous,
        "delta": delta,
        "delta_pct": (delta / previous["total"] * 100) if previous["total"] else 0,
        "publications": publications,
        "actions": actions,
        "meta": meta_week,
        "channels": meta_week["channels"],
    }


def _piece_title(text: str, limit: int = 88) -> str:
    first_line = next((line.strip() for line in str(text or "").splitlines() if line.strip()), "")
    if " En " in first_line:
        first_line = first_line.split(" En ", 1)[0]
    return _clip(first_line, limit)


def _format_int(value: Any) -> str:
    return f"{int(value):,}" if isinstance(value, (int, float)) else "—"


def _format_money(value: Any) -> str:
    return f"${float(value):,.2f}" if isinstance(value, (int, float)) else "—"


def _format_cost(value: Any) -> str:
    return f"${float(value):,.2f}" if isinstance(value, (int, float)) else "—"


def _paid_totals(data: Dict[str, Any]) -> tuple[Optional[float], int, bool]:
    spend_values = []
    conversations = 0
    for key in ("facebook_paid", "instagram_paid", "other_paid"):
        channel = data.get("channels", {}).get(key) or {}
        if isinstance(channel.get("spend"), (int, float)):
            spend_values.append(float(channel["spend"]))
        if isinstance(channel.get("conversations"), int):
            conversations += channel["conversations"]
    spend = round(sum(spend_values), 2) if spend_values else None
    return spend, conversations, bool(spend_values)


def _channel_rows(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = []
    for key in CHANNEL_ORDER:
        channel = (data.get("channels") or {}).get(key) or {}
        if key == "other_paid" and not isinstance(channel.get("spend"), (int, float)):
            continue
        rows.append(channel)
    return rows


def _learnings(data: Dict[str, Any]) -> List[str]:
    notes: List[str] = []
    total = data["conversations"]["total"]
    depth = data["conversations"].get("depth") or {}
    if total:
        notes.append(
            f"{depth.get('3+', 0)} de {total} conversaciones llegaron a 3 o más mensajes."
        )
    notes.append(f"La semana anterior cerró con {data['previous']['total']} conversaciones.")

    facebook = data.get("channels", {}).get("facebook_paid") or {}
    instagram = data.get("channels", {}).get("instagram_paid") or {}
    facebook_conversations = facebook.get("conversations")
    instagram_conversations = instagram.get("conversations")
    if isinstance(facebook_conversations, int) or isinstance(instagram_conversations, int):
        fb_count = int(facebook_conversations or 0)
        ig_count = int(instagram_conversations or 0)
        paid_total = fb_count + ig_count
        if paid_total:
            notes.append(
                f"Facebook aportó {fb_count} de {paid_total} conversaciones de pauta; "
                f"Instagram aportó {ig_count}."
            )

    organic = data.get("channels", {}).get("facebook_organic") or {}
    if isinstance(organic.get("interactions"), (int, float)):
        notes.append(f"Facebook orgánico registró {int(organic['interactions']):,} interacciones de página.")
    return notes[:4]


def _channel_notes(data: Dict[str, Any]) -> List[str]:
    notes = [
        "«—» significa que Meta no expone esa métrica; no es un cero. "
        "Las métricas orgánicas cubren toda la actividad de la cuenta en la semana, no solo el calendario."
    ]
    seen = set()
    for key in CHANNEL_ORDER:
        channel = (data.get("channels") or {}).get(key) or {}
        note = str(channel.get("note") or "").strip()
        if note and note not in seen and channel.get("status") != "unavailable":
            notes.append(note)
            seen.add(note)
    return notes[:4]


def _organic_activity(data: Dict[str, Any]) -> List[str]:
    """Métricas orgánicas disponibles, para que los guiones no se lean como ceros."""
    facebook = (data.get("channels") or {}).get("facebook_organic") or {}
    instagram = (data.get("channels") or {}).get("instagram_organic") or {}
    lines: List[str] = []
    extra = facebook.get("extra") or {}
    if facebook.get("status") not in (None, "unavailable"):
        parts = []
        if facebook.get("pieces") is not None:
            parts.append(f"{int(facebook.get('pieces') or 0):,} publicaciones")
        for key, label in (
            ("page_views", "vistas de página"),
            ("video_views", "vistas de video"),
            ("reactions", "reacciones"),
            ("new_follows", "seguidores nuevos"),
        ):
            if extra.get(key) is not None:
                parts.append(f"{int(extra[key]):,} {label}")
        if facebook.get("clicks") is not None:
            parts.append(f"{int(facebook['clicks']):,} clics en publicaciones")
        lines.append("Facebook orgánico: " + " · ".join(parts) + ".")
    extra = instagram.get("extra") or {}
    if instagram.get("status") not in (None, "unavailable"):
        parts = [f"{int(instagram.get('pieces') or 0):,} publicaciones"]
        if extra.get("likes") is not None:
            parts.append(f"{int(extra['likes']):,} likes")
        if extra.get("comments") is not None:
            parts.append(f"{int(extra['comments']):,} comentarios")
        lines.append("Instagram orgánico: " + " · ".join(parts) + ".")
    return lines


def _recommendations(data: Dict[str, Any], names: Dict[str, str]) -> List[str]:
    """Máximo tres acciones, derivadas de los datos de la semana."""
    notes: List[str] = []
    total = data["conversations"]["total"]
    depth = data["conversations"].get("depth") or {}
    deep_share = (depth.get("3+", 0) / total * 100) if total else 0
    per_ad = data["conversations"].get("per_ad") or {}

    facebook = data.get("channels", {}).get("facebook_paid") or {}
    instagram = data.get("channels", {}).get("instagram_paid") or {}
    fb_count = int(facebook.get("conversations") or 0)
    ig_count = int(instagram.get("conversations") or 0)
    paid_total = fb_count + ig_count
    if paid_total:
        if fb_count / paid_total >= 0.8:
            notes.append(
                f"Concentrar la pauta en Facebook: aportó {fb_count} de {paid_total} conversaciones de la semana."
            )
        elif ig_count / paid_total >= 0.8:
            notes.append(
                f"Concentrar la pauta en Instagram: aportó {ig_count} de {paid_total} conversaciones de la semana."
            )

    if per_ad:
        ad_id, count = max(per_ad.items(), key=lambda item: item[1])
        notes.append(
            f"Mantener a {names.get(ad_id, ad_id)} como creativo principal: trajo {count} conversaciones."
        )
    if total and deep_share < 40:
        notes.append("Revisar el primer mensaje de bienvenida: menos de 4 de cada 10 conversaciones llegan a 3 mensajes.")
    if data["delta"] < 0:
        notes.append("Comparar la caída contra la semana previa antes de cambiar la segmentación.")
    return notes[:3]


def render_weekly_md(data: Dict[str, Any], names: Dict[str, str]) -> str:
    total = data["conversations"]["total"]
    previous = data["previous"]["total"]
    sign = "+" if data["delta"] >= 0 else ""
    paid_spend, paid_conversations, has_paid = _paid_totals(data)
    lines = [
        f"# Reporte semanal · {data['start']} a {data['end']}",
        "",
        f"**Conversaciones:** {total} ({sign}{data['delta']} vs semana anterior)",
        f"**Piezas en calendario:** {len(data['publications'])}",
        f"**Inversión en pauta:** {_format_money(paid_spend)}",
        f"**Conversaciones de pauta:** {paid_conversations if has_paid else '—'}",
        "",
        "## Resultados por canal",
        "",
        "| Canal | Alcance | Impresiones | Interacciones | Clics | Inversión | Conversaciones | Costo/conv |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for channel in _channel_rows(data):
        lines.append(
            "| {label} | {reach} | {impressions} | {interactions} | {clicks} | {spend} | {conversations} | {cost} |".format(
                label=channel.get("label", ""),
                reach=_format_int(channel.get("reach")),
                impressions=_format_int(channel.get("impressions")),
                interactions=_format_int(channel.get("interactions")),
                clicks=_format_int(channel.get("clicks")),
                spend=_format_money(channel.get("spend")),
                conversations=_format_int(channel.get("conversations")),
                cost=_format_cost(channel.get("cost_per_conversation")),
            )
        )
    channel_notes = _channel_notes(data)
    if channel_notes:
        lines.extend(["", *[f"> {note}" for note in channel_notes]])
    organic_lines = _organic_activity(data)
    if organic_lines:
        lines.extend(["", "### Actividad orgánica", ""])
        lines.extend(f"- {line}" for line in organic_lines)
    lines.extend(
        [
        "",
        "## Qué se hizo",
        "",
        ]
    )
    if data["publications"]:
        lines.extend(
            f"- {item['date']} · {item['platform']} · {_piece_title(item['piece'])}"
            for item in data["publications"]
        )
    else:
        lines.append("- Sin publicaciones registradas.")
    lines.extend(["", "## Lo que aprendimos", ""])
    lines.extend(f"- {note}" for note in _learnings(data))
    lines.extend(["", "## Recomendaciones", ""])
    lines.extend(f"{index}. {note}" for index, note in enumerate(_recommendations(data, names), 1))
    lines.extend(
        [
            "",
            "## Qué necesito de ti",
            "",
            "- Aprobar el plan de la siguiente semana.",
            "- Enviar los assets pendientes antes del miércoles.",
            "",
        ]
    )
    return "\n".join(lines)


def render_weekly_html(data: Dict[str, Any], names: Dict[str, str]) -> str:
    total = data["conversations"]["total"]
    previous = data["previous"]["total"]
    delta = data["delta"]
    sign = "+" if delta >= 0 else ""
    depth = data["conversations"].get("depth") or {}
    recommendations = _recommendations(data, names)
    pieces = data["publications"]
    paid_spend, paid_conversations, has_paid = _paid_totals(data)
    channel_notes = _channel_notes(data)

    rec_items = "\n".join(f"<li>{html.escape(note)}</li>" for note in recommendations)
    learning_items = "\n".join(f"<li>{html.escape(note)}</li>" for note in _learnings(data))
    piece_items = "\n".join(
        f"<li><span>{item['date']}</span> {html.escape(item['platform'])} · {html.escape(_piece_title(item['piece']))}</li>"
        for item in pieces
    ) or "<li>Sin publicaciones registradas.</li>"
    channel_rows = "\n".join(
        "<tr>"
        f"<td class=\"channel\">{html.escape(str(channel.get('label') or ''))}</td>"
        f"<td>{_format_int(channel.get('reach'))}</td>"
        f"<td>{_format_int(channel.get('impressions'))}</td>"
        f"<td>{_format_int(channel.get('interactions'))}</td>"
        f"<td>{_format_int(channel.get('clicks'))}</td>"
        f"<td>{_format_money(channel.get('spend'))}</td>"
        f"<td>{_format_int(channel.get('conversations'))}</td>"
        f"<td>{_format_cost(channel.get('cost_per_conversation'))}</td>"
        "</tr>"
        for channel in _channel_rows(data)
    )
    notes_html = "".join(f"<p class=\"note\">{html.escape(note)}</p>" for note in channel_notes)
    organic_html = "".join(
        f"<p class=\"note\">{html.escape(line)}</p>" for line in _organic_activity(data)
    )

    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Reporte semanal · {data['start']} a {data['end']}</title>
<style>
  @page {{ size: A4; margin: 16mm 15mm; }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; font-family: "DejaVu Sans", "Segoe UI", system-ui, sans-serif;
    color: {INK}; background: {PAPER}; font-size: 10.5pt; line-height: 1.5;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }}
  .sheet {{ max-width: 180mm; margin: 0 auto; }}
  header {{ display: flex; justify-content: space-between; align-items: flex-start;
            border-bottom: 2px solid {INK}; padding-bottom: 8px; }}
  .brand {{ font-family: "DejaVu Serif", Georgia, serif; font-size: 15pt;
            letter-spacing: .18em; text-transform: uppercase; }}
  .brand span {{ color: {ORANGE}; }}
  .meta {{ text-align: right; font-size: 8.5pt; color: {MUTED}; line-height: 1.7; }}
  .hero {{ display: grid; grid-template-columns: 1.15fr .85fr; gap: 10mm;
           padding: 12mm 0 10mm; align-items: end; }}
  .hero h1 {{ font-family: "DejaVu Serif", Georgia, serif; font-size: 25pt;
              font-weight: normal; line-height: 1.15; margin: 0 0 6px; }}
  .hero p {{ margin: 0; color: {MUTED}; max-width: 36ch; }}
  .figure {{ border-left: 3px solid {ORANGE}; padding-left: 6mm; }}
  .figure .n {{ font-family: "DejaVu Serif", Georgia, serif; font-size: 52pt;
                line-height: .95; color: {ORANGE}; }}
  .figure .l {{ font-size: 9pt; color: {MUTED}; }}
  .delta {{ font-size: 9pt; color: {DEEP}; margin-top: 2mm; }}
  .kpis {{ display: grid; grid-template-columns: repeat(4, 1fr);
           border-top: 1px solid {RULE}; border-bottom: 1px solid {RULE}; }}
  .kpi {{ padding: 4mm 0 4mm 4mm; border-left: 1px solid {RULE}; }}
  .kpi:first-child {{ border-left: 0; padding-left: 0; }}
  .kpi .v {{ font-family: "DejaVu Serif", Georgia, serif; font-size: 16pt; }}
  .kpi .k {{ font-size: 8.3pt; color: {MUTED}; }}
  section {{ padding-top: 6mm; }}
  h2 {{ font-family: "DejaVu Serif", Georgia, serif; font-size: 13pt; font-weight: normal;
        margin: 0 0 4mm; padding-bottom: 2mm; border-bottom: 1px solid {RULE}; }}
  ul {{ margin: 0; padding-left: 5mm; }}
  li {{ margin-bottom: 2.5mm; }}
  li span {{ color: {MUTED}; font-size: 8.6pt; margin-right: 3mm; }}
  .two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 9mm; }}
  table.metrics {{ width: 100%; border-collapse: collapse; font-size: 7.8pt; }}
  table.metrics th {{ color: {MUTED}; font-size: 7.4pt; font-weight: normal;
                      text-align: right; padding: 1.8mm 1.2mm; border-bottom: 1px solid {RULE}; }}
  table.metrics td {{ text-align: right; padding: 2mm 1.2mm; border-bottom: 1px solid {RULE}; }}
  table.metrics th:first-child, table.metrics td.channel {{ text-align: left; padding-left: 0; }}
  table.metrics td.channel {{ font-weight: 600; }}
  .note {{ color: {MUTED}; font-size: 7.4pt; line-height: 1.35; margin: 1.5mm 0 0; }}
  .callout {{ background: {GOLD}; border-left: 3px solid {ORANGE}; padding: 4mm 5mm; }}
  .callout p {{ margin: 0; }}
  footer {{ margin-top: 12mm; padding-top: 3mm; border-top: 1px solid {RULE};
            display: flex; justify-content: space-between; font-size: 8pt; color: {MUTED}; }}
</style>
</head>
<body>
<div class="sheet">
  <header>
    <div class="brand">Flexi<span>.</span></div>
    <div class="meta">
      Reporte semanal<br>
      {data['start']} — {data['end']}
    </div>
  </header>

  <div class="hero">
    <div>
      <h1>La semana en<br>conversaciones</h1>
      <p>Lo que pasó, lo que aprendimos y lo que sigue. Una página, sin ruido.</p>
    </div>
    <div class="figure">
      <div class="n">{total}</div>
      <div class="l">personas escribieron</div>
      <div class="delta">{sign}{delta} vs. semana anterior ({previous})</div>
    </div>
  </div>

  <div class="kpis">
    <div class="kpi"><div class="v">{len(pieces)}</div><div class="k">piezas en calendario</div></div>
    <div class="kpi"><div class="v">{depth.get('3+', 0)}</div><div class="k">conversaciones de 3+ mensajes</div></div>
    <div class="kpi"><div class="v">{_format_money(paid_spend)}</div><div class="k">inversión en pauta</div></div>
    <div class="kpi"><div class="v">{previous}</div><div class="k">conversaciones la semana previa</div></div>
  </div>

  <section>
    <h2>Resultados por canal</h2>
    <table class="metrics">
      <thead>
        <tr><th>Canal</th><th>Alcance</th><th>Impresiones</th><th>Interacciones</th><th>Clics</th><th>Inversión</th><th>Conversaciones</th><th>Costo/conv</th></tr>
      </thead>
      <tbody>{channel_rows}</tbody>
    </table>
    {notes_html}
    {organic_html}
  </section>

  <section class="two">
    <div>
      <h2>Qué se hizo</h2>
      <ul>{piece_items}</ul>
    </div>
    <div>
      <h2>Lo que aprendimos</h2>
      <ul>{learning_items}</ul>
    </div>
  </section>

  <section>
    <h2>Recomendaciones</h2>
    <ul>{rec_items}</ul>
  </section>

  <section>
    <h2>Qué necesito de ti</h2>
    <div class="callout">
      <p>Aprobar el plan de la siguiente semana y enviar los assets pendientes antes del miércoles.</p>
    </div>
  </section>

  <footer>
    <span>Flexi · Piedras Negras</span>
    <span>Generado el {date.today().isoformat()}</span>
  </footer>
</div>
</body>
</html>
"""


def write_weekly(data: Dict[str, Any], base_path: Optional[Path] = None) -> tuple[Path, Path]:
    root = Path(base_path) if base_path else _project_root()
    directory = root / "tenants" / data["tenant_id"] / "reports" / "semanal"
    directory.mkdir(parents=True, exist_ok=True)
    slug = f"{data['start']}_{data['end']}"
    names = _tenant_ad_names(root / "tenants" / data["tenant_id"])
    md_path = directory / f"reporte_semanal_{slug}.md"
    html_path = directory / f"reporte_semanal_{slug}.html"
    md_path.write_text(render_weekly_md(data, names), encoding="utf-8")
    html_path.write_text(render_weekly_html(data, names), encoding="utf-8")
    return md_path, html_path


def _tenant_ad_names(tenant_dir: Path) -> Dict[str, str]:
    for path in sorted((tenant_dir / "ads" / "campanas").glob("*/meta_ids.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        return {
            str(ad.get("id")): str(ad.get("name") or ad.get("id")).split(" - ")[0]
            for ad in payload.get("ads") or []
            if ad.get("id")
        }
    return {}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Reporte semanal para cliente")
    parser.add_argument("--tenant", required=True)
    parser.add_argument("--reference", help="fecha de referencia YYYY-MM-DD")
    parser.add_argument(
        "--refresh-meta",
        action="store_true",
        help="consulta Meta y actualiza el cache semanal de métricas",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    reference = date.fromisoformat(args.reference) if args.reference else None
    data = build_weekly(args.tenant, reference, refresh_meta=args.refresh_meta)
    md_path, html_path = write_weekly(data)
    if args.json:
        print(json.dumps({"md": str(md_path), "html": str(html_path)}, ensure_ascii=False))
    else:
        print(f"md:   {md_path}")
        print(f"html: {html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
