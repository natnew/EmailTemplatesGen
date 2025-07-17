"""Main Streamlit application entry point."""

import os
import sys
from pathlib import Path

import streamlit as st

# Add src to path for development
src_path = Path(__file__).parent / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

try:
    from email_templates_gen.config import (
        get_settings,
        validate_environment_setup,
        ConfigurationError,
        get_configuration_health,
    )
    from email_templates_gen.utils import setup_logging, get_logger
    
    # Try to initialize configuration
    try:
        validate_environment_setup()
        settings = get_settings()
        setup_logging(settings.log_level, settings.debug)
        logger = get_logger("app")
        logger.info("Application starting with new configuration system")
    except ConfigurationError:
        # Fallback to original behavior if configuration is not set up
        pass
    
except ImportError:
    # Configuration system not available, continue with original app
    pass

# Redirect to the Workflow page by default
st.switch_page("pages/1_Workflow.py")
