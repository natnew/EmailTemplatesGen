# Issue #3: Fix Project Structure and Import Management

## 🔴 Priority: Critical

## Problem Statement

The EmailTemplatesGen project suffers from inconsistent project structure and poor import management, creating maintenance headaches and potential runtime issues:

- **Duplicate modules**: `sharepoint_integration.py` exists in both root and `email_generator/` directories
- **Import hacks**: Multiple files use `sys.path.append()` to manipulate the Python path
- **Inconsistent structure**: Mix of package-style and script-style organization
- **Missing package configuration**: No `pyproject.toml` or proper package setup
- **Import conflicts**: Potential for importing wrong versions of modules
- **Poor maintainability**: Difficult to refactor or reorganize code

## Current Issues in Codebase

### Duplicate Files:
- `sharepoint_integration.py` (root directory)
- `email_generator/sharepoint_integration.py` (package directory)

### Files with Import Hacks:
```python
# pages/1_Workflow.py - Lines 5-6
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sidebar import init_sidebar

# pages/3_Play.py - Lines 12-13
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sidebar import init_sidebar

# tests/test_email_generator.py - Lines 25-26
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
monkeypatch.setitem(sys.modules, 'openai', setup_fake_openai())
```

### Missing Package Structure:
- No `pyproject.toml` for modern Python package management
- Inconsistent `__init__.py` files
- No proper package imports/exports
- Missing development tools configuration

## Acceptance Criteria

### ✅ Clean Project Structure
- [ ] Remove duplicate `sharepoint_integration.py` files (keep one canonical version)
- [ ] Establish clear separation between application code and utilities
- [ ] Create proper package hierarchy with meaningful organization
- [ ] Implement consistent `__init__.py` files with proper exports

### ✅ Modern Python Package Setup
- [ ] Create `pyproject.toml` with project metadata and build configuration
- [ ] Add proper package discovery and installation
- [ ] Configure development tools (black, isort, flake8, mypy) in pyproject.toml
- [ ] Implement editable installation for development

### ✅ Fix Import Management
- [ ] Remove all `sys.path.append()` and `sys.path.insert()` hacks
- [ ] Implement proper relative and absolute imports
- [ ] Create consistent import patterns across all modules
- [ ] Add proper package-level imports

### ✅ Development Tools Configuration
- [ ] Configure black for code formatting
- [ ] Set up isort for import sorting
- [ ] Configure flake8 for linting
- [ ] Set up mypy for type checking
- [ ] Add pre-commit hooks for code quality

### ✅ Testing Infrastructure
- [ ] Update test structure to work with proper package imports
- [ ] Remove import manipulation from test files
- [ ] Add proper test discovery configuration
- [ ] Implement test utilities and fixtures

## Implementation Plan

### Phase 1: Analyze and Plan Structure
1. **Audit current modules and dependencies**
   ```bash
   # Find duplicate files
   find . -name "*.py" -exec basename {} \; | sort | uniq -d
   
   # Find sys.path manipulations
   grep -r "sys.path" --include="*.py" .
   ```

2. **Design new structure**
   ```
   EmailTemplatesGen/
   ├── pyproject.toml
   ├── README.md
   ├── requirements.txt
   ├── src/
   │   └── email_templates_gen/
   │       ├── __init__.py
   │       ├── config/
   │       ├── email_generator/
   │       ├── learnbot/
   │       ├── integrations/
   │       │   ├── __init__.py
   │       │   ├── outlook.py
   │       │   └── sharepoint.py
   │       ├── ui/
   │       │   ├── __init__.py
   │       │   ├── pages/
   │       │   └── components/
   │       └── utils/
   ├── tests/
   ├── docs/
   └── data/
   ```

### Phase 2: Create Modern Package Configuration
```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "email-templates-gen"
version = "0.1.0"
description = "AI-powered email template generation with Outlook and SharePoint integration"
readme = "README.md"
requires-python = ">=3.9"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["email", "ai", "nlp", "outlook", "sharepoint", "streamlit"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]

dependencies = [
    "streamlit>=1.32.0",
    "openai>=1.13.3",
    "msal>=1.25.0",
    "requests>=2.31",
    "langchain>=0.1.9",
    "faiss-cpu",
    "tiktoken",
    "python-dotenv",
    "pydub",
    "openai-whisper",
    "streamlit-webrtc>=0.46",
    "soundfile>=0.12",
    "av>=12.0.0",
    "numpy>=1.26",
    "langchain-core>=0.2.0",
    "langchain-community>=0.2.0",
    "langchain-openai>=0.1.0",
    "Office365-REST-Python-Client>=2.5.0",
    "pydantic-settings",
    "structlog",
    "python-json-logger",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
]

[project.urls]
Homepage = "https://github.com/natnew/EmailTemplatesGen"
Repository = "https://github.com/natnew/EmailTemplatesGen"
Issues = "https://github.com/natnew/EmailTemplatesGen/issues"

[project.scripts]
email-templates-gen = "email_templates_gen.app:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'

[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3

[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

### Phase 3: Restructure Project
1. **Create new directory structure**
   ```bash
   mkdir -p src/email_templates_gen/{config,integrations,ui/pages,ui/components,utils}
   ```

2. **Move and consolidate files**
   ```bash
   # Move email_generator to src/email_templates_gen/
   mv email_generator src/email_templates_gen/
   
   # Move learnbot to src/email_templates_gen/
   mv learnbot src/email_templates_gen/
   
   # Consolidate sharepoint integration
   mv email_generator/sharepoint_integration.py src/email_templates_gen/integrations/sharepoint.py
   rm sharepoint_integration.py  # Remove duplicate
   
   # Move Streamlit pages
   mv pages src/email_templates_gen/ui/
   mv sidebar.py src/email_templates_gen/ui/components/
   ```

3. **Update all import statements**

### Phase 4: Fix Imports
```python
# src/email_templates_gen/ui/pages/workflow.py
import streamlit as st
from email_templates_gen.ui.components.sidebar import init_sidebar

# src/email_templates_gen/ui/pages/play.py
import streamlit as st
from email_templates_gen.email_generator.generator import stream_generated_email
from email_templates_gen.integrations.outlook import send_email
from email_templates_gen.integrations.sharepoint import download_template, upload_template
from email_templates_gen.ui.components.sidebar import init_sidebar

# src/email_templates_gen/__init__.py
"""EmailTemplatesGen - AI-powered email template generation."""

__version__ = "0.1.0"

from email_templates_gen.email_generator import generator
from email_templates_gen.integrations import outlook, sharepoint
from email_templates_gen.learnbot import chatbot, rag_pipeline

__all__ = [
    "generator",
    "outlook", 
    "sharepoint",
    "chatbot",
    "rag_pipeline",
]
```

### Phase 5: Update Application Entry Point
```python
# src/email_templates_gen/app.py
"""Main Streamlit application entry point."""
import streamlit as st
from email_templates_gen.config.settings import AppSettings
from email_templates_gen.utils.logging_config import setup_logging

def main():
    """Initialize and run the Streamlit application."""
    # Load configuration
    settings = AppSettings()
    
    # Setup logging
    setup_logging(settings.log_level, settings.debug)
    
    # Configure Streamlit
    st.set_page_config(
        page_title="EmailTemplatesGen",
        page_icon="📧",
        layout="wide"
    )
    
    # Redirect to workflow page
    st.switch_page("src/email_templates_gen/ui/pages/workflow.py")

if __name__ == "__main__":
    main()
```

### Phase 6: Update Tests
```python
# tests/test_email_generator.py
import pytest
from email_templates_gen.email_generator.generator import stream_generated_email

def test_stream_generated_email_yields_tokens():
    """Test that email generation yields tokens properly."""
    # No more sys.path manipulation needed
    tokens = list(stream_generated_email('input', 'Friendly', 'purpose', 'key'))
    assert len(tokens) > 0
```

## Files to Add

```
├── pyproject.toml
├── src/
│   └── email_templates_gen/
│       ├── __init__.py
│       ├── app.py
│       ├── config/
│       │   └── __init__.py
│       ├── integrations/
│       │   ├── __init__.py
│       │   ├── outlook.py
│       │   └── sharepoint.py
│       ├── ui/
│       │   ├── __init__.py
│       │   ├── components/
│       │   │   ├── __init__.py
│       │   │   └── sidebar.py
│       │   └── pages/
│       │       ├── __init__.py
│       │       ├── workflow.py
│       │       ├── learn.py
│       │       ├── play.py
│       │       └── speak.py
│       └── utils/
│           └── __init__.py
├── .pre-commit-config.yaml
└── setup.cfg
```

## Files to Remove

- `sharepoint_integration.py` (duplicate in root)
- All `sys.path` manipulation code

## Files to Move/Update

- Move `email_generator/` → `src/email_templates_gen/email_generator/`
- Move `learnbot/` → `src/email_templates_gen/learnbot/`
- Move `pages/` → `src/email_templates_gen/ui/pages/`
- Move `sidebar.py` → `src/email_templates_gen/ui/components/sidebar.py`
- Update all import statements in all Python files
- Update all test files to use proper imports

## Testing Requirements

- [ ] All tests pass with new import structure
- [ ] Package can be installed in development mode (`pip install -e .`)
- [ ] All modules can be imported without sys.path manipulation
- [ ] Import statements follow consistent patterns
- [ ] No circular import issues

## Development Workflow

1. **Install in development mode**
   ```bash
   pip install -e .
   pip install -e ".[dev]"
   ```

2. **Run development tools**
   ```bash
   black src/ tests/
   isort src/ tests/
   flake8 src/ tests/
   mypy src/
   pytest tests/
   ```

3. **Pre-commit hooks**
   ```bash
   pre-commit install
   pre-commit run --all-files
   ```

## Definition of Done

- [ ] No duplicate modules in the codebase
- [ ] All `sys.path` manipulations removed
- [ ] Modern `pyproject.toml` configuration
- [ ] Consistent import patterns across all files
- [ ] Package can be installed and imported properly
- [ ] All tests pass with new structure
- [ ] Development tools configured and working
- [ ] Documentation updated with new structure
- [ ] Pre-commit hooks configured

## Related Issues

This issue is a prerequisite for:
- Issue #1: Configuration Management (cleaner config module structure)
- Issue #2: Logging Framework (better logging module organization)
- Future refactoring and feature development

## Estimated Effort

**Story Points:** 21
**Time Estimate:** 3-4 weeks
**Complexity:** Very High (requires careful coordination and testing)

---

**Labels:** `critical`, `technical-debt`, `refactor`, `project-structure`, `imports`
**Assignee:** TBD
**Milestone:** Foundation Improvements v1.0
