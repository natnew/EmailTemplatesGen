import streamlit as st
from email_generator.generator import stream_generated_email
import sys
import os

# Ensure access to project root modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Page setup
st.set_page_config(page_title="Play – Generate Email", layout="wide")

# Centre the layout
_, col, _ = st.columns([1, 3, 1])

with col:
    st.title("📝 Generate an Email Template")
    st.markdown("#### Paste an email you’ve received, or describe the situation. The AI will draft a reply for you.")

    # Sidebar for API key input
    st.sidebar.title("🔐 API Key")
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

    if not openai_api_key:
        st.warning("Please enter your OpenAI API key in the sidebar.")
        st.stop()

    # Input section
    input_mode = st.radio("Choose input method", ["Paste an email", "Describe the situation"])

    if input_mode == "Paste an email":
        input_text = st.text_area("Paste the email you received:", height=200)
    else:
        input_text = st.text_area("Describe what the email should say or respond to:", height=200)

    tone = st.selectbox("Choose tone", ["Professional", "Friendly", "Neutral", "Assertive"])
    purpose = st.selectbox("Email type", ["Reply", "Follow-up", "Request", "Information", "Other"])

    # Generate button with streaming output
    if st.button("Generate Email"):
        if not input_text.strip():
            st.warning("Please enter some text.")
        else:
            st.info("✍️ Generating your email...")
            st.write_stream(stream_generated_email(input_text, tone, purpose, openai_api_key=openai_api_key))
