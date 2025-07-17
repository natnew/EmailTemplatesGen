# Issue #1: Implement Proper Configuration Management and Environment Setup

## 🔴 Priority: Critical

## Problem Statement

The project currently lacks a centralized configuration system and proper environment variable management. This creates several issues:

- API keys and secrets are handled inconsistently across the codebase
- Environment variables are hardcoded with no validation
- No `.env` file support or configuration templates
- Poor error messages when configuration is missing or invalid
- Security risks from exposed credentials in UI components
- Difficult deployment and environment setup

## Current Issues in Codebase

### Files with Configuration Problems:
- `email_generator/outlook_integration.py` - Direct `os.getenv()` calls with no validation
- `pages/3_Play.py` - API key input via Streamlit sidebar (security risk)
- `learnbot/chatbot.py` - API key passed as parameter instead of configured centrally
- Missing `.env` file and configuration validation

### Examples of Current Problems:
```python
# email_generator/outlook_integration.py - Lines 12-16
CLIENT_ID = os.getenv("OUTLOOK_CLIENT_ID")
TENANT_ID = os.getenv("OUTLOOK_TENANT_ID") 
CLIENT_SECRET = os.getenv("OUTLOOK_CLIENT_SECRET")
SENDER_ADDRESS = os.getenv("OUTLOOK_SENDER")
# No validation, fails silently if missing
```

```python
# pages/3_Play.py - Lines 35-38
openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
if not openai_api_key:
    st.warning("Please enter your OpenAI API key in the sidebar.")
# Security risk - API key in UI, no persistence
```

## Acceptance Criteria

### ✅ Core Configuration System
- [ ] Create Pydantic-based settings class with validation
- [ ] Implement `.env` file support with python-dotenv
- [ ] Add configuration validation on application startup
- [ ] Create environment-specific configuration (dev, staging, prod)
- [ ] Implement secure credential loading from multiple sources

### ✅ API Key Management
- [ ] Centralize all API key configuration (OpenAI, Microsoft Graph, SharePoint)
- [ ] Remove API key input from Streamlit UI
- [ ] Add proper credential validation and error handling
- [ ] Implement configuration caching for performance

### ✅ Documentation and Templates
- [ ] Create `.env.example` with all required variables
- [ ] Add configuration documentation in `docs/configuration.md`
- [ ] Update setup instructions with environment configuration
- [ ] Add troubleshooting guide for common configuration issues

### ✅ Error Handling
- [ ] Implement clear error messages for missing configuration
- [ ] Add validation for required vs optional settings
- [ ] Create configuration health check endpoint/function
- [ ] Add graceful degradation for optional services

## Implementation Plan

### Phase 1: Core Configuration Framework
1. **Create configuration module**
   ```
   config/
   ├── __init__.py
   ├── settings.py          # Pydantic settings classes
   ├── validation.py        # Configuration validation logic
   └── environments.py      # Environment-specific configs
   ```

2. **Add dependencies**
   ```bash
   pip install pydantic-settings python-dotenv
   ```

### Phase 2: Implement Settings Classes
```python
# config/settings.py
from pydantic import BaseSettings, validator
from typing import Optional

class OpenAISettings(BaseSettings):
    api_key: str
    model: str = "gpt-4"
    max_tokens: int = 2000
    
    class Config:
        env_prefix = "OPENAI_"

class OutlookSettings(BaseSettings):
    client_id: str
    tenant_id: str
    client_secret: str
    sender_address: str
    
    class Config:
        env_prefix = "OUTLOOK_"

class AppSettings(BaseSettings):
    openai: OpenAISettings
    outlook: OutlookSettings
    debug: bool = False
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
```

### Phase 3: Update Existing Modules
- Refactor `email_generator/outlook_integration.py` to use settings
- Update `pages/3_Play.py` to remove API key input
- Modify `learnbot/chatbot.py` to use centralized configuration
- Update `app.py` to initialize and validate configuration

### Phase 4: Environment Setup
- Create `.env.example` template
- Add configuration validation to startup
- Update documentation and setup instructions

## Files to Add

```
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── validation.py
│   └── environments.py
├── .env.example
├── docs/configuration.md
└── utils/config_loader.py
```

## Files to Update

- `requirements.txt` - Add pydantic-settings, python-dotenv
- `app.py` - Initialize configuration system
- `email_generator/outlook_integration.py` - Use centralized settings
- `email_generator/sharepoint_integration.py` - Use centralized settings
- `learnbot/chatbot.py` - Remove API key parameters
- `pages/3_Play.py` - Remove API key input, use config
- `pages/2_Learn.py` - Update to use centralized config
- `pages/4_Speak.py` - Update to use centralized config
- All test files - Update to work with new configuration system

## Testing Requirements

- [ ] Unit tests for configuration validation
- [ ] Tests for missing environment variables
- [ ] Tests for invalid configuration values
- [ ] Integration tests with mocked environment variables
- [ ] Tests for configuration error handling

## Definition of Done

- [ ] All API keys and secrets managed through centralized configuration
- [ ] No hardcoded environment variable access in application code
- [ ] Configuration validation prevents startup with invalid settings
- [ ] Clear error messages for configuration issues
- [ ] Documentation updated with setup instructions
- [ ] All tests passing with new configuration system
- [ ] Security review completed for credential handling

## Related Issues

This issue is a prerequisite for:
- Issue #2: Logging and Error Handling (needs config for log levels)
- Issue #5: Security Improvements (proper credential management)
- Deployment and CI/CD improvements

## Estimated Effort

**Story Points:** 8
**Time Estimate:** 1-2 weeks
**Complexity:** Medium-High (requires refactoring existing code)

---

**Labels:** `critical`, `technical-debt`, `security`, `configuration`, `refactor`
**Assignee:** TBD
**Milestone:** Foundation Improvements v1.0
