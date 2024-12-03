import streamlit as st
from streamlit.logger import get_logger
from pathlib import Path
import os
LOGGER = get_logger(__name__)

if __name__ == "__main__":
    option = st.selectbox(
        "Choose what type of Tweets you want to see",
        ("Positive", "Negative", "Neutral", "All"),
        key='option'
    )
