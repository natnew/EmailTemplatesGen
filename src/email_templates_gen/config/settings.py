"""Configuration management using Pydantic settings."""

from __future__ import annotations

import os
from typing import Optional

from pydantic import BaseSettings, Field, validator


class OpenAISettings(BaseSettings):
    """OpenAI API configuration."""
    
    api_key: str = Field(..., description="OpenAI API key")
    model: str = Field(default="gpt-4", description="Default OpenAI model")
    max_tokens: int = Field(default=2000, description="Maximum tokens per request")
    temperature: float = Field(default=0.7, description="Temperature for generation")
    
    class Config:
        env_prefix = "OPENAI_"
        env_file = ".env"


class OutlookSettings(BaseSettings):
    """Microsoft Outlook/Graph API configuration."""
    
    client_id: str = Field(..., description="Azure AD application client ID")
    tenant_id: str = Field(..., description="Azure AD tenant ID")
    client_secret: str = Field(..., description="Azure AD application client secret")
    sender_address: str = Field(..., description="Default sender email address")
    
    class Config:
        env_prefix = "OUTLOOK_"
        env_file = ".env"


class SharePointSettings(BaseSettings):
    """SharePoint configuration."""
    
    site_url: Optional[str] = Field(None, description="SharePoint site URL")
    username: Optional[str] = Field(None, description="SharePoint username")
    password: Optional[str] = Field(None, description="SharePoint password")
    folder_url: Optional[str] = Field(None, description="Default SharePoint folder")
    
    class Config:
        env_prefix = "SHAREPOINT_"
        env_file = ".env"


class AppSettings(BaseSettings):
    """Main application configuration."""
    
    # Application settings
    debug: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    environment: str = Field(default="development", description="Environment name")
    
    # Service settings
    openai: OpenAISettings = Field(default_factory=OpenAISettings)
    outlook: OutlookSettings = Field(default_factory=OutlookSettings)
    sharepoint: SharePointSettings = Field(default_factory=SharePointSettings)
    
    # Streamlit settings
    streamlit_server_port: int = Field(default=8501, description="Streamlit server port")
    streamlit_theme: str = Field(default="light", description="Streamlit theme")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate log level is one of the standard levels."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return v.upper()
    
    @validator("environment")
    def validate_environment(cls, v):
        """Validate environment is a known environment."""
        valid_envs = ["development", "staging", "production"]
        if v.lower() not in valid_envs:
            raise ValueError(f"environment must be one of {valid_envs}")
        return v.lower()


# Global settings instance
_settings: Optional[AppSettings] = None


def get_settings() -> AppSettings:
    """Get the global settings instance, creating it if necessary."""
    global _settings
    if _settings is None:
        _settings = AppSettings()
    return _settings


def reload_settings() -> AppSettings:
    """Reload settings from environment/files."""
    global _settings
    _settings = AppSettings()
    return _settings
