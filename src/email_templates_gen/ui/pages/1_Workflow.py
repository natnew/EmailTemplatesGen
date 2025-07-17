"""Workflow page - Project workflow visualization."""

import streamlit as st
from email_templates_gen.ui.components.sidebar import init_sidebar

st.set_page_config(page_title="Workflow", layout="wide")

init_sidebar(
    "Explore the step-by-step process used to build and test the email generator."
)

st.title("📊 Project Workflow")

st.markdown(
    "This guided tour summarises the notebooks that train and evaluate the models"
    " used for template generation. Each tab provides a short description so you"
    " can follow the entire pipeline from data to email delivery."
)

steps = [
    {
        "title": "Data Preparation",
        "image": "../../../images/Sample_Data_EDA_BarChart_Category_001.png",
        "text": (
            "The *01_data_preprocessing* notebooks clean raw emails and extract "
            "fields. You can inspect them in the `notebooks/` folder."
        ),
    },
    {
        "title": "Model Training",
        "image": "../../../images/Sample_Data_EDA_WordCloud_001.png",
        "text": (
            "The *03_model_training* notebooks fine‑tune language models on the "
            "prepared dataset to learn common structures and tones."
        ),
    },
    {
        "title": "Evaluation",
        "image": "../../../images/Sample_Data_EDA_BarChart_Category_001.png",
        "text": (
            "The *04_model_evaluation* notebooks compare different runs and "
            "measure how well the generated templates match expectations."
        ),
    },
    {
        "title": "Email Generation",
        "image": "../../../images/Sample_Data_EDA_WordCloud_001.png",
        "text": (
            "Use the **Play** tab to create templates and send them via Outlook. "
            "SharePoint integration lets you store reusable drafts."
        ),
    },
]

tabs = st.tabs([step["title"] for step in steps])

for tab, step in zip(tabs, steps):
    with tab:
        with st.expander("See details", expanded=True):
            st.image(step["image"], use_column_width=True)
            st.write(step["text"])
