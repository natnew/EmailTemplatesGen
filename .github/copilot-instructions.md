# Copilot Instructions

This is a Python-based Streamlit application designed to automate the generation of email templates using Natural Language Processing (NLP) and machine learning techniques. The application integrates with Microsoft Outlook and SharePoint to streamline the process of creating personalized, context-aware email templates, improving efficiency in professional communication workflows.

## Code Standards

### Required Before Each Commit

- [ ] **Code Formatting**: All Python code must be formatted with `black` and follow PEP 8 standards
- [ ] **Type Hints**: Add type hints to all function parameters and return values
- [ ] **Docstrings**: Include docstrings for all classes, methods, and functions using Google-style format
- [ ] **Import Organization**: Organize imports using `isort` - standard library, third-party, then local imports
- [ ] **Error Handling**: Implement proper exception handling with specific error types
- [ ] **Unit Tests**: Write or update tests for new functionality in the `tests/` directory
- [ ] **Linting**: Code must pass `flake8` and `pylint` checks
- [ ] **Security**: No hardcoded API keys, credentials, or sensitive data in code
- [ ] **Documentation**: Update relevant documentation in `docs/` if functionality changes

### Development Flow

1. **Feature Branch**: Create feature branches from `main` following naming convention: `feature/description`
2. **Small Commits**: Make small, logical commits with descriptive messages
3. **Code Review**: All changes require peer review before merging
4. **Testing**: Run full test suite before creating pull requests
5. **Documentation**: Update README.md and relevant docs for user-facing changes

## Repository Structure

```
├── app.py                      # Main Streamlit application entry point
├── pages/                      # Streamlit multipage application structure
│   ├── 1_Workflow.py          # Project workflow visualization
│   ├── 2_Learn.py             # Learning/training interface
│   ├── 3_Play.py              # Email generation playground
│   └── 4_Speak.py             # Voice integration features
├── email_generator/            # Core email generation logic
│   ├── generator.py           # Main template generation engine
│   ├── outlook_integration.py # Microsoft Outlook API integration
│   └── sharepoint_integration.py # SharePoint connectivity
├── learnbot/                   # AI/ML learning components
│   ├── chatbot.py             # Conversational AI interface
│   └── rag_pipeline.py        # Retrieval-Augmented Generation pipeline
├── notebooks/                  # Jupyter notebooks for experimentation
├── data/                       # Data storage and processing
│   ├── raw/                   # Original email data
│   ├── processed/             # Cleaned and processed datasets
│   └── external/              # External data sources
├── models/                     # Trained ML models
├── tests/                      # Unit and integration tests
├── docs/                       # Project documentation
└── config/                     # Configuration files
```

## Key Guidelines

### Code Quality
- **Single Responsibility**: Each function/class should have one clear purpose
- **DRY Principle**: Avoid code duplication; create reusable functions/modules
- **Error Messages**: Provide clear, actionable error messages for users
- **Logging**: Use proper logging levels (DEBUG, INFO, WARNING, ERROR) instead of print statements
- **Constants**: Define magic numbers and strings as named constants

### Streamlit Best Practices
- **Session State**: Use `st.session_state` for maintaining state across interactions
- **Caching**: Implement `@st.cache_data` and `@st.cache_resource` for expensive operations
- **Layout**: Use columns, containers, and expanders for clean UI organization
- **Performance**: Minimize API calls and heavy computations in the main thread

### AI/ML Integration
- **Model Versioning**: Track and version all trained models
- **Data Validation**: Validate input data before processing
- **Prompt Engineering**: Document and version prompt templates
- **Token Management**: Monitor and optimize API token usage for LLM calls

### Security & Privacy
- **Environment Variables**: Store all secrets in `.env` files (never commit)
- **Data Protection**: Implement proper data sanitization for email content
- **API Rate Limits**: Respect Microsoft Graph API rate limits
- **Access Control**: Implement proper authentication and authorization

### Integration Guidelines
- **Outlook Integration**: Follow Microsoft Graph API best practices
- **SharePoint**: Use proper authentication and handle connection failures gracefully
- **Voice Features**: Ensure audio processing is efficient and user-friendly
- **Cross-Platform**: Code should work across Windows, macOS, and Linux

### Testing Strategy
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test API integrations with mock responses
- **UI Tests**: Test Streamlit components and user workflows
- **Data Tests**: Validate data processing and model outputs
