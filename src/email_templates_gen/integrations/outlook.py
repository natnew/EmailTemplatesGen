"""Outlook helpers using Microsoft Graph."""
from __future__ import annotations

import os
from typing import Optional

import msal
import requests

GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0"
SCOPES = ["https://graph.microsoft.com/.default"]

CLIENT_ID = os.getenv("OUTLOOK_CLIENT_ID")
TENANT_ID = os.getenv("OUTLOOK_TENANT_ID")
CLIENT_SECRET = os.getenv("OUTLOOK_CLIENT_SECRET")
SENDER_ADDRESS = os.getenv("OUTLOOK_SENDER")
AUTHORITY_TEMPLATE = "https://login.microsoftonline.com/{tenant_id}"


def get_access_token(
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    tenant_id: Optional[str] = None,
) -> str:
    """Return an access token for Microsoft Graph."""
    client_id = client_id or CLIENT_ID
    tenant_id = tenant_id or TENANT_ID
    client_secret = client_secret or CLIENT_SECRET

    if not all([client_id, tenant_id, client_secret]):
        raise ValueError("Client ID, tenant ID and client secret are required")

    app = msal.ConfidentialClientApplication(
        client_id,
        authority=AUTHORITY_TEMPLATE.format(tenant_id=tenant_id),
        client_credential=client_secret,
    )

    result = app.acquire_token_silent(SCOPES, account=None)
    if not result:
        result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        error = result.get("error_description", "Unknown error")
        raise RuntimeError(f"Failed to obtain access token: {error}")
    return result["access_token"]


def send_email(
    recipient: str,
    subject: str,
    body: str,
    *,
    sender: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    tenant_id: Optional[str] = None,
) -> None:
    """Send an HTML email via Microsoft Graph."""
    sender = sender or SENDER_ADDRESS
    if not sender:
        raise ValueError("Sender email address must be provided")

    token = get_access_token(
        client_id=client_id, client_secret=client_secret, tenant_id=tenant_id
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    message = {
        "message": {
            "subject": subject,
            "body": {"contentType": "HTML", "content": body},
            "toRecipients": [{"emailAddress": {"address": recipient}}],
        },
        "saveToSentItems": "true",
    }
    endpoint = f"{GRAPH_ENDPOINT}/users/{sender}/sendMail"
    response = requests.post(endpoint, headers=headers, json=message, timeout=10)
    response.raise_for_status()
