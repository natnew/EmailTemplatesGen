import streamlit as st

st.set_page_config(page_title="Speak – Digital Human", layout="wide")

_, col, _ = st.columns([1, 3, 1])

with col:
    st.title("🗣️ Speak with our Digital Human Assistant!")
    st.markdown("""
    Interact directly with our intelligent, lifelike Digital Human powered by NVIDIA's state-of-the-art generative AI. 
    Ask questions, discuss email templates, and get insightful responses in real-time!
    """)

    # Embed the digital human via iframe
    digital_human_url = "https://your-digital-human-url.com"  # replace with actual URL
    
    st.components.v1.iframe(digital_human_url, height=700, scrolling=True)
