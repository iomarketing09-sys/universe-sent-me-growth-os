import csv
import json
import sys
from pathlib import Path


COMMENTS_DIR = (
    Path(__file__).resolve().parents[1]
    / "tenants"
    / "universe"
    / "comment_responses"
    / "facebook_comments"
)
sys.path.insert(0, str(COMMENTS_DIR))

from modules.communications.comments import facebook as comments_main
from comment_log import (
    COMMENT_LOG_FIELDS,
    LEGACY_FIELDS,
    merge_approval_payload,
    migrate_comment_log,
    normalize_comment_row,
    read_comment_log,
)


def test_normalize_legacy_nine_column_row():
    row = [
        "comment_123",
        "¿Precio?",
        "True",
        "True",
        "",
        "question",
        "review",
        "Te compartimos la información por mensaje.",
        "2026-10-30T10:00:00+0000",
    ]

    normalized = normalize_comment_row(row)

    assert normalized["comment_id"] == "comment_123"
    assert normalized["comment_text"] == "¿Precio?"
    assert normalized["decision"] == "review"
    assert normalized["response_text"] == "Te compartimos la información por mensaje."
    assert normalized["created_time"] == "2026-10-30T10:00:00+0000"
    assert normalized["publish_status"] == ""
    assert set(normalized) == set(COMMENT_LOG_FIELDS)


def test_migrate_mixed_log_preserves_rows(tmp_path):
    log_path = tmp_path / "comments_log.csv"
    with log_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(LEGACY_FIELDS)
        writer.writerow(
            [
                "2026-09-11T02:44:35+00:00",
                "comment_1",
                "Comentario viejo",
                "user_1",
                "2026-09-10T11:00:00+0000",
                "True",
                "True",
                "Respuesta vieja",
                "question",
                "Intención",
                "question_about_content",
                "respond",
                "low",
                "",
                "",
            ]
        )
        writer.writerow(
            [
                "comment_2",
                "Comentario de nueve columnas",
                "True",
                "False",
                "",
                "other",
                "no_response",
                "",
                "2026-09-12T00:00:00+0000",
            ]
        )

    result = migrate_comment_log(log_path)
    rows = read_comment_log(log_path)

    assert result.changed
    assert result.rows == 2
    assert result.legacy_rows == 2
    assert rows[0]["response_text"] == "Respuesta vieja"
    assert rows[1]["comment_id"] == "comment_2"
    assert rows[1]["decision"] == "no_response"
    with log_path.open("r", encoding="utf-8", newline="") as handle:
        assert next(csv.reader(handle)) == COMMENT_LOG_FIELDS


def test_merge_approvals_preserves_approved_items():
    existing = {
        "approvals": [
            {
                "comment_id": "existing_1",
                "approved": True,
                "approved_response": "Respuesta aprobada",
            }
        ]
    }
    generated = [
        {
            "comment_id": "new_2",
            "approved": False,
            "approved_response": "Propuesta nueva",
        }
    ]

    merged = merge_approval_payload(existing, generated, generated_at="2026-10-31T00:00:00+00:00")

    assert [item["comment_id"] for item in merged["approvals"]] == ["existing_1", "new_2"]
    assert merged["approvals"][0]["approved"] is True
    assert merged["total_pending"] == 2


def test_merge_approvals_drops_stale_blank_items():
    existing = {
        "approvals": [
            {
                "comment_id": "stale_blank",
                "approved": False,
                "approved_response": None,
            },
            {
                "comment_id": "stale_edited",
                "approved": False,
                "approved_response": "Texto editado por el usuario",
            },
        ]
    }

    merged = merge_approval_payload(existing, [])

    assert [item["comment_id"] for item in merged["approvals"]] == ["stale_edited"]


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self.payload = payload
        self.status_code = status_code

    def json(self):
        return self.payload


def test_publish_approved_marks_reply_and_skips_second_run(tmp_path, monkeypatch):
    approval_path = tmp_path / "aprobaciones.json"
    log_path = tmp_path / "comments_log.csv"
    approval_path.write_text(
        json.dumps(
            {
                "approvals": [
                    {
                        "comment_id": "comment_123",
                        "comment_text": "Comentario original",
                        "character": "Universe",
                        "approved": True,
                        "approved_response": "Respuesta aprobada",
                    }
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    calls = []

    def fake_post(url, data=None, files=None, timeout=None):
        calls.append({"url": url, "data": data, "files": files})
        return FakeResponse({"id": "reply_999"})

    monkeypatch.setenv("PAGE_ACCESS_TOKEN", "test-token")
    monkeypatch.setenv("FB_PAGE_ID", "page_1")
    monkeypatch.setattr(comments_main, "_existing_page_reply", lambda *args: (True, None, ""))
    monkeypatch.setattr("requests.post", fake_post)

    assert comments_main.publish_approved(str(approval_path), str(log_path)) == 0
    saved = json.loads(approval_path.read_text(encoding="utf-8"))
    published = saved["approvals"][0]
    assert published["published"] is True
    assert published["reply_id"] == "reply_999"
    assert len(calls) == 1

    assert comments_main.publish_approved(str(approval_path), str(log_path)) == 0
    assert len(calls) == 1
    rows = read_comment_log(log_path)
    assert rows[-1]["reply_id"] == "reply_999"
    assert rows[-1]["publish_status"] == "published"


def test_publish_approved_skips_reply_found_in_meta(tmp_path, monkeypatch):
    approval_path = tmp_path / "aprobaciones.json"
    log_path = tmp_path / "comments_log.csv"
    approval_path.write_text(
        json.dumps(
            {
                "approvals": [
                    {
                        "comment_id": "comment_456",
                        "approved": True,
                        "approved_response": "Respuesta aprobada",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("PAGE_ACCESS_TOKEN", "test-token")
    monkeypatch.setattr(
        comments_main,
        "_existing_page_reply",
        lambda *args: (True, {"id": "reply_existing", "created_time": "2026-10-30T10:00:00+0000"}, ""),
    )
    monkeypatch.setattr("requests.post", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("no debe publicar")))

    assert comments_main.publish_approved(str(approval_path), str(log_path)) == 0
    saved = json.loads(approval_path.read_text(encoding="utf-8"))
    assert saved["approvals"][0]["reply_id"] == "reply_existing"
    assert read_comment_log(log_path)[-1]["publish_status"] == "already_published"
