"""Tests del harvest sin sincronización automática a Google Drive."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_harvest_module():
    path = Path(__file__).resolve().parents[1] / "tenants" / "universe" / "harvest_comments.py"
    spec = importlib.util.spec_from_file_location("harvest_comments_sync_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, path


def test_harvest_ya_no_expone_copia_a_drive():
    module, path = _load_harvest_module()

    assert not hasattr(module, "sync_approval_files")
    assert not hasattr(module, "DRIVE_CANDIDATES")
    source = path.read_text(encoding="utf-8")
    assert "GoogleDrive" not in source
    assert "shutil.copy2" not in source


def test_harvest_termina_sin_escribir_fuera_de_la_cola_local(tmp_path, monkeypatch, capsys):
    module, _ = _load_harvest_module()
    tenant_dir = tmp_path / "universe"
    comm_dir = tenant_dir / "comment_responses" / "facebook_comments"
    comm_dir.mkdir(parents=True)
    approvals = comm_dir / "aprobaciones.json"
    approvals.write_text('{"approvals": []}', encoding="utf-8")
    (comm_dir / "main.py").write_text(
        "import sys\n"
        "print('Total comentarios: 0')\n"
        "print('Descartados: 0')\n"
        "sys.exit(0)\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(module, "TENANT_DIR", tenant_dir)
    monkeypatch.setattr(module, "COMM_DIR", comm_dir)
    monkeypatch.setattr(module, "APROBACIONES_LOCAL", approvals)
    monkeypatch.setattr(module, "check_omniroute", lambda: False)

    code = module.main(["--hours", "1", "--max-comments", "1"])
    output = capsys.readouterr().out

    assert code == 0
    assert "RECOLECCIÓN COMPLETADA" in output
    assert sorted(path.name for path in tmp_path.iterdir()) == ["universe"]
