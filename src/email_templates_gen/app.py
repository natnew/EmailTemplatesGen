"""Main Streamlit application entry point."""

import os
import sys
from pathlib import Path

import streamlit as st

# Add src to path for development
src_path = Path(__file__).parent.parent.parent / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

from email_templates_gen.config import (
    get_settings,
    validate_environment_setup,
    ConfigurationError,
    get_configuration_health,
)
from email_templates_gen.utils import setup_logging, get_logger
from email_templates_gen.utils.streamlit_error_handler import (
    handle_streamlit_errors,
    show_error_help,
    enable_debug_mode,
)


@handle_streamlit_errors
def initialize_application():
    """Initialize the application with configuration and logging."""
    # Try to validate environment setup
    try:
        validate_environment_setup()
        settings = get_settings()
        
        # Setup logging
        setup_logging(settings.log_level, settings.debug)
        logger = get_logger("app")
        logger.info("Application starting", environment=settings.environment)
        
        # Configure Streamlit
        st.set_page_config(
            page_title="EmailTemplatesGen",
            page_icon="📧",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        
        return True, None
        
    except ConfigurationError as e:
        # Show configuration error page
        st.set_page_config(
            page_title="Configuration Required",
            page_icon="⚙️",
            layout="wide",
        )
        return False, str(e)


def show_configuration_setup_page(error_message: str):
    """Show configuration setup page when environment is not properly configured."""
    st.title("⚙️ Configuration Required")
    st.error(f"Configuration Error: {error_message}")
    
    st.markdown("""
    ## 🚀 Quick Setup Guide
    
    To get started with EmailTemplatesGen, you need to configure your environment:
    
    ### 1. Create Environment File
    Copy the example environment file and customize it:
    """)
    
    if st.button("📋 Copy .env.example to .env"):
        try:
            import shutil
            shutil.copy(".env.example", ".env")
            st.success("✅ Created .env file! Now edit it with your configuration.")
        except Exception as e:
            st.error(f"Failed to copy file: {e}")
    
    st.markdown("""
    ### 2. Required Configuration
    
    Edit your `.env` file and set these required values:
    
    **OpenAI API:**
    - `OPENAI_API_KEY`: Your OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
    
    **Microsoft Outlook Integration:**
    - `OUTLOOK_CLIENT_ID`: Azure AD application client ID
    - `OUTLOOK_TENANT_ID`: Azure AD tenant ID  
    - `OUTLOOK_CLIENT_SECRET`: Azure AD application client secret
    - `OUTLOOK_SENDER_ADDRESS`: Your email address
    
    ### 3. Azure AD Setup (for Outlook)
    
    1. Go to [Azure Portal](https://portal.azure.com)
    2. Navigate to "Azure Active Directory" > "App registrations"
    3. Create a new application or use an existing one
    4. Note the Client ID and Tenant ID
    5. Create a client secret in "Certificates & secrets"
    6. Add Microsoft Graph permissions: `Mail.Send`, `User.Read`
    """)
    
    # Show current configuration health
    st.markdown("### 🔍 Configuration Status")
    health = get_configuration_health()
    
    if health["status"] == "healthy":
        st.success("✅ Configuration is healthy!")
        if st.button("🔄 Restart Application"):
            st.rerun()
    else:
        st.error("❌ Configuration issues found:")
        for issue in health["issues"]:
            st.write(f"• {issue}")
    
    # Show environment variables status
    with st.expander("🔧 Environment Variables Status"):
        env_vars = health.get("environment_variables", {})
        for var, is_set in env_vars.items():
            status = "✅ Set" if is_set else "❌ Missing"
            st.write(f"**{var}**: {status}")


def main():
    """Main application entry point."""
    # Initialize application
    initialized, error = initialize_application()
    
    if not initialized:
        show_configuration_setup_page(error)
        return
    
    # Add debug mode toggle
    enable_debug_mode()
    
    # Add error help to sidebar
    show_error_help()
    
    # Application is properly configured, redirect to workflow page
    logger = get_logger("app")
    logger.info("Application initialized successfully, redirecting to workflow")
    
    # Import and run the workflow page
    try:
        # For now, redirect to the original pages structure until we complete the migration
        st.switch_page("pages/1_Workflow.py")
    except Exception as e:
        logger.error("Failed to load workflow page", error=str(e))
        st.error("Failed to load the main application. Please check your installation.")
        st.info("Try running the application from the original app.py file.")


if __name__ == "__main__":
    main()
