"""Streamlit-specific error handling utilities."""

import functools
import traceback
from typing import Callable, Any, Optional

import streamlit as st

from email_templates_gen.config import ConfigurationError
from email_templates_gen.utils.error_handler import (
    OpenAIError,
    OutlookIntegrationError, 
    SharePointIntegrationError,
    APIError,
    EmailTemplateError,
)
from email_templates_gen.utils.logging_config import get_logger


def handle_streamlit_errors(func: Callable) -> Callable:
    """Decorator for handling errors in Streamlit pages with user-friendly messages.
    
    Args:
        func: The Streamlit page function to wrap
        
    Returns:
        Wrapped function with error handling
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger = get_logger("streamlit_errors")
        
        try:
            return func(*args, **kwargs)
        except ConfigurationError as e:
            logger.error("Configuration error in Streamlit", error=str(e))
            st.error("⚙️ Configuration Error")
            st.markdown(f"**Problem:** {str(e)}")
            st.info("💡 **Solution:** Check your `.env` file and ensure all required environment variables are set. See `.env.example` for reference.")
            with st.expander("Need Help?"):
                st.markdown("""
                1. Copy `.env.example` to `.env`
                2. Fill in your API keys and configuration
                3. Restart the application
                """)
            
        except OpenAIError as e:
            logger.error("OpenAI API error in Streamlit", error=str(e), status_code=e.status_code)
            st.error("🤖 AI Service Error")
            st.markdown("**Problem:** Unable to generate content using AI service.")
            
            if e.status_code == 401:
                st.warning("Your OpenAI API key appears to be invalid.")
                st.info("💡 **Solution:** Check your `OPENAI_API_KEY` in the `.env` file.")
            elif e.status_code == 429:
                st.warning("Rate limit exceeded or quota reached.")
                st.info("💡 **Solution:** Please wait a moment and try again, or check your OpenAI account limits.")
            else:
                st.info("💡 **Solution:** Please try again in a few moments. If the problem persists, check the OpenAI service status.")
                
        except OutlookIntegrationError as e:
            logger.error("Outlook integration error in Streamlit", error=str(e), status_code=e.status_code)
            st.error("📧 Email Service Error")
            st.markdown("**Problem:** Unable to connect to Outlook/Microsoft Graph.")
            st.info("💡 **Solution:** Check your Outlook integration settings in the `.env` file (client ID, tenant ID, client secret).")
            with st.expander("Troubleshooting"):
                st.markdown("""
                1. Verify your Azure AD application is properly configured
                2. Check that all Outlook environment variables are set
                3. Ensure your application has the necessary permissions
                """)
                
        except SharePointIntegrationError as e:
            logger.error("SharePoint integration error in Streamlit", error=str(e))
            st.error("📁 SharePoint Integration Error")
            st.markdown("**Problem:** Unable to connect to SharePoint.")
            st.info("💡 **Solution:** Check your SharePoint configuration in the `.env` file.")
            
        except APIError as e:
            logger.error("General API error in Streamlit", error=str(e), service=e.service)
            st.error(f"🔌 {e.service} Service Error")
            st.markdown(f"**Problem:** Unable to connect to {e.service} service.")
            st.info("💡 **Solution:** Please try again in a few moments. If the problem persists, check your internet connection and service configuration.")
            
        except EmailTemplateError as e:
            logger.error("Email template error in Streamlit", error=str(e))
            st.error("⚠️ Application Error")
            st.markdown(f"**Problem:** {str(e)}")
            st.info("💡 **Solution:** Please try again or contact support if the problem persists.")
            
        except Exception as e:
            logger.error("Unexpected error in Streamlit", error=str(e), error_type=type(e).__name__, exc_info=True)
            st.error("❌ Unexpected Error")
            st.markdown("**Problem:** An unexpected error occurred.")
            st.info("💡 **Solution:** Please try again. If the problem persists, please report this issue.")
            
            # Show technical details in debug mode
            if st.session_state.get("debug_mode", False):
                with st.expander("Technical Details (Debug Mode)"):
                    st.code(f"Error Type: {type(e).__name__}")
                    st.code(f"Error Message: {str(e)}")
                    st.code(f"Traceback:\n{traceback.format_exc()}")
    
    return wrapper


def show_error_help() -> None:
    """Display a help section for common errors."""
    with st.sidebar:
        st.markdown("---")
        st.subheader("❓ Having Issues?")
        
        if st.button("🔧 Check Configuration"):
            from email_templates_gen.config import get_configuration_health
            health = get_configuration_health()
            
            if health["status"] == "healthy":
                st.success("✅ Configuration looks good!")
            else:
                st.error("❌ Configuration issues found:")
                for issue in health["issues"]:
                    st.write(f"• {issue}")
        
        st.markdown("""
        **Common Solutions:**
        - Check your `.env` file exists
        - Verify all API keys are valid
        - Ensure internet connection
        - Try refreshing the page
        """)


def enable_debug_mode() -> None:
    """Enable debug mode for enhanced error reporting."""
    if "debug_mode" not in st.session_state:
        st.session_state.debug_mode = False
    
    with st.sidebar:
        st.session_state.debug_mode = st.checkbox(
            "🐛 Debug Mode", 
            value=st.session_state.debug_mode,
            help="Show detailed error information"
        )
