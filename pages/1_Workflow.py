import os
import sys

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sidebar import init_sidebar

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
    "Data Preparation",
    "Model Training",
    "Evaluation",
    "Email Generation",
]

tabs = st.tabs(steps)

with tabs[0]:
    st.markdown(
        "The *01_data_preprocessing* notebooks clean raw emails and extract fields."
        " You can inspect them in the `notebooks/` folder."
    )

with tabs[1]:
    st.markdown(
        "The *03_model_training* notebooks fine‑tune language models on the"
        " prepared dataset to learn common structures and tones."
    )

with tabs[2]:
    st.markdown(
        "The *04_model_evaluation* notebooks compare different runs and measure"
        " how well the generated templates match expectations."
    )

with tabs[3]:
    st.markdown(
        "Use the **Play** tab to create templates and send them via Outlook."
        " SharePoint integration lets you store reusable drafts."
    )
