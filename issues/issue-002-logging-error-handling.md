# Issue #2: Implement Comprehensive Logging and Error Handling Framework

## 🔴 Priority: Critical

## Problem Statement

The EmailTemplatesGen project currently lacks a structured logging system and consistent error handling patterns. This creates significant challenges:

- **No observability**: Impossible to debug issues in production
- **Poor user experience**: Generic error messages that don't help users
- **Lost debugging information**: No trace of API calls, failures, or performance issues
- **Inconsistent error handling**: Each module handles errors differently
- **No monitoring**: No visibility into API usage, rate limits, or system health
- **Security concerns**: No audit trail for sensitive operations

## Current Issues in Codebase

### Files with Logging/Error Problems:
- `email_generator/generator.py` - No error handling for OpenAI API failures
- `email_generator/outlook_integration.py` - Basic error handling, no logging
- `learnbot/rag_pipeline.py` - No logging of document processing or failures
- `pages/3_Play.py` - No error tracking for user interactions
- All Streamlit pages - Generic error handling with poor UX

### Examples of Current Problems:
```python
# email_generator/generator.py - No error handling
def stream_generated_email(input_text, tone, purpose, openai_api_key):
    client = OpenAI(api_key=openai_api_key)
    # What happens if API key is invalid?
    # What happens if rate limit is hit?
    # What happens if API is down?
    response = client.chat.completions.create(...)
```

```python
# email_generator/outlook_integration.py - Basic error handling
def send_email(recipient: str, subject: str, body: str) -> bool:
    try:
        # ... API call
        return True
    except Exception as e:
        # No logging, generic error handling
        return False
```

## Acceptance Criteria

### ✅ Structured Logging Framework
- [ ] Implement centralized logging configuration using Python's logging module
- [ ] Create structured log format with timestamps, levels, and context
- [ ] Add request/response logging for all external API calls
- [ ] Implement log rotation and retention policies
- [ ] Add performance metrics logging (response times, token usage)

### ✅ Comprehensive Error Handling
- [ ] Create custom exception classes for different error types
- [ ] Implement consistent error handling patterns across all modules
- [ ] Add error recovery mechanisms where appropriate
- [ ] Create error correlation IDs for tracking related issues

### ✅ User Experience Improvements
- [ ] Implement user-friendly error messages in Streamlit UI
- [ ] Add progress indicators for long-running operations
- [ ] Create error reporting mechanism for users
- [ ] Add graceful degradation for service failures

### ✅ Monitoring and Observability
- [ ] Add health check endpoints/functions
- [ ] Implement API usage tracking and rate limit monitoring
- [ ] Create system performance metrics
- [ ] Add audit logging for sensitive operations

### ✅ Development and Debugging
- [ ] Add debug mode with enhanced logging
- [ ] Create logging decorators for function entry/exit
- [ ] Implement configuration-based log level management
- [ ] Add development-friendly error pages

## Implementation Plan

### Phase 1: Logging Infrastructure
1. **Create logging configuration**
   ```
   utils/
   ├── __init__.py
   ├── logging_config.py    # Centralized logging setup
   ├── error_handler.py     # Custom exceptions and handlers
   ├── decorators.py        # Logging and error decorators
   └── monitoring.py        # Performance and health monitoring
   ```

2. **Add logging dependencies**
   ```bash
   pip install structlog python-json-logger
   ```

### Phase 2: Custom Exception Classes
```python
# utils/error_handler.py
class EmailTemplateError(Exception):
    """Base exception for EmailTemplatesGen"""
    pass

class ConfigurationError(EmailTemplateError):
    """Raised when configuration is invalid"""
    pass

class APIError(EmailTemplateError):
    """Raised when external API calls fail"""
    def __init__(self, service: str, message: str, status_code: int = None):
        self.service = service
        self.status_code = status_code
        super().__init__(f"{service} API Error: {message}")

class OutlookIntegrationError(APIError):
    """Raised when Outlook/Microsoft Graph API fails"""
    pass

class OpenAIError(APIError):
    """Raised when OpenAI API fails"""
    pass
```

### Phase 3: Logging Configuration
```python
# utils/logging_config.py
import logging
import structlog
from typing import Dict, Any

def setup_logging(log_level: str = "INFO", debug: bool = False) -> None:
    """Configure structured logging for the application"""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
```

### Phase 4: API Integration Logging
```python
# utils/decorators.py
import functools
import time
from typing import Callable, Any
import structlog

def log_api_call(service: str):
    """Decorator to log API calls with timing and error handling"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger = structlog.get_logger()
            start_time = time.time()
            
            logger.info("API call started", 
                       service=service, 
                       function=func.__name__,
                       args_count=len(args),
                       kwargs_keys=list(kwargs.keys()))
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info("API call successful",
                           service=service,
                           function=func.__name__,
                           duration_seconds=duration)
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error("API call failed",
                            service=service,
                            function=func.__name__,
                            duration_seconds=duration,
                            error=str(e),
                            error_type=type(e).__name__)
                raise
        return wrapper
    return decorator
```

### Phase 5: Streamlit Error Handling
```python
# utils/streamlit_error_handler.py
import streamlit as st
import structlog
from typing import Optional, Callable, Any

def handle_streamlit_errors(func: Callable) -> Callable:
    """Decorator for handling errors in Streamlit pages"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger = structlog.get_logger()
        
        try:
            return func(*args, **kwargs)
        except ConfigurationError as e:
            logger.error("Configuration error", error=str(e))
            st.error("⚙️ Configuration Error: Please check your environment setup.")
            st.info("See the documentation for setup instructions.")
        except OpenAIError as e:
            logger.error("OpenAI API error", error=str(e), status_code=e.status_code)
            st.error("🤖 AI Service Error: Unable to generate content at this time.")
            st.info("Please try again in a few moments or check your API credits.")
        except OutlookIntegrationError as e:
            logger.error("Outlook integration error", error=str(e))
            st.error("📧 Email Service Error: Unable to connect to Outlook.")
            st.info("Please check your Outlook integration settings.")
        except Exception as e:
            logger.error("Unexpected error", error=str(e), error_type=type(e).__name__)
            st.error("❌ An unexpected error occurred. Please try again.")
            with st.expander("Technical Details"):
                st.code(f"Error: {str(e)}")
    return wrapper
```

## Files to Add

```
├── utils/
│   ├── __init__.py
│   ├── logging_config.py
│   ├── error_handler.py
│   ├── decorators.py
│   ├── monitoring.py
│   └── streamlit_error_handler.py
├── logs/
│   ├── .gitkeep
│   └── README.md
└── docs/logging-and-monitoring.md
```

## Files to Update

- `requirements.txt` - Add structlog, python-json-logger
- `app.py` - Initialize logging system
- `email_generator/generator.py` - Add error handling and logging
- `email_generator/outlook_integration.py` - Enhanced error handling
- `email_generator/sharepoint_integration.py` - Add logging and error handling
- `learnbot/chatbot.py` - Add comprehensive logging
- `learnbot/rag_pipeline.py` - Add document processing logging
- `pages/1_Workflow.py` - Add error handling
- `pages/2_Learn.py` - Add error handling and logging
- `pages/3_Play.py` - Comprehensive error handling
- `pages/4_Speak.py` - Add error handling
- All test files - Update to work with new logging system

## Testing Requirements

- [ ] Unit tests for custom exception classes
- [ ] Tests for logging decorators
- [ ] Tests for error handling in API calls
- [ ] Integration tests for error scenarios
- [ ] Tests for Streamlit error handling
- [ ] Performance tests for logging overhead

## Monitoring Integration

- [ ] Add health check endpoint for monitoring systems
- [ ] Create metrics for API response times
- [ ] Add alerting for error rate thresholds
- [ ] Implement log aggregation for production deployment

## Definition of Done

- [ ] All modules use structured logging consistently
- [ ] Custom exception classes implemented for all error types
- [ ] User-friendly error messages in all Streamlit pages
- [ ] API calls logged with timing and error information
- [ ] Error correlation IDs for debugging
- [ ] Performance metrics collected
- [ ] Documentation updated with logging guidelines
- [ ] All tests passing with new error handling

## Related Issues

This issue depends on:
- Issue #1: Configuration Management (for log level configuration)

This issue enables:
- Issue #5: Security Improvements (audit logging)
- Better monitoring and observability
- Improved debugging capabilities

## Estimated Effort

**Story Points:** 13
**Time Estimate:** 2-3 weeks
**Complexity:** High (requires refactoring across entire codebase)

---

**Labels:** `critical`, `technical-debt`, `logging`, `error-handling`, `monitoring`, `refactor`
**Assignee:** TBD
**Milestone:** Foundation Improvements v1.0
