"""Utilities for uploading and downloading templates from SharePoint."""

from __future__ import annotations

import os
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential


def connect(site_url: str, client_id: str, client_secret: str) -> ClientContext:
    creds = ClientCredential(client_id, client_secret)
    return ClientContext(site_url).with_credentials(creds)


def upload_file(ctx: ClientContext, library_url: str, file_path: str) -> str:
    with open(file_path, "rb") as f:
        name = os.path.basename(file_path)
        target_folder = ctx.web.get_folder_by_server_relative_url(library_url)
        target_file = target_folder.upload_file(name, f.read()).execute_query()
    return target_file.serverRelativeUrl


def download_file(ctx: ClientContext, file_url: str, local_path: str) -> None:
    with open(local_path, "wb") as out_file:
        ctx.web.get_file_by_server_relative_url(file_url).download(out_file).execute_query()

