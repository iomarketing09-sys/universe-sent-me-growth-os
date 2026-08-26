#!/usr/bin/env python3
"""Run an isolated, synthetic-only in-memory Headroom compression benchmark.

This benchmark is intentionally not part of the USM metrics pipeline. It uses
only fictional JSON in memory, blocks socket creation, disables the Kompress
ML model, starts no proxy, and confines Headroom's unavoidable CCR cache to a
TemporaryDirectory that is verified as removed. It never enables memory,
learning, wrappers, shared context, OmniRoute, secrets, accounts, or real
metrics.
"""

from __future__ import annotations

import json
import os
import socket
import tempfile
from pathlib import Path
from unittest.mock import patch


def block_network(*_args, **_kwargs):
    raise AssertionError("Synthetic Headroom benchmark must not open a network socket.")


def synthetic_payload() -> str:
    rows = [
        {
            "synthetic_record": number,
            "fictional_series": "aurora_archive",
            "synthetic_counter": number % 5,
            "synthetic_label": "fictitious context compression sample",
            "availability": "synthetic_available",
        }
        for number in range(1, 181)
    ]
    return json.dumps({"synthetic": True, "records": rows}, ensure_ascii=False)


def main() -> int:
    from headroom import CompressConfig, compress

    root_removed = False
    benchmark_summary: dict[str, object] = {}
    with tempfile.TemporaryDirectory(prefix="usm-headroom-synthetic-") as temp_dir:
        root = Path(temp_dir)
        old_environment = {
            key: os.environ.get(key)
            for key in ("HOME", "XDG_CACHE_HOME", "XDG_CONFIG_HOME", "XDG_DATA_HOME", "TMPDIR")
        }
        os.environ.update(
            {
                "HOME": str(root),
                "XDG_CACHE_HOME": str(root / "cache"),
                "XDG_CONFIG_HOME": str(root / "config"),
                "XDG_DATA_HOME": str(root / "data"),
                "TMPDIR": str(root / "tmp"),
            }
        )
        try:
            messages = [
                {"role": "system", "content": "Synthetic benchmark only. Do not use external information."},
                {
                    "role": "user",
                    "content": "Compress this completely fictional JSON sample in memory only.\n" + synthetic_payload(),
                },
            ]
            config = CompressConfig(
                compress_user_messages=True,
                compress_system_messages=False,
                protect_recent=0,
                protect_analysis_context=False,
                min_tokens_to_compress=1,
                kompress_model="disabled",
            )
            with patch.object(socket, "socket", side_effect=block_network):
                result = compress(messages, model="synthetic-local-benchmark", config=config)

            created_files = sorted(
                str(path.relative_to(root))
                for path in root.rglob("*")
                if path.is_file()
            )
            allowed_ccr_files = {
                ".headroom/ccr_store.db",
                ".headroom/ccr_store.db-shm",
                ".headroom/ccr_store.db-wal",
            }
            assert set(created_files).issubset(allowed_ccr_files), created_files
            assert result.tokens_after <= result.tokens_before, result
            benchmark_summary = {
                "status": "headroom_synthetic_benchmark_passed",
                "tokens_before": result.tokens_before,
                "tokens_after": result.tokens_after,
                "tokens_saved": result.tokens_saved,
                "compression_ratio": round(result.compression_ratio, 6),
                "transforms_applied": result.transforms_applied,
                "temporary_ccr_file_count": len(created_files),
                "guarantees": [
                    "fictional_in_memory_input",
                    "network_socket_blocked",
                    "kompress_ml_disabled",
                    "no_proxy",
                    "ccr_confined_to_temporary_directory",
                    "no_memory",
                    "no_learning",
                    "no_shared_context",
                    "no_omniroute",
                    "temporary_home",
                ],
            }
        finally:
            for key, value in old_environment.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value
    root_removed = not root.exists()
    assert root_removed, "The temporary benchmark directory must be removed."
    benchmark_summary["temporary_directory_removed"] = root_removed
    print(json.dumps(benchmark_summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
