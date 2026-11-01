"""Compatibilidad del log canónico de comentarios."""

from modules.communications.comments.log import (
    COMMENT_LOG_FIELDS,
    LEGACY_FIELDS,
    LEGACY_NINE_COLUMN_FIELDS,
    LogMigration,
    append_comment_log,
    merge_approval_payload,
    migrate_comment_log,
    normalize_comment_row,
    read_comment_log,
    write_comment_log,
    write_json_atomic,
)

__all__ = [
    "COMMENT_LOG_FIELDS",
    "LEGACY_FIELDS",
    "LEGACY_NINE_COLUMN_FIELDS",
    "LogMigration",
    "append_comment_log",
    "merge_approval_payload",
    "migrate_comment_log",
    "normalize_comment_row",
    "read_comment_log",
    "write_comment_log",
    "write_json_atomic",
]
