
"""Basic Outlook integration via Microsoft Graph API."""

from __future__ import annotations

import requests
import msal

GRAPH_SCOPE = ["https://graph.microsoft.com/.default"]
GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0"


def get_access_token(client_id: str, client_secret: str, tenant_id: str) -> str:
    """Acquire an app-only access token for Microsoft Graph."""
    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
    )
    result = app.acquire_token_for_client(scopes=GRAPH_SCOPE)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description", "No token received"))

"""Utility functions for sending email via Microsoft Graph."""

from __future__ import annotations

import os
from typing import Optional

import msal
import requests


CLIENT_ID = os.getenv("OUTLOOK_CLIENT_ID")
TENANT_ID = os.getenv("OUTLOOK_TENANT_ID")
CLIENT_SECRET = os.getenv("OUTLOOK_CLIENT_SECRET")
SENDER_ADDRESS = os.getenv("OUTLOOK_SENDER")

AUTHORITY_TEMPLATE = "https://login.microsoftonline.com/{tenant_id}"
SCOPES = ["https://graph.microsoft.com/.default"]


def get_access_token(
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    tenant_id: Optional[str] = None,
) -> str:
    """Acquire an access token for the Microsoft Graph API using client credentials."""

    client_id = client_id or CLIENT_ID
    tenant_id = tenant_id or TENANT_ID
    client_secret = client_secret or CLIENT_SECRET

    if not all([client_id, tenant_id, client_secret]):
        raise ValueError("Client ID, tenant ID, and client secret are required")

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

    token: str,
    from_user: str,
    recipient: str,
    subject: str,
    body_html: str,
) -> None:
    """Send an email using Graph API.

    Parameters
    ----------
    token:
        OAuth access token.
    from_user:
        User ID or email address of the sending account.
    recipient:
        Email address of the recipient.
    subject:
        Subject line of the message.
    body_html:
        HTML body of the email.
    """
    url = f"{GRAPH_ENDPOINT}/users/{from_user}/sendMail"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "message": {
            "subject": subject,
            "body": {"contentType": "HTML", "content": body_html},

    recipient: str,
    subject: str,
    body: str,
    *,
    sender: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    tenant_id: Optional[str] = None,
) -> None:
    """Send an email via Microsoft Graph.

    Parameters
    ----------
    recipient:
        Email address to send to.
    subject:
        Email subject line.
    body:
        HTML body content.
    sender:
        The address of the sending account. Defaults to ``OUTLOOK_SENDER`` env.
    client_id, client_secret, tenant_id:
        Optional credentials overriding environment variables.
    """

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

    response = requests.post(url, headers=headers, json=payload, timeout=10)


    endpoint = f"https://graph.microsoft.com/v1.0/users/{sender}/sendMail"
    response = requests.post(endpoint, headers=headers, json=message, timeout=10)

    response.raise_for_status()

