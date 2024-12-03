import streamlit as st
from streamlit.logger import get_logger
from pathlib import Path
import os

LOGGER = get_logger(__name__)

if __name__ == "__main__":
    st.write("## Please Upload Your Tweet Here")

    tweet= st.text_input("Tweet something!")
    submit = st.button('Post Your Tweet!')
    if submit:
        st.switch_page('pages/twitter_feed.py')
