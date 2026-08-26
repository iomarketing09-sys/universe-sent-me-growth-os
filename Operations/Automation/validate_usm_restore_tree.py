#!/usr/bin/env python3
"""Validate the required logical roots of an historical USM restoration without reading live sources."""

from __future__ import annotations

import os
import stat
import sys
from pathlib import Path


class ValidationError(Exception):
    """Raised when a required restored root is absent or has an unsupported entry."""


def validate_tree(root: Path, logical_name: str) -> None:
    if not root.is_dir():
        raise ValidationError(f"required_root_absent:{logical_name}")

    for item in [root, *sorted(root.rglob("*"), key=lambda value: value.relative_to(root).as_posix())]:
        item_stat = item.lstat()
        if stat.S_ISDIR(item_stat.st_mode) or stat.S_ISREG(item_stat.st_mode):
            continue
        if stat.S_ISLNK(item_stat.st_mode):
            os.readlink(item)
            continue
        raise ValidationError(f"unsupported_entry_type:{logical_name}")


def main() -> int:
    if len(sys.argv) != 2:
        print("USAGE: validate_usm_restore_tree.py RESTORE_ROOT", file=sys.stderr)
        return 2

    restored_root = Path(sys.argv[1])
    required_roots = [
        ("repository", restored_root / "universe-sent-me-growth-os"),
        ("bin", restored_root / "bin"),
        ("metrics_config", restored_root / ".config" / "usm-metrics"),
        ("metrics_data", restored_root / ".local" / "share" / "usm-metrics"),
        ("omniroute", restored_root / "omniroute-pilot"),
    ]

    try:
        for logical_name, root in required_roots:
            validate_tree(root, logical_name)
    except ValidationError as error:
        print(f"ERROR={error}", file=sys.stderr)
        return 1

    print("STATUS=restored_required_roots_structure_validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
