"""Utility modules."""

from email_templates_gen.utils.logging_config import setup_logging, get_logger
from email_templates_gen.utils.error_handler import (
    EmailTemplateError,
    ConfigurationError,
    APIError,
    OpenAIError,
    OutlookIntegrationError,
    SharePointIntegrationError,
)
from email_templates_gen.utils.decorators import (
    log_function_call,
    log_api_call,
    handle_errors,
    retry_on_failure,
)

__all__ = [
    "setup_logging",
    "get_logger", 
    "EmailTemplateError",
    "ConfigurationError",
    "APIError",
    "OpenAIError",
    "OutlookIntegrationError",
    "SharePointIntegrationError",
    "log_function_call",
    "log_api_call", 
    "handle_errors",
    "retry_on_failure",
]
