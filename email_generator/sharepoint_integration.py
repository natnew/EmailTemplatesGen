"""Utilities for interacting with SharePoint to manage email templates."""
from __future__ import annotations

from pathlib import Path

try:
    from office365.sharepoint.client_context import ClientContext
    from office365.runtime.auth.user_credential import UserCredential
except Exception:  # pragma: no cover - library not installed in test env
    ClientContext = None  # type: ignore
    UserCredential = None  # type: ignore


def _require_office365() -> None:
    if ClientContext is None or UserCredential is None:
        raise ImportError(
            "Office365-REST-Python-Client is required for SharePoint integration"
        )


def upload_template(
    site_url: str,
    folder_url: str,
    template_path: Path | str,
    username: str,
    password: str,
) -> str:
    """Upload a template file to SharePoint and return its server-relative URL."""
    _require_office365()
    path = Path(template_path)
    ctx = ClientContext(site_url).with_credentials(UserCredential(username, password))
    target_folder = ctx.web.get_folder_by_server_relative_url(folder_url)
    with path.open("rb") as f:
        uploaded_file = target_folder.upload_file(path.name, f.read())
    ctx.execute_query()
    return uploaded_file.serverRelativeUrl


def download_template(
    site_url: str,
    file_url: str,
    destination_path: Path | str,
    username: str,
    password: str,
) -> Path:
    """Download a template from SharePoint to the local filesystem."""
    _require_office365()
    dest = Path(destination_path)
    ctx = ClientContext(site_url).with_credentials(UserCredential(username, password))
    sharepoint_file = ctx.web.get_file_by_server_relative_url(file_url)
    sharepoint_file.download(dest.as_posix()).execute_query()
    return dest
