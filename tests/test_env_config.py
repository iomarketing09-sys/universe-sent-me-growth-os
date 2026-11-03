"""Pruebas del resolvedor central de entorno Meta."""

from __future__ import annotations

import os
from pathlib import Path

from modules.communications.comments.facebook import load_environment
from modules.config.env import META_ENV_KEYS, load_env_values
from modules.social.meta_publisher import load_integration_env


def test_env_precedence_and_no_mutation(tmp_path, monkeypatch):
    root_env = tmp_path / ".env"
    tenant_env = tmp_path / "tenants" / "universe" / ".env"
    tenant_env.parent.mkdir(parents=True)
    root_env.write_text(
        "FB_PAGE_ID=root-page\nMETA_ACCESS_TOKEN=root-token\n",
        encoding="utf-8",
    )
    tenant_env.write_text(
        "FB_PAGE_ID=tenant-page\nMETA_ACCESS_TOKEN=tenant-token\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("META_ACCESS_TOKEN", "process-token")
    before = dict(os.environ)

    values = load_env_values(
        (root_env, tenant_env),
        environ=os.environ,
        keys=META_ENV_KEYS,
    )

    assert values["FB_PAGE_ID"] == "tenant-page"
    assert values["META_ACCESS_TOKEN"] == "process-token"
    assert dict(os.environ) == before


def test_env_expands_references_without_mutating_process(tmp_path):
    root_env = tmp_path / ".env"
    root_env.write_text(
        "FB_PAGE_ID=page-1\nMETA_PAGE_ID=${FB_PAGE_ID}\n",
        encoding="utf-8",
    )
    before = dict(os.environ)

    values = load_env_values((root_env,), environ={}, keys=META_ENV_KEYS)

    assert values["META_PAGE_ID"] == "page-1"
    assert dict(os.environ) == before


def test_comment_environment_loader_does_not_mutate_process(tmp_path, monkeypatch):
    root_env = tmp_path / ".env"
    root_env.write_text("FB_PAGE_ID=comment-page\n", encoding="utf-8")
    monkeypatch.delenv("FB_PAGE_ID", raising=False)
    before = dict(os.environ)

    values = load_environment(tmp_path, "universe")

    assert values["FB_PAGE_ID"] == "comment-page"
    assert dict(os.environ) == before


def test_meta_publisher_environment_loader_does_not_mutate_process(
    tmp_path, monkeypatch
):
    root_env = tmp_path / ".env"
    root_env.write_text("FB_PAGE_ID=publisher-page\n", encoding="utf-8")
    monkeypatch.delenv("FB_PAGE_ID", raising=False)
    before = dict(os.environ)

    values = load_integration_env(str(tmp_path))

    assert values["FB_PAGE_ID"] == "publisher-page"
    assert dict(os.environ) == before
