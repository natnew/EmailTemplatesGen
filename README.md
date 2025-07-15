# EmailTemplatesGen

This project focuses on automating the generation of email templates using **Natural Language Processing (NLP)**. The solution is designed to be integrated with **Microsoft Outlook** to streamline the process of creating personalized and context-aware email templates, improving efficiency in communication.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Folder Structure](#folder-structure)
3. [Contributing](#contributing)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Outlook Integration and API Key](#outlook-integration-and-api-key)
7. [SharePoint Connectivity](#sharepoint-connectivity)
8. [Development Workflow](#development-workflow)
9. [Collaborators](#collaborators)
10. [License](#license)

## Project Overview

The goal of this project is to reduce the time spent composing repetitive emails by using machine learning and natural language processing techniques to automate the generation of email templates. Key functionalities include:
- **Email template generation** based on contextual data.
- **Customizable email formats** for different purposes (e.g., follow-ups, meeting requests).
- **Reinforcement learning** to improve the email generation based on user feedback.
- Integration with **Microsoft Outlook** via an add-in for seamless usage.

- Centralized template storage using **SharePoint** for easy access.

## Folder Structure

- `app.py` – Streamlit user interface.
- `email_generator/` – Outlook helper utilities.
- `sharepoint_integration.py` – SharePoint file operations.
- `docs/` – Additional documentation.
- `tests/` – Unit tests.

## Contributing

If you'd like to contribute to the project, follow the steps below to get started.

### 1. Fork the Repository

First, you’ll need to **fork** the repository to your GitHub account. A fork creates your own copy of the repository where you can make changes without affecting the original.

1. Navigate to the repository on GitHub: `https://github.com/yourusername/EmailTempGenerationProject`
2. Click the **Fork** button in the upper-right corner of the page to create a copy of the repo under your GitHub account.

### 2. Clone Your Fork

Once you have forked the repository, you need to **clone** it to your local machine:

```bash
git clone https://github.com/yourusername/EmailTempGenerationProject.git
cd EmailTempGenerationProject
```


### Outlook Integration

See [docs/outlook_integration.md](docs/outlook_integration.md) for instructions
on configuring Microsoft Graph credentials and using ``send_email`` to deliver
messages programmatically.

## Installation

Install the project dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

The app now includes a **Workflow** dashboard summarising the notebooks,
a **Play** tab for generating and sending emails through Outlook, and a
template manager backed by SharePoint. The Play tab also offers a few
example templates you can insert and modify before sending.

## Outlook Integration and API Key

Integration with Microsoft Outlook is handled through the Microsoft Graph API.
Use the helper functions in `email_generator/outlook_integration.py` to obtain
an access token via **msal** and send messages directly from a configured
account. Provide your OpenAI API key either through a `secrets.toml` file or the
`OPENAI_API_KEY` environment variable. The app prompts for the key if not
present.

## SharePoint Connectivity

Templates can be stored on SharePoint for team sharing. The module
`sharepoint_integration.py` exposes simple `upload_file` and `download_file`
functions using the **Office365-REST-Python-Client** library. Authenticate with
an app registration and specify the target site and folder to manage template
files.


## Development Workflow

See [docs/roadmap.md](docs/roadmap.md) for planned features. Development occurs on feature branches with pull requests for review.

## Collaborators

- Natasha
- Lana Humphrys

## License

This project is released under the [MIT License](LICENSE).

