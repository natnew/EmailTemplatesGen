import os
import sys
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import email_generator.sharepoint_integration as sp


@pytest.fixture
def tmp_txt(tmp_path):
    path = tmp_path / "demo.txt"
    path.write_text("hello")
    return path


def test_upload_template(monkeypatch, tmp_txt):
    fake_ctx = MagicMock()
    fake_ctx.with_credentials.return_value = fake_ctx
    fake_folder = MagicMock()
    fake_file = MagicMock(serverRelativeUrl="/docs/demo.txt")
    fake_folder.upload_file.return_value = fake_file
    fake_ctx.web.get_folder_by_server_relative_url.return_value = fake_folder

    monkeypatch.setattr(sp, "ClientContext", MagicMock(return_value=fake_ctx))
    monkeypatch.setattr(sp, "UserCredential", MagicMock())

    url = sp.upload_template(
        "https://example.sharepoint.com", "Shared", tmp_txt, "u", "p"
    )

    assert url == "/docs/demo.txt"
    fake_ctx.execute_query.assert_called_once()


def test_download_template(monkeypatch, tmp_path):
    fake_ctx = MagicMock()
    fake_ctx.with_credentials.return_value = fake_ctx
    fake_file = MagicMock()
    fake_file.download.return_value = fake_file
    fake_ctx.web.get_file_by_server_relative_url.return_value = fake_file

    monkeypatch.setattr(sp, "ClientContext", MagicMock(return_value=fake_ctx))
    monkeypatch.setattr(sp, "UserCredential", MagicMock())

    dest = tmp_path / "out.txt"
    result = sp.download_template(
        "https://example.sharepoint.com", "/docs/demo.txt", dest, "u", "p"
    )

    assert result == dest
    fake_file.download.assert_called_with(dest.as_posix())
    fake_file.execute_query.assert_called_once()
