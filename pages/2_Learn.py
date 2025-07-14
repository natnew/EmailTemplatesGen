import streamlit as st
from learnbot.chatbot import stream_answer_from_docs
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Learn About the Project", layout="wide")

_, col, _ = st.columns([1, 3, 1])

with col:
    st.title("🧠 Learn About This Project")
    st.markdown("#### Curious about how this was built? Ask the AI anything about the design, stack or roadmap.")

    st.sidebar.title("🔐 API Key")
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

    if not openai_api_key:
        st.warning("Please enter your OpenAI API key in the sidebar.")
        st.stop()

    st.markdown("##### Try asking one of these:")

    suggestions = [
        "How do I set up the project locally?",
        "What are the latest updates to the project?",
        "How does the email generation work?",
        "Where should I start exploring the code?",
    ]

    cols = st.columns(len(suggestions))
    for col, prompt in zip(cols, suggestions):
        if col.button(prompt, use_container_width=True):
            st.session_state.learn_query = prompt
            st.experimental_rerun()

    query = st.text_input(
        "Ask something about the project...",
        placeholder="e.g. How does the email generation work?",
        key="learn_query",
    )

    if query:
        st.info("🔍 Thinking...")
        st.write_stream(stream_answer_from_docs(query, openai_api_key=openai_api_key))
    else:
        st.info("Ask the AI about how this project works, what tech it's using, or what's planned next.")
