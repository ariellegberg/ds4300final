import streamlit as st
from streamlit.logger import get_logger
from streamlit_extras.switch_page_button import switch_page
from pathlib import Path

import time
import os
LOGGER = get_logger(__name__)




if __name__ == "__main__":
    st.write("## Arielle and Ella's DS4300 Final Project")

    tik_tok_username =st.text_input('Enter Your Tik Tok Username', key='tik_tok')
    upload = st.button('Upload Video')
    if upload:
        switch_page('upload_file')
    time.sleep(1)