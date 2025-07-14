# Outlook Integration

This project can send emails using Microsoft Graph. Set the following environment variables so the helper functions can authenticate without prompting:

- `OUTLOOK_CLIENT_ID`
- `OUTLOOK_TENANT_ID`
- `OUTLOOK_CLIENT_SECRET`
- `OUTLOOK_SENDER` (the sending account)

Example usage:

```python
from email_generator.outlook_integration import send_email

send_email("recipient@example.com", "Subject", "<p>Hello</p>")
```
