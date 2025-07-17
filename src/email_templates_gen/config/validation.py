"""Configuration validation utilities."""

from __future__ import annotations

import os
from typing import List, Tuple

from email_templates_gen.config.settings import AppSettings


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing."""
    pass


def validate_configuration(settings: AppSettings) -> List[str]:
    """Validate configuration settings and return list of issues.
    
    Returns:
        List of validation error messages. Empty list if all valid.
    """
    issues = []
    
    # Validate OpenAI settings
    if not settings.openai.api_key:
        issues.append("OpenAI API key is required (OPENAI_API_KEY)")
    
    if not settings.openai.model:
        issues.append("OpenAI model is required (OPENAI_MODEL)")
    
    # Validate Outlook settings
    required_outlook = [
        ("client_id", "OUTLOOK_CLIENT_ID"),
        ("tenant_id", "OUTLOOK_TENANT_ID"), 
        ("client_secret", "OUTLOOK_CLIENT_SECRET"),
        ("sender_address", "OUTLOOK_SENDER_ADDRESS"),
    ]
    
    for attr, env_var in required_outlook:
        if not getattr(settings.outlook, attr):
            issues.append(f"Outlook {attr} is required ({env_var})")
    
    # Validate email format
    if settings.outlook.sender_address and "@" not in settings.outlook.sender_address:
        issues.append("Outlook sender address must be a valid email")
    
    # Validate log level
    try:
        import logging
        getattr(logging, settings.log_level)
    except AttributeError:
        issues.append(f"Invalid log level: {settings.log_level}")
    
    return issues


def check_required_environment_variables() -> List[Tuple[str, str]]:
    """Check if required environment variables are set.
    
    Returns:
        List of (variable_name, description) tuples for missing variables.
    """
    required_vars = [
        ("OPENAI_API_KEY", "OpenAI API key for AI model access"),
        ("OUTLOOK_CLIENT_ID", "Azure AD application client ID"),
        ("OUTLOOK_TENANT_ID", "Azure AD tenant ID"),
        ("OUTLOOK_CLIENT_SECRET", "Azure AD application client secret"),
        ("OUTLOOK_SENDER_ADDRESS", "Default email sender address"),
    ]
    
    missing = []
    for var_name, description in required_vars:
        if not os.getenv(var_name):
            missing.append((var_name, description))
    
    return missing


def validate_environment_setup() -> None:
    """Validate that the environment is properly configured.
    
    Raises:
        ConfigurationError: If configuration is invalid or incomplete.
    """
    # Check for .env file
    env_file_path = ".env"
    if not os.path.exists(env_file_path):
        raise ConfigurationError(
            f"Environment file {env_file_path} not found. "
            "Copy .env.example to .env and fill in your configuration."
        )
    
    # Check required environment variables
    missing_vars = check_required_environment_variables()
    if missing_vars:
        var_list = "\n".join([f"  - {var}: {desc}" for var, desc in missing_vars])
        raise ConfigurationError(
            f"Missing required environment variables:\n{var_list}\n\n"
            "Please set these variables in your .env file."
        )
    
    # Validate settings
    try:
        settings = AppSettings()
        issues = validate_configuration(settings)
        if issues:
            issue_list = "\n".join([f"  - {issue}" for issue in issues])
            raise ConfigurationError(
                f"Configuration validation failed:\n{issue_list}"
            )
    except Exception as e:
        if isinstance(e, ConfigurationError):
            raise
        raise ConfigurationError(f"Failed to load configuration: {e}")


def get_configuration_health() -> dict:
    """Get the health status of configuration.
    
    Returns:
        Dictionary with configuration health information.
    """
    health = {
        "status": "healthy",
        "issues": [],
        "environment_variables": {},
        "settings_loaded": False,
    }
    
    try:
        # Check environment variables
        missing_vars = check_required_environment_variables()
        if missing_vars:
            health["status"] = "unhealthy"
            health["issues"].extend([f"Missing {var}" for var, _ in missing_vars])
        
        # Try to load settings
        settings = AppSettings()
        health["settings_loaded"] = True
        
        # Validate configuration
        validation_issues = validate_configuration(settings)
        if validation_issues:
            health["status"] = "unhealthy"
            health["issues"].extend(validation_issues)
        
        # Record which environment variables are set (without values)
        env_vars = [
            "OPENAI_API_KEY", "OUTLOOK_CLIENT_ID", "OUTLOOK_TENANT_ID",
            "OUTLOOK_CLIENT_SECRET", "OUTLOOK_SENDER_ADDRESS"
        ]
        for var in env_vars:
            health["environment_variables"][var] = bool(os.getenv(var))
            
    except Exception as e:
        health["status"] = "unhealthy"
        health["issues"].append(f"Configuration error: {e}")
    
    return health
