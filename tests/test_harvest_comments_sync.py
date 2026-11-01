"""Tests de la sincronización local -> Google Drive del harvest."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path


def _load_harvest_module():
    path = Path(__file__).resolve().parents[1] / "tenants" / "universe" / "harvest_comments.py"
    spec = importlib.util.spec_from_file_location("harvest_comments_sync_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_sync_approval_files_copia_colas_y_respeta_la_mas_reciente(tmp_path):
    module = _load_harvest_module()
    local = tmp_path / "local"
    drive = tmp_path / "drive"
    local.mkdir()
    drive.mkdir()

    master = local / "aprobaciones.json"
    batch = local / "aprobaciones_nuevas_8.json"
    master.write_text("master-local", encoding="utf-8")
    batch.write_text("batch-local", encoding="utf-8")

    drive_master = drive / "aprobaciones.json"
    drive_master.write_text("master-drive-mas-nueva", encoding="utf-8")
    os.utime(master, (100, 100))
    os.utime(drive_master, (200, 200))

    synced = module.sync_approval_files(local, drive)

    assert drive_master.read_text(encoding="utf-8") == "master-drive-mas-nueva"
    assert (drive / "aprobaciones_nuevas_8.json").read_text(encoding="utf-8") == "batch-local"
    assert drive / "aprobaciones_nuevas_8.json" in synced
    assert drive_master not in synced


def test_sync_approval_files_sobrescribe_si_la_local_es_mas_nueva(tmp_path):
    module = _load_harvest_module()
    local = tmp_path / "local"
    drive = tmp_path / "drive"
    local.mkdir()
    drive.mkdir()

    master = local / "aprobaciones.json"
    master.write_text("master-local-nueva", encoding="utf-8")
    drive_master = drive / "aprobaciones.json"
    drive_master.write_text("master-drive-vieja", encoding="utf-8")
    os.utime(drive_master, (100, 100))
    os.utime(master, (200, 200))

    synced = module.sync_approval_files(local, drive)

    assert drive_master.read_text(encoding="utf-8") == "master-local-nueva"
    assert drive_master in synced
