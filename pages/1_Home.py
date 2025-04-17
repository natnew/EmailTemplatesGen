import streamlit as st

st.set_page_config(page_title="Email Template Generator", layout="wide")

# Center all elements using columns
_, col, _ = st.columns([1, 3, 1])

with col:
    st.markdown("<h1 style='text-align: center;'>📧 Email Template Generator</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Make your own custom email in a few simple steps!</h3>", unsafe_allow_html=True)

    st.info("""Welcome to the Email Template Generator Project. 👋 This app shows what we're working on or have
    planned for the future. Plus, there's always more going on behind the scenes — we
    sometimes like to surprise you ✨""", icon="🗺")

    st.success(
    """
    Read [the blog post on Streamlit's roadmap](https://blog.streamlit.io/the-next-frontier-for-streamlit/)
    to understand our broader vision.
    """,
    icon="🗺",)

    st.divider()

    with st.expander("🔍 What is this project?"):
        st.markdown("""
        This tool helps colleagues create professional, well-structured email templates with the help of AI.
        
        Whether you're replying to a complex message or starting from scratch, this assistant adapts to your tone and context — and it's built to work seamlessly with Outlook.

        The goal? Less typing, more clarity, and fewer 'drafts you'll never send.'
        """)

    with st.expander("🧠 How does it work?"):
        st.markdown("""
        - Built using **Streamlit**, **OpenAI GPT-4**, and optionally **Whisper** for voice.
        - Uses **prompt engineering** to guide structure, tone, and clarity.
        - The Learn page uses **RAG (Retrieval-Augmented Generation)** to help you explore the project's design via a chatbot.
        - Outlook integration is coming — right now you can export or send test emails.
        """)

    with st.expander("🛣️ Roadmap"):
        st.markdown("""
        | Stage       | Feature                              | Status  |
        |-------------|--------------------------------------|---------|
        | POC         | Email template generation            | ✅ Done |
        | MVP         | Email template generation            | ✅ Done |
        | Phase 2     | AI project explainer via chatbot     | ✅ Done |
        | Phase 3     | Outlook integration (OAuth & send)   | 🔄 In Progress |
        | Phase 4     | Voice assistant interface            | 🧪 Experimental |
        | Future      | Team tone profiles, history tracking | 🧠 Planned |
        """)
