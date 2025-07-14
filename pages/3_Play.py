import os
import sys
import tempfile
from pathlib import Path

import streamlit as st

from email_generator.generator import stream_generated_email
from email_generator.outlook_integration import send_email
from email_generator.sharepoint_integration import download_template, upload_template

# Ensure access to project root modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sidebar import init_sidebar

# Page setup
st.set_page_config(page_title="Play – Generate Email", layout="wide")

init_sidebar(
    "Generate personalized email drafts and manage templates with Outlook and SharePoint."
)

# Centre the layout
_, col, _ = st.columns([1, 3, 1])

with col:
    st.title("📝 Generate an Email Template")
    st.markdown(
        "#### Paste an email you’ve received, or describe the situation. The AI will draft a reply for you."
    )

    # Sidebar for API key input
    st.sidebar.title("🔐 API Key")
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

    if not openai_api_key:
        st.warning("Please enter your OpenAI API key in the sidebar.")
        st.stop()

    # Input section
    input_mode = st.radio(
        "Choose input method", ["Paste an email", "Describe the situation"]
    )

    if input_mode == "Paste an email":
        input_text = st.text_area("Paste the email you received:", height=200)
    else:
        input_text = st.text_area(
            "Describe what the email should say or respond to:", height=200
        )

    tone = st.selectbox(
        "Choose tone", ["Professional", "Friendly", "Neutral", "Assertive"]
    )
    purpose = st.selectbox(
        "Email type", ["Reply", "Follow-up", "Request", "Information", "Other"]
    )

    EXAMPLE_TEMPLATES = {
        "Meeting Invitation": "Hi NAME,\n\nI'd like to invite you to a meeting on DATE at TIME to discuss our next steps.",
        "Project Update": "Hello NAME,\n\nHere is a brief update on the project status...",
        "Thank You": "Dear NAME,\n\nThank you for your assistance with the recent task."
    }
    example_choice = st.selectbox(
        "Or pick an example template",
        ["None"] + list(EXAMPLE_TEMPLATES.keys()),
    )
    if example_choice != "None":
        st.session_state.generated_email = EXAMPLE_TEMPLATES[example_choice]

    # Generate button with streaming output
    if st.button("Generate Email"):
        if not input_text.strip():
            st.warning("Please enter some text.")
        else:
            st.info("✍️ Generating your email...")
            tokens = []
            placeholder = st.empty()
            for token in stream_generated_email(
                input_text, tone, purpose, openai_api_key=openai_api_key
            ):
                tokens.append(token)
                placeholder.markdown("".join(tokens))
            st.session_state.generated_email = "".join(tokens)

    generated = st.session_state.get("generated_email")
    if generated:
        st.markdown("### Draft")
        st.text_area("Email body", value=generated, height=200, key="draft_area")
        recipient = st.text_input("Recipient")
        subject = st.text_input("Subject")
        if st.button("Send via Outlook"):
            if not recipient or not subject:
                st.warning("Please enter recipient and subject")
            else:
                with st.spinner("Sending email..."):
                    send_email(recipient=recipient, subject=subject, body=generated)
                st.success("Email sent")

        with st.expander("SharePoint Template Management"):
            site_url = st.text_input("Site URL")
            folder_url = st.text_input("Folder URL")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Save Template"):
                if not all([site_url, folder_url, username, password]):
                    st.warning("Please fill in SharePoint details")
                else:
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".html"
                    ) as tmp:
                        tmp.write(generated.encode())
                        tmp_path = Path(tmp.name)
                    with st.spinner("Uploading..."):
                        url = upload_template(
                            site_url, folder_url, tmp_path, username, password
                        )
                    st.success(f"Saved to {url}")

            file_url = st.text_input("File URL")
            if st.button("Load Template"):
                if not all([site_url, file_url, username, password]):
                    st.warning("Please fill in SharePoint details")
                else:
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".html"
                    ) as tmp:
                        dest = Path(tmp.name)
                    with st.spinner("Downloading..."):
                        download_template(site_url, file_url, dest, username, password)
                        st.session_state.generated_email = dest.read_text()
                    st.experimental_rerun()
