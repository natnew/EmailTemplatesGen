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
            "toRecipients": [{"emailAddress": {"address": recipient}}],
        },
        "saveToSentItems": "true",
    }
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    response.raise_for_status()

