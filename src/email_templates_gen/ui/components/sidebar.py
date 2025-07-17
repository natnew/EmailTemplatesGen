"""Shared Streamlit UI components."""

import streamlit as st

PROJECT_DESCRIPTION = (
    "Email Template Generator is a Streamlit application that demonstrates an end-to-end workflow "
    "for creating email response templates using large language models. It guides you through data "
    "preparation, model training, evaluation and deployment. Example pages let you ask questions, "
    "generate drafts and even speak with the project mentor in real time."
)

ICON_URL = "https://streamlit.io/images/brand/streamlit-mark-color.png"


def init_sidebar(page_info: str) -> None:
    """Render the shared sidebar with project description."""
    with st.sidebar:
        st.image(ICON_URL, width=30)
        st.title("Email Template Generator")
        st.markdown(PROJECT_DESCRIPTION)
        st.markdown(f"**{page_info}**")
        st.markdown("---")
