"""Estado persistente de intentos de publicación de Social.

Cada slot de Instagram tiene una clave idempotente y un registro local con
intentos, backoff y estado terminal. El estado vive por tenant para que un
fallo de un cliente no contamine a los demás.
"""

from __future__ import annotations

import json
import logging
import os
import re
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

STATE_VERSION = 1

STATUS_PENDING = "pending"
STATUS_RETRY = "retry"
STATUS_PUBLISHED = "published"
STATUS_DEAD = "dead"
STATUS_BLOCKED = "blocked"

TERMINAL_STATUSES = {STATUS_PUBLISHED, STATUS_DEAD, STATUS_BLOCKED}

DEFAULT_MAX_ATTEMPTS = 5
DEFAULT_BASE_DELAY_SECONDS = 900
DEFAULT_MAX_DELAY_SECONDS = 24 * 60 * 60


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds")


def _parse_iso(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def redact_error(message: Any) -> str:
    """Quita tokens de un error antes de persistirlo o mostrarlo."""
    text = str(message or "")
    text = re.sub(r"(access_token=)[^&\s]+", r"\1<redacted>", text, flags=re.I)
    text = re.sub(r"(Bearer\s+)[A-Za-z0-9._-]+", r"\1<redacted>", text, flags=re.I)
    return text[:1000]


def job_key(tenant_id: str, item: Any, platform: str = "Instagram") -> str:
    """Clave estable para un slot. No incluye el caption."""
    return "|".join(
        [
            str(platform).strip().lower(),
            str(tenant_id).strip(),
            str(getattr(item, "date_str", "")).strip(),
            str(getattr(item, "time_str", "")).strip(),
            str(getattr(item, "media_filename", "")).strip(),
        ]
    )


@dataclass
class PublishJob:
    key: str
    tenant_id: str
    platform: str
    date: str
    time: str
    asset_filename: str
    status: str = STATUS_PENDING
    attempts: int = 0
    first_seen_at: str = ""
    last_attempt_at: Optional[str] = None
    next_attempt_at: Optional[str] = None
    last_error: Optional[str] = None
    publication_id: Optional[str] = None
    dead_lettered_at: Optional[str] = None
    released_at: Optional[str] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "PublishJob":
        allowed = {field.name for field in cls.__dataclass_fields__.values()}
        return cls(**{key: value for key, value in payload.items() if key in allowed})

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @property
    def is_terminal(self) -> bool:
        return self.status in TERMINAL_STATUSES


class PublishJobStore:
    """Store JSON por tenant, con escritura atómica y dead-letter append-only."""

    def __init__(
        self,
        base_path: Path,
        tenant_id: str,
        *,
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
        base_delay_seconds: int = DEFAULT_BASE_DELAY_SECONDS,
        max_delay_seconds: int = DEFAULT_MAX_DELAY_SECONDS,
        clock: Callable[[], datetime] = utc_now,
    ):
        if max_attempts < 1:
            raise ValueError("max_attempts debe ser mayor que cero")
        if base_delay_seconds < 0 or max_delay_seconds < 0:
            raise ValueError("los delays no pueden ser negativos")

        self.base_path = Path(base_path)
        self.tenant_id = tenant_id
        self.max_attempts = max_attempts
        self.base_delay_seconds = base_delay_seconds
        self.max_delay_seconds = max_delay_seconds
        self.clock = clock
        state_dir = self.base_path / "tenants" / tenant_id / "data" / "social"
        self.path = state_dir / "publish_state.json"
        self.dead_letter_path = state_dir / "dead_letter.jsonl"

    def _empty_payload(self) -> Dict[str, Any]:
        return {
            "version": STATE_VERSION,
            "tenant_id": self.tenant_id,
            "updated_at": _iso(self.clock()),
            "jobs": {},
        }

    def _load(self) -> Dict[str, Any]:
        if not self.path.is_file():
            return self._empty_payload()
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            logger.warning("[%s] Estado de publicación ilegible: %s", self.tenant_id, exc)
            return self._empty_payload()
        if not isinstance(payload, dict) or not isinstance(payload.get("jobs"), dict):
            logger.warning("[%s] Estado de publicación con formato inválido", self.tenant_id)
            return self._empty_payload()
        return payload

    def _save(self, payload: Dict[str, Any]) -> None:
        payload["version"] = STATE_VERSION
        payload["tenant_id"] = self.tenant_id
        payload["updated_at"] = _iso(self.clock())
        self.path.parent.mkdir(parents=True, exist_ok=True)
        handle = tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=self.path.parent,
            prefix=f".{self.path.name}.",
            suffix=".tmp",
            delete=False,
        )
        temp_path = Path(handle.name)
        try:
            with handle:
                json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_path, self.path)
        finally:
            temp_path.unlink(missing_ok=True)

    def _get(self, key: str) -> Optional[PublishJob]:
        raw = self._load()["jobs"].get(key)
        return PublishJob.from_dict(raw) if isinstance(raw, dict) else None

    def _upsert(self, job: PublishJob) -> None:
        payload = self._load()
        payload["jobs"][job.key] = job.to_dict()
        self._save(payload)

    def get(self, key: str) -> Optional[PublishJob]:
        return self._get(key)

    def is_due(self, key: str, now: Optional[datetime] = None) -> bool:
        job = self._get(key)
        if job is None:
            return True
        if job.is_terminal:
            return False
        next_attempt = _parse_iso(job.next_attempt_at)
        return next_attempt is None or next_attempt <= (now or self.clock())

    def _new_job(self, key: str, item: Any) -> PublishJob:
        return PublishJob(
            key=key,
            tenant_id=self.tenant_id,
            platform="Instagram",
            date=str(getattr(item, "date_str", "")),
            time=str(getattr(item, "time_str", "")),
            asset_filename=str(getattr(item, "media_filename", "")),
            first_seen_at=_iso(self.clock()),
        )

    def record_success(
        self,
        key: str,
        item: Any,
        publication_id: str,
        now: Optional[datetime] = None,
    ) -> PublishJob:
        moment = now or self.clock()
        job = self._get(key) or self._new_job(key, item)
        job.status = STATUS_PUBLISHED
        job.attempts += 1
        job.last_attempt_at = _iso(moment)
        job.next_attempt_at = None
        job.last_error = None
        job.publication_id = publication_id
        self._upsert(job)
        return job

    def record_failure(
        self,
        key: str,
        item: Any,
        error: Any,
        now: Optional[datetime] = None,
    ) -> PublishJob:
        moment = now or self.clock()
        job = self._get(key) or self._new_job(key, item)
        job.attempts += 1
        job.last_attempt_at = _iso(moment)
        job.last_error = redact_error(error)

        if job.attempts >= self.max_attempts:
            job.status = STATUS_DEAD
            job.next_attempt_at = None
            job.dead_lettered_at = _iso(moment)
        else:
            job.status = STATUS_RETRY
            delay = min(
                self.max_delay_seconds,
                self.base_delay_seconds * (2 ** (job.attempts - 1)),
            )
            job.next_attempt_at = _iso(moment + timedelta(seconds=delay))

        self._upsert(job)
        if job.status == STATUS_DEAD:
            self._append_dead_letter(job)
        return job

    def mark_blocked(
        self,
        key: str,
        item: Any,
        reason: Any,
        now: Optional[datetime] = None,
    ) -> PublishJob:
        moment = now or self.clock()
        job = self._get(key) or self._new_job(key, item)
        job.status = STATUS_BLOCKED
        job.last_attempt_at = _iso(moment)
        job.next_attempt_at = None
        job.last_error = redact_error(reason)
        self._upsert(job)
        return job

    def _append_dead_letter(self, job: PublishJob) -> None:
        self.dead_letter_path.parent.mkdir(parents=True, exist_ok=True)
        with self.dead_letter_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(job.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")

    def dead_letters(self) -> List[PublishJob]:
        jobs = self._load()["jobs"].values()
        return [
            PublishJob.from_dict(job)
            for job in jobs
            if isinstance(job, dict) and job.get("status") == STATUS_DEAD
        ]

    def release(self, key: str, statuses=(STATUS_DEAD, STATUS_BLOCKED)) -> Optional[PublishJob]:
        """Devuelve un job terminal a la cola tras una corrección humana."""
        job = self._get(key)
        if job is None or job.status not in set(statuses):
            return None
        job.status = STATUS_RETRY
        job.attempts = 0
        job.next_attempt_at = None
        job.dead_lettered_at = None
        job.released_at = _iso(self.clock())
        self._upsert(job)
        return job

    def release_all(self, statuses=(STATUS_DEAD, STATUS_BLOCKED)) -> int:
        released = 0
        for raw in list(self._load()["jobs"].values()):
            if not isinstance(raw, dict):
                continue
            if raw.get("status") in set(statuses):
                if self.release(str(raw.get("key")), statuses=statuses):
                    released += 1
        return released

    def summary(self) -> Dict[str, int]:
        summary = {
            STATUS_PENDING: 0,
            STATUS_RETRY: 0,
            STATUS_PUBLISHED: 0,
            STATUS_DEAD: 0,
            STATUS_BLOCKED: 0,
        }
        for raw in self._load()["jobs"].values():
            if not isinstance(raw, dict):
                continue
            status = str(raw.get("status") or STATUS_PENDING)
            summary[status] = summary.get(status, 0) + 1
        return summary


def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Inspecciona y libera el estado de Social")
    parser.add_argument("--tenant", required=True)
    parser.add_argument("--base-path", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--release-dead", action="store_true")
    parser.add_argument("--release-blocked", action="store_true")
    parser.add_argument("--release-key")
    args = parser.parse_args(argv)

    store = PublishJobStore(Path(args.base_path), args.tenant)
    changed = 0
    if args.release_key:
        changed = int(store.release(args.release_key) is not None)
    if args.release_dead:
        changed += store.release_all(statuses=(STATUS_DEAD,))
    if args.release_blocked:
        changed += store.release_all(statuses=(STATUS_BLOCKED,))

    payload = {
        "tenant": args.tenant,
        "summary": store.summary(),
        "dead_letters": [job.to_dict() for job in store.dead_letters()],
        "released": changed,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"[{args.tenant}] {payload['summary']} released={changed}")
        for job in payload["dead_letters"]:
            print(f"  dead: {job['key']} attempts={job['attempts']} error={job['last_error']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
