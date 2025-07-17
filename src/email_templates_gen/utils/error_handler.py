"""Custom exception classes and error handlers."""

from __future__ import annotations

from typing import Optional, Dict, Any


class EmailTemplateError(Exception):
    """Base exception for EmailTemplatesGen."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ConfigurationError(EmailTemplateError):
    """Raised when configuration is invalid or missing."""
    pass


class APIError(EmailTemplateError):
    """Base class for external API errors."""
    
    def __init__(
        self,
        service: str,
        message: str,
        status_code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, details)
        self.service = service
        self.status_code = status_code


class OpenAIError(APIError):
    """Raised when OpenAI API calls fail."""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__("OpenAI", message, status_code, details)


class OutlookIntegrationError(APIError):
    """Raised when Outlook/Microsoft Graph API calls fail."""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__("Outlook", message, status_code, details)


class SharePointIntegrationError(APIError):
    """Raised when SharePoint API calls fail."""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__("SharePoint", message, status_code, details)


class DataProcessingError(EmailTemplateError):
    """Raised when data processing operations fail."""
    pass


class TemplateGenerationError(EmailTemplateError):
    """Raised when email template generation fails."""
    pass


class ValidationError(EmailTemplateError):
    """Raised when data validation fails."""
    pass
